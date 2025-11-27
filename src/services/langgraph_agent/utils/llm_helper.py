# src/services/langgraph_agent/utils/llm_helper.py

def update_search_query(cur_search_query, prev_search_query):
    return f'{prev_search_query} {cur_search_query}'