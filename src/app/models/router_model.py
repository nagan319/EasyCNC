import sys
from typing import NamedTuple
from sqlalchemy import Column, String, Float
from ..database import Base
from .utils import get_uuid

class RouterConstants(NamedTuple):
    MAX_ROUTER_DIMENSION = 5000 
    MAX_PLATE_DIMENSION = 5000
    MAX_DRILL_BIT_DIAMETER = 100
    MAX_MILL_BIT_DIAMETER = 100

    ROUTER_DEFAULT_NAME = "New CNC Router"

    DEFAULT_X = 750
    DEFAULT_Y = 1500
    DEFAULT_Z = 500

    DEFAULT_PLATE_X = 1000
    DEFAULT_PLATE_Y = 2000
    DEFAULT_PLATE_Z = 500

    DEFAULT_SAFE_DISTANCE = 50
    DEFAULT_DRILL_BIT_DIAMETER = 5
    DEFAULT_MILL_BIT_DIAMETER = 10

class Router(Base):
    """
    ORM router model.
    """
    __tablename__ = 'routers'
    id = Column(String, primary_key=True, default=get_uuid)
    name = Column(String, nullable=False, default=RouterConstants.ROUTER_DEFAULT_NAME)
    x = Column(Float, nullable=False, default=RouterConstants.DEFAULT_X)
    y = Column(Float, nullable=False, default=RouterConstants.DEFAULT_Y)
    z = Column(Float, nullable=False, default=RouterConstants.DEFAULT_Z)
    plate_x = Column(Float, nullable=False, default=RouterConstants.DEFAULT_PLATE_X)
    plate_y = Column(Float, nullable=False, default=RouterConstants.DEFAULT_PLATE_Y)
    plate_z = Column(Float, nullable=False, default=RouterConstants.DEFAULT_PLATE_Z)
    min_safe_dist_from_edge = Column(Float, nullable=False, default=RouterConstants.DEFAULT_SAFE_DISTANCE)
    drill_bit_diameter = Column(Float, nullable=False, default=RouterConstants.DEFAULT_DRILL_BIT_DIAMETER)
    mill_bit_diameter = Column(Float, nullable=False, default=RouterConstants.DEFAULT_MILL_BIT_DIAMETER)
