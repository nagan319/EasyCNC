"""
Author: nagan319
Date: 2024/06/12
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap

from ..models.plate_model import Plate, PlateConstants
from ..controllers.plate_controller import PlateController
from ..utils.input_parser import InputParser

from ..views.image_editor_status import ImageEditorStatus
from ..views.image_editor_window import ImageEditorWindow

from ..logging import logger

class PlateWidget(QWidget):
    """
    Widget for displaying plate information.
    """

    deleteRequested = pyqtSignal(str)

    MAX_VALUES = {
        "x": PlateConstants.MAX_X,
        "y": PlateConstants.MAX_Y,
        "z": PlateConstants.MAX_Z,
    }

    FIELD_DEFINITIONS = {
        "x": ("Plate x dimension:", f"0-{MAX_VALUES['x']}", 'x'),
        "y": ("Plate y dimension:", f"0-{MAX_VALUES['y']}", 'y'),
        "z": ("Plate z dimension:", f"0-{MAX_VALUES['z']}", 'z'),
        "material": ("Material:", "", PlateConstants.DEFAULT_MATERIAL),
    }

    def __init__(self, plate_id: str, preview_path: str, controller: PlateController, image_editor_status: ImageEditorStatus):
        super().__init__()
        self.id = plate_id
        self.preview_path = preview_path
        self.fields = {}
        self.controller = controller

        self.image_editor_status = image_editor_status

        self.preview_widget = self._get_preview_widget()
        self.editable_fields_widget = self._get_editable_fields_widget()

        layout = QVBoxLayout()
        layout.addWidget(self.preview_widget)
        layout.addWidget(self.editable_fields_widget)
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

        for field_name, (label_text, placeholder_text, attribute_name) in self.FIELD_DEFINITIONS.items():
            field_layout, input_field = self._create_input_field(label_text, placeholder_text, self.controller.get_attribute(self.id, attribute_name))
            layout.addLayout(field_layout)
            self.fields[field_name] = input_field

        button_widget = QWidget()
        button_layout = QHBoxLayout()
        import_image_button = QPushButton("Import Image")
        import_image_button.pressed.connect(self.on_image_imported)
        save_button = QPushButton("Save")
        save_button.pressed.connect(self.on_save_requested)
        delete_button = QPushButton("Delete")
        delete_button.pressed.connect(self.on_delete_requested)
        button_layout.addStretch(1)
        button_layout.addWidget(import_image_button, 2)
        button_layout.addWidget(save_button, 1)
        button_layout.addWidget(delete_button, 1)
        button_layout.addStretch(1)
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        widget.setLayout(layout)
        return widget

    def update_preview(self):
        """ Update plate preview."""
        image = QPixmap(self.preview_path)
        self.preview_widget.setPixmap(image)

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
        try:
            plate_id = self.id
            self.controller.edit_x(plate_id, float(self.fields["x"].text()))
            self.controller.edit_y(plate_id, float(self.fields["y"].text()))
            self.controller.edit_z(plate_id, float(self.fields["z"].text()))
            self.update_preview()
        except ValueError as ve:
            QMessageBox.critical(self, "Error", f"Invalid input: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occured while updating the plate: {e}")

    def on_image_imported(self):
        """User chooses to import image."""
        plate = self.controller.get_by_id(self.id)
        controller = self.controller
        if self.image_editor_status.initialized:
            QMessageBox.warning(self, "Warning", "Image editor window is already initialized.")
            return
        self.image_editor_status.initialized = True
        self.image_editor_window = ImageEditorWindow(self.controller.session, plate)
        self.image_editor_window.imageEditorClosed.connect(self.on_image_editor_closed)

    def on_image_editor_closed(self):
        """ Image editor is closed. """
        self.image_editor_status.initialized = False

    def on_delete_requested(self):
        """ User deletes widget. """
        self.deleteRequested.emit(self.id)
