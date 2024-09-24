"""
Author: nagan319
Date: 2024/09/09
"""

import pytest
from src.app.utils.packing.utils.rectangle2d import Rectangle2D

def test_contains():
    r1 = Rectangle2D(0, 0, 10, 10)
    r2 = Rectangle2D(1, 1, 5, 5)
    r3 = Rectangle2D(11, 11, 1, 1)
    r4 = Rectangle2D(0, 0, 15, 15)
    
    assert r1.contains(r2) == True
    assert r1.contains(r3) == False
    assert r1.contains(r4) == False

def test_fits_inside():
    r1 = Rectangle2D(0, 0, 5, 5)
    r2 = Rectangle2D(0, 0, 10, 10)
    r3 = Rectangle2D(0, 0, 5, 5)
    
    assert r1.fits_inside(r2) == True
    assert r2.fits_inside(r1) == False
    assert r1.fits_inside(r3) == True

def test_intersects():
    r1 = Rectangle2D(0, 0, 10, 10)
    r2 = Rectangle2D(5, 5, 10, 10)
    r3 = Rectangle2D(15, 15, 5, 5)
    r4 = Rectangle2D(10, 0, 5, 5)
    
    assert r1.intersects(r2) == True
    assert r1.intersects(r3) == False
    assert r1.intersects(r4) == False

def test_create_intersection():
    r1 = Rectangle2D(0, 0, 10, 10)
    r2 = Rectangle2D(5, 5, 10, 10)
    r3 = Rectangle2D(15, 15, 5, 5)
    r4 = Rectangle2D(8, 8, 5, 5)
    
    intersection1 = r1.create_intersection(r2)
    intersection2 = r1.create_intersection(r3)
    intersection3 = r1.create_intersection(r4)
    
    assert intersection1 is not None
    assert intersection1.min_x == 5
    assert intersection1.min_y == 5
    assert intersection1.width == 5
    assert intersection1.height == 5
    
    assert intersection2 is None
    
    assert intersection3 is not None
    assert intersection3.min_x == 8
    assert intersection3.min_y == 8
    assert intersection3.width == 2
    assert intersection3.height == 2

def test_edge_cases():
    r1 = Rectangle2D(0, 0, 0, 0)  
    r2 = Rectangle2D(0, 0, 10, 10)
    
    assert r1.contains(r2) == False
    assert r1.fits_inside(r2) == True
    assert r1.intersects(r2) == False
    assert r1.create_intersection(r2) == None
    
    r3 = Rectangle2D(5, 5, 0, 0)  
    assert r3.create_intersection(r2) is None
