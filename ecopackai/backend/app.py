from flask import Flask, request, jsonify
from flask_cors import CORS
from services.predictor import predict_scores

app = Flask(__name__)

# ✅ Enable CORS for frontend (development-safe)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "EcoPackAI backend running",
        "message": "Use POST /predict to get sustainability scores"
    })

# ✅ IMPORTANT: allow OPTIONS for preflight
@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    result = predict_scores(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
