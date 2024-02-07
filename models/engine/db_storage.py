#!/usr/bin/python3
"""This module manages storing and retrieving objects from
a file system storage"""
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib.parse import quote_plus

from ..base_model import Base
from . import *

classes = {"State": State, "City": City}
# classes = classes.copy()
# if classes.get("BaseModel"):
#     del classes["BaseModel"]


class DBStorage:
    """Class for managing DB storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Inistantiate a new instance of the database storage engine class"""
        user = quote_plus(str(getenv("HBNB_MYSQL_USER")))
        pwd = quote_plus(str(getenv("HBNB_MYSQL_PWD")))
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        # CHARSET = "latin1"
        CHARSET = "utf8mb4"

        url = f"mysql+mysqldb://{user}:{pwd}@{host}/{db}?charset={CHARSET}"
        self.__engine = create_engine(url, pool_pre_ping=True,
                                      encoding="utf8")

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects, and can be filtered by cls"""
        objects = {}

        if cls is None:
            cls_list = classes.values()
        elif cls not in classes.values():
            return {}
        else:
            cls_list = [cls]

        for cls in cls_list:
            obj_list = self.__session.query(cls).all()
            for obj in obj_list:
                index = obj.__class__.__name__ + '.' + str(obj.id)
                objects[index] = obj
        return objects

    def new(self, obj):
        """Adds a new object to the current DB session"""
        self.__session.add(obj)

    def save(self):
        """"Commits all the changes of the current DB session"""
        self.__session.commit()

    def reload(self):
        """Creates all tables in the DB and creates the current DB session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)()

    def delete(self, obj=None):
        """Deletes an object from the current DB session"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def close(self, *args, **kwargs):
        '''Closes the SQLAlechemy session'''
        self.__session.close()

    pass
