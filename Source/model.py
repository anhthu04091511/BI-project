import pickle
import os
import numpy as np
import pandas as pd
from keras_preprocessing.sequence import pad_sequences

from keras.models import load_model
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense

class Model:
    def __init__(self):
        self.models_dict = {
            'outliers' : {
                'CB': pickle.load(open('./model/outliers/CB.pkl', 'rb')),
                'DT': pickle.load(open('./model/outliers/DT.pkl', 'rb')),
                'KNN': pickle.load(open('./model/outliers/KNN.pkl', 'rb')),
                'Lasso': pickle.load(open('./model/outliers/Lasso.pkl', 'rb')),
                'LR': pickle.load(open('./model/outliers/LR.pkl', 'rb')),
                'MLP': pickle.load(open('./model/outliers/MLP.pkl', 'rb')),
                'NN_L': tf.keras.models.load_model('./model/outliers/NN_L.h5'),
                'NN_M': tf.keras.models.load_model('./model/outliers/NN_M.h5'),
                'NN_S': tf.keras.models.load_model('./model/outliers/NN_S.h5'),
                'NN_XL': tf.keras.models.load_model('./model/outliers/NN_XL.h5'),
                'NN_XL_nor': tf.keras.models.load_model('./model/outliers/NN_XL_nor.h5'),
                'RF': pickle.load(open('./model/outliers/RF.pkl', 'rb')),
                'Ridge': pickle.load(open('./model/outliers/Ridge.pkl', 'rb')),
                'XGB': pickle.load(open('./model/outliers/XGB.pkl', 'rb')),
            },
            'no_outliers' : {
                'CB': pickle.load(open('./model/no_outliers/CB.pkl', 'rb')),
                'DT': pickle.load(open('./model/no_outliers/DT.pkl', 'rb')),
                'KNN': pickle.load(open('./model/no_outliers/KNN.pkl', 'rb')),
                'Lasso': pickle.load(open('./model/no_outliers/Lasso.pkl', 'rb')),
                'LR': pickle.load(open('./model/no_outliers/LR.pkl', 'rb')),
                'MLP': pickle.load(open('./model/no_outliers/MLP.pkl', 'rb')),
                'NN_L': tf.keras.models.load_model('./model/no_outliers/NN_L.h5'),
                'NN_M': tf.keras.models.load_model('./model/no_outliers/NN_M.h5'),
                'NN_S': tf.keras.models.load_model('./model/no_outliers/NN_S.h5'),
                'NN_XL': tf.keras.models.load_model('./model/no_outliers/NN_XL.h5'),
                'NN_XL_nor': tf.keras.models.load_model('./model/no_outliers/NN_XL_nor.h5'),
                'RF': pickle.load(open('./model/no_outliers/RF.pkl', 'rb')),
                'Ridge': pickle.load(open('./model/no_outliers/Ridge.pkl', 'rb')),
                'XGB': pickle.load(open('./model/no_outliers/XGB.pkl', 'rb')),
            },
            'no_outliers_threshold': {
                'CB': pickle.load(open('./model/no_outliers_threshold/CB.pkl', 'rb')),
                'DT': pickle.load(open('./model/no_outliers_threshold/DT.pkl', 'rb')),
                'KNN': pickle.load(open('./model/no_outliers_threshold/KNN.pkl', 'rb')),
                'Lasso': pickle.load(open('./model/no_outliers_threshold/Lasso.pkl', 'rb')),
                'LR': pickle.load(open('./model/no_outliers_threshold/LR.pkl', 'rb')),
                'MLP': pickle.load(open('./model/no_outliers_threshold/MLP.pkl', 'rb')),
                'NN_L': tf.keras.models.load_model('./model/no_outliers_threshold/NN_L.h5'),
                'NN_M': tf.keras.models.load_model('./model/no_outliers_threshold/NN_M.h5'),
                'NN_S': tf.keras.models.load_model('./model/no_outliers_threshold/NN_S.h5'),
                'NN_XL': tf.keras.models.load_model('./model/no_outliers_threshold/NN_XL.h5'),
                'NN_XL_nor': tf.keras.models.load_model('./model/no_outliers_threshold/NN_XL_nor.h5'),
                'RF': pickle.load(open('./model/no_outliers_threshold/RF.pkl', 'rb')),
                'Ridge': pickle.load(open('./model/no_outliers_threshold/Ridge.pkl', 'rb')),
                'XGB': pickle.load(open('./model/no_outliers_threshold/XGB.pkl', 'rb')),
            }
        }
        self.model_type = 'outliers'
        self.model_name = 'LR'
        
    def select_model(self, model_type, model_name):
        # thay đổi model
        self.model_name = model_name
        self.model_type = model_type
    
    def predict(self, X_test):
        if self.model_name in ['NN_S', 'NN_M', 'NN_L', 'NN_XL', 'NN_XL_nor']:
            y_pred = self.models_dict[self.model_type][self.model_name].predict(X_test, verbose=0)      # dự đoán
            y_pred = y_pred.flatten()
        else:
            y_pred = self.models_dict[self.model_type][self.model_name].predict(X_test)      # dự đoán
        return y_pred[0]
    
