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
from ..models.utils import deserialize_array_list

from ..utils.packing.bin import Bin
from ..utils.packing.utils.area2d import Area2D
from ..utils.packing.utils.dimension2d import Dimension2D
from ..utils.packing.plot import plot_bin_final

from ..logging import logger

class OptimizationController:
    """
    Controller for managing layout optimization. 
    ### Parameters:
    - session: working session.
    - optimization_preview_directory: directory for storing generated preview images.
    """
    MIN_QUANTIZED_VALUE: float = .01 

    def __init__(self, session: Session, optimization_preview_directory: str):
        if not os.path.exists(optimization_preview_directory):
            logger.error(f"Indicated optimization preview directory path does not exist: {optimization_preview_directory}")
            raise FileNotFoundError(f"Directory not found: {optimization_preview_directory}")

        self.session = session

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

        self.routers = selected_routers 
        self.parts = imported_parts
        self.plates = selected_plates 

        self.part_contours = [deserialize_array_list(part.contours) for part in self.parts]
        self.plate_contours = [deserialize_array_list(plate.contours) for plate in self.plates]

        for router in self.routers:
            print(f"Router {router.id} dimensions: ({router.x}, {router.y})")
        
        for contours in self.part_contours:
            print(f"{contours}")

        for contours in self.plate_contours:
            print(f"{contours}")

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
    