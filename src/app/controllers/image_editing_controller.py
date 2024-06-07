"""
Author: nagan319
Date: 2024/06/02
"""

import os
import enum
from typing import Union

import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.plate_model import Plate
from ..models.utils import serialize_array, deserialize_array
from ..utils.image_processing.filters import BinaryFilter, FlatFilter

from ..logging import logger

SUPPORTED_IMAGE_FORMATS = ['.bmp', '.dib', '.jpeg', '.jpg', '.jp2', '.png', '.webp', '.avif']

class EditorState(enum.Enum):
    RAW = 0
    BINARY = 1
    FEATURES = 2
    FLAT = 3

image_filenames = {
    EditorState.RAW: 'raw.png',
    EditorState.BINARY: 'binary.png',
    EditorState.FEATURES: 'features.png',
    EditorState.FLAT: 'flat.png'
}

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

        self.state = EditorState.RAW

    def __init_image_paths__(self):
        self.raw_path = os.path.join(self.image_editing_directory, image_filenames(EditorState.RAW))
        self.bin_path = os.path.join(self.image_editing_directory, image_filenames(EditorState.BINARY))
        self.feat_path = os.path.join(self.image_editing_directory, image_filenames(EditorState.FEATURES))
        self.flat_path = os.path.join(self.image_editing_directory, image_filenames(EditorState.FLAT))        

    def import_image(self, filepath: str) -> None:
        """
        Import raw plate image. Checks for invalid filepath and file type.
        """
        if not os.path.exists(filepath):
            logger.error(f"Indicated raw image filepath does not exist: {filepath}")
            return None
        
        extension = os.path.splitext(filepath)[1]
        if extension not in SUPPORTED_IMAGE_FORMATS:
            logger.error(f"Image file is of invalid format: {extension}")

        self.src_image_path = filepath

    # add checks for state
    def get_image_binary(self, threshold: int):
        """
        Saves binary image with given threshold to preview directory. Checks for invalid state and raw image path.
        """
        if self.state != EditorState.BINARY:
            logger.error("Attempted to get binary image in wrong state.")
            return 
        
        if not os.path.exists(self.raw_path):
            logger.error("Raw image file does not exist.")
            return
        
        bin_filter = BinaryFilter(self.raw_path, self.bin_path, threshold)
        bin_filter.save_image()

    def get_image_features(self):
        pass

    def get_flattened_image(self):
        """
        Saves flattened image to preview directory. Checks for invalid state and feature image path.
        """

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