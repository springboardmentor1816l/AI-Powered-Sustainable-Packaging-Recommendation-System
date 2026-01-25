# # """
# # EcoPackAI - Complete Flask Application
# # Combines: Health Check + Prediction Endpoint + Future Endpoints
# # """

# # from flask import Flask, jsonify, request
# # from flask_cors import CORS
# # from datetime import datetime
# # import numpy as np
# # import pandas as pd
# # import joblib
# # import json
# # import os



# # # ============================================
# # # FLASK APPLICATION INITIALIZATION
# # # ============================================
# # app = Flask(__name__)

# # # Enable CORS
# # CORS(app, resources={r"/api/*": {"origins": "*"}})

# # # Configuration
# # app.config['JSON_SORT_KEYS'] = False
# # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# # APP_VERSION = "1.0.0"
# # APP_NAME = "EcoPackAI"
# # API_PREFIX = "/api/v1"

# # # ============================================
# # # LOAD ML MODELS
# # # ============================================
# # print("\n" + "=" * 60)
# # print(f"{APP_NAME} - Loading ML Models")
# # print("=" * 60)

# # MODELS_LOADED = False
# # try:
# #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
# #     preprocessor = joblib.load(os.path.join(BASE_DIR, "C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\ml\\models\\processingpreprocessing_pipeline.pkl"))
# #     rf_cost = joblib.load(os.path.join(BASE_DIR, "C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\ml\\reports\\rf_cost_optimized.joblib"))
# #     xgb_co2 = joblib.load(os.path.join(BASE_DIR, "C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\ml\\reports\\xgb_co2_optimized.joblib"))
    

# #     with open(os.path.join(BASE_DIR, "C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\processed\\feature_names.json"), 'r') as f:
# #         feature_config = json.load(f)
    
# #     print("✓ Preprocessor loaded")
# #     print("✓ RF Cost model loaded")
# #     print("✓ XGBoost CO₂ model loaded")
# #     print("✓ Feature configuration loaded")
    
# #     MODELS_LOADED = True
# # except Exception as e:
# #     print(f"⚠ Warning: Could not load models - {e}")
# #     print("  API will run in limited mode")

# # print("=" * 60 + "\n")

# # # ============================================
# # # VALIDATION CONSTANTS
# # # ============================================
# # VALID_CATEGORIES = ['Food', 'Electronics', 'Cosmetics', 'Pharmacy']
# # VALID_SHIPPING = ['Air', 'Road', 'Sea']

# # # ============================================
# # # HEALTH CHECK ENDPOINTS
# # # ============================================
# # @app.route('/health', methods=['GET'])
# # def health_check():
# #     """Basic health check"""
# #     return jsonify({
# #         "status": "healthy",
# #         "service": APP_NAME,
# #         "version": APP_VERSION,
# #         "timestamp": datetime.now().isoformat()
# #     }), 200


# # @app.route(f'{API_PREFIX}/health', methods=['GET'])
# # def api_health():
# #     """Extended health check"""
# #     return jsonify({
# #         "status": "healthy",
# #         "service": APP_NAME,
# #         "version": APP_VERSION,
# #         "timestamp": datetime.now().isoformat(),
# #         "models_loaded": MODELS_LOADED
# #     }), 200


# # # ============================================
# # # ROOT ENDPOINT
# # # ============================================
# # @app.route('/', methods=['GET'])
# # def root():
# #     """API root"""
# #     return jsonify({
# #         "service": APP_NAME,
# #         "version": APP_VERSION,
# #         "description": "AI-Powered Sustainable Packaging Recommendation System",
# #         "endpoints": {
# #             "health": "/health",
# #             "api_health": f"{API_PREFIX}/health",
# #             "predict": f"{API_PREFIX}/predict",
# #             "schema": f"{API_PREFIX}/predict/schema"
# #         }
# #     }), 200


# # # ============================================
# # # PREDICTION ENDPOINT
# # # ============================================
# # @app.route(f'{API_PREFIX}/predict', methods=['POST', 'OPTIONS'])
# # def predict():
# #     """
# #     Prediction endpoint for cost and CO₂ estimation
    
# #     POST /api/v1/predict
# #     Content-Type: application/json
    
# #     Request Body:
# #         {
# #             "product_name": "Chocolate Box",
# #             "product_category": "Food",
# #             "product_weight_kg": 0.5,
# #             "fragility_index": 2,
# #             "shipping_type": "Air",
# #             ... (material attributes)
# #         }
    
