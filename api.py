import os
import json
import boto3
import time
import base64
import email

from flask import Flask, render_template, request
from s3_demo import upload_file
import bpy


print("IMPORT OK")
print(bpy.app.version_string)

app = Flask(__name__)

BUCKET_NAME = 'foot-scanning-api'
UPLOAD_FOLDER = 'data'
TMP_DIR = '/tmp/'

@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to API</h1>"

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == "POST":
        s3 = boto3.resource('s3')
        
        f = request.files['file']
        file_name = f.filename
        local_obj_file = TMP_DIR + f.filename
        s3.Bucket(BUCKET_NAME).put_object(Key = file_name, Body= request.files['file'])
        s3.Bucket(BUCKET_NAME).download_file(file_name, local_obj_file)
        # print(request.form.get("file_name"))
        # f = request.files['file']
    
        # upload_file(f"{f.filename}", BUCKET_NAME)
        # # print(file_name)
        return 'Done'
        

if __name__ == "__main__":
    app.run(debug=True)
