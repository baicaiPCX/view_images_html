from flask import Flask,render_template,request,send_from_directory,jsonify,redirect,url_for
import os
import urllib.parse
from PIL import Image

import numpy as np
import base64
import cv2

app=Flask(__name__)

app.config["UPLOAD_FOLDER"]=os.getcwd()
download_floder=app.config["UPLOAD_FOLDER"]+"/upload"

class AIData(object):
    def __init__(self):
        self.input=None
        self.output=None
dict_aidata={}

def img2base64(image):
    retval,buffer=cv2.imencode(".jpg",image)
    image_b64=str(base64.b64encode(buffer),encoding="utf-8")
    return image_b64

def allow_file(filename):
    allow_list=["png","PNG","jpg","jpeg"]
    a=filename.split(".")[1]
    if a in allow_list:
        return True
    else:
        return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_result",methods=["POST","GET"])
def get_result():
    print("get_result......")
    print(dict_aidata)
    out_list=[]
    route=request.access_route[0]
    if route in dict_aidata.keys():
        image=dict_aidata[route].input
        print(image.shape)
        out=img2base64(image)
        out_list.append(out)

        dict_aidata.pop(route)
    else:
        print(route,": not exist!")
    return jsonify(out_list)

@app.route("/upload",methods=["POST","GET"])
def upload():
    print("upload...")
    file=request.files['file']
    # if not file:
    #     return render_template("index.html",status="null")
    if allow_file(file.filename):
        route=request.access_route[0]
        image=np.asarray(Image.open(file))
        print(image.shape)
        aidata=AIData()
        aidata.input=image
        dict_aidata[route]=aidata

        # file.save(os.path.join(app.config["UPLOAD_FOLDER"]+"/upload/",file.filename))
        # return render_template("index.html",status="OK")
    # else:
    #     return "NO"

# if __name__ == "__main__":
#     # app.run(debug=True,host="0.0.0.0")
#     app.run(host="0.0.0.0")