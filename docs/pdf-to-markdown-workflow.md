# Workflow convert PDF sang Markdown có ảnh

Tài liệu này ghi lại luồng chính để convert một file PDF thành bộ Markdown có cấu trúc, có ảnh tách riêng, có bản gốc và bản dịch/giải thích. Có thể dùng lại cho sách kỹ thuật, ebook, report, slide PDF hoặc archive nhiều bài ngắn.

## Mục tiêu đầu ra

Mỗi lần convert nên tạo ra cấu trúc tương tự:

```text
output/<project-slug>/
├── assets/        # ảnh/diagram tách từ PDF
├── manifest/      # danh sách bài/chương, page range, path
├── original/      # Markdown gốc theo ngôn ngữ PDF
├── vi/            # Markdown dịch/giải thích tiếng Việt
└── README.md      # mục lục tiến độ
```

Với mỗi bài/chương:

- `original/<id>-<slug>.md`: giữ nội dung gốc đã extract, chỉ làm sạch lỗi OCR/layout cơ bản.
- `vi/<id>-<slug>.md`: dịch sát, giải thích dễ hiểu, giữ thuật ngữ kỹ thuật tiếng Anh khi cần.
- `assets/<id>/figure-01.png`: ảnh/diagram tách riêng và nhúng lại bằng Markdown.

## Câu hỏi cần chốt trước khi chạy

| Câu hỏi | Vì sao cần hỏi | Ví dụ trả lời |
|---|---|---|
| PDF nằm ở đâu? | Xác định input chính xác. | `/Users/aiot/Downloads/book.pdf` |
| Sách/tài liệu viết về gì? | Chọn thuật ngữ, ví dụ, giọng giải thích. | System design, backend, AI, English learning |
| Muốn output tên gì? | Tạo folder không dấu, an toàn cho Git. | `bytebytego-2025`, `study-system-design` |
| Tách theo gì? | Tránh cắt sai nội dung. | Theo bài, theo chương, theo heading lớn, theo từng trang |
| Có cần giữ bản gốc Markdown không? | Dễ đối chiếu khi dịch sai. | Có, luôn giữ `original/` |
| Có cần tách và nhúng ảnh không? | PDF kỹ thuật thường phụ thuộc diagram. | Có, tách ảnh riêng trong `assets/` |
| Phong cách dịch thế nào? | Đảm bảo người đọc hiểu đúng. | Dịch sát, giải thích theo tư duy lập trình |
| Có thêm ví dụ minh họa không? | Ví dụ giúp học nhanh nhưng phải tách khỏi nội dung gốc. | Có, ví dụ backend/e-commerce/real system |
| Có được public repo không? | Tránh vi phạm bản quyền. | Chỉ private/internal nếu chứa full content |

## Luồng thực hiện chuẩn

### 1. Chuẩn bị thư mục

- Dùng tên folder không dấu, dạng `kebab-case`: `study-system-design`, `bytebytego-2025`.
- Tránh tên tiếng Việt có dấu trong path nếu cần push Git hoặc chạy script đa nền tảng.
- Tạo `output/<project-slug>/`, `scripts/`, `docs/`.

### 2. Inspect PDF

- Đếm số trang.
- Kiểm tra PDF là text-based hay scan/OCR.
- Render vài trang đầu/cuối để nhìn layout thật.
- Xác định quy luật title: font size, vị trí heading, mục lục, số trang, chapter marker.

Command tham khảo:

```zsh
pdfinfo /path/to/book.pdf
pdftotext -layout /path/to/book.pdf /tmp/book.txt
pdfimages -list /path/to/book.pdf | head
```

Nếu PDF là scan, cần OCR trước; nếu PDF đã có text layer, ưu tiên `pdftotext`/`pdfplumber` để giảm lỗi.

### 3. Tạo manifest

Manifest là nguồn sự thật để biết mỗi bài/chương bắt đầu và kết thúc ở trang nào.

Nên lưu cả JSON và Markdown:

- `manifest/articles.json`: để script đọc lại.
- `manifest/toc.md`: để người đọc kiểm tra nhanh.

Mỗi item nên có:

- `id`: số thứ tự, format `001`, `002` khi ghi file.
- `title`: title gốc.
- `slug`: tên file không dấu.
- `start_page`, `end_page`: page range trong PDF.
- `original_path`, `vi_path`, `asset_dir`.
- `image_count`.

### 4. Tách ảnh/diagram

- Dùng `pdfimages` để extract ảnh gốc.
- Lọc ảnh quá nhỏ như icon, logo, bullet decoration.
- Gom ảnh theo bài/chương: `assets/001/figure-01.png`.
- Không nhúng ảnh bằng absolute path trong Markdown repo; dùng relative path để GitHub render được.

Quy ước link:

```md
![Tên bài - hình 1](../assets/001/figure-01.png)
```

### 5. Extract bản gốc Markdown

Mục tiêu bản gốc là để đối chiếu, không phải viết lại.

Quy tắc:

- Giữ title gốc.
- Ghi source và page range.
- Nhúng hình trước phần text nếu tài liệu phụ thuộc diagram.
- Làm sạch unicode/lỗi layout cơ bản: khoảng trắng thừa, smart quote, dash, page break.
- Không tự dịch hoặc diễn giải trong `original/`.

