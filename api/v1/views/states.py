#!/usr/bin/python3
""" State Module """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_objs():
    """ Retrieves the list of all State objects """
    print("Me meti")
    all_states = storage.all(State).values()
    states_list = []

    for state in all_states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_obj(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """ Creates a State """
    body = request.get_json()
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    elif not body["name"]:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(**body)
    new_state.save()

    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def put_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state_body = request.get_json()
    if not state_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in state_body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()

    return make_response(jsonify(state.to_dict()), 200)
