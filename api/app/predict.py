from flask import Flask,request
from flask_restful import Resource
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os, sys
sys.path.insert(1, os.path.abspath('.'))
from config import *
from class_lib.data_processing import *


ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """
        Check if uploaded files are compatible
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class SaySomething(Resource):
    def get(self):
        return {"Welcome": "Welcome to my StackOverflow Modelling"}


class PredictUsingKmeans(Resource):
    def get(self):
        data = get_top_10_prediction()
        return {'status_code':  API_Status.OKAY,
                            'status_message':API_Status_Message.LIST, 
                            'data': data.to_json()}, 200
    def post(self):
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                
                return {'status_code':  API_Status.BAD_PAYLOAD,
                        'status_message':API_Status_Message.MISSING,
                        'data': None}, 406 
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                #dat = pd.read_csv(fil)
                data = file.read()
                input = clean_files(data)
                if isinstance(input, np.ndarray):
                    return {'status_code':  API_Status.OKAY,
                            'status_message':API_Status_Message.PREDICT, 
                            'data': str(input)}, 200
                else:
                    return {'status_code':  API_Status.BAD_PAYLOAD,
                    'status_message':input, 
                    'data': None},400
            else:

                filename = secure_filename(file.filename)
                return {'status_code':  API_Status.BAD_PAYLOAD,
                    'status_message':API_Status_Message.WRONG_FORMAT, 
                    'data': None},400
            """ elif request.is_json:
                print("here for json")
                data = request.get_json(force=True)
                input = clean_json(data) """
        else:
            return {'status_code':  API_Status.BAD_PAYLOAD,
                    'status_message':API_Status_Message.BAD_PAYLOAD, 
                    'data': None}, 400 

""" data = pd.read_sql_query("Select * from public.predictions", db_engine)
print(data)
print(MODELS_PATH) """
