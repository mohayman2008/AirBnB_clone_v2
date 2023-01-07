#!/usr/bin/python3
"""This module contains the difinition of the State class"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from . import storage_type
from .base_model import BaseModel, Base
from .city import City


class State(BaseModel, Base):
    """Class represensts a State"""

    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(128), nullable=False, default='')
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            '''returns the list of City instances with state_id
                equals the current State.id
                FileStorage relationship between State and City
            '''
            from models import storage
            related_cities = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)
            return related_cities

    # def __init__(self):
    #     '''Constructor'''
    #     if storage_type == 'db':
    #         name = getattr(self, "name", None)
    #         if name is None:
    #             name = 'DEFAULT'

    # __tablename__ = 'states'
    # if storage_type == "db":
    #     name = Column(String(128), nullable=False)
    # else:
    #     name = ''

    # def __init__(self, *args, **kwargs):
    #     """Creates an object of the class"""
    #     self.name = ''
    #     base_model.BaseModel.__init__(self, *args, **kwargs)

    #     print(f"A state {self.id:} {self.name:}")
    pass
