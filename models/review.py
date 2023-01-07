#!/usr/bin/python3
"""This module contains the difinition of the Review class"""

from sqlalchemy import Column, String, ForeignKey

from .base_model import BaseModel, Base
from . import storage_type


class Review(BaseModel, Base):
    """Class represensts a review for a place"""

    __tablename__ = 'reviews'
    if storage_type == 'db':
        text = Column(String(1024), nullable=False, default = '')
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""
    pass
