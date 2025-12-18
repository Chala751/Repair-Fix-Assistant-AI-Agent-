from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json, asyncio

from app.agents.repair_agent import repair_agent

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/stream")
async def chat_stream(req: ChatRequest):

    async def generator():
        state = {
            "query": req.message,
            "normalized_query": None,
            "ifixit_device": None,
            "available_guides": None,
            "selected_guide": None,
            "repair_steps": None,
            "fallback_used": False,
            "final_response": None,
            "tool_status": []
        }

        async for event in repair_agent.astream(state):
            node = list(event.values())[0]

            if node.get("tool_status"):
                yield f"data: {json.dumps({'type':'status','content':node['tool_status'][-1]})}\n\n"

        yield f"data: {json.dumps({'type':'response','content':state['final_response']})}\n\n"
        yield f"data: {json.dumps({'type':'done'})}\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")
