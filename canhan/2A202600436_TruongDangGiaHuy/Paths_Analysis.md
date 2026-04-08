# Phân tích 4 Paths — Vietnam Airlines Chatbot NEO
**Sinh viên:** Trương Đặng Gia Huy | **Ngày:** 08/04/2026 | **Sản phẩm:** Chatbot NEO (vietnamairlines.com)

---

## Marketing vs Thực tế

### Marketing hứa gì?
- Trợ lý số 24/7, phản hồi nhanh chóng và chính xác
- Đa nền tảng (web, app, Facebook, Zalo), đa ngôn ngữ
- Database 4,000+ câu hỏi — trả lời hầu hết câu hỏi cơ bản
- Machine learning sau 3 năm: ghi nhớ sở thích, cá nhân hóa câu trả lời
- Hỗ trợ: tra cứu chuyến bay, mua vé, đổi/hoàn vé, hành lý, check-in

### Thực tế quan sát được

| Marketing hứa | Thực tế | Gap? |
|---|---|---|
| Cá nhân hóa câu trả lời | NEO có hỏi lại để refine (hành trình, hạng vé) | Phần nào đúng |
| Đa ngôn ngữ | Welcome bằng tiếng Anh, trả lời bằng tiếng Việt — không nhất quán | CÓ GAP |
| Phản hồi nhanh chóng | Không có loading indicator — user tưởng bot bị treo khi chờ | CÓ GAP |
| 4,000+ câu hỏi | Câu hỏi cơ bản trả lời tốt, có link tham khảo | OK |
| Marketing không nói gì về hạn chế | Có disclaimer nhỏ cuối trang nhưng marketing bỏ qua hoàn toàn | CÓ GAP |

**Nhận xét gap:** Marketing tạo kỳ vọng cao ("trợ lý thông minh, cá nhân hóa") nhưng trải nghiệm thực tế cho thấy đây vẫn là rule-based chatbot với một số khả năng AI. Gap lớn nhất nằm ở việc không đề cập hạn chế và thiếu loading feedback khiến user experience bị gián đoạn.

---

## PATH 1 — Khi AI đúng
**Đánh giá: TỐT NHẤT (path mạnh nhất)**

**Quan sát:**
- Câu hỏi "Hành lý xách tay bao nhiêu kg?" → NEO trả lời chi tiết, chia theo hạng vé (Phổ thông 12kg, Thương gia 18kg, Phổ thông đặc biệt tùy nội địa/quốc tế)
- Có kích thước hành lý cụ thể (56x36x23cm)
- Cung cấp link tham khảo thêm + link Tra cứu hành lý
- Hỏi lại user để cá nhân hóa: "Quý khách vui lòng cho biết hành trình..."
- Câu "Máy bay có wifi không?" → trả lời hợp lý, hướng dẫn kiểm tra khi đặt vé

**Hệ thống confirm thế nào?**
- Không có confidence score hay dấu hiệu "thông tin chính xác"
- User tự đánh giá dựa trên nội dung
- Disclaimer cuối trang: "NEO may make mistakes, please check important information"

**Điểm mạnh:** Nội dung đầy đủ, có link source, có follow-up question
**Điểm yếu:** Link bị render lỗi (hiện raw markdown thay vì hyperlink)

---

## PATH 2 — Khi AI không chắc chắn
**Đánh giá: KHÁ**

**Quan sát:**
- Câu "Tôi muốn đổi vé nhưng không nhớ mã đặt chỗ" → NEO không im lặng
- Đưa giải pháp thay thế: dùng ticket number thay PNR, vào app Quản lý đặt chỗ
- Cung cấp fallback rõ ràng: hotline 19001100, số quốc tế (+84-24)38320320, email onlinesupport@vietnamairlines.com
- Câu hành lý: NEO hỏi thêm hành trình để refine câu trả lời

**Hệ thống xử lý thế nào?**
- KHÔNG bao giờ nói "tôi không chắc" — luôn trả lời với giọng tự tin
- Không show alternatives dạng "Ý bạn là A hay B?"
- Khi không đủ info → hỏi lại HOẶC đưa hướng dẫn chung + fallback hotline

**Điểm mạnh:** Không bỏ user lơ lửng, luôn có next step
**Điểm yếu:** Không thể hiện mức độ chắc chắn, user không biết khi nào AI đang "đoán"

---

## PATH 3 — Khi AI sai
**Đánh giá: YẾU — PATH YẾU NHẤT**

**Quan sát:**
- KHÔNG có nút thumbs up/down hay "Câu trả lời có hữu ích không?"
- KHÔNG có cơ chế để user report câu trả lời sai
- KHÔNG có cách sửa lại (ví dụ: "Ý tôi là..." → NEO không hiểu context trước đó)
- Link trong câu trả lời bị render lỗi (raw markdown) — đây là bug nhưng user không report được
- Disclaimer "NEO may make mistakes" ở cuối trang quá nhỏ, dễ bỏ qua
- Nếu NEO trả lời sai thông tin (ví dụ sai cân nặng hành lý), user hoàn toàn không có cách biết trừ khi tự kiểm chứng

**User biết AI sai bằng cách nào?** Không có cách — phải tự verify
**Sửa bằng cách nào?** Không có — phải hỏi lại từ đầu hoặc gọi hotline
**Bao nhiêu bước?** Nhiều bước: nhận ra sai → không report được → hỏi lại hoặc gọi hotline → chờ xác nhận

**Tại sao đây là path yếu nhất:**
1. Hoàn toàn không có feedback loop — VNA không biết khi nào AI sai
2. User phải tự chịu trách nhiệm verify thông tin
3. Với domain hàng không (giá vé, hành lý, lịch bay), thông tin sai có hậu quả thực tế (mất tiền, lỡ chuyến)
4. Không có cơ chế cải thiện từ lỗi

---

## PATH 4 — Khi user mất tin tưởng
**Đánh giá: KHÁ nhưng có gap**

**Quan sát:**
- CÓ exit: khi user nói "tôi muốn nói chuyện với nhân viên" → NEO chuyển sang agent thật
- Nhân viên thật vào chat: "Xin quý khách vui lòng chờ một lát, nhân viên hỗ trợ khách hàng sẽ kết nối..."
- CÓ fallback rõ ràng: hotline, email được cung cấp trong nhiều câu trả lời

**Điểm yếu:**
- Không có loading indicator khi NEO xử lý → user tưởng bot chết → mất tin tưởng ngay từ đầu
- Không có nút "New Chat" rõ ràng để reset conversation
- Không có suggested questions lúc mở chatbot → user không biết NEO làm được gì
- Welcome message tiếng Anh trong khi user dùng tiếng Việt → disconnect ngay lần đầu
- Nút chuyển sang nhân viên thật không hiển thị sẵn trên UI — phải gõ text yêu cầu

---

## Tóm tắt

**Path mạnh nhất:** Path 1 (AI đúng) — Nội dung chi tiết, có link, có follow-up question

**Path yếu nhất:** Path 3 (AI sai) — Hoàn toàn không có feedback loop, user tự chịu trách nhiệm verify

**Gap marketing lớn nhất:** Marketing hứa "nhanh chóng, chính xác" nhưng không có loading indicator và không có cơ chế xử lý khi sai

**3 cải tiến quan trọng nhất:**
1. Thêm thumbs up/down + report mechanism
2. Thêm loading indicator khi NEO xử lý
3. Thêm source attribution (link nguồn chính thức) kèm mỗi câu trả lời
