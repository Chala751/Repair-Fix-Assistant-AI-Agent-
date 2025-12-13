from app.tools.ifixit import search_device, list_guides, get_guide
from app.tools.cleanup import clean_ifixit_guide

def find_device(state):
    """
    Search for a device using the query from the state.
    Safely handles empty results.
    """
    result = search_device(state["query"])
    matches = result.get("matches", [])  
    if matches:
        state["device"] = matches[0]["title"]
        state["device_id"] = matches[0]["id"]  
    else:
        state["device"] = None
        state["device_id"] = None
    return state

def fetch_guide(state):
    """
    Fetch the first guide for the device if it exists.
    Cleans the guide before storing in state.
    """
    if not state.get("device") or not state.get("device_id"):
        return state

    guides = list_guides(state["device"])
    if not guides or "guides" not in guides or len(guides["guides"]) == 0:
        return state

    guide = get_guide(guides["guides"][0]["guideid"])
    state["guide"] = clean_ifixit_guide(guide)
    return state