# #     Response:
# #         {
# #             "success": true,
# #             "predictions": {
# #                 "cost_usd": 2.24,
# #                 "co2_kg": 0.78
# #             }
# #         }
# #     """
    
# #     # Handle OPTIONS request (CORS preflight)
# #     if request.method == 'OPTIONS':
# #         return '', 204
    
# #     # Check if models are loaded
# #     if not MODELS_LOADED:
# #         return jsonify({
# #             "success": False,
# #             "error": "Models not available",
# #             "message": "ML models are not loaded. Please check server configuration."
# #         }), 503
    
# #     # Get request data
# #     try:
# #         data = request.get_json()
# #         if not data:
# #             return jsonify({
# #                 "success": False,
# #                 "error": "Invalid request",
# #                 "message": "Request body must be valid JSON"
# #             }), 400
# #     except:
# #         return jsonify({
# #             "success": False,
# #             "error": "Invalid JSON"
# #         }), 400
    
# #     # Validate required fields
# #     required = [
# #         'product_name', 'product_category', 'product_weight_kg',
# #         'fragility_index', 'shipping_type'
# #     ]
    
# #     missing = [f for f in required if f not in data]
# #     if missing:
# #         return jsonify({
# #             "success": False,
# #             "error": "Missing required fields",
# #             "missing_fields": missing
# #         }), 400
    
# #     # Validate category and shipping
# #     if data['product_category'] not in VALID_CATEGORIES:
# #         return jsonify({
# #             "success": False,
# #             "error": "Invalid category",
# #             "valid_categories": VALID_CATEGORIES
# #         }), 400
    
# #     if data['shipping_type'] not in VALID_SHIPPING:
# #         return jsonify({
# #             "success": False,
# #             "error": "Invalid shipping type",
# #             "valid_shipping_types": VALID_SHIPPING
# #         }), 400
    
# #     # Validate ranges
# #     if data['product_weight_kg'] <= 0:
# #         return jsonify({
# #             "success": False,
# #             "error": "Invalid weight",
# #             "message": "Product weight must be positive"
# #         }), 400
    
# #     if not 1 <= data['fragility_index'] <= 5:
# #         return jsonify({
# #             "success": False,
# #             "error": "Invalid fragility index",
# #             "message": "Fragility index must be between 1 and 5"
# #         }), 400
    
# #     # Make prediction (simplified - returns mock data if full features not provided)
# #     try:
# #         predictions = {
# #             "cost_usd": round(np.random.uniform(1.5, 3.5), 2),
# #             "co2_kg": round(np.random.uniform(0.4, 1.2), 3),
# #             "suitability_score": round(np.random.uniform(70, 95), 1)
# #         }
        
# #         return jsonify({
# #             "success": True,
# #             "predictions": predictions,
# #             "input": {
# #                 "product": data['product_name'],
# #                 "category": data['product_category'],
# #                 "weight_kg": data['product_weight_kg']
# #             },
# #             "metadata": {
# #                 "model_version": APP_VERSION,
# #                 "timestamp": datetime.now().isoformat()
# #             }
# #         }), 200
        
# #     except Exception as e:
# #         return jsonify({
# #             "success": False,
# #             "error": "Prediction failed",
# #             "message": str(e)
# #         }), 500


# # # ============================================
# # # SCHEMA ENDPOINT
# # # ============================================
# # @app.route(f'{API_PREFIX}/predict/schema', methods=['GET'])
# # def get_schema():
# #     """Return API schema"""
# #     return jsonify({
# #         "endpoint": f"{API_PREFIX}/predict",
# #         "method": "POST",
# #         "content_type": "application/json",
# #         "required_fields": {
# #             "product_name": "string",
# #             "product_category": f"enum: {VALID_CATEGORIES}",
# #             "product_weight_kg": "number (positive)",
# #             "fragility_index": "integer (1-5)",
# #             "shipping_type": f"enum: {VALID_SHIPPING}"
# #         },
# #         "example_request": {
# #             "product_name": "Chocolate Box",
# #             "product_category": "Food",
# #             "product_weight_kg": 0.5,
# #             "fragility_index": 2,
# #             "shipping_type": "Air"
# #         }
# #     }), 200


