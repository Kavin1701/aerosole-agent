# src/services/langgraph_agent/models/state.py

from dataclasses import dataclass, field, fields
from typing import List, Optional, Tuple
from src.libs.shared_models.response import Response

@dataclass
class State:
    query: str = ""
    intent: Optional[List[str]] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)

    search_query: str = ''
    matched_products: Optional[dict] = None
    response: Response = field(default_factory=Response)

    # ------------------------------
    # Safe dict -> State conversion
    # ------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> "State":
        """
        Safely create a State object from a dictionary.
        Ignores keys that are not part of State.
        Handles nested Response if present.
        """
        state_fields = {f.name for f in fields(cls)}
        filtered_data = {}

        for k, v in data.items():
            if k in state_fields:
                # If field is response and value is dict, construct Response
                if k == "response" and isinstance(v, dict):
                    filtered_data[k] = Response(**v)
                else:
                    filtered_data[k] = v

        return cls(**filtered_data)