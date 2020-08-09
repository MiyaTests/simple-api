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
try:
    res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/get_ref', json = data)
except:
    res = requests.post('http://localhost:5000/api/get_ref', json = data)
if res.ok:
    print("res ok")
    res = res.json()
    mean = res["mean"]
    std = res["std"]
else:
    sys.exit(res)

video = cv2.VideoCapture("../temp/pao.mp4")
ok = True
while ok:
    ok, frame = video.read()
    frame = cv2.resize(frame, None, fx=0.2, fy=0.2)
    frame = frame.tolist()
    hashtable = {"img": frame, "mean": mean, "std": std}
    data = json.dumps(hashtable)
    print(sys.getsizeof(data))
    try:
        res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/segmentation', json = data)
    except:
        res = requests.post('http://localhost:5000/api/segmentation', json = data)
    if res.ok:
        res = res.json()
        print(res)
    else:
        print(res)

