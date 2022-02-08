#!/usr/bin/python3
"""Import package"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        list.append(city.to_dict())
    return jsonify(list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves a City object by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by id"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    elif "name" not in data.keys():
        abort(400, description="Missing name")
    else:
        new_city = City(**data)
        new_city.state_id = state.id
        storage.new(new_city)
        storage.save()
        obj = storage.get(State, new_city.id)
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object by id"""
    obj = storage.get(City, city_id)
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
