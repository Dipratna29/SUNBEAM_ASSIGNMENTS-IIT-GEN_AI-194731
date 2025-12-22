import os
import requests
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Weather Report",
    page_icon="🌦",
    layout="centered"
)

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -----------------------------
# Initialize LLM
# -----------------------------
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# -----------------------------
# UI Header
# -----------------------------
st.title("🌦 AI Weather Report")
st.subheader("Welcome, to weather report:")
st.write("Enter city to get weather report...")

city = st.text_input("City:")

# -----------------------------
# API Functions
# -----------------------------
def get_current_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    return requests.get(url, params=params).json()

def get_forecast(city):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
    return requests.get(url, params=params).json()

def ai_summary(weather):
    prompt = f"""
    Weather details:
    Temperature: {weather['main']['temp']} °C
    Feels Like: {weather['main']['feels_like']} °C
    Humidity: {weather['main']['humidity']} %
    Pressure: {weather['main']['pressure']} hPa
    Weather: {weather['weather'][0]['description']}
    Wind Speed: {weather['wind']['speed']} m/s

    Explain weather in simple English.
    """
    return llm.invoke(prompt).content

# -----------------------------
# Button Action
# -----------------------------
if st.button("🔍 Get Weather"):
    if not city:
        st.warning("Please enter city name")
    else:
        weather = get_current_weather(city)
        forecast = get_forecast(city)

        if weather.get("cod") != 200:
            st.error("City not found!")
        else:
            country = weather["sys"]["country"]
            flag_url = f"https://flagsapi.com/{country}/flat/64.png"
            icon = weather["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"

            # -----------------------------
            # Current Weather Section
            # -----------------------------
            st.header(f"Weather Report for {weather['name']}")
            st.image(flag_url, width=60)
            st.image(icon_url)

            st.markdown(f"""
            **Temperature:** {weather['main']['temp']}°C (feels like {weather['main']['feels_like']}°C)  
            **Humidity:** {weather['main']['humidity']}%  
            **Pressure:** {weather['main']['pressure']} hPa  
            **Weather Conditions:** {weather['weather'][0]['description'].title()}  
            **Wind Speed:** {weather['wind']['speed']} m/s  
            **Rain Information:** {"Rain available" if "rain" in weather else "No rain data available"}
            """)

            # -----------------------------
            # AI Explanation
            # -----------------------------
            st.subheader("🤖 Weather Summary")
            st.write(ai_summary(weather))

            # -----------------------------
            # 5-Day Forecast Chart
            # -----------------------------
            temps = []
            dates = []

            for item in forecast["list"]:
                temps.append(item["main"]["temp"])
                dates.append(item["dt_txt"])

            fig = px.line(
                x=dates,
                y=temps,
                labels={"x": "Date & Time", "y": "Temperature (°C)"},
                title="📊 5-Day Temperature Trend"
            )
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("🚀 Powered by OpenWeather API, Groq LLM & Streamlit")
