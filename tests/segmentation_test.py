import cv2
import json
import numpy as np
import requests
import sys

mean = [56.27984383108058, 68.00405248461786, 87.22748276458523]
#std = [1.8398114550799392, 1.9249768766144562, 5.338755033895804]
std = [11.042436, 11.551544, 32.036402]

img = cv2.imread("../temp/pao.jpg")
#frame = cv2.resize(frame, None, fx=0.2, fy=0.2)
frame = img.tolist()
hashtable = {"img": frame, "mean": mean, "std": std}
data = json.dumps(hashtable)
print(sys.getsizeof(data))
try:
    res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/segmentation', json = data)
except:
    res = requests.post('http://localhost:5000/api/segmentation', json = data)
if res.ok:
    print("res ok")
    res = res.json()
    print(res)
    x = res["x"]
    y = res["y"]
    w = res["w"]
    h = res["h"]
    img_dim = [len(img[0]), len(img)]
    print(img_dim)
    start_pt = (int((x - w/2)*img_dim[0]), int((y - h/2)*img_dim[1]))
    end_pt = (int((x + w/2)*img_dim[0]), int((y + h/2)*img_dim[1]))
    print(start_pt)
    print(end_pt)
    color = [0, 0, 0]
    cv2.rectangle(img, start_pt, end_pt, color, 2)
    cv2.imshow("pao", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(res)

