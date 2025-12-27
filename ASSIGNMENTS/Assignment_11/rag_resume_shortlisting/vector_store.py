from collections import defaultdict
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DB_DIR = "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def get_db():
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )

def add_resume(text, resume_id, ai_metadata=None):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)

    metadata = {
        "resume_id": resume_id,
        **(ai_metadata or {})
    }

    db = get_db()
    db.add_texts(
        texts=chunks,
        metadatas=[metadata] * len(chunks)
    )
    db.persist()

def delete_resume(resume_id):
    db = get_db()
    db._collection.delete(where={"resume_id": resume_id})

def list_resumes():
    db = get_db()
    data = db._collection.get(include=["metadatas"])
    if not data or "metadatas" not in data:
        return []
    return sorted(set(m["resume_id"] for m in data["metadatas"]))

def get_resume_metadata(resume_id):
    db = get_db()
    data = db._collection.get(
        where={"resume_id": resume_id},
        include=["metadatas"]
    )
    if data["metadatas"]:
        return data["metadatas"][0]
    return {}

def search_resumes(job_desc, top_n):
    db = get_db()

    # fetch more chunks
    results = db.similarity_search(job_desc, k=top_n * 5)

    resume_scores = defaultdict(int)
    resume_docs = {}

    for doc in results:
        rid = doc.metadata["resume_id"]
        resume_scores[rid] += 1
        resume_docs[rid] = doc

    ranked = sorted(
        resume_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [resume_docs[rid] for rid, _ in ranked[:top_n]]
