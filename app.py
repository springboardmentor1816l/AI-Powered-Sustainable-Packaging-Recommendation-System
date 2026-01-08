from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import logging

db = SQLAlchemy()
cache = Cache()

API_KEY = "mysecretkey123"


def require_api_key(func):
    def wrapper(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def create_app(testing=False):
    app = Flask(__name__)

    # CONFIG
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres123@localhost:5432/flash_backend_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = testing

    if testing:
        app.config["CACHE_TYPE"] = "NullCache"
    else:
        app.config["CACHE_TYPE"] = "SimpleCache"
        app.config["CACHE_DEFAULT_TIMEOUT"] = 60

    # INIT EXTENSIONS
    db.init_app(app)
    cache.init_app(app)

    # LOGGING
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # ROUTES
    @app.route("/")
    def home():
        return "Flask server is running successfully"

    @app.route("/predict/<product_name>")
    @cache.cached(timeout=60)
    @require_api_key
    def predict(product_name):
        return {
            "product": product_name,
            "recommendation": "Recycled Plastic"
        }

    return app


# RUN APP (ONLY WHEN NOT TESTING)
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
