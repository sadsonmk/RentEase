#!/usr/bin/python3
"""handles views for users"""

import os
from api.views import app_views
from flasgger.utils import swag_from
from flask import current_app, send_from_directory
from flask import Flask, abort, jsonify, make_response, request
from models import storage
from models.user import User
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from datetime import datetime


time = "%Y-%m-%dT%H:%M:%S.%f"


def parse_form_data(request):
    return {
        'full_name': request.form.get('full_name'),
        'email': request.form.get('email'),
        'phone_number': request.form.get('phone_number'),
        'password': request.form.get('password'),
        'verification_status': int(request.form.get('verification_status')),
        'profile_picture': request.files.get('profile_picture', None),
        'bio': request.form.get('bio'),
        'user_role': int(request.form.get('user_role'))
    }


def delete_file(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The file does not exist")


def handle_file_upload(file, upload_folder):
    if file.filename == '':
        abort(404, 'No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Check if the directory exists, if not, create it
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Read the file into a byte array
        with open(file_path, 'rb') as f:
            blob = f.read()

        return file_path, blob


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_user_instance(json_data):
    instance = User(**json_data)
    instance.save()
    return instance


def get_image():
    image = request.files.get('image')
    if not image:
        raise ValueError
    image = Image.open(image.stream).convert('RGB')
    return image


def get_file_bytes(filename) -> None | bytes:
    if not (_uploaded := request.files.get(filename)):
        return None
    return _uploaded.read()


# def upload_profile_image():
#     data = request.files
#     uploaded_image = upload(data.get("image"))
#     current_user.update(image=uploaded_image["public_id"])
#     return {"image": uploaded_image["url"]}


def validate_json(json_data, fields):
    for field, field_type in fields.items():
        if not json_data.get(field) or not isinstance(
            json_data.get(field),
                field_type):
            abort(400,
                  description=f"Missing, empty or wrong type for {field}:\
                    Expected {field_type} but got {type(field)}")


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    user = storage.get(User, user_id) or abort(404, "User not found")
    return jsonify(user.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/create_user.yml', methods=['POST'])
def create_user():
    # Perform validation
    fields = {
        'full_name': str,
        'email': str,
        'phone_number': str,
        'password': str,
        'verification_status': int,
        'profile_picture': str,
        'bio': str,
        'user_role': int
    }

    if request.content_type.startswith('multipart/form-data'):
        # Parse form data
        json_data = parse_form_data(request)
        # Assuming you have a Flask request object with a file
        file = request.files['profile_picture']

        # Check if the post request has the file part
        if json_data['profile_picture']:
            file = request.files['profile_picture']
            file.filename = secure_filename(str(datetime.now().strftime(time)) + file.filename)
            
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path, blob = handle_file_upload(file, upload_folder)
            json_data['profile_picture'] = file.filename

    elif request.content_type.startswith('application/json'):
        json_data = request.get_json() or abort(400, description="Not a JSON")
    else:
        abort(415, description="Unsupported Media Type")

    # Validate JSON data
    validate_json(json_data, fields)
    binary_data = blob
    # Create User instance
    instance = create_user_instance(json_data)
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/update_user.yml', methods=['PUT'])
def update_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404, description="User not found")

    # Perform validation
    fields = {
        'full_name': str,
        'phone_number': str,
        'verification_status': int,
        'profile_picture': str,
        'bio': str,
        'user_role': int
    }

    if request.content_type.startswith('multipart/form-data'):
        # Parse form data
        json_data = parse_form_data(request)

        # Assuming you have a Flask request object with a file
        if 'profile_picture' in request.files:
            # Delete the old picture
            if user.profile_picture:
                delete_file(user.profile_picture)

            file = request.files['profile_picture']
            file.filename = secure_filename(str(datetime.now().strftime(time)) + file.filename)
            
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path, blob = handle_file_upload(file, upload_folder)
            json_data['profile_picture'] = file.filename

        # Update user fields
        for key, value in json_data.items():
            if key in fields and hasattr(user, key):
                setattr(user, key, value)

    elif request.content_type.startswith('application/json'):
        json_data = request.get_json() or abort(400, description="Not a JSON")
        # Update user fields
        for key, value in json_data.items():
            if key in fields and hasattr(user, key):
                setattr(user, key, value)
    else:
        abort(415, description="Unsupported Media Type")

    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id) or abort(404, "User not found")
    storage.delete(user)
    storage.save()
    return make_response(jsonify({'message': 'User deleted'}), 200)


@app_views.route('/uploads/<filename>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_image.yml', methods=['GET'])
def uploaded_file(filename):
    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    if not upload_folder:
        current_app.logger.error("UPLOAD_FOLDER is not set")
        return jsonify({'message': 'Server configuration error'}), 500

    dir_path = os.path.join(upload_folder, '')
    if not os.path.isdir(dir_path):
        current_app.logger.error(f"Directory {dir_path} does not exist")
        return jsonify({'message': 'File not found'}), 404

    file_path = os.path.join(dir_path, filename)
    if not os.path.isfile(file_path):
        current_app.logger.error(f"File {file_path} does not exist")
        return jsonify({'message': 'File not found'}), 404

    return send_from_directory(dir_path, filename)
