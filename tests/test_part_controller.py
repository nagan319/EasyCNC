'''
Author: nagan319
Date: 2024/06/03
'''

import os
import pytest
import tempfile
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.controllers.part_controller import PartController
from src.app.models.part_model import Part, PartConstants

"""
Tests for PartController.

Test Coverage:
    - Initialization
        // Directly inherits from superclass, no tests necessary
    - Add part from file
        - Test attempted add from invalid filepath
        - Test file of invalid type
        - Test valid file 
            - correct parameters
            - correct preview image generation
        - Test adding duplicates
    - Remove part
        // Directly inherits from superclass, no tests necessary
    - Remove all parts
        // Directly inherits from superclass, no tests necessary
    - Get total amount 
        - Zero parts in DB
        - Nonzero number of parts
    - Get filename 
        - Valid and correct value
    - Get thickness
        - Valid and correct value
    - Get material
        - Valid and correct value
    - Get contours
        - Test existing contours
        - Test empty contours
    - Get amount
        - Valid and correct value
    - Edit material
        - Test Null string no effect
        - Value is correctly modified otherwise
    - Edit amount
        - <0 for new amount handles smoothly
        - Does not accept amount if total exceeds maximum value
        - Value is correctly modified otherwise 
"""

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def stl_file_path_valid():
    parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'stl files')
    stl_file = os.path.abspath(os.path.join(parent_dir, 'RollerConnectorPlate.STL'))
    assert os.path.exists(stl_file), f"STL file {stl_file} does not exist"
    return stl_file

@pytest.fixture
def stl_file_path_invalid():
    parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'stl files')
    invalid_stl_file = os.path.abspath(os.path.join(parent_dir, 'invalid.STL'))
    assert os.path.exists(invalid_stl_file), f"Invalid STL file {invalid_stl_file} does not exist"
    return invalid_stl_file

@pytest.fixture
def non_stl_filepath():
    parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'images')
    non_stl_file = os.path.abspath(os.path.join(parent_dir, 'image5.jpeg'))
    assert os.path.exists(non_stl_file), f"Non-STL file {non_stl_file} does not exist"
    return non_stl_file

@pytest.fixture(scope="module")
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope="module")
def Base():
    return Part.metadata 

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
def create_part_table(engine, Base):
    Base.create_all(engine)
    yield
    Base.drop_all(engine)

@pytest.fixture
def controller(session, temp_dir):
    preview_image_directory = temp_dir
    controller = PartController(session, preview_image_directory)
    return controller

def test_add_part_from_nonexistent_file(controller):
    part = controller.add_from_file("invalid path")
    assert part is None

def test_add_part_from_invalid_file(controller, stl_file_path_invalid):
    part = controller.add_from_file(stl_file_path_invalid)
    assert part is None  # Importing an invalid file should return None

def test_add_from_wrong_file_type(controller, non_stl_filepath):
    part = controller.add_from_file(non_stl_filepath)
    assert part is None

# part attributes are checked when testing accessor methods
def test_add_part_from_valid_file(controller, stl_file_path_valid):
    part = controller.add_from_file(stl_file_path_valid)
    assert part is not None
    assert os.path.exists(controller._get_preview_image_path(part.id))

def test_add_duplicate(controller, stl_file_path_valid):
    initial = controller.add_from_file(stl_file_path_valid)
    duplicate = controller.add_from_file(stl_file_path_valid)
    assert initial is not None
    assert duplicate is None

def test_get_total_part_amount_empty_db(controller):
    assert controller.get_total_amount() == 0

def test_get_total_part_amount(controller, stl_file_path_valid):
    controller.add_from_file(stl_file_path_valid)
    controller.add_from_file(stl_file_path_valid)
    assert controller.get_total_amount() == 1  # Only one part should be imported as the second import is a duplicate

def test_get_filename(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.get_filename(part_id) == 'RollerConnectorPlate.STL'

def test_get_thickness(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.get_thickness(part_id) == 6.349999904632568

def test_get_material(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.get_material(part_id) == PartConstants.DEFAULT_MATERIAL

def test_get_contours(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert isinstance(controller.get_contours(part_id), np.ndarray)

def test_get_amount(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.get_amount(part_id) == 1

def test_edit_material(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.edit_material(part_id, 'new_material') is not None
    assert controller.get_material(part_id) == 'new_material'

def test_edit_material_null_value(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.edit_material(part_id, '') is None
    assert controller.edit_material(part_id, None) is None  
    assert controller.get_material(part_id) == PartConstants.DEFAULT_MATERIAL

def test_edit_amount(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.edit_amount(part_id, 2) is not None
    assert controller.get_amount(part_id) == 2

def test_edit_amount_invalid_value(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.edit_amount(part_id, 0) is None
    assert controller.edit_amount(part_id, 5.13) is None
    assert controller.edit_amount(part_id, -2) is None

def test_edit_amount_exceeds_maximum(controller, stl_file_path_valid):
    part_id = controller.add_from_file(stl_file_path_valid).id
    assert controller.edit_amount(part_id, controller.MAX_PART_AMOUNT+1) is None
    