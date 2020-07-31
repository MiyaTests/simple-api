from flask import Flask
from flask import request, jsonify
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

# Elastic Beanstalk looks for an 'application' that is callable by default
app = Flask(__name__)

# Health Check 
@app.route('/healthcheck')
def hello_world():
    return 'Your Server is working!'

# REST API
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

@app.route('/api/show_image', methods=['GET', 'POST'])
def show_image():
    img = mpimg.imread("image.jpg")
    plt.imshow(img)
    plt.show()
    return json.dumps("your image")

# Run the application
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application.
    app.debug = True
    app.run(host="0.0.0.0")