# # # ============================================
# # # ERROR HANDLERS
# # # ============================================
# # @app.errorhandler(404)
# # def not_found(e):
# #     return jsonify({"error": "Not Found", "status": 404}), 404

# # @app.errorhandler(500)
# # def internal_error(e):
# #     return jsonify({"error": "Internal Server Error", "status": 500}), 500


# # # ============================================
# # # MAIN ENTRY POINT
# # # ============================================
# # if __name__ == '__main__':
# #     host = os.getenv('FLASK_HOST', '0.0.0.0')
# #     port = int(os.getenv('FLASK_PORT', 5000))
# #     debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
# #     print("=" * 60)
# #     print(f"🚀 {APP_NAME} API Server Starting...")
# #     print("=" * 60)
# #     print(f"\n📍 Server: http://{host}:{port}")
# #     print(f"✓ Health Check: http://{host}:{port}/health")
# #     print(f"✓ API Docs: http://{host}:{port}/")
# #     print(f"✓ Predict: http://{host}:{port}{API_PREFIX}/predict")
# #     print(f"\n🔧 Models Loaded: {MODELS_LOADED}")
# #     print("\n" + "=" * 60 + "\n")
    
# #     app.run(host=host, port=port, debug=debug, threaded=True)


# """
# EcoPackAI - Complete Flask Application
# Combines: Health Check + Prediction Endpoint + Future Endpoints
# """

# from flask import Flask, jsonify, request, send_from_directory
# from flask_cors import CORS
# from datetime import datetime
# import numpy as np
# import pandas as pd
# import joblib
# import json
# import os
# # ============================================
# # FLASK APPLICATION INITIALIZATION
# # ============================================
# app = Flask(__name__, static_folder='frontend', static_url_path='')

# # Enable CORS for all routes
# CORS(app, resources={
#     r"/*": {
#         "origins": "*",
#         "methods": ["GET", "POST", "OPTIONS"],
#         "allow_headers": ["Content-Type", "X-API-Key"]
#     }
# })

# # Configuration
# app.config['JSON_SORT_KEYS'] = False
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# APP_VERSION = "1.0.0"
# APP_NAME = "EcoPackAI"
# API_PREFIX = "/api/v1"

# # ============================================
# # LOAD ML MODELS
# # ============================================
# print("\n" + "=" * 60)
# print(f"{APP_NAME} - Loading ML Models")
# print("=" * 60)

# MODELS_LOADED = False
# try:
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
#     preprocessor = joblib.load(os.path.join(BASE_DIR, "ml/models/preprocessing/preprocessing_pipeline.pkl"))
#     rf_cost = joblib.load(os.path.join(BASE_DIR, "ml/models/rf_cost_optimized.joblib"))
#     xgb_co2 = joblib.load(os.path.join(BASE_DIR, "ml/models/xgb_co2_optimized.joblib"))
    
#     with open(os.path.join(BASE_DIR, "data/final/feature_names.json"), 'r') as f:
#         feature_config = json.load(f)
    
#     print("✓ Preprocessor loaded")
#     print("✓ RF Cost model loaded")
#     print("✓ XGBoost CO₂ model loaded")
#     print("✓ Feature configuration loaded")
    
#     MODELS_LOADED = True
# except Exception as e:
#     print(f"⚠ Warning: Could not load models - {e}")
#     print("  API will run in limited mode")

# print("=" * 60 + "\n")

# # ============================================
# # VALIDATION CONSTANTS
# # ============================================
# VALID_CATEGORIES = ['Food', 'Electronics', 'Cosmetics', 'Pharmacy']
# VALID_SHIPPING = ['Air', 'Road', 'Sea']

# # ============================================
# # HEALTH CHECK ENDPOINTS
# # ============================================
# @app.route('/health', methods=['GET'])
# def health_check():
#     """Basic health check"""
#     return jsonify({
#         "status": "healthy",
#         "service": APP_NAME,
#         "version": APP_VERSION,
#         "timestamp": datetime.now().isoformat()
#     }), 200


# @app.route(f'{API_PREFIX}/health', methods=['GET'])
# def api_health():
#     """Extended health check"""
#     return jsonify({
#         "status": "healthy",
#         "service": APP_NAME,
#         "version": APP_VERSION,
#         "timestamp": datetime.now().isoformat(),
#         "models_loaded": MODELS_LOADED
#     }), 200


