#!/usr/bin/python3
"""Package models"""

from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


if storage_type == 'db':
    from .engine.db_storage import DBStorage
    storage = DBStorage()

else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()

__all__ = ["base_model", "amenity", "city", "place", "review", "state",
           "user", "engine"]
