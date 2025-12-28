import os
from dotenv import load_dotenv


load_dotenv()


PDF_FOLDER = r"D:\SUNBEAM\SUNBEAM_ASSIGNMENTS-IIT-GEN_AI-194731\ASSIGNMENTS\Assignment_11\Agentic_Rag\Pdfs"


CHROMA_DIR = "Chroma_db_full_docs"

# Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
