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
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

"""
Temporary directory paths
"""

''' these must be created when downloading from github '''
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

IMAGE_PREVIEW_PATH = os.path.join(CACHE_DIR, 'image preview')
if not os.path.exists(IMAGE_PREVIEW_PATH):
    os.makedirs(IMAGE_PREVIEW_PATH)

PART_PREVIEW_PATH = os.path.join(CACHE_DIR, 'part preview')
if not os.path.exists(PART_PREVIEW_PATH):
    os.makedirs(PART_PREVIEW_PATH)

PLATE_PREVIEW_PATH = os.path.join(CACHE_DIR, 'plate preview')
if not os.path.exists(PLATE_PREVIEW_PATH):
    os.makedirs(PLATE_PREVIEW_PATH)

ROUTER_PREVIEW_PATH = os.path.join(CACHE_DIR, 'router preview')
if not os.path.exists(ROUTER_PREVIEW_PATH):
    os.makedirs(ROUTER_PREVIEW_PATH)

LAYOUT_PREVIEW_PATH = os.path.join(CACHE_DIR, 'layouts')
if not os.path.exists(LAYOUT_PREVIEW_PATH):
    os.makedirs(LAYOUT_PREVIEW_PATH)

LAYOUT_FILENAME = 'layout.png'

USER_SETTINGS_PATH = os.path.join(DATA_DIR, 'user_settings.json')

"""
Resource paths
"""

LOGO_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'images', 'app logo.PNG')
ICON_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'images', 'app icon.PNG')
FONT_DIR = os.path.join(ROOT_DIR, 'app', 'resources', 'fonts')
HELP_TEXT_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'help_text.txt')
STYLESHEET_PATH = os.path.join(ROOT_DIR, 'app', 'resources', 'stylesheet.qss')
