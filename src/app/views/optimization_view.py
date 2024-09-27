import os
import json

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, 
    QPushButton, QMessageBox, QScrollArea, QTextEdit
)
from .view_template import ViewTemplate
from PyQt6.QtGui import QPixmap

from sqlalchemy.orm import Session

from src.app.controllers.optimization_controller import OptimizationController

from ..translations import optimization_view
from ..logging import logger

from ..utils.settings_enum import CONVERSION_FACTORS

from ...paths import LAYOUT_PREVIEW_PATH

class OptimizationView(ViewTemplate):
    """
    View for displaying placement optimization. 
    """
    def __init__(self, session: Session, language: int, units: int):
        super().__init__()

        self.texts = optimization_view
        self.language = language
        self.units = units

        self.controller = OptimizationController(session, LAYOUT_PREVIEW_PATH, CONVERSION_FACTORS[self.units])

        self.session = session
        self._setup_ui()
        logger.debug("Successfully initialized OptimizationView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.generate_button = QPushButton(self.texts['generate_button_text'][self.language])
        self.generate_button.pressed.connect(self.generate_layout)

        generate_button_wrapper = QWidget()
        generate_button_wrapper_layout = QHBoxLayout()
        generate_button_wrapper_layout.addStretch(1)
        generate_button_wrapper_layout.addWidget(self.generate_button, 2)
        generate_button_wrapper_layout.addStretch(1)
        generate_button_wrapper.setLayout(generate_button_wrapper_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True) 

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.preview_widget = QLabel()
        self.preview_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_widget = QLabel()
        self.text_widget.setWordWrap(True)
        self.text_widget.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.scroll_layout.addWidget(self.preview_widget)
        self.scroll_layout.addWidget(self.text_widget, 1)

        self.scroll_area.setWidget(self.scroll_content)

        main_layout.addWidget(generate_button_wrapper)
        main_layout.addWidget(self.scroll_area, 1) 

        main_widget.setLayout(main_layout)

        self.__init_template_gui__(self.texts['view_name'][self.language], main_widget)

    def generate_layout(self):
        """ Generate optimized part placement layout. """
        try:
            self.controller.optimize()
            pixmap = QPixmap(LAYOUT_PREVIEW_PATH)
            self.preview_widget.setPixmap(pixmap)
            formatted_text = json.dumps(self.controller.placements, indent=4)
            self.text_widget.setText(formatted_text)
        except Exception as e:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language], 
                self.texts['layout_error_text'][self.language]+f" {e}"
            )
            logger.error(f"Error generating layout: {str(e)}")
