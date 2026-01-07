import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    os.makedirs("logs", exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s"
    )

    app_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=5_000_000, backupCount=3
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)

    error_handler = RotatingFileHandler(
        "logs/error.log", maxBytes=5_000_000, backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    app.logger.setLevel(logging.INFO)
