from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from tools import resume_retrieval_tool
from config import GROQ_API_KEY

# Initialize LLM
llm = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    temperature=0.3
)


system_message = SystemMessage(content="""
You are an intelligent resume analysis agent.

Rules:
- For resume questions, ALWAYS use resume_retrieval_tool
- Answer only from retrieved content
- If info missing, say: I don't know
- Output format:
  Full Name:
  Resume File Name:
  Resume Summary:
""")

# Create ReAct Agent
agent = create_react_agent(
    llm,
    tools=[resume_retrieval_tool]
)
