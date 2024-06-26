"""
Author: nagan319
Date: 2024/06/13
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog

from ..controllers.image_editing_controller import ImageEditingController

from ..utils.image_processing.constants import SUPPORTED_IMAGE_FORMATS_STR

from ..translations import image_load_widget

class ImageLoadWidget(QWidget):
    """
    Widget for handling image imports.
    """
    imageImported = pyqtSignal()

    def __init__(self, controller: ImageEditingController, language: int):
        super().__init__()

        self.texts = image_load_widget
        self.language = language

        self.controller = controller
        self._setup_ui()
    
    def _setup_ui(self):
        self.main_layout = QVBoxLayout()

        self.button_frame = QWidget()
        self.button_frame_layout = QHBoxLayout()
        self.import_button = QPushButton(self.texts['import_button_text'][self.language])
        self.import_button.pressed.connect(self.import_image_file)

        self.button_frame_layout.addStretch(2)
        self.button_frame_layout.addWidget(self.import_button, 1)
        self.button_frame_layout.addStretch(2)
        self.button_frame.setLayout(self.button_frame_layout)

        self.main_layout.addStretch(3)
        self.main_layout.addWidget(self.button_frame, 1)
        self.main_layout.addStretch(3)

        self.setLayout(self.main_layout)

    def import_image_file(self):
        """ Import an image file to use as src. """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", SUPPORTED_IMAGE_FORMATS_STR)
        self.controller.save_src_image(file_path)
        self.imageImported.emit()
