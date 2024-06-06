'''
Author: nagan319
Date: 2024/06/04
'''

import os
import pytest
import tempfile
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.controllers.plate_controller import PlateController
from src.app.models.plate_model import Plate, PlateConstants
from src.app.models.utils import serialize_array, deserialize_array

"""
Tests for PlateController class.

Test Coverage:
    - Initialization
        - Test all preview images from existing plates saved    
    - Add new plate
        - Test attempted add when max amount met
        - Test correct addition of empty plate
        - Test preview correctly saving
    - Remove plate
        // Directly inherits from superclass, no tests necessary
    - Get amount
        // Directly inherits from superclass, no tests necessary
    - Get x
        - Valid and correct value
    - Get y
        - Valid and correct value
    - Get Z
        - Valid and correct value
    - Get contours
        - Test null value
        - Test correct deserialization of serialized contour
    - Edit x
        - Valid and correct value
        - Out of bounds value does not affect data
    - Edit y
        - Valid and correct value
        - Out of bounds value does not affect data
    - Edit z
        - Valid and correct value
        - Out of bounds value does not affect data
    - Edit material
        - Test Null string no effect
        - Value is correctly modified otherwise
    - Edit contours
        - Test Null contour
        - Test invalid input contour
        - Test valid contour correct serialization and deserialization
    - Save preview
        - Test preview image saving correctly
        - Test output image size if possible (related to dpi)
"""

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture(scope="module")
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope="module")
def Base():
    return Plate.metadata 

@pytest.fixture(scope="module")
def session_factory(engine, Base):
    Base.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session

@pytest.fixture(scope="function")
def session(session_factory):
    session = session_factory()
    yield session
    session.close()

@pytest.fixture(scope="function", autouse=True)
def create_router_table(engine, Base):
    Base.create_all(engine)
    yield
    Base.drop_all(engine)

@pytest.fixture
def controller(session, temp_dir):
    preview_image_directory = temp_dir
    controller = PlateController(session, preview_image_directory)
    return controller

def test_preview_initialization(session, temp_dir):
    preview_image_directory = temp_dir
    amt_plates = PlateController.MAX_PLATE_AMOUNT - 1
    plate_ids = []

    for _ in range(amt_plates):
        plate = Plate()
        session.add(plate)
        plate_ids.append(plate.id)
    
    session.commit()

    controller = PlateController(session, preview_image_directory)
    
    for plate_id in plate_ids:
        preview_image_path = controller._get_preview_image_path(plate_id)
        assert os.path.exists(preview_image_path), f"Preview image path does not exist for plate ID: {plate_id}"

def test_add_when_amount_exceeded(controller):
    for _ in range(controller.MAX_PLATE_AMOUNT):
        controller.add_new()
    new_plate = controller.add_new()
    assert new_plate is None
    assert controller.get_amount() == controller.MAX_PLATE_AMOUNT

def test_add_new(controller):
    new_plate = controller.add_new()
    assert isinstance(new_plate, Plate)
    assert controller.get_amount() == 1
    assert os.path.exists(controller._get_preview_image_path(new_plate.id))

def test_get_amount(controller):
    assert controller.get_amount() == 0
    controller.add_new()
    assert controller.get_amount() == 1

def test_get_x(controller):
    new_plate = controller.add_new()
    assert controller.get_x(new_plate.id) == PlateConstants.DEFAULT_X

def test_get_y(controller):
    new_plate = controller.add_new()
    assert controller.get_y(new_plate.id) == PlateConstants.DEFAULT_Y

def test_get_z(controller):
    new_plate = controller.add_new()
    assert controller.get_z(new_plate.id) == PlateConstants.DEFAULT_Z

def test_get_contours(controller):
    new_plate = controller.add_new()
    assert controller.get_contours(new_plate.id) == None
    new_contour = np.array([1, 2, 3])
    serialized_contour = serialize_array(new_contour)
    controller._edit_item_attr(new_plate.id, 'contours', serialized_contour)
    retrieved_contour = controller.get_contours(new_plate.id)
    assert np.array_equal(retrieved_contour, new_contour)

def test_edit_x(controller):
    new_plate = controller.add_new()
    modified_plate = controller.edit_x(new_plate.id, PlateConstants.MAX_X-1)
    assert modified_plate is not None
    assert modified_plate.x == PlateConstants.MAX_X-1

def test_edit_x_invalid(controller):
    new_plate = controller.add_new()
    modified_plate = controller.edit_x(new_plate.id, 0)
    assert modified_plate is None

def test_edit_y(controller):
    new_plate = controller.add_new()
    modified_plate = controller.edit_y(new_plate.id, PlateConstants.MAX_Y-1)
    assert modified_plate is not None
    assert modified_plate.y == PlateConstants.MAX_Y-1

    modified_plate = controller.edit_y(new_plate.id, 0)
    assert modified_plate is None

def test_edit_y_invalid(controller):
    new_plate = controller.add_new()
    modified_plate = controller.edit_y(new_plate.id, 0)
    assert modified_plate is None

def test_edit_z(controller):
    new_plate = controller.add_new()
    modified_plate = controller.edit_z(new_plate.id, PlateConstants.MAX_Z-1)
    assert modified_plate is not None
    assert modified_plate.z == PlateConstants.MAX_Z-1

def test_edit_z_invalid(controller):
    new_plate = controller.add_new()
    modified_plate = controller.edit_z(new_plate.id, 0)
    assert modified_plate is None

def test_edit_material(controller):
    new_plate = controller.add_new()
    new_material = "Abazaz"
    modified_plate = controller.edit_material(new_plate.id, new_material)
    assert modified_plate is not None
    assert modified_plate.material == new_material

def test_edit_material_null_value(controller):
    new_plate = controller.add_new()
    assert controller.edit_material(new_plate.id, "") is None
    assert controller.edit_material(new_plate.id, None) is None

def test_edit_contours(controller):
    new_plate = controller.add_new()
    new_contour = np.array([1, 2, 3])
    modified_plate = controller.edit_contours(new_plate.id, new_contour)
    assert modified_plate is not None
    assert modified_plate.contour == serialize_array(new_contour)

def test_edit_contours_null_contour(controller):
    new_plate = controller.add_new()
    assert controller.edit_contours(new_plate.id, None) is not None
    assert controller.edit_contours(new_plate.id, np.array([])) is not None

def test_save_preview(controller, temp_dir):
    new_plate = controller.add_new()
    new_plate.preview_path = controller._get_preview_image_path(new_plate.id)
    assert os.path.exists(new_plate.preview_path)
    assert os.path.getsize(new_plate.preview_path) > 0
    