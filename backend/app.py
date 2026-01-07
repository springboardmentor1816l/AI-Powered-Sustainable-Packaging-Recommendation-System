from flask import Flask
from backend.config import Config
from backend.extensions import db, cache, migrate
from backend.routes.predict import predict_bp
from backend.logging_config import setup_logging
from backend.middleware.logging_middleware import register_logging
from backend import models


def create_app():
    setup_logging()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)

    register_logging(app)

    app.register_blueprint(predict_bp, url_prefix="/api")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


# 🔥 THIS IS WHAT KEEPS THE CONTAINER ALIVE
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)
