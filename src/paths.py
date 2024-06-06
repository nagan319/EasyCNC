"""
Author: nagan319
Date: 2024/05/31
"""

import os

"""
Path configuration for app.
"""

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATABASE_URI = f'sqlite:///{os.path.join(DATA_DIR, "app_data.db")}'

LOGS_DIR = os.path.join(ROOT_DIR, 'logs')
