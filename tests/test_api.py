import unittest
import json
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from backend.db import db

class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_predict_unauthorized(self):
        response = self.app.post('/predict', json={})
        self.assertEqual(response.status_code, 401)

    def test_predict_valid(self):
        headers = {'X-API-Key': 'default-dev-key'}
        data = {
            "product_weight_g": 150.0,
            "product_category": "electronics",
            "fragility_score": 0.8,
            "material_type": "cardboard",
            "material_recyclability_score": 0.9,
            "transport_distance_km": 500.0
        }
        response = self.app.post('/predict', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('predicted_cost', response.json)
        self.assertIn('predicted_co2_impact', response.json)

    def test_predict_invalid_input(self):
        headers = {'X-API-Key': 'default-dev-key'}
        data = {
            "product_weight_g": 150.0
            # Missing other fields
        }
        response = self.app.post('/predict', json=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()
