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

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == "POST":
        s3 = boto3.resource('s3')
        # print(request.form.get("file_name"))
        f = request.files['file']
    
        file_name = upload_file(f"{f.filename}", BUCKET_NAME)
        print(file_name)
        return 'Done'
        

if __name__ == "__main__":
    app.run(debug=True)
