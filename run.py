import sys

from PyQt6.QtWidgets import QApplication

from src.app.load_settings import load_user_settings
from src.app.mainwindow import MainWindow
from src.app.styling import apply_styling

from src.paths import USER_SETTINGS_PATH

if __name__ == "__main__":
    app = QApplication([])
    user_settings = load_user_settings(USER_SETTINGS_PATH)
    apply_styling(app, user_settings['language'])
    main_window = MainWindow(user_settings)
    main_window.show()
    sys.exit(app.exec())
