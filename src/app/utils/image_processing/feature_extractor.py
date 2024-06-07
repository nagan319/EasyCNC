"""
Author: nagan319
Date: 2024/04/12
"""

import math
import os
import numpy as np
import cv2
from typing import List, Tuple, Union

from .utils import Size, Colors
from .features import Features

from ...logging import logger

class FeatureExtractor:
    """
    Class for retrieving critical features from plate image. Saves features in Features class as an attribute. Extracts features when initialized.

    ### Parameters:
    - src_path: Source image filepath.
    - size: Size of image.    

    ### Attributes:
    - features: Found features. Corners are of type numpy.cint
    
    ### Raises:
    - FileNotFoundError, ValueError for invalid input parameters.
    """
    MIN_CTR_AREA = 1000
    MIN_CTR_DIST_FROM_EDGE = 100

    CORNER_DIST_DELTA = 16
    MIN_CORNER_ANGLE = 60
    MIN_CORNER_SEPARATION = 1000

    def __init__(self, src_path: str, size: Size):
        self.features: Features

        if not os.path.exists(src_path):
            raise FileNotFoundError(f"File '{src_path}' not found.")
        if size.w <= 0 or size.h <= 0:
            raise ValueError("Size dimensions must be positive values.")

        image = cv2.imread(src_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Unable to read image file '{src_path}'.")

        max_contour, other_contours = self._get_contours(image, size)
        corners = self._get_corners(max_contour) if max_contour is not None else None

        self.features = Features(plate_contour=max_contour, other_contours=other_contours, corners=corners)

    def _get_contours(self, image, size: Size) -> Tuple[np.array, List[np.array]]:
        """
        Finds contours that exceed area threshold and are a certain threshold away from the edge of the image. 
        """
        contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        filtered_contours: List[np.array] = []

        for contour in contours:
            area: float = cv2.contourArea(contour)

            if area < self.MIN_CTR_AREA:
                continue

            edge_flag = False

            for point in contour:
                x, y = point[0] # points stored as [[x, y]]

                epsilon: float = self.MIN_CTR_DIST_FROM_EDGE

                if x < epsilon or x > size.w - epsilon or y < epsilon or y > size.h - epsilon:
                    edge_flag = True
                    break
        
            if edge_flag and area < size.w * size.h // 4: # checks size in case plate is close to edge
                continue

            filtered_contours.append(contour)

        if not filtered_contours:
            return (None, None)
        
        areas = [cv2.contourArea(contour) for contour in filtered_contours]
        max_area_idx = areas.index(max(areas))
        max_contour = filtered_contours.pop(max_area_idx)
        other_contours = filtered_contours

        if len(other_contours) == 0:
            other_contours = None

        return max_contour, other_contours

    def _get_corners(self, max_contour: np.ndarray) -> List[Tuple[float, float]]:
        """
        Finds plate corners using derivatives and norm product.

        Arguments:
        - max_contour: Plate contour.
        
        Returns:
        - List of found corners stored as tuples of floats.
        """
        corners: List[Tuple[float, float]] = []
        length = len(max_contour)

        for i, point in enumerate(max_contour):

            delta: int = self.CORNER_DIST_DELTA

            prev_idx: int = (i - delta) % length 
            next_idx: int = (i + delta) % length

            x_prev, y_prev = max_contour[prev_idx][0]
            x, y = point[0]
            x_next, y_next = max_contour[next_idx][0]
            
            dx1, dy1 = x - x_prev, y - y_prev
            dx2, dy2 = x_next - x, y_next - y

            dot_product = dx1 * dx2 + dy1 * dy2
            norm_product = np.sqrt((dx1 ** 2 + dy1 ** 2) * (dx2 ** 2 + dy2 ** 2))

            if norm_product == 0:
                angle = 0
            else:
                cos_theta = max(min(dot_product / norm_product, 1.0), -1.0) # ensures valid range
                angle = np.arccos(cos_theta) * (180.0 / np.pi)

            if angle > self.MIN_CORNER_ANGLE:
                corners.append((x, y))

        filtered_corners = [corners[0]]  

        for i in range(1, len(corners)):
            distance = ((corners[i][0] - filtered_corners[-1][0]) ** 2 + (corners[i][1] - filtered_corners[-1][1]) ** 2) ** 0.5 
            if distance > self.MIN_CORNER_SEPARATION:
                filtered_corners.append(corners[i])

        return filtered_corners
    