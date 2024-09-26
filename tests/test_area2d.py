"""
Author: nagan319
Date: 2024/09/26
"""

import pytest
from shapely.geometry import Polygon
from src.app.utils.packing.utils.rectangle2d import Rectangle2D
from src.app.utils.packing.utils.vector2d import Vector2D
from src.app.utils.packing.utils.area2d import Area2D  

'''
necessary tests:

initialization:
    id 
    id and shape that is shape
    id and shape that is rectangle2d
    id and points

get_bb:
    correctly returns bounding box
        test for various shapes

get_position:
    accurately returns position
        test for same shapes as get_bb

don't do add or subtract for now

move:
    shape is correctly moved and position updated (call get_position to check)
    test multiple vectors on same shape

place_in_position:
    test in same way as 'move'

rotate
    check shape rotating correctly

is_inside_area, is_inside_rect, intersection
    various checks that return T/F, edge cases

'''

@pytest.fixture
def sample_shape():
    """ Sample fixture for an Area2D object initialized with points. """
    points = [(0, 0), (4, 0), (4, 3), (0, 3)]
    return Area2D(id="test_shape", points=points)

@pytest.fixture
def sample_rect():
    """ Sample fixture for an Area2D object initialized with a rectangle. """
    rectangle = Rectangle2D(0, 0, 4, 3)  # Rectangle with min_x, min_y, width, height
    return Area2D(id="test_rect", shape=rectangle)

### Initialization Tests

def test_initialization_with_id():
    area = Area2D(id="test_area")
    assert area.id == "test_area"
    assert isinstance(area.shape, Polygon)

def test_initialization_with_shape(sample_shape):
    area_copy = Area2D(id="copy", shape=sample_shape)
    assert area_copy.shape.equals(sample_shape.shape)

def test_initialization_with_rectangle(sample_rect):
    area = Area2D(id="rect_area", shape=sample_rect)
    assert area.shape.equals(sample_rect.shape)

def test_initialization_with_points():
    points = [(0, 0), (4, 0), (4, 3), (0, 3)]
    area = Area2D(id="test_with_points", points=points)
    assert area.shape.equals(Polygon(points))

### Bounding Box Tests

def test_get_bb(sample_shape):
    bb = sample_shape.get_bb()
    assert bb.min_x == 0
    assert bb.min_y == 0
    assert bb.width == 4
    assert bb.height == 3

def test_get_bb_with_rect(sample_rect):
    bb = sample_rect.get_bb()
    assert bb.min_x == 0
    assert bb.min_y == 0
    assert bb.width == 4
    assert bb.height == 3

### Position Tests

def test_get_position(sample_shape):
    pos = sample_shape.get_position()
    assert pos == (0, 0)

def test_get_position_with_rect(sample_rect):
    pos = sample_rect.get_position()
    assert pos == (0, 0)

### Movement Tests

def test_move_shape(sample_shape):
    vector = Vector2D(2, 2)
    sample_shape.move(vector)
    pos = sample_shape.get_position()
    assert pos == (2, 2)

def test_move_shape_multiple(sample_shape):
    vector1 = Vector2D(1, 1)
    vector2 = Vector2D(3, -1)
    sample_shape.move(vector1)
    assert sample_shape.get_position() == (1, 1)
    sample_shape.move(vector2)
    assert sample_shape.get_position() == (4, 0)

### Place in Position Tests

def test_place_in_position(sample_shape):
    sample_shape.place_in_position(5, 5)
    pos = sample_shape.get_position()
    assert pos == (5, 5)

def test_place_in_position_with_rect(sample_rect):
    sample_rect.place_in_position(10, 10)
    pos = sample_rect.get_position()
    assert pos == (10, 10)

### Rotation Tests

def test_rotate_shape(sample_shape):
    sample_shape.rotate(90)
    bb = sample_shape.get_bb()
    assert bb.width == 3
    assert bb.height == 4  # After 90-degree rotation, dimensions should swap

def test_rotate_multiple(sample_shape):
    sample_shape.rotate(45)
    assert sample_shape.rotation == 45
    sample_shape.rotate(90)
    assert sample_shape.rotation == 135

### Inside Area and Intersection Tests

def test_is_inside_area(sample_shape, sample_rect):
    assert sample_shape.is_inside_area(sample_rect) == True

def test_is_inside_rect(sample_rect):
    container = Rectangle2D(0, 0, 10, 10)
    assert sample_rect.is_inside_rect(container) == True

def test_intersection(sample_shape):
    overlapping_shape = Area2D(points=[(2, 2), (6, 2), (6, 5), (2, 5)])
    assert sample_shape.intersection(overlapping_shape) == True

def test_no_intersection(sample_shape):
    non_overlapping_shape = Area2D(points=[(10, 10), (15, 10), (15, 15), (10, 15)], shift_to_origin=False)
    assert sample_shape.intersection(non_overlapping_shape) == False

