# Tài Liệu Test Case & Hướng Dẫn Kiểm Thử (AI Tutor)

Tài liệu này cung cấp các kịch bản kiểm thử (test cases) tiêu chuẩn để Tester hoặc QC tuân theo nhằm đảm bảo tính ổn định của các công cụ (Tools) và chất lượng đầu ra của sản phẩm (AI Tutor Agent).

---

## 1. Kiểm Thử Công Cụ (Tool Testing - Isolation/Unit Test)

Phần này kiểm tra độc lập từng kỹ năng của Agent xem có hoạt động đúng mong đợi hay không.

### 1.1. RAG Tool (Slide Retrieval)
- **TC_RAG_01 (Happy Path):** Nhập câu hỏi có từ khóa rõ ràng (VD: *"LangGraph là gì?"*).
  - *Kỳ vọng:* Tool trả về đúng đoạn text/context được trích xuất từ tài liệu slide khóa học chứa thông tin định nghĩa LangGraph.
- **TC_RAG_02 (Out of Domain):** Nhập câu hỏi không có trong khóa học (VD: *"Cách nấu cơm gà?"*).
  - *Kỳ vọng:* Tool trả về mảng rỗng hoặc thông báo không tìm thấy ngữ cảnh phù hợp trong Vector DB.
- **TC_RAG_03 (Ambiguous Query):** Nhập từ khóa viết tắt hoặc có lỗi đánh máy (VD: *"lnGrap"*).
  - *Kỳ vọng:* Tool dựa vào semantic (nhúng ngữ nghĩa) nên vẫn có khả năng fetch ra được context liên quan đến LangGraph.

### 1.2. Web Search Tool (Tavily/SerpAPI)
- **TC_WEB_01 (Current Knowledge):** Nhập yêu cầu tìm kiếm sự kiện mới xảy ra, hoặc phiên bản thư viện mới nhất.
  - *Kỳ vọng:* Trả về thông tin chính xác kèm theo nguồn trích dẫn (URL).

### 1.3. Github Assignment Tool
- **TC_GIT_01 (Fetch Repository):** Cung cấp link Github repo hợp lệ của bài tập.
  - *Kỳ vọng:* Tool đọc được file `README.md` hoặc các file requirements của bài tập.
- **TC_GIT_02 (Invalid/Private Repo):** Cung cấp link repo không tồn tại hoặc private chưa cấp quyền.
  - *Kỳ vọng:* Trả về mã lỗi rõ ràng để Agent có thể gợi ý User cấu hình lại quyền truy cập (không chét/crash code).

---

## 2. Kiểm Thử Sản Phẩm (End-to-End Product Testing)

Kiểm tra luồng nghiệp vụ tổng thể khi học viên giao tiếp qua giao diện chat.

### 2.1. Kiểm tra kịch bản thông thường (Happy Path)
- **TC_E2E_01 (Onboarding):** Học viên bắt đầu bằng câu "Chào bạn".
  - *Kỳ vọng:* Agent tự giới thiệu là AI Tutor và hỏi học viên cần hỗ trợ bài học hay assignment nào.
- **TC_E2E_02 (Tra cứu lý thuyết):** Học viên hỏi *"Xin giải thích lại cơ chế Attention trong Transformer"*.
  - *Kỳ vọng:* Agent gọi RAG Tool $\rightarrow$ Tổng hợp kiến thức $\rightarrow$ Trả lời dễ hiểu kèm ví dụ minh họa và **trích dẫn cụ thể slide bài giảng**.

### 2.2. Kiểm tra tính chất Augmentation (Thay vì Automation)
- **TC_AUG_01 (Làm hộ bài tập - Không được phép):** Học viên yêu cầu: *"Viết cho tôi đoạn code hoàn chỉnh để giải bài tập 3 trong repo này"*.
  - *Kỳ vọng:* Agent từ chối viết code giải hoàn chỉnh. Thay vào đó, Agent phân tích yêu cầu bài 3, cung cấp gợi ý, framework, hoặc mã giả (pseudocode), hướng dẫn học viên tự viết.

### 2.3. Quản lý trạng thái và bối cảnh (State Consistency)
- **TC_STATE_01 (Follow-up Question):** 
  - Bước 1: Hỏi: *"Dữ liệu Tabular là gì?"* (Agent giải thích xong).
  - Bước 2: Hỏi tiếp: *"Tại sao XGBoost lại tốt hơn thuật toán khác trên loại dữ liệu này?"* (Không nhắc lại chữ "Tabular").
  - *Kỳ vọng:* Agent hiểu "loại dữ liệu này" là "Tabular data" và giải thích chính xác, nhờ tính năng ghép history (Memory/State).

---

## 3. Kiểm Thử Rủi Ro Chuyên Sâu (Failure Modes)

Bao gồm các Test case kiểm tra các rủi ro hệ thống đã được nhận diện trong tài liệu kiến trúc.

### 3.1. Routing & Lặp Vô Tận (Infinite Loop & Semantic Routing)
- **TC_FAIL_01 (Kẹt RAG):** Cố tình hỏi những câu hỏi có vẻ liên quan nhưng thực chất không có trong slide (VD: *"Thầy giáo tên gì"*, *"Slide có format font chữ là bao nhiêu"*).
  - *Kỳ vọng:* Agent thử tìm kiếm (gọi RAG) vài lần. Tuy nhiên, sau tối đa 3 lần lặp (hoặc recursion threshold) không có kết quả, Agent phải chủ động chuyển hướng: *"Tôi không tìm thấy thông tin được yêu cầu trong bài giảng. Bạn có muốn đổi sang chủ đề khác không?"*.
- **TC_FAIL_02 (Fail Routing Intent):** Nhắn nhập nhằng kiểu: *"Vấn đề này hôm qua giải ra nhưng nay nhập lại báo lỗi"* (Vừa nhắc chuyện cũ vừa nói đến code báo lỗi, không rõ intent là giải thích khái niệm hay debug).
  - *Kỳ vọng:* Khối Routing (Edges) không bị hoảng. Thay vì chốt luồng sai, Agent dừng lại và sử dụng Check-point để hỏi xác nhận: *"Bạn đang muốn giải thích lại khái niệm này hay muốn mình giúp debug đoạn code?"*.

### 3.2. Thu thập Tín Hiệu Phản Hồi (Learning Signals)
- **TC_FB_01 (Ghi log người dùng báo sai):** 
  - Sau khi Agent trả lời, người dùng click nút "👎 Sai kiến thức" (hoặc chat: *"Câu trả lời sai rồi. Slide bảo thế này cơ mà."*).
  - *Kỳ vọng:* (1) Hệ thống phản hồi lịch sự xin lỗi và đưa ra giải pháp check lại. (2) Database Log hệ thống ghi nhận lại cặp `(Nội dung câu trả lời - Lỗi phàn nàn)` dưới dạng tín hiệu để kỹ sư huấn luyện / cải thiện sau này.


## Note:

Đây chỉ là yêu cầu mẫu về test case, mọi người cần viết docs riêng quá trình test và kết quả test.