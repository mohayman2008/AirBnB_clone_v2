#!/usr/bin/python3
"""This module contains the difinition of the City class"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import storage_type
from .base_model import BaseModel, Base
from .place import Place

from . import base_model, storage_type


class City(BaseModel, Base):
    """Class represensts a City"""

    __tablename__ = 'cities'
    if storage_type == 'db':
        name = Column(String(128), nullable=False, default='')
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='cities',
                              cascade='all, delete, delete-orphan')
    else:
        name = ''
        state_id = ''

    # __tablename__ = 'cities'
    # if storage_type == "db":
    #     name = Column(String(128), nullable=False)
    #     state_id = Column(String(60), ForeignKey("states.id"),
    #                       nullable=False)
    # else:
    #     name = ''
    #     state_id = ''
    pass
