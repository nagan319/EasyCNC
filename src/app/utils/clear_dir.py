"""
Author: nagan319
Date: 2024/06/13
"""

import os
from ..logging import logger

def clear_dir(dir_path: str):
    """ Clear all files in folder. """
    if not os.path.exists(dir_path):
        logger.error(f"Attempted to clear nonexistend directory {dir_path}")
        raise FileNotFoundError()
    try:
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.debug(f"Removed file {file_path}")
    except Exception as e:
        logger.error(f"Encountered exception while attempting to clear directory {e}")
