import streamlit as st
import os
import pandas as pd
import json


from pdf_utils import extract_text_from_pdf
from vector_store import (
    add_resume, delete_resume, list_resumes,
    search_resumes, get_resume_metadata
)
from resume_ai import resume_summary, resume_scoring
from report_generator import generate_pdf_report

st.set_page_config("AI Resume Shortlisting", layout="wide")
st.title(" AI Enabled Resume Shortlisting System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Upload Resumes",
        "List Resumes",
        "Delete Resume",
        "Shortlist Resumes"
    ]
)




if menu == "Dashboard":
    st.header(" HR Dashboard")

    resumes = list_resumes()
    st.metric("Total Resumes", len(resumes))


elif menu == "Upload Resumes":
    st.header("Bulk Resume Upload (PDF)")

    files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if files:
        for file in files:
            with open(file.name, "wb") as f:
                f.write(file.read())

            text = extract_text_from_pdf(file.name)

            with st.spinner(f"Analyzing {file.name}"):
                summary = resume_summary(text)

            add_resume(
                text,
                file.name,
                ai_metadata={"summary": summary}
            )

            os.remove(file.name)

        st.success("All resumes uploaded and analyzed")


elif menu == "List Resumes":
    st.header("Stored Resumes")
    for r in list_resumes():
        st.write("•", r)


elif menu == "Delete Resume":
    st.header("Delete Resume")
    resumes = list_resumes()

    if resumes:
        r = st.selectbox("Select resume", resumes)
        if st.button("Delete"):
            delete_resume(r)
            st.success("Resume deleted")


elif menu == "Shortlist Resumes":
    st.header("Shortlist & Rank Resumes")

    job_desc = st.text_area("Enter Job Description", height=150)
    top_n = st.slider("Top N", 1, 10, 3)

    if st.button("Shortlist"):
        results = search_resumes(job_desc, top_n)

        names, scores = [], []

        for i, doc in enumerate(results, 1):
            rid = doc.metadata["resume_id"]
            st.markdown(f"## {i}. {rid}")

            with st.spinner("Evaluating resume with AI"):
                summary = resume_summary(doc.page_content)
                score_text = resume_scoring(doc.page_content, job_desc)

            st.subheader("📌 Professional Summary")
            st.write(summary)

            st.subheader("📊 AI Evaluation")
            st.write(score_text)

            pdf_name = f"{rid}_AI_Report.pdf"
            generate_pdf_report(pdf_name, summary, score_text)

            with open(pdf_name, "rb") as f:
                st.download_button(
                    " Download AI Report",
                    f,
                    file_name=pdf_name
                )

            
            score_value = int([s for s in score_text.split() if s.isdigit()][0])
            names.append(rid)
            scores.append(score_value)

        df = pd.DataFrame({"Resume": names, "Score": scores})
        st.subheader(" Resume Ranking Chart")
        st.bar_chart(df.set_index("Resume"))
