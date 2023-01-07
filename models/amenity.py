#!/usr/bin/python3
"""This module contains the difinition of the Amenity class"""

from sqlalchemy import Column, String

from . import storage_type
from .base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Class represensts an amenity"""

    __tablename__ = 'amenities'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""
    pass
