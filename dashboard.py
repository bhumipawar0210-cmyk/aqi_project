import streamlit as st
import requests
from graph import get_data
import pandas as pd
import pydeck as pdk

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Environmental Health Analytics",
    page_icon="🌍",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
    }

    h1 {
        color: #00d4ff;
        text-align: center;
    }

    .stButton>button {
        background-color: #00d4ff;
        color: black;
        border-radius: 10px;
        height: 45px;
        width: 100%;
        font-weight: bold;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🌍 SMART AQI LOGIN")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# ---------------- DASHBOARD ----------------
st.title("🌍 SMART AQI DASHBOARD")

# ---------------- CHATBOT ----------------
st.subheader("🤖 AQI AI Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask about AQI / Health / Pollution")

def get_chat_response(query, aqi):
    query = query.lower()

    if "good" in query or "safe" in query:
        if aqi <= 50:
            return "Yes 👍 Air quality is GOOD."
        elif aqi <= 100:
            return "Moderate ⚠️ Air is okay but limit exposure."
        else:
            return "No ❌ Air is polluted."

    if "aqi" in query:
        return f"AQI level is {aqi}."

    if "health" in query:
        if aqi <= 50:
            return "Low health risk 🟢"
        elif aqi <= 100:
            return "Moderate health risk 🟡"
        else:
            return "High health risk 🔴"

    return "Ask about AQI, health or pollution."

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("User Information")

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 100, 21)

    asthma = st.checkbox("Asthma")
    heart = st.checkbox("Heart Disease")

    check_button = st.button("Check Risk")

# ---------------- API CALL ----------------
data = {}

if check_button:
    try:
        response = requests.post(
            "http://127.0.0.1:8000/user-health-risk",
            json={
                "name": name,
                "age": age,
                "region": "Maharashtra",
                "asthma": asthma,
                "heart_disease": heart
            }
        )

        data = response.json()

        st.success("Result")

        col1, col2 = st.columns(2)

        with col1:
            aqi = data.get("aqi", 0)

            if aqi <= 50:
                status = "Good 🟢"
            elif aqi <= 100:
                status = "Moderate 🟡"
            else:
                status = "Poor 🔴"

            st.metric("AQI", f"{aqi} ({status})")

        with col2:
            risk = data.get("health_risk", "N/A")

            st.metric("Health Risk", risk)

        st.success(data.get("recommendation", "No recommendation"))

        # CHAT RESPONSE
        if user_input:
            reply = get_chat_response(user_input, aqi)
            st.session_state.chat_history.append((user_input, reply))

    except Exception as e:
        st.error(f"FastAPI Error: {e}")

# ---------------- CHAT DISPLAY ----------------
for q, a in st.session_state.chat_history:
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 AI:** {a}")
    st.markdown("---")

# ---------------- AQI CHART ----------------
st.subheader("📊 AQI Trend")

df = get_data()

if df is not None and not df.empty:
    st.line_chart(df["aqi"])
    st.dataframe(df)
else:
    st.warning("No data found")

# ---------------- MAHARASHTRA MAP ----------------
st.subheader("🌍 Maharashtra AQI Map")

city_data = [
    {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "aqi": 120