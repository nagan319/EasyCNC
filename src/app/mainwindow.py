"""
Author: nagan319
Date: 2024/06/10
"""

from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from typing import Dict

import json

from .views.view_manager import ViewManager 
from .views.home_view import HomeView
from .views.part_view import PartView
from .views.plate_view import PlateView
from .views.router_view import RouterView
from .views.optimization_view import OptimizationView
from .views.settings_view import SettingsView
from .views.help_view import HelpView
from .widgets.nav_bar import NavBar

from .utils.clear_dir import clear_dir
from .utils.settings_enum import DEFAULT_LANGUAGE, DEFAULT_UNITS

from .database import init_db, teardown_db, get_session, close_session
from ..paths import IMAGE_PREVIEW_PATH, PART_PREVIEW_PATH, PLATE_PREVIEW_PATH, ROUTER_PREVIEW_PATH, ICON_PATH, USER_SETTINGS_PATH

from .translations import main_window
from .logging import logger

APP_TITLE = "EasyCNC"
MIN_WIDTH, MIN_HEIGHT = 1200, 900

class MainWindow(QMainWindow):
    """
    Main window of application.
    """

    def __init__(self, user_settings: dict):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setMinimumSize(MIN_WIDTH, MIN_HEIGHT)

        self.setup_db()

        self.texts = main_window

        user_language = user_settings['language']
        user_units = user_settings['units']

        views = {
            self.texts['home_button'][user_language]: \
                HomeView(user_language),
            self.texts['part_button'][user_language]: \
                PartView(self.session, PART_PREVIEW_PATH, user_language, user_units),
            self.texts['stock_button'][user_language]: \
                PlateView(self.session, PLATE_PREVIEW_PATH, user_language),
            self.texts['router_button'][user_language]: \
                RouterView(self.session, ROUTER_PREVIEW_PATH, user_language),
            self.texts['layout_button'][user_language]: \
                OptimizationView(self.session, user_language),
            self.texts['settings_button'][user_language]: \
                SettingsView(USER_SETTINGS_PATH, user_language),
            self.texts['help_button'][user_language]: \
                HelpView(user_language)
        }

        nav_bar = NavBar(views.keys())
        view_manager = ViewManager(views.values())

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) 
        layout.setSpacing(0)
        layout.addWidget(nav_bar, 2)
        layout.addWidget(view_manager, 8)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        nav_bar.button_clicked.connect(view_manager.set_view)

        logger.debug("Main window initialized successfully.")

    def setup_db(self):
        """ Initialize database. """
        try:
            init_db()
            self.session = get_session()
            logger.debug("Database setup complete and session started.")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")   

    def closeEvent(self, event):
        """ Close application at exit. """
        try:
            if self.session:
                close_session()
                logger.debug("Database session closed.")
            teardown_db()
            logger.debug("Database connection disposed.")
            for directory in [IMAGE_PREVIEW_PATH, PART_PREVIEW_PATH, PLATE_PREVIEW_PATH, ROUTER_PREVIEW_PATH]:
                clear_dir(directory)
        except Exception as e:
            logger.error(f"Error closing database: {e}")
        event.accept()
