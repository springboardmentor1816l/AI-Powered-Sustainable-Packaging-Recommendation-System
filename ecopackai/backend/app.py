from flask import Flask
from routes.predict import predict_bp
from routes.recommend import recommend_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(predict_bp, url_prefix="/predict")
    app.register_blueprint(recommend_bp, url_prefix="/recommend")

    @app.route("/")
    def health():
        return {"status": "EcoPackAI API running"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
