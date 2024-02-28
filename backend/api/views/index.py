#!/usr/bin/python3
"""This file returns the JSON status ok"""

from api.views import app_views
from flask import Flask, jsonify
from models import storage
from models.base_model import Base, BaseModel
from models.booking import Booking
from models.property import Property
from models.review import Review
from models.user import User

classes = {"Bookings": Booking, "Property": Property, 
           "Review": Review, "User": User}


@app_views.route('/index', strict_slashes=False, methods=['GET'])
def index():
    """home screen of the app"""
    return jsonify({"status": "OK"})

@app_views.route('/home', strict_slashes=False, methods=['GET'])
def home():
    """home screen of the app"""
    return jsonify([{'id': 1,
        "title": 'Apartment',
        'description': 'a modern apartment building',
        'image': '...',
        'price': '$1,500/month',
        'location': 'Beijing/China'},  {
       'id': 2,
       "title": 'Apartment',
       'description': 'a modern apartment building',
       'image': '...',
       'price': '$2,500/month',
       'location': 'Shanghai/China'
   }])

@app_views.route('/', strict_slashes=False, methods=['GET'])
def base():
    """home screen of the app"""
    return jsonify({
        'id': 1,
        'title': 'Apartment',
        'description': 'a modern apartment building',
        'image': '...',
        'price': '$1,500/month',
        'location': 'Beijing/China'
    })

@app_views.route('/stats')
def num_objects():
    """counts each object in store"""
    result = {}
    for key, value in classes.items():
        total = storage.count(value)
        result[key.lower()] = total
    return jsonify(result)
