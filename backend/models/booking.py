#!/usr/bin/python

from datetime import datetime
from models.base_model import BaseModel, Base
from flask import Flask
import sqlalchemy
from sqlalchemy import Column, String, Integer, Double
from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Booking(BaseModel, Base):
    __tablename__ = 'bookings'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    property_id = Column(String(60), ForeignKey('properties.id'), nullable=False)
    number_of_users = Column(Integer, nullable=False)
    total_cost = Column(Double, nullable=False)
    rent_purpose = Column(String(500), nullable=False)
    return_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    payment_status = Column(Boolean, nullable=False, default=False)

    user = relationship("User", foreign_keys="Booking.user_id",
                        back_populates="bookings")
    property = relationship("Property", foreign_keys="Booking.property_id",
                            back_populates="bookings")
    review = relationship("Review", back_populates="booking", uselist=False)

    def __init__(self, *args, **kwargs):
        """initializes Booking object"""
        super().__init__(*args, **kwargs)
