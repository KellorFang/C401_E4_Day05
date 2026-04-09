"""
Web Search Tool Module
Dùng API mở rộng tìm kiếm (Tavily hoặc SerpAPI) cho các câu hỏi Out-of-Domain hoặc kiến thức cập nhật.
"""

import os

def search_web(query: str) -> str:
    """
    Thực hiện search query trên mạng.
    
    Args:
        query (str): Cụm từ cần tìm.
        
    Returns:
        str: Kết quả summary từ web.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    # TODO: Gọi Tavily Search API
    return f"Dummy web search results for: {query}"
