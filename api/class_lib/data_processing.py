from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from io import StringIO
import pickle
import os, sys
from .processing import PreProcessing, PredictUsingModel
sys.path.insert(1, os.path.abspath('.'))
from config import *

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

try:
    host = os.getenv('DB_HOST')
    db = os.getenv('DB_DATABASE')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    port = os.getenv('DB_PORT')
    conn = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, db)
    db_engine = create_engine(conn)
except Exception as err:
    print(f"{err}")

preprocessing = PreProcessing()
predict_model = PredictUsingModel()

def clean_files(data):
    """
        function to perform preprocessing and predictions
    """
    s=str(data,'utf-8')
    data = StringIO(s) 
    df=pd.read_csv(data)
    cleaned_data = preprocessing.clean_files(df)
    if isinstance(cleaned_data, pd.DataFrame):
        #predicted_val_kmeans = predict_model.predictUsingKmeans(cleaned_data)
        predicted_val_dt = predict_model.predictUsingDT(cleaned_data)
        insert_into_db(df, predicted_val_dt)
        return predicted_val_dt
    else:
        return cleaned_data
    
    
def insert_into_db(input, output) -> None:
    """
        Insert input and output into the database
    """
    with db_engine.connect() as conn:
        query = f'''INSERT INTO predictions(user_input, predicted_output) VALUES (:input_val, :output_val)'''
        result = conn.execute(text(query), input_val = str(input), output_val = str(output))
        

def get_top_10_prediction() -> pd.DataFrame:
    """
        Get TOP 10 Predictions
    """
    query = f'SELECT p.user_input, p.predicted_output, p.txtdate FROM predictions p ORDER BY p.txtdate DESC LIMIT 10'
    result = pd.read_sql_query(query, db_engine)
    return result