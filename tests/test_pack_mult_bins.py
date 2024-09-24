import os
import random
from typing import List, Tuple
from src.app.utils.packing.packing_algo import execute_packing_algorithm

import pytest

@pytest.fixture
def preview_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'packing algo preview', 'multiple bins.png')

def generate_random_piece(id: str, max_width: float, max_height: float) -> Tuple[str, List[Tuple[float, float]]]:
    """Generate a random rectangular piece."""
    width = random.uniform(1, max_width)
    height = random.uniform(1, max_height)
    return id, [(0, 0), (0, height), (width, height), (width, 0), (0, 0)]

def test_packing_algo(preview_path):
    """ Test packing algorithm with four bins and randomly-sized pieces. Call with -s -k and view saved preview to test. """
    res = execute_packing_algorithm(
        [
            ('1', (100, 100)),
            ('2', (200, 100)),
            ('3', (20, 50)),
            ('4', (60, 40))
        ],
        [
            generate_random_piece(f'piece_{i}', 6, 6) for i in range(700)  
        ],
        preview_path
    )
    print(res)
