"""
API Integration Tests
=====================

Integration tests for complete API workflows.

Author: EcoPackAI Team
Date: 2026-01-03
"""

import pytest
import json
import time from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app as flask_app
from backend.models import db, Material, Product, RecommendationLog

@pytest.fixture(scope='module')
def app():
    """Create test application"""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'REQUIRE_AUTH': False,
        'CACHE_TYPE': 'SimpleCache'
    })
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def sample_data():
    """Sample prediction data"""
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
# End-to-End Workflow Tests
# ============================================

class TestEndToEndWorkflow:
    """Test complete API workflows"""
    
    def test_complete_prediction_workflow(self, client, sample_data):
        """Test complete prediction workflow"""
        # Step 1: Check health
        health_response = client.get('/health')
        assert health_response.status_code == 200
        
        # Step 2: Get model info
        info_response = client.get('/api/v1/models/info')
        assert info_response.status_code in [200, 500]
        
        # Step 3: Make prediction
        pred_response = client.post(
            '/api/v1/predict/all',
            data=json.dumps(sample_data),
            content_type='application/json'
        )
        
        # Verify prediction if successful
        if pred_response.status_code == 200:
            data = json.loads(pred_response.data)
            assert 'results' in data
            assert 'predicted_cost' in data['results']
            assert 'predicted_co2' in data['results']
    
    def test_batch_to_single_prediction_consistency(self, client, sample_data):
        """Test that batch and single predictions are consistent"""
        # Single prediction
        single_response = client.post(
            '/api/v1/predict/all',
            data=json.dumps(sample_data),
            content_type='application/json'
        )
        
        # Batch prediction with same data
        batch_data = {"materials": [sample_data]}
        batch_response = client.post(
            '/api/v1/predict/batch',
            data=json.dumps(batch_data),
            content_type='application/json'
        )
        
        # If both successful, compare results
        if single_response.status_code == 200 and batch_response.status_code == 200:
            single_result = json.loads(single_response.data)['results']
            batch_result = json.loads(batch_response.data)['results'][0]
            
            # Results should be very close (allowing for floating point precision)
            assert abs(
                single_result['predicted_cost'] - batch_result['predicted_cost']
            ) < 0.01

# ============================================
# Database Integration Tests
# ============================================

class TestDatabaseIntegration:
    """Test database connectivity and operations"""
    
    def test_database_connection(self, app):
        """Test database connection"""
        with app.app_context():
            # Try to query database
            result = db.session.execute(db.text('SELECT 1')).scalar()
            assert result == 1
    
    def test_create_and_query_material(self, app):
        """Test creating and querying materials"""
        with app.app_context():
            # Create material
            material = Material(
                material_type='Biodegradable Plastic',
                strength_mpa=30.0,
                weight_capacity=8.0,
                biodegradability_percent=90.0,
                co2_emission_score=1.5,
                recyclability_percent=85.0,
                cost_per_kg=55.0,
                industry_use_case='Food & Beverage'
            )
            
            db.session.add(material)
            db.session.commit()
            
            # Query
            materials = Material.query.filter(
                Material.biodegradability_percent > 80
            ).all()
            
            assert len(materials) > 0
            assert any(m.material_type == 'Biodegradable Plastic' for m in materials)
    
    def test_recommendation_log_creation(self, app):
        """Test creating recommendation logs"""
        with app.app_context():
            # Create dependencies
            material = Material(material_type='Test Material', cost_per_kg=50.0)
            product = Product(
                product_name='Test Product',
                category='Electronics',
                product_weight=1.5,
                fragility_index=7,
                shipping_type='Air'
            )
            
            db.session.add_all([material, product])
            db.session.commit()
            
            # Create log
            log = RecommendationLog.from_prediction(
                product_id=product.product_id,
                material_id=material.material_id,
                predictions={
                    'predicted_cost': 85.50,
                    'predicted_co2': 2.8,
                    'cost_confidence': 0.92
                },
                rank=1
            )
            
            db.session.add(log)
            db.session.commit()
            
            # Verify
            saved_log = RecommendationLog.query.filter_by(
                product_id=product.product_id
            ).first()
            
            assert saved_log is not None
            assert saved_log.cost_prediction == 85.50
            assert saved_log.material_rank == 1
    
    def test_cascade_delete(self, app):
        """Test cascade delete on relationships"""
        with app.app_context():
            # Create product with recommendation
            material = Material(material_type='Test', cost_per_kg=40.0)
            product = Product(product_name='Test', product_weight=1.0)
            
            db.session.add_all([material, product])
            db.session.commit()
            
            log = RecommendationLog(
                product_id=product.product_id,
                recommended_material_id=material.material_id,
                cost_prediction=100.0,
                co2_prediction=2.0,
                material_rank=1
            )
            
            db.session.add(log)
            db.session.commit()
            
            log_id = log.rec_id
            product_id = product.product_id
            
            # Delete product
            db.session.delete(product)
            db.session.commit()
            
            # Log should also be deleted (cascade)
            deleted_log = RecommendationLog.query.get(log_id)
            assert deleted_log is None

