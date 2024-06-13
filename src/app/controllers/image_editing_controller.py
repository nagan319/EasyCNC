"""
Author: nagan319
Date: 2024/06/02
"""

import os
import enum
import math
from typing import Union, Tuple, List

import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session
import cv2

from ..models.plate_model import Plate, PlateConstants
from ..models.utils import serialize_array, deserialize_array

from ..controllers.generic_controller import GenericController

from ..utils.image_processing.binary_filter import BinaryFilter
from ..utils.image_processing.features import Features
from ..utils.image_processing.feature_extractor import FeatureExtractor
from ..utils.image_processing.feature_plotter import FeaturePlotter
from ..utils.image_processing.matrix_generator import MatrixGenerator
from ..utils.image_processing.utils import Size, Colors

from ..logging import logger

SUPPORTED_IMAGE_FORMATS = ['.bmp', '.dib', '.jpeg', '.jpg', '.jp2', '.png', '.webp', '.avif']

"""
Image resizing:
- raw (src size)
- display size
- flattened/processed size
"""

class EditorState(enum.Enum):
    RAW = 0
    BINARY = 1
    FEATURES = 2
    FEATURES_EXTRACTED = 3
    FEATURES_FINALIZED = 4
    FLAT_CTRS_EXTRACTED = 5
    FLAT_FINALIZED = 6

image_filenames = {
    EditorState.RAW: 'raw.png',
    EditorState.BINARY: 'binary.png',
    EditorState.FEATURES: 'features.png',
    EditorState.FLAT_FINALIZED: 'flat.png'
}

''''
Necessary refactoring:
- separate saving images and updating state
'''

