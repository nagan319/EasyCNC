from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtGui import QIcon

from ...paths import IMAGE_PREVIEW_PATH, ICON_PATH

from src.app.models.plate_model import Plate
from src.app.controllers.plate_controller import PlateController

class ImageEditorWindow(QMainWindow):
    """
    Separate window initialized when image editing mode is activated. Singleton class.
    """
    MIN_HEIGHT = 800
    MIN_WIDTH = 800
    WINDOW_TITLE = 'Attach Image File'

    imageEditorClosed = pyqtSignal()

    def __init__(self, plate: Plate, controller: PlateController):
        super().__init__()
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setCentralWidget(QWidget())
        self._initialized = True
        self.show()

    def closeEvent(self, event):
        self.imageEditorClosed.emit()
        super().closeEvent(event)
    