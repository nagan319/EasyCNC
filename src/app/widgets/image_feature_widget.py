"""
Author: nagan319
Date: 2024/06/13
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QPixmap

from ..widgets.interactive_preview import InteractivePreview

import enum

from ..controllers.image_editing_controller import ImageEditingController

from ..translations import image_feature_widget

class Mode(enum.Enum):
    ADD_MISSING_CORNERS = 0
    REMOVE_EXCESS_FEATURES = 1

class ImageFeatureWidget(QWidget):
    """
    Widget for extracting and managing image features.
    """
    featuresFinalized = pyqtSignal()

    def __init__(self, controller: ImageEditingController, min_height: int, language: int):
        super().__init__()

        self.texts = image_feature_widget
        self.language = language

        self.controller = controller
        self.min_height = min_height
        self.mode = None
        self._setup_ui()

    def _setup_ui(self):
        layout_with_margins = QHBoxLayout()

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        top_bar = QWidget()
        top_layout = QHBoxLayout()

        self.corner_counter = QLabel()
        self.corner_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.delete_button = QPushButton(self.texts['delete_selection_text'][self.language])
        self.delete_button.pressed.connect(self.on_delete_button_pressed)

        top_layout.addWidget(self.corner_counter, 1)
        top_layout.addStretch(2)
        top_layout.addWidget(self.delete_button, 1)
        top_bar.setLayout(top_layout)

        self.preview_widget = InteractivePreview()
        self.preview_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_widget.inputDetected.connect(self.on_mouse_clicked)

        self.mode_label = QLabel()
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.save_button_widget = self._get_save_button_widget()

        main_layout.addWidget(top_bar)
        main_layout.addWidget(self.preview_widget)
        main_layout.addWidget(self.mode_label)
        main_layout.addWidget(self.save_button_widget)
        main_widget.setLayout(main_layout)

        layout_with_margins.addStretch(1)
        layout_with_margins.addWidget(main_widget, 5)
        layout_with_margins.addStretch(1)
        self.setLayout(layout_with_margins)

    def _get_save_button_widget(self) -> QWidget:
        """ Button for saving features. """
        save_button_wrapper = QWidget()
        save_button_wrapper_layout = QHBoxLayout()

        save_button = QPushButton(self.texts['save_features_text'][self.language])
        save_button.pressed.connect(self.on_save_button_pressed)

        save_button_wrapper_layout.addStretch(2)
        save_button_wrapper_layout.addWidget(save_button, 1)
        save_button_wrapper_layout.addStretch(2)

        save_button_wrapper.setLayout(save_button_wrapper_layout)
        return save_button_wrapper     

    def update(self):
        """ 
        Update all necessary widgets and parameters. 
        """
        self.controller.save_image_features()

        amt_corners = len(self.controller.features.corners)

        ''' Update mode '''
        if amt_corners < 4:
            self.mode = Mode.ADD_MISSING_CORNERS
            self.controller.unselect_contour()
            self.controller.unselect_corner()
        else:
            self.mode = Mode.REMOVE_EXCESS_FEATURES

        ''' Update corner counter '''
        self.corner_counter.setText(f"{self.texts['corners_amt_text'][self.language]}{amt_corners}/4")

        ''' Update preview widget '''
        pixmap = QPixmap(self.controller.feat_path).scaledToHeight(int(self.min_height * .75))
        self.preview_widget.setPixmap(pixmap)
        
        ''' Update mode label '''
        mode_text = self.texts['add_corners_text'][self.language] \
            if self.mode == Mode.ADD_MISSING_CORNERS else \
                self.texts['remove_excess_text'][self.language]
        self.mode_label.setText(mode_text)

    def on_mouse_clicked(self, pos: tuple):
        """ User clicks on interactive preview. X needs to be adjusted slightly. """
        scale_factor = self.preview_widget.height() / self.controller.processing_resolution.h * 1.02
        scaled_pos = (int(pos[0] / scale_factor), int(pos[1] / scale_factor)) 
        if self.mode == Mode.ADD_MISSING_CORNERS:
            self.controller.add_corner(scaled_pos)
        elif not self.controller.check_feature_selected(scaled_pos):
            return 
        self.update()

    def on_delete_button_pressed(self):
        """ User chooses to delete a selected feature. """
        corner = self.controller.features.selected_corner_idx
        contour = self.controller.features.selected_contour_idx

        if corner is None and contour is None:
            return 
        if corner is not None:
            self.controller.remove_selected_corner()
        if contour is not None:
            self.controller.remove_selected_contour()

        self.update()

    def on_save_button_pressed(self):
        """ Features are finalized. """
        if self.controller.finalize_features():
            self.featuresFinalized.emit()
