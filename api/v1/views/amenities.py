#!/usr/bin/python3
""" Amenity Module """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_objs():
    """ Retrieves the list of all Amenity objects """
    all_amenities = storage.all(Amenity).values()
    amenities_list = []

    for amenity in all_amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def amenity_obj(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """ Creates a Amenity """
    body = request.get_json()
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    elif "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(**body)
    new_amenity.save()

    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """ Updates a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity_body = request.get_json()
    if not amenity_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in amenity_body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 200)
