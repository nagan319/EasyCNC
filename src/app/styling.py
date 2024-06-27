import os
from PyQt6.QtGui import QFont, QFontDatabase
from .utils.settings_enum import LanguageEnum
from ..paths import STYLESHEET_PATH, FONT_DIR

fonts = {
    LanguageEnum.ENG_UK.value: 'NotoSans-Light.ttf', 
    LanguageEnum.ENG_US.value: 'NotoSans-Light.ttf', 
    LanguageEnum.JP.value: 'NotoSansCJKjp-Light.otf',
    LanguageEnum.CN_TRAD.value: 'NotoSansCJKtc-Light.otf',
    LanguageEnum.CN_SIMP.value: 'NotoSansCJKsc-Light.otf',
    LanguageEnum.RUS.value: 'NotoSans-Light.ttf'
}

def apply_styling(app, language: int):
    """ Set app stylesheet and font. """
    app_font_family = set_font(app, language)
    if app_font_family:
        set_stylesheet(app, app_font_family)

def set_font(app, language: int) -> str:
    """ Set application font to font specified in path. Returns the font family name. """
    font_id = QFontDatabase.addApplicationFont(os.path.join(FONT_DIR, fonts[language]))
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app_font = QFont(font_family)
        app.setFont(app_font)
        return font_family
    else:
        print("Failed to load font.")
        return ""

def set_stylesheet(app, font_family: str):
    """Set the application stylesheet from the given file."""
    try:
        with open(STYLESHEET_PATH, "r", encoding="utf-8") as file:
            stylesheet = file.read()
            stylesheet = stylesheet.replace('DynamicFont', font_family)
            app.setStyleSheet(stylesheet)
    except IOError as e:
        print(f"Error opening or reading file: {e}")
