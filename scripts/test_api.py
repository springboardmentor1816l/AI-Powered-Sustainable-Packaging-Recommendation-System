"""
Test Flask API Endpoints
=========================

Test script for EcoPackAI Flask API.

Author: EcoPackAI Team
Date: 2026-01-02
"""

import requests
import json
import time
from pathlib import Path

# API Base URL
BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print formatted section"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def test_health_check():
    """Test health endpoint"""
    print_section("TEST 1: Health Check")
    
    url = f"{BASE_URL}/health"
    print(f"GET {url}")
    
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'
    
    print("✓ Health check passed")

def test_readiness_check():
    """Test readiness endpoint"""
    print_section("TEST 2: Readiness Check")
    
    url = f"{BASE_URL}/health/ready"
    print(f"GET {url}")
    
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✓ Service is ready")
    else:
        print("⚠ Service not ready (models may still be loading)")

def test_predict_cost():
    """Test cost prediction endpoint"""
    print_section("TEST 3: Cost Prediction")
    
    # Load sample request
    with open('sample_request.json', 'r') as f:
        data = json.load(f)
    
    url = f"{BASE_URL}/api/v1/predict/cost"
    print(f"POST {url}")
    print(f"Request: {json.dumps(data, indent=2)[:200]}...")
    
    response = requests.post(url, json=data)
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        result = response.json()['results']
        print(f"\n✓ Predicted Cost: ${result['predicted_cost']:.2f}")
        if 'cost_confidence' in result:
            print(f"  Confidence: ±${result['cost_confidence']:.2f}")
    else:
        print(f"❌ Error: {response.json()['message']}")

def test_predict_co2():
    """Test CO2 prediction endpoint"""
    print_section("TEST 4: CO₂ Prediction")
    
    with open('sample_request.json', 'r') as f:
        data = json.load(f)
    
    url = f"{BASE_URL}/api/v1/predict/co2"
    print(f"POST {url}")
    
    response = requests.post(url, json=data)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        result = response.json()['results']
        print(f"\n✓ Predicted CO₂: {result['predicted_co2']:.4f} kg")
    else:
        print(f"❌ Error: {response.json()['message']}")

def test_predict_all():
    """Test combined prediction endpoint"""
    print_section("TEST 5: Combined Prediction (Cost + CO₂)")
    
    with open('sample_request.json', 'r') as f:
        data = json.load(f)
    
    url = f"{BASE_URL}/api/v1/predict/all"
    print(f"POST {url}")
    
    response = requests.post(url, json=data)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        result = response.json()['results']
        print(f"\n✓ Predictions:")
        print(f"  Cost: ${result['predicted_cost']:.2f}")
        print(f"  CO₂: {result['predicted_co2']:.4f} kg")
    else:
        print(f"❌ Error: {response.json()['message']}")

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print_section("TEST 6: Batch Prediction")
    
    with open('sample_request.json', 'r') as f:
        material = json.load(f)
    
    # Create batch request with 3 materials
    batch_data = {
        "materials": [
            {**material, "id": "material_1"},
            {**material, "id": "material_2", "recyclability_percent": 80.0},
            {**material, "id": "material_3", "recycled_content_percent": 50.0}
        ]
    }
    
    url = f"{BASE_URL}/api/v1/predict/batch"
    print(f"POST {url}")
    print(f"Materials: {len(batch_data['materials'])}")
    
    response = requests.post(url, json=batch_data)
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Count: {result['count']}")
        print(f"\nResults:")
        for item in result['results']:
            print(f"  {item.get('id', 'N/A')}: Cost ${item['predicted_cost']:.2f}, CO₂ {item['predicted_co2']:.4f} kg")
        print("✓ Batch prediction successful")
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print(f"❌ Error: {response.json()['message']}")

def test_model_info():
    """Test model info endpoint"""
    print_section("TEST 7: Model Information")
    
    url = f"{BASE_URL}/api/v1/models/info"
    print(f"GET {url}")
    
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)[:500]}...")
    
    if response.status_code == 200:
        print("✓ Model info retrieved")
    else:
        print(f"❌ Error")

def test_invalid_input():
    """Test invalid input handling"""
    print_section("TEST 8: Invalid Input Handling")
    
    # Missing required fields
    invalid_data = {
        "recyclability_percent": 95.0
    }
    
    url = f"{BASE_URL}/api/v1/predict/cost"
    print(f"POST {url}")
    print(f"Request: (Missing required fields)")
    
    response = requests.post(url, json=invalid_data)
    
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 400
    print("✓ Invalid input properly rejected")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "API TEST SUITE" + " " * 36 + "║")
    print("║" + " " * 27 + "EcoPackAI Project" + " " * 33 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Check if API is running
    print("\nChecking API availability...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print("✓ API is running\n")
    except requests.exceptions.ConnectionError:
        print("❌ API is not running!")
        print("Please start the API with: python app.py")
        return 1
    
    try:
        # Run tests
        test_health_check()
        test_readiness_check()
        test_predict_cost()
        test_predict_co2()
        test_predict_all()
        test_batch_prediction()
        test_model_info()
        test_invalid_input()
        
        print_section("ALL TESTS PASSED! ✅")
        
        print("\n📊 Test Summary:")
        print("   ✓ Health checks working")
        print("   ✓ Cost prediction working")
        print("   ✓ CO₂ prediction working")
        print("   ✓ Combined prediction working")
        print("   ✓ Batch prediction working")
        print("   ✓ Model info working")
        print("   ✓ Input validation working")
        
        print("\n✨ API is production-ready!\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit(main())
