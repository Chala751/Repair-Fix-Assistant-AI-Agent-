from app.tools.ifixit import search_device, list_guides, get_guide
from app.tools.cleanup import clean_ifixit_guide

def find_device(state):
    result = search_device(state["query"])
    if result:
        state["device"] = result[0]["title"]
    return state

def fetch_guide(state):
    if not state.get("device"):
        return state

    guides = list_guides(state["device"])
    if not guides:
        return state

    guide = get_guide(guides[0]["guideid"])
    state["guide"] = clean_ifixit_guide(guide)
    return state
