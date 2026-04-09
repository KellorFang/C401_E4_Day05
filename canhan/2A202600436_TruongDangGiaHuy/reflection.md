# Individual reflection — Trương Đặng Gia Huy

## 1. Role
Agent architect + backend engineer. Phụ trách thiết kế agent core, system prompt, Streamlit UI, và viết tests.

## 2. Đóng góp cụ thể
- Thiết kế và implement agent core (`agent.py`): dùng `create_agent` với GPT-4o-mini, wire 4 tools
- Viết system prompt theo cấu trúc XML 5 lớp (Persona → Rules → Capabilities → Constraints → Output Format), áp dụng meta-prompting technique và guardrails cụ thể (không viết code hộ, phải cite source, phải hỏi lại khi ambiguous)
- Scaffold các tool của teammate (web search, arxiv, github) với @tool decorator + TODO rõ ràng
- Xây dựng Streamlit chat UI (`app.py`) với session state, chat history, loading spinner
- Viết 14 unit tests (`tests/test_agent.py`) chạy offline không cần API key

## 3. SPEC mạnh/yếu
- Mạnh nhất: RAG pipeline và system prompt
  - RAG: slides 90% là hình nên phải dùng RapidOCR thay vì parser thường. Pipeline: PDF → OCR → recursive chunking → embedding → ChromaDB với rich metadata (source, page number) cho phép cross-check và reference chính xác
  - System prompt: dùng meta-prompting technique với XML structure 5 lớp, có guardrails cụ thể (không fabricate, phải cite, hỏi lại khi không rõ), tool routing rules với when/when-not cho từng tool
- Yếu nhất: UI — hiện tại chỉ có Streamlit chat đơn giản. Muốn làm thêm embedded slide viewer (hiện slide image từ metadata), interactive quiz components, và các UI elements phong phú hơn nhưng chưa kịp implement

## 4. Đóng góp khác
- Viết technical spec chi tiết (`technical_spec.md`) với architecture diagram, component interfaces, failure modes
- Review và integrate teammate's RAG implementation, rename function cho compatible

## 5. Bài học
Khi thiết kế RAG cho tài liệu nhiều hình ảnh, không thể dùng text parser thường — cần OCR (RapidOCR) để extract nội dung. Việc gắn metadata (source file, slide number) vào từng chunk từ đầu giúp việc citation và cross-reference dễ dàng hơn nhiều về sau, thay vì phải re-ingest.

System prompt không chỉ là "viết một đoạn text" — cần có cấu trúc rõ ràng (persona, rules, capabilities, constraints, output format) và guardrails cụ thể để agent hoạt động đúng như mong muốn.

## 6. Nếu làm lại
- Test sớm hơn: nên test prompt và RAG pipeline từ tối Day 5 thay vì chỉ viết spec, để có thêm 2-3 vòng iterate
- Sync nhiều hơn với teammate: coordinate thường xuyên hơn về tool implementation để tránh conflict (ví dụ: teammate implement RAG khác interface, phải rename và integrate lại)
- Đơn giản hoá scope ban đầu: bắt đầu với ít tool/feature hơn (chỉ RAG + web search), chạy ổn định rồi mới thêm arxiv và github tool

## 7. AI giúp gì / AI sai gì
- **Giúp:** dùng Claude để scaffold project structure, viết test cases, và brainstorm failure modes (Claude gợi ý được các edge case như "semantic routing failure khi câu hỏi ambiguous" mà nhóm chưa nghĩ tới).
- **Sai/mislead:** Claude gợi ý thêm nhiều future features (knowledge review mode, learning mode, slide viewer) vào spec — nghe hay nhưng scope quá lớn cho thời gian thực tế. Phải tự quyết định đâu là MVP và đâu là roadmap. Bài học: AI brainstorm tốt nhưng không biết giới hạn scope và deadline, mình phải là người giữ scope.
