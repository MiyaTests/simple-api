import cv2
import json
import numpy as np
import requests
import sys
from zipfile import ZipFile
import io
import os

cap=cv2.VideoCapture(0)
flag = True
while(True):
    if cv2.waitKey(1) & 0xFF == ord(' '):
        flag = not(flag)
        print(flag)
        # Capture frame-by-frame
    if flag == True:
        ret, frame = cap.read()
        if frame is None:
            break
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        continue
ret,frame=cap.read()
cap.release()
cv2.destroyAllWindows()

#frame = cv2.imread("../temp/ref.jpeg")
#frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
list_frame = frame.tolist()
data = json.dumps(list_frame)
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

mean = [56.27984383108058, 68.00405248461786, 87.22748276458523]
std = [11.042436, 11.551544, 32.036402] #[1.8398114550799392, 1.9249768766144562, 5.338755033895804]
cv2.imshow("reference", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('../temp/real_time.mp4', fourcc, 20.0, (640,480))

while(True):
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame', frame)
    c = cv2.waitKey(1)
    if c & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()


video = cv2.VideoCapture("../temp/real_time.mp4")
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
