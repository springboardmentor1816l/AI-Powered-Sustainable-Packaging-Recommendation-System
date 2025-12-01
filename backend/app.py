from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Expected JSON payload (example):
    {
      "product_id": "P001",
      "weight_g": 500,
      "dimensions_cm": {"l":10,"w":5,"h":5},
      "priority": ["cost","co2"]
    }
    """
    data = request.get_json()
    # TODO: call ML inference module
    # placeholder response
    response = {
        "product_id": data.get("product_id"),
        "recommendations": [
            {"material":"Corrugated Cardboard","score":0.92,"estimated_co2_kg":0.12,"estimated_cost_usd":0.25},
            {"material":"Recycled Paper","score":0.86,"estimated_co2_kg":0.15,"estimated_cost_usd":0.22}
        ]
    }
    return jsonify(response), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
