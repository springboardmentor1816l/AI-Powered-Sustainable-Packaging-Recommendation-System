from flask import Flask, request, jsonify
from services.predictor import predict_scores

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "EcoPackAI backend running",
        "message": "Use POST /predict to get sustainability scores"
    })

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    result = predict_scores(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
