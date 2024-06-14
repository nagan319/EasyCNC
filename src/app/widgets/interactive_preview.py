"""
Author: nagan319
Date: 2024/06/13
"""

from PyQt6.QtCore import QPoint, pyqtSignal
from PyQt6.QtWidgets import QLabel

class InteractivePreview(QLabel):
    """
    Clickable preview
    """
    inputDetected = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        """ Emits relative position of user mouse click. """
        label_size = self.size()
        pixmap_size = self.pixmap().size()

        if pixmap_size.height() == 0:
            return
        
        image_pos = QPoint(
            (label_size.width() - pixmap_size.width()) // 2,
            (label_size.height() - pixmap_size.height()) // 2
        )
        mouse_pos = event.pos()
        relative_pos: QPoint = mouse_pos - image_pos
        self.inputDetected.emit((relative_pos.x(), relative_pos.y()))