class Preprocessor:
    def __init__(self, maxlen=35):
        self.model_type = 'outliers'
        self.MAXLEN = maxlen
        # scaler
        self.scaler_dict = {
            'outliers': pickle.load(open('processor/outliers/scaler.pkl', 'rb')),
            'no_outliers' : pickle.load(open('processor/no_outliers/scaler.pkl', 'rb')),
            'no_outliers_threshold': pickle.load(open('processor/no_outliers_threshold/scaler.pkl', 'rb'))
        }
        # amenities tokenizer
        self.amenities_tokenizer= pickle.load(open('processor/amenities_tokenizer.pkl', 'rb'))
        # label encoders
        self.dict_label_encoder = pickle.load(open('processor/dict_label_encoder.pkl', 'rb'))
        # embedding
        self.embedding =  load_model('processor/embedding_model.h5')
    
    def select_processor(self, model_type):
        self.model_type = model_type

    # xử lý bên dưới
    def texts_to_pad_sequences(self, text):
        print(text)
        sequences = self.amenities_tokenizer['tokenizer'].texts_to_sequences(text)
        padded_sequences = pad_sequences(sequences, maxlen=self.MAXLEN)
        return padded_sequences
    
    def embedding_data(self, padded_sequences):
        # Biến đổi dữ liệu để lấy embedding của "amenities"
        return self.embedding.predict(padded_sequences, verbose=0)
    
    def process(self, data):
        #data: dict
        # if data.get('cityname') == '':
        #     return ''
        
        data = {
            #'category': data.get('category'),
            'amenities': data.get('amenities').lower(),
            'bathrooms': int(data.get('bathrooms')),
            'bedrooms': int(data.get('bedrooms')),
            #'fee': 'yes' if data.get('fee') else 'no',
            #'pets_allowed': data.get('pets_allowed').lower(),
            'square_feet': float(data.get('square_feet')),
            #'cityname': data.get('cityname').lower().replace('city', '').replace('of', '').strip(),
            'state': data.get('state').lower().replace('District of','').strip(),
            'latitude': float(data.get('latitude')),
            'longitude': float(data.get('longitude'))
        }
        df_test = pd.DataFrame([data])
        df_test = df_test.fillna("")
        # Lấy tên của tất cả các cột có kiểu dữ liệu là object
        object_columns = df_test.select_dtypes(include='object').columns

        # Duyệt qua từng cột và chuyển đổi giá trị thành chữ thường
        for col in object_columns:
            df_test[col] = df_test[col].str.lower()

        features_label_encoder = ['state']
        for feature in features_label_encoder:
            df_test[feature] = self.dict_label_encoder[feature].transform(df_test[feature])
        #
        pad_seq_amenities_test = self.texts_to_pad_sequences(df_test['amenities'].values)

        amenities_embedded_test = self.embedding_data(pad_seq_amenities_test)
        # lấy ra các đặc trưng dạng số
        num_features = ['bathrooms', 'bedrooms', 'square_feet', 'state', 'latitude', 'longitude']
        numerical_features_test = df_test[num_features].values
        numerical_features_test_scaled = self.scaler_dict[self.model_type].transform(numerical_features_test)

        X_test = np.concatenate([numerical_features_test_scaled, amenities_embedded_test], axis=1)
        return X_test