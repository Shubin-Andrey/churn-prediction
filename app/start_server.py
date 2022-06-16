# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages

import dill
import os
dill._dill._reverse_typemap['ClassType'] = type
from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import itertools
from time import strftime

# initialize our Flask application and the model
app = Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
    # load the pre-trained model
    global model
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    print(model)

modelpath = 'XGB_pipeline.dill'
load_model(modelpath)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""


@app.route('/predict', methods=['POST'])
def predict():
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    if request.method == "POST":
        # ensure an image was properly uploaded to our endpoint
        feature_dict = {'Geography': '', 'Gender': '', 'Tenure': '', 'HasCrCard': '', 'IsActiveMember': '',
                        'CreditScore': '', 'Age': '', 'Balance': '', 'NumOfProducts': '', 'EstimatedSalary': ''}
        request_json = request.get_json()

        for keys_ in feature_dict:
            feature_dict[keys_] = request_json[keys_]

        df = pd.DataFrame.from_dict(feature_dict)
        try:
            preds = model.predict_proba(df)
            print(preds)
            data["predictions"] = f'{preds[:, 1][0]}'
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return jsonify(data)

        # indicate that the request was a success
        data["success"] = True
        print('OK')
        print(data)
        # return the data dictionary as a JSON response
    return jsonify(data)


if __name__ == '__main__':
    app.run()

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)