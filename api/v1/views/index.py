#!/usr/bin/python3
"""Import package"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity


@app_views.route('/status')
def status():
    """This function return a json as example"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats')
def stats():
    """retrieves the number of each objects by type"""
    n_objs = {}
    classes = {"Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews", "State": "states",
               "User": "users"}
    for key, value in classes.items():
        n_objs[value] = storage.count(key)
    return jsonify(n_objs)
