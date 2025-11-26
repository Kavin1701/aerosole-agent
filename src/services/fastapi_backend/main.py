# services/fastapi_backend/main.py

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from src.services.langgraph_agent.main import aerosole_agent

env_path = Path(__file__).resolve().parents[3] / "config" / "fastapi.env"
load_dotenv(dotenv_path=env_path)

PORT = int(os.getenv("PORT"))
HOST = os.getenv("HOST")

fastapi_backend = FastAPI(title="Aerosole Agent API")

@fastapi_backend.get("/")
async def root():
    return {"message": "Aerosole Agent API is running"}

class QueryRequest(BaseModel):
    query: str

@fastapi_backend.post("/api/invoke_agent", tags=["Aerosole Agent"])
async def invoke_agent(req: QueryRequest):
    result = aerosole_agent.invoke({"query": req.query})

    response_str = result["response"]           # <-- string
    response_json = json.loads(response_str)    # <-- convert to dict

    return response_json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.services.fastapi_backend.main:fastapi_backend",
        host=HOST,
        port=PORT,
        reload=True,
    )
