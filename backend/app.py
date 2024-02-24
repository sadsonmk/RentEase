#!/usr/bin/python3
"""starts a flask app for our api"""

from api.views import app_views
from flask import Flask, jsonify
from models import storage

app = Flask(__name__)
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