from flask import Flask
from config import Config
from extensions import db, cache
from routes.health import health_bp
from routes.predict import predict_bp
import logging
import os
import time
from sqlalchemy.exc import OperationalError

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    cache.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp)

    # Create logs directory
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/app.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    # ✅ WAIT FOR MYSQL
    with app.app_context():
        for i in range(10):  # retry 10 times
            try:
                db.create_all()
                logging.info("Database connected and tables created")
                break
            except OperationalError:
                logging.warning("Database not ready, retrying...")
                time.sleep(3)
        else:
            raise RuntimeError("Database not available")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
