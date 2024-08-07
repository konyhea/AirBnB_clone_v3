#!/usr/bin/python3
"""create state from flask app"""
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_cities(city_id):
    """Retrieve  places of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Get specific place with id"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def del_place(place_id):
    """Delete place_id from storage"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Create place from cities"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get(User, data['user_id'])
    if not user:
        return abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """update place with specific id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_attr = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_attr:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    return abort(404)
