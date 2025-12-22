import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

# -------------------------------
# TOOL
# -------------------------------
@tool
def calculator(expression):
    """
    Solves arithmetic expressions with +, -, *, /, ()
    """
    try:
        return str(eval(expression))
    except:
        return "Error: Cannot solve expression"


# -------------------------------
# LLM SETUP
# -------------------------------
llm = init_chat_model(
    model="google/gemma-3-12b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)

agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt="You are a helpful assistant. Answer in short."
)

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(
    page_title="LangChain Agent Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 LangChain Agent with Calculator")
st.caption("Powered by local Gemma model")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type a message or math expression...")

if user_input:
    # show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # invoke agent
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    ai_reply = result["messages"][-1].content

    # show AI message
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )
    with st.chat_message("assistant"):
        st.markdown(ai_reply)

# Clear chat button
if st.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()
