import cv2
import json
import numpy as np
import requests
import sys

cap=cv2.VideoCapture(0)
ret,frame=cap.read()
frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
frame = frame.tolist()
data = json.dumps(frame)
print(sys.getsizeof(data))
res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/add_message/122', json = data)
#res = requests.post('http://localhost:5000/api/add_message/122', json = data)
if res.ok:
    print("res ok")
    res = res.json()
    print(res["size"])
    data = res["data"]
    cv2.imshow("Image", cv2.UMat(np.array(data, dtype=np.uint8)))
    key = cv2.waitKey(0)

    cv2.destroyAllWindows()
else:
    print(res)

