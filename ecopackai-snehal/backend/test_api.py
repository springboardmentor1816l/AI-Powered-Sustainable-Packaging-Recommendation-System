# """

import pytest
import json
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import Flask app and models - FIXED IMPORT
from app import app
from model import db, Material, Product, Recommendation


# ============================================
# TEST CONFIGURATION
# ============================================

@pytest.fixture
def client():
    """Create test client with in-memory database"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "product_name": "Test Product",
        "product_category": "Food",
        "product_weight_kg": 0.5,
        "fragility_index": 2,
        "shipping_type": "Air"
    }


# ============================================
# HEALTH CHECK TESTS
# ============================================

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_api_health_check(client):
    """Test API health check endpoint"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'models_loaded' in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'endpoints' in data
    assert 'version' in data


# ============================================
# PREDICTION ENDPOINT TESTS
# ============================================

def test_predict_valid_input(client, sample_product_data):
    """Test prediction with valid input"""
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(sample_product_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] == True
    assert 'predictions' in data
    assert 'cost_usd' in data['predictions']
    assert 'co2_kg' in data['predictions']


def test_predict_missing_fields(client):
    """Test prediction with missing required fields"""
    incomplete_data = {
        "product_name": "Test"
    }
    
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(incomplete_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] == False
    assert 'missing_fields' in data


def test_predict_invalid_category(client, sample_product_data):
    """Test prediction with invalid category"""
    sample_product_data['product_category'] = 'InvalidCategory'
    
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(sample_product_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'Invalid category' in data['error']


def test_predict_invalid_weight(client, sample_product_data):
    """Test prediction with invalid weight"""
    sample_product_data['product_weight_kg'] = -5
    
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(sample_product_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_predict_invalid_fragility(client, sample_product_data):
    """Test prediction with invalid fragility index"""
    sample_product_data['fragility_index'] = 10
    
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(sample_product_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_predict_invalid_json(client):
    """Test prediction with invalid JSON"""
    response = client.post(
        '/api/v1/predict',
        data='{"invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_predict_empty_body(client):
    """Test prediction with empty request body"""
    response = client.post(
        '/api/v1/predict',
        data='',
        content_type='application/json'
    )
    
    assert response.status_code == 400


# ============================================
# SCHEMA ENDPOINT TESTS
# ============================================

def test_get_schema(client):
    """Test schema endpoint"""
    response = client.get('/api/v1/predict/schema')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'required_fields' in data
    assert 'example_request' in data


# ============================================
# ERROR HANDLING TESTS
# ============================================

def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    if response.content_type == 'application/json':
        data = json.loads(response.data)
        assert 'error' in data


# ============================================
# DATABASE TESTS
# ============================================

def test_create_material(client):
    """Test creating material in database"""
    with app.app_context():
        material = Material(
            material_type="Test Material",
            packaging_type="Test Package",
            cost_per_unit_usd=1.5,
            recyclability_percent=80
        )
        db.session.add(material)
        db.session.commit()
        
        assert material.material_id is not None
        
        retrieved = Material.query.filter_by(material_type="Test Material").first()
        assert retrieved is not None
        assert retrieved.cost_per_unit_usd == 1.5


def test_create_product(client):
    """Test creating product in database"""
    with app.app_context():
        product = Product(
            product_name="Test Product",
            category="Food",
            product_weight=0.5,
            fragility_index=2
        )
        db.session.add(product)
        db.session.commit()
        
        assert product.product_id is not None


# ============================================
# INTEGRATION TESTS
# ============================================

def test_full_prediction_workflow(client, sample_product_data):
    """Test complete prediction workflow"""
    # Step 1: Check health
    health_response = client.get('/health')
    assert health_response.status_code == 200
    
    # Step 2: Get schema
    schema_response = client.get('/api/v1/predict/schema')
    assert schema_response.status_code == 200
    
    # Step 3: Make prediction
    predict_response = client.post(
        '/api/v1/predict',
        data=json.dumps(sample_product_data),
        content_type='application/json'
    )
    assert predict_response.status_code == 200
    
    data = json.loads(predict_response.data)
    assert 'predictions' in data
    assert 'metadata' in data


# ============================================
# PERFORMANCE TESTS
# ============================================

def test_response_time(client, sample_product_data):
    """Test API response time"""
    import time
    
    start = time.time()
    response = client.post(
        '/api/v1/predict',
        data=json.dumps(sample_product_data),
        content_type='application/json'
    )
    end = time.time()
    
    response_time = end - start
    
    assert response_time < 2.0
    assert response.status_code == 200


# ============================================
# RUN TESTS
# ============================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])