from typing import TypedDict, Optional

class RepairState(TypedDict):
    query: str
    device: Optional[str]
    guide: Optional[dict]
    fallback_used: bool
