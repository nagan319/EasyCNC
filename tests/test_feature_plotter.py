"""
Author: nagan319
Date: 2024/06/07
"""

import pytest

import os
import cv2
import numpy as np
from src.app.utils.image_processing.utils import Size, Colors
from src.app.utils.image_processing.features import Features

from src.app.utils.image_processing.feature_plotter import FeaturePlotter

"""
Tests for FeaturePlotter class.

Test coverage:
    - Initialization:
        Parameters are correctly initialized
    - Save features
        Image saves correctly
        Correct image resolution
"""

@pytest.fixture
def temp_dir(tmpdir):
    return tmpdir

def test_init():
    dst_path = "test_dst_path"
    size = Size(1000, 1000)
    colors = Colors(bg_col=(100, 100, 100), ctr_col=(33, 33, 33))
    features = Features(
        plate_contour=np.array([1, 2, 3]), 
        other_contours=[np.array([4, 5, 6]), np.array([7, 8, 9])], 
        corners=[(55, 22), (77, 23)], 
        selected_contour_idx=1, 
        selected_corner_idx=0)
    plotter = FeaturePlotter(dst_path, size, features, colors)
    
    assert plotter.dst_path == dst_path
    assert plotter.size.w == size.w and plotter.size.h == size.h
    assert np.array_equal(plotter.features.plate_contour, features.plate_contour)
    assert plotter.features.selected_contour_idx == features.selected_contour_idx

def test_save_features(temp_dir):
    dst_path = os.path.join(temp_dir, "test_image.png")
    size = Size(1000, 1000)
    colors = Colors(bg_col=(100, 100, 100), ctr_col=(33, 33, 33))
    features = Features(
        plate_contour=np.array([[[100, 200]], [[200, 200]], [[200, 300]], [[100, 300]]]), 
        other_contours=[np.array([[[400, 500]], [[500, 500]], [[500, 600]], [[400, 600]]])], 
        corners=[(150, 250), (450, 550)], 
        selected_contour_idx=0, 
        selected_corner_idx=1)
    
    plotter = FeaturePlotter(dst_path, size, features, colors)
    plotter.save_features()
    
    assert os.path.exists(dst_path)
    
    image = cv2.imread(dst_path)
    assert image.shape[1] == size.w
    assert image.shape[0] == size.h
