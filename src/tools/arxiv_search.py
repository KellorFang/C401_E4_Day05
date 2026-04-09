"""ArXiv Tool — searches academic papers for research references."""

from langchain_core.tools import tool


@tool
def search_arxiv(query: str) -> str:
    """Search academic papers on arXiv for research references. Use when students
    ask about cutting-edge research or want paper citations.
    Do NOT use for practical course content or assignments."""
    # TODO (Teammate): Implement ArXiv retrieval
    # Suggested approach:
    #   from langchain_community.retrievers import ArxivRetriever
    #   retriever = ArxivRetriever(load_max_docs=3)
    #   docs = retriever.invoke(query)
    #   Format: "Title: ...\nSummary: ...\nURL: ..." for each paper
    # Reference: references/15-arxiv-retriever.md
    return f"TODO: Chua implement — can ket noi ArXiv retriever. Query: {query}"
