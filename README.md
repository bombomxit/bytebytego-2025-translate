# Tủ sách System Design - Tiếng Việt

Hai bộ tài liệu để học thiết kế hệ thống: **System Design Interview** của Alex Xu để đọc theo chương và luyện bài thiết kế; **ByteByteGo 2025** để tra cứu từng chủ đề qua bài ngắn và sơ đồ.

## Chọn tài liệu

| Bộ tài liệu | Nội dung | Bắt đầu đọc |
| --- | --- | --- |
| **System Design Interview - Tập 1** | 16 chương, lời đầu và lời kết; đối chiếu 269 trang PDF nguồn, 226 ảnh gốc | [Mục lục tập 1](output/system-design-interview-vol-1/README.md) · [Chương 1](output/system-design-interview-vol-1/vi/chuong-01-mo-rong-tu-con-so-khong-den-hang-trieu-nguoi-dung.md) |
| **ByteByteGo 2025** | 217 bài tiếng Việt, bản đối chiếu tiếng Anh và 226 ảnh | [Mục lục tóm tắt](output/bytebytego-2025/vi/000-muc-luc-tom-tat.md) · [Danh sách đầy đủ](output/bytebytego-2025/README.md) |

[Mở thư mục docs](docs/README.md) để xem các bộ tài liệu, bài chia sẻ và hướng dẫn biên tập ở cùng một nơi.

## Cách dùng

- **Học theo mạch:** đọc tập 1 từ chương 1-3 để xây nền tảng và khung phỏng vấn, rồi chọn bài thiết kế từ chương 4-15. Mỗi chương có điều hướng trước/sau và về mục lục.
- **Tra cứu nhanh:** mở mục lục ByteByteGo, tìm tên chủ đề và đọc từng bài. Bản gốc và bản Việt giữ cùng số thứ tự để dễ đối chiếu.
- **Liên hệ công việc:** đọc bài [Một request chậm đi qua hệ thống như thế nào](docs/superpowers/sharing/2026-08-06-request-cache-database-sharing.md), từ browser tới Redis và database.

## Quy ước nội dung

Bản dịch chính giữ ý và cấu trúc của nguồn. Ghi chú, ví dụ hoặc phần học tập được bổ sung có nhãn riêng để phân biệt với lời tác giả. Ảnh được nhúng bằng đường dẫn tương đối; nhãn trong ảnh gốc có thể vẫn là tiếng Anh. Mỗi bộ ghi rõ phạm vi và cách kiểm tra ở README của bộ đó.

> Lưu ý bản quyền: nội dung gốc thuộc tác giả/đơn vị phát hành tài liệu. Repo này nên dùng cho mục đích học cá nhân hoặc nội bộ khi có quyền sử dụng phù hợp; không nên public lại toàn bộ sách nếu chưa có quyền phân phối.

## Cấu trúc

```text
.
├── docs/
│   ├── README.md                         # Tủ sách, bài chia sẻ, hướng dẫn biên tập
│   ├── pdf-to-markdown-workflow.md
│   ├── pdf-to-markdown-prompt-template.md
│   ├── conversion-quality-checklist.md
│   └── superpowers/sharing/               # Bài chia sẻ theo chủ đề
├── output/
│   ├── bytebytego-2025/                   # Giữ các đường dẫn hiện có
│   │   ├── original/
│   │   ├── vi/
│   │   ├── assets/
│   │   ├── manifest/
│   │   └── README.md
│   └── system-design-interview-vol-1/
│       ├── vi/                           # 16 chương, lời đầu/kết, thuật ngữ
│       ├── assets/                       # 226 ảnh gốc
│       ├── manifest/                     # Phạm vi trang và metadata kiểm tra
│       ├── QA.md
│       └── README.md
└── scripts/
    ├── audit_docs.py                      # Kiểm tra cả hai bộ và liên kết
    ├── add_study_questions.py
    └── bytebytego_pipeline.py
```

## Biên tập và kiểm tra

- [Workflow PDF sang Markdown](docs/pdf-to-markdown-workflow.md)
- [Prompt mẫu cho tài liệu mới](docs/pdf-to-markdown-prompt-template.md)
- [Checklist chất lượng](docs/conversion-quality-checklist.md)

Kiểm tra liên kết Markdown, ảnh và phạm vi tập 1 từ thư mục repo; lệnh này không cần PDF nguồn hoặc thư viện ngoài:

```sh
python3 scripts/audit_docs.py
```

<details>
<summary>Chạy lại pipeline và audit riêng ByteByteGo</summary>

## Chạy lại pipeline ByteByteGo

Script hiện tại đang hard-code đường dẫn PDF và output cho cuốn ByteByteGo. Nếu muốn chạy lại:

```zsh
python3 scripts/bytebytego_pipeline.py all --force
```

Chạy từng phần:

```zsh
python3 scripts/bytebytego_pipeline.py manifest
python3 scripts/bytebytego_pipeline.py images --force
python3 scripts/bytebytego_pipeline.py originals --force
python3 scripts/bytebytego_pipeline.py readme
```

Bổ sung hoặc sinh lại phần câu hỏi cuối mỗi bài dịch:

```zsh
python3 scripts/add_study_questions.py
```

## Audit nhanh

```zsh
python3 - <<'PY'
from pathlib import Path
import json
import re

root = Path('output/bytebytego-2025')
manifest = json.loads((root / 'manifest/articles.json').read_text())
vi_articles = sorted(p for p in (root / 'vi').glob('*.md') if not p.name.startswith('000-'))
missing = []
missing_study_questions = []

for md in sorted(list((root / 'original').glob('*.md')) + list((root / 'vi').glob('*.md'))):
    text = md.read_text()
    for match in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', text):
        if not (md.parent / match.group(1)).resolve().exists():
            missing.append((str(md), match.group(1)))

for md in vi_articles:
    text = md.read_text()
    if '## Câu hỏi ôn tập + trả lời + thinking học tập + liên hệ' not in text:
        missing_study_questions.append(md.name)

summary = (root / 'vi/000-muc-luc-tom-tat.md').read_text()
readme = (root / 'README.md').read_text()

print('manifest_articles', manifest['article_count'])
print('originals', len(list((root / 'original').glob('*.md'))))
print('vi_articles', len(vi_articles))
print('summary_rows', len(re.findall(r'^\| \d{3} \|', summary, flags=re.M)))
print('readme_done_rows', sum('Đã dịch' in line for line in readme.splitlines()))
print('missing_image_links', len(missing))
print('missing_study_questions', len(missing_study_questions))
PY
```

Kết quả tốt hiện tại:

```text
manifest_articles 217
originals 217
vi_articles 217
summary_rows 217
readme_done_rows 217
missing_image_links 0
missing_study_questions 0
```

</details>
