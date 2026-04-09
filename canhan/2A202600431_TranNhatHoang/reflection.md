1. **Role cụ thể trong nhóm:** 
   * **RAG Tool Developer**: Chuyên trách nghiên cứu, phát triển và tối ưu hóa luồng Data Ingestion (tiền xử lý và vector hóa dữ liệu) cho pipeline RAG.

2. **Phần phụ trách cụ thể (liệt kê 2-3 đóng góp có output rõ):**
   * **Phát triển & Debug Data Ingestion:** Cài đặt luồng trích xuất dữ liệu đa phương tiện từ PDF (text, images) và tối ưu hóa chuẩn bị dữ liệu đầu vào RAG.
   * **Phân tích hiệu năng hệ thống trích xuất (`pdf_parser.py`):** Trực tiếp test script trên các tập dữ liệu thử thách (file `B5.pdf` 49 trang) để đánh giá giới hạn công cụ.
      * *Điểm mạnh:* Trích xuất văn bản phẳng (plain text) với tính chính xác cực cao, làm cơ sở tốt cho Text Splitter.
      * *Điểm yếu:* Làm vỡ cấu trúc (structure loss) đối với khối dữ liệu phức tạp như sơ đồ (Diagrams) và bảng biểu (Tables), gây ra data nhiễu và không tối ưu khi chuyển qua vector.

3. **SPEC phần nào mạnh nhất, phần nào yếu nhất? Vì sao?**
   * **Mạnh nhất (Mục System Prompt & Metadata):** Kiến trúc chặt chẽ ở khâu định nghĩa Output Metadata (source, page, lecture_date) và Rule cho Agent bằng XML. Việc ép LLM bám sát nguồn context RAG giúp triệt tiêu hoàn toàn khả năng sinh câu trả lời ảo (Hallucination) và tăng độ tin cậy tuyệt đối.
   * **Yếu nhất (Mục 4.3 Ingestion Pipeline - Quản lý vòng đời dữ liệu & Vector Deduplication):** SPEC chỉ thiết kế luồng quy trình theo dạng một chiều (thả file PDF và chạy một lần). Là một RAG Developer, tôi đánh giá đây là một lỗ hổng chí mạng vì SPEC thiếu hoàn toàn cơ chế quản lý ID tài liệu và xử lý trùng lặp (Deduplication). Trong thực tế, slide bài giảng sẽ được giảng viên cập nhật, chỉnh sửa liên tục. Với thiết kế hiện tại, mỗi lần chạy lại script cập nhật, ChromaDB sẽ sinh ra hàng loạt các bản sao (duplicate chunks) của cùng một trang slide. Điều này sẽ khiến RAG truy xuất ra một đống kết quả rác/trùng lặp, làm nhiễu loạn hoàn toàn bối cảnh (context) trước khi đưa cho LLM tổng hợp, phá vỡ độ chính xác vốn có của hệ thống.

4. **Đóng góp cụ thể khác với mục 2:**
   * **R&D Công nghệ:** Đánh giá chéo và thử nghiệm các thư viện thay thế hiệu quả hơn (so sánh tradeoff giữa `easyocr` và `PyMuPDF`) cho pipeline xử lý văn bản.
   * **Testing & Gỡ lỗi toàn hệ thống:** Hỗ trợ Debug trực tiếp luồng Agent RAG và giải quyết triệt để các rắc rối về tương thích thư viện trong môi trường cục bộ.

5. **1 điều học được trong hackathon mà trước đó chưa biết:**
   * Khả năng làm việc dưới mô hình "Timeboxing" khắc nghiệt: Nhận thức rõ cách bẻ nhỏ nhanh một kiến trúc AI thô thành các module độc lập, và vận hành ghép nối nhịp nhàng để triển khai ra một Minimum Viable Product (MVP) trơn tru trong thời lượng vô cùng ngắn.

6. **Nếu làm lại, đổi gì? (Về Technical):**
   * **Dẹp bỏ Text Splitter cổ điển:** Không dùng Recursive Splitter cho các slide học thuật. Chuyển sang Framework Parsing thông minh (như `LlamaParse` hoặc module `Unstructured`) để phân loại độc lập Text/Table/Image, duy trì nguyên vẹn cấu trúc DOM của tài liệu.
   * **Sử dụng Vision LLM (VLM):** Loại bỏ chiến lược dậm chân tại chỗ bằng OCR CPU nặng nề. Gọi API các mô hình VLM nhỏ gọn để quét qua những trang chứa Diagram, tự động sinh chú thích (Image-to-Text captioning) rồi mới Embedding. Việc này giúp ChromaDB ôm trọn tri thức đồ họa mà bình thường RAG bỏ lỡ.

7. **AI giúp gì? AI sai/mislead ở đâu?**
   * **Lợi ích (Điểm mạnh):** Đóng vai trò là một "Pair-programmer" đắc lực, tăng tốc x10 tốc độ code boilerplate, phác thảo cấu trúc System Prompt, và chẩn đoán lỗi dependency (import/syntax) tốt.
   * **Mislead (Điểm yếu):** Hoàn toàn thất bại trong việc đánh giá bối cảnh tài nguyên (Hardware Context). Điển hình là việc AI liên tục đề xuất chạy nguyên bản workflow OCR cục bộ trên CPU cho những file PDF khổng lồ mà không cảnh báo bottlenecks thời gian. Nhóm mất thêm nhiều chu kỳ debug không đáng có mới nhận ra và tinh chỉnh lại hướng tiếp cận.