#!/usr/bin/python3
"""Import package"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    list = []
    for i in storage.all(State).values():
        list.append(i.to_dict())
    return jsonify(list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_by_id(state_id):
    """Retrieves a State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by id"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    elif "name" not in data.keys():
        abort(400, description="Missing name")
    else:
        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        obj = storage.get(State, new_state.id)
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by id"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    else:
        data = request.get_json(silent=True)
        if data is None:
            abort(400, description="Not a JSON")
        list_arg = ["id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in list_arg:
                setattr(obj, key, value)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 200)
