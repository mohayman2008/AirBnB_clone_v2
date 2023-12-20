#!/usr/bin/python3
"""This module manages storing and retrieving objects from
a Data Base storage"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from . import Amenity, City, Place, Review, State, User
from models.base_model import Base, BaseModel
from . import classes

# if getenv('HBNB_TYPE_STORAGE') == 'db':
#     from models.place import place_amenity

# classes = {"State": State, "City": City}
classes = classes.copy()
del classes["BaseModel"]


class DBStorage:
    """Class for managing DB storage"""
    __engine = None
    __session = None

    def __init__(self):
        '''Initialize the DB engine'''
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        CHARSET = 'latin1'
        url = 'mysql+mysqldb://{}:{}@{}/{}?charset={}'.format(user, pwd, host,
                                                              db, CHARSET)
        # url = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}?charset={CHARSET}'
        self.__engine = create_engine(url, pool_pre_ping=True,
                                      encoding=CHARSET)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the DB and returns a dictionary of all objects.
        It can also be filtered by cls"""
        objects_d = {}
        if cls is None:
            cls_list = classes.values()
        elif cls not in classes.values():
            return {}
        else:
            cls_list = [cls]

        for cls in cls_list:
            objects = self.__session.query(cls).all()
            for obj in objects:
                index = '.'.join((cls.__name__, obj.id))
                objects_d[index] = obj
        return objects_d

    def new(self, obj):
        """Adds a new object to the current DB session"""
        self.__session.add(obj)
        pass

    def save(self):
        """Commits all the changes of the current DB session"""
        self.__session.commit()
        pass

    def reload(self):
        """Creates all tables in the DB and creates the current DB session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)()

    def delete(self, obj=None):
        """Deletes an object from the current DB session"""
        if obj is not None:
            self.__session.delete(obj)
        pass

    def remove(self, index):
        """Removes object corresponding to an <index> from the
        current DB session"""
        cls_name, id = index.split('.')
        cls = classes[cls_name]
        obj = self.__session.query(cls).filter(cls.id == id)
        self.__session.delete(obj)

    def close(self, *args, **kwargs):
        '''Reload the objects from the database'''
        self.__session.close()
    pass
