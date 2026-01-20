from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.routes.predict import predict_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(predict_bp)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify service status.
    Returns a JSON response indicating the service is healthy.
    """
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
