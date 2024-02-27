#!/usr/bin/python3
"""handles views for users"""

from models.user import User
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

def validate_json(json_data, fields):
    for field, field_type in fields.items():
        if not json_data.get(field) or not isinstance(json_data.get(field), field_type):
            abort(400, description=f"Missing, empty or wrong type for {field}")

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    return jsonify([user.to_dict() for user in storage.all(User).values()])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id) or abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users', methods=['POST'])
def create_user():
    json_data = request.get_json() or abort(400, description="Not a JSON")
    fields = {
        'full_name': str,
        'email': str,
        'phone_number': str,
        'password': str,
        'verification_status': int,
        'profile_picture': (bytes, bytearray),
        'bio': str,
        'user_role': int
    }
    validate_json(json_data, fields)
    instance = User(**json_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id) or abort(404)
    data = request.get_json() or abort(400, description="Not a JSON")
    ignore = ['id', 'email', 'created_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id) or abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({'message': 'User deleted'}), 200)
