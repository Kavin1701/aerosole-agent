from typing import List
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from src.services.langgraph_agent.utils.llm import get_llm


# ---------------- Pydantic Output Model ----------------

class EntityResponse(BaseModel):
    entities: List[str]


# ---------------- Prompt ----------------

ENTITY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Extract key entities from a user query. Entities can be:
- Objects
- Places
- Categories
- Concepts
- Multi-word phrases

### STRICT OUTPUT FORMAT

Return ONLY valid JSON:

{{
  "entities": [
    "entity1",
    "entity2"
  ]
}}
"""
    ),
    (
        "human",
        "Query: {search_query}\nReturn JSON only."
    )
])



# ---------------- Chain ----------------

llm_model = get_llm()
structured_llm = llm_model.with_structured_output(EntityResponse)
chain = ENTITY_PROMPT | structured_llm
