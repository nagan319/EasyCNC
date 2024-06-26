"""
Author: nagan319
Date: 2024/06/10
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QScrollArea, QMessageBox
from .view_template import ViewTemplate
from ..widgets.part_widget import PartWidget

from ..controllers.part_controller import PartController

from ..translations import part_view
from ..logging import logger

class PartView(ViewTemplate):
    """
    View for handling imported parts. 
    """
    def __init__(self, session, part_preview_dir: str, language: int, units: int):
        super().__init__()

        self.texts = part_view
        self.language = language
        self.units = units

        self.controller = PartController(session, part_preview_dir)
        self.controller.remove_all_with_previews()
        self.widget_map = {}

        self._setup_ui()
        logger.debug("Successfully initialized PartView.")

    def _setup_ui(self):
        """ 
        Initialize widget ui.
        """
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        self.import_button = QPushButton("Import Parts")
        self.import_button.pressed.connect(self.import_file)

        import_button_wrapper = QWidget()
        import_button_wrapper_layout = QHBoxLayout()
        import_button_wrapper_layout.addStretch(2)
        import_button_wrapper_layout.addWidget(self.import_button, 1)
        import_button_wrapper_layout.addStretch(2)
        import_button_wrapper.setLayout(import_button_wrapper_layout)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(import_button_wrapper)
        main_widget.setLayout(main_layout)

        self._update_button_amount()

        self.__init_template_gui__(self.texts['view_name'][self.language], main_widget)

    def import_file(self) -> None:
        """
        Import file from selected filepath and create a new widget if valid.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "STL Files (*.stl)")
        
        if file_path:
            try:
                part = self.controller.add_from_file(file_path)
                
                if part is not None:
                    new_part_widget = PartWidget(
                        part.id, 
                        self.controller._get_preview_image_path(part.id), 
                        self.language
                    )
                    new_part_widget.amountEdited.connect(self.on_amount_edited)
                    new_part_widget.materialEdited.connect(self.on_material_edited)
                    new_part_widget.deleteRequested.connect(self.on_delete_requested)
                    self.scroll_layout.addWidget(new_part_widget)
                    self.widget_map[part.id] = new_part_widget  
                    self._update_button_amount()
                    logger.debug(f"Part added successfully from {file_path}")

                else:
                    QMessageBox.warning(
                        self, 
                        self.texts['import_fail_title'][self.language], 
                        self.texts['import_fail_text'][self.language]
                    )
                    logger.warning(f"Failed to import part from {file_path}")

            except Exception as e:
                QMessageBox.critical(
                    self, 
                    self.texts['import_error_title'][self.language], 
                    f"{self.texts['import_error_text'][self.language]}{str(e)}"
                )
                logger.error(f"Error importing file {file_path}: {str(e)}")

    def on_material_edited(self, part_id: str, new_val: str) -> None:
        """ Update material stored in db to reflect ui change. """
        try: 
            self.controller.edit_material(part_id, new_val)
        except Exception as e:
            logger.error(f"Encountered exception while setting material of part {part_id} to {new_val}")

    def on_amount_edited(self, part_id: str, new_val: int) -> None:
        """ Update amount stored in db to reflect ui change. """
        try:
            self.controller.edit_amount(part_id, new_val)
            self._update_button_amount()
        except Exception as e:
            logger.error(f"Encountered exception while setting amount of part {part_id} to {new_val}")

    def on_delete_requested(self, part_id: str) -> None:
        """ Delete widget from db. """
        try:
            self.controller.remove(part_id)
            widget = self.widget_map.pop(part_id)
            widget.setParent(None) 
            widget.deleteLater()
            self._update_button_amount()
        except Exception as e:
            logger.error(f"Encountered exception while removing part from db: {e}")

    def _update_button_amount(self) -> None:
        """ Update to reflect amount of widgets in db."""
        try:
            self.import_button.setText(f"{self.texts['button_text'][self.language]}{self.controller.get_total_amount()}/{self.controller.MAX_PART_AMOUNT}")
        except Exception as e:
            logger.error(f"Encountered exception while updating amount widget: {e}")            

    def closeEvent(self):
        """ Clear out db and remove part previews. """
        try:
            self.controller.remove_all_with_previews()
        except Exception as e:
            logger.error(f"Encountered exception while clearing out part db: {e}")
