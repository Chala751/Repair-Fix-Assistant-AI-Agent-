from app.tools.ifixit import get_ifixit_tools
from app.tools.web_search import web_search
from app.tools.cleanup import format_final_answer

ifixit = get_ifixit_tools()

async def normalize_query(state):
    state["tool_status"].append("🔍 Normalizing query")
    state["ifixit_device"] = state["query"]
    return state

async def search_device(state):
    state["tool_status"].append("📱 Searching device on iFixit")
    result = await ifixit.search_devices(state["ifixit_device"])
    if not result:
        return state
    return state

async def list_guides(state):
    state["tool_status"].append("📚 Listing repair guides")
    guides = await ifixit.list_guides(state["ifixit_device"])
    if guides:
        state["available_guides"] = guides["guides"]
    return state

async def select_guide(state):
    state["tool_status"].append("✅ Selecting best guide")
    guides = state.get("available_guides", [])
    if guides:
        state["selected_guide"] = guides[0]
    return state

async def fetch_guide(state):
    state["tool_status"].append("🛠 Fetching repair steps")
    guide = state["selected_guide"]
    if guide:
        state["repair_steps"] = await ifixit.fetch_repair_guide(guide["guideid"])
    return state

async def fallback_search(state):
    state["tool_status"].append("🌐 Using web fallback")
    state["final_response"] = await web_search(state["query"])
    state["fallback_used"] = True
    return state

async def format_response(state):
    state["tool_status"].append("📦 Formatting response")
    state["final_response"] = format_final_answer(state)
    return state
