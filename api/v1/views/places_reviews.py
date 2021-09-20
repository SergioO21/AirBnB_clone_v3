#!/usr/bin/python3
""" Place Module """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models import storage
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def review_objs(place_id):
    """ Retrieves the list of all Place reviews objects """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all_reviews = place.reviews
    reviews_list = []

    for review in all_reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def review_obj(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def post_review(place_id):
    """ Creates a Review """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    body = request.get_json()
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    elif "user_id" not in body:
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    elif "text" not in body:
        return make_response(jsonify({"error": "Missing text"}), 400)

    user = storage.get(User, body.get("user_id"))
    if not user:
        abort(404)

    body["review_id"] = place_id
    new_review = Review(**body)
    new_review.save()

    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review_body = request.get_json()
    if not review_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in review_body.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()

    return make_response(jsonify(review.to_dict()), 200)
