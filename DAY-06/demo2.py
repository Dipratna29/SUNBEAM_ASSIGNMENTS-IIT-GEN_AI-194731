import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit UI
st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.title("🤖 Chat with Groq LLM")

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from Groq
    response = llm.invoke(user_input)

    # Show assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )
    with st.chat_message("assistant"):
        st.markdown(response.content)
