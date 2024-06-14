"""
Author: nagan319
Date: 2024/06/11
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QMessageBox
from .view_template import ViewTemplate
from .image_editor_status import ImageEditorStatus
from ..widgets.plate_widget import PlateWidget
from ..controllers.plate_controller import PlateController
from ..logging import logger

class PlateView(ViewTemplate):
    """
    View for handling plates. 
    """
    def __init__(self, session, plate_preview_dir: str):
        super().__init__()

        self.controller = PlateController(session, plate_preview_dir)
        self.widget_map = {}

        self.image_editor_status = ImageEditorStatus()

        self._setup_ui()
        self.populate_plate_widgets()
        logger.debug("Successfully initialized PlateView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        self.import_button = QPushButton("Add New Plate")
        self.import_button.pressed.connect(self.add_plate)

        import_button_wrapper = QWidget()
        import_button_wrapper_layout = QHBoxLayout()
        import_button_wrapper_layout.addStretch(2)
        import_button_wrapper_layout.addWidget(self.import_button, 1)
        import_button_wrapper_layout.addStretch(2)
        import_button_wrapper.setLayout(import_button_wrapper_layout)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area, 1)
        main_layout.addWidget(import_button_wrapper)
        main_widget.setLayout(main_layout)

        self.__init_template_gui__("Manage Stock", main_widget)
    
    def populate_plate_widgets(self):
        """ Populate the layout with existing plates from the database. """
        try:
            plates = self.controller.get_all()
            for plate in plates:
                plate_widget = PlateWidget(plate.id, self.controller._get_preview_image_path(plate.id), self.controller, self.image_editor_status)
                plate_widget.deleteRequested.connect(self.on_delete_requested)
                self.scroll_layout.addWidget(plate_widget)
                self.widget_map[plate.id] = plate_widget
                logger.debug(f"Plate widget added successfully for plate ID: {plate.id}")
            self._update_button_amount()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while populating plates: {e}")
            logger.error(f"Error populating plates: {str(e)}")

    def add_plate(self):
        """
        Add a new default plate.
        """
        try:
            plate = self.controller.add_new()
            
            if plate is not None:
                new_plate_widget = PlateWidget(plate.id, self.controller._get_preview_image_path(plate.id), self.controller, self.image_editor_status)
                new_plate_widget.deleteRequested.connect(self.on_delete_requested)
                self.scroll_layout.addWidget(new_plate_widget)
                self.widget_map[plate.id] = new_plate_widget
                self._update_button_amount()
                logger.debug(f"Default plate added successfully.")
            else:
                QMessageBox.warning(self, "Operation Failed", "A new plate could not be added.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while adding a new plate: {e}")
            logger.error(f"Error adding new plate: {str(e)}")

    def on_delete_requested(self, plate_id: str) -> None:
        """ Delete widget from db. """
        try:
            self.controller.remove(plate_id)
            widget = self.widget_map.pop(plate_id)
            widget.setParent(None) 
            widget.deleteLater()
            self._update_button_amount()
        except Exception as e:
            logger.error(f"Encountered exception while removing router from db: {e}")

    def _update_button_amount(self):
        """ Update the import button text to reflect the number of widgets in the layout. """
        try:
            self.import_button.setText(f"Add Plates: {self.controller.get_amount()}/{self.controller.MAX_PLATE_AMOUNT}")
        except Exception as e:
            logger.error(f"Encountered exception while updating amount widget: {e}")
