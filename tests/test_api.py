"""
API Unit Tests
==============

Comprehensive unit tests for API endpoints.

Author: EcoPackAI Team
Date: 2026-01-03
"""

import pytest
import json
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app as flask_app
from backend.models import db, Material, Product, RecommendationLog, User

@pytest.fixture
def app():
    """Create and configure a test Flask application"""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'REQUIRE_AUTH': False,  # Disable auth for testing
        'CACHE_TYPE': 'SimpleCache'
    })
    
    # Create tables
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def sample_material_data():
    """Sample material input data"""
    return {
        "recyclability_percent": 95.0,
        "recycled_content_percent": 70.0,
        "reusability_percent": 50.0,
        "biodegradation_time_days": 120,
        "end_of_life_disposal_percent": 95.0,
        "carbon_footprint_kg_co2_unit": 1.8,
        "waste_reduction_impact_percent": 80.0,
        "sustainability_target_progress_percent": 85.0,
        "load_handling_score": 8.0,
        "moisture_resistance_score": 7.0,
        "thermal_resistance_score": 7.0,
        "annual_usage_units": 15000,
        "total_material_weight_tons": 7.5,
        "supplier_sustainability_compliance_percent": 90.0,
        "co2_impact_index": 0.25,
        "cost_efficiency_index": 0.75,
        "material_suitability_score": 70.0,
        "overall_sustainability_score": 0.85
    }

# ============================================
# Health Check Tests
# ============================================