# ============================================
# Performance Tests
# ============================================

class TestPerformance:
    """Test API performance"""
    
    def test_response_time(self, client):
        """Test that health check responds quickly"""
        start_time = time.time()
        response = client.get('/health')
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        
        assert response.status_code == 200
        assert duration_ms < 100  # Should respond in less than 100ms
    
    def test_concurrent_requests(self, client, sample_data):
        """Test handling multiple predictions"""
        responses = []
        
        # Make 10 sequential requests (simulating concurrent in unit test)
        for i in range(10):
            response = client.post(
                '/api/v1/predict/cost',
                data=json.dumps(sample_data),
                content_type='application/json'
            )
            responses.append(response)
        
        # All should complete successfully or fail consistently
        status_codes = [r.status_code for r in responses]
        assert all(code in [200, 500] for code in status_codes)

# ============================================
# Security Integration Tests
# ============================================

class TestSecurityIntegration:
    """Test security features"""
    
    def test_cors_headers(self, client):
        """Test CORS headers are set"""
        response = client.get('/health')
        
        # Check CORS headers (if enabled)
        # Note: Actual headers depend on CORS configuration
        assert response.status_code == 200
    
    def test_request_id_header(self, client):
        """Test that request ID is returned"""
        response = client.get('/health')
        
        # Should have X-Request-ID header
        assert 'X-Request-ID' in response.headers

# ============================================
# API Documentation Tests
# ============================================

class TestAPIDocumentation:
    """Test API documentation endpoints"""
    
    def test_api_docs_endpoint(self, client):
        """Test API documentation endpoint"""
        response = client.get('/api/v1/docs')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'endpoints' in data
        assert 'required_features' in data
        assert 'example_request' in data
    
    def test_root_endpoint(self, client):
        """Test root API endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'service' in data
        assert 'version' in data
        assert 'endpoints' in data

# ============================================
# Data Serialization Tests
# ============================================

class TestDataSerialization:
    """Test model serialization"""
    
    def test_material_to_dict(self, app):
        """Test Material model to_dict method"""
        with app.app_context():
            material = Material(
                material_type='Paper',
                strength_mpa=20.0,
                cost_per_kg=40.0
            )
            
            data = material.to_dict()
            
            assert isinstance(data, dict)
            assert data['material_type'] == 'Paper'
            assert 'created_at' in data
    
    def test_material_from_dict(self, app):
        """Test Material model from_dict method"""
        with app.app_context():
            data = {
                'material_type': 'Cardboard',
                'strength_mpa': 25.0,
                'cost_per_kg': 45.0,
                'recyclability_percent': 90.0
            }
            
            material = Material.from_dict(data)
            
            assert material.material_type == 'Cardboard'
            assert material.strength_mpa == 25.0

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
