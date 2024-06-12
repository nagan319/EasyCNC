from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap

from ..models.plate_model import Plate, PlateConstants
from ..utils.input_parser import InputParser

from ..logging import logger

class PlateWidget(QWidget):
    """
    Widget for displaying plate information.
    """

    deleteRequested = pyqtSignal(str)
    saveRequested = pyqtSignal(str, dict)

    MAX_VALUES = {
        "x": PlateConstants.MAX_X,
        "y": PlateConstants.MAX_Y,
        "z": PlateConstants.MAX_Z,
    }

    FIELD_DEFINITIONS = {
        "x": ("Plate x dimension:", f"0-{MAX_VALUES['x']}", PlateConstants.DEFAULT_X),
        "y": ("Plate y dimension:", f"0-{MAX_VALUES['y']}", PlateConstants.DEFAULT_Y),
        "z": ("Plate z dimension:", f"0-{MAX_VALUES['z']}", PlateConstants.DEFAULT_Z),
        "material": ("Material:", "", PlateConstants.DEFAULT_MATERIAL),
    }

    def __init__(self, plate_id: str, preview_path: str):
        super().__init__()
        self.id = plate_id
        self.preview_path = preview_path
        self.fields = {}

        preview_widget = self._get_preview_widget()
        editable_fields_widget = self._get_editable_fields_widget()

        layout = QVBoxLayout()
        layout.addWidget(preview_widget)
        layout.addWidget(editable_fields_widget)
        self.setLayout(layout)

    def _get_preview_widget(self) -> QLabel:
        """ Widget containing preview container. """
        widget = QLabel()
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image = QPixmap(self.preview_path)
        widget.setPixmap(image)
        return widget

    def _create_input_field(self, label_text: str, placeholder_text: str, default_value: str) -> QHBoxLayout:
        """ Helper function to create an input field with a label, placeholder, and default value. """
        layout = QHBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder_text)
        input_field.setText(str(default_value))
        input_field.editingFinished.connect(self.on_field_edited)
        layout.addWidget(label, 2)
        layout.addWidget(input_field, 1)
        return layout, input_field

    def _get_editable_fields_widget(self) -> QWidget:
        """ Widget containing editable fields and delete button. """
        widget = QWidget()
        layout = QVBoxLayout()

        for field_name, (label_text, placeholder_text, default_value) in self.FIELD_DEFINITIONS.items():
            field_layout, input_field = self._create_input_field(label_text, placeholder_text, default_value)
            layout.addLayout(field_layout)
            self.fields[field_name] = input_field

        button_widget = QWidget()
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.pressed.connect(self.on_save_requested)
        delete_button = QPushButton("Delete")
        delete_button.pressed.connect(self.on_delete_requested)
        button_layout.addStretch(1)
        button_layout.addWidget(save_button, 1)
        button_layout.addWidget(delete_button, 1)
        button_layout.addStretch(1)
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        widget.setLayout(layout)
        return widget

    def on_field_edited(self):
        """ Update field value when editing is finished. """
        sender = self.sender()
        for field_name, input_field in self.fields.items():
            if sender == input_field:
                max_value = self.MAX_VALUES.get(field_name, None)
                if max_value is not None:
                    parsed_value = InputParser.parse_text(sender.text(), 0, max_value)
                    sender.setText(str(parsed_value))
                break

    def on_save_requested(self):
        """ User presses save button. """
        updated_data = {}
        for field_name, input_field in self.fields.items():
            max_value = self.MAX_VALUES.get(field_name, None)
            if max_value is not None:
                updated_data[field_name] = InputParser.parse_text(input_field.text(), 0, max_value)
        self.saveRequested.emit(self.id, updated_data)

    def on_delete_requested(self):
        """ User deletes widget. """
        self.deleteRequested.emit(self.id)
