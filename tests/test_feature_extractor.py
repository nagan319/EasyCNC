"""
Author: nagan319
Date: 2024/06/07
"""

import os
from typing import Tuple
import numpy as np

import pytest
from pytest import raises

from src.app.utils.image_processing.utils import Size
from src.app.utils.image_processing.feature_extractor import FeatureExtractor

"""
Tests for FeatureExtractor class.

Test coverage:
    Initialization:

"""

@pytest.fixture
def bin_img_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'images', 'image0bin.png')

@pytest.fixture
def invalid_filetype():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'stl files', 'RollerConnectorPlate.STL')

def test_init_invalid_path():
    with raises(FileNotFoundError):
        FeatureExtractor("random invalid path", Size(100, 100))

def test_init_invalid_size(bin_img_path):
    with raises(ValueError):
        FeatureExtractor(bin_img_path, Size(0, 0))

def test_init_invalid_filetype(invalid_filetype):
    with raises(ValueError):
        FeatureExtractor(invalid_filetype, Size(100, 100))

def test_plate_contour_extraction(bin_img_path):
    extractor = FeatureExtractor(bin_img_path, Size(1000, 2000))
    assert len(extractor.features.plate_contour) > 1000 
    assert isinstance(extractor.features.plate_contour, np.ndarray)

def test_other_contour_extraction(bin_img_path):
    extractor = FeatureExtractor(bin_img_path, Size(1000, 2000))
    assert len(extractor.features.other_contours) > 0 
    assert isinstance(extractor.features.other_contours[0], np.ndarray)

def test_corner_extraction(bin_img_path):
    extractor = FeatureExtractor(bin_img_path, Size(1000, 2000))
    assert len(extractor.features.corners) == 3 
    assert isinstance(extractor.features.corners[0], tuple) 
