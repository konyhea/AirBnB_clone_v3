#!/usr/bin/python3
"""create state from flask app"""
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_states():
    """Retrieve  cities  object of a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """Get specific city with id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def del_city(city_id):
    """Delete city_id from storage"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Create city in cities"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    if 'name' not in kwargs:
        return abort(400, 'Missing name')
    kwargs['state_id'] = state_id
    city = City(**kwargs)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """update city with specific id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_attr = ['id', 'state_id',  'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_attr:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    return abort(404)
