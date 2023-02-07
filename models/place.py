#!/usr/bin/python3
"""This module contains the difinition of the Place class"""
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
# from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import relationship

from .base_model import BaseModel, Base
# from .amenity import Amenity
# from .review import Review
from . import storage_type

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False),
                      mysql_charset='latin1')


class Place(BaseModel, Base):
    """Class represensts a place"""

    __tablename__ = 'places'
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    if storage_type == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True, default=None)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        user = relationship('User', back_populates='places')
        cities = relationship('City', back_populates='places')
        reviews = relationship('Review', back_populates='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity', secondary='place_amenity',
                                 viewonly=False,
                                 back_populates='place_amenities')
    else:
        @property
        def reviews(self):
            """Returns a list of the reviews related to the current place"""
            from . import storage, Review
            related = []
            for review in storage.all(Review):
                if review.place_id == self.id:
                    related.append(review)
            return related

        @property
        def amenities(self):
            """Returns the list of Amenity instances linked to the Place"""
            from . import storage, Amenity
            related = []
            aminities_d = storage.all(Amenity)
            for id in self.amenity_ids:
                index = '.'.join(('Amenity', id))
                related.append(amenities_d[index])
            return related

        @amenities.setter
        def amenities(self, amenity):
            """Adds the 'id' of a linked Aminity instance to 'self.amenity_ids'
            """
            from . import Amenity
            if not isinstance(amenity, Amenity):
                return None
            if amenity.id not in self.amenity_ids:
                self.amenity_ids.append(amenity.id)
