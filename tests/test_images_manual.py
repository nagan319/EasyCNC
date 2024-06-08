"""
Author: nagan319
Date: 2024/06/08
"""

import os
import sys
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.models.plate_model import Plate
from src.app.controllers.image_editing_controller import ImageEditingController
from src.app.utils.image_processing.feature_plotter import FeaturePlotter
from src.app.utils.image_processing.utils import Size

"""
Saves images to real directory to assess processor quality.
"""

def test_images_manual():

    engine = create_engine('sqlite:///:memory:')

    session = sessionmaker(bind=engine)
    test_directory = 'image test dir'
    plate = Plate(x=1000, y=2000, z=100)

    src_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test data', 'images', 'image5.jpeg')

    controller = ImageEditingController(session, test_directory, plate)

    print(f"src saved: {controller.save_src_image(src_image_path)}")
    print(f"binary saved: {controller.save_binary_image(128)}")
    controller.finalize_binary()
    print(f"features extracted: {controller.extract_image_features()}")
    generate_report(controller)
    print(f"features saved: {controller.save_image_features()}")
    plotter = FeaturePlotter(dst_path=os.path.join(test_directory, "plotting.png"), size=controller.processing_resolution, features=controller.features)
    plotter.save_features()

def generate_report(controller: ImageEditingController):
    string = f"""
        plate contour: {controller.features.plate_contour[:50]}
        other contours: {len(controller.features.other_contours)}
        corners: {controller.features.corners}
    """
    path = os.path.join(controller.image_editing_directory, "report.txt")
    with open(path, 'w') as file:
        file.write(string)
    file.close()
