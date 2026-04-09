# Individual reflection — Phạm Đỗ Ngọc Minh (2A202600256)

## 1. Role
Tool designer - phụ trách thiết kế tool call api của tavily và arxiv. Người đi đánh giá các nhóm trong zone.

## 2. Đóng góp cụ thể
- Thiết kế tool call api của tavily và arxiv
- Đánh giá các nhóm trong zone
- Hỗ trợ thiết kế tool github

## 3. SPEC mạnh/yếu
- Mạnh nhất: Definition và descriptions của các tools (Web search & ArXiv) được viết rất rõ ràng, phân ranh giới tốt (Web cho kiến thức lập trình/thư viện mở rộng, ArXiv cho academic papers). Việc giới hạn định dạng và bắt exception (try/except) giúp agent không bị lỗi crash khi kết nối API hoặc thiếu key.
- Yếu nhất: Tool trả về kết quả theo Top-K bị cắt cụt (truncated content còn 300 ký tự) nhằm tiết kiệm token nhưng rủi ro cao làm mất ngữ cảnh quan trọng nếu phần hay nằm ở cuối trang. Phụ thuộc lớn vào chất lượng của query do LLM sinh ra.

## 4. Đóng góp khác
- Giúp nhóm làm xong spec draft và spec final.
- Hướng dẫn cả nhóm phương thức nộp bài

## 5. Điều học được
Trước đây mình nghĩ tích hợp Search API chỉ đơn giản là ném query vào lấy kết quả ra. 
Sau khi tự tay build các tools (Tavily/ArXiv) cho AI tự gọi, mình mới hiểu: LLM rất nhạy cảm với "Tool descriptions" (docstring). Chỉ cần viết description không chặt, LLM sẽ gọi nhầm tool. Thêm nữa, quyết định giới hạn độ dài văn bản trả về (ví dụ 300 ký tự) là một quyết định đánh đổi (trade-off) quan trọng giữa chi phí/token limit và mức độ đầy đủ của thông tin (Information adequacy), chứ không phải thích trả về bao nhiêu cũng được.
Sau Hackathon mình cũng học được thêm tinh thần trách nhiệm làm việc nhóm, hoàn thiện task được giao.

## 6. Nếu làm lại
Sẽ cải thiện cơ chế lấy nội dung: thay vì chỉ lấy snippet 300 ký tự cắt ngọn cộc lốc, mình sẽ nghiên cứu cách cho tool parse và tóm tắt trực tiếp các thẻ HTML quan trọng hoặc tích hợp `Read_Page` tool để AI đọc chi tiết link nếu cần. Ngoài ra, sẽ test prompt với nhiều use-cases thực tế hơn sớm từ ngày đầu.

## 7. AI giúp gì / AI sai gì
- **Giúp:** Các LLM (Claude, Gemini) hỗ trợ viết boiler-plate code để tích hợp tool qua Langchain cực kì nhanh và chuẩn xác (như `langchain_community.tools.tavily_search` hay `ArxivRetriever`). Giúp gợi ý các format metadata rất tốt.
- **Sai/mislead:** Trong lúc brainstorm triển khai, AI đôi khi "bày vẽ" chèn thêm các tính năng Web scraping phức tạp bằng BeautifulSoup hay Selenium thẳng vào tool nhỏ làm mất tập trung và có thể gây Timeout cho LLM. Bài học: AI brainstorm tốt nhưng mình phải vững scope và giữ cho tool có Single Responsibility (làm đúng 1 việc).