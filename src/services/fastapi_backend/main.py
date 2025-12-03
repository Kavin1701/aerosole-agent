# services/fastapi_backend/main.py

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from src.services.langgraph_agent.graph import aerosole_agent
from src.services.langgraph_agent.main import run_graph
from src.libs.shared_models.response import Response as ResponseSchema
from fastapi.middleware.cors import CORSMiddleware

cache = {}

env_path = Path(__file__).resolve().parents[3] / "config" / "fastapi.env"
load_dotenv(dotenv_path=env_path)

PORT = int(os.getenv("PORT"))
HOST = os.getenv("HOST")

fastapi_backend = FastAPI(title="Aerosole Agent API")

fastapi_backend.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # you can allow all if needed
    allow_headers=["*"],
)

@fastapi_backend.get("/")
async def root():
    return {"message": "Aerosole Agent API is running"}

class QueryRequest(BaseModel):
    query: str


@fastapi_backend.post("/api/invoke_agent", response_model=ResponseSchema, tags=["Aerosole Agent"])
async def invoke_agent(req: QueryRequest):
    thread_id = "12345"
    user_query = req.query
    state = run_graph(thread_id, user_query, aerosole_agent, cache)
    state.response.user_query = user_query
    return state.response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.services.fastapi_backend.main:fastapi_backend",
        host=HOST,
        port=PORT,
        reload=False,
    )
