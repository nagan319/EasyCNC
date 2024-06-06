"""
Author: nagan319
Date: 2024/06/05
"""

import json
import os
from ..utils.settings_enum import LanguageEnum, UnitsEnum
from ..logging import logger

class UserSettingsController:
    """
    Controller for handling user settings.
    - user_settings_path: path to user json folder.
    """
    def __init__(self, user_settings_path: str):
        if not os.path.exists(user_settings_path):
            logger.error(f"Attempted to initialize UserSettingsController with invalid filepath {user_settings_path}")
            raise FileNotFoundError(f"File not found: {user_settings_path}")
        self.user_settings_path = user_settings_path
        self._load_settings()
    
    def _load_settings(self):
        """ Load user settings path."""
        with open(self.user_settings_path, 'r') as file:
            try:
                self.user_settings = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError, KeyError, ValueError) as e:
                logger.error(f"Error loading settings from {self.user_settings_path}: {e}")
                self.user_settings = {
                    'language': LanguageEnum.ENG_US.value,
                    'units': UnitsEnum.MM.value
                }

    def get_user_language(self) -> LanguageEnum:
        """ Get user language. Defaults to ENG_US. """
        try:
            return LanguageEnum.__members__.get(self.user_settings['language'])
        except KeyError:
            logger.warning(f"Invalid language value in settings: {self.user_settings['language']}. Defaulting to {LanguageEnum.ENG_US.name}.")
            return LanguageEnum.ENG_US
    
    def get_user_units(self) -> UnitsEnum:
        """ Get user units. Defaults to MM. """
        try:
            return UnitsEnum.__members__.get(self.user_settings['units'])
        except KeyError:
            logger.warning(f"Invalid units value in settings: {self.user_settings['units']}. Defaulting to {UnitsEnum.MM.name}.")
            return UnitsEnum.MM
    
    def set_user_language(self, language: LanguageEnum):
        """ Set user language."""
        self.user_settings['language'] = language.value
        self._save_settings()
    
    def set_user_units(self, units: UnitsEnum):
        """ Set user units. """
        self.user_settings['units'] = units.value
        self._save_settings()
    
    def _save_settings(self):
        """ Save settings to json. """
        with open(self.user_settings_path, 'w') as file:
            json.dump(self.user_settings, file)
