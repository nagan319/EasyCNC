"""
Author: nagan319
Date: 2024/06/13
"""
import numpy as np
import cv2
from typing import List, Tuple
from .utils import Size

from ...logging import logger

class MatrixGenerator:
    """
    Generates transformation matrix for flattening image contours.
    """
    def __init__(self, output_resolution: Size, corners: List[Tuple[float, float]]):
        if len(corners) != 4 or not all(isinstance(point, tuple) and len(point) == 2 for point in corners):
            raise ValueError("Corners must be a list of four (x, y) tuples.")
        try:
            self.src_corners = self._sort_corners(corners) 
            self.dst_corners = self._get_rectangle_corners(output_resolution)
            self.transformation_matrix = self._get_transformation_matrix(self.src_corners, self.dst_corners)
            logger.debug("Successfully generated transformation matrix.")
        except Exception as e:
            logger.error(f"An error occured while attempting to generate a transformation matrix: {e}")

    def matrix(self) -> np.ndarray:
        """ Get transformation matrix."""
        return self.transformation_matrix

    @staticmethod
    def _sort_corners(corners: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Sorts list of input corners in top left, top right, bottom left, and bottom right order.
        """
        avg_x = sum(point[0] for point in corners) / len(corners)
        avg_y = sum(point[1] for point in corners) / len(corners)
        sorted_corners = [None for _ in range(4)]

        for corner in corners:
            x, y = corner
            if x < avg_x and y < avg_y: 
                sorted_corners[0] = corner
            elif x > avg_x and y < avg_y: 
                sorted_corners[1] = corner
            elif x < avg_x and y > avg_y: 
                sorted_corners[2] = corner
            else:
                sorted_corners[3] = corner
        
        return sorted_corners
    
    @staticmethod
    def _get_rectangle_corners(size: Size) -> List[Tuple[float, float]]:
        """
        Returns array of rectangle corners based on input resolution.
        """
        top_left = (0, 0)
        top_right = (size.w, 0)
        bottom_right = (size.w, size.h)
        bottom_left = (0, size.h)
        return [top_left, top_right, bottom_left, bottom_right]
    
    @staticmethod
    def _get_transformation_matrix(src_pts: List[Tuple[float, float]], dst_pts: List[Tuple[float, float]]) -> np.ndarray:
        """
        Gets CV transformation matrix based on desired input and output points.

        Arguments:
        - src_pts: list of sorted input corners.
        - dst_pts: list of sorted output corners.

        Returns:
        - Numpy array containing CV transformation matrix.
        """
        src_pts = np.array(src_pts, dtype=np.float32)
        dst_pts = np.array(dst_pts, dtype=np.float32)
        return cv2.getPerspectiveTransform(src_pts, dst_pts)
    