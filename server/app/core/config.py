from pydantic import BaseModel
import os

class Settings(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY")

    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    model_temperature: float = float(os.getenv("MODEL_TEMPERATURE", 0))

    tavily_max_results: int = int(os.getenv("TAVILY_MAX_RESULTS", 3))

settings = Settings()
