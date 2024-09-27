"""
Author: nagan319
Date: 2024/06/23
"""

import os
import enum
from collections import defaultdict
from typing import Union, Tuple, List

from sqlalchemy.orm import Session

from ..models.router_model import Router
from ..models.plate_model import Plate
from ..models.part_model import Part
from ..models.utils import deserialize_array, deserialize_array_list

from ..utils.packing.bin import Bin
from ..utils.packing.utils.area2d import Area2D
from ..utils.packing.utils.dimension2d import Dimension2D
from ..utils.packing.packing_algo import execute_packing_algorithm

from ..logging import logger

class OptimizationController:
    """
    Controller for managing layout optimization. 
    ### Parameters:
    - session: working session.
    - preview_path: preview image filename
    """
    MIN_QUANTIZED_VALUE: float = .01 

    def __init__(self, session: Session, preview_path: str, conversion_factor: float = 1.0):
        if not os.path.exists(os.path.dirname(preview_path)):
            logger.error(f"Indicated optimization preview directory path does not exist: {preview_path}")
            raise FileNotFoundError(f"Directory not found: {preview_path}")

        self.session = session
        self.preview_path = preview_path
        self.conversion_factor = conversion_factor

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

        router_sizes = [(router.plate_x, router.plate_y) for router in self.routers_orm]
        max_plate_x = min(router_sizes, key=lambda size: size[0])[0]
        max_plate_y = min(router_sizes, key=lambda size: size[1])[1]

        plates = []

        for plate in self.plates_orm:
            if plate.x <= max_plate_x and plate.y <= max_plate_y:
                contour_list = []
                if plate.contours is not None:
                    contour_list = [contour.reshape(-1, 2).tolist() for contour in deserialize_array_list(plate.contours)]
                    for contour in contour_list:
                        for i, point in enumerate(contour):
                            contour[i] = (point[0], point[1])
                plates.append((plate.id, (plate.x, plate.y), contour_list))

        if len(plates) == 0:
            raise ValueError("Selected plates exceed maximum size of selected router.")

        parts = []

        for part in self.parts_orm:
            id = part.id
            amount = part.amount
            contour = deserialize_array(part.contours).tolist()
            for i, point in enumerate(contour):
                contour[i] = (point[0], point[1])
            for i in range(amount):
                parts.append((f"{id}-{i+1}", contour))

        self.placements = execute_packing_algorithm(plates, parts, self.preview_path, self.conversion_factor)

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

    @staticmethod
    def _quantize_val(value: float) -> float:
        return round(value, 2)
    