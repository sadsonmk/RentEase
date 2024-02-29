#!/usr/bin/env python3

from models.base_model import BaseModel, Base
from flask import Flask
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import Float, ForeignKey, Boolean

class Property(BaseModel, Base):
    __tablename__ = 'properties'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    location = Column(String(500), nullable=False)
    address = Column(String(500), nullable=False)
    type = Column(String(45), nullable=False)
    picture = Column(String(500), nullable=True, default=None)
    price = Column(Float, nullable=False)
    availability = Column(Boolean, nullable=False)
    miscellaneous = Column(String(500))

    user = relationship("User", foreign_keys="Property.user_id",
                        back_populates="properties")
    bookings = relationship("Booking", back_populates="property")
    reviews = relationship("Review", back_populates="property")

    def __init__(self, *args, **kwargs):
        """initializes Property object"""
        super().__init__(*args, **kwargs)
