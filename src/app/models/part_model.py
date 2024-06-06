import sys
from typing import NamedTuple
from sqlalchemy import Column, Integer, String, Float, Text
from ..database import Base
from .utils import get_uuid

class PartConstants(NamedTuple):
    DEFAULT_MATERIAL = "Aluminum"

class Part(Base):
    """
    ORM part model.
    """
    __tablename__ = 'parts'
    id = Column(String, primary_key=True, default=get_uuid)
    filename = Column(String, unique=True)
    thickness = Column(Float, nullable=False)
    material = Column(String, nullable=False, default=PartConstants.DEFAULT_MATERIAL)
    contours = Column(Text, nullable=False)
    amount = Column(Integer, nullable=False, default=1)
