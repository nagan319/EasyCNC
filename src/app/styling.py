from PyQt6.QtGui import QFont, QFontDatabase
from ..paths import STYLESHEET_PATH, FONT_PATH

def apply_styling(app):
    """ Set app stylesheet and font. """
    set_stylesheet(app)
    set_font(app)

def set_stylesheet(app):
    """Set the application stylesheet from the given file."""
    try:
        with open(STYLESHEET_PATH, "r", encoding="utf-8") as file:
            stylesheet = file.read()
            app.setStyleSheet(stylesheet)
    except IOError as e:
        print(f"Error opening or reading file: {e}")

def set_font(app):
    """ Set application font to font specified in path. """
    font_id = QFontDatabase.addApplicationFont(FONT_PATH)
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app_font = QFont(font_family)  
        app.setFont(app_font)
    else:
        print("Failed to load font.")