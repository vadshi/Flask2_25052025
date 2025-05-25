from my_app.hello_as_bp.models import MESSAGES
from flask import Blueprint, jsonify


hello = Blueprint("hello", __name__)

@hello.route("/")
@hello.route("/hello", methods=["GET"])
def hello_world():
    return jsonify(MESSAGES["default"]), 200


@hello.get("/show/<key>")
def get_message(key: str):
    return jsonify(MESSAGES.get(key) or f"URL: /show/{key} not found."), 200