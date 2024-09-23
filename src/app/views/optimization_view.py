"""
Author: nagan319
Date: 2024/06/13
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMessageBox
from .view_template import ViewTemplate
from PyQt6.QtGui import QPixmap

from sqlalchemy.orm import Session

from src.app.controllers.optimization_controller import OptimizationController

from ..translations import optimization_view
from ..logging import logger

from ...paths import LAYOUT_PREVIEW_PATH

class OptimizationView(ViewTemplate):
    """
    View for displaying placement optimization. 
    """
    def __init__(self, session: Session, language: int):
        super().__init__()

        self.texts = optimization_view
        self.language = language

        self.controller = OptimizationController(session, LAYOUT_PREVIEW_PATH)

        self.session = session
        self._setup_ui()
        logger.debug("Successfully initialized OptimizationView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        self.generate_button = QPushButton("Generate Optimal Layout")
        self.generate_button.pressed.connect(self.generate_layout)

        generate_button_wrapper = QWidget()
        generate_button_wrapper_layout = QHBoxLayout()
        generate_button_wrapper_layout.addStretch(1)
        generate_button_wrapper_layout.addWidget(self.generate_button, 2)
        generate_button_wrapper_layout.addStretch(1)
        generate_button_wrapper.setLayout(generate_button_wrapper_layout)

        main_layout.addWidget(generate_button_wrapper)

        main_widget.setLayout(main_layout)

        self.__init_template_gui__(self.texts['view_name'][self.language], main_widget)

    def generate_layout(self):
        """ Generate optimized part placement layout. """
        try:
            self.controller.optimize()
        except Exception as e:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language], 
                f"{e}" # modify
            )
            logger.error(f"Error generating layout: {str(e)}")
