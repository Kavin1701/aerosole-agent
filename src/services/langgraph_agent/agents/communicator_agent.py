# src/services/langgraph_agent/agents/communicator_agent.py

import json
from src.services.langgraph_agent.models.state import State
from src.libs.shared_utils.logger import logger

def communicator_node(state: State) -> State:
    logger.info("[COMMUNICATOR_NODE] Start >>>>>> ")

    # Ensure previous intent is "search"
    if len(state.intent) >= 2 and state.intent[-2] == "search":
        
        # Build JSON response
        response = {
            "status": "success",
            "results_count": len(state.matched_products),
            "results": []
        }

        for title, pdata in state.matched_products.items():
            response["results"].append({
                "title": title,
                "subtitle": pdata.get("subtitle"),
                "short_description": pdata.get("short_description"),
                "style_description": pdata.get("style_description"),
                "details": pdata.get("details"),
                "price": pdata.get("price"),
                "num_colors": pdata.get("num_colors")
            })

        # Convert to JSON string for REST response
        state.response = json.dumps(response, indent=2)

        logger.info("[COMMUNICATOR_NODE] Reply JSON built.")
    
    else:
        # If somehow the intent is not search, fallback
        state.response = json.dumps({
            "status": "no-search-intent",
            "message": "No valid search intent detected."
        }, indent=2)

    state.query = "end the agent call"
    return state
