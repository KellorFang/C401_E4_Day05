"""RAG Tool — Trích xuất kiến thức tập bài giảng dùng NVIDIA AI Endpoints."""

import os
import glob
import re
from typing import List, Dict
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

load_dotenv()

# Global variable to hold our compiled pipeline
_GLOBAL_RAG_CHAIN = None


# ---------------------------------------------------------
# Step 1: Load Real Data from src/dataset/*.md
# ---------------------------------------------------------
def load_dataset_slides(dataset_dir: str):
    """
    Quét toàn bộ file .md trong dataset, cắt theo Slide marker (---)
    và gán metadata (tên file, số trang).
    """
    all_docs = []
    md_files = glob.glob(os.path.join(dataset_dir, "*.md"))

    if not md_files:
        print(f"⚠️  Không tìm thấy file .md nào trong {dataset_dir}")
        return []

    print(f"📂 Đang nạp dữ liệu từ {len(md_files)} bài học...")

    for file_path in md_files:
        filename = os.path.basename(file_path).replace(".md", "")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Tách theo Slide marker
        slides = content.split("---")

        for slide_text in slides:
            slide_text = slide_text.strip()
            if not slide_text:
                continue

            # Trích xuất số trang từ "## Slide N"
            page_match = re.search(r"## Slide (\d+)", slide_text)
            page_num = int(page_match.group(1)) if page_match else 0

            # Làm sạch header nếu cần
            doc = Document(
                page_content=slide_text, metadata={"source": filename, "page": page_num}
            )
            all_docs.append(doc)

    print(f"✅ Đã nạp {len(all_docs)} slides.")
    return all_docs


# ---------------------------------------------------------
# Step 2: Build the RAG Engine (NVIDIA Optimized)
# ---------------------------------------------------------
def initialize_knowledge_base(docs: List[Document]):
    """
    Index dữ liệu dùng NVIDIA Embeddings và thiết lập Hybrid Retriever + Reranker.
    """
    global _GLOBAL_RAG_CHAIN

    if not docs:
        print("❌ Không có dữ liệu để khởi tạo Knowledge Base.")
        return

    # 1. Chunking (Recursive)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)

    # 2. Embedding & Retrieval (HuggingFace Local + FAISS + BM25)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    dense_retriever = FAISS.from_documents(chunks, embeddings).as_retriever(
        search_kwargs={"k": 5}
    )

    sparse_retriever = BM25Retriever.from_documents(chunks)
    sparse_retriever.k = 5

    hybrid_retriever = EnsembleRetriever(
        retrievers=[dense_retriever, sparse_retriever], weights=[0.5, 0.5]
    )

    # 3. ChatNVIDIA Setup
    # Sử dụng model openai/gpt-oss-120b với API Key NVIDIA
    llm = ChatNVIDIA(model="openai/gpt-oss-120b", temperature=0.1, max_tokens=2048)

    prompt = ChatPromptTemplate.from_template("""
    Bạn là một trợ giảng AI chuyên về khóa học AI cơ bản. 
    Hãy sử dụng nội dung context dưới đây để trả lời câu hỏi của sinh viên.
    Nếu không có trong context, hãy thành thật trả lời là bạn không biết.
    Luôn ghi rõ nguồn (Tên bài & Slide) khi trích dẫn.

    Context:
    {context}

    Câu hỏi: {question}
    """)

    def format_docs(docs):
        formatted = []
        for doc in docs:
            src = doc.metadata.get("source", "N/A")
            pg = doc.metadata.get("page", "N/A")
            formatted.append(f"[Nguồn: {src}, Slide {pg}]\n{doc.page_content}")
        return "\n\n---\n\n".join(formatted)

    _GLOBAL_RAG_CHAIN = (
        {"context": hybrid_retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print("🚀 Hệ thống RAG NVIDIA đã sẵn sàng!")


# ---------------------------------------------------------
# Step 3: Define the LangGraph Tool
# ---------------------------------------------------------
@tool
def search_pdf_knowledge(query: str) -> str:
    """
    Search thông tin trong tập slide bài giảng (B1-B5).
    Dùng công cụ này khi sinh viên hỏi về lý thuyết, ví dụ hoặc các khái niệm trong bài học.
    """
    if _GLOBAL_RAG_CHAIN is None:
        return "Error: Hệ thống RAG chưa được khởi tạo."

    # Thực hiện search và lấy kết quả
    return _GLOBAL_RAG_CHAIN.invoke(query)


# ---------------------------------------------------------
# Step 4: Run Test
# ---------------------------------------------------------
if __name__ == "__main__":
    # 1. Load dữ liệu thật từ src/dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "dataset")
    extracted_docs = load_dataset_slides(dataset_path)

    # 2. Khởi tạo pipeline
    initialize_knowledge_base(extracted_docs)

    # 3. Test Query
    test_query = "Sự khác biệt chính giữa Chatbot và Agent là gì?"
    print(f"\n💬 Query: '{test_query}'")

    # Test streaming với RAG Chain
    print("\n🤖 Assistant (RAG Streaming with Potential Reasoning):")

    full_response = ""
    # Streaming từ chuỗi RAG để đảm bảo truy xuất (retrieval) được thực thi
    for chunk in _GLOBAL_RAG_CHAIN.stream(test_query):
        print(chunk, end="", flush=True)
        full_response += chunk

    print("\n\n✅ Done.")
