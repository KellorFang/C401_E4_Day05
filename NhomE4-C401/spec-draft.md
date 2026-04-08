# AI Product Canvas

**Project:** AI Tutor cho học viên khoá học AI in Action
---
## 1. Canvas
|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi guide** | User nào? Pain gì? AI giải quyết gì mà cách hiện tại không giải được? | 1. Khi AI sai thì user bị ảnh hưởng thế nào? User biết AI sai bằng cách nào? User sửa bằng cách nào? <br> 2. Khi AI đúng thì user được lợi gì? <br> 3. Khi AI không chắc chắn thì sao? <br> 4. Khi user không hài lòng, mất niềm tin thì sao? | Cost bao nhiêu/request? Latency bao lâu? Risk chính là gì? |
| **Trả lời** | *Học viên sau khi nghe giải thích lý thuyết xong, chưa hiểu rõ hay buổi chiều làm assignment gặp khó khăn, bắt buộc phải xem lại slide để đọc lại kiến thức. <br> <br> AI có thể trả lời câu hỏi của học viên, giải thích lại kiến thức, đưa ra ví dụ, gợi ý bài tập tương tự.* | *1. Khi AI trả lời sai → user có thể làm sai yêu cầu từ assignment, hoặc không hiểu đúng kiến thức. User biết AI sai khi đọc lại slide và thấy khác biệt, hoặc khi làm sai và bị báo lỗi. User sửa bằng cách hỏi lại AI hoặc xem lại slide, báo lỗi trực tiếp cho AI để replan và kiểm tra lại kiến thức.* <br> *2. Khi AI đúng → user được lợi khi có thể trả lời câu hỏi của mình nhanh chóng, không cần xem lại slide, có thể hiểu rõ hơn kiến thức, có thể làm bài tập tốt hơn.* <br> *3. Khi AI không chắc chắn → AI có thể trả lời không , AI sẽ biết mình không chắc chắn và có thể hỏi lại user hoặc xem lại slide.* <br> *4. Khi user không hài lòng, mất niềm tin → có đánh giá sau khi user trả lời xong, nếu user không hài lòng thì AI sẽ replan và kiểm tra lại kiến thức, ghi lại log để cải thiện.* | **cost:** ~$0.001/request <br> <br> **latency**: <1s <br> <br> **risk**: quá context window nếu xử lí tài liệu không tốt, search engine tìm thấy thông tin quá dài* |

---

## Automation hay augmentation?

**Justify:**

*Augmentation — AI gợi ý, hỏi lại xác nhận với user, user quyết định cuối cùng.*

*Automation — quá trình tìm kiếm thông tin từ tài liệu, slide, search engine.*

---

## Learning signal

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | User correction đi vào đâu? | *Mỗi lần user feedback thông tin bị sai → ghi log → dùng để cải thiện model* |
| 2 | Product thu signal gì để biết tốt lên hay tệ đi? | *Đếm log số lần mà user feedback thông tin bị sai, số lần user sửa output, số lần user không hài lòng với output* |
| 3 | Data thuộc loại nào? | *Domain-specific — model trả lời dựa trên tài liệu của khoá học* |

**Có marginal value không?** 

Model có thể biết kiến thức này nhưng chưa chắc đã tuân theo format hay yêu cầu của assignment, chưa biết rõ khoá học có kiến thức chi tiết nào. 

**Ai khác cũng thu được data này không?**

Không vì dựa trên tài liệu nội bộ của khoá học, không public.

---
## 3. Eval metrics

AI tutor hiện có hai tính năng cốt lõi. Với mỗi tính năng, ta cần định nghĩa cụ thể "Báo Nhầm" (False Positive) và "Bỏ Sót" (False Negative) nghĩa là gì.

### Tính năng A: Trích xuất chủ đề từ slide

AI quét slide và quyết định: "Đây là một chủ đề" hoặc "Đây không phải chủ đề."

| | AI nói "Đây LÀ chủ đề" | AI nói "Đây KHÔNG phải chủ đề" |
|---|---|---|
| **Thực sự là chủ đề** | ✅ Đúng (TP) | ❌ **Bỏ Sót (FN)** — sinh viên không thấy chủ đề này, không thể học |
| **Không phải chủ đề** | ❌ **Báo Nhầm (FP)** — sinh viên thấy một chủ đề giả/không liên quan trong danh sách | ✅ Đúng (TN) |

**Loại lỗi nào tệ hơn?**

- **Báo Nhầm (FP):** Sinh viên thấy một chủ đề rác như "chân trang slide" hoặc "tên giảng viên" bị trích xuất thành chủ đề. Khó chịu, nhưng sinh viên có thể bỏ qua.
- **Bỏ Sót (FN):** Một chủ đề thật trên slide bị bỏ lọt hoàn toàn. Sinh viên không biết nó tồn tại — không thể học thứ mình không nhìn thấy. **Cái này tệ hơn.**

**Quyết định: Ưu tiên RECALL cho Trích xuất Chủ đề.**

Thêm vài chủ đề giả thì chấp nhận được. Bỏ sót chủ đề thật nghĩa là sinh viên có lỗ hổng kiến thức mà không hề hay biết.

| Metric | Mục tiêu | Lý do |
|---|---|---|
| Recall | ≥ 95% | Gần như không bao giờ bỏ sót chủ đề thật |
| Precision | ≥ 75% | Một ít nhiễu OK; sinh viên có thể bỏ qua chủ đề không liên quan |

---

