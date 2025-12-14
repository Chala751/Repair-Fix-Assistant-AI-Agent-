from app.tools.ifixit import search_device, list_guides, get_guide
from app.tools.cleanup import clean_ifixit_guide

def find_device(state):
    """Search for a device using the query."""
    device = search_device(state["query"])
    if device:
        state["device"] = device["title"]
        state["device_wikiid"] = device["wikiid"]
    else:
        state["device"] = None
        state["device_wikiid"] = None
    return state

def fetch_guide(state):
    """Fetch first guide for the device and clean it."""
    if not state.get("device"):
        return state

    guides = list_guides(state["device"])
    if not guides:
        return state

    guide_id = guides[0].get("guideid")
    if not guide_id:
        return state

    guide = get_guide(guide_id)
    state["guide"] = clean_ifixit_guide(guide)
    return state
