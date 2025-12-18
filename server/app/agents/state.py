from typing import TypedDict, Optional, List, Dict

class AgentState(TypedDict):
    query: str
    normalized_query: Optional[str]
    ifixit_device: Optional[str]
    available_guides: Optional[List[Dict]]
    selected_guide: Optional[Dict]
    repair_steps: Optional[Dict]
    fallback_used: bool
    final_response: Optional[str]
    tool_status: List[str]
