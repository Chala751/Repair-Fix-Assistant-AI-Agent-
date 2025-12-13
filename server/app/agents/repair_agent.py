from langgraph.graph import StateGraph
from app.agents.state import RepairState
from app.agents.nodes import find_device, fetch_guide


graph = StateGraph(RepairState)


graph.add_node("find_device", find_device)
graph.add_node("fetch_guide", fetch_guide)


graph.set_entry_point("find_device")


graph.add_edge("find_device", "fetch_guide")


repair_agent = graph.compile()
