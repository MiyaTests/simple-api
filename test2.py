import requests

res = requests.post('http://localhost:5000/api/read_file')
if res.ok:
    print(res.json())
res = requests.post('http://localhost:5000/api/create_file')
if res.ok:
    print(res.json())
res = requests.post('http://localhost:5000/api/read_file')
if res.ok:
    print(res.json())