### Tính năng B: Hành động trên chủ đề (Giải thích / Đơn giản hóa / Nghiên cứu thêm / Tạo quiz)

Ở đây AI tạo nội dung giáo dục. Câu hỏi "phân loại" trở thành: Output này có đủ tốt để hiển thị cho sinh viên không?

| | AI hiển thị output | AI giấu/cảnh báo output |
|---|---|---|
| **Output đúng & hữu ích** | ✅ Đúng (TP) | ❌ **Bỏ Sót (FN)** — sinh viên không nhận được giải thích hữu ích |
| **Output sai hoặc gây hiểu nhầm** | ❌ **Báo Nhầm (FP)** — sinh viên học thứ SAI | ✅ Đúng (TN) |

**Loại lỗi nào tệ hơn?**

- **Bỏ Sót (FN):** AI quá thận trọng, từ chối giải thích hoặc nói "Tôi không chắc." Sinh viên không được giúp đỡ. Bực mình, nhưng không gây hại — có thể thử lại hoặc hỏi cách khác.
- **Báo Nhầm (FP):** AI tự tin dạy sinh viên thứ **sai về mặt kiến thức**. Sinh viên tin tưởng tutor và ghi nhớ kiến thức sai. **Cái này tệ hơn nhiều.**

**Quyết định: Ưu tiên PRECISION cho Hành động trên Chủ đề.**

AI nói "Tôi không chắc về điều này" tốt hơn nhiều so với tự tin dạy sai.

| Metric | Mục tiêu | Lý do |
|---|---|---|
| Precision | ≥ 95% | Khi AI dạy, phải dạy đúng |
| Recall | ≥ 80% | Vẫn phủ được phần lớn chủ đề, nhưng OK nếu thận trọng với edge case |

---

### Áp dụng vào các **tính năng con** của tutor:

| Tính năng con | User thấy lỗi không? | Chi phí lỗi | Ưu tiên |
|---|---|---|---|
| **Trích xuất chủ đề** | Có — sinh viên thấy danh sách chủ đề | Bỏ sót chủ đề = mất giá trị học tập (FN) | **RECALL** |
| **Đơn giản hóa** | Một phần — sinh viên có thể không phát hiện lỗi tinh vi | Đơn giản hóa sai = hiểu nhầm (FP) | **PRECISION** |
| **Nghiên cứu thêm** | Một phần — sinh viên tin nguồn được trích dẫn | Nguồn bịa = thông tin sai lệch (FP) | **PRECISION** |
| **Tạo quiz** | Có — sinh viên thấy quiz & đáp án | Đáp án sai = sinh viên học sai; nhưng có thể phát hiện | **PRECISION** (nghiêng về) |
| **Giải thích cách khác** | Một phần — phép so sánh có thể gây hiểu nhầm | Phép so sánh tệ = nhầm lẫn, nhưng ít "sai cứng" hơn | **Cân bằng** |

---


## 4. Top 3 Failure Modes trong LangGraph Agent

---

### 4.1. Vòng lặp vô tận (Infinite Loops)

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

### 4.2. State Inconsistency & Overwriting

LangGraph dựa vào một đối tượng `State` chung được truyền qua các nút. Lỗi thường xảy ra khi cập nhật trạng thái này không đúng cách.

### Trigger

Khi sử dụng các luồng song song (Parallel execution) — ví dụ: một nhánh Agent đang chấm điểm (grading) bài làm của sinh viên, nhánh còn lại đang chuẩn bị gợi ý (hinting). Nếu cả hai cùng ghi đè vào một trường `history` mà không có logic reducer (như `operator.add`), dữ liệu sẽ bị mất.

### Hệ quả

AI Tutor sẽ "quên" những gì nó vừa nói ở bước trước, hoặc phản hồi của nó trở nên rời rạc, không ăn nhập với tiến trình học tập của sinh viên.

### Mitigation

- Hướng dẫn sinh viên cách sử dụng `Annotated` và các hàm reducer để gộp (merge) dữ liệu thay vì ghi đè hoàn toàn.
- Định nghĩa Schema cho `State` rõ ràng: Phân tách rõ giữa `internal_monologue` (suy nghĩ nội bộ của Agent) và `final_response` (phản hồi cho sinh viên).

---

### 4.3. Semantic Routing Failures

Đây là lỗi logic tại các nút điều hướng (Conditional Edges), nơi Agent quyết định bước tiếp theo dựa trên nội dung hội thoại.

### Trigger

AI Tutor không nhận diện được ý định (intent) của sinh viên.

> **Ví dụ:** Sinh viên nói *"Tôi không hiểu"*, nhưng Agent lại hiểu nhầm là sinh viên muốn **"Chuyển sang bài học mới"** thay vì **"Giải thích lại bằng ví dụ dễ hơn"**.

### Hệ quả

Tạo ra trải nghiệm "ông nói gà, bà nói vịt". Tutor đẩy sinh viên đi quá nhanh qua các kiến thức nền tảng hoặc lặp lại những giải thích mà sinh viên đã khẳng định là không hiệu quả.

### Mitigation

- Sử dụng **Structured Output** (Pydantic) cho các nút phân loại ý định để đảm bảo đầu ra của LLM luôn khớp với các cạnh (edges) đã định nghĩa trong đồ thị.
- Thiết lập một nút **"Check-point"**: Sau mỗi 2–3 bước giải thích, Tutor phải hỏi xác nhận mức độ hiểu bài của sinh viên trước khi di chuyển đến nút nội dung tiếp theo.

## 5. ROI 3 KỊCH BẢN

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
