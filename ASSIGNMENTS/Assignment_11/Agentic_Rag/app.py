import os
import pandas as pd
import streamlit as st
from config import PDF_FOLDER
from utils import extract_candidate_name
from agent import agent, system_message

# Page config
st.set_page_config(page_title="Agentic Resume RAG", layout="wide")
st.title("📄 Agentic Resume Intelligence")

# Show uploaded resumes
data = []
for file in os.listdir(PDF_FOLDER):
    if file.endswith(".pdf"):
        data.append({
            "PDF File": file,
            "Candidate Name": extract_candidate_name(os.path.join(PDF_FOLDER, file))
        })

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# Sidebar controls
with st.sidebar:
    st.header("Resume Management")

    upload = st.file_uploader("Upload Resume", type=["pdf"])
    delete = st.selectbox("Delete Resume", ["Select"] + df["PDF File"].tolist())

    if upload:
        with open(os.path.join(PDF_FOLDER, upload.name), "wb") as f:
            f.write(upload.getbuffer())
        st.success("Resume added. Refresh app.")

    if delete != "Select":
        if st.button("Confirm Delete"):
            os.remove(os.path.join(PDF_FOLDER, delete))
            st.success("Resume deleted. Refresh app.")

# Chat input
query = st.chat_input("Ask resume-related question")

if query:
    response = agent.invoke({
        "messages": [system_message, {"role": "user", "content": query}]
    })

    st.subheader("Answer")
    st.write(response["messages"][-1].content)
