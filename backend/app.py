from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # allows frontend to call backend

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Temporary rule-based recommendation (NO dataset needed)
    recommendations = [
        {
            "rank": 1,
            "material": "Molded Pulp",
            "cost": 45,
            "co2": 1.2,
            "score": 0.92
        },
        {
            "rank": 2,
            "material": "Corrugated Board",
            "cost": 30,
            "co2": 1.8,
            "score": 0.81
        }
    ]

    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
