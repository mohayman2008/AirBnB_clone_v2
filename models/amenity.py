#!/usr/bin/python3
"""This module contains the difinition of the Amenity class"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from . import storage_type
from .base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Class represensts an amenity"""

    __tablename__ = 'amenities'
    name = ""
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place', secondary='place_amenity')
    pass
