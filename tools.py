import json
from typing import List, Dict, Any
from langchain.tools import tool
from ddgs import DDGS


@tool
def search_web(query: str, max_results: int = 5) -> str:
    """Search the web for current information about a topic, event, or query.
    
    Args:
        query: The search query to look up on the web
        max_results: Maximum number of search results to return (default: 5)
    
    Returns:
        JSON string containing search results with title, url, and snippet
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href") or r.get("url", ""),
                    "snippet": r.get("body", "")
                })
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})
