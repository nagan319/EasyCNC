import json
from typing import Dict

from .utils.settings_enum import DEFAULT_LANGUAGE, DEFAULT_UNITS

from .logging import logger

def load_user_settings(filepath: str) -> Dict[str, int]:
    """ Retrieve user language and units settings. """
    try:
        with open(filepath, 'r') as file:
            logger.debug(f"Successfully loaded user settings. ") 
            return json.load(file)
    except Exception as e:
        logger.error(f"Encountered exception while attempting to configure user settings: {e}")
        return {
            'user_language': DEFAULT_LANGUAGE,
            'user_units': DEFAULT_UNITS
        }       