#!/usr/bin/python3
"""create state from flask app"""
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_all_amenities():
    """Retrieve  amenities from db"""
    amenity_list = []
    for key, value in storage.all(Amenity).items():
        amenity_list.append(value.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """Get specific amwnity with id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def del_amenity(amenity_id):
    """Delete amenity_id from storage"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create amenity in the db"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    if 'name' not in kwargs:
        return abort(400, 'Missing name')
    amenity = Amenity(**kwargs)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Update amenity with specific id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_attr = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_attr:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    return abort(404)
