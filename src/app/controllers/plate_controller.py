"""
Author: nagan319
Date: 2024/06/01
"""

from typing import Union, Tuple, List

import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.plate_model import Plate, PlateConstants
from ..models.utils import serialize_array, deserialize_array

import matplotlib.pyplot as plt
from ..utils.plotting_util import PlottingConstants, _generate_rectangle_coordinates

from ..logging import logger

from .generic_controller import GenericController

class PlateController(GenericController):
    """
    Controller for handling plate logic.
    - session: working session.
    - preview_image_directory: directory for storing plate preview images.
    """
    MAX_PLATE_AMOUNT: int = 50

    def __init__(self, session: Session, preview_image_directory: str):
        super().__init__(session, Plate, preview_image_directory)
        for plate in self._get_all_items():
            self.save_preview(plate)
    '''
    Add new plates
    '''
    def add_new(self) -> Union[Plate, None]:
        """
        Add new plate with default properties. Returns new plate or None if an error occurs.
        """
        if self.get_amount() >= self.MAX_PLATE_AMOUNT:
            logger.debug(f"Attempted to add new plate at max amount reached.")
            return None

        try:
            new_plate = Plate()
            self._add_item_to_db(new_plate)
            self.save_preview(new_plate)
            return new_plate
        except Exception as e:
            logger.error(f"Encountered error while attempting to create new plate: {e}")
            return None
    '''
    Remove plates
    '''
    def remove(self, id: str) -> bool:
        """ Remove part from db and delete preview image. Returns True if successful, False otherwise. """
        return self._remove_item_and_preview(id)
    '''
    Get plate attributes
    '''
    def get_amount(self) -> int:
        """ Get amount of plates in db. Returns -1 if an error is encountered. """ 
        return self._get_item_amount()

    def get_x(self, id: str) -> Union[float, None]:
        """ Get plate x dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'x')
    
    def get_y(self, id: str) -> Union[float, None]:
        """ Get plate y dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'y')

    def get_z(self, id: str) -> Union[float, None]:
        """ Get plate z dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'z')

    def get_contours(self, id: str) -> Union[np.array, None]:
        """ Get plate contours. Returns None if an error occurs."""
        contours_as_string = self._get_item_attr(id, 'contours')
        return deserialize_array(contours_as_string)
    '''
    Modify plate attributes
    '''
    def edit_x(self, id: str, new_val: float) -> Union[Plate, None]:
        """ Edit plate x dimension. Returns modified plate or None in the case of an error."""
        if new_val <= 0 or new_val > PlateConstants.MAX_X:
            return None
        return self._edit_item_attr(id, 'x', new_val)

    def edit_y(self, id: str, new_val: float) -> Union[Plate, None]:
        """ Edit plate y dimension. Returns modified plate or None in the case of an error."""
        if new_val <= 0 or new_val > PlateConstants.MAX_Y:
            return None
        return self._edit_item_attr(id, 'y', new_val)

    def edit_z(self, id: str, new_val: float) -> Union[Plate, None]:
        """ Edit plate y dimension. Returns modified plate or None in the case of an error."""
        if new_val <= 0 or new_val > PlateConstants.MAX_Z:
            return None
        return self._edit_item_attr(id, 'z', new_val)
    
    def edit_material(self, part_id: int, new_material: str) -> Union[Plate, None]:
        """
        Edit plate amount. Returns modified plate or None if an error occurs.
        """
        if new_material == "" or new_material is None:
            return None
        return self._edit_item_attr(part_id, 'material', new_material)
    
    def edit_contours(self, part_id: int, new_contour: np.array) -> Union[Plate, None]:
        """
        Edit plate contours. Returns modified plate or None if an error occurs.
        """
        contours_as_string = serialize_array(new_contour)
        return self._edit_item_attr(self, part_id, contours_as_string)
    '''
    Preview image logic
    '''
    def save_preview(self, plate: Plate, figsize: Tuple[int, int] = (4, 4), dpi: int = 80):
        """
        Saves a preview image for a plate using matplotlib. 

        Arguments:
        - plate: Plate ORM instance.
        - figsize: Width and height in inches (defaults to 4x4).
        - dpi: Pixels per inch (defaults to 80).
        """
        try:
            image_path = self._get_preview_image_path(plate)
            image_contours = plate.contours
            plate_xy = (plate.width_x, plate.height_y)
            plate_rect_x, plate_rect_y = _generate_rectangle_coordinates(*plate_xy)
        except AttributeError:
            return

        plt.figure(figsize=figsize)
        
        plt.plot(plate_rect_x, plate_rect_y, color=PlottingConstants.PLOT_LINE_COLOR)

        if image_contours:
            contours_list = eval(image_contours) 
            for contour in contours_list:
                contour_array = np.array(contour)
                x_coords = contour_array[:, 0]
                y_coords = contour_array[:, 1]
                plt.plot(x_coords, y_coords, color=PlottingConstants.PLOT_LINE_COLOR, linewidth=1)

        plt.grid(True)
        plt.gca().set_facecolor(PlottingConstants.PLOT_BG_COLOR)
        plt.gca().set_aspect('equal')
        plt.grid(False)
        plt.tick_params(axis='x', colors=PlottingConstants.PLOT_TEXT_COLOR)
        plt.tick_params(axis='y', colors=PlottingConstants.PLOT_TEXT_COLOR)

        plt.gca().spines['top'].set_color(PlottingConstants.PLOT_TEXT_COLOR)
        plt.gca().spines['bottom'].set_color(PlottingConstants.PLOT_TEXT_COLOR)
        plt.gca().spines['left'].set_color(PlottingConstants.PLOT_TEXT_COLOR)
        plt.gca().spines['right'].set_color(PlottingConstants.PLOT_TEXT_COLOR)

        plt.savefig(image_path, bbox_inches='tight', facecolor=PlottingConstants.PLOT_BG_COLOR, dpi=dpi)
        plt.close()
