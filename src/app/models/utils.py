"""
Author: nagan319
Date: 2024/05/31
"""

import numpy as np
import base64
import uuid
import io

from ..logging import logger

from typing import Union, Type, Any
from sqlalchemy import Integer, Float, String, Text, Boolean

"""
Util functions for dealing with models.
"""

ORM_TYPE_MAP = {
    Integer: int,
    Float: float,
    String: str,
    Text: str,
    Boolean: bool
}

def get_python_type(sqlalchemy_type) -> Union[Type, tuple]:
    """ 
    Get the corresponding Python type(s) for a given SQLAlchemy type. 
    """
    for sqlalchemy_base_type, python_type in ORM_TYPE_MAP.items():
        if isinstance(sqlalchemy_type, sqlalchemy_base_type):
            return python_type
    return None

def is_value_of_type(value: Any, sqlalchemy_type) -> bool:
    """ 
    Check if a value matches the expected SQLAlchemy type. 
    """
    python_type = get_python_type(sqlalchemy_type)
    if python_type is None:
        return False
    if isinstance(python_type, tuple):
        return isinstance(value, python_type)
    return isinstance(value, python_type)

def get_uuid() -> str:
    """ Generate new UUID."""
    return (str(uuid.uuid4()))

def serialize_array(arr: np.array) -> str:
    """
    Serialize np array as a base 64 string for storage in SQL.
    """
    if arr is None:
        return None
    try:
        with io.BytesIO() as buffer:
            np.save(buffer, arr)
            binary_data = buffer.getvalue()
            base64_str = base64.b64encode(binary_data).decode('utf-8')
        return base64_str
    except (IOError, OSError) as e:
        logger.error(f"Error serializing array: {e}")
        return None

def deserialize_array(base64_str: str) -> np.array:
    """
    Deserialize base 64 SQL string back into np array.
    """
    if base64_str is None:
        return None
    try: 
        binary_data = base64.b64decode(base64_str)
        with io.BytesIO(binary_data) as buffer:
            arr = np.load(buffer)
        return arr
    except (IOError, OSError) as e:
        logger.error(f"Error deserializing array: {e}")
        return None
