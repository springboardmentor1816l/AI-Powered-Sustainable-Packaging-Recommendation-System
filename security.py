import os
from flask import request, jsonify
from functools import wraps

API_KEY = os.getenv("PACKAGING_API_KEY")

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_key = request.headers.get("X-API-KEY")

        if not client_key or client_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

        return func(*args, **kwargs)

    return wrapper
