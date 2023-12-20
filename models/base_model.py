#!/usr/bin/python3
"""This module contains the difinition of the BaseModel class"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, String, DateTime
from sqlalchemy import Column, String, DateTime  # , DATETIME

from . import storage_type
import models
# storage = ''

Base = declarative_base()
Base.__table_args__ = {
        "mysql_default_charset": "latin1"
    }


class BaseModel:
    """The base model for all the objects of the app"""

    # id = Column(String(60), primary_key=True, default=str(uuid4()),
    #             nullable=False, unique=True)
    id = Column(String(60), primary_key=True, default=str(uuid4()),
                nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    # id = Column(String(60), primary_key=True, nullable=False, unique=True)
    # created_at = Column(DATETIME, default=datetime.utcnow(), nullable=False)
    # updated_at = Column(DATETIME, default=datetime.utcnow(), nullable=False)
    # from . import storage

    def __init__(self, *args, **kwargs):
        """Creates an object of the class"""
        from . import storage
        self.__class__.storage = storage

        if not len(kwargs):
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            return

        for key, val in kwargs.items():
            if key == "__class__":
                continue
            elif key == "created_at":
                self.created_at = datetime.fromisoformat(val)
            elif key == "updated_at":
                self.updated_at = datetime.fromisoformat(val)
            else:
                setattr(self, key, val)

        if getattr(self, 'id', None) is None:
            self.id = str(uuid4())
        if getattr(self, 'created_at', None) is None:
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """Returns the string representation of the object"""
        new_dict = dict(self.__dict__)
        if '_sa_instance_state' in new_dict.keys():
            del (new_dict['_sa_instance_state'])
        # return f"[{self.__class__.__name__}] ({self.id}) {new_dict}"
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, new_dict)

    def save(self):
        """Updates self.updated_at with the current datetime"""
        self.updated_at = datetime.now()
        self.storage.new(self)
        self.storage.save()
        pass

    def to_dict(self):
        """Returns a dictionary representation of the object"""
        dictionary = dict(self.__dict__)
        dictionary["__class__"] = self.__class__.__name__
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del (dictionary['_sa_instance_state'])
        return dictionary

    def delete(self):
        """Deletes the object from storage"""
        self.storage.delete(self)
        pass
    pass
