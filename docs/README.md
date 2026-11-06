# Tài liệu học System Design

[← Trang chính](../README.md)

## Tủ sách

| Tài liệu | Phù hợp khi | Mở đọc |
| --- | --- | --- |
| **System Design Interview - Tập 1, Alex Xu** | Cần học nền tảng, khung phỏng vấn và luyện bài thiết kế theo chương | [Mục lục 16 chương](../output/system-design-interview-vol-1/README.md) · [Bắt đầu từ chương 1](../output/system-design-interview-vol-1/vi/chuong-01-mo-rong-tu-con-so-khong-den-hang-trieu-nguoi-dung.md) |
| **ByteByteGo Big Archive System Design 2025** | Cần tra cứu chủ đề, xem sơ đồ và ôn nhanh từng bài | [Mục lục tóm tắt 217 bài](../output/bytebytego-2025/vi/000-muc-luc-tom-tat.md) · [Bản gốc và bản dịch](../output/bytebytego-2025/README.md) |

Mỗi bộ có mục lục riêng và ảnh đi cùng bài. Tập 1 có liên kết chương trước/sau; ByteByteGo giữ số thứ tự tương ứng giữa bản gốc và bản Việt.

## Bài chia sẻ

- [Một request chậm đi qua hệ thống như thế nào](superpowers/sharing/2026-08-06-request-cache-database-sharing.md): từ FE/mobile tới Redis và database, cách nhìn điểm nghẽn và vai trò của index.

## Biên tập tài liệu

| Hướng dẫn | Dùng khi |
| --- | --- |
| [Workflow PDF sang Markdown](pdf-to-markdown-workflow.md) | Chuẩn bị nguồn, chia bài, trích ảnh và tổ chức đầu ra |
| [Prompt mẫu](pdf-to-markdown-prompt-template.md) | Giao việc chuyển đổi và dịch tài liệu mới |
| [Checklist chất lượng](conversion-quality-checklist.md) | Rà độ đầy đủ, ảnh, liên kết và nội dung trước khi đưa vào repo |
| [Kết quả kiểm tra tập 1](../output/system-design-interview-vol-1/QA.md) | Xem phạm vi kiểm tra và giới hạn của bản dịch |

Chạy `python3 scripts/audit_docs.py` từ thư mục gốc repo để kiểm tra cấu trúc và liên kết của cả hai bộ.
