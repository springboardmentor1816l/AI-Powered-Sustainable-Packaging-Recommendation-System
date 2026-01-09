from flask import request, jsonify

API_KEY = "ecopackai-secret"

def require_api_key():
    api_key = request.headers.get("X-API-KEY")

    if api_key != API_KEY:
        return jsonify({
            "error": "Unauthorized – Invalid API Key"
        }), 401
