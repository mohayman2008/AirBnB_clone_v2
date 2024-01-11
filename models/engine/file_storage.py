#!/usr/bin/python3
"""This module manages storing and retrieving objects from
a file system storage"""

import json

from . import classes


class FileStorage:
    """Class for managing file system storage"""
    # __file_path = "data.json"
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects, and can be filtered by cls"""
        if cls is None:
            return self.__objects
        if cls not in classes.values():
            return {}
        return {key: val for key, val in self.__objects.items()
                if isinstance(val, cls)}

    def new(self, obj):
        """Adds a new object to the dictionary of objects
        with key <obj class name>.id"""
        key = obj.__class__.__name__ + '.' + str(obj.id)
        self.__objects[key] = obj
        pass

    def save(self):
        """Serializes and saves objects to disk in JSON format"""
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            objects_d = {}
            for key, obj in self.__objects.items():
                objects_d[key] = obj.to_dict()
            json.dump(objects_d, f)
        pass

    def reload(self):
        """Loads the saved JSON file and deserializes the objects
        to the objects dictionary"""
        self.__class__.__objects = {}
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                objects_d = json.load(f)

            for key, attributes in objects_d.items():
                obj = classes[attributes["__class__"]](**attributes)
                self.__objects[key] = obj
        except (FileNotFoundError, Exception):
            return

    def delete(self, obj=None):
        """Deletes an object from the dictionaries of the objects"""
        if obj is not None:
            cls_name = obj.__class__.__name__
            id = obj.id
            index = '.'.join((cls_name, id))
            if index in self.__objects.keys():
                del self.__objects[index]
                self.save()
        pass

    def remove(self, index):
        """Removes object corresponding <index> from the dictionaries of the
        objects"""
        del self.__objects[index]
        self.save()

    def close(self, *args, **kwargs):
        '''Reload the objects from the JSON file'''
        self.reload()
        pass
    pass
