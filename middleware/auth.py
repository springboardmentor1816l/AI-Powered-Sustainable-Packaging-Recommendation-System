from flask import request, jsonify
from functools import wraps

# In a real app, this would be an environment variable
API_KEY = "ecopack-secret-2026"

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for X-API-KEY in headers
        if request.headers.get('X-API-KEY') == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401
    return decorated_function