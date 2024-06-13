"""
Author: nagan319
Date: 2024/04/15
"""

import os
import numpy as np
import cv2
from typing import Tuple, List

from .utils import Size, Colors
from .constants import SUPPORTED_IMAGE_FORMATS

from ...logging import logger

class BinaryFilter:
    """
    Filter for converting color image to thresholded binary. Assumes valid src and dst paths.

    ### Parameters:
    - src_path: source path.
    - dst_path: destination path.
    - threshold: threshold value that separates white from black, must be in range [0, 255].

    ### Raises
    - ValueError or TypeError if threshold value is invalid.
    """

    def __init__(self, src_path: str, dst_path: str, threshold: int):

        if not os.path.exists(src_path):
            logger.error(f"Attempted to initialize BinaryFilter with invalid src path: {src_path}")
            raise FileNotFoundError()

        if os.path.splitext(src_path)[1] not in SUPPORTED_IMAGE_FORMATS:
            logger.error(f"Attempted to initialize BinaryFilter with invalid src filetype: {src_path}")
            raise FileNotFoundError()         

        if threshold < 0 or threshold > 255:
            logger.error("Threshold value must be in range 0-255")
            raise ValueError()
        
        if not isinstance(threshold, int):
            logger.error("Threshold must be integer value")
            raise TypeError()
        
        self.threshold = threshold

        self.src_path = src_path
        self.dst_path = dst_path

        self.image = cv2.imread(self.src_path, cv2.IMREAD_COLOR)
    
    def save_image(self):
        """ Saves thresholded image to dst path specified at initialization. """
        self._apply_binary_filter()
        cv2.imwrite(self.dst_path, self.image)

    def _apply_binary_filter(self):
        """
        Applies CV binary filter after preprocessing using Gaussian blur.
        """
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) 
        image = cv2.GaussianBlur(image, (7, 7), 0)
        _, image = cv2.threshold(image, self.threshold, 255, cv2.THRESH_BINARY) 
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((10, 10), np.uint8))
        self.image = image
