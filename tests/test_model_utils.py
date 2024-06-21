"""
Author: nagan319
Date: 2024/06/01
"""

import pytest
import numpy as np
from sqlalchemy import Integer, Float, String, Text, Boolean
from src.app.models.utils import get_uuid, serialize_array, deserialize_array, serialize_array_list, deserialize_array_list, get_python_type, is_value_of_type

"""
Tests for ORM model utility functions.

Test coverage:
- retrieval of uuid
- np array serialization and deserialization
- list of np arrays serialization and deserialization
- converting sql type to python type
- converting python type to sql type
"""

@pytest.fixture
def sample_array():
    return np.array([[1, 2, 3], [4, 5, 6]])

@pytest.fixture
def sample_array_list():
    return [np.array([[1, 2, 3], [4, 5, 6]]), np.array([[7, 8, 9], [10, 11, 12]])]

def test_get_uuid():
    assert isinstance(get_uuid(), str)

def test_serialize_array(sample_array):
    serialized_array = serialize_array(sample_array)
    assert isinstance(serialized_array, str)

def test_deserialize_array(sample_array):
    serialized_array = serialize_array(sample_array)
    deserialized_array = deserialize_array(serialized_array)
    assert isinstance(deserialized_array, np.ndarray)
    assert np.array_equal(deserialized_array, sample_array)

def test_serialize_deserialize_round_trip(sample_array):
    serialized_array = serialize_array(sample_array)
    deserialized_array = deserialize_array(serialized_array)
    assert np.array_equal(deserialized_array, sample_array)
    
def test_serialize_array_list(sample_array_list):
    serialized_list = serialize_array_list(sample_array_list)
    assert isinstance(serialized_list, str)

def test_deserialize_array_list(sample_array_list):
    serialized_list = serialize_array_list(sample_array_list)
    deserialized_list = deserialize_array_list(serialized_list)
    assert isinstance(deserialized_list, list)
    assert all(isinstance(arr, np.ndarray) for arr in deserialized_list)
    for original, deserialized in zip(sample_array_list, deserialized_list):
        assert np.array_equal(original, deserialized)

def test_serialize_deserialize_array_list_round_trip(sample_array_list):
    serialized_list = serialize_array_list(sample_array_list)
    deserialized_list = deserialize_array_list(serialized_list)
    for original, deserialized in zip(sample_array_list, deserialized_list):
        assert np.array_equal(original, deserialized)
        
def test_serialize_empty_array_list():
    empty_list = []
    serialized_list = serialize_array_list(empty_list)
    deserialized_list = deserialize_array_list(serialized_list)
    assert deserialized_list == None

def test_serialize_array_list_with_empty_array():
    array_list_with_empty_array = [np.array([]), np.array([1, 2, 3])]
    serialized_list = serialize_array_list(array_list_with_empty_array)
    deserialized_list = deserialize_array_list(serialized_list)
    assert deserialized_list[0].size == 0
    assert np.array_equal(deserialized_list[1], array_list_with_empty_array[1])

def test_get_python_type():
    assert get_python_type(Integer()) == int
    assert get_python_type(Float()) == float
    assert get_python_type(String()) == str
    assert get_python_type(Text()) == str
    assert get_python_type(Boolean()) == bool
    assert get_python_type(None) == None

def test_is_value_of_type():
    assert is_value_of_type(1, Integer())
    assert not is_value_of_type("1", Integer())
    
    assert is_value_of_type(1.0, Float())
    assert not is_value_of_type("1.0", Float())

    assert is_value_of_type("test", String())
    assert not is_value_of_type(1, String())
    
    assert is_value_of_type("test", Text())
    assert not is_value_of_type(1, Text())

    assert is_value_of_type(True, Boolean())
    assert is_value_of_type(False, Boolean())
    assert not is_value_of_type("True", Boolean())
    
    assert not is_value_of_type(1, None)
