import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import PDF_FOLDER, CHROMA_DIR
from utils import extract_candidate_name
import streamlit as st

@st.cache_resource
def load_vector_store():
    """
    Loads PDFs → creates embeddings → stores in Chroma DB
    """
    loader = DirectoryLoader(PDF_FOLDER, glob="*.pdf", loader_cls=PyPDFLoader)
    docs = list(loader.lazy_load())

    # Add metadata 
    for doc in docs:
        source = doc.metadata.get("source", "")
        doc.metadata["resume_id"] = os.path.basename(source)
        doc.metadata["candidate_name"] = extract_candidate_name(source)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name="resumes_full"
    )

    # Add docs only once
    if vector_store._collection.count() == 0:
        vector_store.add_documents(docs)

    return vector_store