Template:

```md
# 001 - Article Title

- Source: <book name>
- PDF pages: 8-9
- Figures: 1

## Figures

![Article Title - figure 1](../assets/001/figure-01.png)

## Original Extracted Text

<text extracted from PDF>
```

### 6. Dịch sang tiếng Việt

Mục tiêu bản dịch là `dịch sát + dễ hiểu`, không phải phóng tác.

Nên dùng cấu trúc ổn định:

```md
# 001 - Tên bài gốc

- Nguồn: <book name>
- Trang PDF: 8-9
- Ảnh: 1

## Hình minh họa

![Tên bài - hình 1](../assets/001/figure-01.png)

## Dịch sát

<bản dịch bám sát nội dung gốc>

## Tóm tắt

<giải thích ngắn, dễ hiểu>

## Ví dụ thực tế - không nằm trong tài liệu gốc

<ví dụ tự thêm, gắn với lĩnh vực người học quan tâm>

## Thuật ngữ chính

| Thuật ngữ | Nghĩa trong bài |
|---|---|

## Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ

> Đây là phần học tập thêm ở cuối file. Câu hỏi ưu tiên lấy từ tài liệu gốc; nếu bài không có câu hỏi riêng thì dùng tiêu đề/nội dung chính để tạo câu hỏi tự kiểm tra.

### Câu hỏi 1

**Nguồn câu hỏi:** Câu hỏi trong tài liệu gốc.

**Câu hỏi:** <question>

**Trả lời:** <trả lời trực tiếp câu hỏi>

**Thinking học tập + liên hệ:** <khung suy nghĩ công khai giúp người đọc biết cách trả lời và liên hệ project thật>
```

Quy tắc dịch:

- Giữ thuật ngữ kỹ thuật tiếng Anh nếu bản dịch tiếng Việt kém tự nhiên: `load balancer`, `cache`, `sharding`, `rate limiting`.
- Khi dịch thuật ngữ lần đầu, có thể viết `bộ cân bằng tải (load balancer)`.
- Không thêm claim mới vào mục `Dịch sát` nếu PDF không nói.
- Nếu cần giải thích thêm, đặt vào `Tóm tắt` hoặc `Ví dụ thực tế - không nằm trong tài liệu gốc`.
- Ở cuối mỗi file dịch, thêm `Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ` để biến câu hỏi trong tài liệu gốc thành câu trả lời tham khảo.
- Dùng đúng nhãn `Trả lời`; câu trả lời phải trả lời trực tiếp câu hỏi đã đặt ra.
- `Thinking học tập + liên hệ` nên là cách suy nghĩ công khai: problem statement, luồng chính, trade-off, khi nào dùng/không dùng, scale, failure mode, observability và liên hệ với project thật.
- Nếu ảnh có chữ quan trọng, dịch ý chính của chữ trong ảnh ở gần hình hoặc trong phần tóm tắt.

### 7. Tạo mục lục và README tiến độ

README của từng output nên có:

- Giới thiệu ngắn.
- Quy ước thư mục.
- Link tới `original/` và `vi/` cho từng bài/chương.
- Trạng thái `Đã dịch`/`Chưa dịch`.
- Link tới mục lục tóm tắt tiếng Việt.

Mục lục tóm tắt tiếng Việt nên có:

- Số thứ tự.
- Trang PDF.
- Tên bài.
- Link bản dịch.
- Một câu “học được gì”.

### 8. Audit chất lượng

Audit tối thiểu:

- Số bài trong manifest = số file `original` = số file `vi`.
- Tất cả image link trong Markdown trỏ tới file tồn tại.
- Mỗi bài tiếng Việt có đủ section bắt buộc.
- Mỗi bài tiếng Việt có phần `Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ` ở cuối file.
- Bảng mục lục có đủ số dòng.
- Không còn placeholder như `TODO`, `TBD`, `dịch sau`.

Command kiểm image link tham khảo:

```zsh
python3 - <<'PY'
from pathlib import Path
import re

root = Path('output/<project-slug>')
missing = []

for md in root.rglob('*.md'):
    for match in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', md.read_text()):
        target = (md.parent / match.group(1)).resolve()
        if not target.exists():
            missing.append((str(md), match.group(1)))

print('missing_image_links', len(missing))
if missing:
    print(missing[:20])
PY
```

## Chiến lược làm theo batch

Với PDF dài, không nên dịch một lần toàn bộ bằng tay.

- Batch 1: tạo manifest + extract ảnh + original Markdown.
- Batch 2: dịch 5-10 bài đầu để kiểm format.
- Batch 3: audit format rồi mới dịch hàng loạt.
- Batch 4: tạo mục lục tóm tắt.
- Batch 5: audit cuối và review ngẫu nhiên một số bài có nhiều diagram.

## Lưu ý bản quyền khi đưa lên Git

- Nếu repo chứa full text, bản dịch đầy đủ hoặc ảnh trích từ sách có bản quyền, nên để repo `private` hoặc dùng nội bộ.
- Nếu muốn public repo, chỉ nên public workflow, script, prompt và ghi chú tự viết; không public toàn bộ nội dung gốc/ảnh/dịch nếu chưa có quyền phân phối.
- README cần nói rõ nguồn tài liệu và phạm vi sử dụng.
