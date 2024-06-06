"""
Author: nagan319
Date: 2024/06/02
"""

import os
from typing import Union

import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.plate_model import Plate
from ..models.utils import serialize_array, deserialize_array
from ..utils.image_processing.filters import BinaryFilter, FlatFilter

from ..logging import logger

# do this later

class ImageEditingController:
    """
    Controller for editing plate contours using imported image.
    ### Parameters:
    - session: working session.
    - image_editing_directory: directory for storing plate images in various states.
    - plate: plate to be modified.
    """
    RAW_IMAGE_BASENAME = 'raw.png'
    BINARY_IMAGE_BASENAME = 'bin.png'
    FEATURES_IMAGE_BASENAME = 'feat.png'
    FLATTENED_IMAGE_BASENAME = 'flat.png'

    def __init__(self, session: Session, image_editing_directory: str, plate: Plate):

        if not os.path.exists(image_editing_directory):
            logger.error(f"Indicated image editing directory path does not exist: {image_editing_directory}")
            raise FileNotFoundError(f"Directory not found: {image_editing_directory}")

        if plate.x <= 0 or plate.y <= 0:
            logger.error("Attempted to use image editor with plate of invalid dimensions")
            raise ValueError("Plate dimensions must be positive non-zero values")

        self.session = session
        self.image_editing_directory = image_editing_directory
        self.plate = plate
        self.__init_image_paths__()

    def __init_image_paths__(self):
        self.raw_path = os.path.join(self.image_editing_directory, self.RAW_IMAGE_BASENAME)
        self.bin_path = os.path.join(self.image_editing_directory, self.BINARY_IMAGE_BASENAME)
        self.feat_path = os.path.join(self.image_editing_directory, self.FEATURES_IMAGE_BASENAME)
        self.flat_path = os.path.join(self.image_editing_directory, self.FLATTENED_IMAGE_BASENAME)        

    def import_image(self, filepath: str) -> None:
        """
        Import raw plate image.
        """
        if not os.path.exists(filepath):
            logger.error(f"Indicated raw image filepath does not exist: {filepath}")
            return None
        
        self.src_image_path = filepath

    # add checks for state
    def get_image_binary(self, threshold: int):
        bin_filter = BinaryFilter(self.raw_path, self.bin_path, threshold)
        bin_filter.save_image()

    def get_image_features(self):
        pass

    def get_flattened_image(self):
        pass

    def save_changes_to_db(self):
        pass

    '''
    def _save_raw_image(self):
        image: np.ndarray = cv2.imread(self.src_img_path, cv2.IMREAD_COLOR)
        image = self.__resize_image(image, self.MAX_IMG_W, self.MAX_IMG_H)
        resolution = image.shape[:2]
        self.__init_resolution__(resolution)
        cv2.imwrite(self.raw_path, image)
    '''