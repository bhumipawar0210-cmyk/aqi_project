def get_recommendation(aqi):

    if aqi <= 50:
        return "Air quality is good. Safe for outdoor activities."

    elif aqi <= 100:
        return "Moderate air quality. Sensitive people should limit outdoor exposure."

    elif aqi <= 150:
        return "Wear a mask while outdoors."

    elif aqi <= 200:
        return "Avoid outdoor exercise."

    else:
        return "Stay indoors and use an air purifier."