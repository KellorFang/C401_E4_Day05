# AI Tutor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the AI Tutor agent core (`agent.py`) and scaffold all teammate-owned components (`tools/`, `ingest.py`, `app.py`) so the project is runnable end-to-end with dummy tool outputs.

**Architecture:** Single agent using `create_agent` (LangChain) + GPT-5-mini + 4 tools (`search_slides`, `search_web`, `fetch_assignment`, `search_arxiv`). Streamlit chat UI. ChromaDB for vector storage. LangSmith for tracing. Huy implements the agent core; teammates fill in tool implementations and UI.

**Tech Stack:** `langchain`, `langchain-openai`, `langchain-community`, `langchain-chroma`, `streamlit`, `tavily-python`, `python-dotenv`, `arxiv`

---

## File Structure

```
src/
├── app.py                  # Streamlit chat UI (scaffold — teammate implements)
├── agent.py                # create_agent + system prompt + tool wiring (Huy implements)
├── ingest.py               # PDF -> chunk -> embed -> ChromaDB (scaffold — teammate implements)
├── tools/
│   ├── __init__.py         # Re-exports all 4 tool functions
│   ├── rag.py              # search_slides — ChromaDB retriever (scaffold — teammate implements)
│   ├── web_search.py       # search_web — Tavily (scaffold — teammate implements)
│   ├── github.py           # fetch_assignment — GitHub REST API (scaffold — teammate implements)
│   └── arxiv_search.py     # search_arxiv — ArXiv retriever (scaffold — teammate implements)
├── data/
│   └── slides/             # Drop PDF files here
│       └── .gitkeep
└── chroma_db/              # Persisted vector DB (gitignored)
tests/
└── test_agent.py           # Agent core unit tests
.env.example                # API key template
requirements.txt            # Python dependencies
```

**Replaces:** `src/agent/agent.py` (old manual LangGraph approach) — the approved spec uses `create_agent` instead.

---

### Task 1: Project Infrastructure

**Files:**
- Modify: `.gitignore`
- Create: `.env.example`
- Create: `requirements.txt`
- Create: `src/data/slides/.gitkeep`

- [ ] **Step 1: Update `.gitignore`**

```
.DS_Store
**/.DS_Store
**/__pycache__
.env
src/chroma_db/
*.pyc
.pytest_cache/
```

- [ ] **Step 2: Create `.env.example`**

```
# Required
OPENAI_API_KEY=sk-...        # GPT-5-mini + embeddings
TAVILY_API_KEY=tvly-...      # Web search
GITHUB_TOKEN=ghp_...         # GitHub repo access

# Optional (recommended)
LANGSMITH_API_KEY=lsv2-...   # Tracing
LANGSMITH_TRACING=true
```

- [ ] **Step 3: Create `requirements.txt`**

```
langchain>=0.3
langchain-openai>=0.3
langchain-community>=0.3
langchain-chroma>=0.1.2
langchain-pymupdf4llm
tavily-python
streamlit
python-dotenv
arxiv
```

- [ ] **Step 4: Create `src/data/slides/.gitkeep`**

Empty file — just ensures the directory exists in git.

- [ ] **Step 5: Commit**

```bash
git add .gitignore .env.example requirements.txt src/data/slides/.gitkeep
git commit -m "chore: add project infrastructure — .env.example, requirements, .gitignore"
```

---

### Task 2: Tool Scaffolds (for teammates)

**Files:**
- Create: `src/tools/__init__.py`
- Create: `src/tools/rag.py` (replaces existing)
- Create: `src/tools/web_search.py` (replaces existing)
- Create: `src/tools/github.py` (replaces existing)
- Create: `src/tools/arxiv_search.py` (new)

Each tool has the `@tool` decorator, correct signature, docstring, suggested approach in comments, and a placeholder return so the agent doesn't crash during development.

- [ ] **Step 1: Create `src/tools/rag.py`**

