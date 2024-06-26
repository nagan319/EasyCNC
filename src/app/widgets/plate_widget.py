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

from ..utils.image_processing.image_editor_status import ImageEditorStatus
from ..views.image_editor_window import ImageEditorWindow

from ..translations import plate_widget
from ..logging import logger

class PlateWidget(QWidget):
    """
    Widget for displaying plate information.
    """

    deleteRequested = pyqtSignal(str)

    MAX_HEIGHT = 350

    def __init__(self, plate_id: str, preview_path: str, controller: PlateController, image_editor_status: ImageEditorStatus, language: int):
        super().__init__()

        self.texts = plate_widget
        self.language = language

        self.id = plate_id
        self.preview_path = preview_path
        self.fields = {}
        self.controller = controller

        self.max_values = {
            "x": PlateConstants.MAX_X,
            "y": PlateConstants.MAX_Y,
            "z": PlateConstants.MAX_Z,
        }

        self.field_definitions = {
            "x": (self.texts['plate_x_dim'][self.language], f"0-{self.max_values['x']}", 'x'),
            "y": (self.texts['plate_y_dim'][self.language], f"0-{self.max_values['y']}", 'y'),
            "z": (self.texts['plate_z_dim'][self.language], f"0-{self.max_values['z']}", 'z'),
            "material": (self.texts['plate_material'][self.language], "", 'material'),
        }

        self.image_editor_status = image_editor_status

        self.preview_widget = self._get_preview_widget()
        self.editable_fields_widget = self._get_editable_fields_widget()

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.preview_widget)
        layout.addWidget(self.editable_fields_widget)
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

    def _create_input_field(self, label_text: str, placeholder_text: str, value: str) -> QHBoxLayout:
        """ Helper function to create an input field with a label, placeholder, and default value. """
        layout = QHBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder_text)
        input_field.setText(str(value))
        input_field.editingFinished.connect(self.on_field_edited)
        layout.addWidget(label, 2)
        layout.addWidget(input_field, 1)
        return layout, input_field

    def _get_editable_fields_widget(self) -> QWidget:
        """ Widget containing editable fields and delete button. """
        widget = QWidget()
        layout = QVBoxLayout()

        for field_name, (label_text, placeholder_text, attribute_name) in self.field_definitions.items():
            value = self.controller.get_attribute(self.id, attribute_name)
            field_layout, input_field = self._create_input_field(label_text, placeholder_text, value)
            layout.addLayout(field_layout)
            self.fields[field_name] = input_field

        button_widget = QWidget()
        button_layout = QHBoxLayout()
        self.select_button = QPushButton(self.texts['select_text'][self.language])
        self.select_button.pressed.connect(self.on_select_pressed)
        import_image_button = QPushButton(self.texts['import_image_text'][self.language])
        import_image_button.pressed.connect(self.on_image_imported)
        save_button = QPushButton(self.texts['save_text'][self.language])
        save_button.pressed.connect(self.on_save_requested)
        delete_button = QPushButton(self.texts['delete_text'][self.language])
        delete_button.pressed.connect(self.on_delete_requested)
        button_layout.addStretch(1)
        button_layout.addWidget(import_image_button, 2)
        button_layout.addWidget(self.select_button, 1)
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
                max_value = self.max_values.get(field_name, None)
                if max_value is not None:
                    parsed_value = InputParser.parse_text(sender.text(), 0, max_value)
                    sender.setText(str(parsed_value))
                break

    def update_selection_status(self):
        """ Updates visuals to indicate selection status. """
        if self.controller.get_selected(self.id):
            self.preview_widget.setStyleSheet("QLabel {border: 2px solid #b7de70;}")
            self.select_button.setStyleSheet("QPushButton {background-color: #b7de70;}")
            self.select_button.setText(self.texts['unselect_text'][self.language])
        else:
            self.preview_widget.setStyleSheet("QLabel {border: 0px solid white;}")
            self.select_button.setStyleSheet("QPushButton {background-color: #eeeeee;}")
            self.select_button.setText(self.texts['select_text'][self.language])

    def on_save_requested(self):
        """ User presses save button. """
        try:
            plate_id = self.id
            self.controller.edit_x(plate_id, float(self.fields["x"].text()))
            self.controller.edit_y(plate_id, float(self.fields["y"].text()))
            self.controller.edit_z(plate_id, float(self.fields["z"].text()))
            self.controller.edit_material(plate_id, self.fields["material"].text())
            self.controller.save_preview(self.controller.get_by_id(plate_id))
            self.update_preview()
        except ValueError as ve:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language],
                f"{self.texts['invalid_input_text'][self.language]}{ve}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language], 
                f"{self.texts['error_updating_text'][self.language]}{e}"
            )

    def on_image_imported(self):
        """User chooses to import image."""
        plate = self.controller.get_by_id(self.id)
        controller = self.controller
        if self.image_editor_status.initialized:
            QMessageBox.warning(
                self, 
                self.texts['warning_title'][self.language],
                self.texts['img_editor_initialized_text'][self.language]
            )
            return
        self.image_editor_status.initialized = True
        self.image_editor_window = ImageEditorWindow(self.controller.session, plate, self.language)
        self.image_editor_window.imageEditorClosed.connect(self.on_image_editor_closed)

    def on_image_editor_closed(self):
        """ Image editor is closed. """
        self.image_editor_status.initialized = False
        self.update_preview()

    def on_select_pressed(self):
        """ User presses select / unselect button. """
        try:
            curr_status = self.controller.get_selected(self.id)
            self.controller.edit_selected(self.id, (not curr_status))
            self.update_selection_status()
        except Exception as e:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language], 
                f"{self.texts['selection_error_text'][self.language]}{e}"
            )

    def on_delete_requested(self):
        """ User deletes widget. """
        self.deleteRequested.emit(self.id)
