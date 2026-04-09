"""
RAG Tool Module
Giao tiếp với Vector Database (ChromaDB/Qdrant) để lấy content khóa học.
"""

def retrieve_from_slide(query: str, top_k: int = 3) -> str:
    """
    Nhúng câu hỏi (Embed) và quét trên VectorDB để lấy top chunks context.
    
    Args:
        query (str): Câu hỏi/Từ khóa liên quan đến slide.
        top_k (int): Số lượng chunk muốn lấy.
        
    Returns:
        str: Chuỗi văn bản chứa thông tin khóa học.
    """
    # TODO: Embedding query
    # TODO: Tìm kiếm similarity trên VectorDB
    # TODO: Kết hợp kết quả
    
    return "Dummy context retrieved from Slide."
