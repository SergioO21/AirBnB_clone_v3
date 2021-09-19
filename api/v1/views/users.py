#!/usr/bin/python3
""" User Module """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users_objs():
    """ Retrieves the list of all User objects """
    all_users = storage.all(User).values()
    users_list = []

    for user in all_users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_obj(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """ Creates a User """
    body = request.get_json()
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in body:
        return make_response(jsonify({"Missing email"}), 400)
    elif 'password' not in body:
        return make_response(jsonify({"Missing password"}), 400)

    new_user = User(**body)
    new_user.save()

    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"])
def put_user(user_id):
    """ Updates a User object """
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
