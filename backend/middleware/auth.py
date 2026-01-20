from flask import request, jsonify, current_app, g
from functools import wraps
import logging

security_logger = logging.getLogger("security")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # ✅ ALLOW CORS PREFLIGHT REQUESTS
        if request.method == "OPTIONS":
            return "", 200

        api_key = request.headers.get("X-API-KEY")

        if not api_key or api_key != current_app.config["API_KEY"]:
            security_logger.warning(
                "Unauthorized access attempt",
                extra={"request_id": getattr(g, "request_id", "-")}
            )
            return jsonify({"error": "Unauthorized"}), 401

        return f(*args, **kwargs)

    return decorated
