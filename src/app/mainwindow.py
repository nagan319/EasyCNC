"""
Author: nagan319
Date: 2024/06/10
"""

from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from typing import List

from .views.view_manager import ViewManager 
from .views.home_view import HomeView
from .views.part_view import PartView
from .views.plate_view import PlateView
from .views.router_view import RouterView
from .widgets.nav_bar import NavBar

from .database import init_db, teardown_db, get_session, close_session
from ..paths import IMAGE_PREVIEW_PATH, PART_PREVIEW_PATH, PLATE_PREVIEW_PATH, ROUTER_PREVIEW_PATH

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

        self.setup_db()

        nav_buttons = [
            "Home",
            "Import Parts",
            "Manage Stock",
            "Manage Routers"
        ]

        views = [
            HomeView(),
            PartView(self.session, PART_PREVIEW_PATH),
            PlateView(self.session, PLATE_PREVIEW_PATH),
            RouterView(self.session, ROUTER_PREVIEW_PATH)
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
        except Exception as e:
            logger.error(f"Error closing database: {e}")
        event.accept()
