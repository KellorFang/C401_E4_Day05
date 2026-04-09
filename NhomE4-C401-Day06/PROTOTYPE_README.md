# Prototype — AI Tutor C401

## Mô tả
Chatbot giúp sinh viên khoá "AI in Action" (C401) tại VinUniversity hiểu bài sau
lecture. Sinh viên hỏi câu hỏi → AI tìm slide liên quan qua RAG, tra web, tìm paper
trên arXiv → trả lời kèm trích dẫn slide cụ thể (lecture, trang, ngày).
AI chỉ gợi ý và giải thích (augmentation), không bao giờ viết code hộ (không automation).

## Level: Working prototype
- UI: Streamlit chat app chạy được local
- 1 flow chính chạy thật: nhập câu hỏi → agent chọn tool (RAG/Web/ArXiv) → trả lời kèm citation
- RAG: 581 chunks từ 330 slides (B1-B5), ChromaDB local
- Agent: GPT-4o-mini với ReAct loop (LangChain `create_agent`)

## Links
- Prototype: chạy local `cd src && streamlit run app.py`
- Spec chi tiết: xem file `technical_spec.md`
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

## Phân công
| Thành viên | Phần | Output |
|-----------|------|--------|
| Trương Đặng Gia Huy | Agent core + system prompt + UI + tests | `agent.py`, `app.py`, `tests/test_agent.py` |
| Teammate | Web search tool + ArXiv tool | `tools/web_search.py`, `tools/arxiv_search.py` |
| Teammate | GitHub tool (scaffold) | `tools/github.py` |
