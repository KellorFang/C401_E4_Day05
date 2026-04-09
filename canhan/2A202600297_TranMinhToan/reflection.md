### reflection.md

```markdown
# Individual reflection — Trần Minh Toàn (2A202600297)

## 1. Role
Tool integration + prompt support. Phụ trách tìm hiểu, tích hợp và test 2 tool `GitHub` và `PubMed` cho prototype.

## 2. Đóng góp cụ thể
- Tích hợp tool `GitHub` để truy xuất repo/tài liệu kỹ thuật khi cần tham chiếu
- Tích hợp tool `PubMed` để tìm paper và nguồn y khoa đáng tin cậy cho câu trả lời

## 3. SPEC mạnh/yếu
- Mạnh nhất: failure modes — nhóm nghĩ ra được case "triệu chứng chung chung"
  mà AI gợi ý quá rộng, và có mitigation cụ thể (hỏi thêm câu follow-up)
- Yếu nhất: ROI — 3 kịch bản thực ra chỉ khác số user, assumption gần giống nhau.
  Nên tách assumption rõ hơn (VD: conservative = chỉ dùng ở 1 chi nhánh,
  optimistic = rollout toàn hệ thống)

## 4. Đóng góp khác
- Hỗ trợ team kiểm tra demo flow cho phần gọi tool và cách hiển thị kết quả trả về
- Góp ý chỉnh prompt khi AI gọi sai tool hoặc trả về thông tin quá rộng

## 5. Điều học được
Trước hackathon mình nghĩ tool chỉ là phần phụ thêm cho AI.
Sau khi trực tiếp làm với `GitHub` và `PubMed`, mình mới thấy chất lượng câu trả lời
phụ thuộc rất nhiều vào việc chọn đúng nguồn và viết prompt đủ rõ để model gọi đúng tool.
Một model mạnh vẫn có thể trả lời kém nếu không được grounding bằng nguồn phù hợp.

## 6. Nếu làm lại
Sẽ test phần tool-calling sớm hơn thay vì đợi gần demo mới chạy nhiều case.
Nếu làm từ đầu, nhóm có thể phát hiện sớm các tình huống gọi sai tool hoặc trả kết quả quá rộng,
và sẽ có thêm thời gian refine prompt lẫn UX hiển thị output.

## 7. AI giúp gì / AI sai gì
- **Giúp:** dùng Claude để brainstorm các failure modes cho chatbot hỗ trợ học sinh học khóa AI 20K —
  nó gợi ý được case học viên hỏi quá mơ hồ hoặc nhảy sang bài khác mà không nêu rõ ngữ cảnh.
  Dùng Gemini để test prompt nhanh qua AI Studio.
- **Sai/mislead:** Claude gợi ý thêm feature như "chấm bài tự động" hoặc "lộ trình học cá nhân" —
  nghe hay nhưng scope quá lớn cho hackathon. Suýt bị scope creep nếu không dừng lại.
  Bài học: AI brainstorm tốt nhưng không biết tự giới hạn phạm vi bài toán.
```

---