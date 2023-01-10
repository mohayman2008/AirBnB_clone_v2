#!/usr/bin/python3
"""Package models"""

from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

BaseModel = __import__('base_model', globals(), level=1).BaseModel
Base = base_model.Base
Amenity = __import__('amenity', globals(), level=1).Amenity
City = __import__('city', globals(), level=1).City
Place = __import__('place', globals(), level=1).Place
Review = __import__('review', globals(), level=1).Review
State = __import__('state', globals(), level=1).State
User = __import__('user', globals(), level=1).User


if storage_type == 'db':
    from .engine.db_storage import DBStorage
    storage = DBStorage()

else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()

__all__ = ["base_model", "BaseModel", "Base", "amenity", "Amenity",
           "city", "City", "place", "Place", "review", "Review",
           "state", "State", "user", "User", "engine", "storage"]
