from app.tools.ifixit import search_device, list_guides, get_guide
from app.tools.cleanup import clean_ifixit_guide

FORBIDDEN_WORDS = [
    "replacement", "repair", "issues", "fix",
    "problem", "screen", "battery", "speaker"
]


def is_valid_device_slug(slug: str) -> bool:
    slug_lower = slug.lower()
    return not any(word in slug_lower for word in FORBIDDEN_WORDS)

def find_device(state):
    device = search_device(state["query"])
    if not device:
        return state

    title = device.get("title")
    if not title:
        return state

    slug = title.replace(" ", "_")

    # 🛑 HARD STOP
    if not is_valid_device_slug(slug):
        state["fallback_used"] = True
        return state

    state["device_title"] = title
    state["device_slug"] = slug
    return state


def fetch_guide(state):
    slug = state.get("device_slug")
    if not slug:
        return state

    guides = list_guides(slug)
    if not guides:
        return state

    intent = state["query"].lower()

    selected_id = None
    fallback_id = None

    for g in guides:
        guide_id = g.get("guideid")

        # ✅ skip wikis
        if not guide_id:
            continue

        # normalize guide_id (string → int)
        try:
            guide_id = int(guide_id)
        except Exception:
            continue

        title = (g.get("title") or "").lower()

        # 🎯 intent match
        if "screen" in intent and "screen" in title:
            selected_id = guide_id
            break

        if "battery" in intent and "battery" in title:
            selected_id = guide_id
            break

        if "speaker" in intent and "speaker" in title:
            selected_id = guide_id
            break

        # remember first valid guide
        if not fallback_id:
            fallback_id = guide_id

    # fallback if no intent match
    if not selected_id:
        selected_id = fallback_id

    if not selected_id:
        return state

    guide = get_guide(selected_id)
    state["guide"] = clean_ifixit_guide(guide)
    return state
