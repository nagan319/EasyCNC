"""
Author: nagan319
Date: 2024/05/31
"""

import os

"""
Path configuration for app
"""

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATABASE_URI = f'sqlite:///{os.path.join(DATA_DIR, "app_data.db")}'

LOGS_DIR = os.path.join(ROOT_DIR, 'logs')

"""
Temporary directory paths
"""

CACHE_DIR = os.path.join(DATA_DIR, 'cache')
IMAGE_PREVIEW_PATH = os.path.join(CACHE_DIR, 'image preview')
PART_PREVIEW_PATH = os.path.join(CACHE_DIR, 'part preview')
PLATE_PREVIEW_PATH = os.path.join(CACHE_DIR, 'plate preview')
ROUTER_PREVIEW_PATH = os.path.join(CACHE_DIR, 'router preview')

"""
Resource paths
"""

LOGO_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'images', 'app logo.PNG')
ICON_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'images', 'app icon.PNG')
FONT_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'metropolis_light.otf')
HELP_TEXT_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'help_text.txt')
STYLESHEET_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'stylesheet.qss')