```python
"""RAG Tool — queries ChromaDB for course slide content."""

from langchain_core.tools import tool


@tool
def search_slides(query: str) -> str:
    """Search course lecture slides for relevant content about AI concepts,
    theory, and examples. Use this when students ask about course material.
    Do NOT use for external library docs or current events."""
    # TODO (Teammate): Implement ChromaDB retrieval
    # Suggested approach:
    #   1. Load persisted ChromaDB from ./chroma_db/
    #      vector_store = Chroma(persist_directory="./chroma_db/",
    #                            embedding_function=embeddings)
    #   2. retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    #   3. docs = retriever.invoke(query)
    #   4. Format results: "[source p.N]\ncontent" for each doc
    # Reference: references/13-langchain-chroma-integration.md
    return "TODO: Chưa implement — cần kết nối ChromaDB retriever."
```

- [ ] **Step 2: Create `src/tools/web_search.py`**

```python
"""Web Search Tool — searches the internet via Tavily."""

import os

from langchain_core.tools import tool


@tool
def search_web(query: str) -> str:
    """Search the web for programming knowledge, library docs, or topics
    not covered in course slides. Use when the question goes beyond course material.
    Do NOT use when the answer is likely in course slides."""
    # TODO (Teammate): Implement Tavily search
    # Suggested approach:
    #   from langchain_community.tools.tavily_search import TavilySearchResults
    #   search = TavilySearchResults(api_key=os.getenv("TAVILY_API_KEY"))
    #   results = search.invoke(query)
    #   Format and return results as a string
    return f"TODO: Chưa implement — cần kết nối Tavily API. Query: {query}"
```

- [ ] **Step 3: Create `src/tools/github.py`**

```python
"""GitHub Tool — fetches README.md from assignment repos."""

import os

from langchain_core.tools import tool


@tool
def fetch_assignment(repo_url: str) -> str:
    """Fetch the README.md from a GitHub repository to understand assignment
    requirements. Use when a student shares a repo link or asks about an assignment.
    Do NOT use when no repo URL is mentioned."""
    # TODO (Teammate): Implement GitHub REST API call
    # Suggested approach:
    #   1. Parse repo_url to extract owner/repo
    #      e.g. "https://github.com/owner/repo" -> owner, repo
    #   2. Call GitHub REST API: GET /repos/{owner}/{repo}/readme
    #      Headers: {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    #   3. Decode base64 content from response
    #   4. Return the markdown text
    #   5. Handle errors: 404, private repo, rate limit
    return f"TODO: Chưa implement — cần kết nối GitHub API. URL: {repo_url}"
```

- [ ] **Step 4: Create `src/tools/arxiv_search.py`**

```python
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
    return f"TODO: Chưa implement — cần kết nối ArXiv retriever. Query: {query}"
```

- [ ] **Step 5: Create `src/tools/__init__.py`**

```python
"""Tool registry — re-exports all tools for agent.py to import."""

from tools.rag import search_slides
from tools.web_search import search_web
from tools.github import fetch_assignment
from tools.arxiv_search import search_arxiv

ALL_TOOLS = [search_slides, search_web, fetch_assignment, search_arxiv]
```

- [ ] **Step 6: Commit**

```bash
git add src/tools/__init__.py src/tools/rag.py src/tools/web_search.py src/tools/github.py src/tools/arxiv_search.py
git commit -m "feat: add tool scaffolds with @tool decorator and TODOs for teammates"
```

---

### Task 3: Ingestion Pipeline Scaffold (for teammates)

**Files:**
- Create: `src/ingest.py`

- [ ] **Step 1: Create `src/ingest.py`**

