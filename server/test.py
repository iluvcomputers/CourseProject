import requests
r = requests.post('http://localhost:5000/search', json={"query": ["discriminative"]})
r.status_code
print("Response: ",r)
print(r.json())
