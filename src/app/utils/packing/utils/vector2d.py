"""
Author: nagan319
Date: 2024/09/05
"""

import math

class Vector2D:
    """ Simple vector class. """ 
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def inverse(self) -> 'Vector2D':
        """ Get inverse of vector """
        return Vector2D(-self.x, -self.y)
    
    def magnitude(self) -> float:
        """ Get magnitude of vector """
        return math.hypot(self.x, self.y)
    