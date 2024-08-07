#!/usr/bin/python3
"""create state from flask app"""
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """Retrieve all user obj"""
    user = storage.all(User).value()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """Get specific user with id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)  # noqa
def del_user(user_id):
    """Delete user_id from storage"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create user to Userss"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    if 'email' not in kwargs:
        return abort(400, 'Missing email')
    if 'password' not in kwargs:
        return abort(400, 'Missing password')
    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """update user with specific id"""
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            return abort(404, 'Not a JSON')
        if request.content_type != 'application/json':
            return abort(404, 'Not a JSON')
        data = request.get_json()
        ignore_attr = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_attr:
                setattr(User, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    return abort(404)
