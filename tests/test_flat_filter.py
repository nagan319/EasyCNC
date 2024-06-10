"""
Author: nagan319
Date: 2024/06/03
"""

import os
import pytest
from src.app.utils.image_processing.utils import Size, Colors
from src.app.utils.image_processing.filters import FlatFilter

"""
Tests for flat filter.

Test Coverage:
    - Initialization
        - checks invalid paths 
        - handles invalid filetypes
        - handles wrong amount of corners
    - Save image
        - correctly saves modified image
"""

@pytest.fixture
def src_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'images', 'image5.jpeg')

@pytest.fixture
def invalid_filetype():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'stl files', 'RollerConnectorPlate.STL')

@pytest.fixture
def temp_dir(tmpdir):
    return tmpdir

def test_flat_filter_initialization_invalid_paths(src_path, invalid_filetype):
    with pytest.raises(FileNotFoundError):
        FlatFilter("nonexistent/path/image.jpg", "output/path/image.jpg", Size(100, 100), [(0, 0), (100, 0), (100, 100), (0, 100)])

    with pytest.raises(FileNotFoundError):
        FlatFilter(invalid_filetype, "output/path/image.jpg", Size(100, 100), [(0, 0), (100, 0), (100, 100), (0, 100)])

def test_flat_filter_initialization_invalid_corners(src_path):
    with pytest.raises(ValueError):
        # Invalid number of corners
        FlatFilter(src_path, "output/path/image.jpg", Size(100, 100), [(0, 0), (100, 0), (100, 100)])

    with pytest.raises(ValueError):
        # Non-tuple corner
        FlatFilter(src_path, "output/path/image.jpg", Size(100, 100), [(0, 0), (100, 0), (100, 100), 0])

def test_flat_filter_save_image(src_path, temp_dir):
    output_path = os.path.join(temp_dir, "output_image.jpg")
    flat_filter = FlatFilter(src_path, output_path, Size(100, 100), [(0, 0), (100, 0), (100, 100), (0, 100)])
    flat_filter.save_image()
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
