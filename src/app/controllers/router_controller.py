"""
Author: nagan319
Date: 2024/06/03
"""

import os
from typing import Union, Tuple

import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.router_model import Router, RouterConstants

import matplotlib.pyplot as plt
from ..utils.plotting_util import PlottingConstants, _generate_rectangle_coordinates

from ..logging import logger

from .generic_controller import GenericController

# implement atexit logic to remove preview images

class RouterController(GenericController):
    """
    Controller for handling router logic.
    ### Parameters:
    - session: working session.
    - preview_image_directory: directory for storing router preview images.
    """
    MAX_ROUTER_AMOUNT: int = 10

    def __init__(self, session: Session, preview_image_directory: str):
        super().__init__(session, Router, preview_image_directory)
        for router in self._get_all_items():
            self.save_preview(router)
    '''
    Add new routers
    '''
    def add_new(self) -> Union[Router, None]:
        """
        Add new router with default properties. Returns new router or None if an error occurs.
        """
        if self.get_amount() >= self.MAX_ROUTER_AMOUNT:
            logger.debug(f"Attempted to add new router at max amount reached.")
            return None
        
        try:
            new_router = Router()
            self._add_item_to_db(new_router)
            self.save_preview(new_router)
            return new_router
        except Exception as e:
            logger.error(f"Encountered error while attempting to create new router: {e}")
            return None     
    '''
    Remove routers
    '''
    def remove(self, id: str) -> bool:
        """
        Remove router from db and delete preview image. Returns True if successful, False otherwise.
        """
        return self._remove_item_and_preview(id)
    '''
    Get router attributes
    '''
    def get_amount(self) -> int:
        """ Get amount of routers in db. Returns -1 if an error is encountered. """ 
        return self._get_item_amount()

    def get_x(self, id: str) -> Union[float, None]:
        """ Get router x dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'x')
    
    def get_y(self, id: str) -> Union[float, None]:
        """ Get router y dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'y')

    def get_z(self, id: str) -> Union[float, None]:
        """ Get router z dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'z')
    
    def get_plate_x(self, id: str) -> Union[float, None]:
        """ Get router max plate x dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'plate_x')

    def get_plate_y(self, id: str) -> Union[float, None]:
        """ Get router max plate y dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'plate_y')
    
    def get_plate_z(self, id: str) -> Union[float, None]:
        """ Get router max plate z dimension. Returns None if an error occurs."""
        return self._get_item_attr(id, 'plate_z')  
    
    def get_min_safe_dist_from_edge(self, id: str) -> Union[float, None]:
        """ Get router min distance from edge. Returns None if an error occurs."""
        return self._get_item_attr(id, 'min_safe_dist_from_edge')

    def get_drill_bit_diameter(self, id: str) -> Union[float, None]:
        """ Get router drill bit diameter. Returns None if an error occurs.""" 
        return self._get_item_attr(id, 'drill_bit_diameter')

    def get_mill_bit_diameter(self, id: str) -> Union[float, None]:
        """ Get router mill bit diameter. Returns None if an error occurs.""" 
        return self._get_item_attr(id, 'mill_bit_diameter')   
    '''
    Modify router attributes
    '''
    def edit_name(self, id: str, new_val: str) -> Union[Router, None]:
        """ Edit router name. Returns modified router or None in the case of an error. """
        return self._edit_item_attr(id, 'name', new_val)

    def edit_x(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router x dimension. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > RouterConstants.MAX_ROUTER_DIMENSION:
            return None
        return self._edit_item_attr(id, 'x', new_val)

    def edit_y(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router y dimension. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > RouterConstants.MAX_ROUTER_DIMENSION:
            return None
        return self._edit_item_attr(id, 'y', new_val)
    
    def edit_z(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router z dimension. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > RouterConstants.MAX_ROUTER_DIMENSION:
            return None
        return self._edit_item_attr(id, 'z', new_val)

    def edit_plate_x(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router max plate x dimension. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > RouterConstants.MAX_PLATE_DIMENSION:
            return None
        return self._edit_item_attr(id, 'plate_x', new_val)
    
    def edit_plate_y(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router max plate y dimension. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > RouterConstants.MAX_PLATE_DIMENSION:
            return None
        return self._edit_item_attr(id, 'plate_y', new_val)

    def edit_plate_z(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router max plate z dimension. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > RouterConstants.MAX_PLATE_DIMENSION:
            return None
        return self._edit_item_attr(id, 'plate_z', new_val)
    
    def edit_min_safe_dist_from_edge(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router min safe distance from edge. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > min(self.get_x(id), self.get_y(id)) // 2:
            return None
        return self._edit_item_attr(id, 'min_safe_dict_from_edge', new_val)

    def edit_mill_bit_diameter(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router mill bit diameter. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > RouterConstants.MAX_MILL_BIT_DIAMETER:
            return None
        return self._edit_item_attr(id, 'mill_bit_diameter', new_val)

    def edit_drill_bit_diameter(self, id: str, new_val: float) -> Union[Router, None]:
        """ Edit router drill bit diameter. Returns modified router or None in the case of an error."""
        if new_val <= 0 or new_val > RouterConstants.MAX_DRILL_BIT_DIAMETER:
            return None
        return self._edit_item_attr(id, 'drill_bit_diameter', new_val)
    '''
    Preview image logic
    '''
    def save_preview(self, router: Router, figsize: Tuple[int, int] = (8, 8), dpi: int = 80):
        """
        Saves a preview image for a router using matplotlib.

        Arguments:
        - router: Router ORM instance.
        - figsize: Width and height in inches (defaults to 8x8).
        - dpi: Pixels per inch (defaults to 80).
        """
        try:
            image_path = self._get_preview_image_path(router.id)
            router_xy = (router.machineable_area_x, router.machineable_area_y)
            plate_xy = (router.max_plate_size_x, router.max_plate_size_y)
            safe_distance = router.min_safe_dist_from_edge
        except AttributeError:
            return

        if not all(coord is not None for coord in router_xy + plate_xy + (safe_distance,)):
            return

        router_x_offset = (plate_xy[0] - router_xy[0]) / 2
        router_y_offset = plate_xy[1] - router_xy[1]

        plate_rect_x, plate_rect_y = _generate_rectangle_coordinates(*plate_xy)
        router_rect_x, router_rect_y = _generate_rectangle_coordinates(*router_xy, router_x_offset, router_y_offset)
        safe_rect_x, safe_rect_y = _generate_rectangle_coordinates(*(dim - 2 * safe_distance for dim in plate_xy), safe_distance, safe_distance)

        plt.figure(figsize=figsize)

        plt.plot(plate_rect_x, plate_rect_y, color=PlottingConstants.PLOT_LINE_COLOR, linestyle=':')
        plt.plot(router_rect_x, router_rect_y, color=PlottingConstants.PLOT_LINE_COLOR)
        plt.plot(safe_rect_x, safe_rect_y, color=PlottingConstants.PLOT_LINE_COLOR, linestyle='--')

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
