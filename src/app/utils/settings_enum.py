"""
Author: nagan319
Date: 2024/06/05
"""

import enum

"""
Enums for storing user settings.
"""

class LanguageEnum(enum.Enum):
    ENG_US = 0
    ENG_UK = 1
    CN_SIMP = 2
    CN_TRAD = 3
    RUS = 4
    JP = 5

class UnitsEnum(enum.Enum):
    MM = 0
    IN = 1

DEFAULT_LANGUAGE = LanguageEnum.ENG_US.value
DEFAULT_UNITS = UnitsEnum.MM.value
