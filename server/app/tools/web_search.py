import asyncio
from tavily import TavilyClient
from app.core.config import settings

client = TavilyClient(api_key=settings.tavily_api_key)

async def web_search(query: str):
  
    results = await asyncio.to_thread(
        client.search, query, max_results=settings.tavily_max_results
    )

    if not results:
        return "No web results found."

   
    formatted_results = []
    for r in results:
        if isinstance(r, dict):
            formatted_results.append(f"{r.get('title', 'No title')}: {r.get('url', 'No URL')}")
        else:
           
            formatted_results.append(r)
    
    return "\n".join(formatted_results)
