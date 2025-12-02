# src/services/langgraph_agent/agents/discovery_agent.py

import pandas as pd
from langgraph.graph import StateGraph, END
from src.services.langgraph_agent.models.state import State
from langgraph.types import Command
from src.libs.shared_utils.logger import logger
# from src.services.vectorization.tf_idf_retriever import TfidfRetriever
from src.services.vectorization.vector_retriever import VectorRetriever
from src.services.langgraph_agent.utils.llm_helper import update_search_query, find_matched_entities

def search_node(state: State, df1: pd.DataFrame, df2: pd.DataFrame, retriever: VectorRetriever) -> State:
    logger.info("[SEARCH_NODE] Start: >>>>>> ")

    cur_query = state.query
    prev_query = state.search_query

    query = update_search_query(cur_query, prev_query)
    logger.info(f" <QUERY>: {query}")
    
    # Run similarity search and sort by confidence
    retrieved = sorted(retriever(query, top_k=5), key=lambda r: r["confidence"], reverse=True)

    retrieved_titles = [r["title"] for r in retrieved]
    retrieved_scores = [r["confidence"] for r in retrieved]
    logger.info(f"{retrieved_titles} - {retrieved_scores}")

    # Filter df only for matched titles
    matched_df = df1[df1["title"].isin(retrieved_titles)]

    # Map title → confidence
    confidence_map = {item["title"]: item["confidence"] for item in retrieved}

    # Convert to dict keyed by title in order of confidence
    state.matched_products = {
        title: {
            "subtitle": row["subtitle"],
            "short_description": row["short_description"],
            "style_description": row["style_description"],
            "details": row["details"],
            "price": row["price"],
            "num_colors": row["num_colors"],
            "img": df2[df2['title_x'] == title].head(1)['img'].iloc[0],
            "confidence": confidence_map.get(title),
            "entities": find_matched_entities(
                query,
                f'{title} {row["subtitle"]} {row["short_description"]} {row["style_description"]} {row["details"]}'
            )
        }
        for title, row in matched_df.set_index("title").loc[retrieved_titles].iterrows()
    }



    logger.debug("[SEARCH_NODE] Sorted matched products: %s", state.matched_products)

    state.search_query = query
    state.query = "communicate to the user"
    return state


# def clear_search_node(state: State) -> State:
#     logger.info("[CLEAR_SEARCH_NODE] Start: >>>>>> ")

#     state.