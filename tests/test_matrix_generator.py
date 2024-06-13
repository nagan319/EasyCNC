"""
Author: nagan319
Date: 2024/06/13
"""

import pytest
import numpy as np
from src.app.utils.image_processing.utils import Size
from src.app.utils.image_processing.matrix_generator import MatrixGenerator

"""
Tests for matrix generator.

Test Coverage:
    - Initialization
        - check invalid corners
        - check valid initialization and matrix generation
        - src corners are sorted correctly
        - dst corners are retrieved correctly
    - Get matrix
        - correctly returns transformation matrix
"""

@pytest.fixture
def valid_corners():
    return [(100, 100), (0, 100), (100, 0), (0, 0)]

@pytest.fixture
def valid_size():
    return Size(1000, 1000)

@pytest.fixture
def valid_generator(valid_size, valid_corners):
    return MatrixGenerator(valid_size, valid_corners)

def test_matrix_generator_init_invalid_corners(valid_size):
    with pytest.raises(ValueError):
        ''' Invalid number of corners '''
        MatrixGenerator(valid_size, [(0, 0), (100, 0), (100, 100)])

    with pytest.raises(ValueError):
        ''' Non-tuple corner '''
        MatrixGenerator(valid_size, [(0, 0), (100, 0), (100, 100), 0])

def test_matrix_generator_correct_src_corners(valid_generator):
    assert valid_generator.src_corners ==  [(0, 0), (100, 0), (0, 100), (100, 100)]

def test_matrix_generator_correct_dst_corners(valid_generator):
    assert valid_generator.dst_corners == [(0, 0), (1000, 0), (0, 1000), (1000, 1000)]

def test_matrix_generator_correct_matrix(valid_generator):
    assert isinstance(valid_generator.transformation_matrix, np.ndarray)
    matrix_func_return = valid_generator.matrix()
    assert np.array_equal(valid_generator.transformation_matrix, matrix_func_return)
