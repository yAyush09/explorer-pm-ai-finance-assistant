# preprocess.py
import joblib
import pandas as pd

# Load label encoder
le = joblib.load('saved_model/label_encoder.pkl')

def preprocess_user_input(data_dict, model):
    df = pd.DataFrame([data_dict])
    df['Occupation'] = le.transform([df['Occupation'][0]])

    # Align columns with model input
    expected_columns = model.feature_names_in_
    df = df[expected_columns]

    return df
