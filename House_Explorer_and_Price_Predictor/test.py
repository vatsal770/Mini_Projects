import requests

url = "http://127.0.0.1:8000/predict"
data = {
    "city": "Bangalore",
    "bhk": 2,
    "area": 1000.0
}
res = requests.post(url, json=data)
print(res.json())