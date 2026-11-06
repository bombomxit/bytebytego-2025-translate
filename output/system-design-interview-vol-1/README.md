# System Design Interview - Tập 1, bản tiếng Việt

[← Tủ sách](../../docs/README.md) · [ByteByteGo 2025](../bytebytego-2025/README.md)

**Tác giả:** Alex Xu. Bản dịch gồm 16 chương, lời đầu và lời kết, tương ứng 269 trang PDF nguồn.

Bắt đầu từ [lời nói đầu](vi/00-loi-mo-dau.md), hoặc vào ngay [chương 1](vi/chuong-01-mo-rong-tu-con-so-khong-den-hang-trieu-nguoi-dung.md). Mỗi chương là một file Markdown riêng, có liên kết chương trước/sau và đường về mục lục này.

## Mục lục

| Chương | Nội dung | Trang PDF nguồn |
| --- | --- | --- |
| 1 | [Mở rộng từ con số không đến hàng triệu người dùng](vi/chuong-01-mo-rong-tu-con-so-khong-den-hang-trieu-nguoi-dung.md) | 5-33 |
| 2 | [Ước tính sơ bộ](vi/chuong-02-uoc-tinh-so-bo.md) | 34-41 |
| 3 | [Khung phương pháp cho phỏng vấn thiết kế hệ thống](vi/chuong-03-khung-phuong-phap-cho-phong-van-thiet-ke-he-thong.md) | 42-50 |
| 4 | [Thiết kế bộ giới hạn tốc độ](vi/chuong-04-thiet-ke-bo-gioi-han-toc-do.md) | 51-70 |
| 5 | [Thiết kế cơ chế băm nhất quán](vi/chuong-05-thiet-ke-co-che-bam-nhat-quan.md) | 71-86 |
| 6 | [Thiết kế kho khóa-giá trị](vi/chuong-06-thiet-ke-kho-khoa-gia-tri.md) | 87-109 |
| 7 | [Thiết kế bộ sinh ID duy nhất trong hệ thống phân tán](vi/chuong-07-thiet-ke-bo-sinh-id-duy-nhat-trong-he-thong-phan-tan.md) | 110-118 |
| 8 | [Thiết kế dịch vụ rút gọn URL](vi/chuong-08-thiet-ke-dich-vu-rut-gon-url.md) | 119-131 |
| 9 | [Thiết kế trình thu thập dữ liệu web](vi/chuong-09-thiet-ke-trinh-thu-thap-du-lieu-web.md) | 132-150 |
| 10 | [Thiết kế hệ thống thông báo](vi/chuong-10-thiet-ke-he-thong-thong-bao.md) | 151-165 |
| 11 | [Thiết kế hệ thống bảng tin](vi/chuong-11-thiet-ke-he-thong-bang-tin.md) | 166-177 |
| 12 | [Thiết kế hệ thống trò chuyện](vi/chuong-12-thiet-ke-he-thong-tro-chuyen.md) | 178-199 |
| 13 | [Thiết kế hệ thống tự động hoàn thành tìm kiếm](vi/chuong-13-thiet-ke-he-thong-tu-dong-hoan-thanh-tim-kiem.md) | 200-219 |
| 14 | [Thiết kế YouTube](vi/chuong-14-thiet-ke-youtube.md) | 220-243 |
| 15 | [Thiết kế Google Drive](vi/chuong-15-thiet-ke-google-drive.md) | 244-263 |
| 16 | [Tiếp tục học hỏi](vi/chuong-16-tiep-tuc-hoc-hoi.md) | 264-268 |

[Lời kết](vi/17-loi-ket.md) · [Bảng thuật ngữ](vi/thuat-ngu.md)

## Cách dùng

- Đọc lần lượt chương 1-3 để nắm các thành phần nền tảng, cách ước tính quy mô và khung tiếp cận phỏng vấn.
- Chương 4-15 là các bài toán thiết kế cụ thể. Có thể chọn theo nhu cầu và đối chiếu các khái niệm qua bảng thuật ngữ.
- Chương 16 tổng hợp tài nguyên và blog kỹ thuật để học tiếp. Với những bài ngắn để tra cứu, xem [ByteByteGo 2025](../bytebytego-2025/vi/000-muc-luc-tom-tat.md).

## Phạm vi bản dịch và đối chiếu

- Giữ nội dung theo thứ tự nguồn, gồm ví dụ, số liệu, công thức và tài liệu tham khảo. Comment `trang-pdf` chỉ vị trí trang PDF tương ứng.
- Có đủ **226 ảnh gốc**, gồm bìa, sơ đồ, bảng và mã nguồn dạng ảnh. **Chữ, nhãn và mã bên trong ảnh vẫn bằng tiếng Anh**; phần giải thích bên ngoài ảnh được dịch sang tiếng Việt.
- Bản dịch đã kiểm tra cấu trúc toàn bộ và đọc chéo chọn mẫu ở mọi chương. Đây chưa phải bản đã soát song ngữ từng dòng. Xem [phạm vi và kết quả kiểm tra](QA.md) cùng [quy ước biên tập](manifest/translation-conventions.md).
- Ghi chú do người dịch bổ sung mang nhãn **Ghi chú bản dịch**, tách khỏi lời tác giả. Các nhận định kỹ thuật còn lại phản ánh nội dung và thời điểm xuất bản của sách.
- PDF và văn bản tiếng Anh trích xuất được lưu ở workspace nguồn, không đóng gói trong repo này. [Metadata trang và ảnh](manifest/chapters.json) giữ thông tin để đối chiếu khi có PDF tương ứng.

## Phiên bản nguồn

Nguồn tập 1 có 269 trang và 16 chương. Hai file được cung cấp để dịch có cùng SHA-256; file mang tên “volume 2” thực chất là bản trùng tập 1. Bộ này chưa bao gồm tập 2.

SHA-256 nguồn: `1556d7a7cbcc1ec82dacfad4ffde2d39674fef27f34e00a7b7aa483878d5e821`.

Nội dung gốc thuộc tác giả và đơn vị phát hành. Bản tiếng Việt này phục vụ việc học và đối chiếu.
