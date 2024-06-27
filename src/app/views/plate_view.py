"""
Author: nagan319
Date: 2024/06/11
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QMessageBox, QLineEdit
from .view_template import ViewTemplate
from ..widgets.plate_widget import PlateWidget

from ..utils.image_processing.image_editor_status import ImageEditorStatus
from ..utils.input_parser import InputParser
from ..utils.settings_enum import CONVERSION_FACTORS

from ..controllers.plate_controller import PlateController

from ..translations import plate_view
from ..logging import logger

class PlateView(ViewTemplate):
    """
    View for handling plates. 
    """
    def __init__(self, session, plate_preview_dir: str, language: int, units: int):
        super().__init__()

        self.texts = plate_view
        self.language = language
        self.units = units

        self.controller = PlateController(session, plate_preview_dir, CONVERSION_FACTORS[self.units])
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

        self.select_thickness_input = QLineEdit()
        self.select_thickness_input.setPlaceholderText(self.texts['thickness_placeholder'][self.language])
        self.select_thickness_input.setMinimumWidth(120)

        self.select_material_input = QLineEdit()
        self.select_material_input.setPlaceholderText(self.texts['material_placeholder'][self.language])
        self.select_material_input.setMinimumWidth(120)

        self.select_button = QPushButton(self.texts['select_property_text'][self.language])
        self.select_button.pressed.connect(self.on_select_by_property)

        self.import_button = QPushButton(self.texts['add_new_text'][self.language])
        self.import_button.pressed.connect(self.add_plate)

        selection_wrapper = QWidget()
        selection_wrapper_layout = QHBoxLayout()
        selection_wrapper_layout.addStretch(2)
        selection_wrapper_layout.addWidget(self.select_button, 2)  
        selection_wrapper_layout.addWidget(self.select_thickness_input, 1)
        selection_wrapper_layout.addWidget(self.select_material_input, 1)
        selection_wrapper_layout.addStretch(2)
        selection_wrapper.setLayout(selection_wrapper_layout)

        import_button_wrapper = QWidget()
        import_button_wrapper_layout = QHBoxLayout()
        import_button_wrapper_layout.addStretch(1)
        import_button_wrapper_layout.addWidget(self.import_button, 2)
        import_button_wrapper_layout.addStretch(1)
        import_button_wrapper.setLayout(import_button_wrapper_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(import_button_wrapper, 2)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(selection_wrapper, 2)
        bottom_layout.addStretch(1)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area, 1)
        main_layout.addLayout(bottom_layout)
        main_widget.setLayout(main_layout)

        self.__init_template_gui__(self.texts['view_name'][self.language], main_widget)
    
    def populate_plate_widgets(self):
        """ Populate the layout with existing plates from the database. """
        try:
            plates = self.controller.get_all()
            for plate in plates:
                plate_widget = PlateWidget(
                    plate.id, 
                    self.controller._get_preview_image_path(plate.id), 
                    self.controller, 
                    self.image_editor_status, 
                    self.language,
                    self.units
                )
                plate_widget.deleteRequested.connect(self.on_delete_requested)
                self.scroll_layout.addWidget(plate_widget)
                self.widget_map[plate.id] = plate_widget
                logger.debug(f"Plate widget added successfully for plate ID: {plate.id}")
            self._update_button_amount()
            self.on_selection_changed()
        except Exception as e:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language], 
                f"{self.texts['error_populating_text'][self.language]}{e}"
            )
            logger.error(f"Error populating plates: {str(e)}")

    def add_plate(self):
        """
        Add a new default plate.
        """
        try:
            plate = self.controller.add_new()
            if plate is not None:
                new_plate_widget = PlateWidget(
                    plate.id, 
                    self.controller._get_preview_image_path(plate.id), 
                    self.controller, 
                    self.image_editor_status, 
                    self.language,
                    self.units
                )
                new_plate_widget.deleteRequested.connect(self.on_delete_requested)
                self.scroll_layout.addWidget(new_plate_widget)
                self.widget_map[plate.id] = new_plate_widget
                self._update_button_amount()
                logger.debug(f"Default plate added successfully.")
            else:
                QMessageBox.warning(
                    self, 
                    self.texts['operation_failed_title'][self.language], 
                    self.texts['could_not_add_text'][self.language]
                )
        except Exception as e:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language], 
                f"{self.texts['error_adding_text'][self.language]}{e}"
            )
            logger.error(f"Error adding new plate: {str(e)}")

    def on_selection_changed(self) -> None:
        """ Changes selection status of all plates. """
        for plate_widget in self.widget_map.values():
            plate_widget.update_selection_status()

    def on_select_by_property(self):
        """ Selection based on material and thickness. """
        try:
            thickness = float(InputParser.parse_text(self.select_thickness_input.text())) / CONVERSION_FACTORS[self.units]
            material = self.select_material_input.text()
            if not self.controller.select_by_property(thickness, material):
                QMessageBox.critical(
                    self, 
                    self.texts['error_title'][self.language], 
                    self.texts['failed_to_select_plates_text'][self.language],
                )  
                return
            self.on_selection_changed()
        except ValueError:
            QMessageBox.warning(
                self, 
                self.texts['invalid_input_title'][self.language], 
                self.texts['invalid_input_text'][self.language]
            )
        except AttributeError as e:
            QMessageBox.critical(
                self, 
                self.texts['error_title'][self.language],  
                f"{self.texts['plate_selection_error_text'][self.language]}{e}"
            )
            logger.error(f"Error selecting plates: {str(e)}")

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
            self.import_button.setText(f"{self.texts['add_new_text'][self.language]}{self.controller.get_amount()}/{self.controller.MAX_PLATE_AMOUNT}")
        except Exception as e:
            logger.error(f"Encountered exception while updating amount widget: {e}")
