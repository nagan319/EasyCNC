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

def test_preview_initialization(session, temp_dir):
    preview_image_directory = temp_dir
    amt_routers = RouterController.MAX_ROUTER_AMOUNT - 1
    router_ids = []

    for _ in range(amt_routers):
        router = Router()
        session.add(router)
        session.commit()
        router_ids.append(router.id)

    controller = RouterController(session, preview_image_directory)
    
    for router_id in router_ids:
        preview_image_path = controller._get_preview_image_path(router_id)
        assert os.path.exists(preview_image_path), f"Preview image path does not exist for router ID: {router_id}"

def test_add_new(controller):
    new_router = controller.add_new()
    assert isinstance(new_router, Router)
    assert controller.get_amount() == 1
    assert os.path.exists(controller._get_preview_image_path(new_router.id))

def test_add_when_amount_exceeded(controller):
    for _ in range(controller.MAX_ROUTER_AMOUNT):
        controller.add_new()
    new_router = controller.add_new()
    assert new_router is None
    assert controller.get_amount() == controller.MAX_ROUTER_AMOUNT

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

def test_edit_name_null_value(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_name(new_router.id, "")
    assert modified_router is None
    modified_router = controller.edit_name(new_router.id, None)
    assert modified_router is None

def test_edit_x(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_x(new_router.id, float(RouterConstants.MAX_ROUTER_DIMENSION-1))
    assert modified_router is not None
    assert modified_router.x == RouterConstants.MAX_ROUTER_DIMENSION-1

def test_edit_x_invalid(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_x(new_router.id, 0)
    assert modified_router is None

def test_edit_y(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_y(new_router.id, float(RouterConstants.MAX_ROUTER_DIMENSION-1))
    assert modified_router is not None
    assert modified_router.y == RouterConstants.MAX_ROUTER_DIMENSION-1

def test_edit_y_invalid(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_y(new_router.id, 0)
    assert modified_router is None

def test_edit_z(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_z(new_router.id, float(RouterConstants.MAX_ROUTER_DIMENSION-1))
    assert modified_router is not None
    assert modified_router.z == RouterConstants.MAX_ROUTER_DIMENSION-1

def test_edit_z_invalid(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_z(new_router.id, 0)
    assert modified_router is None

def test_edit_plate_x(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_x(new_router.id, float(RouterConstants.MAX_PLATE_DIMENSION-1))
    assert modified_router is not None
    assert modified_router.x == RouterConstants.MAX_PLATE_DIMENSION-1

def test_edit_plate_x_invalid(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_x(new_router.id, 0)
    assert modified_router is None

def test_edit_plate_y(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_y(new_router.id, float(RouterConstants.MAX_PLATE_DIMENSION-1))
    assert modified_router is not None
    assert modified_router.y == RouterConstants.MAX_PLATE_DIMENSION-1

def test_edit_plate_y_invalid(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_y(new_router.id, 0)
    assert modified_router is None

def test_edit_plate_z(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_z(new_router.id, float(RouterConstants.MAX_PLATE_DIMENSION-1))
    assert modified_router is not None
    assert modified_router.z == RouterConstants.MAX_PLATE_DIMENSION-1

def test_edit_plate_z_invalid(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_plate_z(new_router.id, 0)
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
    modified_router = controller.edit_mill_bit_diameter(new_router.id, float(RouterConstants.MAX_MILL_BIT_DIAMETER-1))
    assert modified_router is not None
    assert modified_router.mill_bit_diameter == RouterConstants.MAX_MILL_BIT_DIAMETER-1

def test_edit_mill_bit_diameter_invalid(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_mill_bit_diameter(new_router.id, 0)
    assert modified_router is None

def test_edit_drill_bit_diameter(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_drill_bit_diameter(new_router.id, float(RouterConstants.MAX_DRILL_BIT_DIAMETER-1))
    assert modified_router is not None
    assert modified_router.drill_bit_diameter == RouterConstants.MAX_DRILL_BIT_DIAMETER-1

def test_edit_drill_bit_diameter_invalid(controller):
    new_router = controller.add_new()
    modified_router = controller.edit_drill_bit_diameter(new_router.id, 0)
    assert modified_router is None

def test_save_preview(controller, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    controller.preview_image_directory = temp_dir
    new_router = controller.add_new()
    assert new_router is not None, "Failed to create a new plate."
    new_router_id = new_router.id
    preview_path = controller._get_preview_image_path(new_router_id)
    assert os.path.exists(preview_path), f"Preview path does not exist: {preview_path}"
    file_size = os.path.getsize(preview_path)
    assert file_size > 0, f"Preview file is empty: {preview_path}"
    print(f"Preview file size: {file_size}")
    