import requests
import json

url = "http://127.0.0.1:5000/predict"

data = [
    {
        "product_weight": 1.5,
        "fragility_index": 3,
        "shipping_type": "Air",
        "category": "Electronics",
        "material_type": "Cardboard",
        "strength_mpa": 6,
        "weight_capacity": 5,
        "recyclability_percent": 85,
        "biodegradability_percent": 90
    }
]

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:")
print(response.json())
