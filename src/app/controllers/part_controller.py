"""
Author: nagan319
Date: 2024/06/01
"""

import os
from typing import Union

import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.part_model import Part
from ..models.utils import serialize_array, deserialize_array
from ..utils.stl_parser import STLParser
from ..logging import logger

from .generic_controller import GenericController 

class PartController(GenericController):
    """
    Controller for handling part logic.
    ### Parameters:
    - session: working session.
    - preview_image_directory: directory for storing part preview images.
    """
    MAX_PART_AMOUNT: int = 20

    def __init__(self, session: Session, preview_image_directory: str):
        super().__init__(session, Part, preview_image_directory)
    '''
    Add new parts
    '''
    def add_from_file(self, filepath: str) -> Union[Part, None]:
        """
        Extract part from STL file and add to db, create preview image.
        Returns newly created part if successful, None otherwise
        """
        if not os.path.exists(filepath):
            logger.error(f"STL file does not exist: {filepath}")
            return None

        duplicates = self.session.query(Part).filter(Part.filename == os.path.basename(filepath)).first()
        if duplicates is not None:
            logger.debug(f"Attempted to add already existing STL file: {filepath}")
            return None

        try:
            parser = STLParser(filepath) 
            parser.parse_stl()
            part = Part(
                filename=os.path.basename(filepath), 
                thickness=parser.thickness,
                contours=serialize_array(parser.outer_contour)
            )
            self._add_item_to_db(part)
            dst_path = self._get_preview_image_path(str(part.id))
            parser.save_preview_image(dst_path)
            logger.debug(f"Imported file {filepath} successfully")
            return part
        except Exception as e:
            logger.error(f"Encountered error while attempting to import file {filepath}: {e}")
            return None
    '''
    Remove parts
    '''
    def remove(self, id: str) -> bool:
        """ Remove part from db and delete preview image. Returns True if successful, False otherwise. """
        return self._remove_item_and_preview(id)

    def remove_all(self):
        """ Clears out part db. """
        self._remove_all_items_from_db()

    def remove_all_with_previews(self):
        """ Clear out part db and remove image previews. """
        self._remove_all_items_and_previews()
    '''
    Get part attributes
    '''
    def get_total_amount(self) -> Union[int, None]:
        """ Get total amount of imported parts. """
        return self.session.query(func.sum(Part.amount)).scalar() or 0  

    def get_filename(self, id: str) -> Union[str, None]:
        """ Get total amount of imported parts. """
        return self._get_item_attr(id, 'filename')

    def get_thickness(self, id: str) -> Union[float, None]:
        """ Get part thickness. Returns None if error occurs. """
        return self._get_item_attr(id, 'thickness')

    def get_material(self, id: str) -> Union[str, None]:
        """ Get total amount of imported parts. """
        return self._get_item_attr(id, 'material')

    def get_contours(self, id: str) -> Union[np.array, None]:
        """ Get part contours. Returns None if an error occurs. """
        contours = self._get_item_attr(id, 'contours')
        return deserialize_array(contours) if contours else None

    def get_amount(self, id: str) -> Union[int, None]:
        """
        Get part amount. Returns part amount or None if an error occurs.
        """
        return self._get_item_attr(id, 'amount')
    '''
    Modify part attributes
    '''
    def edit_material(self, id: str, new_material: str) -> Union[str, None]:
        """
        Edit part material. Returns modified part or None if an error occurs.
        """
        if new_material is None or new_material == '':
            return None
        return self._edit_item_attr(id, 'material', new_material)

    def edit_amount(self, id: str, new_val: int) -> Union[Part, None]:
        """
        Edit part amount. Returns modified part or None if an error occurs.
        """
        if new_val is None or new_val <= 0 or not isinstance(new_val, int):
            logger.error(f"Attempted invalid input value for part amount: {new_val}")
            return None
        current_amount = self.get_amount(id) or 0
        new_total = self.get_total_amount() - current_amount + new_val
        if new_val < 1 or new_total > self.MAX_PART_AMOUNT:
            return None
        return self._edit_item_attr(id, 'amount', new_val)
    