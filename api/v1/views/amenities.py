#!/usr/bin/python3
"""Import package"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity():
    """Retrieves the list of all Amenity objects"""
    list = []
    for i in storage.all(Amenity).values():
        list.append(i.to_dict())
    return jsonify(list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new Amenity"""
    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    elif "name" not in data.keys():
        abort(400, description="Missing name")
    else:
        new_amenity = Amenity(**data)
        storage.new(new_amenity)
        storage.save()
        obj = storage.get(Amenity, new_amenity.id)
        return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object by id"""
    obj = storage.get(Amenity, amenity_id)
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
