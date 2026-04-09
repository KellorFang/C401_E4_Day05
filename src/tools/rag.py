# =============================================================================
# Scaffold version (search_slides) — commented out, kept for reference.
# =============================================================================
#
# """RAG Tool — queries ChromaDB for course slide content."""
#
# from langchain_core.tools import tool
#
#
# @tool
# def search_slides(query: str) -> str:
#     """Search course lecture slides for relevant content about AI concepts,
#     theory, and examples. Use this when students ask about course material.
#     Do NOT use for external library docs or current events."""
#     # TODO (Teammate): Implement ChromaDB retrieval
#     # Suggested approach:
#     #   from langchain_chroma import Chroma
#     #   from langchain_openai import OpenAIEmbeddings
#     #   1. Load persisted ChromaDB from ./chroma_db/
#     #      embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
#     #      vector_store = Chroma(persist_directory="./chroma_db/",
#     #                            embedding_function=embeddings)
#     #   2. retriever = vector_store.as_retriever(search_kwargs={"k": 3})
#     #   3. docs = retriever.invoke(query)
#     #   4. Format results: "[source p.N]\ncontent" for each doc
#     # Reference: references/13-langchain-chroma-integration.md
#     return "TODO: Chưa implement — cần kết nối ChromaDB retriever."


"""
RAG Tool Module — Teammate thangnn05's FAISS+BM25 hybrid implementation.
"""

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

load_dotenv()

_GLOBAL_RAG_CHAIN = None


def load_parsed_pdf_data(mock_filepath: str):
    """Simulates reading the output from teammates' PDF parsing tool."""
    print(f"Loading extracted data from: {mock_filepath}...")
    return [
        {"text": "The Error Code ER-404 means the database connection timed out.", "page": 1, "section": "Troubleshooting"},
        {"text": "To fix a leaking pipe, turn off the water main and apply Teflon tape.", "page": 2, "section": "Maintenance"},
        {"text": "Our Q3 revenue grew by 15% to reach $5.2 million.", "page": 3, "section": "Financials"},
        {"text": "If you encounter a timeout error, check your network firewall settings.", "page": 1, "section": "Troubleshooting"}
    ]


def initialize_knowledge_base(parsed_data):
    """Takes parsed data, chunks it, embeds it, builds Hybrid+Reranker pipeline."""
    global _GLOBAL_RAG_CHAIN

    documents = [
        Document(
            page_content=item["text"],
            metadata={"page": item["page"], "section": item["section"]}
        )
        for item in parsed_data
    ]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    chunks = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    dense_retriever = FAISS.from_documents(chunks, embeddings).as_retriever(search_kwargs={"k": 4})

    sparse_retriever = BM25Retriever.from_documents(chunks)
    sparse_retriever.k = 4

    hybrid_retriever = EnsembleRetriever(
        retrievers=[dense_retriever, sparse_retriever], weights=[0.5, 0.5]
    )

    cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    compressor = CrossEncoderReranker(model=cross_encoder, top_n=2)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=hybrid_retriever
    )

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_template("""
    Answer the user's question using ONLY the context provided below.
    Include the section and page number in your answer if available.

    Context:
    {context}

    Question: {question}
    """)

    def format_docs(docs):
        return "\n\n".join(
            f"[Page {doc.metadata.get('page')}, {doc.metadata.get('section')}]: {doc.page_content}"
            for doc in docs
        )

    _GLOBAL_RAG_CHAIN = (
        {"context": compression_retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print("Knowledge base initialized successfully!")


@tool
def search_slides(query: str) -> str:
    """Search course lecture slides for relevant content about AI concepts,
    theory, and examples. Use this when students ask about course material.
    Do NOT use for external library docs or current events."""
    if _GLOBAL_RAG_CHAIN is None:
        return "Error: The knowledge base has not been initialized."
    return _GLOBAL_RAG_CHAIN.invoke(query)


if __name__ == "__main__":
    extracted_data = load_parsed_pdf_data("mock_output.json")
    initialize_knowledge_base(extracted_data)

    test_query = "What does ER-404 mean, and where can I find info about it?"
    print(f"\nAgent calling tool with query: '{test_query}'")
    result = search_slides.invoke({"query": test_query})
    print(f"\nTool Output:\n{result}")
