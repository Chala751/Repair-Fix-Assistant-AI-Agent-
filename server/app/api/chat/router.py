from fastapi import APIRouter
from app.agents.repair_agent import repair_agent
from app.utils.streaming import stream_response

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/stream")
def chat_stream(query: str):
    """
    Stream repair guide step by step.
    Handles errors gracefully and informs the user.
    """
    def generator():
        
        yield "🔍 Searching iFixit for your device...\n"

        try:
            
            result = repair_agent.invoke({"query": query})

            
            guide = result.get("guide")
            if guide is None:
                yield " No guides found for your device.\n"
                return

            
            yield f" Guide found: {guide.get('title')}\n\n"
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
