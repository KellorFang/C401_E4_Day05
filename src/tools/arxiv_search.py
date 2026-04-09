"""ArXiv Tool — searches academic papers for research references."""

from langchain_core.tools import tool


@tool
def search_arxiv(query: str) -> str:
    """Search academic papers on arXiv for research references. Use when students
    ask about cutting-edge research or want paper citations.
    Do NOT use for practical course content or assignments."""
    try:
        from langchain_community.retrievers import ArxivRetriever
        retriever = ArxivRetriever(load_max_docs=3)
        docs = retriever.invoke(query)
        if not docs:
            return f"Không tìm thấy bài báo nào trên arXiv cho: {query}"
        formatted = []
        for i, doc in enumerate(docs, start=1):
            title   = doc.metadata.get("Title", "N/A")
            url     = doc.metadata.get("Entry ID", doc.metadata.get("arxiv_url", "N/A"))
            summary = doc.page_content.strip()
            formatted.append(
                f"[{i}] Title  : {title}\n"
                f"    URL    : {url}\n"
                f"    Summary: {summary[:300]}{'...' if len(summary) > 300 else ''}"
            )
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Lỗi khi gọi ArXiv Retriever: {e}"

