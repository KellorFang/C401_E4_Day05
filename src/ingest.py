"""
Ingestion Pipeline — Parsed slide .md files -> chunk -> embed -> ChromaDB.

Run once after adding or updating slides in tools/slide_output/.

Usage:
    cd src && python ingest.py
"""

import os
import re
import glob
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

SLIDES_DIR = os.path.join(os.path.dirname(__file__), "tools", "slide_output")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")


def load_slides(slides_dir: str = SLIDES_DIR) -> list[Document]:
    """Load parsed .md slide files, split by slide markers, return Documents."""
    md_files = sorted(glob.glob(os.path.join(slides_dir, "*.md")))
    if not md_files:
        print(f"No .md files found in {slides_dir}/")
        return []

    print(f"Found {len(md_files)} file(s). Loading...")

    docs = []
    for file_path in md_files:
        filename = os.path.basename(file_path).replace(".md", "")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        slides = content.split("---")
        for slide_text in slides:
            slide_text = slide_text.strip()
            if not slide_text:
                continue

            page_match = re.search(r"## Slide (\d+)", slide_text)
            page_num = int(page_match.group(1)) if page_match else 0

            docs.append(Document(
                page_content=slide_text,
                metadata={"source": filename, "page": page_num},
            ))

    print(f"Loaded {len(docs)} slides.")
    return docs


def ingest_slides(slides_dir: str = SLIDES_DIR, persist_dir: str = PERSIST_DIR):
    """Load slides, chunk, embed with OpenAI, store in ChromaDB."""
    docs = load_slides(slides_dir)
    if not docs:
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(
        collection_name="course_slides",
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )

    uuids = [str(uuid4()) for _ in range(len(chunks))]
    vector_store.add_documents(documents=chunks, ids=uuids)
    print(f"Stored {len(chunks)} chunks in ChromaDB at {persist_dir}/")


if __name__ == "__main__":
    ingest_slides()
