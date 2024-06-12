import sys

from PyQt6.QtWidgets import QApplication

from src.app.mainwindow import MainWindow
from src.app.styling import apply_styling

if __name__ == "__main__":
    app = QApplication([])
    apply_styling(app)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

