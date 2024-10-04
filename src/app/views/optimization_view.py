import os
import json
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QScrollArea
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

        self.generated_layout = False
        self.saved_layout = False

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

        self.table_widget = QTableWidget()
        self.table_widget.setWordWrap(True)
        self.table_widget.setStyleSheet("border: none;")

        self.table_widget_layout = QHBoxLayout()
        self.table_widget_layout.addStretch(1)
        self.table_widget_layout.addWidget(self.table_widget, 100)
        self.table_widget_layout.addStretch(1)

        self.scroll_layout.addWidget(self.preview_widget)
        self.scroll_layout.addLayout(self.table_widget_layout)
        self.scroll_layout.addStretch(1)

        self.scroll_area.setWidget(self.scroll_content)

        self.save_button = QPushButton(self.texts['save_button_text'][self.language])
        self.save_button.pressed.connect(self.save_layout)

        save_button_wrapper = QWidget()
        save_button_wrapper_layout = QHBoxLayout()
        save_button_wrapper_layout.addStretch(1)
        save_button_wrapper_layout.addWidget(self.save_button, 2)
        save_button_wrapper_layout.addStretch(1)
        save_button_wrapper.setLayout(save_button_wrapper_layout)

        main_layout.addWidget(generate_button_wrapper)
        main_layout.addWidget(self.scroll_area, 1) 
        main_layout.addWidget(save_button_wrapper)

        main_widget.setLayout(main_layout)

        self.__init_template_gui__(self.texts['view_name'][self.language], main_widget)

    def generate_layout(self):
        """Generate optimized part placement layout and update the table."""
        if self.saved_layout == True:
            return

        try:
            self.controller.optimize()

            pixmap = QPixmap(LAYOUT_PREVIEW_PATH)
            self.preview_widget.setPixmap(pixmap)

            placements_data = self.controller.placements

            filtered_placements = {piece_id: placement_info for piece_id, placement_info in placements_data.items() if 'edge' not in piece_id and 'ctr' not in piece_id}

            self.table_widget.clearContents()
            self.table_widget.setRowCount(len(filtered_placements))
            self.table_widget.setColumnCount(3)
            self.table_widget.setHorizontalHeaderLabels(['Piece ID', 'Bin ID', 'Coordinates'])

            self.table_widget.setColumnWidth(0, 300)
            self.table_widget.setColumnWidth(1, 300)
            self.table_widget.setColumnWidth(2, 280)

            self.table_widget.setStyleSheet("border: 1px solid #cccccc;")

            for row_idx, (piece_id, placement_info) in enumerate(filtered_placements.items()):
                if placement_info is None:
                    bin_id = 'Not Placed'
                    coordinates_text = '-'
                else:
                    bin_id, coordinates = placement_info
                    if coordinates:
                        coordinates_text = f"({(coordinates[0]*CONVERSION_FACTORS[self.units]):.2f}, {(coordinates[1]*CONVERSION_FACTORS[self.units]):.2f})"
                    else:
                        coordinates_text = '-'

                self.table_widget.setItem(row_idx, 0, QTableWidgetItem(piece_id))
                self.table_widget.setItem(row_idx, 1, QTableWidgetItem(bin_id))
                self.table_widget.setItem(row_idx, 2, QTableWidgetItem(coordinates_text))

            row_height = 30
            self.table_widget.setFixedHeight(row_height * len(filtered_placements) + 50)
            self.table_widget.verticalScrollBar().setEnabled(False)

            self.generated_layout = True

        except Exception as e:
            QMessageBox.critical(
                self,
                self.texts['error_title'][self.language],
                self.texts['layout_error_text'][self.language] + f" {e}"
            )
            logger.error(f"Error generating layout: {str(e)}")


    def save_layout(self):
        """ Save added parts to plates in database """
        if not self.generated_layout or self.saved_layout:
            return

        try:
            self.controller.save_layout()
            self.saved_layout = True

            QMessageBox.information(
                self,
                self.texts['success'][self.language],
                self.texts['saved_successfully'][self.language]
            )

        except Exception as e:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language], 
                self.texts['layout_save_error_text'][self.language]+f" {traceback.format_exc()}"
            )
            logger.error(f"Error saving layout: {str(e)}")     
