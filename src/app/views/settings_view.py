"""
Author: nagan319
Date: 2024/06/25
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .view_template import ViewTemplate
from ..logging import logger

class SettingsView(ViewTemplate):
    """
    View for displaying settings information.
    """
    def __init__(self):
        super().__init__()

        self._setup_ui()
        logger.debug("Successfully initialized SettingsView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.__init_template_gui__("Settings", main_widget)
