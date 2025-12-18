from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

api_key = os.getenv("GROQ_API_KEY")
print("API Key:", api_key)
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)



user_input = input("You: ")

result = llm.stream(user_input)
# for chunk in result:
#     print(chunk.content, end="")
result = llm.invoke(user_input)
print("AI: ", result.content)