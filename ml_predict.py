import joblib
import numpy as np

model = joblib.load("aqi_model.pkl")

def predict_aqi(pm25, temperature):
    prediction = model.predict(np.array([[pm25, temperature]]))
    return round(prediction[0])