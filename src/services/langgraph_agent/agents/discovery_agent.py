# src/services/langgraph_agent/agents/discovery_agent.py

import pandas as pd
from langgraph.graph import StateGraph, END
from src.services.langgraph_agent.models.state import State
from langgraph.types import Command
from src.libs.shared_utils.logger import logger
from src.services.vectorization.tf_idf_retriever import TfidfRetriever
retriever = TfidfRetriever()

def search_node(state: State, df: pd.DataFrame) -> State:
    logger.info("[SEARCH_NODE] Start: >>>>>> ")

    query = state.query

    # Run TF-IDF retrieval
    retrieved = retriever(query, top_k=5)
    retrieved_titles = [r["title"] for r in retrieved]

    # Filter df
    matched_df = df[df["title"].isin(retrieved_titles)]

    # Convert to dict keyed by title
    state.matched_products = {
        row["title"]: {
            "subtitle": row["subtitle"],
            "short_description": row["short_description"],
            "style_description": row["style_description"],
            "details": row["details"],
            "price": row["price"],
            "num_colors": row["num_colors"]
        }
        for _, row in matched_df.iterrows()
    }

    logger.info("[SEARCH_NODE] Matched products: %s", state.matched_products)

    state.query = "communicate to the user"
    return state

