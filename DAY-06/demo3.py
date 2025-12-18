import streamlit as st
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Groq Chat", layout="centered")
st.title("💬 Chat with Groq LLM")

# Initialize LLM (Groq OpenAI-compatible)
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)

# Initialize conversation memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display previous messages
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("You:")

if user_input:
    # Add user message
    user_msg = {"role": "user", "content": user_input}
    st.session_state.conversation.append(user_msg)

    with st.chat_message("user"):
        st.markdown(user_input)

    # Invoke LLM with full conversation
    llm_output = llm.invoke(st.session_state.conversation)

    # Add assistant response
    assistant_msg = {
        "role": "assistant",
        "content": llm_output.content
    }
    st.session_state.conversation.append(assistant_msg)

    with st.chat_message("assistant"):
        st.markdown(llm_output.content)
