import cv2
import json
import numpy as np
import requests
import sys
from zipfile import ZipFile
import io
import os

frame = cv2.imread("../temp/ref3.jpeg")
#frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
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

print("mean")
print(mean)
print("std")
print(std)
#mean = [56.27984383108058, 68.00405248461786, 87.22748276458523]
#std = [11.042436, 11.551544, 32.036402] #[1.8398114550799392, 1.9249768766144562, 5.338755033895804]

video = cv2.VideoCapture("../temp/pao.mp4")
ok = True
count = 0
max_frame = 10
class_number = 0
class_name = "pao"
path = "../temp/"
#zipObj = ZipFile(path+'sample.zip', 'w')
with ZipFile(path+'sample.zip', mode="w") as zf:
    f = open("classes.txt", 'w')
    f.write("pao frances")
    f.close()
    zf.write("classes.txt")
    os.remove("classes.txt")
    while ok or count > max_frame:
        ok, frame = video.read()
        #frame = cv2.resize(frame, None, fx=0.2, fy=0.2)
        img = frame.tolist()
        hashtable = {"img": img, "mean": mean, "std": std}
        data = json.dumps(hashtable)
        print(sys.getsizeof(data))
        try:
            res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/segmentation', json = data)
        except:
            res = requests.post('http://localhost:5000/api/segmentation', json = data)
        if res.ok:
            res = res.json()
            print(res)
            cv2.imwrite("%s%d.jpg" %(path+class_name, count), frame)     
            #buf = io.BytesIO()
            #cv2.imwrite(buf, frame)
            #zf.writestr("%s%d.jpg" %(path+class_name, count), buf.getvalue())

            #buf = io.BytesIO()
            box = (class_number, res['x'], res['y'], res['w'], res['h'])
            f = open("%s%d.txt" %(path+class_name, count), 'w')
            #f = open(buf, 'w')
            f.write("%d %f %f %f %f" %box)
            f.close()
            #zf.writestr("%s%d.txt" %(path+class_name, count), buf.getvalue())
            zf.write("%s%d.jpg" %(path+class_name, count))
            zf.write("%s%d.txt" %(path+class_name, count))
            os.remove("%s%d.jpg" %(path+class_name, count))
            os.remove("%s%d.txt" %(path+class_name, count))
            count += 1
        else:
            print(res)
