import requests

url = "http://127.0.0.1:5000/predict"
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "demo-key"
}


payload = {
    "recyclability": 0.8,
    "co2_factor": 1.2,
    "weight": 0.05
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.text)
