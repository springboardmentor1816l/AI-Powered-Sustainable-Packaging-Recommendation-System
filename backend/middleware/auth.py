from flask import request, jsonify

API_KEY = "secret421"

def require_api_key():
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
