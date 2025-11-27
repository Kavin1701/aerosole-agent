# src/services/langgraph_agent/graph.py

import pandas as pd
from pathlib import Path
from src.services.vectorization.tf_idf_retriever import TfidfRetriever
from langgraph.graph import StateGraph, END, START
from src.services.langgraph_agent.models.state import State
from src.services.langgraph_agent.agents.communicator_agent import communicator_node
from src.services.langgraph_agent.agents.discovery_agent import search_node
from src.services.langgraph_agent.orchestrator import orchestrator_node, controller_node, route_from_controller
from langgraph.checkpoint.memory import MemorySaver

shoes_master = Path(__file__).resolve().parents[3] / "data" / "vans_shoes_master.csv"
df = pd.read_csv(shoes_master)
tfidf_retriever = TfidfRetriever(df=df)

graph = StateGraph(State)
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("controller", controller_node)
graph.add_node("search", lambda s: search_node(s, df, tfidf_retriever))
graph.add_node("communicator", communicator_node)

graph.add_conditional_edges(
    "controller",
    route_from_controller,
    {
        "search": "search",
        "communicate": "communicator",
        "end": END
    }
)

graph.set_entry_point("orchestrator")
graph.add_edge("orchestrator", "controller")
graph.add_edge("communicator", "orchestrator")
graph.add_edge("search", "orchestrator")

checkpointer = MemorySaver()
aerosole_agent = graph.compile()
# result = aerosole_agent.invoke({"query": "search me casual shoes"})
# print(result['response'])