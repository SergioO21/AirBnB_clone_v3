#!/usr/bin/python3
""" Index module """


from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """ Route that returns a json response"""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass
