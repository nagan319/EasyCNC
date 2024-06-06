"""
Author: nagan319
Date: 2024/06/05
"""

import os
import json
import pytest
from pytest import raises
import tempfile
from src.app.controllers.user_settings_controller import UserSettingsController
from src.app.utils.settings_enum import LanguageEnum, UnitsEnum

"""
Tests for UserSettingsController class.

Test Coverage:
    - Test retrieving data
        - correct retrieval
        - does not accept invalid filepath
    - Test getting language
        - Test getting valid language
        - Test getting invalid language (should default to ENG_US)
    - Test getting units
        - Test getting valid units
        - Test getting invalid units (should default to MM)
    - Test setting language
        - Test setting valid language
        - Check json file for change
    - Test setting units
        - Test setting valid units
        - Check json file for change
"""

@pytest.fixture
def user_settings_path(tmp_path):
    temp_dir = tmp_path / "user_settings"
    temp_dir.mkdir()

    fake_settings_values = {
        "language": LanguageEnum.JP.value,
        "units": UnitsEnum.IN.value
    }
    fake_settings_path = temp_dir / "user_settings.json"
    with open(fake_settings_path, 'w') as file:
        json.dump(fake_settings_values, file)
    return str(fake_settings_path)

@pytest.fixture
def invalid_user_settings_path(tmp_path):
    temp_dir = tmp_path / "user_settings"
    temp_dir.mkdir()

    invalid_settings_values = {
        "language": -1, 
        "units": -2      
    }
    invalid_settings_path = temp_dir / "invalid_user_settings.json"
    with open(invalid_settings_path, 'w') as file:
        json.dump(invalid_settings_values, file)
    return str(invalid_settings_path)

def test_valid_init(user_settings_path):
    controller = UserSettingsController(user_settings_path)
    assert controller.user_settings['language'] == LanguageEnum.JP
    assert controller.user_settings['units'] == UnitsEnum.IN

def test_invalid_init():
    with raises(FileNotFoundError):
        controller = UserSettingsController("random invalid path")

def test_get_language(user_settings_path):
    controller = UserSettingsController(user_settings_path)
    assert controller.get_user_language() == LanguageEnum.JP

def test_get_language_invalid(invalid_user_settings_path):
    controller = UserSettingsController(invalid_user_settings_path)
    assert controller.get_user_language() == LanguageEnum.ENG_US

def test_get_units(user_settings_path):
    controller = UserSettingsController(user_settings_path)
    assert controller.get_user_units() == UnitsEnum.IN

def test_get_units_invalid(invalid_user_settings_path):
    controller = UserSettingsController(invalid_user_settings_path)
    assert controller.get_user_units() == UnitsEnum.MM

def test_set_language(user_settings_path):
    controller = UserSettingsController(user_settings_path)
    controller.set_user_language(LanguageEnum.CN_TRAD)
    assert controller.get_user_language() == LanguageEnum.CN_TRAD
    with open(user_settings_path, 'r') as file:
        settings = json.load(file)
    assert settings['language'] == LanguageEnum.CN_TRAD.value

def test_set_units(user_settings_path):
    controller = UserSettingsController(user_settings_path)
    controller.set_user_units(UnitsEnum.MM)
    assert controller.get_user_units() == UnitsEnum.MM
    with open(user_settings_path, 'r') as file:
        settings = json.load(file)
    assert settings['units'] == UnitsEnum.MM.value
