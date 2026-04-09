# PDF Extraction for Image-Heavy Slides (Diagrams, Charts, Figures)

> Problem: PyMuPDF's basic `page.get_text()` only extracts selectable text. Course slides are often image-heavy — diagrams, screenshots, text rendered as images — so you get almost nothing.

## Solution: `PyMuPDF4LLM` + Multimodal Image Parsing

`pymupdf4llm` is a wrapper built specifically for LLM/RAG pipelines. It has three options for handling images in PDFs:

| Approach | How it works | Best for |
|---|---|---|
| **RapidOCR** | Lightweight OCR, extracts text from images | Text rendered as images (fast, free) |
| **Tesseract** | Traditional OCR, higher precision | Dense text in images |
| **LLMImageBlobParser (GPT-4o-mini)** | Sends images to a vision LLM to *describe* them | **Diagrams, charts, architecture figures** |

For slides with diagrams, **the LLM approach is the right one** — OCR can't "read" a flowchart, but GPT-4o-mini can describe what the diagram shows, and that description becomes searchable text in ChromaDB.

## Installation

```bash
pip install -qU langchain-community langchain-pymupdf4llm langchain-openai
```

## Single PDF Extraction

```python
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_openai import ChatOpenAI

loader = PyMuPDF4LLMLoader(
    "./data/slides/lecture-01.pdf",
    extract_images=True,
    images_parser=LLMImageBlobParser(
        model=ChatOpenAI(model="gpt-4o-mini", max_tokens=1024)
    ),
    table_strategy="lines",  # also extract tables as markdown
)

docs = loader.load()  # each page → Document with text + image descriptions + tables
```

## Multiple PDFs at Once

```python
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_pymupdf4llm import PyMuPDF4LLMParser

loader = GenericLoader(
    blob_loader=FileSystemBlobLoader(path="./data/slides/", glob="*.pdf"),
    blob_parser=PyMuPDF4LLMParser(
        extract_images=True,
        images_parser=LLMImageBlobParser(
            model=ChatOpenAI(model="gpt-4o-mini", max_tokens=1024)
        )
    )
)
docs = loader.load()
```

## Then Chunk and Embed

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
# → embed and store in ChromaDB
```

## Image Parsing Options Detail

### RapidOCR (Lightweight, Free)
```python
from langchain_community.document_loaders.parsers import RapidOCRBlobParser

loader = PyMuPDF4LLMLoader(
    "./data/slides/lecture-01.pdf",
    extract_images=True,
    images_parser=RapidOCRBlobParser()
)
```
Note: Designed primarily for Chinese and English text recognition.

### Tesseract (High Precision)
```python
from langchain_community.document_loaders.parsers import TesseractBlobParser

loader = PyMuPDF4LLMLoader(
    "./data/slides/lecture-01.pdf",
    extract_images=True,
    images_parser=TesseractBlobParser()
)
```

### Multimodal LLM — GPT-4o-mini (Best for Diagrams)
```python
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from langchain_openai import ChatOpenAI

loader = PyMuPDF4LLMLoader(
    "./data/slides/lecture-01.pdf",
    extract_images=True,
    images_parser=LLMImageBlobParser(
        model=ChatOpenAI(model="gpt-4o-mini", max_tokens=1024)
    )
)
```

## Trade-offs

- **Cost:** LLM image parser costs a small amount per image (GPT-4o-mini vision is cheap), but it only runs once during ingestion, not at query time.
- **Speed:** LLM parsing is slower than OCR but produces much better descriptions of diagrams.
- **Quality:** OCR can't "read" a flowchart; a vision LLM can describe what the diagram shows.

## Sources

- [PyMuPDF4LLM LangChain Integration](https://docs.langchain.com/oss/python/integrations/document_loaders/pymupdf4llm)
- [Building a Multimodal LLM Application with PyMuPDF4LLM](https://artifex.com/blog/building-a-multimodal-llm-application-with-pymupdf4llm)
- [PyMuPDF4LLM API Docs](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/api.html)
- [Complete RAG Pipeline with OCR](https://medium.com/@caring_smitten_gerbil_914/complete-rag-pipeline-from-pdf-using-mistral-ocr-qdrant-llms-in-python-b845b7164ebb)
