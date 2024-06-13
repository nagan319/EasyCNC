from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap

from ..models.router_model import RouterConstants
from ..controllers.router_controller import RouterController
from ..utils.input_parser import InputParser

from ..logging import logger

class RouterWidget(QWidget):
    """
    Widget for displaying router information.
    """

    deleteRequested = pyqtSignal(str)

    MAX_VALUES = {
        "x": RouterConstants.MAX_ROUTER_DIMENSION,
        "y": RouterConstants.MAX_ROUTER_DIMENSION,
        "z": RouterConstants.MAX_ROUTER_DIMENSION,
        "plate_x": RouterConstants.MAX_PLATE_DIMENSION,
        "plate_y": RouterConstants.MAX_PLATE_DIMENSION,
        "plate_z": RouterConstants.MAX_PLATE_DIMENSION,
        "min_safe_dist_from_edge": RouterConstants.MAX_PLATE_DIMENSION // 2,
        "drill_bit_diameter": RouterConstants.MAX_DRILL_BIT_DIAMETER,
        "mill_bit_diameter": RouterConstants.MAX_MILL_BIT_DIAMETER
    }

    FIELD_DEFINITIONS = {
        "x": ("Router x dimension:", f"0-{MAX_VALUES['x']}", 'x'),
        "y": ("Router y dimension:", f"0-{MAX_VALUES['y']}", 'y'),
        "z": ("Router z dimension:", f"0-{MAX_VALUES['z']}", 'z'),
        "plate_x": ("Max plate x dimension:", f"0-{MAX_VALUES['plate_x']}", 'plate_x'),
        "plate_y": ("Max plate y dimension:", f"0-{MAX_VALUES['plate_y']}", 'plate_y'),
        "plate_z": ("Max plate z dimension:", f"0-{MAX_VALUES['plate_z']}", 'plate_z'),
        "min_safe_dist_from_edge": ("Minimum safe edge distance:", f"0-{MAX_VALUES['min_safe_dist_from_edge']}", 'min_safe_dist_from_edge'),
        "drill_bit_diameter": ("Drill bit diameter:", f"0-{MAX_VALUES['drill_bit_diameter']}", 'drill_bit_diameter'),
        "mill_bit_diameter": ("Mill bit diameter:", f"0-{MAX_VALUES['mill_bit_diameter']}", 'mill_bit_diameter')
    }

    def __init__(self, router_id: str, preview_path: str, controller: RouterController):
        super().__init__()
        self.id = router_id
        self.preview_path = preview_path
        self.fields = {}
        self.controller = controller  

        self.preview_widget = self._get_preview_widget()
        self.editable_fields_widget = self._get_editable_fields_widget()

        layout = QHBoxLayout()
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

        self.name_input = QLineEdit()
        self.name_input.setObjectName("nameInput")
        self.name_input.setPlaceholderText(self.controller.get_name(self.id))
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        for field_name, (label_text, placeholder_text, attribute_name) in self.FIELD_DEFINITIONS.items(): 
            field_layout, input_field = self._create_input_field(label_text, placeholder_text, self.controller.get_attribute(self.id, attribute_name))
            layout.addLayout(field_layout)
            self.fields[field_name] = input_field

        button_widget = QWidget()
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.pressed.connect(self.on_save_pressed)
        delete_button = QPushButton("Delete")
        delete_button.pressed.connect(self.on_delete_pressed)
        button_layout.addStretch(1)
        button_layout.addWidget(save_button, 1)
        button_layout.addWidget(delete_button, 1)
        button_layout.addStretch(1)
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        widget.setLayout(layout)
        return widget

    def update_preview(self):
        """ Update router preview."""
        image = QPixmap(self.preview_path)
        self.preview_widget.setPixmap(image)

    def on_field_edited(self):
        """ Update field value when editing is finished. """
        sender = self.sender()
        if sender == self.name_input:
            return
        for field_name, input_field in self.fields.items():
            if sender == input_field:
                max_value = self.MAX_VALUES.get(field_name, None)
                if max_value is not None:
                    parsed_value = InputParser.parse_text(sender.text(), 0, max_value)
                    sender.setText(str(parsed_value))
                break

    def on_save_pressed(self):
        """ User presses save button. """
        try:
            router_id = self.id
            self.controller.edit_name(router_id, self.name_input.text())
            self.controller.edit_x(router_id, float(self.fields["x"].text()))
            self.controller.edit_y(router_id, float(self.fields["y"].text()))
            self.controller.edit_z(router_id, float(self.fields["z"].text()))
            self.controller.edit_plate_x(router_id, float(self.fields["plate_x"].text()))
            self.controller.edit_plate_y(router_id, float(self.fields["plate_y"].text()))
            self.controller.edit_plate_z(router_id, float(self.fields["plate_z"].text()))
            self.controller.edit_min_safe_dist_from_edge(router_id, float(self.fields["min_safe_dist_from_edge"].text()))
            self.controller.edit_drill_bit_diameter(router_id, float(self.fields["drill_bit_diameter"].text()))
            self.controller.edit_mill_bit_diameter(router_id, float(self.fields["mill_bit_diameter"].text()))
            self.controller.save_preview(self.controller.get_by_id(router_id))
            self.update_preview()
        except ValueError as ve:
            QMessageBox.critical(self, "Error", f"Invalid input: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occured while updating the router: {e}")

    def on_delete_pressed(self):
        """ User deletes widget. """
        self.deleteRequested.emit(self.id)