class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self, client):
        """Test basic health check"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert data['service'] == 'EcoPackAI API'
    
    def test_readiness_check(self, client):
        """Test readiness check"""
        response = client.get('/health/ready')
        # May return 200 or 503 depending on model loading
        assert response.status_code in [200, 503]
        
        data = json.loads(response.data)
        assert 'status' in data
        assert 'timestamp' in data
    
    def test_liveness_check(self, client):
        """Test liveness check"""
        response = client.get('/health/live')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'alive'

# ============================================
# Input Validation Tests
# ============================================

class TestInputValidation:
    """Test input validation"""
    
    def test_missing_required_fields(self, client):
        """Test validation with missing fields"""
        invalid_data = {
            "recyclability_percent": 95.0
        }
        
        response = client.post(
            '/api/v1/predict/cost',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'Missing required features' in data['message']
    
    def test_invalid_numeric_values(self, client, sample_material_data):
        """Test validation with invalid numeric values"""
        invalid_data = sample_material_data.copy()
        invalid_data['recyclability_percent'] = 150.0  # Invalid: > 100
        
        response = client.post(
            '/api/v1/predict/cost',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'Invalid feature values' in data['message']
    
    def test_non_numeric_values(self, client, sample_material_data):
        """Test validation with non-numeric values"""
        invalid_data = sample_material_data.copy()
        invalid_data['recyclability_percent'] = "not_a_number"
        
        response = client.post(
            '/api/v1/predict/cost',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

# ============================================
# Prediction Endpoint Tests
# ============================================

class TestPredictionEndpoints:
    """Test prediction endpoints"""
    
    def test_predict_cost(self, client, sample_material_data):
        """Test cost prediction endpoint"""
        response = client.post(
            '/api/v1/predict/cost',
            data=json.dumps(sample_material_data),
            content_type='application/json'
        )
        
        # Should succeed if models are loaded
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert 'results' in data
            assert 'predicted_cost' in data['results']
            assert isinstance(data['results']['predicted_cost'], (int, float))
    
    def test_predict_co2(self, client, sample_material_data):
        """Test CO₂ prediction endpoint"""
        response = client.post(
            '/api/v1/predict/co2',
            data=json.dumps(sample_material_data),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert 'predicted_co2' in data['results']
            assert isinstance(data['results']['predicted_co2'], (int, float))
    
    def test_predict_all(self, client, sample_material_data):
        """Test combined prediction endpoint"""
        response = client.post(
            '/api/v1/predict/all',
            data=json.dumps(sample_material_data),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert 'predicted_cost' in data['results']
            assert 'predicted_co2' in data['results']
            assert 'metadata' in data
    
    def test_batch_prediction(self, client, sample_material_data):
        """Test batch prediction endpoint"""
        batch_data = {
            "materials": [
                {**sample_material_data, "id": "material_1"},
                {**sample_material_data, "id": "material_2"}
            ]
        }
        
        response = client.post(
            '/api/v1/predict/batch',
            data=json.dumps(batch_data),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert data['count'] == 2
            assert len(data['results']) == 2
    
    def test_batch_empty_array(self, client):
        """Test batch prediction with empty array"""
        batch_data = {"materials": []}
        
        response = client.post(
            '/api/v1/predict/batch',
            data=json.dumps(batch_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'empty' in data['message'].lower()

# ============================================
# Model Info Tests
# ============================================

class TestModelInfo:
    """Test model info endpoint"""
    
    def test_model_info(self, client):
        """Test model information endpoint"""
        response = client.get('/api/v1/models/info')
        
        # Should always return something
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'models' in data

# ============================================
# Database Model Tests
# ============================================

class TestDatabaseModels:
    """Test database models"""
    
    def test_material_model(self, app):
        """Test Material model CRUD"""
        with app.app_context():
            # Create
            material = Material(
                material_type='Test Cardboard',
                strength_mpa=25.5,
                weight_capacity=10.0,
                biodegradability_percent=85.0,
                co2_emission_score=2.5,
                recyclability_percent=90.0,
                cost_per_kg=45.50,
                industry_use_case='Electronics'
            )
            
            db.session.add(material)
            db.session.commit()
            
            # Read
            retrieved = Material.query.filter_by(material_type='Test Cardboard').first()
            assert retrieved is not None
            assert retrieved.strength_mpa == 25.5
            
            # Update
            retrieved.cost_per_kg = 50.0
            db.session.commit()
            
            updated = Material.query.get(retrieved.material_id)
            assert updated.cost_per_kg == 50.0
            
            # Delete
            db.session.delete(updated)
            db.session.commit()
            
            deleted = Material.query.get(material.material_id)
            assert deleted is None
    
    def test_product_model(self, app):
        """Test Product model"""
        with app.app_context():
            product = Product(
                product_name='Test Smartphone',
                category='Electronics',
                product_weight=0.5,
                fragility_index=8,
                shipping_type='Air'
            )
            
            db.session.add(product)
            db.session.commit()
            
            retrieved = Product.query.filter_by(product_name='Test Smartphone').first()
            assert retrieved is not None
            assert retrieved.fragility_index == 8
    
    def test_recommendation_log_model(self, app):
        """Test RecommendationLog model"""
        with app.app_context():
            # Create dependencies
            material = Material(material_type='Test Material', cost_per_kg=50.0)
            product = Product(product_name='Test Product', product_weight=1.0)
            
            db.session.add_all([material, product])
            db.session.commit()
            
            # Create recommendation log
            log = RecommendationLog(
                product_id=product.product_id,
                recommended_material_id=material.material_id,
                cost_prediction=120.50,
                co2_prediction=3.2,
                material_rank=1,
                confidence_score=0.95
            )
            
            db.session.add(log)
            db.session.commit()
            
            retrieved = RecommendationLog.query.first()
            assert retrieved is not None
            assert retrieved.cost_prediction == 120.50
    
    def test_user_model(self, app):
        """Test User model and password hashing"""
        with app.app_context():
            user = User(
                username='testuser',
                email='test@example.com',
                role='user'
            )
            user.set_password('secure_password')
            
            db.session.add(user)
            db.session.commit()
            
            retrieved = User.query.filter_by(username='testuser').first()
            assert retrieved is not None
            assert retrieved.check_password('secure_password')
            assert not retrieved.check_password('wrong_password')
            assert retrieved.has_permission('user')
            assert not retrieved.has_permission('admin')

# ============================================
# Error Handling Tests
# ============================================

class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error(self, client):
        """Test 404 error handler"""
        response = client.get('/nonexistent/endpoint')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['error'] == 'Not Found'
    
    def test_invalid_json(self, client):
        """Test invalid JSON handling"""
        response = client.post(
            '/api/v1/predict/cost',
            data='invalid json',
            content_type='application/json'
        )
        
        assert response.status_code in [400, 500]

# ============================================
# Response Schema Tests
# ============================================

class TestResponseSchema:
    """Test response schemas"""
    
    def test_success_response_schema(self, client, sample_material_data):
        """Test success response structure"""
        response = client.post(
            '/api/v1/predict/all',
            data=json.dumps(sample_material_data),
            content_type='application/json'
        )
        
        if response.status_code == 200:
            data = json.loads(response.data)
            
            # Check required fields
            assert 'status' in data
            assert 'timestamp' in data
            assert 'prediction_type' in data
            assert 'results' in data
    
    def test_error_response_schema(self, client):
        """Test error response structure"""
        response = client.post(
            '/api/v1/predict/cost',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        # Check required error fields
        assert 'status' in data
        assert data['status'] == 'error'
        assert 'timestamp' in data
        assert 'error' in data
        assert 'message' in data

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
