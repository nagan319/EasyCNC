from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap

from ..models.part_model import Part, PartConstants

from ..logging import logger

class PartWidget(QWidget):
    """
    Widget for displaying part information.
    """

    ''' Id and new value if applicable'''
    deleteRequested = pyqtSignal(str)
    amountEdited = pyqtSignal(str, int)
    materialEdited = pyqtSignal(str, str)

    def __init__(self, part_id: str, preview_path: str):
        super().__init__()
        self.id = part_id
        self.preview_path = preview_path

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

    def _get_editable_fields_widget(self) -> QWidget:
        """ Widget containing editable fields and delete button. """
        widget = QWidget()
        layout = QHBoxLayout()

        amount_input = QLineEdit()
        amount_input.setPlaceholderText("Amount")
        amount_input.textEdited.connect(self.on_amount_edited)
        amount_input.setText("1")

        material_input = QLineEdit()
        material_input.setPlaceholderText("Material")
        material_input.textEdited.connect(self.on_material_edited)
        material_input.setText(PartConstants.DEFAULT_MATERIAL)

        delete_button = QPushButton("Delete")
        delete_button.pressed.connect(self.on_delete_requested) 

        layout.addStretch(2)
        layout.addWidget(amount_input, 1)
        layout.addWidget(material_input, 1)
        layout.addWidget(delete_button, 1)
        layout.addStretch(2)

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
