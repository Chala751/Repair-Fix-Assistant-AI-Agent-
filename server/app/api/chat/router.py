from fastapi import APIRouter
from app.agents.repair_agent import repair_agent, initial_repair_state
from app.utils.streaming import stream_response

from app.tools.ifixit import search_device, list_guides, get_guide
from app.tools.cleanup import clean_ifixit_guide
from urllib.parse import quote

router = APIRouter(prefix="/chat", tags=["Chat"])
router = APIRouter(prefix="/debug", tags=["Debug iFixit"])

@router.post("/stream")
def chat_stream(query: str):
    """Stream repair guide step by step."""
    def generator():
        yield "🔍 Searching iFixit for your device...\n"

        try:
            result = repair_agent.invoke(initial_repair_state(query))

            guide = result.get("guide")
            if not guide:
                yield " No guides found for your device.\n"
                return

            yield f"Guide found: {guide.get('title')}\n\n"
            yield f"{guide.get('introduction')}\n\n"

            for step in guide.get("steps", []):
                yield f"Step: {step.get('title')}\n"
                yield f"{step.get('text')}\n"
                images = step.get("images", [])
                if images:
                    yield f"Images: {', '.join(images)}\n"
                yield "\n"

        except Exception as e:
            yield f" An error occurred: {str(e)}\n"

    return stream_response(generator())


@router.get("/device-guides")
def device_guides(query: str):
    """
    Search iFixit for a device and retrieve its guides.
    Returns guide titles and URLs for inspection.
    """
    try:
        
        device_title = search_device(query)
        if not device_title:
            return {"error": "No matching device found on iFixit."}

        
        raw_guides = list_guides(device_title)
        if not raw_guides:
            device_url = f"https://www.ifixit.com/Device/{quote(device_title)}"
            return {
                "device": device_title,
                "guides": [],
                "info": f"No guides found. Check iFixit page: {device_url}"
            }

        
        guides_list = []
        for guide in raw_guides:
            guide_id = guide.get("wikiid") or guide.get("guideid")
            if not guide_id:
                continue
            raw_guide_data = get_guide(guide_id)
            cleaned = clean_ifixit_guide(raw_guide_data)
            guides_list.append(cleaned)

        return {
            "device": device_title,
            "guides": guides_list
        }

    except Exception as e:
        return {"error": str(e)}