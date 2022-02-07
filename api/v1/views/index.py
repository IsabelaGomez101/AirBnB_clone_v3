#!/usr/bin/python3
"""Import package"""
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """This function return a json as example"""
    stat = {"status": "OK"}
    return stat
