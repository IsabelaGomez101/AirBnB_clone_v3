#!/usr/bin/python3
"""Import package"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """This function return a json as example"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    n_objs = {}
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    keys = ["amenities", "cities", "places", "reviews", "states", "users"]
    for i in range(len(classes)):
        n_objs[keys[i]] = storage.count(classes[i])
    return jsonify(n_objs)
