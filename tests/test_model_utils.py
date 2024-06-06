import pytest
import numpy as np
from src.app.models.utils import get_uuid, serialize_array, deserialize_array

"""
Tests for ORM model utility functions.

Test coverage:
- retrieval of uuid
- np array serialization and deserialization
"""

@pytest.fixture
def sample_array():
    return np.array([[1, 2, 3], [4, 5, 6]])

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
    