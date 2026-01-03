from flask import request, jsonify
from config import Config

def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if api_key != Config.API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
