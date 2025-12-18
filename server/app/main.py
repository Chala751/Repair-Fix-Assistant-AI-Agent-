from fastapi import FastAPI
from app.api.chat.router import router as chat_router

app = FastAPI(title="Repair Fix Assistant")

app.include_router(chat_router)

@app.get("/")
def health():
    return {"status": "ok"}
