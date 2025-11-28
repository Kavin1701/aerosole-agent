# src/services/langgraph_agent/agents/discovery_agent.py

import pandas as pd
from langgraph.graph import StateGraph, END
from src.services.langgraph_agent.models.state import State
from langgraph.types import Command
from src.libs.shared_utils.logger import logger
from src.services.vectorization.tf_idf_retriever import TfidfRetriever
from src.services.langgraph_agent.utils.llm_helper import update_search_query

def search_node(state: State, df1: pd.DataFrame, df2: pd.DataFrame, retriever: TfidfRetriever) -> State:
    logger.info("[SEARCH_NODE] Start: >>>>>> ")

    cur_query = state.query
    prev_query = state.search_query

    query = update_search_query(cur_query, prev_query)
    logger.info(f" <QUERY>: {query}")
    
    # Run TF-IDF retrieval
    retrieved = retriever(query, top_k=5)
    retrieved_titles = [r["title"] for r in retrieved]

    # Filter df
    matched_df = df1[df1["title"].isin(retrieved_titles)]

    # Convert to dict keyed by title
    state.matched_products = {
        row["title"]: {
            "subtitle": row["subtitle"],
            "short_description": row["short_description"],
            "style_description": row["style_description"],
            "details": row["details"],
            "price": row["price"],
            "num_colors": row["num_colors"],
            "img": df2[df2['title_x'] == row['title']].head(1)['img'].iloc[0],
        }
        for _, row in matched_df.iterrows()
    }

    logger.debug("[SEARCH_NODE] Matched products: %s", state.matched_products)

    state.search_query = query
    state.query = "communicate to the user"
    return state

# def clear_search_node(state: State) -> State:
#     logger.info("[CLEAR_SEARCH_NODE] Start: >>>>>> ")

#     state.