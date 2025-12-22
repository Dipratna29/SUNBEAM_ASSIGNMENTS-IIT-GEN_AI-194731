import streamlit as st
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
import pandas as pd
import duckdb
import time

# ---------------------------------
# ENV + PAGE
# ---------------------------------
load_dotenv()

st.set_page_config(
    page_title="CSV SQL AI Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊📈📉 CSV → SQL AI Assistant")
st.caption("Chat with your CSV files using SQL powered by Groq LLM")

# ---------------------------------
# SIDEBAR
# ---------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("**Model:** llama-3.3-70b-versatile")
    st.markdown("**Engine:** DuckDB")
    st.markdown("---")
    st.markdown("### 📌 Example Questions")
    st.markdown("- Total records per table")
    st.markdown("- Average salary by department")
    st.markdown("- Join two tables")

# ---------------------------------
# INIT LLM
# ---------------------------------
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------------------
# SESSION STATE
# ---------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "tables" not in st.session_state:
    st.session_state.tables = {}

# ---------------------------------
# MULTI CSV UPLOAD
# ---------------------------------
uploaded_files = st.file_uploader(
    "📂 Upload one or more CSV files",
    type="csv",
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        table_name = os.path.splitext(file.name)[0]
        df = pd.read_csv(file)
        st.session_state.tables[table_name] = df

    st.success(f"Loaded {len(st.session_state.tables)} table(s)")

    with st.expander("🧬 Table Schemas"):
        for name, df in st.session_state.tables.items():
            st.markdown(f"### `{name}`")
            st.dataframe(
                pd.DataFrame({
                    "Column": df.columns,
                    "Type": df.dtypes.astype(str)
                })
            )

# ---------------------------------
# CHAT DISPLAY
# ---------------------------------
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------
# USER INPUT
# ---------------------------------
user_input = st.chat_input("Ask anything about your data...")

if user_input and st.session_state.tables:
    # Add user message
    st.session_state.chat.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build schema text
    schema_text = ""
    for name, df in st.session_state.tables.items():
        schema_text += f"\nTable: {name}\n{df.dtypes}\n"

    # Prompt
    sql_prompt = f"""
You are a senior SQLite expert.

Available Tables & Schemas:
{schema_text}

User Question:
{user_input}

Instruction:
Generate ONLY a valid SQL query.
Use table names exactly.
No explanation.
If not possible return 'Error'.
"""

    # ---------------------------------
    # STREAMING SQL GENERATION
    # ---------------------------------
    with st.chat_message("assistant"):
        st.markdown("🧠 **Generating SQL...**")
        sql_box = st.empty()
        sql_text = ""

        for chunk in llm.stream(sql_prompt):
            sql_text += chunk.content
            sql_box.code(sql_text, language="sql")
            time.sleep(0.02)

    st.session_state.chat.append(
        {"role": "assistant", "content": f"```sql\n{sql_text}\n```"}
    )

    # ---------------------------------
    # SQL EDITOR
    # ---------------------------------
    st.markdown("## ✏️ Edit SQL (Optional)")
    edited_sql = st.text_area(
        "Modify SQL before execution",
        value=sql_text,
        height=120
    )

    # ---------------------------------
    # EXECUTE SQL
    # ---------------------------------
    if st.button("🚀 Execute SQL"):
        try:
            con = duckdb.connect()
            for name, df in st.session_state.tables.items():
                con.register(name, df)

            result_df = con.execute(edited_sql).df()

            st.markdown("## 📈 Query Result")
            st.dataframe(result_df)

            # ---------------------------------
            # DOWNLOAD RESULT
            # ---------------------------------
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Result as CSV",
                csv,
                "query_result.csv",
                "text/csv"
            )

            # ---------------------------------
            # EXPLANATION
            # ---------------------------------
            explain_prompt = f"""
Explain this SQL result in simple English.

Question:
{user_input}

Result:
{result_df.head(10)}
"""
            explanation = llm.invoke(explain_prompt).content

            st.markdown("## 🧠 Explanation")
            st.info(explanation)

        except Exception as e:
            st.error(f"Execution Error: {e}")

elif not uploaded_files:
    st.info("👆 Upload CSV files to begin")

