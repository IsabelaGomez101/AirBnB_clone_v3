#!/usr/bin/python3
"""Import package"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    list = []
    for i in storage.all(User).values():
        list.append(i.to_dict())
    return jsonify(list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by id"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    elif "email" not in data.keys():
        abort(400, description="Missing email")
    elif "password" not in data.keys():
        abort(400, description="Missing password")
    else:
        new_user = User(**data)
        storage.new(new_user)
        storage.save()
        obj = storage.get(User, new_user.id)
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by id"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    else:
        data = request.get_json(silent=True)
        if data is None:
            abort(400, description="Not a JSON")
        list_arg = ["id", "email", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in list_arg:
                setattr(obj, key, value)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 200)
