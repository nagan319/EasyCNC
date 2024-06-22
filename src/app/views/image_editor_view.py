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
from ..widgets.image_feature_widget import ImageFeatureWidget
from ..widgets.image_flat_widget import ImageFlatWidget

from ...paths import IMAGE_PREVIEW_PATH

from ..logging import logger

class EditorViews(enum.Enum):
    LOAD = 0
    THRESHOLD = 1
    FEATURES = 2
    FLAT = 3

class ImageEditorView(QStackedWidget):
    """
    View for processing image and detecting features.
    """
    editingFinished = pyqtSignal()

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

        self.image_feature_widget = ImageFeatureWidget(self.controller, self.min_height)
        self.image_feature_widget.featuresFinalized.connect(self.on_features_finalized)

        self.image_flat_widget = ImageFlatWidget(self.controller, self.min_height)
        self.image_flat_widget.flatFinalized.connect(self.on_flat_finalized)

        self.addWidget(self.image_load_widget)
        self.addWidget(self.image_threshold_widget)
        self.addWidget(self.image_feature_widget)
        self.addWidget(self.image_flat_widget)

    def on_image_imported(self):
        """ Image importing is finalized. """
        self.setCurrentIndex(EditorViews.THRESHOLD.value)
        self.image_threshold_widget.public_update()
        logger.debug("Image import finished.")

    def on_thresholding_finalized(self):
        """ Binary is finalized. """
        self.setCurrentIndex(EditorViews.FEATURES.value)
        self.controller.extract_image_features()
        self.image_feature_widget.update()
        logger.debug("Image thresholding finished.")

    def on_features_finalized(self):
        """ Features are finalized. """
        self.setCurrentIndex(EditorViews.FLAT.value)
        self.controller.get_flattened_contours()
        self.controller.save_flattened_image()
        self.image_flat_widget.update()
        logger.debug("Image features finalized.")

    def on_flat_finalized(self):
        """ Flattened image finalized. """
        logger.debug("Image flattening finalized.")
        self.editingFinished.emit()
