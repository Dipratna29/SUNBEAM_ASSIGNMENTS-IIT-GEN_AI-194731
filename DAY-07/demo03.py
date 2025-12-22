import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests

# -------------------- SETUP --------------------
load_dotenv()
st.set_page_config(page_title="LangChain Agent with Tools", layout="wide")

st.title("🤖 LangChain Agent with Tools")
st.write("Calculator • File Reader • Weather • Knowledge Lookup")

# -------------------- TOOLS --------------------

@tool
def calculator(expression: str) -> str:
    """Solves arithmetic expressions"""
    try:
        return str(eval(expression))
    except:
        return "Error: Invalid expression"


@tool
def read_file(filepath: str) -> str:
    """Reads content of a text file"""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except:
        return "Error: File not found"


@tool
def get_weather(city: str) -> str:
    """Returns current weather of a city"""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )
        response = requests.get(url)
        return json.dumps(response.json())
    except:
        return "Error: Weather not found"


@tool
def knowledge_lookup(topic: str) -> str:
    """Basic knowledge lookup"""
    knowledge_base = {
        "ai": "AI is the simulation of human intelligence in machines.",
        "ml": "Machine Learning is a subset of AI that learns from data.",
        "llm": "LLM stands for Large Language Model.",
        "agent": "An agent uses tools to perform tasks intelligently."
    }
    return knowledge_base.get(topic.lower(), "No data available")

# -------------------- MODEL --------------------

llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

# -------------------- AGENT --------------------

agent = create_agent(
    model=llm,
    tools=[
        calculator,
        read_file,
        get_weather,
        knowledge_lookup
    ],
    system_prompt="You are a helpful assistant. Answer briefly."
)

# -------------------- SESSION STATE --------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- UI --------------------

user_input = st.text_input("Enter your query:")

if st.button("Ask Agent"):
    if user_input:
        with st.spinner("Agent is thinking..."):
            result = agent.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })

            final_answer = result["messages"][-1].content

            # save history
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", final_answer))

            # logging (tool flow)
            with st.expander("🔍 Message History / Tool Calls"):
                for msg in result["messages"]:
                    st.write(msg)

# -------------------- CHAT DISPLAY --------------------

st.subheader("💬 Chat History")
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")
