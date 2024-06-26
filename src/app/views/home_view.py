"""
Author: nagan319
Date: 2024/06/11
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap

from ..translations import home_view
from ..logging import logger

from ...paths import LOGO_PATH

class HomeView(QWidget):
    """
    Home widget containing app logo and version information.
    """

    def __init__(self, language: int):
        super().__init__()

        self.texts = home_view
        self.language = language

        layout = QVBoxLayout()

        logo_label = QLabel()
        logo_label.setPixmap(QPixmap(LOGO_PATH).scaledToWidth(1000))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        app_description_label = QLabel(self.texts['app_description_text'][self.language])

        layout.addStretch()
        layout.addWidget(logo_label)
        layout.addStretch()
        layout.addWidget(app_description_label)

        self.setLayout(layout)
        logger.debug(f"Initialized home view.")

