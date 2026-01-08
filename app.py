from flask import Flask, jsonify
from extensions.db import db
from api.predict import predict_bp
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///local.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    app.register_blueprint(predict_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
