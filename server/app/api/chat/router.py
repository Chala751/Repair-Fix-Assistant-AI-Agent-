from fastapi import APIRouter
from app.agents.repair_agent import repair_agent, initial_repair_state
from app.utils.streaming import stream_response

from app.tools.ifixit import search_device, list_guides, get_guide
from app.tools.cleanup import clean_ifixit_guide
from urllib.parse import quote

chat_router = APIRouter(prefix="/chat", tags=["Chat"])
debug_router = APIRouter(prefix="/debug", tags=["Debug iFixit"])


@chat_router.post("/stream")
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


@debug_router.get("/device-guides")
def device_guides(device: str):
    """
    Debug endpoint to inspect raw CATEGORY guides.
    """
    try:
        guides = list_guides(device)

        cleaned = []
        for g in guides:
            guide_id = g.get("guideid") or g.get("wikiid")
            if not guide_id:
                continue  # skip non-guides

            cleaned.append({
                "id": guide_id,
                "title": g.get("title"),
                "type": "guide" if "guideid" in g else "wiki"
            })

        return {
            "device": device,
            "guide_count": len(cleaned),
            "guides": cleaned
        }

    except Exception as e:
        return {"error": str(e)}
