"""
Author: nagan319
Date: 2024/06/12
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap

from ..models.part_model import Part, PartConstants

from ..translations import part_widget
from ..logging import logger

class PartWidget(QWidget):
    """
    Widget for displaying part information.
    """

    deleteRequested = pyqtSignal(str)
    amountEdited = pyqtSignal(str, int)
    materialEdited = pyqtSignal(str, str)

    MAX_HEIGHT = 350

    def __init__(self, part_id: str, preview_path: str, language: int):
        super().__init__()
        self.id = part_id
        self.preview_path = preview_path

        self.texts = part_widget
        self.language = language

        preview_widget = self._get_preview_widget()
        editable_fields_widget = self._get_editable_fields_widget()

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(preview_widget)
        layout.addWidget(editable_fields_widget)
        layout.addStretch(1)
        self.setLayout(layout)
        self.setMaximumHeight(self.MAX_HEIGHT)

    def _get_preview_widget(self) -> QLabel:
        """ Widget containing preview container. """
        widget = QLabel()
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image = QPixmap(self.preview_path)
        widget.setPixmap(image)
        return widget

    def _get_editable_fields_widget(self) -> QWidget:
        """ Widget containing editable fields and delete button. """
        widget = QWidget()
        layout = QVBoxLayout()

        amount_layout = QHBoxLayout()
        amount_label = QLabel(self.texts['amount_text'][self.language])
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText(self.texts['amount_text'][self.language])
        self.amount_input.textEdited.connect(self.on_amount_edited)
        self.amount_input.setText("1")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)

        material_layout = QHBoxLayout()
        material_label = QLabel(self.texts['material_text'][self.language])
        self.material_input = QLineEdit()
        self.material_input.setPlaceholderText(self.texts['material_text'][self.language])
        self.material_input.textEdited.connect(self.on_material_edited)
        self.material_input.setText(PartConstants.DEFAULT_MATERIAL)
        material_layout.addWidget(material_label)
        material_layout.addWidget(self.material_input)

        button_layout = QHBoxLayout()
        delete_button = QPushButton(self.texts['delete_text'][self.language])
        delete_button.pressed.connect(self.on_delete_requested)
        button_layout.addWidget(delete_button)

        layout.addLayout(amount_layout)
        layout.addLayout(material_layout)
        layout.addLayout(button_layout)
        layout.addStretch(1)

        widget.setLayout(layout)
        return widget

    def on_amount_edited(self, text: str):
        """ User edits amount. """
        try: 
            new_amount = int(text)
            self.amountEdited.emit(self.id, new_amount)
            logger.debug(f"Changed amount to value {new_amount}")
        except ValueError:
            logger.warning(f"Attempted to change amount to invalid string: {text}")

    def on_material_edited(self, text: str):
        """ User edits material. """
        try: 
            self.amountEdited.emit(self.id, text)
            logger.debug(f"Changed amount to value {text}")
        except Exception as e:
            logger.warning(f"Encountered exception while changing material: {e}")

    def on_delete_requested(self):
        """ User deletes widget. """
        self.deleteRequested.emit(self.id)
