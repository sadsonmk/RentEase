#!/usr/bin/python3
"""handles views for properties"""

import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import current_app
from models.property import Property
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from api.views.utils import Utility


time = "%Y-%m-%dT%H:%M:%S.%f"

@app_views.route('/properties', methods=['GET'], strict_slashes=False)
@swag_from('documentation/property/all_properties.yml')
def get_properties():
    return jsonify([property.to_dict() for property in storage.all(Property).values()])


@app_views.route('/properties/<property_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/property/get_property.yml', methods=['GET'])
def get_property(property_id):
    property = storage.get(Property, property_id) or abort(404)
    return jsonify(property.to_dict())


@app_views.route('/properties', methods=['POST'], strict_slashes=False)
@swag_from('documentation/property/post_property.yml', methods=['POST'])
def create_property():
    fields = {
        'user_id': str,
        'title': str,
        'description': str,
        'location': str,
        'address': str,
        'type': str,
        'picture': str,
        'price': float,
        'availability': bool,
        'miscellaneous': str
    }

    if request.content_type.startswith('multipart/form-data'):
        json_data = Utility.parse_form_data(request)

        if 'picture' in request.files:
            file = request.files['picture']
            if file:
                file.filename = Utility.secure_filename_with_time(file)
                upload_folder = current_app.config['PROPERTY']
                file_path, blob = Utility.handle_file_upload(file, upload_folder)
                json_data['picture'] = file.filename
    elif request.content_type.startswith('application/json'):
        json_data = request.get_json() or abort(400, description="Not a JSON")
    else:
        abort(415, description="Unsupported Media Type")

    Utility.validate_json(json_data, fields)

    instance = Property(**json_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/properties/<property_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/property/put_property.yml', methods=['PUT'])
def update_property(property_id):
    property: Property = storage.get(Property, property_id)
    if not property:
        abort(404, description="Property not found")

    # Perform validation
    fields = {
        'user_id': str,
        'title': str,
        'description': str,
        'location': str,
        'address': str,
        'type': str,
        'picture': str,
        'price': float,
        'availability': bool,
        'miscellaneous': str
    }

    if request.content_type.startswith('multipart/form-data'):
        # Parse form data
        json_data = Utility.parse_form_data(request)

        # Assuming you have a Flask request object with a file
        if 'picture' in request.files:
            
            upload_folder = current_app.config['PROPERTY']
            # Delete the old picture
            if property.picture:
                Utility.delete_file(property.picture, upload_folder)

            file = request.files['picture']
            if file:
                file.filename = Utility.secure_filename_with_time(file)

                file_path, blob = Utility.handle_file_upload(file, upload_folder)
                json_data['picture'] = file.filename

        # Update property fields
        for key, value in json_data.items():
            if key in fields and hasattr(property, key):
                setattr(property, key, value)

    elif request.content_type.startswith('application/json'):
        json_data = request.get_json() or abort(400, description="Not a JSON")
        # Update property fields
        for key, value in json_data.items():
            if key in fields and hasattr(property, key):
                setattr(property, key, value)
    else:
        abort(415, description="Unsupported Media Type")

    property.save()
    return jsonify(property.to_dict()), 200

@app_views.route('/properties/<property_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/property/delete_property.yml', methods=['DELETE'])
def delete_property(property_id):
    property = storage.get(Property, property_id) or abort(404)
    storage.delete(property)
    storage.save()
    return make_response(jsonify({'message': 'Property deleted'}), 200)