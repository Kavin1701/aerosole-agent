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
Extract meaningful standalone entities from the user query. 
Break longer compound phrases into smaller meaningful parts if needed.

Entities may include:
- Attributes (ex: "aesthetic", "lightweight")
- Styles (ex: "checkerboard", "retro design")
- Product types (ex: "low top shoe", "running shoes")
- Materials (ex: "leather", "canvas")
- Concepts or categories

Rules:
- Prefer concise entities that represent meaning on their own.
- Avoid generic filler words such as "with", "for", "and", "the".
- Do NOT include numbers unless they indicate size, model, or SKU.
- Do NOT include stopwords or repeated phrases.
- Maintain multi-word entities only if they represent a known concept 
  (e.g., "low top shoe", "mountain bike", "air cushion sole").

### OUTPUT FORMAT (STRICT)

Return ONLY valid JSON:

{{
  "entities": [
    "entity1",
    "entity2",
    "entity3"
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
