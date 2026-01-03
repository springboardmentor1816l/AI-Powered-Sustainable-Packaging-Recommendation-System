from flask import Flask, jsonify
from api.predict import predict_bp   # Option B import

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(predict_bp, url_prefix="/api")

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "ok",
            "service": "EcoPackAI Model API"
        }), 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
