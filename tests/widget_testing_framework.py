"""
Author: nagan319
Date: 2024/06/08
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

def display_widget(widget):
    """
    Check a widget's appearance when displaying.
    """
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(widget)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    display_widget()
    