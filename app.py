from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

MODEL_PATH = 'models/mobilenetv2_exp2_10.h5'
model = load_model(MODEL_PATH)
# from tensorflow.keras.applications import MobileNetV2
print('Model loaded. Check http://127.0.0.1:5000/')

def decode_predictions(threshed, pred):
    """
    Converts float pred to the output string.
    """
    if int(threshed) == 0:
        return f"Malignant; Confidence: {round((1-float(pred))*100, 1)}%"
    elif int(threshed) == 1:
        return f"Non-Malignant; Confidence: {round(float(pred)*100)}%"

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(400, 400))
                         # color_mode="rgba")
    x = image.img_to_array(img)
    x = preprocess_input(x)[None]
    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        # thresholding
        threshed = (preds > 0.5)*1
        # Process your result for human
        pred_class = decode_predictions(threshed, preds)
        # print(preds.shape, pred_class)
        return pred_class
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
