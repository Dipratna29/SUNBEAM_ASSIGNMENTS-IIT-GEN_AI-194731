from langchain_community.document_loaders import PyPDFLoader

def extract_text_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return " ".join(d.page_content for d in docs)
