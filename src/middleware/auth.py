from flask import request, jsonify
from functools import wraps
import os

# In real production, load this from ENV
API_KEY = os.getenv("ECOPACK_API_KEY", "ecopack-secret-key")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return jsonify({
                "error": "API key missing"
            }), 401

        if api_key != API_KEY:
            return jsonify({
                "error": "Invalid API key"
            }), 403

        return f(*args, **kwargs)
    return decorated
