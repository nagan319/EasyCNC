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

class ImageEditorWindow(QMainWindow):
    """
    Separate window initialized when image editing mode is activated. 
    """
    MIN_HEIGHT = 800
    MIN_WIDTH = 800
    WINDOW_TITLE = 'Attach Image File'
    
    imageEditorClosed = pyqtSignal()
    
    def __init__(self, session: Session, plate: Plate):
        super().__init__()
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))
        
        self.image_editor_view = ImageEditorView(session, plate, self.MIN_WIDTH, self.MIN_HEIGHT)
        self.image_editor_view.editingFinished.connect(self.onEditingFinished)
        self.setCentralWidget(self.image_editor_view)
        self.show()

    def onEditingFinished(self):
        """ Received editing finished signal from widget. """
        self.close()

    def closeEvent(self, event):
        """ Activated on self.close called. """
        self.imageEditorClosed.emit()
        super().closeEvent(event)
