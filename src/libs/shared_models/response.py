# src/libs/shared_models/response.py
from pydantic import BaseModel, Field

class Response(BaseModel):
    result_from: str = "default"
    result: dict = Field(default_factory=dict)
    completion_status: str = "incomplete"
