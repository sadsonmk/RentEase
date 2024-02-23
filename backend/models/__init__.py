#!/usr/bin/python3
"""
initialize the models package
"""

from models.engine.storage import DBStorage
storage = DBStorage()
storage.reload()
