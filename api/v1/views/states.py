#!/usr/bin/python3
"""create state from flask app"""
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """Retrieve all state obj"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """Get specific state with id"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def del_state(state_id):
    """Delete state_id from storage"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create state to states"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(404, 'Not a JSON')
    kwargs = request.get_json()
    if 'name' not in kwargs:
        return abort(400, 'Missing name')
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update state with specific id"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_attr = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_attr:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    return abort(404)
