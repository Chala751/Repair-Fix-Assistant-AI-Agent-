from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # API Keys
    tavily_api_key: str = Field(..., env="TAVILY_API_KEY")
    gemini_api_key: str | None = Field(default=None, env="GEMINI_API_KEY")

    # App config
    server_host: str = Field(default="0.0.0.0", env="SERVER_HOST")
    server_port: int = Field(default=8000, env="SERVER_PORT")

    # Search config
    tavily_max_results: int = Field(default=3, env="TAVILY_MAX_RESULTS")

    class Config:
        env_file = ".env"
        extra = "ignore"   # ignore unused env vars safely


settings = Settings()
