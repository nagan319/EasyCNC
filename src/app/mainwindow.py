"""
Author: nagan319
Date: 2024/06/10
"""

from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from typing import List

from .views.view_manager import ViewManager 
from .views.home_view import HomeView

from .widgets.nav_bar import NavBar

from .logging import logger

APP_TITLE = "EasyCNC"
MIN_WIDTH, MIN_HEIGHT = 1000, 600

class MainWindow(QMainWindow):
    """
    Main window of application.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)

        nav_buttons = [
            "Home"
        ]

        views = [
            HomeView()
        ]   

        nav_bar = NavBar(nav_buttons)
        view_manager = ViewManager(views)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) 
        layout.setSpacing(0)
        layout.addWidget(nav_bar, 2)
        layout.addWidget(view_manager, 8)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        logger.debug("Main window initialized successfully.")
