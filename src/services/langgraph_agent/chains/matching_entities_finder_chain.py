from typing import List
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from src.services.langgraph_agent.utils.llm import get_llm

# ---------------- Pydantic Output Model ----------------

class EntityMatch(BaseModel):
    entity: str
    confidence: float


class EntityResponse(BaseModel):
    entities: List[EntityMatch]


# ---------------- Prompt ----------------

ENTITY_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     """
You extract meaningful product-related entities from the user query ONLY if they appear in (or are strong synonyms of) concepts found in the product context.

---

### ENTITY RULES

- Extract only meaningful product attributes, features, types, or variations.
- Keep phrases concise: **2–4 words max**.
- Avoid long or sentence-like entities.
- Do NOT return multiple versions of the same meaning.
- If an entity appears with **confidence 1.0**, do NOT return weaker variations of the same meaning.
- Maximum **3 unique entities**.

---

### CONFIDENCE RULES

| Match Type | Confidence |
|------------|------------|
| Exact phrase match in both query & context | **1.0** |
| Minor variation (plural, ordering) | **0.9** |
| Strong synonym | **0.75–0.89** |
| Anything weaker → **exclude** |

---

### OUTPUT FORMAT (STRICT)

Return ONLY valid JSON in this format:

{{
  "entities": [
    {{
      "entity": "string",
      "confidence": float
    }}
  ]
}}

If no valid match exists, return:

{{
  "entities": []
}}
"""),
    ("human",
     """
User Query: {search_query}

Product Context:
{product_context}

Return JSON only.
""")
])

# ---------------- Chain ----------------

llm_model = get_llm()
structured_llm = llm_model.with_structured_output(EntityResponse)
chain = ENTITY_PROMPT | structured_llm
