#!/usr/bin/python3
"""handles views for reviews"""

from models.review import Review
from models import storage
from api.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from datetime import datetime

def validate_json(json_data, fields):
    """
    Validates the JSON data against the specified fields.
    Aborts with a 400 status code if a field is missing, empty, or of the wrong type.
    """
    for field, field_type in fields.items():
        if not json_data.get(field) or not isinstance(json_data.get(field), field_type):
            abort(400, description=f"Missing, empty or wrong type for {field}")

@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
@swag_from('documentation/review/all_reviews.yml')
def get_reviews():
    """Returns all reviews in JSON format."""
    return jsonify([review.to_dict() for review in storage.all(Review).values()])

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/review/get_review.yml', methods=['GET'])
def get_review(review_id):
    """Returns a specific review in JSON format."""
    review = storage.get(Review, review_id) or abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews', methods=['POST'])
def create_review():
    """
    Creates a new review.
    Validates the JSON data before creating the review.
    """
    json_data = request.get_json() or abort(400, description="Not a JSON")
    fields = {
        'user_id': str,
        'property_id': str,
        'booking_id': str,
        'comment': str,
        'rating': int,
        'miscellaneous': str,
        'picture': (bytes, type(None))
    }
    validate_json(json_data, fields)
    instance = Review(**json_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/review/put_review.yml', methods=['PUT'])
def update_review(review_id):
    """
    Updates a specific review.
    Validates the JSON data before updating the review.
    """
    review = storage.get(Review, review_id) or abort(404)
    data = request.get_json() or abort(400, description="Not a JSON")
    ignore = ['id', 'user_id', 'property_id', 'booking_id']
    fields = {
        'comment': str,
        'rating': int,
        'miscellaneous': str,
        'picture': (bytes, type(None)),
        'updated_at': datetime
    }
    for key, value in data.items():
        if key not in ignore:
            if key in fields and not isinstance(value, fields[key]):
                abort(400, description=f"Wrong type for {key}")
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)

@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/review/delete_review.yml', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a specific review."""
    review = storage.get(Review, review_id) or abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({'message': 'Review deleted'}), 200)
