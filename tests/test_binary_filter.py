"""
Author: nagan319
Date: 2024/06/03
"""

import os
import numpy as np
import cv2
import pytest
from src.app.utils.image_processing.filters import BinaryFilter
import tempfile

"""
Tests for binary filter.

Test coverage:
- errors in case of invalid input threshold values
- image saves correctly
"""

@pytest.fixture
def src_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'images', 'image5.jpeg')

@pytest.fixture
def invalid_filetype():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'stl files', 'RollerConnectorPlate.STL')

@pytest.fixture
def setup_binary_filter(src_path, tmp_path):
    src_path = src_path
    dst_path = os.path.join(tmp_path, "binary_filter_test.png")
    threshold = 127
    yield src_path, dst_path, threshold

def test_binary_filter_invalid_src_path():
    with pytest.raises(FileNotFoundError):
        BinaryFilter("random invalid path", "dst_path.png", 100)

def test_binary_filter_invalid_src_filetype(invalid_filetype):
    with pytest.raises(FileNotFoundError):
        BinaryFilter(invalid_filetype, "dst_path.png", 100)

def test_binary_filter_invalid_threshold(src_path, tmp_path):

    dst_path = os.path.join(tmp_path, "binary_filter_test.png")

    with pytest.raises(ValueError):
        BinaryFilter(src_path, dst_path, -1)

    with pytest.raises(ValueError):
        BinaryFilter(src_path, dst_path, 256)

    with pytest.raises(TypeError):
        BinaryFilter(src_path, dst_path, 128.5)

    with pytest.raises(TypeError):
        BinaryFilter(src_path, dst_path, "invalid")

    with pytest.raises(TypeError):
        BinaryFilter(src_path, dst_path, None)

def test_binary_filter_save_image(setup_binary_filter):
    src_path, dst_path, threshold = setup_binary_filter

    binary_filter = BinaryFilter(src_path, dst_path, threshold)
    binary_filter.save_image()

    assert os.path.exists(dst_path)

    original_image = cv2.imread(src_path)
    saved_image = cv2.imread(dst_path)
    assert original_image.shape == saved_image.shape
