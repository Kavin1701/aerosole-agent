# src/services/langgraph_agent/agents/communicator_agent.py

import json
from src.services.langgraph_agent.models.state import State
from src.libs.shared_utils.logger import logger

def communicator_node(state: State) -> State:
    logger.info("[COMMUNICATOR_NODE] Start >>>>>> ")

    if len(state.intent) >= 2 and state.intent[-2] == "search":

        result_payload = {
            "current_search_query": state.search_query,
            "product_count": len(state.matched_products),
            "products": [
                {
                    "title": title,
                    "subtitle": pdata.get("subtitle"),
                    "short_description": pdata.get("short_description"),
                    "style_description": pdata.get("style_description"),
                    "details": pdata.get("details"),
                    "price": pdata.get("price"),
                    "num_colors": pdata.get("num_colors"),
                    "img": pdata.get("img"),
                    "entities": pdata.get("entities"),
                    "confidence": pdata.get("confidence")
                }
                for title, pdata in state.matched_products.items()
            ]
        }

        state.response.result = result_payload
        state.response.result_from = "search_products"
        state.response.completion_status = 'success'

        logger.info("[COMMUNICATOR_NODE] JSON structure created.")

    else:
        state.response.result = {
            "status": "no-search-intent",
            "message": "No valid search intent detected."
        }
        state.response.result_from = "agent"
        state.response.completion_status = 'error'

    state.query = "end"
    return state
