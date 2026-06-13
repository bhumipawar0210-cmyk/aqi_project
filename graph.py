from graph import get_data
import mysql.connector
import pandas as pd

def get_data():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="health_db"
    )

    query = "SELECT * FROM environmental_data"

    df = pd.read_sql(query, conn)

    conn.close()

    return df

    def predict_future_aqi(df):
    if df is None or df.empty:
        return 0

    # simple prediction (basic logic)
    return round(df["aqi"].mean())