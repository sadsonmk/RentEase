#!/usr/bin/python3
"""handles views for properties"""

from models.property import Property
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

def validate_json(json_data, fields):
    for field, field_type in fields.items():
        if not json_data.get(field) or not isinstance(json_data.get(field), field_type):
            abort(400, description=f"Missing, empty or wrong type for {field}")

@app_views.route('/properties', methods=['GET'], strict_slashes=False)
@swag_from('documentation/property/all_properties.yml')
def get_properties():
    return jsonify([property.to_dict() for property in storage.all(Property).values()])

@app_views.route('/properties/<property_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/property/get_property.yml', methods=['GET'])
def get_property(property_id):
    property = storage.get(Property, property_id) or abort(404)
    return jsonify(property.to_dict())

@app_views.route('/properties', methods=['POST'])
def create_property():
    json_data = request.get_json() or abort(400, description="Not a JSON")
    fields = {
        'user_id': str,
        'title': str,
        'description': str,
        'location': str,
        'address': str,
        'type': str,
        'picture': (bytes, bytearray),
        'price': float,
        'availability': bool,
        'miscellaneous': str
    }
    validate_json(json_data, fields)
    instance = Property(**json_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/properties/<property_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/property/put_property.yml', methods=['PUT'])
def update_property(property_id):
    property = storage.get(Property, property_id) or abort(404)
    data = request.get_json() or abort(400, description="Not a JSON")
    ignore = ['id', 'user_id', 'created_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(property, key, value)
    storage.save()
    return make_response(jsonify(property.to_dict()), 200)

@app_views.route('/properties/<property_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/property/delete_property.yml', methods=['DELETE'])
def delete_property(property_id):
    property = storage.get(Property, property_id) or abort(404)
    storage.delete(property)
    storage.save()
    return make_response(jsonify({'message': 'Property deleted'}), 200)