class ImageEditingController(GenericController):
    """
    Controller for editing plate contours using imported image.
    ### Parameters:
    - session: working session.
    - image_editing_directory: directory for storing plate images in various states.
    - plate: plate to be modified.
    """
    MAX_PROCESSING_SIZE = Size(2000, 2000)
    FLAT_IMAGE_REDUCTION_FACTOR = 5 

    def __init__(self, session: Session, image_editing_directory: str, plate: Plate):
        self.session: Session
        self.plate: Plate

        self.state: EditorState

        self.src_image_path: str
        self.raw_path: str
        self.bin_path: str
        self.feat_path: str
        self.flat_path: str

        self.processing_resolution: Size

        self.features: Features
        self.flattened_contours: List[np.ndarray]

        if not os.path.exists(image_editing_directory):
            logger.error(f"Indicated image editing directory path does not exist: {image_editing_directory}")
            raise FileNotFoundError(f"Directory not found: {image_editing_directory}")

        if plate.x <= 0 or plate.y <= 0:
            logger.error("Attempted to use image editor with plate of invalid dimensions.")
            raise ValueError("Plate dimensions must be positive non-zero values.")

        if plate.x > PlateConstants.MAX_X or \
            plate.y > PlateConstants.MAX_Y or \
                plate.z > PlateConstants.MAX_Z:
            logger.error("Attempted to use image editor with plate of invalid dimensions.")
            raise ValueError("Plate dimensions must be within allowed range.")          

        self.session = session
        self.image_editing_directory = image_editing_directory
        self.plate = plate
        self.__init_image_paths__()

        self.state = EditorState.RAW

    def __init_image_paths__(self):
        """ Initialize image filepaths. """
        self.raw_path = os.path.join(self.image_editing_directory, image_filenames.get(EditorState.RAW))
        self.bin_path = os.path.join(self.image_editing_directory, image_filenames.get(EditorState.BINARY))
        self.feat_path = os.path.join(self.image_editing_directory, image_filenames.get(EditorState.FEATURES))
        self.flat_path = os.path.join(self.image_editing_directory, image_filenames.get(EditorState.FLAT_FINALIZED))  

    '''
    Raw image handling
    '''
    def save_src_image(self, filepath: str) -> bool:
        """ 
        Import raw plate image. Checks for invalid filepath and file type. 
        Returns True if successful, False otherwise.
        """

        if self.state != EditorState.RAW:
            logger.error(f"Attempted to import raw image in wrong ImageEditingController state.")
            return False

        if not os.path.exists(filepath):
            logger.error(f"Indicated raw image filepath does not exist: {filepath}")
            return False
        
        extension = os.path.splitext(filepath)[1]
        if extension not in SUPPORTED_IMAGE_FORMATS:
            logger.error(f"Image file is of invalid format: {extension}")
            return False
        
        try:
            self.src_image_path = filepath
            self.processing_resolution = ImageEditingController.save_resized_image(self.src_image_path, self.raw_path, self.MAX_PROCESSING_SIZE)
            self.state = EditorState.BINARY
            logger.debug(f"Raw image saved successfully: {filepath}")   
            return True
        except Exception as e:
            logger.error(f"Encountered exception while attempting to save binary image: {e}")
            return False
    
    @staticmethod
    def save_resized_image(src_path: str, dst_path: str, size_limits: Size) -> Size:
        """ Save resized image to dst path. Returns size of new image. """
        image: np.ndarray = cv2.imread(src_path, cv2.IMREAD_COLOR)
        image = ImageEditingController._resize_image(image, size_limits)
        new_height, new_width = image.shape[:2]
        cv2.imwrite(dst_path, image)
        logger.debug(f"Successfully saved resized image from {src_path} to {dst_path}")
        return Size(new_width, new_height)

    @staticmethod
    def _resize_image(image: np.ndarray, max_size: Size) -> np.ndarray:
        """ Upscale image to fit within indicated size constraints. """
        initial_height, initial_width = image.shape[:2]
        scale_factor = min(max_size.w / initial_width, max_size.h / initial_height)

        new_width = round(initial_width * scale_factor)
        new_height = round(initial_height * scale_factor)
        
        new_dim = (new_width, new_height)
        resized_image = cv2.resize(image, new_dim, interpolation=cv2.INTER_LANCZOS4)

        return resized_image
    '''
    Binary image handling
    '''
    def save_binary_image(self, threshold: int) -> bool:
        """
        Saves binary image with given threshold to preview directory. Checks for invalid state and raw image path.
        Returns True if successful, False otherwise.
        """
        if self.state != EditorState.BINARY:
            logger.error("Attempted to get binary image in wrong state.")
            return False
        
        if not os.path.exists(self.raw_path):
            logger.error("Raw image file does not exist.")
            return False
        
        if threshold > 255 or threshold < 0 or not isinstance(threshold, int):
            logger.error("Attempted to generate binary image with invalid threshold value.")
            return False

        try:
            bin_filter = BinaryFilter(self.raw_path, self.bin_path, threshold)
            bin_filter.save_image()
            logger.debug("Binary image saved successfully.")
            return True
        except Exception as e:
            logger.error(f"Encountered exception while attempting to save binary image: {e}")
            return False
        
    def finalize_binary(self):
        """ Modifies state to confirm finalization of binary image editing."""
        self.state = EditorState.FEATURES
    '''
    Feature handling
    '''
    def extract_image_features(self) -> bool:
        """
        Extract image features and save to class parameter. Checks for invalid state and image path.
        Returns True if successful, False otherwise.
        """
        if self.state != EditorState.FEATURES:
            logger.error("Attempted to extract features in wrong state.")
            return False
        
        if not os.path.exists(self.bin_path):
            logger.error("Binary image file does not exist.")
            return False
        
        try:
            feature_extractor = FeatureExtractor(self.bin_path, self.processing_resolution) 
            self.features = feature_extractor.features
            self.state = EditorState.FEATURES_EXTRACTED
            logger.debug("Image features extracted successfully.")
            return True
        except Exception as e:
            logger.error(f"Encountered exception while attempting to extract image features: {e}")
            return False

    def save_image_features(self) -> bool:
        """
        Saves image features to preview directory. Checks for invalid state.
        Returns True if successful, False otherwise. 
        """
        if self.state != EditorState.FEATURES_EXTRACTED:
            logger.error("Attempted to save image features in wrong state.")
            return False
        
        try:
            feature_plotter = FeaturePlotter(
                dst_path=self.feat_path, 
                size=self.processing_resolution, 
                features=self.features) # default colors
            feature_plotter.save_features()
            logger.debug(f"Image features saved successfully to {self.feat_path}")
            return True
        except Exception as e:
            logger.error(f"Encountered exception while attempting to save image features: {e}")
            return False
        
    def _valid_features(self) -> bool:
        """ Returns True if features are valid for flattening. """
        return self.features and \
            self.features.plate_contour is not None and \
            len(self.features.corners) == 4
    
    def finalize_features(self):
        """ Modifies state to confirm finalization of feature editing."""
        self.state = EditorState.FEATURES_FINALIZED
    '''
    Manual feature editing
    '''
    def select_corner(self, n: int):
        """ Change selected corner. """
        if self.features is not None:
            self.features.selected_corner_idx = n

    def unselect_corner(self):
        """ Set selected corner to None. """
        if self.features is not None:
            self.features.selected_corner_idx = None


    def select_contour(self, n: int):
        """ Change selected contour. """
        if self.features is not None:
            self.features.selected_contour_idx = n

    def unselect_contour(self):
        """ Set selected contour to None. """
        if self.features is not None:
            self.features.selected_contour_idx = None


    def remove_selected_corner(self):
        """ Removes selected corner. """
        if self.features is None or self.features.selected_corner_idx is None:
            return False
        if 0 <= self.features.selected_corner_idx < len(self.features.corners):
            del self.features.corners[self.features.selected_corner_idx]
            self.unselect_corner()
            return True
        return False

    def remove_selected_contour(self) -> bool:
        """ Removes selected contour. """
        if self.features is None or self.features.selected_contour_idx is None:
            return False
        if 0 <= self.features.selected_contour_idx < len(self.features.other_contours):
            del self.features.other_contours[self.features.selected_contour_idx]
            self.unselect_contour()
            return True
        return False

    def add_corner(self, coordinates: tuple) -> bool:
        """ Add a new corner at the specified coordinate. Returns True if added successfully. """
        x, y = coordinates
        if not (0 <= x < self.processing_resolution.w) or not (0 <= y < self.processing_resolution.h):
            return False
        new_corner = (x, y)
        self.features.corners.append(new_corner)
        return True

    def check_feature_selected(self, coordinates: Tuple[float, float]) -> bool:
        """ Check if a feature is present near the selected coordinate, and select if true. """
        THRESHOLD: int = 20

        if self.features.corners is not None:
            for i, corner in enumerate(self.features.corners):
                if ImageEditingController.distance(coordinates, corner) < THRESHOLD:
                    self.unselect_contour()
                    self.select_corner(i)
                    return True
        
        ''' Skips points for increased speed '''
        if self.features.other_contours is not None:
            for i, contour in enumerate(self.features.other_contours):
                for point in contour[::int(THRESHOLD*2)]:
                    if ImageEditingController.distance(coordinates, point) < THRESHOLD:
                        self.unselect_corner()
                        self.select_contour(i)
                        return True

        return False

    @staticmethod
    def distance(p1: tuple, p2: tuple) -> float:
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt(abs(x2 - x1)**2 + abs(y2 - y1)**2)

    '''
    Image flattening
    '''
    def get_flattened_contours(self) -> bool:
        """
        Flatten contours using image transformation matrix
        """
        if self.state != EditorState.FEATURES_FINALIZED:
            logger.error("Attempted to extract transformation matrix in wrong state.")
            return False   

        try:
            raw_contours = self.features.other_contours
            output_resolution = Size(self.plate.x, self.plate.y)
            matrix_generator = MatrixGenerator(output_resolution, self.features.corners)    
            transformation_matrix = matrix_generator.matrix()
            flattened_contours = []
            for contour in raw_contours:
                flattened_contour = cv2.perspectiveTransform(contour, transformation_matrix)
                flattened_contours.append(flattened_contour)
            self.flattened_contours = flattened_contours
            logger.debug("Successfully extracted flattened contours.")
            self.state = EditorState.FLAT_CTRS_EXTRACTED
            return True
        except Exception as e:
            logger.error(f"Encountered exception while attempting to retrieve flattened contours: {e}")
            return False

    def save_flattened_image(self) -> bool:
        """
        Save image containing flattened contours to preview directory.
        """
        if self.state != EditorState.FLAT_CTRS_EXTRACTED:
            logger.error("Attempted to save flattened image in wrong state.")
            return False 

        try:
            plotter = FeaturePlotter(
                self.flat_path, 
                Size(self.plate.x // self.FLAT_IMAGE_REDUCTION_FACTOR, self.plate.y // self.FLAT_IMAGE_REDUCTION_FACTOR), 
                Features(other_contours=self.flattened_contours)
            )
            plotter.save_features()
            self.state = EditorState.FLAT_FINALIZED
            return True
        except Exception as e:
            logger.error(f"Encountered exception while attempting to save flattened image: {e}")
            return False       

    def save_flattened_contours(self) -> bool:
        """
        Save flattened contours to db.
        """
        if self.state != EditorState.FLAT_FINALIZED:
            logger.error("Attempted to save flat contours in wrong state.")
            return False   

        try:
            self._edit_item_attr(self.plate.id, 'contours', serialize_array(self.flattened_contours))
            return True
        except Exception as e:
            logger.error(f"Encountered exception while attempting to save flattened contours: {e}")
            return False               
