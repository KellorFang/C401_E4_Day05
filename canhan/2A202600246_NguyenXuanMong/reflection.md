# Báo Cáo Cá Nhân - Reflection
**Họ và tên:** Nguyễn Xuân Mong  
**Mã sinh viên:** 2A202600246  
**Project:** AI Tutor cho học viên khoá học được thiết kế sẵn (cụ thể: khoá AI in Action)

---

### 1. Role cụ thể trong nhóm
Trong dự án, role cụ thể của em là **Phát triển RAG Tool (RAG Tool Developer)**. Nhiệm vụ trọng tâm là thiết kế, xây dựng và tối ưu hệ thống trích xuất dữ liệu cũng như rà soát (debug) tiến trình đọc-hiểu dữ liệu (Retrieval) để tích hợp thành công vào AI Agent của nhóm.

### 2. Phần phụ trách cụ thể
- **Thực nghiệm và thiết kế Trích xuất dữ liệu (Data Extraction):** Dưới sự phối hợp rà soát và gợi ý thư viện từ hai thành viên Nhật Hoàng và Trương Huy, em đã tiến hành thực nghiệm và xây dựng thành công bộ công cụ `ocr_pdf.py` sử dụng framework PyMuPDF để bóc tách chính xác text, cấu trúc slide và loại bỏ nhiễu dư thừa. (Output: Luồng ingestion sinh ra file `.md` chứa metadata Số bài, Số Slide).
- **Phát triển Data Chunking theo ngữ cảnh:** Thay vì cắt chữ ngẫu nhiên cứng nhắc, em thiếp lập luồng chia nhỏ văn bản theo ranh giới từng Slide (Slide-aware chunking). (Output: Kho dứ liệu đầu vào tương thích 100% với Vector Database).

### 3. SPEC phần nào mạnh nhất, phần nào yếu nhất? Vì sao?
- **Phần mạnh nhất - SPEC Data Ingestion & RAG Tooling:** Do được đầu tư rất lớn vào khâu phân tích PDF và thực nghiệm framework, dữ liệu được xử lý từ gốc rất sạch và có cấu trúc chặt chẽ. Hệ thống RAG tool nhờ vậy mà đảm bảo được khả năng truy xuất chính xác cao, trích dẫn đúng nguồn gốc dữ liệu.
- **Phần yếu nhất - SPEC Agent Orchestration:** He thống hiện tại đang triển khai theo kiến trúc Single Agent. Do phải ôm đồm quá nhiều công cụ và xử lý luồng thao tác kéo dài (long-running tasks) trên một luồng duy nhất, điều này dễ dẫn đến các lỗi liên quan đến cách ly ngữ cảnh (context isolation) và bị tràn cửa sổ ngữ cảnh.

### 4. Đóng góp cụ thể khác với mục 2
- **Hỗ trợ Code và Debug mảng Retrieval:** Bên cạnh tác vụ độc lập, em đóng vai trò hỗ trợ các thành viên khác debug chéo (cross-debug) cho mã nguồn hệ thống Retrieval. Em đã hỗ trợ tái cấu trúc cách gọi model nhúng, sửa lỗi kết nối Hybrid Search, và khắc phục những lỗi version khi đồng bộ codebase của cá nhân em với khung làm việc chung của cả nhóm.

### 5. 1 điều học được trong Hackathon mà trước đó chưa biết
**Tư duy Thực nghiệm (Experimentation Mindset) thông qua cộng tác:** Trước đây em thường có thói quen giải quyết vấn đề theo một framework quen thuộc. Nhưng thông qua sự định hướng và gợi ý liên tục từ Nhật Hoàng và Trương Huy (đề xuất PyMuPDF để chống lỗi layout), em học được cách benchmark nhiều giải pháp cùng lúc trước khi bắt tay vào code ứng dụng một giải pháp khó nhằn.

### 6. Nếu làm lại, đổi gì?
**Chuyển quy mô từ Single Agent sang Multi-Agent Architecture.** 
Thay vì để một Agent duy nhất ôm hết tác vụ (vừa trò chuyện, vừa gọi RAG tool, vừa xử lý logic) giống hiện tại, em sẽ chia nhỏ thành nhiều Agent phân luồng chuyên biệt. Việc này sẽ giúp **giảm context isolation** (mỗi Agent chỉ tập trung xử lý một vùng kiến thức/ngữ cảnh nhất định) và **tối ưu cho các long-running tasks** không bị treo hệ thống hoặc quên mất yêu cầu gốc ban đầu.

### 7. AI giúp gì? AI sai/mislead ở đâu?
- **AI giúp gì:** AI là trợ thủ đắc lực trong việc **gợi ý các thư viện** và **phân tích logic** cách thức thiết lập luồng trích xuất tài liệu phức tạp. Nó giúp em lên ý tưởng cấu trúc các class cho Tool, generate cực nhanh cấu trúc Regex, cũng như hỗ trợ boilerplate code để hoàn thành framework Ingestion một cách thần tốc.
- **AI sai/mislead ở đâu:** 
  - Đôi khi AI cho ra những đoạn code sử dụng **các thư viện không phù hợp, quá mới, hoặc không tương thích** với bộ công cụ hiện tại của dự án. 
  - Về tính logic, khi em yêu cầu một phương thức trích xuất dữ liệu ảnh **ưu tiên ít tốn tài nguyên hệ thống (Local CPU)**, AI lại "ảo giác" và liên tục hướng dẫn dùng các **phương pháp cực tốn chi phí** (như gọi request qua API Vision của bên thứ 3) hoặc bắt buộc hệ thống **phải có GPU rời** để chạy qua các mạng học sâu nặng nề. Về sau em phải tự chủ động định hướng lại AI để sử dụng phương án nhẹ nhàng hơn.
