# src/services/langgraph_agent/orchestrator.py

from langgraph.graph import StateGraph, END
from src.services.langgraph_agent.models.state import State
from langgraph.types import Command
from src.libs.shared_utils.logger import logger

def orchestrator_node(state: State) -> State:
    logger.info("[ORCHESTRATOR_NODE] Start >>>>> ")

    query = state.query.lower()

    if query == "end":
        state.intent.append("end")
        state.messages.append("Intent classified as END.")
        logger.info("[ORCHESTRATOR_NODE] Intent classified as END for query='%s'", query)

    # elif any(word in query for word in ["clear", "refresh"]):
    #     state.intent.append("clear_search")
    #     state.messages.append("Intent classified as CLEAR_SEARCH")
    #     logger.info

    elif any(word in query for word in ["communicate"]):
        state.intent.append("communicate")
        state.messages.append("Intent classified as COMMUNICATE.")
        logger.info("[ORCHESTRATOR_NODE] Intent classified as COMMUNICATE for query='%s'", query)

    else:
        state.intent.append("search")
        state.messages.append("Intent classified as SEARCH.")
        logger.info("[ORCHESTRATOR_NODE] Intent classified as SEARCH for query='%s'", query)

    logger.debug("[ORCHESTRATOR_NODE] EXIT: %s", state)
    return state


def controller_node(state: State) -> State:
    logger.info("[CONTROLLER] Pass-through >>>>>> ")
    return state

def route_from_controller(state: State) -> str:
    logger.debug("[CONTROLLER] Routing decision, current state: %s", state)
    return state.intent[-1]  # safe now
