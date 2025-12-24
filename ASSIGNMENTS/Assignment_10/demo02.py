from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st  
code_text = """
Artificial Intelligence (AI) is transforming modern technology.

It enables machines to learn from data, recognize patterns, and make decisions with minimal human intervention.

Key applications of AI include:
- Natural Language Processing (chatbots, translators)
- Computer Vision (face recognition, medical imaging)
- Recommendation Systems (Netflix, Amazon)

AI is widely used in industries such as healthcare, finance, agriculture, and education.

However, AI also raises ethical concerns including data privacy, bias, and job displacement.
Addressing these challenges is crucial for responsible AI development.
"""

code_splitter = RecursiveCharacterTextSplitter.from_language(
    language="python",
    chunk_size=1000,
    chunk_overlap=100
)

docs = code_splitter.create_documents([code_text])

for i, doc in enumerate(docs):
    st.write(f"### Code Chunk {i+1}")
    st.write(doc.page_content)