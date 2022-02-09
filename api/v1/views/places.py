#!/usr/bin/python3
"""Import package"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_cities(city_id):
    """Retrieves the list of all Cities objects of a Place"""
    list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for i in storage.all(Place).values():
        if i.city_id == city_id:
            list.append(i.to_dict())
    return jsonify(list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by id"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data.keys():
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if "name" not in data.keys():
        abort(400, description="Missing name")
    data["city_id"] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    obj = storage.get(Place, new_place.id)
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by id"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
        list_arg = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in list_arg:
                setattr(obj, key, value)
        storage.save()
        return make_response(jsonify(obj.to_dict()), 200)
