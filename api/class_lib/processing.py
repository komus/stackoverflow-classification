import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import pickle
import os, sys
sys.path.insert(1, os.path.abspath('.'))
from config import *

from dotenv import load_dotenv
from pathlib import Path


class PreProcessing:
    def __init__(self) -> None:
        model_pkl_filename = MODELS_PATH + 'labelencoding.pkl'
        with open(model_pkl_filename, "rb") as f:
            self.__lb_encode = pickle.load(f)
        
        lb_name = MODELS_PATH + 'onehotencoding.pkl'
        with open(lb_name, "rb") as f:
            self.__ohe_encode = pickle.load(f)
    
    def clean_files(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            data = self.__clean_up_columns(data)
            stack_features = self.__fill_empty(data)
            stack_features = self.__label_encode(stack_features)
            stack_features = self.__one_hot_encode(stack_features)
            """ dt_feature = stack_features.copy().drop(columns=['user_badge_type', 'tags_count', 'encoded_user_badge'])
            feature_y = stack_features['tags_count']
            dt_feature_knn = stack_features.copy().drop(columns=['user_badge_type','encoded_user_badge']) """
            return stack_features
            

        except Exception as error:
            return f"{error}"
    
    def __clean_up_columns(self, data:pd.DataFrame) -> pd.DataFrame:
        data = data.drop(columns='Unnamed: 0')
        data['id'] = data['id'].apply(lambda x: x[x.find('question-summary-') + 17:]).astype(int)
        data['answer']=data['answer'].str.extract(r'(\d)').astype(int)
        data['views']=data['views'].str.extract(r'(\d)').astype(int)
        data['user_reputation_score']= data.user_reputation_score.replace(',','', regex=True)
        data['user_reputation_score']= (data.user_reputation_score.replace(r'[km]+$', '', regex=True).astype(float) * data.user_reputation_score.str.extract(r'[\d\.]+([km]+)', expand=False).fillna(1).replace(['k','m'], [10**3, 10**6]).astype(int))
        data['user_badge_number'] = data.user_badge.str.extract(r'(\d)')
        data['user_badge_type'] = data.user_badge.str.extract('([a-zA-Z]+)', expand=True)
        data['tags_count'] = data.tags.str.split(':').str.len()-1
        data['question_time'] = pd.to_datetime(data['question_time'])
        max_date = pd.to_datetime("now")
        data['days_in_queue'] = data['question_time'].apply(lambda x: days_in_batch(max_date, x.replace(tzinfo=None)))
        return data

    def __fill_empty(self, data: pd.DataFrame) -> pd.DataFrame:
        stack_features = data[['user_reputation_score', 'votes','answer', 'views', 'accepted_answer', 'user_badge_number','user_badge_type', 'tags_count', 'days_in_queue']]
        for col in categorical:
            stack_features[col] = stack_features[col].replace(r'^\s*$', 'NaN', regex=True)
            
        for col in numerical:
            stack_features[col] = stack_features[col].fillna(0)
        
        return stack_features

    def __label_encode(self, data:pd.DataFrame) -> pd.DataFrame:
        data['encoded_user_badge'] = self.__lb_encode.transform(data['user_badge_type'])
        return data

    def __one_hot_encode(self, data:pd.DataFrame) -> pd.DataFrame:
        encoded_badge = self.__ohe_encode.transform(data[['encoded_user_badge']]).toarray()
        encoded_badge = pd.DataFrame(encoded_badge)
        stack_features = pd.merge(data, encoded_badge, left_index=True, right_index=True)
        return stack_features


class PredictUsingModel:
    def __init__(self) -> None:
        model_pkl_filename = MODELS_PATH + 'kmeans_3_clusters.pkl'
        with open(model_pkl_filename, "rb") as f:
            self.__kmeans = pickle.load(f)
        
        lb_name = MODELS_PATH + 'decisiontree.pkl'
        with open(lb_name, "rb") as f:
            self.__decisiontree = pickle.load(f)

    def predictUsingKmeans(self, data:pd.DataFrame) -> np.array:
        data = data.drop(columns=['user_badge_type','encoded_user_badge'])
        labels =  self.__kmeans.predict(data)
        return labels

    def predictUsingDT(self, data:pd.DataFrame) -> np.array:
        data = data.drop(columns=['user_badge_type', 'tags_count', 'encoded_user_badge'])
        predicted_class = self.__decisiontree.predict(data)
        return predicted_class