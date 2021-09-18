#!/usr/bin/python3
""" Index module """

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """ Route that returns a json response"""
    return jsonify({"status": "OK"})

@app_views.route("/stats", strict_slashes=False)
def stats():
    """ Retrieves the number of each element by type"""
    new_dict2 = {}
    for key, value in classes.item:
        number = storage.count(value)
        new_dict2[key] = number
    return jsonify(new_dict2)

if __name__ == "__main__":
    pass
