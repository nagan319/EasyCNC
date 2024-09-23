"""
Author: nagan319
Date: 2024/09/05
"""

from typing import Union

class Rectangle2D: 
    """ 2D rectangle class. """
    def __init__(self, x: float, y: float, width: float, height: float):
        self.width = width
        self.height = height
        self.min_x = x
        self.min_y = y
        self.max_x = self.min_x + self.width
        self.max_y = self.min_y + self.height
        self.area = self.width * self.height

    def contains(self, other: 'Rectangle2D') -> bool:
        """ Check if other rectangle is fully contained inside. Considers rectangle coordinates. """
        return (
            self.width >= other.width and
            self.height >= other.height and
            self.min_x <= other.min_x and
            self.min_y <= other.min_y and
            self.min_x + self.width >= other.min_x + other.width and
            self.min_y + self.height >= other.min_y + other.height
        )
    
    def fits_inside(self, other: 'Rectangle2D') -> bool:
        """
        Check if rectangle can theoretically fit inside other rectangle. Includes rectangles of the same size.
        """
        return self.width <= other.width and self.height <= other.height

    def fits_inside_rotated(self, other: 'Rectangle2D') -> bool:
        """
        Check if rectangle can theoretically fit inside other rectangle when rotated 90 degrees. Includes rectangles of the same size.
        """
        return self.width <= other.height and self.height <= other.width

    def intersects(self, other: 'Rectangle2D') -> bool:
        """
        Check if intersections with other rectangle are present. Returns False for adjacent rectangles.
        """
        if self.max_x <= other.min_x or other.max_x <= self.min_x:
            return False
        if self.max_y <= other.min_y or other.max_y <= self.min_y:
            return False
        return True

    def create_intersection(self, other: 'Rectangle2D') -> Union['Rectangle2D', None]:
        """
        Return rectangle that represents the intersection of two rectangles.
        """
        inter_left = max(self.min_x, other.min_x)
        inter_bottom = max(self.min_y, other.min_y)
        inter_right = min(self.max_x, other.max_x)
        inter_top = min(self.max_y, other.max_y)
        
        if inter_left < inter_right and inter_bottom < inter_top:
            inter_width = inter_right - inter_left
            inter_height = inter_top - inter_bottom
            return Rectangle2D(inter_left, inter_bottom, inter_width, inter_height)
        
        return None
    
    def __eq__(self, other):
        """
        All parameters are equal
        """
        if isinstance(other, Rectangle2D):
            return (self.min_x == other.min_x and
                    self.min_y == other.min_y and
                    self.width == other.width and
                    self.height == other.height)
        return False
    
    def __repr__(self):
        return f"Rectangle2D({self.min_x}, {self.min_y}, {self.width}, {self.height})"
    