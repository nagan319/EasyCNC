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
from src.app.controllers.router_controller import RouterController
from src.app.models.router_model import Router, RouterConstants

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture(scope="module")
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope="module")
def Base():
    return Router.metadata 

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
    controller = RouterController(session, preview_image_directory)
    return controller

'''
Adding:
- test adding new router
- test adding when amount is already exceded
'''

def test_add_new(controller):
    new_router = controller.add_new()
    assert isinstance(new_router, Router)
    assert controller.get_amount() == 1

def test_add_when_amount_exceeded(controller):
    for _ in range(controller.MAX_ROUTER_AMOUNT):
        controller.add_new()
    new_router = controller.add_new()
    assert new_router is None
    assert controller.get_amount() == controller.MAX_ROUTER_AMOUNT

'''
Removing:
- test success
- test removing invalid index
'''

def test_remove_success(controller):
    router_id = controller.add_new().id
    assert controller.remove(router_id) is True
    assert controller.get_amount() == 0

def test_remove_invalid_index(controller):
    removed = controller.remove("invalid_id")
    assert removed is False
    assert controller.get_amount() == 0

'''
Accessing:
- test all accesor method success
'''

def test_get_x(controller):
    new_router = controller.add_new()
    assert controller.get_x(new_router.id) == RouterConstants.DEFAULT_X

def test_get_y(controller):
    new_router = controller.add_new()
    assert controller.get_y(new_router.id) == RouterConstants.DEFAULT_Y

def test_get_z(controller):
    new_router = controller.add_new()
    assert controller.get_z(new_router.id) == RouterConstants.DEFAULT_Z

def test_get_plate_x(controller):
    new_router = controller.add_new()
    assert controller.get_plate_x(new_router.id) == RouterConstants.DEFAULT_PLATE_X

def test_get_plate_y(controller):
    new_router = controller.add_new()
    assert controller.get_plate_y(new_router.id) == RouterConstants.DEFAULT_PLATE_Y

def test_get_plate_z(controller):
    new_router = controller.add_new()
    assert controller.get_plate_z(new_router.id) == RouterConstants.DEFAULT_PLATE_Z

def test_get_min_safe_dist_from_edge(controller):
    new_router = controller.add_new()
    assert controller.get_min_safe_dist_from_edge(new_router.id) == RouterConstants.DEFAULT_SAFE_DISTANCE

def test_get_drill_bit_diameter(controller):
    new_router = controller.add_new()
    assert controller.get_drill_bit_diameter(new_router.id) == RouterConstants.DEFAULT_DRILL_BIT_DIAMETER

def test_get_mill_bit_diameter(controller):
    new_router = controller.add_new()
    assert controller.get_mill_bit_diameter(new_router.id) == RouterConstants.DEFAULT_MILL_BIT_DIAMETER

'''
Modifying:
- test setting attribute to valid / invalid value
'''

def test_edit_name(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_name(new_router.id, "New Name")
    assert modified_router is not None
    assert modified_router.name == "New Name"

def test_edit_x(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_x(new_router.id, 20.0)
    assert modified_router is not None
    assert modified_router.x == 20.0

    modified_router = controller.edit_x(new_router.id, -5.0)
    assert modified_router is None

def test_edit_y(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_y(new_router.id, 20.0)
    assert modified_router is not None
    assert modified_router.y == 20.0

    modified_router = controller.edit_y(new_router.id, -5.0)
    assert modified_router is None

def test_edit_z(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_z(new_router.id, 20.0)
    assert modified_router is not None
    assert modified_router.z == 20.0

    modified_router = controller.edit_z(new_router.id, -5.0)
    assert modified_router is None

def test_edit_plate_x(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_x(new_router.id, 20.0)
    assert modified_router is not None
    assert modified_router.plate_x == 20.0

    modified_router = controller.edit_plate_x(new_router.id, -5.0)
    assert modified_router is None

def test_edit_plate_y(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_y(new_router.id, 20.0)
    assert modified_router is not None
    assert modified_router.plate_y == 20.0

    modified_router = controller.edit_plate_y(new_router.id, -5.0)
    assert modified_router is None

def test_edit_plate_z(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_z(new_router.id, 20.0)
    assert modified_router is not None
    assert modified_router.plate_z == 20.0

    modified_router = controller.edit_plate_z(new_router.id, -5.0)
    assert modified_router is None

# this doesn't work, fix
def test_edit_min_safe_dist_from_edge(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_min_safe_dist_from_edge(new_router.id, 5.0)
    assert modified_router is not None
    assert modified_router.min_safe_dist_from_edge == 5.0

    modified_router = controller.edit_min_safe_dist_from_edge(new_router.id, -5.0)
    assert modified_router is None

def test_edit_mill_bit_diameter(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_mill_bit_diameter(new_router.id, 5.0)
    assert modified_router is not None
    assert modified_router.mill_bit_diameter == 5.0

    modified_router = controller.edit_mill_bit_diameter(new_router.id, -5.0)
    assert modified_router is None

def test_edit_drill_bit_diameter(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_drill_bit_diameter(new_router.id, 5.0)
    assert modified_router is not None
    assert modified_router.drill_bit_diameter == 5.0

    modified_router = controller.edit_drill_bit_diameter(new_router.id, -5.0)
    assert modified_router is None

'''
Preview:
- test saving router preview image
'''

def test_save_preview(controller, temp_dir):
    new_router = controller.add_new()
    new_router.preview_path = controller._get_preview_image_path(new_router.id)
    controller.save_preview(new_router)
    assert os.path.exists(new_router.preview_path)
    assert os.path.getsize(new_router.preview_path) > 0
    