from flask import Flask, jsonify
from predict import register_prediction_routes

# Create Flask app
app = Flask(__name__)

# Register prediction routes
register_prediction_routes(app)

# ------------------------
# Health Check Endpoint
# ------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "UP",
        "service": "EcoPackAI API",
        "message": "Service is running successfully"
    }), 200


# ------------------------
# Run the Flask App
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
