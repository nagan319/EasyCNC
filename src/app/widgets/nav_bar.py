"""
Author: nagan319
Date: 2024/06/10
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from typing import List

class NavBar(QWidget):
    """
    Nav bar initialized with list of button names (text). Buttons emit index in nav bar when pressed.
    """
    button_clicked = pyqtSignal(int)

    def __init__(self, button_names: List[str]):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for i, button_text in enumerate(button_names):
            button = QPushButton(button_text)
            button.setObjectName("menuButton")
            button.clicked.connect(lambda _, index=i: self.button_clicked.emit(index))
            layout.addWidget(button, 1)

        footer = QWidget() 
        footer.setObjectName("navBar")
        layout.addWidget(footer, 10)
        self.setLayout(layout)
