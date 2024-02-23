#!/usr/bin/python

from models.base_model import BaseModel, Base
from flask import Flask
import sqlalchemy
from sqlalchemy import Column, String, Integer, BLOB
from sqlalchemy.orm import relationship
from backend import db


class User(db.Model, BaseModel, Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(200), nullable=False)
    email = Column(String(150), nullable=False)
    phone_number = Column(String(15), nullable=False)
    password = Column(String(500), nullable=False)
    verification_status = Column(Integer, nullable=False)
    profile_picture = Column(BLOB, nullable=False)
    bio = Column(String(1000), nullable=False)
    user_role = Column(Integer, nullable=False)
    bookings = relationship("Bookings", back_populates="user")
    properties = relationship("Place", back_populates="user")  
    reviews = relationship("Review", back_populates="user")

    def __init__(self, *args, **kwargs):
        """initializes User objec"""
        super().__init__(*args, **kwargs)
