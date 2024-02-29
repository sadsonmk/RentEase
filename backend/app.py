#!/usr/bin/python3
"""starts a flask app for our api"""
import os
from werkzeug.datastructures import FileStorage
from api.views import app_views
from flask import Flask, jsonify
from models import storage
import logging

app = Flask(__name__)


relative_path = './backend/misc/owners/UPLOAD_FOLDER'
absolute_path = os.path.abspath(relative_path)

relative_prop = './backend/misc/props/PROPERTY'
absolute_prop = os.path.abspath(relative_prop)

relative_revs = './backend/revs/props/REVIEWS'
absolute_revs = os.path.abspath(relative_revs)

app.config['UPLOAD_FOLDER'] = absolute_path
app.config['PROPERTY'] = absolute_prop
app.config['REVIEWS'] = absolute_revs
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

upload_folder = app.config['UPLOAD_FOLDER']
prop_folder = app.config['UPLOAD_FOLDER']
revs_folder = app.config['UPLOAD_FOLDER']

# Check if the directory exists, if not, create it
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# Check if the directory exists, if not, create it
if not os.path.exists(prop_folder):
    os.makedirs(prop_folder)

# Check if the directory exists, if not, create it
if not os.path.exists(revs_folder):
    os.makedirs(revs_folder)


# Set up the logger
handler = logging.FileHandler('error.log')  # errors are logged to this file
handler.setLevel(logging.ERROR)  # only log errors and above
app.logger.addHandler(handler)

# Your routes and other code...

app.register_blueprint(app_views)

@app.teardown_appcontext
def tear(exception):
    """closes the app and frees up resources"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return jsonify({'error': "Page Not found"}), 404


# value_host = os.getenv('HBNB_API_HOST')
# value_port = os.getenv('HBNB_API_PORT')
# if value_host is not None:
#     host = value_host
# else:
host = '0.0.0.0'

# if value_port is not None:
#     port = value_port
# else:
port = 5000

if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)