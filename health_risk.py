def calculate_risk(aqi, pm25, age, asthma):

    score = 0

    if aqi >= 4:
        score += 40

    if pm25 > 35:
        score += 30

    if age > 60:
        score += 20

    if asthma:
        score += 30

    if score >= 70:
        return "High Risk"

    elif score >= 40:
        return "Medium Risk"

    else:
        return "Low Risk"