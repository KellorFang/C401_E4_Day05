"""Web Search Tool — searches the internet via Tavily."""

import os

from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """Search the web for programming knowledge, library docs, or topics
    not covered in course slides. Use when the question goes beyond course material.
    Do NOT use when the answer is likely in course slides."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Lỗi: TAVILY_API_KEY chưa được cấu hình trong biến môi trường."

    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        search = TavilySearchResults(max_results=5, tavily_api_key=api_key)
        results = search.invoke(query)
        # results là list of dicts: [{"url": ..., "content": ...}, ...]
        if not results:
            return f"Không tìm thấy kết quả nào cho: {query}"
        formatted = []
        for i, r in enumerate(results, start=1):
            url     = r.get("url", "N/A")
            content = r.get("content", "").strip()
            formatted.append(f"[{i}] {url}\n    {content[:300]}{'...' if len(content) > 300 else ''}")
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Lỗi khi gọi Tavily Search API: {e}"

