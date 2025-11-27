# src/services/langgraph_agent/agents/discovery_agent.py

import pandas as pd
from langgraph.graph import StateGraph, END
from src.services.langgraph_agent.models.state import State
from langgraph.types import Command
from src.libs.shared_utils.logger import logger
from src.services.vectorization.tf_idf_retriever import TfidfRetriever
from src.services.langgraph_agent.utils.llm_helper import update_search_query

def search_node(state: State, df: pd.DataFrame, retriever: TfidfRetriever) -> State:
    logger.info("[SEARCH_NODE] Start: >>>>>> ")

    cur_query = state.query
    prev_query = state.search_query

    query = update_search_query(cur_query, prev_query)
    logger.info(f" <QUERY>: {query}")
    
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
            "num_colors": row["num_colors"],
            "img": "https://assets.vans.com/images/t_img/c_fill,g_center,f_auto,h_550,e_unsharp_mask:100,w_440/dpr_2.0/v1750722159/VN000DARBKA-HERO/Sk8Hi-GORETEX-Insulated-Shoe.jpg",
        }
        for _, row in matched_df.iterrows()
    }

    logger.debug("[SEARCH_NODE] Matched products: %s", state.matched_products)

    state.search_query = query
    state.query = "communicate to the user"
    return state

