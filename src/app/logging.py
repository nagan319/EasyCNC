import os
import logging

from ..paths import LOGS_DIR

"""
Sets up logging configuration and initializes logger when imported.
"""

os.chmod(LOGS_DIR, 0o777)
APP_LOG_FILENAME = 'app.log'
ERROR_LOG_FILENAME = 'error.log'

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
'''
Configure app logger.
'''
app_log_filepath = os.path.join(LOGS_DIR, APP_LOG_FILENAME)
file_handler_app = logging.FileHandler(app_log_filepath)
file_handler_app.setLevel(logging.DEBUG)
formatter_app = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler_app.setFormatter(formatter_app)
logger.addHandler(file_handler_app)

'''
Configure error logger.
'''
error_log_filepath = os.path.join(LOGS_DIR, ERROR_LOG_FILENAME)
file_handler_error = logging.FileHandler(error_log_filepath)
file_handler_error.setLevel(logging.ERROR)
formatter_error = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler_error.setFormatter(formatter_error)
logger.addHandler(file_handler_error)