```python
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
    # Step 1 — Parse PDFs (extract text + images/diagrams)
    #   Suggested: PyMuPDF4LLM with LLMImageBlobParser for diagrams
    #   See: references/16-pdf-extraction-with-images.md
    #
    #   from langchain_pymupdf4llm import PyMuPDF4LLMLoader
    #   for pdf_path in pdf_files:
    #       loader = PyMuPDF4LLMLoader(pdf_path, extract_images=True, ...)
    #       docs = loader.load()
    #
    # Step 2 — Chunk documents
    #   Suggested: RecursiveCharacterTextSplitter (chunk_size=500, chunk_overlap=50)
    #   See: references/14-chunking-strategies-for-rag.md
    #
    #   from langchain_text_splitters import RecursiveCharacterTextSplitter
    #   splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    #   chunks = splitter.split_documents(docs)
    #
    # Step 3 — Tag chunks with metadata
    #   Each chunk should have: {"source": filename, "page": page_number}
    #
    # Step 4 — Embed and store in ChromaDB
    #   See: references/13-langchain-chroma-integration.md
    #
    #   from langchain_openai import OpenAIEmbeddings
    #   from langchain_chroma import Chroma
    #   embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    #   vector_store = Chroma.from_documents(
    #       chunks, embeddings, persist_directory=persist_dir
    #   )

    print("TODO: Ingestion pipeline chưa được implement.")
    for f in pdf_files:
        print(f"  - {f}")


if __name__ == "__main__":
    ingest_slides()
```

- [ ] **Step 2: Commit**

```bash
git add src/ingest.py
git commit -m "feat: add ingestion pipeline scaffold with TODOs for teammates"
```

---

### Task 4: Agent Core — TDD (Huy implements)

**Files:**
- Create: `tests/test_agent.py`
- Create: `src/agent.py` (replaces `src/agent/agent.py`)

- [ ] **Step 1: Write the failing tests**

Create `tests/test_agent.py`:

