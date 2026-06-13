import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Sample dataset (replace later with real AQI dataset)
data = {
    "pm25": [20, 30, 40, 60, 80, 100, 120, 150],
    "temperature": [25, 26, 27, 28, 29, 30, 31, 32],
    "aqi": [50, 60, 80, 100, 120, 150, 180, 200]
}

df = pd.DataFrame(data)

X = df[["pm25", "temperature"]]
y = df["aqi"]

model = RandomForestRegressor()
model.fit(X, y)

joblib.dump(model, "aqi_model.pkl")

print("Model trained and saved successfully")