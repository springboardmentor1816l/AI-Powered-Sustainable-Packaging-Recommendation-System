import uuid
import logging
from flask import request, g

logger = logging.getLogger("request")

def register_logging(app):

    @app.before_request
    def before_request():
        g.request_id = str(uuid.uuid4())
        logger.info(
            f"Incoming request {request.method} {request.path}",
            extra={"request_id": g.request_id}
        )

    @app.after_request
    def after_request(response):
        logger.info(
            f"Response {response.status_code} for {request.method} {request.path}",
            extra={"request_id": g.request_id}
        )
        return response
