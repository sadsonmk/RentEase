#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.booking import Booking
from models.property import Property
from models.review import Review
from models.user import User
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Bookings": Booking, "Property": Property, 
           "Review": Review, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        # RNT_MYSQL_USER = getenv('RNT_MYSQL_USER')
        # RNT_MYSQL_PWD = getenv('RNT_MYSQL_PWD')
        # RNT_MYSQL_HOST = getenv('RNT_MYSQL_HOST')
        # RNT_MYSQL_DB = getenv('RNT_MYSQL_DB')
        # RNT_ENV = getenv('RNT_ENV')

        RNT_MYSQL_USER = 'dev'
        RNT_MYSQL_PWD = 'dev_pwd'
        RNT_MYSQL_HOST = '127.0.0.1'
        RNT_MYSQL_DB = 'rent_ease_db'
        RNT_ENV = getenv('RNT_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(RNT_MYSQL_USER,
                                             RNT_MYSQL_PWD,
                                             RNT_MYSQL_HOST,
                                             RNT_MYSQL_DB))
        if RNT_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def get(self, cls, id):
        """a method to retrieve one object"""
        for value in classes.values():
            if value == cls:
                return self.__session.query(cls).get(id)

    def count(self, cls=None):
        """method to count the number of objects in storage"""
        if cls is not None:
            return self.__session.query(cls).count()
        else:
            total = 0
            for value in classes.values():
                total += self.__session.query(value).count()
            return total

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()