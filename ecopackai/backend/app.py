import os
import sys

# =====================================================
# Add project root (ecopackai) to Python path
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # ecopackai/backend
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))  # ecopackai
sys.path.insert(0, PROJECT_ROOT)

# =====================================================
# Flask imports (AFTER path fix)
# =====================================================
from flask import Flask
from routes.predict import predict_bp
from routes.recommend import recommend_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(predict_bp, url_prefix="/predict")
    app.register_blueprint(recommend_bp, url_prefix="/recommend")

    @app.route("/")
    def health():
        return {"status": "EcoPackAI backend running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


