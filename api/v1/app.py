#!/usr/bin/python3
"""
Main App
"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = getenv('HBNB_API_PORT')

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(error):
    """
    Remove the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(threaded=True, host=HBNB_API_HOST, port=HBNB_API_PORT)
