import streamlit as st
import pandas as pd
from pandasql import sqldf

st.title("Upload CSV ")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])


if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)
    st.success("CSV file uploaded successfully!")

    st.subheader("Preview of CSV Data")
    st.dataframe(df)

    st.subheader("Enter SQL Query")
    st.markdown(" Use **df** as table name")

    # SQL query input
    query = st.text_area(
        "Example: SELECT * FROM df LIMIT 5"
    )

    if st.button("Execute Query"):
            result = sqldf(query, {"df": df})
            st.subheader("Query Result")
            st.dataframe(result)
       

