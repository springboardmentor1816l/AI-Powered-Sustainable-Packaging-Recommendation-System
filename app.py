from flask import Flask
from api.predict import predict_bp

app = Flask(__name__)
app.register_blueprint(predict_bp, url_prefix="/api")

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
