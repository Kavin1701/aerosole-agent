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
     """You are an AI assistant that extracts key descriptive entities ONLY from the product text that directly correspond to specific elements explicitly mentioned in the user's query. 

Do not include any entities that are not directly referenced or synonymous with phrases in the query. For example, if the query mentions 'padded collar for support', only extract that if present in the product context; ignore unrelated features like colors, brands, or other specs.

Focus on meaningful, concise multi-word phrases that combine for better description (e.g., 'padded collar for support' instead of separate words), but only if they match query elements.

Ignore generic terms like 'shoes' unless combined meaningfully with query specifics. Do not hallucinate or imply anything beyond exact or near-exact matches in the product context.

Assign confidence: 1.0 for exact phrase matches, 0.9-0.7 for strong synonyms or partial matches present in both, below 0.7 if not sufficiently direct—exclude if below 0.7.

Respond strictly in JSON in the format:
{{"entities":[{{"entity":"string","confidence":float}}]}}. 

If no matches, return empty list: {{"entities":[]}}."""),
    ("human",
     """
User Query: {search_query}

Product Context:
{product_context}

Return JSON only, do not include any explanatory text.
""")
])


# ---------------- Chain ----------------

llm_model = get_llm()
structured_llm = llm_model.with_structured_output(EntityResponse)
chain = ENTITY_PROMPT | structured_llm