from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.chat.router import router as chat_router

load_dotenv()

app = FastAPI(
    title="Repair Fix Assistant API",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(chat_router)
