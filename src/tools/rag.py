"""RAG Tool — queries ChromaDB for course slide content."""

from langchain_core.tools import tool


@tool
def search_slides(query: str) -> str:
    """Search course lecture slides for relevant content about AI concepts,
    theory, and examples. Use this when students ask about course material.
    Do NOT use for external library docs or current events."""
    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vector_store = Chroma(
            persist_directory="./chroma_db/",
            embedding_function=embeddings,
        )
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(query)

        if not docs:
            return f"Không tìm thấy nội dung nào trong slide cho: {query}"

        formatted = []
        for doc in docs:
            source = doc.metadata.get("source", "N/A")
            page = doc.metadata.get("page", "N/A")
            formatted.append(f"[{source}, Slide {page}]\n{doc.page_content}")
        return "\n\n---\n\n".join(formatted)

    except Exception as e:
        return f"Lỗi khi truy vấn ChromaDB: {e}"
