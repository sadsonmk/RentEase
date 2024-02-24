#!/usr/bin/python3
"""handles views for bookings"""

from models.booking import Booking
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

def parse_date(date_string):
    """
    Parses a date string into a datetime object using the format '%Y-%m-%dT%H:%M:%S.%f'.
    Aborts with a 400 status code if the date string is not in the correct format.
    """
    try:
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        abort(400, description="Invalid date format, expected YYYY-MM-DDTHH:MM:SS.ssssss")

@app_views.route('/bookings', methods=['GET'], strict_slashes=False)
@swag_from('documentation/booking/all_bookings.yml')
def get_bookings():
    """Returns all bookings in JSON format."""
    return jsonify([booking.to_dict() for booking in storage.all(Booking).values()])

@app_views.route('/bookings/<booking_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/booking/get_booking.yml', methods=['GET'])
def get_booking(booking_id):
    """Returns a specific booking in JSON format."""
    booking = storage.get(Booking, booking_id) or abort(404)
    return jsonify(booking.to_dict())

@app_views.route('/bookings', methods=['POST'])
def create_booking():
    """
    Creates a new booking.
    Validates the JSON data and parses the return_date before creating the booking.
    """
    json_data = request.get_json() or abort(400, description="Not a JSON")
    fields = {
        'user_id': str,
        'property_id': str,
        'number_of_users': int,
        'total_cost': float,
        'rent_purpose': str,
        'payment_status': bool
    }
    validate_json(json_data, fields)
    json_data['return_date'] = parse_date(json_data['return_date'])
    instance = Booking(**json_data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/bookings/<booking_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/booking/put_booking.yml', methods=['PUT'])
def update_booking(booking_id):
    """
    Updates a specific booking.
    Validates the JSON data and parses the return_date and updated_at before updating the booking.
    """
    booking = storage.get(Booking, booking_id) or abort(404)
    data = request.get_json() or abort(400, description="Not a JSON")
    ignore = ['id', 'user_id', 'property_id', 'created_at']
    fields = {
        'number_of_users': int,
        'total_cost': float,
        'rent_purpose': str,
        'payment_status': bool,
        'updated_at': datetime
    }
    for key, value in data.items():
        if key not in ignore:
            if key == 'return_date' or key == 'updated_at':
                value = parse_date(value)
            elif key in fields and not isinstance(value, fields[key]):
                abort(400, description=f"Wrong type for {key}")
            setattr(booking, key, value)
    storage.save()
    return make_response(jsonify(booking.to_dict()), 200)

@app_views.route('/bookings/<booking_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/booking/delete_booking.yml', methods=['DELETE'])
def delete_booking(booking_id):
    """Deletes a specific booking."""
    booking = storage.get(Booking, booking_id) or abort(404)
    storage.delete(booking)
    storage.save()
    return make_response(jsonify({'message': 'Booking deleted'}), 200)
