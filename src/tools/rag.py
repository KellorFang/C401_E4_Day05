"""RAG Tool — queries ChromaDB for course slide content."""

from langchain_core.tools import tool


@tool
def search_slides(query: str) -> str:
    """Search course lecture slides for relevant content about AI concepts,
    theory, and examples. Use this when students ask about course material.
    Do NOT use for external library docs or current events."""
    # TODO (Teammate): Implement ChromaDB retrieval
    # Suggested approach:
    #   from langchain_chroma import Chroma
    #   from langchain_openai import OpenAIEmbeddings
    #   1. Load persisted ChromaDB from ./chroma_db/
    #      embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    #      vector_store = Chroma(persist_directory="./chroma_db/",
    #                            embedding_function=embeddings)
    #   2. retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    #   3. docs = retriever.invoke(query)
    #   4. Format results: "[source p.N]\ncontent" for each doc
    # Reference: references/13-langchain-chroma-integration.md
    return "TODO: Chua implement — can ket noi ChromaDB retriever."
