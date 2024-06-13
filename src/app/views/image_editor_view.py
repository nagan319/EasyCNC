"""
Author: nagan319
Date: 2024/06/12
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QStackedWidget

from sqlalchemy.orm import Session

import enum

from ..models.plate_model import Plate
from ..controllers.image_editing_controller import ImageEditingController

from ..widgets.image_load_widget import ImageLoadWidget
from ..widgets.image_threshold_widget import ImageThresholdWidget

from ...paths import IMAGE_PREVIEW_PATH

class EditorViews(enum.Enum):
    LOAD = 0
    THRESHOLD = 1
    FEATURES = 2
    FLAT = 3

class ImageEditorView(QStackedWidget):
    """
    View for processing image and detecting features.
    """
    def __init__(self, session: Session, plate: Plate, min_width: int, min_height: int):
        super().__init__()
        self.plate = plate
        self.controller = ImageEditingController(session, IMAGE_PREVIEW_PATH, self.plate)
        self.min_width = min_width
        self.min_height = min_height
        self._setup_ui()
    
    def _setup_ui(self):
        self.setCurrentIndex(EditorViews.LOAD.value)

        self.image_load_widget = ImageLoadWidget(self.controller)
        self.image_load_widget.imageImported.connect(self.on_image_imported)

        self.image_threshold_widget = ImageThresholdWidget(self.controller, self.min_height)
        self.image_threshold_widget.thresholdingFinalized.connect(self.on_thresholding_finalized)

        self.addWidget(self.image_load_widget)
        self.addWidget(self.image_threshold_widget)

    def on_image_imported(self):
        """ Image importing is finalized. """
        self.setCurrentIndex(EditorViews.THRESHOLD.value)
        self.image_threshold_widget.public_update()

    def on_thresholding_finalized(self):
        """ Binary is finalized. """
        print("Successfully imported binary.")
        '''
        self.setCurrentIndex(2)
        self.image_converter.initialize_features()
        self.image_converter.save_features()
        self.image_feature_widget.update()
        '''

    '''
    def on_features_finalized(self):
        self.setCurrentIndex(3)
        self.image_converter.save_flattened()
        self.image_flat_widget.update()

    def on_image_saved(self):
        self.editingFinished.emit()
    '''