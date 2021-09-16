from flask import Flask, redirect, url_for, request, render_template, make_response
import json
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import pickle


app = Flask(__name__)
model = None
with open('knnModel.pickle', 'rb') as file:
    model = pickle.load(file)

@app.route('/knn', methods = ['GET','POST'])
def get_request():
    global model
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request_json and 'data' in request_json:
        data = np.array([request_json['data']])
        temp = model.predict(data)[0]
        return f'{temp}'
        
    else:
        return f'You need enter data'

def predict(data):
    global model
    if model == None:
        with open('knnModel.pickle', 'rb') as file:
            model = pickle.load(file)
    ret = model.predict(data)
    return ret[0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)