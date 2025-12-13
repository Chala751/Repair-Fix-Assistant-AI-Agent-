from langchain_tavily import TavilySearchResults
from app.core.config import settings

search_tool = TavilySearchResults(
    max_results=settings.tavily_max_results,
    api_key=settings.tavily_api_key
)
