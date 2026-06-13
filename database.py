import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="health_db"
    )

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS environmental_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(50),
        aqi INT,
        pm25 FLOAT,
        pm10 FLOAT,
        temperature FLOAT,
        humidity FLOAT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def save_data(city, aqi, pm25, pm10, temperature, humidity):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO environmental_data
    (city, aqi, pm25, pm10, temperature, humidity)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (city, aqi, pm25, pm10, temperature, humidity)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()