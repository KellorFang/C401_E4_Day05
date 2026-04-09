"""
Ingestion Pipeline — PDF slides -> chunk -> embed -> ChromaDB.

Run once after adding or updating slides in src/data/slides/.

Usage:
    python ingest.py
"""

import os
import glob

from dotenv import load_dotenv

load_dotenv()


def ingest_slides(slides_dir: str = "data/slides", persist_dir: str = "chroma_db"):
    """Parse all PDFs in slides_dir, chunk, embed, and store in ChromaDB.

    Args:
        slides_dir: Path to directory containing PDF files.
        persist_dir: Path to ChromaDB persistence directory.
    """
    pdf_files = glob.glob(os.path.join(slides_dir, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {slides_dir}/")
        return

    print(f"Found {len(pdf_files)} PDF file(s). Starting ingestion...")

    # TODO (Teammate): Implement the ingestion pipeline
    #
    # Step 1 — Parse PDFs (extract text + images/diagrams + tables)
    #   Suggested: PyMuPDF4LLM with LLMImageBlobParser for diagrams
    #   See: references/16-pdf-extraction-with-images.md
    #
    #   Option A — Load all PDFs in a directory at once (recommended):
    #
    #   from langchain_community.document_loaders import FileSystemBlobLoader
    #   from langchain_community.document_loaders.generic import GenericLoader
    #   from langchain_pymupdf4llm import PyMuPDF4LLMParser
    #   from langchain_community.document_loaders.parsers import LLMImageBlobParser
    #   from langchain_openai import ChatOpenAI
    #
    #   loader = GenericLoader(
    #       blob_loader=FileSystemBlobLoader(path=slides_dir, glob="*.pdf"),
    #       blob_parser=PyMuPDF4LLMParser(
    #           extract_images=True,
    #           images_parser=LLMImageBlobParser(
    #               model=ChatOpenAI(model="gpt-4o-mini", max_tokens=1024)
    #           ),
    #           table_strategy="lines",  # extract tables as markdown
    #       )
    #   )
    #   docs = loader.load()
    #
    #   Option B — Load one PDF at a time (if you need per-file control):
    #
    #   from langchain_pymupdf4llm import PyMuPDF4LLMLoader
    #
    #   all_docs = []
    #   for pdf_path in pdf_files:
    #       loader = PyMuPDF4LLMLoader(
    #           pdf_path,
    #           extract_images=True,
    #           images_parser=LLMImageBlobParser(
    #               model=ChatOpenAI(model="gpt-4o-mini", max_tokens=1024)
    #           ),
    #           table_strategy="lines",
    #       )
    #       all_docs.extend(loader.load())
    #   docs = all_docs
    #
    # Step 2 — Chunk documents
    #   Recursive chunking is best for structured educational content like slides.
    #   See: references/14-chunking-strategies-for-rag.md
    #
    #   from langchain_text_splitters import RecursiveCharacterTextSplitter
    #   splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    #   chunks = splitter.split_documents(docs)
    #
    # Step 3 — Tag chunks with metadata
    #   PyMuPDF4LLM auto-populates metadata (source, page, etc.), but verify
    #   each chunk has at least: {"source": filename, "page": page_number}
    #
    # Step 4 — Embed and store in ChromaDB
    #   See: references/13-langchain-chroma-integration.md
    #
    #   from uuid import uuid4
    #   from langchain_openai import OpenAIEmbeddings
    #   from langchain_chroma import Chroma
    #
    #   embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    #   vector_store = Chroma(
    #       collection_name="course_slides",
    #       embedding_function=embeddings,
    #       persist_directory=persist_dir,
    #   )
    #   uuids = [str(uuid4()) for _ in range(len(chunks))]
    #   vector_store.add_documents(documents=chunks, ids=uuids)

    print("TODO: Ingestion pipeline chua duoc implement.")
    for f in pdf_files:
        print(f"  - {f}")


if __name__ == "__main__":
    ingest_slides()
