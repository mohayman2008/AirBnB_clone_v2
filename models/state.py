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
    name = ''
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', back_populates='state',
                              cascade='all, delete, delete-orphan')
    else:
        @property
        def cities(self):
            """Returns a list of the cities that belongs to the current state
            """
            from . import storage
            the_list = []
            for city in storage.all(City).values():
                state_id = getattr(city, "state_id", None)
                if state_id is not None and state_id == self.id:
                    the_list.append(city)
            return the_list
    pass
