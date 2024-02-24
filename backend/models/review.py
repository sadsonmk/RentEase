#!/usr/bin/env python3

from models.base_model import BaseModel, Base
from flask import Flask
import sqlalchemy
from sqlalchemy import Column, String, Integer, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Review(BaseModel, Base):
    __tablename__ = 'review'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    property_id = Column(String(60), ForeignKey('properties.id'), nullable=False)
    booking_id = Column(String(60), ForeignKey('bookings.id'), nullable=False)
    comment = Column(String(1000), nullable=False)
    rating = Column(Integer, nullable=False)
    miscellaneous = Column(String(1000), default="")
    picture = Column(BLOB, nullable=True, default=None)

    user = relationship("User", foreign_keys="Review.user_id",
                        back_populates="reviews")
    property = relationship("Property", foreign_keys="Review.property_id",
                            back_populates="reviews")
    booking = relationship("Booking", foreign_keys="Review.booking_id",
                           back_populates="review")

    def __init__(self, *args, **kwargs):
        """initializes Review object"""
        super().__init__(*args, **kwargs)
