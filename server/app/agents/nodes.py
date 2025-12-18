from app.tools.ifixit import get_ifixit_tools
from app.tools.web_search import web_search
from app.tools.cleanup import format_final_answer

ifixit = get_ifixit_tools()



async def normalize_query(state):
    state.setdefault("tool_status", []).append("🔍 Normalizing query")
    state["ifixit_device"] = state.get("query", "")
    return state

async def search_device(state):
    state.setdefault("tool_status", []).append("📱 Searching device on iFixit")
    result = await ifixit.search_devices(state.get("ifixit_device", ""))
    if not result:
        state["ifixit_search_result"] = None
    else:
        state["ifixit_search_result"] = result
    return state

async def list_guides(state):
    state.setdefault("tool_status", []).append("📚 Listing repair guides")
    guides = await ifixit.list_guides(state.get("ifixit_device", ""))
    if guides:
        state["available_guides"] = guides.get("guides", [])
    else:
        state["available_guides"] = []
    return state

async def select_guide(state):
    state.setdefault("tool_status", []).append("✅ Selecting best guide")
    guides = state.get("available_guides", [])
    if guides:
        state["selected_guide"] = guides[0]
    else:
        state["selected_guide"] = None
    return state

async def fetch_guide(state):
    state.setdefault("tool_status", []).append("🛠 Fetching repair steps")
    guide = state.get("selected_guide")
    if guide:
        steps = await ifixit.fetch_repair_guide(guide.get("guideid"))
        state["repair_steps"] = steps if steps else {}
    else:
        state["repair_steps"] = {}
    return state


async def fallback_search(state):
    state.setdefault("tool_status", []).append("🌐 Using web fallback")
    
    # Correctly await the async function
    state["final_response"] = await web_search(state.get("query", ""))
    state["fallback_used"] = True
    return state

async def format_response(state):
    state.setdefault("tool_status", []).append("📦 Formatting response")
    state["repair_steps"] = state.get("repair_steps") or {}
    state["final_response"] = format_final_answer(state)
    return state
