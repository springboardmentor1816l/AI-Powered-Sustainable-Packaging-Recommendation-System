from flask import Flask, jsonify
from api.predict import predict_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(predict_bp, url_prefix="/api")

    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "UP",
            "service": "EcoPackAI API",
            "message": "Service is healthy"
        }), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
