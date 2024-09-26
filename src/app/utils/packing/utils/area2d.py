"""
Author: nagan319
Date: 2024/09/05
"""

import numpy as np

from shapely.geometry import Polygon
from shapely.affinity import rotate, translate

from .rectangle2d import Rectangle2D
from .vector2d import Vector2D

import enum
from typing import Tuple, List

class BoundsEnum(enum.Enum):
    """ 
    Enums for shapely shape.bounds object. 
    """
    MINX = 0
    MINY = 1
    MAXX = 2
    MAXY = 3

class Area2D:
    """ Class to store irregular 2D shape and compute related operations. """
    def __init__(self, id: str=None, shape=None, points=None, shift_to_origin=True):
        """ Initialize Area2D object with optional shape or points parameter. """
        if points is not None:
            if not all(isinstance(point, tuple) and len(point) == 2 for point in points):
                raise ValueError("Points must be a list of tuples with two elements each.")
            
            if shift_to_origin:
                min_x = float('inf')
                min_y = float('inf')

                for point in points:
                    x, y = point[0], point[1]
                    min_x, min_y = min(min_x, x), min(min_y, y)
                
                for i, point in enumerate(points):
                    points[i] = (point[0] - min_x, point[1] - min_y)

            self.shape = Polygon(points)
        elif isinstance(shape, Area2D):
            self.shape = shape.shape
        elif isinstance(shape, Rectangle2D):
            self.shape = Area2D._create_poly_from_rect(shape)
        else:
            self.shape = Polygon()

        self.id = id
        self.area = self.shape.area
        self.rotation = 0.0

    """ Util methods """

    @staticmethod
    def _create_poly_from_rect(rectangle: Rectangle2D) -> Polygon:
        """ Utility method to initialize from Rectangle2D object. """
        vertices = [
            (rectangle.min_x, rectangle.min_y),  
            (rectangle.min_x + rectangle.width, rectangle.min_y),
            (rectangle.min_x + rectangle.width, rectangle.min_y + rectangle.height),
            (rectangle.min_x, rectangle.min_y + rectangle.height),  
            (rectangle.min_x, rectangle.min_y)
        ]
        return Polygon(vertices)
    
    def _update_area(self) -> None:
        """ Update area parameter using area of shapely polygon. """
        self.area = self.shape.area

    def __repr__(self) -> str:
        """ Return a string representation of the Area2D object. """
        id_info = f"ID: {self.id}, " if self.id else ""
        bounding_box = self.get_bb()
        return f"\n{id_info}Bounding Box: (min_x: {bounding_box.min_x}, min_y: {bounding_box.min_y}, width: {bounding_box.width}, height: {bounding_box.height})"

    """ Accessor methods """

    def get_area(self) -> float:
        """ Get area of shape """
        return self.shape.area

    def get_rotation(self) -> float:
        """ Get rotation of shape. """
        return self.rotation

    def get_free_area(self) -> float:
        """ Free area left inside bounding box. """
        return self.shape.envelope.area - self.shape.area

    def get_bb(self) -> Rectangle2D:
        """ Get bounding box of shape. Returns Rectangle2D object. """
        bounds = self.shape.bounds
        min_x = bounds[BoundsEnum.MINX.value]
        min_y = bounds[BoundsEnum.MINY.value]
        max_x = bounds[BoundsEnum.MAXX.value]
        max_y = bounds[BoundsEnum.MAXY.value]
        return Rectangle2D(min_x, min_y, max_x - min_x, max_y - min_y)

    def get_position(self) -> Tuple[float, float]:
        """ Get absolute position of piece in bin. """
        bounds = self.shape.bounds
        min_x = bounds[BoundsEnum.MINX.value]
        min_y = bounds[BoundsEnum.MINY.value]
        return (min_x, min_y)

    """ Modifying shape """

    def add(self, other: 'Area2D') -> None:
        """ Add area of another Area2D object. """
        combined_polygon = self.shape.union(other.shape)
        self.shape = combined_polygon
        self._update_area() 

    def subtract(self, other: 'Area2D') -> None:
        """ Subtract area of another Area2D object. """
        subtracted_polygon = self.shape.difference(other.shape)
        self.shape = subtracted_polygon
        self._update_area()

    """ Movement """

    def move(self, vector: Vector2D) -> None:
        """ Translate shape by given vector. """
        self.shape = translate(self.shape, vector.x, vector.y)

    def place_in_position(self, x: float, y: float) -> None:
        """ Place shape in given position. """
        bb = self.get_bb()
        dx = x - bb.min_x
        dy = y - bb.min_y
        self.move(Vector2D(dx, dy))

    def rotate(self, degrees: float) -> None:
        """ Rotate shape by indicated amount around bounding box center. """
        self.rotation += degrees
        self.rotation %= 360
        self.shape = rotate(self.shape, degrees, origin='center')

    """ Bound checks """

    def is_inside_area(self, container: 'Area2D') -> bool:
        """ Check if shape is inside Area2D. Returns True if corners/edges match. """
        return self.shape.within(container.shape)

    def is_inside_rect(self, container: Rectangle2D) -> bool:
        """ Check if shape is inside rectangle. Returns True if corners/edges match. """
        container_poly = Area2D._create_poly_from_rect(container)
        return self.shape.within(container_poly)

    def intersection(self, other: 'Area2D') -> bool:
        """ Check if intersection exists with other shape. """
        inters = self.shape.intersection(other.shape)
        return not inters.is_empty
