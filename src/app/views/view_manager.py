"""
Author: nagan319
Date: 2024/06/10
"""

from PyQt6.QtWidgets import QWidget, QStackedWidget
from typing import List

from ..logging import logger

class ViewManager(QStackedWidget):
    """
    Viewer widget for switching between app views.
    """
    def __init__(self, widgets: List[QWidget]):
        super().__init__()

        self.amt_widgets = len(widgets)

        for widget in widgets:
            self.addWidget(widget)

        self.set_view(0)

    def set_view(self, i: int) -> bool:
        """ Set view to given index. Returns false if index is invalid. """
        if i < 0 or i >= self.amt_widgets:
            logger.error(f"Attempted to set app view to invalid index: {i}")
            return False
        
        self.setCurrentIndex(i)
        logger.debug(f"Set app view to index {i}")
        return True
        