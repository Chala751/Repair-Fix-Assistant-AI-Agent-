from typing import TypedDict, Optional

class RepairState(TypedDict):
    query: str
    device_title: Optional[str]
    device_slug: Optional[str]
    guide: Optional[dict]
    fallback_used: bool
