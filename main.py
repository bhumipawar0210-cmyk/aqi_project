from fastapi import FastAPI
from ai_recommendation import get_recommendation
from weather_api import get_environment_data
from health_risk import calculate_risk
from database import create_table, save_data
from models import UserData
from ml_predict import predict_aqi

app = FastAPI()

create_table()

# -------------------- HEALTH-RISK (STATIC MUMBAI) --------------------
@app.get("/health-risk")
def health_risk():

    lat = 19.0760
    lon = 72.8777

    data = get_environment_data(lat, lon)

    save_data(
        "Mumbai",
        data["aqi"],
        data["pm25"],
        data["pm10"],
        data["temperature"],
        data["humidity"]
    )

    risk = calculate_risk(
        data["aqi"],
        data["pm25"],
        25,
        True
    )

    recommendation = get_recommendation(data["aqi"])

    return {
        "city": "Mumbai",
        "aqi": data["aqi"],
        "pm25": data["pm25"],
        "pm10": data["pm10"],
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "health_risk": risk,
        "recommendation": recommendation
    }


# -------------------- USER HEALTH RISK (MAHARASHTRA MODEL) --------------------
@app.post("/user-health-risk")
def user_health_risk(user: UserData):

    region = user.region

    cities = {
        "Mumbai": (19.0760, 72.8777),
        "Pune": (18.5204, 73.8567),
        "Nagpur": (21.1458, 79.0882),
        "Nashik": (19.9975, 73.7898)
    }

    total_aqi = 0
    count = 0

    for city, coords in cities.items():
        data = get_environment_data(coords[0], coords[1])
        total_aqi += data["aqi"]
        count += 1

    avg_aqi = total_aqi / count

    save_data(
        "Maharashtra",
        avg_aqi,
        0, 0, 0, 0
    )

    risk = calculate_risk(
        avg_aqi,
        0,
        user.age,
        user.asthma
    )

    recommendation = get_recommendation(avg_aqi)

    return {
        "name": user.name,
        "region": region,
        "aqi": avg_aqi,
        "health_risk": risk,
        "recommendation": recommendation
    }


# -------------------- ML AQI PREDICTION --------------------
@app.get("/predict-aqi")
def predict():

    pm25 = 60
    temperature = 28

    predicted = predict_aqi(pm25, temperature)

    return {
        "pm25": pm25,
        "temperature": temperature,
        "predicted_aqi": predicted
    }