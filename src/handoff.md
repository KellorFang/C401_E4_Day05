# Tài Liệu Handoff: AI Tutor - Khoá học AI in Action

## 1. Tổng Quan Dự Án (Project Overview)
**AI Tutor** là một assistant Agent hướng tới học viên của khoá học AI in Action. 
- **Vấn đề (Pain point):** Sau buổi học lý thuyết, học viên thường chưa nắm rõ ngay hoặc gặp khó khăn khi làm assignment. Việc phải tra cứu lại nhiều slide lý thuyết mất thời gian và ngắt quãng luồng tư duy.
- **Giải pháp:** Agent giúp hỏi đáp kiến thức, giải thích nhanh các khái niệm, đưa ra ví dụ, gợi ý bài tập tương tự. Agent cũng có quyền truy cập repo Github để hỗ trợ assignment.
- **Cơ chế hoạt động:** **Augmentation** - AI gợi ý, đưa ra lời giải thích và học viên sẽ là người quyết định và làm bài cuối cùng. Automation ở khía cạnh tìm kiếm lý thuyết/slide.

## 2. Kiến Trúc & Công Nghệ (Tech Stack)
- **Mô hình Ngôn ngữ (LLM):** `gpt-5-nano`.
- **Core Framework:** LangGraph để quản lý luồng hội thoại và tư duy của Agent (Reasoning, Routing).
- **Công cụ (Tools):**
  - **Tavily Search:** Tìm kiếm thông tin mở rộng trên web.
  - **RAG (Retrieval-Augmented Generation):** Dùng ChromaDB hoặc Qdrant để trích xuất nội dung từ Slide khoá học. Đầu vào là domain-specific data nội bộ.
  - **Feedback & Logging:** Hệ thống thu thập phản hồi của user (đúng/sai, hài lòng/không) để cải thiện mô hình.
  - **GitHub Tool:** Truy cập đọc yêu cầu assignment.

## 3. Phân Công Công Việc (Task Assignments)
Dự án được chia task theo các cụm chức năng chính:
- **System prompt + LangGraph (1 người):** Xây dựng luồng hội thoại, thiết kế `State` để tránh mất bối cảnh (State inconsistency), xử lý định tuyến (Semantic Routing).
- **Search slide - RAG (2 người):** Xây dựng chunking, embedding, luồng truy xuất (Retrieval) nội dung slide.
- **Search web + Git (2 người):** Tích hợp công cụ tìm kiếm trên web và kết nối repo Github để hỗ trợ làm assignment.
- **Feedback - Monitoring (1 người):** Xây dựng cơ chế bắt logging, đo lường các learning signals (số lần report sai, tỷ lệ sửa lỗi).
- **Testing (1 người):** Test unit cho tool, test end-to-end, và đặc biệt là test các Failure Modes.

## 4. Rủi Ro Thường Gặp & Cách Khắc Phục (Failure Modes & Mitigations)
Theo phân tích thiết kế, người xây dựng LangGraph cần đặc biệt chú ý 3 lỗi sau:
1. **Vòng lặp vô tận (Infinite Loops):** Agent bị kẹt khi RAG không tìm ra kết quả.
   *Khắc phục:* Thiết lập `recursion_limit` và thêm nút "Escalation" sau 3 lần thất bại để báo cho người dùng hoặc đề xuất đổi câu hỏi.
2. **Quên bối cảnh (State Inconsistency):** Xung đột khi ghi đè State ở các luồng xử lý song song.
   *Khắc phục:* Dùng `reducer` phù hợp trong LangGraph State (ví dụ `operator.add` cho history).
3. **Điều hướng sai (Semantic Routing Failures):** AI hiểu sai ý định của user dẫn đến chạy sai luồng.
   *Khắc phục:* Bắt buộc xuất ra `Structured Output (Pydantic)` khi phân loại ý định, thêm các bước Check-point hỏi lại người dùng.

## 5. Tiêu Chuẩn Đánh Giá (Learning Signals & Success)
- **Learning Signals:** Mọi dự đoán sai rớt vào luồng user correction cần được ghi log. Đếm số lần user không hài lòng để tối ưu lại prompt hoặc RAG.
- **Kill criteria (Tiêu chí dừng pilot):** 
  - Tỷ lệ quay lại dùng (retention) < 40%.
  - Độ chính xác đánh giá bởi Giảng viên/TA < 70%.
