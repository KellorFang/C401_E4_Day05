'''
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
"""
RAG Tool Module
Giao tiếp với Vector Database (ChromaDB/Qdrant) để lấy content khóa học.

def retrieve_from_slide(query: str, top_k: int = 3) -> str:
    
    Nhúng câu hỏi (Embed) và quét trên VectorDB để lấy top chunks context.
    
    Args:
        query (str): Câu hỏi/Từ khóa liên quan đến slide.
        top_k (int): Số lượng chunk muốn lấy.
        
    Returns:
        str: Chuỗi văn bản chứa thông tin khóa học.
    
    # TODO: Embedding query
    # TODO: Tìm kiếm similarity trên VectorDB
    # TODO: Kết hợp kết quả
    
    return "Dummy context retrieved from Slide."

"""
'''

import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

load_dotenv()

# Global variable to hold our compiled pipeline so the tool can access it
_GLOBAL_RAG_CHAIN = None

# ---------------------------------------------------------
# Step 1: Simulate Reading Teammates' Extracted Data
# ---------------------------------------------------------
def load_parsed_pdf_data(mock_filepath: str):
    """
    Simulates reading the output from your teammates' PDF parsing tool.
    Ideally, they provide a list of dictionaries with text and metadata.
    """
    print(f"Loading extracted data from: {mock_filepath}...")
    # In reality, this might be: json.load(open(mock_filepath))
    return [
        {"text": "The Error Code ER-404 means the database connection timed out.", "page": 1, "section": "Troubleshooting"},
        {"text": "To fix a leaking pipe, turn off the water main and apply Teflon tape.", "page": 2, "section": "Maintenance"},
        {"text": "Our Q3 revenue grew by 15% to reach $5.2 million.", "page": 3, "section": "Financials"},
        {"text": "If you encounter a timeout error, check your network firewall settings.", "page": 1, "section": "Troubleshooting"}
    ]

# ---------------------------------------------------------
# Step 2: Build the RAG Engine (Ingestion + Setup)
# ---------------------------------------------------------
def initialize_knowledge_base(parsed_data):
    """
    Takes the parsed data, chunks it, embeds it, and builds the Hybrid+Reranker pipeline.
    This should run ONCE when your app starts.
    """
    global _GLOBAL_RAG_CHAIN
    
    # 1. Convert parsed data into LangChain Document objects
    documents = [
        Document(
            page_content=item["text"], 
            metadata={"page": item["page"], "section": item["section"]}
        ) 
        for item in parsed_data
    ]

    # 2. Chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    chunks = text_splitter.split_documents(documents)

    # 3. Embedding & Retrieval (Hybrid Search)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    dense_retriever = FAISS.from_documents(chunks, embeddings).as_retriever(search_kwargs={"k": 4})
    
    sparse_retriever = BM25Retriever.from_documents(chunks)
    sparse_retriever.k = 4

    hybrid_retriever = EnsembleRetriever(
        retrievers=[dense_retriever, sparse_retriever], weights=[0.5, 0.5]
    )

    # 4. Refinement (Cross-Encoder Re-ranker)
    cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    compressor = CrossEncoderReranker(model=cross_encoder, top_n=2)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=hybrid_retriever
    )

    # 5. The Generation Chain
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    prompt = ChatPromptTemplate.from_template("""
    Answer the user's question using ONLY the context provided below. 
    Include the section and page number in your answer if available.
    
    Context:
    {context}

    Question: {question}
    """)

    def format_docs(docs):
        # Format documents to include metadata for the LLM
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

# ---------------------------------------------------------
# Step 3: Define the LangGraph Tool
# ---------------------------------------------------------
@tool
def search_pdf_knowledge(query: str) -> str:
    """
    Use this tool to search the internal PDF knowledge base. 
    Pass a specific, detailed question as the query.
    """
    if _GLOBAL_RAG_CHAIN is None:
        return "Error: The knowledge base has not been initialized."
    
    # Execute the RAG pipeline
    return _GLOBAL_RAG_CHAIN.invoke(query)

# ---------------------------------------------------------
# Step 4: Run the Prototype
# ---------------------------------------------------------
if __name__ == "__main__":
    # 1. Load the data (teammates' output)
    extracted_data = load_parsed_pdf_data("mock_output.json")
    
    # 2. Ingest data and build the pipeline
    initialize_knowledge_base(extracted_data)
    
    # 3. The LLM Agent will now be able to call this tool in LangGraph!
    # Here is what happens when the tool is called:
    test_query = "What does ER-404 mean, and where can I find info about it?"
    print(f"\nAgent calling tool with query: '{test_query}'")
    
    result = search_pdf_knowledge.invoke({"query": test_query})
    print(f"\nTool Output:\n{result}")


# Add Chunk piece citation 
#   Ingestion: We stored {"page": item["page"], "section": item["section"]} alongside the text.
#   Formatting: The format_docs function grabbed that metadata so the LLM could "see" which page it was reading from.

# Embedding information
#   We used OpenAIEmbeddings(model="text-embedding-3-small") to convert the text chunks into vectors.
#   FAISS then built a vector index for fast semantic search.
#   BM25Retriever handles keyword-based search.
#   EnsembleRetriever combines both for optimal recall.
#   CrossEncoderReranker re-ranks the results for better accuracy.
#   ContextualCompressionRetriever applies the re-ranker to the retrieved documents.
#   The final RAG chain combines retrieval, re-ranking, and LLM generation for accurate, context-aware answers.

