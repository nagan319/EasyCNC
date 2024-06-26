"""
Author: nagan319
Date: 2024/06/13
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt6.QtGui import QPixmap

from ..controllers.image_editing_controller import ImageEditingController

from ..translations import image_threshold_widget

class ImageThresholdWidget(QWidget):
    """
    Widget for applying binary threshold filter to image. 
    """
    thresholdingFinalized = pyqtSignal()

    COLOR_MIN = 0
    COLOR_MAX = 255
    COLOR_MID = (COLOR_MIN + COLOR_MAX)//2

    def __init__(self, controller: ImageEditingController, min_height: int, language: int):
        super().__init__()

        self.texts = image_threshold_widget
        self.language = language

        self.controller = controller
        self.min_height = min_height
        self.threshold = self.COLOR_MID
        self._setup_ui()

    def _setup_ui(self):
        layout_with_margins = QHBoxLayout()

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.preview_widget = QLabel()
        self.preview_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slider = self._get_slider()
        
        slider_label = self._get_slider_label()
        save_button_widget = self._get_save_button_widget()

        main_layout.addWidget(self.preview_widget, 3)
        main_layout.addWidget(slider_label, 0)
        main_layout.addWidget(self.slider, 1)
        main_layout.addWidget(save_button_widget, 0)
        main_widget.setLayout(main_layout)

        layout_with_margins.addStretch(1)
        layout_with_margins.addWidget(main_widget, 5)
        layout_with_margins.addStretch(1)

        self.setLayout(layout_with_margins)

    def _get_slider_label(self) -> QWidget:
        """ 
        Label to go above threshold slider. 
        """
        slider_label = QLabel(self.texts['slider_label'][self.language])
        slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return slider_label

    def _get_slider(self) -> QWidget:
        """ 
        Slider for controlling threshold.
        """
        slider = QSlider()
        slider.setOrientation(Qt.Orientation.Horizontal) 
        slider.setMinimum(self.COLOR_MIN)
        slider.setMaximum(self.COLOR_MAX)
        slider.setValue(self.COLOR_MID)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)  
        slider.setTickInterval
        slider.valueChanged.connect(self.on_threshold_parameter_edited)
        return slider

    def _get_save_button_widget(self) -> QWidget:
        """ 
        Button to save binary and its wrapper.
        """
        save_button_wrapper = QWidget()
        save_button_wrapper_layout = QHBoxLayout()
        save_button = QPushButton(self.texts['save_button'][self.language])
        save_button.pressed.connect(self.on_save_button_pressed)

        save_button_wrapper_layout.addStretch(2)
        save_button_wrapper_layout.addWidget(save_button, 1)
        save_button_wrapper_layout.addStretch(2)
        save_button_wrapper.setLayout(save_button_wrapper_layout)
        return save_button_wrapper

    def _update_display(self):
        pixmap = QPixmap(self.controller.bin_path)
        scaled_pixmap = pixmap.scaledToHeight(int(self.min_height * .75))
        self.preview_widget.setPixmap(scaled_pixmap)
    
    def public_update(self):
        """ External update method for when view is initialized. """
        self.on_threshold_parameter_edited(self.COLOR_MID)

    def on_threshold_parameter_edited(self, value: int):
        """ Save image with updated threshold value. """
        self.threshold = value
        self.controller.save_binary_image(self.threshold)
        self._update_display()

    def on_save_button_pressed(self):
        """ User presses save button. """
        self.controller.finalize_binary()
        self.thresholdingFinalized.emit()
