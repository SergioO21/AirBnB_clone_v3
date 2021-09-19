#!/usr/bin/python3
""" User Module """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.state import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users_objs():
    """ Retrieves the list of all State objects """
    all_users = storage.all(User).values()
    users_list = []

    for user in all_users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_obj(state_id):
    """ Retrieves a State object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(state_id):
    """ Deletes a State object """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """ Creates a State """
    body = request.get_json()
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if body.get('email') is None:
        return make_response("Missing email", 400)
    elif body.get('password') is None:
        return make_response("Missing password", 400)

    new_state = State(**body)
    new_state.save()

    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """ Updates a State object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user_body = request.get_json()
    if not user_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in user_body.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()

    return make_response(jsonify(user.to_dict()), 200)
