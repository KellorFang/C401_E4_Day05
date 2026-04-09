# Individual reflection — Nguyễn Ngọc Thắng (2A202600191)

1. **Role cụ thể trong group**: 
Điều phối team thống nhất đề tài, phân công việc cho các thành viên trong nhóm, RAG tool engineer. Phụ trách thiết kế eval metrics cho dự án và code file "rag.py".

#Bổ sung dựa trên code cũ + tham khảo reflection.md
2. **Phần phụ trách cụ thể**: 
- Nghiên cứu cách xây dựng Industry-level RAG và áp dụng vào dự án, bao gồm áp dụng kĩ thuật Recursive chunking, metadata filtering, sử dụng model text-embedding-3-small để tối ưu semantic search, và áp dụng hybrid search (kết hợp semantic search và keyword search). 
- Chịu trách nhiệm xây dựng công cụ RAG (`search_slides`) tích hợp vào Agent. Sử dụng bộ giải pháp: LangChain framework, ChromaDB (Vector Store), và mô hình `text-embedding-3-small` của OpenAI để thực hiện nhúng (embedding) và truy xuất dữ liệu từ slide bài giảng.
- Quyết định eval metric cho mỗi tính năng của Agent.

3. **SPEC phần mạnh nhất**: 
**4.4 RAG** (trong file SPEC). Đây là phần được hiện thực hóa đầy đủ nhất từ bản thiết kế, hỗ trợ truy xuất thông tin kèm dẫn chứng (source, page) chính xác. 
**SPEC phần yếu nhất**: **UI**. Giao diện mới dừng lại ở mức Streamlit mặc định, chưa có nhiều tùy biến nâng cao về trải nghiệm người dùng (UX).

4. **Đóng góp cụ thể khác với phần 2**: 
- Thực hiện Unit Test (đã vượt qua 14 tests) và Debug hệ thống để đảm bảo tính ổn định cho Agent; 
- Khảo sát và đánh giá 3/4 nhóm khác bằng cách đặt các câu hỏi chuyên môn xoay quanh "Pain points" và kiến thức "4 paths" được học trong khóa C401.
- Điều phối team thống nhất đề tài, phân công việc cho các thành viên trong nhóm.

5. **Một điều học được trong Hackathon mà trước đó chưa biết**: Trước Hackathon, nghĩ rằng Precision và Recall chỉ được sử dụng riêng lẻ. Nhưng sau khi thiết kế Eval Metrics cho AI Tutor, hiểu rằng đây là những quyết định quan trọng về sản phẩm (Product Decision). Cụ thể: chúng tôi ưu tiên **Recall >= 95% cho việc trích xuất chủ đề** (Topic Extraction) vì việc bỏ sót kiến thức gây ra lỗ hổng cho sinh viên nguy hiểm hơn là việc thừa thông tin; nhưng lại ưu tiên **Precision >= 95% cho việc giải thích khái niệm và tạo quiz** vì kiến thức sai sẽ trực tiếp gây hại cho việc học. Việc chọn metric nào cao hơn cho tính năng nào chính là sự đánh đổi giữa rủi ro và giá trị thực tế cho người dùng, không chỉ là con số lập trình.

6. **Nếu làm lại, sẽ đổi gì**: 
- Sẽ tập trung đầu tư thêm vào thiết kế UI/UX để sản phẩm có vẻ ngoài chuyên nghiệp hơn. 
- Nghiên cứu kỹ hơn về các kỹ thuật chunking và metadata filtering trước khi bắt tay vào code để tối ưu hóa hiệu suất tìm kiếm của RAG.

7. **AI giúp gì**: Hỗ trợ mạnh mẽ trong việc sinh mã nguồn khung (boilerplate) cho RAG và giải thích cơ chế hoạt động của các thành phần trong LangGraph. Tuy nhiên, AI thường xuyên cung cấp thông tin lỗi thời về các thư viện (ví dụ như gợi ý sai tên module `langchain_nvidia_ai_endpoints`) và gặp khó khăn khi xử lý các lỗi phụ thuộc (dependencies) giữa các package đã cài đặt.