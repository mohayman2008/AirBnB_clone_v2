#!/usr/bin/python3
"""This module contains the difinition of the Review class"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .base_model import BaseModel, Base
from . import storage_type


class Review(BaseModel, Base):
    """Class represensts a review for a place"""

    __tablename__ = 'reviews'
    place_id = ""
    user_id = ""
    text = ""

    if storage_type == 'db':
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
        user = relationship('User', back_populates='reviews')
        place = relationship('Place', back_populates='reviews')
    pass
