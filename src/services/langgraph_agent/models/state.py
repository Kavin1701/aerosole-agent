# src/services/langgraph_agent/models/state.py

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

@dataclass
class State:
    query: str = ""   # User's raw input text
    intent: Optional[List[str]] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)
    matched_products: Optional[dict] = None
    response: Optional[str] = None
