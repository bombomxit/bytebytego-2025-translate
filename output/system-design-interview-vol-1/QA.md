# Kết quả kiểm tra bản dịch tập 1

## Phạm vi và nguồn

- 16 chương, lời đầu và lời kết, tương ứng toàn bộ 269 trang của PDF được cung cấp.
- Hai PDF được cung cấp có cùng SHA-256; file mang tên “volume 2” là bản trùng tập 1.
- Đầu ra là Markdown có dẫn ảnh gốc; chữ, bảng và mã nguồn nằm trong ảnh giữ nguyên tiếng Anh.

## Kiểm tra cấu trúc

- 18 file nội dung có đúng phạm vi và thứ tự marker trang nguồn, tổng 269 marker, không thiếu hoặc lặp trang.
- Đủ 226 ảnh, đúng thứ tự nguồn; mọi đường dẫn ảnh tồn tại. Đã kiểm tra giải mã toàn bộ 226 file ảnh và xem mẫu trực quan.
- Mỗi file nội dung có một tiêu đề cấp 1, code fence cân bằng; đường dẫn nội bộ hợp lệ.
- URL trong văn bản nguồn được đối chiếu với bản dịch, có xử lý URL bị PDF ngắt dòng. Đây là kiểm tra giữ đúng URL, không phải xác nhận các website cũ còn hoạt động.
- Có điều hướng về mục lục và chương trước/sau. Các câu bị ngắt giữa hai trang PDF được nối lại khi biên tập.

Chạy kiểm tra cấu trúc từ repo root: `python3 scripts/audit_docs.py`. Kết quả kiểm tra lúc nhập bản Việt được lưu trong [quality-check.json](manifest/quality-check.json). PDF và file `.txt` trung gian không đóng gói trong repo; bản tiếng Anh hiện có trong `original/`. Bước đối chiếu URL nguồn và kiểm tra giải mã ảnh đã được thực hiện ở workspace dịch trước khi nhập. Nội dung Markdown khi nhập được đối chiếu với bản dịch local, chỉ thay đổi đường dẫn và cách dẫn nguồn PDF.

## Bản gốc tiếng Anh

- 18 file Markdown: 16 chương, lời đầu và lời kết; không tạo bản tiếng Anh cho bảng thuật ngữ bổ trợ do người dịch biên soạn.
- Trích trực tiếp từ PDF có SHA-256 khớp manifest, không dịch ngược từ bản Việt. Giữ nội dung của đủ 269 trang và dùng chung 226 hình, không nhân bản ảnh.
- So sánh SHA-256 văn bản từng trang sau khi chuẩn hóa khoảng trắng và giải mã HTML entities với [hash nguồn](manifest/original-text-checks.json). Audit kiểm tra đủ trang theo đúng thứ tự, toàn bộ hình và liên kết Anh ↔ Việt.
- Hình nằm sau phần chữ của trang PDF tương ứng. Đây là văn bản trích xuất để đọc và đối chiếu; ngắt dòng, bảng và công thức trong lớp chữ có thể không giữ cách trình bày PDF. Các hình, bảng và code dạng ảnh vẫn được giữ nguyên.

Tạo lại bản Anh từ đúng PDF local (cần Poppler `pdftotext`, không cần thư viện Python ngoài):

```sh
python3 scripts/import_system_design_originals.py /duong/dan/tap-1.pdf
python3 scripts/audit_docs.py
```

## Đọc chéo nội dung

Các subagent đọc chéo bản dịch do người khác thực hiện. Chưa phát hiện lỗi dịch hoặc thiếu nội dung trong các mẫu sau:

| Chương | Trang PDF đã đọc chéo |
| --- | --- |
| 1 | 15, 30 |
| 2 | 38, 39 |
| 3 | 43, 44 |
| 4 | 62, 64 |
| 5 | 75, 82 |
| 6 | 88, 96 |
| 7 | 111, 114 |
| 8 | 120, 128 |
| 9 | 133, 134, 145 |
| 10 | 152, 160, 161 |
| 11 | 167, 172, 173 |
| 12 | 179, 190 |
| 13 | 201, 208 |
| 14 | 221, 230, 235, 238 |
| 15 | 246, 255, 260 |
| 16 | 264-268, toàn bộ chương và 70 URL |

Lời đầu trang 1-4 và lời kết trang 269 được đọc đối chiếu toàn bộ. Danh mục tham khảo của các chương được kiểm tra đầy đủ; ví dụ số học và ghi chú sửa lỗi nguồn ở các chương 4, 8 và 12 được đối chiếu riêng.

Đây là bản dịch học tập đã kiểm tra cấu trúc toàn bộ và đọc chéo chọn mẫu. Chưa thực hiện soát song ngữ từng dòng của toàn bộ sách hoặc dịch chữ bên trong mọi ảnh.

## Ghi chú biên tập

Những bất nhất rõ ràng của nguồn được đánh dấu **Ghi chú bản dịch**, gồm ký hiệu `0.7%` ở chương 4, thuật ngữ vector clock ở chương 6, phép tính dung lượng ở chương 8, tên API/endpoint ở chương 10, mô tả nhiều thiết bị ở chương 12 và ví dụ tiền tố ở chương 13. Các ghi chú được tách khỏi lời tác giả.

[← Mục lục tập 1](README.md) · [Tủ sách](../../docs/README.md)
