# Technical & Architecture Documentation

Tài liệu này mô tả chi tiết về cấu trúc kỹ thuật, kiến trúc hệ thống và luồng dữ liệu (Data Flow) của dự án **AI Tutor**.

## 1. Directory Tree (Cấu Trúc Thư Mục)

Dự án được tổ chức theo module, tách biệt giữa logic Agent, các công cụ (Tools) và cấu hình.

```text
C401_E4_Day05/
│
├── .gitignore               # Cấu hình bỏ qua các file không cần thiết trên git
├── NhomE4-C401/             # Tài liệu, bản nháp (Spec/Canvas draft) của nhóm
├── canhan/                  # Không gian làm việc cá nhân của các thành viên
└── src/                     # Source code chính của dự án
    ├── .env                 # File chứa các biến môi trường (API Keys, Config)
    ├── handoff.md           # Tài liệu Handoff & Phân công công việc
    │
    ├── agent/               # Thư mục chứa logic lõi của hệ thống Agent
    │   └── agent.py         # File khởi tạo LangGraph, định nghĩa State, Node, và Edge
    │
    └── tools/               # Thư mục chứa các công cụ hỗ trợ cho Agent
        ├── rag.py           # Công cụ RAG (Chroma/Qdrant) để truy xuất dữ liệu từ Slide
        ├── web_search.py    # (Dự kiến) Công cụ tìm kiếm Web (Tavily/SerpAPI)
        └── github.py        # (Dự kiến) Công cụ giao tiếp với Github repo assignment
```

## 2. Technical Architecture (Kiến Trúc Kỹ Thuật)

Hệ thống được thiết kế theo hướng **Stateful Agentic Workflow**, với thành phần trung tâm là LangGraph để kiểm soát chu trình suy luận của AI.

### 2.1. Core Components (Các Thành Phần Cốt Lõi)
- **Cơ sở dữ liệu (Database):**
  - **Vector DB (ChromaDB / Qdrant):** Chứa các nội dung từ slide bài giảng đã được chunk & embedding. Dùng để tìm kiếm ngữ nghĩa theo thời gian thực (Realtime Semantic Search).
- **Agent Orchestrator:**
  - **LangGraph:** Quản lý quy trình hội thoại (State) và tính toán State trung gian (Reducer). Bọc (Wrap) LLM `gpt-5-nano` để nó có thể ra quyết định gọi Tool nào, dựa trên prompt hiện tại.
- **Tools (Các kỹ năng của Agent):**
  - **Slide Retrieval (RAG):** Cung cấp kiến thức độc quyền, chính xác từ giáo trình (Domain-specific).
  - **Web Retrieval:** Quét thông tin mới trên mạng (hỗ trợ cho những lỗi/kiến thức lập trình bổ sung nếu user hỏi lệch ra khỏi slide nhưng vẫn trong môn học).
  - **Github Assignment Integration:** Nắm bắt context của bài tập sinh viên đang làm.

### 2.2. Data & Execution Flow (Luồng Xử Lý Dữ Liệu)

```mermaid
graph TD;
    User[Sinh Viên] -->|Hỏi bài / Nhờ xem assignment| Agent[Agent Interceptor (LangGraph)]
    Agent -->|Kiểm tra Intent| Router{Router Decision}
    Router -->|Cần kiến thức trong khóa| RAG[RAG Tool]
    Router -->|Cần thông tin bên ngoài| WebSearch[Web Search Tool]
    Router -->|Cần xem code/yêu cầu| Github[Github Tool]
    
    RAG -->|Trích xuất Context| VectorDB[(Slide Vector DB)]
    VectorDB --> RAG
    
    RAG --> Agent_Reasoning[LLM Reasoning & Synthesis]
    WebSearch --> Agent_Reasoning
    Github --> Agent_Reasoning
    
    Agent_Reasoning -->|Định dạng / Gợi ý (Không trọn vẹn lời giải)| User
    
    User -->|Feedback Sai/Thiếu| Feedback[Logging System]
    Feedback -->|Learning Signal| DB[(Log DB)]
```

## 3. Quản Lý Trạng Thái (State Management & Mitigations)

Vì đây là môi trường hội thoại liên tục, việc quản lý **State** trong `agent.py` rất quan trọng:
- **State Schema:** Bao gồm `conversation_history`, `current_intent`, `internal_monologue` (suy nghĩ nháp), và `retrieved_context`.
- **Merge Logic:** Các bước gọi tool kết thúc sẽ gọi operator để `append` thêm thông tin vào context thay vì đè nội dung cũ, giúp Agent không bị "bệnh mất trí nhớ" (State Inconsistency).
- **Safety / Hard-Break:** Cấu hình Graph không được lặp lại chu kỳ Reasoning quá N lần (Recursion Limit = 3) để tránh tốn token do lặp vòng kín (Infinite Loop).
