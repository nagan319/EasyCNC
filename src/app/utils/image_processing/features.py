"""
Author: nagan319
Date: 2024/06/07
"""

from typing import List
import numpy as np

class Features:
    """
    Class for storing detected plate features (for use with non-flattened image).

    ### Parameters:
    - plate_contour: Main contour of plate.
    - other_contours: Other found contours.
    - corners: Plate corners.
    - selected_contour: Index of selected contour.
    - selected_corner: Index of selected corner.
    """
    def __init__(self, plate_contour: np.array=None, other_contours: List[np.array]=None, corners: List[tuple]=None, selected_contour_idx: int=None, selected_corner_idx: int=None):
        self.plate_contour: np.ndarray = plate_contour
        self.other_contours: List[np.array] = other_contours
        self.corners: List[tuple] = corners
        self.selected_contour_idx: int = selected_contour_idx
        self.selected_corner_idx: int = selected_corner_idx
        