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

    DEFAULT_LANGUAGE = LanguageEnum.ENG_US
    DEFAULT_UNITS = UnitsEnum.MM

    def __init__(self, user_settings_path: str):
        if not os.path.exists(user_settings_path):
            logger.error(f"Attempted to initialize UserSettingsController with invalid filepath {user_settings_path}")
            raise FileNotFoundError()
        self.user_settings_path = user_settings_path
        self._load_settings()
    
    def _load_settings(self):
        """ Load user settings path."""
        with open(self.user_settings_path, 'r') as file:
            try:
                settings_values = json.load(file)
                self.user_settings = {
                    'language': LanguageEnum(settings_values['language']),
                    'units': UnitsEnum(settings_values['units'])
                }
            except (json.JSONDecodeError, FileNotFoundError, KeyError, ValueError) as e:
                logger.error(f"Error loading settings from {self.user_settings_path}: {e}")
                self.user_settings = {
                    'language': self.DEFAULT_LANGUAGE,
                    'units': self.DEFAULT_UNITS
                }

    def _save_settings(self):
        """ Save settings to json. """
        with open(self.user_settings_path, 'w') as file:
            settings_values = {
                'language': self.user_settings['language'].value,
                'units': self.user_settings['units'].value
            }
            json.dump(settings_values, file)

    def get_user_language(self) -> LanguageEnum:
        """ Get user language. Defaults to ENG_US. """
        try:
            return self.user_settings['language']
        except KeyError:
            logger.warning(f"Invalid language value in settings: {self.user_settings['language']}. Defaulting to {self.DEFAULT_LANGUAGE}.")
            return self.DEFAULT_LANGUAGE
    
    def get_user_units(self) -> UnitsEnum:
        """ Get user units. Defaults to MM. """
        try:
            return self.user_settings['units']
        except KeyError:
            logger.warning(f"Invalid units value in settings: {self.user_settings['units']}. Defaulting to {self.DEFAULT_UNITS}.")
            return self.DEFAULT_UNITS
    
    def set_user_language(self, language: LanguageEnum):
        """ Set user language."""
        self.user_settings['language'] = language
        self._save_settings()
    
    def set_user_units(self, units: UnitsEnum):
        """ Set user units. """
        self.user_settings['units'] = units
        self._save_settings()
    

