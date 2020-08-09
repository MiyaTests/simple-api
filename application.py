from flask import Flask
from flask import request, jsonify
import numpy as np
from numpy import linalg as la
from random import randint
import json

# Elastic Beanstalk looks for an 'application' that is callable by default
app = Flask(__name__)

# Health Check 
@app.route('/healthcheck')
def hello_world():
    return 'Your Server is working!'

# REST API
@app.route('/api/get_ref', methods=['GET', 'POST'])
def get_ref():
    content = request.json
    img = json.loads(content)
    L = 100
    img = np.array(img)
    d1, d2, d3 = img.shape
    img = img.reshape((d1*d2, d3))
    for pixel in img:
        pixel[0] = int(L*pixel[0]/la.norm(pixel))
        pixel[1] = int(L*pixel[1]/la.norm(pixel))
        pixel[2] = int(L*pixel[2]/la.norm(pixel))
    mean = np.mean(img, axis=0)
    std = np.std(img, axis=0)
    hashtable = {"mean": mean.tolist(), "std": std.tolist()}
    content = json.dumps(hashtable)
    return content

@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    frame = json.loads(content)
    n = len(frame)
    hashtable = {"size": n, "data": frame}
    content = json.dumps(hashtable)
    return content

@app.route('/api/create_file', methods=['GET', 'POST'])
def create_file():
    f = open("hello.txt", "w")
    f.write("helloooo")
    content = json.dumps("criou arquivo")
    return content

@app.route('/api/read_file', methods=['GET', 'POST'])
def read_file():
    try:
        f = open("hello.txt", "r")
        content = json.dumps(f.read())
    except:
        content = json.dumps("erro ao ler o arquivo")
    return content

# Run the application
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application.
    app.debug = True
    app.run(host="0.0.0.0")
