"""
Author: nagan319
Date: 2024/06/12
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QStackedWidget

from sqlalchemy.orm import Session

from ..models.plate_model import Plate
from ..controllers.image_editing_controller import ImageEditingController

from ..widgets.image_load_widget import ImageLoadWidget

from ...paths import IMAGE_PREVIEW_PATH

class ImageEditorView(QStackedWidget):
    """
    View for processing image and detecting features.
    """
    def __init__(self, session: Session, plate: Plate):
        super().__init__()
        self.plate = plate
        self.controller = ImageEditingController(session, IMAGE_PREVIEW_PATH, self.plate) 
        self._setup_ui()
    
    def _setup_ui(self):
        self.setCurrentIndex(0)

        self.image_load_widget = ImageLoadWidget(self.controller)
        self.image_load_widget.imageImported.connect(self.on_image_imported)

        self.addWidget(self.image_load_widget)

        '''
        for widget in [
            self.image_load_widget,
            self.image_threshold_widget,
            self.image_feature_widget,
            self.image_flat_widget]:
            self.addWidget(widget)
        '''

    def on_image_imported(self):
        print("Works correctly")
        # self.setCurrentIndex(1)
        # self.image_threshold_widget.update()

    '''
    def on_binary_finalized(self):
        self.setCurrentIndex(2)
        self.image_converter.initialize_features()
        self.image_converter.save_features()
        self.image_feature_widget.update()

    def on_features_finalized(self):
        self.setCurrentIndex(3)
        self.image_converter.save_flattened()
        self.image_flat_widget.update()

    def on_image_saved(self):
        self.editingFinished.emit()
    '''