import os

from flask import jsonify, request


def validate_service_token():
    expected_token = os.environ["BACKEND_API_TOKEN"]
    authorization = request.headers.get("Authorization")

    if authorization != f"Bearer {expected_token}":
        return jsonify({
            "error": "Unauthorized"
        }), 401

    return None
