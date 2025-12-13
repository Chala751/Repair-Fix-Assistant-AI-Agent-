from sse_starlette.sse import EventSourceResponse
from typing import Generator

def stream_response(generator: Generator[str, None, None]):
    def event_generator():
        for chunk in generator:
            yield {"data": chunk}
    return EventSourceResponse(event_generator())
