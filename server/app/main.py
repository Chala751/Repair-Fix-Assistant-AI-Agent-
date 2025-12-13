from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Repair Fix Assistant API",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
