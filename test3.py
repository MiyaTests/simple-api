import requests

res = requests.post('http://localhost:5000/api/show_image')
if res.ok:
    print(res.json())

