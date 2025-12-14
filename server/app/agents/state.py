from typing import TypedDict, Optional

class RepairState(TypedDict):
    query: str
    device: Optional[str]
    device_wikiid: Optional[int]
    guide: Optional[dict]
    fallback_used: bool
