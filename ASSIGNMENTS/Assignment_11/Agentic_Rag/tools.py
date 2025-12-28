from langchain_core.tools import tool
from vector_store import load_vector_store

vector_store = load_vector_store()

@tool
def resume_retrieval_tool(query: str) -> str:
    """
    Search resumes using semantic similarity.
    Always used for resume-related questions.
    """
    results = vector_store.similarity_search(query=query, k=4)

    if not results:
        return "No relevant resume information found."

    response = ""
    for i, doc in enumerate(results, 1):
        response += f"""
Resume {i}
File Name: {doc.metadata.get('resume_id')}
Candidate Name: {doc.metadata.get('candidate_name')}

{doc.page_content}
-------------------------
"""
    return response.strip()