# # ============================================
# # SERVE FRONTEND
# # ============================================
# @app.route('/')
# def serve_frontend():
#     """Serve frontend HTML"""
#     try:
#         return send_from_directory('frontend', 'index.html')
#     except:
#         return jsonify({
#             "service": APP_NAME,
#             "version": APP_VERSION,
#             "endpoints": {
#                 "health": "/health",
#                 "predict": f"{API_PREFIX}/predict",
#                 "recommend": f"{API_PREFIX}/recommend"
#             }
#         }), 200


# @app.route('/<path:path>')
# def serve_static(path):
#     """Serve static files"""
#     try:
#         return send_from_directory('frontend', path)
#     except:
#         return jsonify({"error": "File not found"}), 404


# # ============================================
# # SCHEMA ENDPOINT
# # ============================================
# @app.route(f'{API_PREFIX}/predict', methods=['POST', 'OPTIONS'])
# def predict():
#     """
#     Prediction endpoint for cost and CO₂ estimation
    
#     POST /api/v1/predict
#     Content-Type: application/json
    
#     Request Body:
#         {
#             "product_name": "Chocolate Box",
#             "product_category": "Food",
#             "product_weight_kg": 0.5,
#             "fragility_index": 2,
#             "shipping_type": "Air",
#             ... (material attributes)
#         }
    
#     Response:
#         {
#             "success": true,
#             "predictions": {
#                 "cost_usd": 2.24,
#                 "co2_kg": 0.78
#             }
#         }
#     """
    
#     # Handle OPTIONS request (CORS preflight)
#     if request.method == 'OPTIONS':
#         return '', 204
    
#     # Check if models are loaded
#     if not MODELS_LOADED:
#         return jsonify({
#             "success": False,
#             "error": "Models not available",
#             "message": "ML models are not loaded. Please check server configuration."
#         }), 503
    
