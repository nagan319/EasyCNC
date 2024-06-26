"""
Author: nagan319
Date: 2024/06/21
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap

from ..controllers.image_editing_controller import ImageEditingController

from ..translations import image_flat_widget

class ImageFlatWidget(QWidget):
    """
    Widget for viewing flattened images.
    """
    flatFinalized = pyqtSignal()

    def __init__(self, controller: ImageEditingController, min_height: int, language: int):
        super().__init__()

        self.texts = image_flat_widget
        self.language = language

        self.controller = controller
        self.min_height = min_height
        self._setup_ui()
        
    def _setup_ui(self):
        layout_with_margins = QHBoxLayout()

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.preview_widget = QLabel()
        self.preview_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        save_button_widget = self._get_save_button_widget()

        main_layout.addWidget(self.preview_widget, 1)
        main_layout.addWidget(save_button_widget, 0)
        main_widget.setLayout(main_layout)

        layout_with_margins.addStretch(1)
        layout_with_margins.addWidget(main_widget, 5)
        layout_with_margins.addStretch(1)

        self.setLayout(layout_with_margins)
    
    def _get_save_button_widget(self) -> QWidget:
        """ 
        Button to save flat contours and its wrapper.
        """
        save_button_wrapper = QWidget()
        save_button_wrapper_layout = QHBoxLayout()
        save_button = QPushButton(self.texts['save_button_text'][self.language])
        save_button.pressed.connect(self.on_save_button_pressed)

        save_button_wrapper_layout.addStretch(2)
        save_button_wrapper_layout.addWidget(save_button, 1)
        save_button_wrapper_layout.addStretch(2)
        save_button_wrapper.setLayout(save_button_wrapper_layout)
        return save_button_wrapper

    def update(self):
        """
        Updates preview to display flattened contours.
        """
        pixmap = QPixmap(self.controller.flat_path)
        scaled_pixmap = pixmap.scaledToHeight(int(self.min_height * .75))
        self.preview_widget.setPixmap(scaled_pixmap)

    def on_save_button_pressed(self):
        """ User presses save button. """
        self.controller.update_plate()
        self.flatFinalized.emit()
