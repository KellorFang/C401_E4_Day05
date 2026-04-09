1. **Role cụ thể trong group**: Điều phối team thống nhất đề tài, thiết kế pipeline cho hệ thống RAG, trực tiếp lập trình tool `rag.py`. Đồng thời tham gia khảo sát và đánh giá 3/4 nhóm khác bằng cách đặt các câu hỏi chuyên môn xoay quanh "Pain points" và kiến thức "4 paths" được học trong khóa C401.

#Bổ sung dựa trên code cũ
2. **Phần phụ trách cụ thể**: Nghiên cứu cách xây dựng Industry-level RAG và áp dụng vào dự án, bao gồm các kĩ thuật chunking, metadata filtering, và tối ưu hóa hiệu suất tìm kiếm. Chịu trách nhiệm xây dựng công cụ RAG (`search_slides`) tích hợp vào Agent. Sử dụng bộ giải pháp: LangChain framework, ChromaDB (Vector Store), và mô hình `text-embedding-3-small` của OpenAI để thực hiện nhúng (embedding) và truy xuất dữ liệu từ slide bài giảng.

3. **SPEC phần mạnh nhất**: **4.4 RAG** (trong file SPEC). Đây là phần được hiện thực hóa đầy đủ nhất từ bản thiết kế, hỗ trợ truy xuất thông tin kèm dẫn chứng (source, page) chính xác. **SPEC phần yếu nhất**: **UI**. Giao diện mới dừng lại ở mức Streamlit mặc định, chưa có nhiều tùy biến nâng cao về trải nghiệm người dùng (UX).

4. **Đóng góp cụ thể khác với phần 2**: Thực hiện Unit Test (đã vượt qua 14 tests) và Debug hệ thống để đảm bảo tính ổn định cho Agent; tham gia đóng góp ý kiến phản biện tích cực cho các nhóm bạn dựa trên tiêu chí thực tiễn của dự án.

5. **Một điều học được trong Hackathon mà trước đó chưa biết**: Chấp nhận đánh đổi phạm vi dự án (Scope) để đảm bảo chất lượng và tính khả thi. Việc tập trung làm tốt một tính năng cốt lõi quan trọng hơn là làm nhiều tính năng nhưng không hoàn thiện.

6. **Nếu làm lại, sẽ đổi gì**: Sẽ tập trung đầu tư thêm vào thiết kế UI/UX để sản phẩm có vẻ ngoài chuyên nghiệp hơn. Đồng thời, nghiên cứu kỹ hơn về các kỹ thuật chunking và metadata filtering trước khi bắt tay vào code để tối ưu hóa hiệu suất tìm kiếm của RAG.

7. **AI giúp gì**: Hỗ trợ mạnh mẽ trong việc sinh mã nguồn khung (boilerplate) cho RAG và giải thích cơ chế hoạt động của các thành phần trong LangChain. Tuy nhiên, AI thường xuyên cung cấp thông tin lỗi thời về các thư viện (ví dụ như gợi ý sai tên module `langchain_nvidia_ai_endpoints`) và gặp khó khăn khi xử lý các lỗi phụ thuộc (dependencies) giữa các package đã cài đặt.
