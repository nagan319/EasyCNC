"""
Author: nagan319
Date: 2024/06/25
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox
from .view_template import ViewTemplate

from ..controllers.user_settings_controller import UserSettingsController, LanguageEnum, UnitsEnum

from ..logging import logger

class SettingsView(ViewTemplate):
    """
    View for displaying settings information.
    """
    def __init__(self, user_settings_path: str):
        super().__init__()

        self.controller = UserSettingsController(user_settings_path)

        self._setup_ui()
        logger.debug("Successfully initialized SettingsView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        language_layout = QHBoxLayout()

        MIN_ELEM_WIDTH = 120

        self.language_label = QLabel("Language:")
        self.language_label.setMinimumWidth(MIN_ELEM_WIDTH)
        self.language_combo = QComboBox()
        self.language_combo.setMinimumWidth(MIN_ELEM_WIDTH)
        self.language_combo.addItems([e.name for e in LanguageEnum])
        self.language_combo.setCurrentText(self.controller.get_user_language().name)
        language_layout.addStretch(1)
        language_layout.addWidget(self.language_label)
        language_layout.addWidget(self.language_combo)
        language_layout.addStretch(1)
        main_layout.addLayout(language_layout)

        units_layout = QHBoxLayout()

        self.units_label = QLabel("Units:")
        self.units_label.setMinimumWidth(MIN_ELEM_WIDTH)
        self.units_combo = QComboBox()
        self.units_combo.setMinimumWidth(MIN_ELEM_WIDTH)
        self.units_combo.addItems([e.name for e in UnitsEnum])
        self.units_combo.setCurrentText(self.controller.get_user_units().name)
        units_layout.addStretch(1)
        units_layout.addWidget(self.units_label)
        units_layout.addWidget(self.units_combo)
        units_layout.addStretch(1)
        main_layout.addLayout(units_layout)

        save_button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        save_button_layout.addStretch(2)
        save_button_layout.addWidget(self.save_button)
        save_button_layout.addStretch(2)
        main_layout.addLayout(save_button_layout)

        main_layout.addStretch(1)
        main_widget.setLayout(main_layout)
        self.__init_template_gui__("Settings", main_widget)

    def save_settings(self):
        """ Save settings to the controller. """
        try:
            language = LanguageEnum[self.language_combo.currentText()]
            units = UnitsEnum[self.units_combo.currentText()]
            
            self.controller.set_user_language(language)
            self.controller.set_user_units(units)

            QMessageBox.information(self, "Settings Saved", "Your settings have been saved successfully.")
        except KeyError as e:
            logger.error(f"Invalid setting value: {e}")
            QMessageBox.critical(self, "Error", "Invalid settings values. Please check your input and try again.")
