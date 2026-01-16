from flask import Flask, jsonify, request, send_from_directory
from src.api.predict import predict_bp
from src.db.database import db
from src.logging.logger import setup_logger
from src.cache.cache import cache
from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

def create_app():
    app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://ecopack_user:ecopack123@localhost:3306/ecopack"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    import src.db.models

    logger = setup_logger()
    cache.init_app(app)

    @app.before_request
    def log_request():
        logger.info(
            f"Request | {request.method} {request.path} | IP={request.remote_addr}"
        )

    app.register_blueprint(predict_bp)

    # ✅ Serve frontend pages
    @app.route("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/results.html")
    def results():
        return send_from_directory(FRONTEND_DIR, "results.html")

    @app.route("/analytics.html")
    def analytics():
        return send_from_directory(FRONTEND_DIR, "analytics.html")

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
