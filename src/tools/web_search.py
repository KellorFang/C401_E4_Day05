"""Web Search Tool — searches the internet via Tavily."""

import os

from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """Search the web for programming knowledge, library docs, or topics
    not covered in course slides. Use when the question goes beyond course material.
    Do NOT use when the answer is likely in course slides."""
    # TODO (Teammate): Implement Tavily search
    # Suggested approach:
    #   from langchain_community.tools.tavily_search import TavilySearchResults
    #   search = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
    #   results = search.invoke(query)
    #   Format and return results as a string
    return f"TODO: Chua implement — can ket noi Tavily API. Query: {query}"
