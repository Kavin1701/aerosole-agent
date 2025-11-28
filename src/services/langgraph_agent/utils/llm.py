# src/services/langgraph_agent/utils/llm.py

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq

env_path = Path(__file__).resolve().parents[4] / "config" / "langgraph_agent.env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm(model_name: str = "llama-3.1-8b-instant", temperature: float = 0.1):
    if not GROQ_API_KEY:
        raise ValueError("❌ GROQ_API_KEY is missing. Check .env file.")

    return ChatGroq(
        model=model_name,
        temperature=temperature,
        api_key=GROQ_API_KEY
    )