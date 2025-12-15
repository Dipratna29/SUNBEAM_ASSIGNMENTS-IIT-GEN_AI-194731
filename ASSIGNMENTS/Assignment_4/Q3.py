import streamlit as st
import time

st.title("Simple Chatbot")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


def stream_reply(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.2)   # delay for chat effect



for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# User input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.write(user_input)

    bot_reply = f"You said: {user_input}"

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
    # st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    # st.image("https://www.python.org/static/community_logos/python-logo.png")
    # st.download_button("Download Example File", data="Example file content", file_name="example.txt")
    # st.audio_input("Record your voice:")


    # Stream bot reply
    with st.chat_message("assistant"):
        st.write_stream(stream_reply(bot_reply))