from fastapi import APIRouter
from app.agents.repair_agent import repair_agent
from app.utils.streaming import stream_response

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/stream")
def chat_stream(query: str):
    def generator():
        yield "Searching iFixit...\n"
        result = repair_agent.invoke({"query": query})
        yield str(result["guide"])

    return stream_response(generator())
