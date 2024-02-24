#!/usr/bin/python3
"""initializes the app environment"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api")

from api.views.index import *
from api.views.users import *
from api.views.properties import *
from api.views.bookings import *
from api.views.reviews import *
