import cv2
import json
import numpy as np
import requests
import sys

mean = [56.27984383108058, 68.00405248461786, 87.22748276458523]
std = [1.8398114550799392, 1.9249768766144562, 5.338755033895804]
frame = cv2.imread("../temp/pao_41.jpg")
frame = cv2.resize(frame, None, fx=0.2, fy=0.2)
frame = frame.tolist()
hashtable = {"img": frame, "mean": mean, "std": std}
data = json.dumps(hashtable)
print(sys.getsizeof(data))
res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/segmentation', json = data)
#res = requests.post('http://localhost:5000/api/segmentation', json = data)
if res.ok:
    print("res ok")
    res = res.json()
    print(res)
else:
    print(res)

