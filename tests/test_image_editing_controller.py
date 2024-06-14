"""
Author: nagan319
Date: 2024/06/07
"""

import os
import pytest
from pytest import raises
import tempfile
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.utils.image_processing.features import Features
from src.app.utils.image_processing.utils import Size
from src.app.models.plate_model import Plate, PlateConstants
from src.app.controllers.image_editing_controller import ImageEditingController, EditorState

"""
Tests for ImageController class.

IMPLEMENT CONTOUR TRANSFORMATION LOGIC

Test Coverage:
    Initialization:
        - invalid image editing directory
        - invalid plate dimesions
        - valid initialization
    Saving raw image:
        - attempt in wrong state
        - nonexistent image path
        - wrong filetype
        - successful import
        - correct state transition
        - correct resizing logic
    Saving binary image:
        - attempt in wrong state
        - invalid threshold values
        - successful save
        - correct state transition
    Extracting image features:
        - attempt in wrong state
        - successful extraction
        - correct state transition
    Saving image features:
        - attempt in wrong state
        - successful save
    Finalizing image features:
        - test successful state transition
"""

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def valid_raw_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'images', 'image5.jpeg')

@pytest.fixture
def valid_bin_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'images', 'image0bin.png')

@pytest.fixture
def wrong_filetype_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'stl files', 'RollerConnectorPlate.STL')

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
def create_plate_table(engine, Base):
    Base.create_all(engine)
    yield
    Base.drop_all(engine)

@pytest.fixture
def controller(session, temp_dir):
    image_editing_directory = temp_dir
    valid_plate = Plate(x=PlateConstants.MAX_X, y=PlateConstants.MAX_Y, z=PlateConstants.MAX_Z)  
    controller = ImageEditingController(session, image_editing_directory, valid_plate)
    return controller

def test_init_invalid_directory(session):
    with raises(FileNotFoundError):
        ImageEditingController(session, "invalid directory", Plate())

def test_init_invalid_plate_dimensions(temp_dir):
    with raises(ValueError):
        invalid_plate = Plate(x=-1, y=100, z=100)
        ImageEditingController(session, temp_dir, invalid_plate)

    with raises(ValueError):
        invalid_plate = Plate(x=100, y=0, z=100)
        ImageEditingController(session, temp_dir, invalid_plate)

    with raises(ValueError):
        invalid_plate = Plate(x=100, y=100, z=PlateConstants.MAX_X + 1)
        ImageEditingController(session, temp_dir, invalid_plate)

def test_init_valid_plate_dimensions(controller):
    assert controller.state == EditorState.RAW

def test_import_raw_invalid_state(controller, valid_raw_path):
    controller.state = EditorState.BINARY
    assert controller.save_src_image(valid_raw_path) == False

def test_import_invalid_path(controller):
    assert controller.save_src_image("random invalid path") == False

def test_import_wrong_filetype(controller, wrong_filetype_path):
    assert controller.save_src_image(wrong_filetype_path) == False

def test_successful_import(controller, valid_raw_path):
    assert controller.save_src_image(valid_raw_path) == True
    assert controller.src_image_path == valid_raw_path
    assert controller.state == EditorState.BINARY
    assert os.path.exists(controller.raw_path)

def test_get_resized_image_upscale():
    image = np.zeros((500, 500, 3), dtype=np.uint8)
    max_size = Size(1000, 1000)
    resized_image = ImageEditingController._resize_image(image, max_size)
    assert resized_image.shape[:2] == (1000, 1000)

def test_get_resized_image_downscale():
    image = np.zeros((2000, 2000, 3), dtype=np.uint8)
    max_size = Size(1000, 1000)
    resized_image = ImageEditingController._resize_image(image, max_size)
    assert resized_image.shape[:2] == (1000, 1000)

def test_get_resized_image_same_size():
    image = np.zeros((800, 800, 3), dtype=np.uint8)
    max_size = Size(800, 800)
    resized_image = ImageEditingController._resize_image(image, max_size)
    assert resized_image.shape[:2] == (800, 800)

def test_get_resized_image_different_dimensions():
    image = np.zeros((600, 800, 3), dtype=np.uint8)  
    max_size = Size(1000, 500)  
    resized_image = ImageEditingController._resize_image(image, max_size)
    assert resized_image.shape[:2] == (500, 667)

def test_get_resized_image_invalid_input():
    image = np.zeros((500, 500, 3), dtype=np.uint8)
    with pytest.raises(ValueError):
        resized_image = ImageEditingController._resize_image(image, Size(-100, -100))

    with pytest.raises(ValueError):
        resized_image = ImageEditingController._resize_image(image, Size(0, 0))

