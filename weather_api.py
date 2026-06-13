import requests

API_KEY = "4fc7d6af051e187b72f038b4e287f029"

def get_environment_data(lat, lon):

    air_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    air = requests.get(air_url).json()
    weather = requests.get(weather_url).json()

    return {
        "aqi": air["list"][0]["main"]["aqi"],
        "pm25": air["list"][0]["components"]["pm2_5"],
        "pm10": air["list"][0]["components"]["pm10"],
        "temperature": weather["main"]["temp"],
        "humidity": weather["main"]["humidity"]
    }