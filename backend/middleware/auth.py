from functools import wraps
from flask import request, jsonify
import os

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        valid_api_key = os.environ.get('API_KEY', 'default-dev-key')
        
        if api_key and api_key == valid_api_key:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401
    return decorated_function
