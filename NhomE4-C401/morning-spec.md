# AI Product Canvas

Chatbot NEO - Vietnam Airlines
---

## Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi** | **User nào?**<br>- Khách hàng hay đặt vé ngại tra cứu thông tin<br>- Người cần thông tin nhanh trước chuyến bay<br><br> **Pain gì?**<br>- Tốn thời gian tra cứu giá vé, thông tin chuyến bay qua nhiều trang web<br> <br> **AI giải quyết gì?** <br>- Tra cứu thông tin giá vé, giờ bay, giờ hạ cánh, hỗ trợ đặt vé từ các thông tin người dùng yêu cầu<br><br>**Điểm chưa giải được:**<br>- Không có giá vé realtime<br>- Không tra cứu chuyến bay live<br>- Không xử lý booking end-to-end | <br> **Precision**<br> Tập trung vào trả lời đúng với các thông tin tra cứu, hỗ trợ chuyển hướng đặt vé đúng sau khi cos đủ thông tin của người dùng<br> <br> **Khi AI sai, user bị ảnh hưởng gì?**<br>- Có thể hiểu sai chính sách (đổi vé, hành lý) <br>- Mất thời gian / chi phí phát sinh<br><br>**User biết AI sai bằng cách nào?**<br>- So sánh thông tin vé, thông tin chuyến bay với website chính thức<br><br>**User sửa bằng cách nào?**<br>- Yêu cầu chatbot tra cứu lại<br>- Có feedback cho AI<br><br>**Trust hiện tại:**<br>- Trung bình (do rule-based, không realtime, dễ outdated) <br> **Trust Recovery** <br> - Nếu AI chưa tự tin (debate framework) <br> Nếu không thì trả về phản hồi không có thông tin | **Cost/request:**<br>- Thấp khoảng 0.001$ với gpt4-nano<br><br>**Latency:**<br>- Rất nhanh (<1s)<br><br>**Feasibility:**<br>- Cao (đã triển khai đơn giản, dễ maintain rule)<br><br>**Risk chính:**<br>- Nội dung outdated (policy thay đổi)<br> Cần có hàm kiểm tra kết quả truy xuất ra có trùng với kết quả truy xuất lúc gần phản hồi cho người dùng không.<br>- UX kém nếu intent detect sai<br>|

---

## Automation hay augmentation?
 Augmentation — AI gợi ý, user quyết định cuối cùng
 - AI cần hỏi lại làm rõ thông tin, xác minh quyết định của người dùng trước khi thực hiện hành động.
---

## Learning signal

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | **Implicit Signal (Tín hiệu ngầm thu được là gì?)** | - Tỷ lệ click vào link đặt vé (CTR) sau khi chatbot cung cấp thông tin chuyến bay.<br>- User dừng hội thoại (thoát) hoặc đưa ra yêu cầu mới ngay mà không phải hỏi lại (re-prompt) để sửa lỗi AI. |
| 2 | **Explicit Signal (Tín hiệu tự nguyện từ user là gì?)** | - Nút đánh giá Upvote/Downvote hoặc Rating (1-5 sao) sao khi kết thúc phiên tư vấn.<br>- User trực tiếp gửi tin nhắn bắt lỗi như: "Giá này sai rồi", "Tôi không thấy chuyến bay này trên web". |
| 3 | **Hệ thống sẽ học hỏi và cải thiện như thế nào?** | - Phân tích log các đoạn chat bị Downvote hoặc re-prompt nhiều để điều chỉnh lại Prompts.<br>- Theo dõi những thông tin bị sai sót để cập nhật lại cơ sở dữ liệu bay (KB), thay đổi cách gọi API hoặc cải thiện UI để user đỡ hiểu lầm. |
---

*AI Product Canvas — Ngày 5 — VinUni A20 — AI Thực Chiến · 2026*