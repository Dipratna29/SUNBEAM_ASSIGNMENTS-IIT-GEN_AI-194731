from langchain_community.document_loaders import PyPDFLoader

def extract_candidate_name(pdf_path):
    """
    Extract candidate name from first page of resume.
    Assumes name appears in first 2 words.
    """
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        words = pages[0].page_content.strip().split()
        return " ".join(words[:2])
    except:
        return "Unknown"
