import cv2
import json
import numpy as np
import requests
import sys

frame = cv2.imread("../temp/ref.jpeg")
frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
frame = frame.tolist()
data = json.dumps(frame)
print(sys.getsizeof(data))
#res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/get_ref', json = data)
res = requests.post('http://localhost:5000/api/get_ref', json = data)
if res.ok:
    print("res ok")
    res = res.json()
    print(res["mean"])
    print(res["std"])
else:
    print(res)

