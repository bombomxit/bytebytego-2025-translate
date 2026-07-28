# Prompt mẫu convert PDF sang Markdown

Dùng file này như prompt khởi đầu cho Codex/AI khi muốn convert một PDF khác thành bộ Markdown có bản gốc, bản dịch, ảnh và tóm tắt.

## Prompt đầy đủ

```text
Tôi có một file PDF cần convert sang Markdown.

PDF path:
<đường dẫn PDF tuyệt đối>

Mục tiêu:
- Tách PDF thành từng bài/chương theo cấu trúc hợp lý.
- Tạo 2 bản Markdown:
  - `original/`: bản gốc đã extract và làm sạch nhẹ.
  - `vi/`: bản dịch tiếng Việt sát nghĩa, dễ hiểu cho người đọc Việt Nam.
- Tách ảnh/diagram riêng vào `assets/` và nhúng lại vào Markdown.
- Tạo `manifest/`, README tiến độ và mục lục tóm tắt.

Trước khi làm, hãy hỏi tôi từng câu cần thiết nếu chưa rõ:
1. Sách/tài liệu này viết về chủ đề gì?
2. Người đọc chính là ai: beginner, developer, senior engineer, manager hay học sinh/sinh viên?
3. Muốn tách theo bài, chương, heading lớn hay từng trang?
4. Muốn phong cách dịch thế nào: dịch sát, giải thích dễ hiểu, hay vừa dịch vừa bình luận?
5. Thuật ngữ kỹ thuật nên giữ tiếng Anh nhiều hay Việt hóa nhiều?
6. Có cần thêm ví dụ minh họa không? Nếu có, ví dụ nên theo domain nào: backend, e-commerce, fintech, AI, DevOps, mobile app?
7. Có cần dịch/giải thích chữ trong ảnh không?
8. Output folder muốn đặt tên gì? Hãy dùng tên không dấu, dạng `kebab-case`.
9. Repo/output này sẽ private hay public? Nếu public, hãy tránh đưa full text/ảnh sách có bản quyền.

Nếu tôi nói “làm đi” khi đã đủ thông tin, hãy tự chạy theo luồng:
1. Inspect PDF: số trang, text layer, layout, ảnh, quy luật heading.
2. Tạo manifest gồm id, title, slug, start_page, end_page, original_path, vi_path, asset_dir, image_count.
3. Extract ảnh/diagram vào `output/<slug>/assets/<id>/figure-xx.png`.
4. Extract text gốc vào `output/<slug>/original/<id>-<slug>.md`.
5. Dịch sang `output/<slug>/vi/<id>-<slug>.md` với cấu trúc:
   - Hình minh họa
   - Dịch sát
   - Tóm tắt
   - Ví dụ thực tế - không nằm trong tài liệu gốc
   - Thuật ngữ chính
6. Tạo `output/<slug>/vi/000-muc-luc-tom-tat.md`.
7. Tạo `output/<slug>/README.md`.
8. Tạo hoặc cập nhật README gốc của repo.
9. Chạy audit:
   - số bài manifest/original/vi khớp nhau;
   - không thiếu image link;
   - mỗi bài dịch có đủ section;
   - không còn placeholder `TODO`, `TBD`, `dịch sau`.

Quy tắc dịch:
- Dịch sát ý gốc, không bịa thêm trong phần `Dịch sát`.
- Giữ thuật ngữ English quen thuộc khi cần: API Gateway, cache, JWT, RAG, load balancer, sharding, rate limiting.
- Nếu thêm ví dụ ngoài tài liệu, bắt buộc đặt trong mục `Ví dụ thực tế - không nằm trong tài liệu gốc`.
- Ưu tiên giải thích theo tư duy lập trình và system design.
- Viết tiếng Việt rõ, tự nhiên, dễ hiểu; tránh dịch máy thô.

Sau khi xong, báo cáo:
- Output folder.
- Số bài gốc/dịch.
- Số ảnh.
- File mục lục chính.
- Kết quả audit.
- Những điểm cần tôi tự review lại nếu có.
```

## Prompt ngắn khi đã biết rõ yêu cầu

```text
Convert PDF `<path>` sang Markdown trong `output/<slug>`.

Chủ đề tài liệu: <topic>.
Người đọc: <audience>.
Tách theo: <article/chapter/heading/page>.
Phong cách: dịch sát tiếng Việt, giữ thuật ngữ kỹ thuật English khi tự nhiên hơn.
Ảnh: tách riêng vào `assets/` và nhúng lại vào từng file MD.
Output: giữ cả `original/` và `vi/`, có manifest, README, mục lục tóm tắt.
Ví dụ thêm: <không/có, domain ví dụ>.

Làm tuần tự, audit link ảnh và số lượng file trước khi báo xong.
```

## Bộ câu hỏi biến đổi theo từng loại sách

### Sách system design/backend

- Ví dụ nên bám vào hệ thống nào: e-commerce, banking, chat app, social network, SaaS, AI app?
- Người đọc cần hiểu ở mức interview, production engineering hay kiến trúc tổng quan?
- Thuật ngữ nào nên giữ nguyên: cache, queue, shard, replica, CDN, gateway, failover?

### Sách AI/data

- Ví dụ nên bám vào RAG, chatbot, recommendation, data pipeline hay MLOps?
- Công thức/toán có cần giải thích bằng trực giác trước không?
- Có cần bảng thuật ngữ model/dataset/embedding/vector database không?

### Sách ngoại ngữ/kỹ năng học

- Có cần giữ câu gốc để đối chiếu không?
- Có cần thêm ví dụ câu, phát âm, collocation, bài tập nhỏ không?
- Dịch theo nghĩa tự nhiên hay dịch từng cụm để học cấu trúc?

### Report kinh doanh/sản phẩm

- Có cần executive summary trước từng chương không?
- Có cần chuyển số liệu thành bảng dễ đọc không?
- Có cần phân biệt rõ “fact từ report” và “nhận xét thêm” không?

