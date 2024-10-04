"""
Author: nagan319
Date: 2024/06/23
"""

import os
import enum
from collections import defaultdict
from typing import Union, Tuple, List
import numpy as np

from sqlalchemy.orm import Session

from ..models.router_model import Router
from ..models.plate_model import Plate
from ..models.part_model import Part
from ..models.utils import deserialize_array, deserialize_array_list, serialize_array, serialize_array_list

from ..utils.packing.bin import Bin
from ..utils.packing.utils.area2d import Area2D
from ..utils.packing.utils.dimension2d import Dimension2D
from ..utils.packing.packing_algo import execute_packing_algorithm

from ..logging import logger

import matplotlib.pyplot as plt

class OptimizationController:
    """
    Controller for managing layout optimization. 
    ### Parameters:
    - session: working session.
    - preview_path: preview image filename
    """
    MIN_QUANTIZED_VALUE: float = .01 
    ID_AMOUNT_DELIMITER = "__"

    def __init__(self, session: Session, preview_path: str, conversion_factor: float = 1.0):
        if not os.path.exists(os.path.dirname(preview_path)):
            logger.error(f"Indicated optimization preview directory path does not exist: {preview_path}")
            raise FileNotFoundError(f"Directory not found: {preview_path}")

        self.session = session
        self.preview_path = preview_path
        self.conversion_factor = conversion_factor

        self.routers_orm, self.parts_orm, self.plates_orm = None, None, None
        self.placements = None

    def optimize(self):
        """ Call optimization algorithm and generate layout using selected plates, parts, and routers. """

        selected_routers: List[Router] = self._get_selected_routers()
        if selected_routers is None:
            raise ValueError("No routers selected.")

        imported_parts: List[Part] = self._get_imported_parts()
        if imported_parts is None:
            raise ValueError("No parts selected.")

        part_thicknesses = defaultdict(list)
        part_materials = defaultdict(list)

        for part in imported_parts:
            material = part.material.lower().strip()
            thickness = OptimizationController._quantize_val(part.thickness)
            part_materials[material].append(part)
            part_thicknesses[thickness].append(part)

        if len(part_materials) == 0 or len(part_thicknesses) == 0:
            raise ValueError("Import parts before attempting to generate a layout.")
        elif len(part_materials) > 1 or len(part_thicknesses) > 1:
            raise ValueError("All imported parts must be of same thickness and material.")

        selected_plates: List[Plate] = self._get_selected_plates()
        if selected_plates is None:
            raise ValueError("No plates selected.")
        
        plate_thicknesses = defaultdict(list)
        plate_materials = defaultdict(list)

        for plate in selected_plates:
            material = plate.material.lower().strip()
            thickness = OptimizationController._quantize_val(plate.z)
            plate_materials[material].append(plate)
            plate_thicknesses[thickness].append(plate)

        if len(plate_materials) != 1 or len(plate_thicknesses) != 1:
            raise ValueError("All imported plates must be of same thickness and material.")
        
        if list(plate_thicknesses.keys())[0] != list(part_thicknesses.keys())[0]:
            raise ValueError("Imported part and plate thicknesses do not match.")      
        if list(plate_materials.keys())[0] != list(part_materials.keys())[0]:
            raise ValueError("Imported part and plate materials do not match.")    

        self.routers_orm = selected_routers 
        self.parts_orm = imported_parts
        self.plates_orm = selected_plates 

        mill_bit_diameter = max([router.mill_bit_diameter for router in self.routers_orm])
        drill_bit_diameter = max([router.drill_bit_diameter for router in self.routers_orm])
        max_bit_diameter = max(drill_bit_diameter, mill_bit_diameter)

        edge_distance = max([router.min_safe_dist_from_edge for router in self.routers_orm])

        router_sizes = [(router.plate_x, router.plate_y) for router in self.routers_orm]
        max_plate_x = min(router_sizes, key=lambda size: size[0])[0]
        max_plate_y = min(router_sizes, key=lambda size: size[1])[1]

        plates = []

        for plate in self.plates_orm:
            if plate.x <= max_plate_x and plate.y <= max_plate_y:
                contour_list = OptimizationController._get_formatted_plate_ctrs(plate)
                plates.append((plate.id, (plate.x, plate.y), contour_list))

        if len(plates) == 0:
            raise ValueError("Selected plates exceed maximum size of selected router.")

        parts = []

        for part in self.parts_orm:
            part_id = part.id
            amount = part.amount
            contour = OptimizationController._get_formatted_part_ctr(part)
            for i in range(amount):
                parts.append((OptimizationController._get_part_id_with_amt(part_id, i), contour))

        self.placements = execute_packing_algorithm(
            plates, 
            parts, 
            max_bit_diameter, 
            edge_distance,
            self.preview_path, 
            self.conversion_factor
        )

    def save_layout(self) -> Tuple[set, set]:
        """ Save generated layout to database. Returns tuple of used pieces and used bins. """
        if self.placements is None:
            return

        used_pieces = set()
        used_bins = set()

        for piece_id, placement in self.placements.items():
            if 'edge' in piece_id or 'ctr' in piece_id:
                continue

            stripped_id = OptimizationController._strip_amt_part_id(piece_id)
            used_pieces.add(piece_id)

            bin_id, coordinates = placement
            delta_x, delta_y = coordinates

            used_bins.add(bin_id)

            used_part = self.session.query(Part).filter(Part.id == stripped_id).all()[0]
            used_part_contour = OptimizationController._get_formatted_part_ctr(used_part)

            used_plate = self.session.query(Plate).filter(Plate.id == bin_id).all()[0]
            used_plate_contours = OptimizationController._get_formatted_plate_ctrs(used_plate)

            shifted_contour = []

            for point in used_part_contour:
                shifted_contour.append((int(point[0] + delta_x), int(point[1] + delta_y)))

            used_plate_contours.append(shifted_contour)

            setattr(
                used_plate, 
                'contours', 
                OptimizationController._get_reverted_plate_ctrs(used_plate_contours)
            )
            self.session.commit()
        
        return (used_pieces, used_bins)

    """ Part ID handling """

    @staticmethod
    def _get_part_id_with_amt(part_id: str, particular_part_idx: int) -> str:
        """ Get part id in the case of multiple imported parts. """
        return part_id + OptimizationController.ID_AMOUNT_DELIMITER + str(particular_part_idx)

    @staticmethod
    def _strip_amt_part_id(id_w_amount: str) -> str:
        """ Split amount from part ID """
        return id_w_amount.split(OptimizationController.ID_AMOUNT_DELIMITER)[0]

    """ Contour retrieval and formatting """ 

    @staticmethod
    def _get_formatted_plate_ctrs(plate: Plate) -> List[List[Tuple[float, float]]]:
        """ Get properly formatted contour list for given plate """ 
        formatted_contours =  [contour.reshape(-1, 2).tolist() for contour in deserialize_array_list(plate.contours)] if plate.contours is not None else []
        for contour in formatted_contours:
            for i, point in enumerate(contour):
                contour[i] = (point[0], point[1])
        return formatted_contours
    
    @staticmethod
    def _get_reverted_plate_ctrs(contours: List[List[Tuple[float, float]]]) -> str:
        """ Get plate contours reverted back to serialized string format. Returns in format [np.array([[[x, y]], [[x, y]], [[x, y]], ...]), ...] serialized as a string. """
        contour_list = []
        for contour in contours:
            contour_list.append(np.array([[[point[0], point[1]]] for point in contour]))
        return serialize_array_list(contour_list)

    @staticmethod
    def _get_formatted_part_ctr(part: Part) -> List[Tuple[float, float]]:
        """ Get properly formatted contours for given part """
        contour = deserialize_array(part.contours).tolist()
        for i, point in enumerate(contour):
            contour[i] = (point[0], point[1])
        return contour

    """ Database queries """

    def _get_selected_routers(self) -> List[Router]:
        """ Get all selected routers. """
        try:
            return self.session.query(Router).filter(Router.selected == True).all()  
        except Exception as e:
            logger.error(f"Encountered exception while attempting to get routers' selection status: {e}")

    def _get_imported_parts(self) -> List[Part]:
        """ Get all imported parts. """
        try:
            return self.session.query(Part).all()
        except Exception as e:
            logger.error(f"Encountered exception while attempting to get imported parts: {e}")
            return None

    def _get_selected_plates(self) -> List[Plate]:
        """ Get all selected plates. """
        try:
            return self.session.query(Plate).filter(Plate.selected == True).all()
        except Exception as e:
            logger.error(f"Encountered exception while attempting to get selected plates: {e}")
            return None

    """ Other util methods """

    @staticmethod
    def _quantize_val(value: float) -> float:
        return round(value, 2)
    