#!/usr/bin/python3
"""This module contains the difinition of the City class"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import base_model, storage_type
Base = base_model.Base


class City(base_model.BaseModel, Base):
    """Class represensts a City"""

    __tablename__ = "cities"

    if storage_type == "db":
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        name = Column(String(128), nullable=False)
        state = relationship("State", back_populates="cities")
    else:
        state_id = ''
        name = ''
    pass
