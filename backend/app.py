import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_migrate import Migrate
from backend.db import db
from backend.cache import cache
from backend.models.material import Material
from backend.models.product import Product
from backend.models.prediction import RecommendationLog

from backend.routes.predict import predict_bp
from backend.routes.analytics import analytics_bp

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

db.init_app(app)
migrate = Migrate(app, db)
cache.init_app(app)

# Logging Configuration
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Application startup')

app.register_blueprint(predict_bp)
app.register_blueprint(analytics_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/results')
def results_page():
    return render_template('results.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

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
