from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import *

def should_fallback(state):
    if not state.get("selected_guide"):
        return "fallback"
    return "format"

def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("normalize", normalize_query)
    graph.add_node("search", search_device)
    graph.add_node("guides", list_guides)
    graph.add_node("select", select_guide)
    graph.add_node("fetch", fetch_guide)
    graph.add_node("fallback", fallback_search)
    graph.add_node("format", format_response)

    graph.set_entry_point("normalize")

    graph.add_edge("normalize", "search")
    graph.add_edge("search", "guides")
    graph.add_edge("guides", "select")

    graph.add_conditional_edges(
        "select",
        should_fallback,
        {
            "fallback": "fallback",
            "format": "fetch"
        }
    )

    graph.add_edge("fetch", "format")
    graph.add_edge("fallback", "format")
    graph.add_edge("format", END)

    return graph.compile()

repair_agent = build_agent()
