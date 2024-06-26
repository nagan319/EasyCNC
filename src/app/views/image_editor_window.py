"""
Author: nagan319
Date: 2024/06/12
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtGui import QIcon

from sqlalchemy.orm import Session

from ...paths import IMAGE_PREVIEW_PATH, ICON_PATH

from src.app.models.plate_model import Plate
from .image_editor_view import ImageEditorView

from ..translations import image_editor_window
from ..logging import logger

class ImageEditorWindow(QMainWindow):
    """
    Separate window initialized when image editing mode is activated. 
    """
    MIN_HEIGHT = 800
    MIN_WIDTH = 800
    
    imageEditorClosed = pyqtSignal()
    
    def __init__(self, session: Session, plate: Plate, language: int):
        super().__init__()

        self.texts = image_editor_window
        self.language = language

        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setWindowTitle(self.texts['window_title'][self.language])
        self.setWindowIcon(QIcon(ICON_PATH))
        
        self.image_editor_view = ImageEditorView(
            session, 
            plate, 
            self.MIN_WIDTH, 
            self.MIN_HEIGHT,
            self.language
        )
        self.image_editor_view.editingFinished.connect(self.onEditingFinished)
        self.setCentralWidget(self.image_editor_view)
        self.show()
        logger.debug("Initialized image editor window.")

    def onEditingFinished(self):
        """ Received editing finished signal from widget. """
        self.close()

    def closeEvent(self, event):
        """ Activated on self.close called. """
        self.imageEditorClosed.emit()
        logger.debug("Closed image editor window.")
        super().closeEvent(event)
