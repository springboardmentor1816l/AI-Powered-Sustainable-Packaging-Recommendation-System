from flask import Flask, jsonify, render_template
from extensions.db import db
from api.predict import predict_bp
import os

def create_app():
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )

    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///local.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Home page
    @app.route("/")
    def home():
        return render_template("index.html")

    # Health check
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    # API routes
    app.register_blueprint(predict_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
