#!/usr/bin/python3
"""initializes the app environment"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api")

from api.views.index import *
from api.views.users import *
# from api.views.places_reviews import *