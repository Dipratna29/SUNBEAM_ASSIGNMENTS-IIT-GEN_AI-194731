import os
import streamlit as s
import mysql.connector
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

# ---------- ENV ----------
load_dotenv()
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")
DB_NAME = "sunbeam"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------- LLM ----------
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# ---------- SESSION STATE ----------
defaults = {
    "btn": False,
    "conversation": [],
    "conn": None,
    "cursor": None,
    "table_name": None,
    "metadata": None
}
for k, v in defaults.items():
    s.session_state.setdefault(k, v)

# ---------- DB UTILS ----------
def fetch_database_data(query):
    if not s.session_state.cursor:
        return "Error: Database not connected. Please connect database first."
    try:
        cur = s.session_state.cursor
        cur.execute(query)
        return cur.fetchall()
    except mysql.connector.Error as e:
        return f"MySQL Error: {e}"

def load_database():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DB_NAME
        )
        cur = conn.cursor()
        s.session_state.update({"conn": conn, "cursor": cur})

        s.success("Connected to MYSQL database!")

        cur.execute("SHOW TABLES")
        table = cur.fetchall()[0][0]
        s.session_state.table_name = table
        s.write("Tables in database:", table)

        cur.execute(f"DESCRIBE {table}")
        schema = cur.fetchall()
        s.session_state.metadata = schema
        s.table(schema)

    except mysql.connector.Error as e:
        s.error(e)

def disc_database():
    try:
        if s.session_state.cursor:
            s.session_state.cursor.close()
        if s.session_state.conn:
            s.session_state.conn.close()
        s.session_state.update({"cursor": None, "conn": None})
        s.success("Database disconnected")
    except Exception as e:
        s.error(e)

# ---------- AGENT ----------
agent = create_agent(
    model=llm,
    tools=[fetch_database_data],
    system_prompt="You are a helpful assistant. Give correct answer."
)

# ---------- UI ----------
s.title("MYSQL Data explorer")

if s.button("Connect Database", type="primary"):
    load_database()

if s.button("Disconnect Database", type="primary"):
    disc_database()

question = s.chat_input("Ask something about database...")

if question:
    s.subheader("You")
    s.write(question)

    sql_prompt = f"""
    Table name: {s.session_state.table_name}
    Table schema: {s.session_state.metadata}
    Question: {question}

    Instruction:
    - You are a MySQL expert
    - Generate ONLY SQL query
    - No explanation, no markdown
    - Use LOWER() for text matching
    - If not possible, reply with: Error: please ask right question
    """

    query = llm.invoke(sql_prompt).content.strip()
    s.markdown(query)

    result = fetch_database_data(query)
    s.table(result)

    explain_prompt = f"""
    Table name: {s.session_state.table_name}
    Query output: {result}

    Instruction:
    - Explain output in simple English
    - Do NOT explain SQL syntax
    - If empty, say: No data found for the question
    """

    explanation = llm.invoke(explain_prompt).content.strip()
    s.subheader("Assistant")
    s.write(explanation)
