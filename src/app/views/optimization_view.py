"""
Author: nagan319
Date: 2024/06/13
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap

from sqlalchemy.orm import Session

from ..logging import logger

class OptimizationView(QWidget):
    """
    Widget containing layout optimization options.
    """

    def __init__(self, session: Session):
        super().__init__()
        logger.debug(f"Initialized optimization view.")

