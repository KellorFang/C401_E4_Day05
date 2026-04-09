# Prototype — AI Tutor C401

## Mo ta
Chatbot giup sinh vien khoa "AI in Action" (C401) tai VinUniversity hieu bai sau
lecture. Sinh vien hoi cau hoi -> AI tim slide lien quan qua RAG, tra web, tim paper
tren arXiv -> tra loi kem trich dan slide cu the (lecture, trang, ngay).
AI chi goi y va giai thich (augmentation), khong bao gio viet code ho (khong automation).

## Level: Working prototype
- UI: Streamlit chat app chay duoc local
- 1 flow chinh chay that: nhap cau hoi -> agent chon tool (RAG/Web/ArXiv) -> tra loi kem citation
- RAG: 581 chunks tu 330 slides (B1-B5), ChromaDB local
- Agent: GPT-4o-mini voi ReAct loop (LangChain `create_agent`)

## Links
- Prototype: chay local `cd src && streamlit run app.py`
- Spec chi tiet: xem file `specs/PROTOTYPE_README.md`
- Final spec: xem file `final-spec.md`
- Demo slide: xem file `demo-slide.pdf`

## Tools
- UI: Streamlit
- AI: OpenAI GPT-4o-mini (agent + embeddings text-embedding-3-small)
- RAG: ChromaDB (local, in-process) + RecursiveCharacterTextSplitter
- Web search: Tavily API
- Academic search: ArXiv Retriever (LangChain)
- Tracing: LangSmith
- Framework: LangChain (create_agent, tool binding, ReAct loop)

## Phan cong
| Thanh vien | Phan | Output |
|-----------|------|--------|
| Huy | Agent core + system prompt + ingestion + UI + tests | `agent.py`, `ingest.py`, `tools/rag.py`, `app.py`, `tests/test_agent.py` |
| Teammate | Web search tool + ArXiv tool | `tools/web_search.py`, `tools/arxiv_search.py` |
| Teammate | GitHub tool (scaffold) | `tools/github.py` (TODO) |
