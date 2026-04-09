from typing import Annotated
from langchain_community.document_loaders import PubMedLoader
from langchain_core.tools import tool


@tool
def pubmed_search_tool(
    query: Annotated[str, "Cụm từ cần tìm kiếm trên PubMed"],
    max_results: Annotated[int, "Số lượng kết quả tối đa"] = 3
) -> str:
    """
    Tìm kiếm tài liệu y khoa trên PubMed và trả về tóm tắt.
    
    Args:
        query (str): Cụm từ cần tìm.
        max_results (int): Số lượng kết quả tối đa (mặc định: 3).
        
    Returns:
        str: Kết quả summary từ web.
    """
    try:
        # Khởi tạo PubMed loader với query
        loader = PubMedLoader(query=query, load_max_docs=max_results)
        
        # Tải tài liệu
        documents = loader.load()
        
        if not documents:
            return f"Không tìm thấy kết quả nào cho truy vấn: '{query}'"
        
        # Tạo summary từ các tài liệu
        summary_parts = []
        summary_parts.append(f"Tìm thấy {len(documents)} kết quả cho '{query}':\n")
        
        for idx, doc in enumerate(documents, 1):
            # Lấy metadata
            metadata = doc.metadata
            title = metadata.get('title', 'Không có tiêu đề')
            authors = metadata.get('authors', 'Không rõ tác giả')
            pub_date = metadata.get('published', 'Không rõ ngày')
            
            # Lấy nội dung tóm tắt (giới hạn 500 ký tự)
            content = doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content
            
            summary_parts.append(f"\n--- Kết quả {idx} ---")
            summary_parts.append(f"Tiêu đề: {title}")
            summary_parts.append(f"Tác giả: {authors}")
            summary_parts.append(f"Ngày xuất bản: {pub_date}")
            summary_parts.append(f"Tóm tắt: {content}\n")
        
        return "\n".join(summary_parts)
        
    except Exception as e:
        return f"Lỗi khi tìm kiếm PubMed: {str(e)}"


# Ví dụ sử dụng trong LangGraph workflow
