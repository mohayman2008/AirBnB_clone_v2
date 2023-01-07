#!/usr/bin/python3
"""This module contains the difinition of the User class"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base_model import BaseModel, Base
from . import storage_type


class User(BaseModel, Base):
    """Class represensts users"""

    __tablename__ = 'users'
    if storage_type == 'db':
        email = Column(String(128), nullable=False, default = '')
        password = Column(String(128), nullable=False, default = '')
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='user',
                              cascade='all, delete, delete-orphan')
        reviews = relationship('Review', backref='user',
                               cascade='all, delete, delete-orphan')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
    pass
