import numpy as np
import base64
import uuid
import io

from ..logging import logger

"""
Util functions for dealing with models.
"""

def get_uuid() -> str:
    """
    Generate new UUID.
    """
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
    