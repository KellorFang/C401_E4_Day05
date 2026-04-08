
# Top 3 Failure Modes trong LangGraph Agent

---

## 1. Vòng lặp vô tận (Infinite Loops)

Trong LangGraph, việc cho phép các nút (nodes) quay lại các nút trước đó (cycles) là một tính năng mạnh mẽ nhưng cũng là "con dao hai lưỡi".

### Trigger

Khi sinh viên đưa ra một câu hỏi mơ hồ hoặc Agent không tìm thấy câu trả lời trong tài liệu bài giảng (RAG), nút `Reasoning` có thể liên tục yêu cầu nút `Retrieval` tìm kiếm lại với các từ khóa tương tự mà không có điều kiện dừng rõ ràng.

### Hệ quả

- Gây lãng phí Token và tăng chi phí API đột biến.
- Hệ thống bị treo hoặc trả về lỗi `RecursionLimitReached` (mặc định là 25 bước trong LangGraph).

### Mitigation

- Thiết kế một nút **"Escalation"** (Chuyển tiếp): Nếu số lần lặp lại một tác vụ vượt quá 3 lần, Agent phải tự động trả lời: *"Tôi không tìm thấy thông tin cụ thể, bạn có muốn thảo luận về khía cạnh khác không?"*
- Cấu hình `config={"recursion_limit": N}` một cách chặt chẽ.

---

## 2. State Inconsistency & Overwriting

LangGraph dựa vào một đối tượng `State` chung được truyền qua các nút. Lỗi thường xảy ra khi cập nhật trạng thái này không đúng cách.

### Trigger

Khi sử dụng các luồng song song (Parallel execution) — ví dụ: một nhánh Agent đang chấm điểm (grading) bài làm của sinh viên, nhánh còn lại đang chuẩn bị gợi ý (hinting). Nếu cả hai cùng ghi đè vào một trường `history` mà không có logic reducer (như `operator.add`), dữ liệu sẽ bị mất.

### Hệ quả

AI Tutor sẽ "quên" những gì nó vừa nói ở bước trước, hoặc phản hồi của nó trở nên rời rạc, không ăn nhập với tiến trình học tập của sinh viên.

### Mitigation

- Hướng dẫn sinh viên cách sử dụng `Annotated` và các hàm reducer để gộp (merge) dữ liệu thay vì ghi đè hoàn toàn.
- Định nghĩa Schema cho `State` rõ ràng: Phân tách rõ giữa `internal_monologue` (suy nghĩ nội bộ của Agent) và `final_response` (phản hồi cho sinh viên).

---

## 3. Semantic Routing Failures

Đây là lỗi logic tại các nút điều hướng (Conditional Edges), nơi Agent quyết định bước tiếp theo dựa trên nội dung hội thoại.

### Trigger

AI Tutor không nhận diện được ý định (intent) của sinh viên.

> **Ví dụ:** Sinh viên nói *"Tôi không hiểu"*, nhưng Agent lại hiểu nhầm là sinh viên muốn **"Chuyển sang bài học mới"** thay vì **"Giải thích lại bằng ví dụ dễ hơn"**.

### Hệ quả

Tạo ra trải nghiệm "ông nói gà, bà nói vịt". Tutor đẩy sinh viên đi quá nhanh qua các kiến thức nền tảng hoặc lặp lại những giải thích mà sinh viên đã khẳng định là không hiệu quả.

### Mitigation

- Sử dụng **Structured Output** (Pydantic) cho các nút phân loại ý định để đảm bảo đầu ra của LLM luôn khớp với các cạnh (edges) đã định nghĩa trong đồ thị.
- Thiết lập một nút **"Check-point"**: Sau mỗi 2–3 bước giải thích, Tutor phải hỏi xác nhận mức độ hiểu bài của sinh viên trước khi di chuyển đến nút nội dung tiếp theo.
***5. ROI 3 KỊCH BẢN***
## Đề tài: AI tutor bài giảng cho sinh viên

|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | 80 sinh viên dùng thử, 40% engage thường xuyên. Chỉ pilot 1–2 môn, nội dung hạn chế. | 400 sinh viên active, 65% engage thường xuyên. Triển khai 5–6 môn, TA giảm tải rõ rệt. | 1.500 sinh viên active (~40% VinUni), 80% engage thường xuyên. Triển khai toàn trường + license cho trường đối tác (Year 2+). |
| **Cost** | 80 SV × 20 phút tiết kiệm = 26.7 giờ/ngày → ~$214 | 400 SV × 25 phút = 167 giờ/ngày → ~$1.336 + TA giảm 2h/ngày ($20/h) = ~$40 → Tổng ~$1.376| 1.500 SV × 30 phút = 750 giờ/ngày → ~$6.000 + doanh thu license → Tổng ~$6.450 |
| **Benefit** | Mỗi user tiết kiệm 15 phút/ngày → 12.5 giờ/ngày tổng | 58 giờ/ngày | 425 giờ/ngày |
| **Net** | +$184 | +$1.226 | +$6.000 |

**Kill criteria:**: Dừng dự án nếu sau 4 tuần pilot:
- Tỷ lệ sinh viên quay lại dùng lần 2 < 40% (low retention = sản phẩm không có giá trị thực)
- Độ chính xác trả lời của AI < 70% theo đánh giá của giảng viên (AI sai nhiều = hại hơn lợi)
- Cost/ngày vượt quá benefit 2 tháng liên tục