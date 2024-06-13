"""
Author: nagan319
Date: 2024/06/12
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel

from .view_template import ViewTemplate
from ..logging import logger

from ...paths import HELP_TEXT_PATH

class HelpView(ViewTemplate):
    """
    View for displaying help information.
    """
    def __init__(self):
        super().__init__()

        self._setup_ui()
        logger.debug("Successfully initialized HelpView.")

    def _setup_ui(self):
        """ Initialize widget ui. """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.content_widget)

        with open(HELP_TEXT_PATH, 'r') as file:
            text = file.read()
            file.close()

        help_text = QLabel()
        help_text.setText(text)  
        help_text.setWordWrap(True)
        self.content_layout.addWidget(help_text)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        main_widget.setLayout(main_layout)

        self.__init_template_gui__("Help", main_widget)

    def set_help_text(self, text: str):
        """ Set the help text content. """
        help_text = QLabel()
        help_text.setText(text)
        help_text.setWordWrap(True)
        self.content_layout.addWidget(help_text)
