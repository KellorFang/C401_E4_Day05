# Individual reflection — 2A202600104_LeQuyCong

## 1. Role
Thuyết trình + report. Theo dõi tiến trình của nhóm.

## 2. Đóng góp cụ thể
- Hoàn thiện phần spec-final.md
- Hoàn thiện phần report
- Slide demo 

## 3. SPEC mạnh/yếu
- Mạnh nhất: Thiết kế hệ thống Rich Metadata (page number, lecture date) kết hợp với Visual Slide Discovery UX. Điều này giúp học viên không chỉ nhận được câu trả lời dạng văn bản mà còn thấy được đúng hình ảnh slide gốc để đối chiếu, giải quyết triệt để pain point tra cứu thủ công.

- Yếu nhất: Phần quản lý Cost và Latency vẫn còn dựa trên ước tính lý thuyết (GPT-5-mini), chưa có dữ liệu benchmark thực tế khi gọi đồng thời 4 tools (RAG, Web, Github, ArXiv) trong một ReAct loop phức tạp.

## 4. Đóng góp khác
- Hệ thống hóa toàn bộ tài liệu kỹ thuật từ Day 5 sang bản SPEC finale, đảm bảo tính nhất quán giữa giao diện UI, logic Agent và các công cụ Tools.
- Trực quan hóa kiến trúc hệ thống bằng sơ đồ Mermaid và quản lý các tài nguyên demo (ảnh, slide) trong file đặc tả.
- Phối hợp cùng nhóm để tối ưu hóa System Prompt theo cấu trúc 5-layer anatomy, giúp Agent định tuyến chính xác giữa RAG và Web search.


## 5. Điều học được
Học được kinh nghiệm tối ưu prompt, cách thiết kế hệ thống một hệ thống AI Agent.

## 6. Nếu làm lại
Hoàn thiện phần RAG nhanh hơn để có thời gian hoàn thiện phần UI với các feedback của người dùng tốt hơn.

## 7. AI giúp gì / AI sai gì
- **Giúp:** dùng Claude để brainstorm failure modes, gợi ý hệ thống hoàn chỉnh.

- **Sai/mislead:** Gợi ý prompt nhưng quá dài, không đánh trực tiếp vào vấn đề cần giải quyết 