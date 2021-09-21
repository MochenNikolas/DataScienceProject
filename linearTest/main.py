import json
import pandas as pd
import numpy as np
from google.cloud import storage
from sklearn.linear_model import LinearRegression
import pickle

model = None

def get_request(request):
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
        temp = predict(data)
        return f'{temp}'
    else:
        return f'You need enter data'

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def predict(data):
    global model
    # Model load which only happens during cold starts
    download_blob('data-science-project-models', 'linearModel.pickle', '/tmp/linearModel.pickle')
    if model == None:
        with open('/tmp/linearModel.pickle', 'rb') as file:
            model = pickle.load(file)

    ret = model.predict(data)
    return ret[0]

