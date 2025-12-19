from langchain.chat_models import init_chat_model
import os
import streamlit as st
from dotenv import load_dotenv
import requests

load_dotenv()
weatherapi_key = os.getenv("Weather_API")
api_key = os.getenv("Groq_API_Key")
llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = api_key
)

st.header("🌤 Weather App")
st.write("Welcome to the Weather App!")

if 'conversation' not in st.session_state:
    st.session_state.conversation = [
    
        {"role": "system", "content": "You are explain weather."}
    ]

for msg in st.session_state.conversation:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.write(msg["content"])   

city = st.text_input("Enter city")
if city:
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherapi_key}&units=metric"
        response = requests.get(url)
        weather = response.json()

        if weather.get("cod") != 200:
            st.error("City not found")
        else:
            temp = weather["main"]["temp"]
            humidity = weather["main"]["humidity"]
            wind_speed = weather["wind"]["speed"]
            st.write(f"Temperature: {temp} °C")
            st.write(f"Humidity: {humidity} %")
            st.write(f"Wind Speed: {wind_speed} m/s")

            llm_input = f"""
                -City: {city}
                -temperature: {temp}
                -humidity: {humidity}
                -wind_speed: {wind_speed}

                explain the weather in simple English.
                
            """
            explanation = llm.invoke(llm_input)
            st.session_state.conversation.append({"role": "assistant", "content": explanation.content})
            st.write("Weather Explanation:", explanation.content)
    except:
        st.error("Some error occurred")