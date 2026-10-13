from flask import Blueprint, jsonify

# from ..auth import validate_service_token

hello = Blueprint("hello", __name__, url_prefix="/api")


# Token validation per blueprint
# @hello.before_request
# def authenticate():
#     return validate_service_token()

@hello.get("/hello")
def get_hello():
    return jsonify({
        "message": "Hello from Flask!"
    })
