#!/usr/bin/python3
"""This module contains the difinition of the State class"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import base_model, City, storage_type
Base = base_model.Base


class State(base_model.BaseModel, Base):
    """Class represensts a State"""

    __tablename__ = "states"

    if storage_type == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", back_populates="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ''

        @property
        def cities(self):
            all_cities = self.storage.all(City)
            cities = []
            for city in all_cities:
                if city.state_id == self.id:
                    cities.append(city)
            return cities
    pass
