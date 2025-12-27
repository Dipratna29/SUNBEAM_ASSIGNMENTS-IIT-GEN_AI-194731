import streamlit as s
import pandas as pd
from datetime import datetime
import os

USERS_FILE = "users.csv"
FILES_FILE = "userfiles.csv"

def load_users():
    if not os.path.exists(USERS_FILE):
        pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)
    return pd.read_csv(USERS_FILE)

def save_user(username, password):
    df = load_users()
    df.loc[len(df)] = [username, password]
    df.to_csv(USERS_FILE, index=False)

def save_upload_history(username, filename):
    if os.path.exists(FILES_FILE):
        df = pd.read_csv(FILES_FILE)
    else:
        df = pd.DataFrame(columns=["username", "filename", "datetime"])

    df.loc[len(df)] = [username, filename, datetime.now()]
    df.to_csv(FILES_FILE, index=False)

def home_page():
    s.title("Home")
    s.write("Welcome to CSV Explorer App")

def login_page():
    s.header("Login page")
    with s.form("login"):
        user = s.text_input("Username")
        pwd = s.text_input("Password", type="password")
        if s.form_submit_button("Login"):
            df = load_users()
            if ((df.username == user) & (df.password == pwd)).any():
                s.success("Login successful!")
                s.session_state.update({
                    "authenticated": True,
                    "user": user,
                    "page": "csv_explorer"
                })
            else:
                s.error("Invalid username or password")

def registration_page():
    s.title("Registration page")
    with s.form("register"):
        s.text_input("First name")
        s.text_input("Last name")
        user = s.text_input("Username")
        p1 = s.text_input("Password", type="password")
        p2 = s.text_input("Re-enter password", type="password")
        if s.form_submit_button("Register"):
            if p1 == p2:
                save_user(user, p1)
                s.success("Registration successfully done")
                s.session_state.page = "Login"
                s.rerun()
            else:
                s.toast("Incorrect password match")

def explore_csv_page():
    s.header("Explore CSV")
    file = s.file_uploader("Upload CSV file", type="csv")
    if file:
        df = pd.read_csv(file)
        s.dataframe(df)
        save_upload_history(s.session_state.user, file.name)

def history_page():
    s.header("Upload history")
    if os.path.exists(FILES_FILE):
        df = pd.read_csv(FILES_FILE)
        s.dataframe(df[df.username == s.session_state.user])


with s.sidebar:
    s.header("⊞ Menu")
    if not s.session_state.authenticated:
        if s.button("Login page", use_container_width=True):
            s.session_state.page = "Login"
        if s.button("Registration page", use_container_width=True):
            s.session_state.page = "registration"
        if s.button("Home page", use_container_width=True):
            s.session_state.page = "main"
    else:
        if s.button("Explore csv", use_container_width=True):
            s.session_state.page = "csv_explorer"
        if s.button("History", use_container_width=True):
            s.session_state.page = "history"
        if s.button("Logout"):
            s.session_state.update({
                "authenticated": False,
                "user": None,
                "page": "main"
            })
            s.rerun()

{
    "Login": login_page,
    "registration": registration_page,
    "main": home_page,
    "csv_explorer": explore_csv_page,
    "history": history_page
}.get(s.session_state.page, home_page)()
