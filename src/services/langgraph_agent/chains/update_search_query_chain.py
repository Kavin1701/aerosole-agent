from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from src.services.langgraph_agent.utils.llm import get_llm

class UpdatedQuery(BaseModel):
    updated_search_query: str


SEARCH_UPDATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You update product search queries based only on explicit user instructions.
RULES:
- For REMOVALS: If the user says "don't want", "exclude", "remove", or similar for a specific attribute (e.g., "skateboarding"), delete it from the query—do NOT add negatives like "-skateboarding".
- For ADDITIONS/REPLACEMENTS: If the user says "I need/want [new attribute]" or "for [purpose/context]", explicitly add or replace with those details as a short, natural phrase (e.g., "casual shoe for outings" → add "casual shoe for outings" to preserve semantics for embeddings).
- Do NOT guess, infer, or add unrelated details—only use words/phrases directly from the user's message.
- Modify only when the user clearly adds, removes, replaces, or specifies something—otherwise, leave unchanged.
- If vague or unclear, do nothing.
- The final result must be a concise keyword phrase: Combine terms naturally (e.g., "low top casual shoe for rainy outings")—avoid full sentences, but keep short connectors like "for" if they appear in the user's explicit addition.
- No explanation, no commentary, no reasoning.
STRICTLY NO HALLUCINATIONS:
- Only incorporate direct user phrasing; do not reword for "better semantics."
Return a JSON object matching:
{{
  "updated_search_query": "<final refined query>"
}}
"""),
    ("human", """
Previous Search Query: "{prev_search_query}"
User Message: "{cur_search_query}"
Return ONLY the refined search query as JSON.
""")
])

# ---------------- Chain ----------------

llm_model = get_llm()
structured_llm = llm_model.with_structured_output(UpdatedQuery)
chain = SEARCH_UPDATION_PROMPT | structured_llm