# src/services/langgraph_agent/main.py

from src.services.langgraph_agent.models.state import State

def run_graph(thread_id, query, agent, cache):
    config = {"configurable": {"thread_id": thread_id}}

    if thread_id in cache:
        # Update only the query of the cached state
        state = cache[thread_id]
        state.query = query
    else:
        # Create new state
        state = State(query=query)

    # Invoke agent
    result = agent.invoke(state, config=config)

    # Update cached state with result, preserving old fields not in result
    updated_state = State.from_dict(result)
    cache[thread_id] = updated_state

    return updated_state