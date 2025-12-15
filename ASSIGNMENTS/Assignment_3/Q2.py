import streamlit as st
import requests

# ---------- Session State ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "logout" not in st.session_state:
    st.session_state.logout = False


# ---------- Fake Login Function ----------
def login(username, password):
    return username == password


# ---------- Get Weather Function ----------
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=13226762cf08d11904e1fd2ee94af569&units=metric"
    response = requests.get(url)
    return response.json()


# ---------- Logout ----------
def logout():
    st.session_state.logged_in = False
    st.session_state.logout = True


# ---------- UI ----------
st.title(" Weather Application")

# ----- Logout Message -----
if st.session_state.logout:
    st.success(" Thanks for using the application!")
    st.stop()


# ----- Login Page -----
if not st.session_state.logged_in:
    st.subheader(" Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid login! Username and password must be same.")

# ----- Weather Page -----
else:
    st.subheader(" Current Weather")

    city = st.text_input("Enter City Name")

    if st.button("Get Weather"):
        if city:
            data = get_weather(city)

            if data.get("cod") != 200:
                st.error("City not found!")
            else:
                st.write(f"**City:** {data['name']}")
                st.write(f"**Temperature:** {data['main']['temp']} °C")
                st.write(f"**Weather:** {data['weather'][0]['description']}")
                st.write(f"**Humidity:** {data['main']['humidity']}%")
        else:
            st.warning("Please enter a city name")

    st.button("Logout", on_click=logout)
