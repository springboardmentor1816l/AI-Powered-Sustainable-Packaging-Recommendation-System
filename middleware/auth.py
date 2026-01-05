from flask import request, abort

def require_api_key():
    api_key = request.headers.get("X-API-KEY")

    if api_key != "mysecretkey":
        abort(401)
