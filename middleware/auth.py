from flask import request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

def require_api_key():
    key = request.headers.get("X-API-Key")
    if not key or key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