```python
"""Unit tests for the AI Tutor agent core."""

import os
import sys

import pytest

# Add src/ to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent import SYSTEM_PROMPT, create_tutor_agent  # noqa: E402


# --- System Prompt Tests ---


class TestSystemPrompt:
    """Verify the system prompt contains all required sections from the spec."""

    def test_has_persona_section(self):
        assert "<persona>" in SYSTEM_PROMPT

    def test_has_rules_section(self):
        assert "<rules>" in SYSTEM_PROMPT

    def test_has_capabilities_section(self):
        assert "<capabilities>" in SYSTEM_PROMPT

    def test_has_constraints_section(self):
        assert "<constraints>" in SYSTEM_PROMPT

    def test_has_output_format_section(self):
        assert "<output_format>" in SYSTEM_PROMPT

    def test_no_fabrication_rule(self):
        assert "NEVER fabricate" in SYSTEM_PROMPT

    def test_citation_requirement(self):
        assert "cite" in SYSTEM_PROMPT.lower() or "Lecture" in SYSTEM_PROMPT

    def test_language_rule(self):
        """Agent must respond in the student's language."""
        assert "language" in SYSTEM_PROMPT.lower()

    def test_no_complete_solutions_constraint(self):
        """Agent must not write full assignment solutions."""
        assert "NEVER write complete code solutions" in SYSTEM_PROMPT

    def test_retry_limit_constraint(self):
        """Agent must stop retrying after 2 failures."""
        assert "2" in SYSTEM_PROMPT and "repeat" in SYSTEM_PROMPT.lower()


# --- Tool Registration Tests ---


class TestToolScaffolds:
    """Verify all tool functions are callable and return strings."""

    def test_search_slides_callable(self):
        from tools.rag import search_slides

        result = search_slides.invoke("test query")
        assert isinstance(result, str)

    def test_search_web_callable(self):
        from tools.web_search import search_web

        result = search_web.invoke("test query")
        assert isinstance(result, str)

    def test_fetch_assignment_callable(self):
        from tools.github import fetch_assignment

        result = fetch_assignment.invoke("https://github.com/test/repo")
        assert isinstance(result, str)

    def test_search_arxiv_callable(self):
        from tools.arxiv_search import search_arxiv

        result = search_arxiv.invoke("test query")
        assert isinstance(result, str)


# --- Agent Creation Tests (requires API key) ---


class TestAgentCreation:
    """Integration tests — require OPENAI_API_KEY to run."""

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY",
    )
    def test_create_tutor_agent_returns_agent(self):
        agent = create_tutor_agent()
        assert agent is not None

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY",
    )
    def test_agent_is_invocable(self):
        agent = create_tutor_agent()
        assert hasattr(agent, "invoke")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/truonghuy/Desktop/C401_E4_Day05 && PYTHONPATH=src python -m pytest tests/test_agent.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'agent'` (because `src/agent.py` doesn't exist yet)

- [ ] **Step 3: Implement `src/agent.py`**

```python
"""
AI Tutor Agent Core — C401 AI in Action.

Creates the tutor agent using LangChain's create_agent with GPT-5-mini
and 4 tools: search_slides, search_web, fetch_assignment, search_arxiv.

Usage:
    from agent import create_tutor_agent
    agent = create_tutor_agent()
    response = agent.invoke({"messages": [{"role": "user", "content": "..."}]})
"""

from dotenv import load_dotenv
from langchain.agents import create_agent

from tools import ALL_TOOLS

load_dotenv()

SYSTEM_PROMPT = """\
<persona>
You are an AI Tutor for the "AI in Action" (C401) course at VinUniversity.
You are patient, encouraging, and knowledgeable about AI/ML concepts.
You are NOT a code-writing service. You are NOT a general-purpose assistant.
</persona>

<rules>
- ALWAYS check retrieved slide context before answering course-related questions.
- ALWAYS cite the source slide and page number when using slide content
  (e.g., "Theo Lecture 03, trang 12...").
- MUST ask a clarifying question when the student's intent is ambiguous —
  do NOT guess and route to the wrong tool.
- MUST respond in the same language the student uses. Default: Vietnamese.
  Use English for technical terms.
- If you cannot find the answer after searching slides AND web, explicitly state:
  "Mình không tìm thấy thông tin này trong tài liệu khoá học."
  Do NOT fabricate an answer.
</rules>

<capabilities>
You have access to the following tools:

1. search_slides: Search course lecture slides stored in a vector database.
   - Use when: student asks about course concepts, theory, definitions,
     examples from lectures.
   - Do NOT use when: question is clearly about external libraries,
     current events, or non-course topics.

2. search_web: Search the internet via Tavily.
   - Use when: student needs info beyond course slides — library docs,
     error debugging, latest framework versions.
   - Do NOT use when: the answer is likely in course slides.

3. fetch_assignment: Read README.md from a GitHub repository.
   - Use when: student shares a GitHub URL or asks about assignment requirements.
   - Do NOT use when: no repo URL is mentioned or relevant.

4. search_arxiv: Search academic papers on arXiv.
   - Use when: student asks about research papers, academic references,
     or cutting-edge AI research.
   - Do NOT use when: question is about practical course content or assignments.
</capabilities>

<constraints>
- NEVER write complete code solutions for assignments. Instead: explain the
  concept, provide pseudocode, give hints, suggest the approach, and let
  the student write the final code.
- NEVER fabricate information, citations, or slide references.
- NEVER answer questions outside the scope of the AI/ML course
  (e.g., politics, sports, cooking). Politely redirect:
  "Mình chỉ hỗ trợ về nội dung khoá học AI in Action thôi nhé!"
- NEVER repeat the same failed search more than 2 times. After 2 failures,
  inform the student and suggest rephrasing.
</constraints>

<output_format>
- Use Markdown: headers, bullet points, code blocks where appropriate.
- Keep answers concise but thorough.
- Structure complex explanations as: concept -> example -> connection to course material.
- When citing slides, use format: **[Lecture X, p.Y]**
</output_format>
"""


def create_tutor_agent():
    """Create and return the AI Tutor agent.

    Returns a compiled agent ready to be invoked via .invoke() or .stream().
    Uses GPT-5-mini with 4 tools and the course-specific system prompt.
    """
    agent = create_agent(
        "openai:gpt-5-mini",
        tools=ALL_TOOLS,
        prompt=SYSTEM_PROMPT,
    )
    return agent
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/truonghuy/Desktop/C401_E4_Day05 && PYTHONPATH=src python -m pytest tests/test_agent.py -v -k "not TestAgentCreation"`

Expected: All `TestSystemPrompt` and `TestToolScaffolds` tests PASS.

(The `TestAgentCreation` tests are skipped unless `OPENAI_API_KEY` is set.)

- [ ] **Step 5: Commit**

```bash
git add tests/test_agent.py src/agent.py
git commit -m "feat: implement agent core with create_agent, system prompt, and tool wiring (TDD)"
```

---

### Task 5: Streamlit UI Scaffold (for teammates)

**Files:**
- Create: `src/app.py`

- [ ] **Step 1: Create `src/app.py`**

```python
"""
AI Tutor — C401 AI in Action — Streamlit Chat UI.

Usage:
    streamlit run src/app.py
"""

import streamlit as st

from agent import create_tutor_agent

# --- Page Config ---
st.set_page_config(page_title="AI Tutor — C401", page_icon="🎓")
st.title("AI Tutor — C401 AI in Action")

# TODO (Teammate): Implement the chat UI
#
# Suggested approach using Streamlit chat components:
#
# 1. Initialize agent in session state (run once):
#    if "agent" not in st.session_state:
#        st.session_state.agent = create_tutor_agent()
#
# 2. Initialize message history:
#    if "messages" not in st.session_state:
#        st.session_state.messages = []
#
# 3. Display chat history:
#    for msg in st.session_state.messages:
#        with st.chat_message(msg["role"]):
#            st.markdown(msg["content"])
#
# 4. Handle user input:
#    if prompt := st.chat_input("Hỏi mình về khoá học AI in Action..."):
#        st.session_state.messages.append({"role": "user", "content": prompt})
#        with st.chat_message("user"):
#            st.markdown(prompt)
#
#        # 5. Get agent response (streaming):
#        with st.chat_message("assistant"):
#            response = st.session_state.agent.invoke(
#                {"messages": [{"role": "user", "content": prompt}]}
#            )
#            # Extract the final message content from response
#            # st.markdown(response_content)
#
#        st.session_state.messages.append(
#            {"role": "assistant", "content": response_content}
#        )

st.info("🚧 Chat UI chưa được implement. Xem TODOs trong source code.")
```

- [ ] **Step 2: Commit**

```bash
git add src/app.py
git commit -m "feat: add Streamlit UI scaffold with TODOs for teammates"
```

---

### Task 6: Cleanup Old Files

**Files:**
- Remove: `src/agent/agent.py` (replaced by `src/agent.py`)
- Remove: `src/agent/` directory

The old `src/agent/agent.py` used a manual LangGraph StateGraph approach. The approved spec uses `create_agent` instead. The new implementation lives at `src/agent.py`.

- [ ] **Step 1: Remove old agent directory**

```bash
git rm src/agent/agent.py
rmdir src/agent 2>/dev/null || true
```

- [ ] **Step 2: Run tests one final time to confirm nothing broke**

Run: `cd /Users/truonghuy/Desktop/C401_E4_Day05 && PYTHONPATH=src python -m pytest tests/test_agent.py -v -k "not TestAgentCreation"`

Expected: All tests PASS.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove old LangGraph agent skeleton, replaced by create_agent approach"
```

---

## Summary of What's Implemented vs. Scaffolded

| Component | File | Status | Owner |
|---|---|---|---|
| Agent core + system prompt | `src/agent.py` | **Implemented** | Huy |
| Unit tests | `tests/test_agent.py` | **Implemented** | Huy |
| RAG tool | `src/tools/rag.py` | Scaffold + TODO | Teammate |
| Web search tool | `src/tools/web_search.py` | Scaffold + TODO | Teammate |
| GitHub tool | `src/tools/github.py` | Scaffold + TODO | Teammate |
| ArXiv tool | `src/tools/arxiv_search.py` | Scaffold + TODO | Teammate |
| Ingestion pipeline | `src/ingest.py` | Scaffold + TODO | Teammate |
| Streamlit UI | `src/app.py` | Scaffold + TODO | Teammate |
| Project infra | `.env.example`, `requirements.txt` | **Implemented** | Huy |
