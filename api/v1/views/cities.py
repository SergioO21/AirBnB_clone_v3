#!/usr/bin/python3
""" City Module """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_objs(state_id):
    """ Retrieves the list of all City objects """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    all_cities = state.cities
    cities_list = []

    for city in all_cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_obj(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def post_city(state_id):
    """ Creates a City """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    body = request.get_json()
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    elif "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    body["state_id"] = state_id
    new_city = City(**body)
    new_city.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city_body = request.get_json()
    if not city_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in city_body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()

    return make_response(jsonify(city.to_dict()), 200)