def test_save_binary_invalid_state(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    controller.state = EditorState.FEATURES
    assert controller.save_binary_image(128) == False

def test_save_binary_invalid_threshold(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    assert controller.save_binary_image(256) == False
    assert controller.save_binary_image(-1) == False
    assert controller.save_binary_image(122.6) == False

def test_save_binary_successful(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    assert controller.save_binary_image(128)
    assert os.path.exists(controller.bin_path)

def test_finalize_binary(controller):
    controller.state = EditorState.BINARY
    assert controller.finalize_binary() == True
    assert controller.state == EditorState.FEATURES
    assert controller.finalize_binary() == False

def test_extract_features_invalid_state(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    controller.save_binary_image(128)
    controller.state = EditorState.RAW
    assert controller.extract_image_features() == False

def test_extract_features_successful(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    controller.save_binary_image(128)
    controller.finalize_binary()
    assert controller.extract_image_features() == True
    assert controller.features.plate_contour is not None
    assert len(controller.features.other_contours) > 0
    assert len(controller.features.corners) == 3
    assert controller.features.selected_corner_idx is None
    assert controller.features.selected_contour_idx is None
    assert controller.state == EditorState.FEATURES_EXTRACTED

def test_select_corner(controller):
    controller.features = Features(corners=[(1, 1), (2, 2)], selected_corner_idx=None)
    controller.select_corner(1)
    assert controller.features.selected_corner_idx == 1

def test_unselect_corner(controller):
    controller.features = Features(corners=[(1, 1), (2, 2)], selected_corner_idx=None)
    controller.select_corner(1)
    controller.unselect_corner()
    assert controller.features.selected_corner_idx is None

def test_select_contour(controller):
    controller.features = Features(other_contours=[np.array([[[1, 1]], [[2, 2]]])])
    controller.select_contour(0)
    assert controller.features.selected_contour_idx == 0

def test_unselect_contour(controller):
    controller.features = Features(other_contours=[np.array([[[1, 1]], [[2, 2]]])])
    controller.select_contour(1)
    controller.unselect_contour()
    assert controller.features.selected_contour_idx is None

def test_remove_selected_corner(controller):
    controller.features = Features(corners=[(1, 1), (2, 2), (3, 3)])
    controller.features.selected_corner_idx = 1
    controller.remove_selected_corner()
    assert controller.features.selected_corner_idx is None
    assert len(controller.features.corners) == 2

def test_remove_selected_contour(controller):
    controller.features = Features(other_contours=[np.array([[[1, 1]], [[2, 2]]])])
    controller.features.selected_contour_idx = 0
    controller.remove_selected_contour()
    assert controller.features.selected_contour_idx is None
    assert len(controller.features.other_contours) == 0  

def test_add_corner(controller):
    controller.features = Features(corners=[(1, 1), (2, 2), (3, 3)])
    controller.processing_resolution = Size(100, 100)
    amt_before = len(controller.features.corners)
    controller.add_corner((99, 99))
    assert len(controller.features.corners) == amt_before + 1

def test_add_corner_invalid_values(controller):
    controller.features = Features()
    controller.processing_resolution = Size(100, 100)
    assert controller.add_corner((-1, 0)) == False
    assert controller.add_corner((99, 100)) == False

def test_check_feature_selected_corner_match(controller):
    controller.features = Features(corners=[(26, 26)])
    assert controller.check_feature_selected((15, 15)) == True
    assert controller.features.selected_corner_idx == 0

def test_check_feature_selected_contour_match(controller):
    controller.features = Features(other_contours=np.array([[[7, 7]]]))
    assert controller.check_feature_selected((20, 20)) == True
    assert controller.features.selected_contour_idx == 0

def test_check_feature_selected_no_match(controller):
    controller.features = Features(corners=[(80, 80)])
    assert controller.check_feature_selected((100, 100)) == False
    assert controller.features.selected_corner_idx is None
    assert controller.features.selected_contour_idx is None

def test_save_image_features_invalid_state(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    controller.save_binary_image(128)
    controller.finalize_binary()
    controller.extract_image_features()
    controller.state = EditorState.RAW
    assert controller.save_image_features() == False

def test_save_image_features_successful(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    controller.save_binary_image(128)
    controller.finalize_binary()
    controller.extract_image_features()
    assert controller.save_image_features() == True
    assert os.path.exists(controller.feat_path)

def test_finalize_features(controller):
    controller.state = EditorState.FEATURES_EXTRACTED
    assert controller.finalize_features() == True
    assert controller.state == EditorState.FEATURES_FINALIZED
    assert controller.finalize_features() == False

'''
# make sure to check correct contour flattening using manual test

necessary additions:
    - test get flattened contours
        - wrong state
        - class variable updated correctly and makes sense
        - state transition
    - test save flattened image
        - wrong state
        - correct save logic
        - correct state transition
    - test update plate
        - wrong state
        - item in db gets updated correctly
'''

def test_get_flattened_contours_wrong_state(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    controller.save_binary_image(128)
    controller.finalize_binary()
    controller.extract_image_features()
    controller.save_image_features()
    controller.finalize_features()
    controller.state = EditorState.BINARY
    assert controller.get_flattened_contours == False

def test_get_flattened_contours_correct_extraction(controller, valid_raw_path):
    controller.save_src_image(valid_raw_path)
    controller.save_binary_image(128)
    controller.finalize_binary()
    controller.extract_image_features()
    controller.save_image_features()
    controller.finalize_features()
    assert controller.get_flattened_contours() == True
    assert len(controller.flattened_contours) == len(controller.features.other_contours)
