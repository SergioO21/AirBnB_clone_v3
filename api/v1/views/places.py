#!/usr/bin/python3
""" City Module """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models.city import City
from models.place import Place
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def place_city_objs(city_id):
    """ Retrieves the list of all City places objects """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    all_places = city.places
    places_list = []

    for place in all_places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_obj_id(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def post_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    body = request.get_json()
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    elif "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    body["city_id"] = city_id
    new_place = Place(**body)
    new_place.save()

    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place_body = request.get_json()
    if not place_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in place_body.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, key, value)
    place.save()

    return make_response(jsonify(place.to_dict()), 200)