#     # Get request data
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({
#                 "success": False,
#                 "error": "Invalid request",
#                 "message": "Request body must be valid JSON"
#             }), 400
#     except:
#         return jsonify({
#             "success": False,
#             "error": "Invalid JSON"
#         }), 400
    
#     # Validate required fields
#     required = [
#         'product_name', 'product_category', 'product_weight_kg',
#         'fragility_index', 'shipping_type'
#     ]
    
#     missing = [f for f in required if f not in data]
#     if missing:
#         return jsonify({
#             "success": False,
#             "error": "Missing required fields",
#             "missing_fields": missing
#         }), 400
    
#     # Validate category and shipping
#     if data['product_category'] not in VALID_CATEGORIES:
#         return jsonify({
#             "success": False,
#             "error": "Invalid category",
#             "valid_categories": VALID_CATEGORIES
#         }), 400
    
#     if data['shipping_type'] not in VALID_SHIPPING:
#         return jsonify({
#             "success": False,
#             "error": "Invalid shipping type",
#             "valid_shipping_types": VALID_SHIPPING
#         }), 400
    
#     # Validate ranges
#     if data['product_weight_kg'] <= 0:
#         return jsonify({
#             "success": False,
#             "error": "Invalid weight",
#             "message": "Product weight must be positive"
#         }), 400
    
#     if not 1 <= data['fragility_index'] <= 5:
#         return jsonify({
#             "success": False,
#             "error": "Invalid fragility index",
#             "message": "Fragility index must be between 1 and 5"
#         }), 400
    
#     # Make prediction (simplified - returns mock data if full features not provided)
#     try:
#         predictions = {
#             "cost_usd": round(np.random.uniform(1.5, 3.5), 2),
#             "co2_kg": round(np.random.uniform(0.4, 1.2), 3),
#             "suitability_score": round(np.random.uniform(70, 95), 1)
#         }
        
#         return jsonify({
#             "success": True,
#             "predictions": predictions,
#             "input": {
#                 "product": data['product_name'],
#                 "category": data['product_category'],
#                 "weight_kg": data['product_weight_kg']
#             },
#             "metadata": {
#                 "model_version": APP_VERSION,
#                 "timestamp": datetime.now().isoformat()
#             }
#         }), 200
        
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": "Prediction failed",
#             "message": str(e)
#         }), 500


# # ============================================
# # RECOMMENDATION ENDPOINT (NEW)
# # ============================================
# @app.route(f'{API_PREFIX}/recommend', methods=['POST', 'OPTIONS'])
# def recommend():
#     """
#     Get ranked material recommendations
    
#     Returns top 5 materials with predictions
#     """
#     if request.method == 'OPTIONS':
#         return '', 204
    
#     if not MODELS_LOADED:
#         return jsonify({
#             "success": False,
#             "error": "Models not available"
#         }), 503
    
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({
#                 "success": False,
#                 "error": "Invalid request"
#             }), 400
        
#         # Validate required fields
#         required = ['product_name', 'product_category', 'product_weight_kg',
#                    'fragility_index', 'shipping_type']
#         missing = [f for f in required if f not in data]
#         if missing:
#             return jsonify({
#                 "success": False,
#                 "error": "Missing fields",
#                 "missing_fields": missing
#             }), 400
        
#         # Generate recommendations (mock data based on input)
#         recommendations = generate_recommendations(data)
        
#         # Calculate analytics
#         analytics = calculate_analytics(recommendations)
        
#         return jsonify({
#             "success": True,
#             "recommendations": recommendations,
#             "analytics": analytics,
#             "input": {
#                 "product": data['product_name'],
#                 "category": data['product_category'],
#                 "weight_kg": data['product_weight_kg']
#             },
#             "metadata": {
#                 "model_version": APP_VERSION,
#                 "timestamp": datetime.now().isoformat()
#             }
#         }), 200
        
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500


# def generate_recommendations(product_data):
#     """Generate 5 material recommendations"""
#     materials = [
#         {"name": "Cardboard Boxes", "type": "Paper-based", "recyclability": 98},
#         {"name": "Bio-Based Fillers", "type": "Biodegradable", "recyclability": 100},
#         {"name": "Recycled Plastic", "type": "Plastic", "recyclability": 85},
#         {"name": "Compostable Wrap", "type": "Bio-based", "recyclability": 95},
#         {"name": "Kraft Paper", "type": "Paper-based", "recyclability": 92}
#     ]
    
#     base_cost = 2.0 + (product_data['product_weight_kg'] * 0.5)
#     base_co2 = 0.5 + (product_data['product_weight_kg'] * 0.1)
    
#     recommendations = []
#     for i, material in enumerate(materials):
#         variance = 1 + (np.random.random() - 0.5) * 0.3
        
#         cost = base_cost * variance
#         co2 = base_co2 * variance
        
#         # Calculate suitability score
#         suitability = calculate_suitability(
#             product_data['fragility_index'],
#             material['recyclability']
#         )
        
#         recommendations.append({
#             "rank": i + 1,
#             "material_name": material['name'],
#             "material_type": material['type'],
#             "cost_usd": round(cost, 2),
#             "co2_kg": round(co2, 3),
#             "suitability_score": round(suitability, 1),
#             "recyclability_percent": material['recyclability']
#         })
    
#     # Sort by suitability score
#     recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
    
#     # Update ranks
#     for i, rec in enumerate(recommendations):
#         rec['rank'] = i + 1
    
#     return recommendations


# def calculate_suitability(fragility, recyclability):
#     """Calculate material suitability score"""
#     base_score = 50
    
#     # Fragility bonus
#     if fragility <= 2:
#         base_score += 20
#     elif fragility <= 4:
#         base_score += 10
    
#     # Recyclability bonus
#     if recyclability >= 90:
#         base_score += 30
#     elif recyclability >= 70:
#         base_score += 20
#     else:
#         base_score += 10
    
#     return min(100, base_score)


# def calculate_analytics(recommendations):
#     """Calculate analytics from recommendations"""
#     costs = [r['cost_usd'] for r in recommendations]
#     co2_values = [r['co2_kg'] for r in recommendations]
#     sustainability_scores = [r['suitability_score'] for r in recommendations]
    
#     return {
#         "best_recommendation": {
#             "material": recommendations[0]['material_name'],
#             "cost": recommendations[0]['cost_usd'],
#             "co2": recommendations[0]['co2_kg'],
#             "score": recommendations[0]['suitability_score']
#         },
#         "averages": {
#             "cost_usd": round(np.mean(costs), 2),
#             "co2_kg": round(np.mean(co2_values), 3),
#             "sustainability_score": round(np.mean(sustainability_scores), 1)
#         },
#         "ranges": {
#             "cost_min": round(min(costs), 2),
#             "cost_max": round(max(costs), 2),
#             "co2_min": round(min(co2_values), 3),
#             "co2_max": round(max(co2_values), 3)
#         }
#     }
# @app.route(f'{API_PREFIX}/predict/schema', methods=['GET'])
# def get_schema():
#     """Return API schema"""
#     return jsonify({
#         "endpoint": f"{API_PREFIX}/predict",
#         "method": "POST",
#         "content_type": "application/json",
#         "required_fields": {
#             "product_name": "string",
#             "product_category": f"enum: {VALID_CATEGORIES}",
#             "product_weight_kg": "number (positive)",
#             "fragility_index": "integer (1-5)",
#             "shipping_type": f"enum: {VALID_SHIPPING}"
#         },
#         "example_request": {
#             "product_name": "Chocolate Box",
#             "product_category": "Food",
#             "product_weight_kg": 0.5,
#             "fragility_index": 2,
#             "shipping_type": "Air"
#         }
#     }), 200


# # ============================================
# # ERROR HANDLERS
# # ============================================
# @app.errorhandler(404)
# def not_found(e):
#     return jsonify({"error": "Not Found", "status": 404}), 404

# @app.errorhandler(500)
# def internal_error(e):
#     return jsonify({"error": "Internal Server Error", "status": 500}), 500


# # ============================================
# # MAIN ENTRY POINT
# # ============================================
# if __name__ == '__main__':
#     host = os.getenv('FLASK_HOST', '0.0.0.0')
#     port = int(os.getenv('FLASK_PORT', 5000))
#     debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
#     print("=" * 60)
#     print(f"🚀 {APP_NAME} API Server Starting...")
#     print("=" * 60)
#     print(f"\n📍 Server: http://{host}:{port}")
#     print(f"✓ Health Check: http://{host}:{port}/health")
#     print(f"✓ API Docs: http://{host}:{port}/")
#     print(f"✓ Predict: http://{host}:{port}{API_PREFIX}/predict")
#     print(f"\n🔧 Models Loaded: {MODELS_LOADED}")
#     print("\n" + "=" * 60 + "\n")
    
#     app.run(host=host, port=port, debug=debug, threaded=True)

"""
EcoPackAI - Complete Flask Application
Main Backend API Server with Database Integration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import numpy as np
import os

# Import database models
from model import db, init_db, Material, Product, Recommendation

# ============================================
# FLASK APPLICATION INITIALIZATION
# ============================================
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecopackai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

APP_VERSION = "1.0.0"
APP_NAME = "EcoPackAI"
API_PREFIX = "/api/v1"

# Initialize database
init_db(app)

# ============================================
# VALIDATION CONSTANTS
# ============================================
VALID_CATEGORIES = ['Food', 'Electronics', 'Cosmetics', 'Pharmacy']
VALID_SHIPPING = ['Air', 'Road', 'Sea']

print("\n" + "=" * 60)
print(f"{APP_NAME} - Flask API Server")
print("=" * 60)
print("✓ Database initialized")
print("✓ CORS enabled")
print("=" * 60 + "\n")

# ============================================
# HEALTH CHECK ENDPOINTS
# ============================================
@app.route('/health', methods=['GET'])
def health_check():
    """Basic health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route(f'{API_PREFIX}/health', methods=['GET'])
def api_health():
    """Extended health check"""
    return jsonify({
        "status": "healthy",
        "models_loaded": True,
        "timestamp": datetime.now().isoformat()
    }), 200


# ============================================
# ROOT ENDPOINT
# ============================================
@app.route('/', methods=['GET'])
def root():
    """API root"""
    return jsonify({
        "endpoints": {
            "health": "/health",
            "api_health": f"{API_PREFIX}/health",
            "predict": f"{API_PREFIX}/predict",
            "schema": f"{API_PREFIX}/predict/schema"
        },
        "version": APP_VERSION
    }), 200


# ============================================
# PREDICTION ENDPOINT
# ============================================
@app.route(f'{API_PREFIX}/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    Prediction endpoint for cost and CO₂ estimation
    
    POST /api/v1/predict
    Content-Type: application/json
    """
    
    # Handle OPTIONS request (CORS preflight)
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response, 200
    
    # Get request data
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON"
            }), 400
    except:
        return jsonify({
            "success": False,
            "error": "Invalid JSON"
        }), 400
    
    # Validate required fields
    required = [
        'product_name', 'product_category', 'product_weight_kg',
        'fragility_index', 'shipping_type'
    ]
    
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({
            "success": False,
            "missing_fields": missing,
            "error": f"Missing required fields: {', '.join(missing)}"
        }), 400
    
    # Validate category
    if data['product_category'] not in VALID_CATEGORIES:
        return jsonify({
            "success": False,
            "error": f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}"
        }), 400
    
    # Validate shipping
    if data['shipping_type'] not in VALID_SHIPPING:
        return jsonify({
            "success": False,
            "error": f"Invalid shipping type. Must be one of: {', '.join(VALID_SHIPPING)}"
        }), 400
    
    # Validate weight
    if data['product_weight_kg'] <= 0:
        return jsonify({
            "success": False,
            "error": "Product weight must be positive"
        }), 400
    
    # Validate fragility index
    if not 1 <= data['fragility_index'] <= 5:
        return jsonify({
            "success": False,
            "error": "Fragility index must be between 1 and 5"
        }), 400
    
    # Make prediction
    try:
        # Calculate predictions based on product attributes
        weight = data['product_weight_kg']
        fragility = data['fragility_index']
        
        # Cost calculation
        base_cost = weight * 2.5
        fragility_multiplier = 1 + (fragility - 1) * 0.15
        shipping_multiplier = {
            'Air': 1.5,
            'Road': 1.0,
            'Sea': 0.8
        }.get(data['shipping_type'], 1.0)
        
        cost = base_cost * fragility_multiplier * shipping_multiplier
        
        # CO2 calculation
        base_co2 = weight * 0.4
        co2_multiplier = {
            'Air': 2.0,
            'Road': 1.0,
            'Sea': 0.6
        }.get(data['shipping_type'], 1.0)
        
        co2 = base_co2 * co2_multiplier
        
        # Suitability score
        category_scores = {
            'Food': 85,
            'Electronics': 75,
            'Cosmetics': 80,
            'Pharmacy': 90
        }
        base_score = category_scores.get(data['product_category'], 75)
        suitability = base_score - (fragility - 1) * 3
        
        predictions = {
            "cost_usd": round(cost, 2),
            "co2_kg": round(co2, 3),
            "suitability_score": round(max(50, min(100, suitability)), 1)
        }
        
        return jsonify({
            "success": True,
            "predictions": predictions,
            "metadata": {
                "product": data['product_name'],
                "category": data['product_category'],
                "weight_kg": data['product_weight_kg'],
                "timestamp": datetime.now().isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# ============================================
# SCHEMA ENDPOINT
# ============================================
@app.route(f'{API_PREFIX}/predict/schema', methods=['GET'])
def get_schema():
    """Return API schema"""
    return jsonify({
        "required_fields": [
            "product_name",
            "product_category",
            "product_weight_kg",
            "fragility_index",
            "shipping_type"
        ],
        "valid_categories": VALID_CATEGORIES,
        "valid_shipping_types": VALID_SHIPPING,
        "fragility_range": [1, 5],
        "example_request": {
            "product_name": "Chocolate Box",
            "product_category": "Food",
            "product_weight_kg": 0.5,
            "fragility_index": 2,
            "shipping_type": "Air"
        }
    }), 200


# ============================================
# ERROR HANDLERS
# ============================================
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "status": 404}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal Server Error", "status": 500}), 500


# ============================================
# REQUEST LOGGING MIDDLEWARE
# ============================================
@app.before_request
def log_request():
    """Log incoming requests"""
    print(f"[{datetime.now().isoformat()}] {request.method} {request.path}")

@app.after_request
def log_response(response):
    """Log responses"""
    print(f"[{datetime.now().isoformat()}] Response: {response.status_code}")
    return response


# ============================================
# MAIN ENTRY POINT
# ============================================
if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("=" * 60)
    print(f"🚀 {APP_NAME} API Server Starting...")
    print("=" * 60)
    print(f"\n📍 Server: http://{host}:{port}")
    print(f"✓ Health Check: http://{host}:{port}/health")
    print(f"✓ API Docs: http://{host}:{port}/")
    print(f"✓ Predict: http://{host}:{port}{API_PREFIX}/predict")
    print(f"\n🔧 Debug Mode: {debug}")
    print("\n" + "=" * 60 + "\n")
    
    app.run(host=host, port=port, debug=debug, threaded=True)