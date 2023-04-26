import requests
import json

response = requests.get("https://pypi.org/pypi/qiskit-terra/json")
data = response.json()
data_items = data["releases"].items()

for key, value in data_items:
    print(key)