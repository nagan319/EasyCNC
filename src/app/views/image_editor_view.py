"""
Author: nagan319
Date: 2024/06/12
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QStackedWidget

from ..models.plate_model import Plate
from ..controllers.plate_controller import PlateController

class ImageEditorView(QStackedWidget):
    """
    View for processing image and detecting features.
    """
    def __init__(self, plate: Plate, controller: PlateController):
        super().__init__()
        