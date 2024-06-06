import sys
from typing import NamedTuple
from sqlalchemy import Column, String, Float, Text
from ..database import Base
from .utils import get_uuid

class PlateConstants(NamedTuple):
    MAX_X = 5000
    MAX_Y = 5000
    MAX_Z = 5000
    DEFAULT_X = 1000
    DEFAULT_Y = 1000
    DEFAULT_Z = 1000
    DEFAULT_MATERIAL = "Aluminum"

class Plate(Base):
    """
    ORM plate model.
    """
    __tablename__ = 'plates'
    id = Column(String, primary_key=True, default=get_uuid)
    x = Column(Float, nullable=False, default=PlateConstants.DEFAULT_X)
    y = Column(Float, nullable=False, default=PlateConstants.DEFAULT_Y)
    z = Column(Float, nullable=False, default=PlateConstants.DEFAULT_Z)
    material = Column(String, nullable=False, default=PlateConstants.DEFAULT_MATERIAL)
    contours = Column(Text, nullable=True, default=None)
    