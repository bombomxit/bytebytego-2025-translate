# ByteByteGo 2025 - Vietnamese System Design Study Notes

Repo này lưu bản chuyển đổi từ PDF `Bytebytego_Big_Archive_System_Design_2025.pdf` sang Markdown để học system design theo luồng dễ đọc hơn.

Mỗi bài được tách riêng thành 2 bản:

- Bản gốc tiếng Anh đã extract và làm sạch nhẹ.
- Bản tiếng Việt dịch sát, có giải thích theo tư duy lập trình/system design.

> Lưu ý bản quyền: nội dung gốc thuộc tác giả/đơn vị phát hành tài liệu. Repo này nên dùng cho mục đích học cá nhân hoặc nội bộ khi có quyền sử dụng phù hợp; không nên public lại toàn bộ sách nếu chưa có quyền phân phối.

## Nội dung

- Tổng số bài đã tách: `217`.
- Tổng số ảnh/diagram đã tách: `226`.
- Mục lục tiếng Việt: `output/bytebytego-2025/vi/000-muc-luc-tom-tat.md`.
- README chi tiết theo bộ sách: `output/bytebytego-2025/README.md`.
- Script pipeline hiện tại: `scripts/bytebytego_pipeline.py`.

## Cấu trúc

```text
.
├── docs/
│   ├── conversion-quality-checklist.md
│   ├── pdf-to-markdown-workflow.md
│   └── pdf-to-markdown-prompt-template.md
├── output/
│   └── bytebytego-2025/
│       ├── assets/        # ảnh/diagram tách từ PDF
│       ├── manifest/      # danh sách bài, page range, đường dẫn
│       ├── original/      # Markdown gốc tiếng Anh
│       ├── vi/            # Markdown dịch tiếng Việt
│       └── README.md      # mục lục tiến độ từng bài
└── scripts/
    └── bytebytego_pipeline.py
```

## Cách đọc

- Nếu muốn học nhanh bằng tiếng Việt: mở `output/bytebytego-2025/vi/000-muc-luc-tom-tat.md`.
- Nếu muốn đối chiếu bản gốc: mở file cùng số thứ tự trong `output/bytebytego-2025/original/` và `output/bytebytego-2025/vi/`.
- Ảnh được tách riêng trong `output/bytebytego-2025/assets/` và nhúng lại vào từng file Markdown bằng relative link.

## Quy ước bản dịch

- Dịch sát ý gốc, không tự thêm nội dung vào phần dịch chính.
- Giữ thuật ngữ tiếng Anh khi đó là thuật ngữ kỹ thuật quen dùng: `API Gateway`, `cache`, `JWT`, `RAG`, `load balancer`, `rate limiting`.
- Ví dụ tự thêm luôn nằm trong mục `Ví dụ thực tế - không nằm trong tài liệu gốc`.
- Mỗi bài tiếng Việt ưu tiên cấu trúc: hình minh họa, dịch sát, tóm tắt, ví dụ thực tế, thuật ngữ chính.

## Tái sử dụng cho PDF khác

Các tài liệu trong `docs/` mô tả lại luồng chính để convert PDF khác sang Markdown:

- `docs/pdf-to-markdown-workflow.md`: workflow từng bước từ PDF sang Markdown có ảnh.
- `docs/pdf-to-markdown-prompt-template.md`: prompt mẫu để đưa cho Codex/AI khi convert sách khác.
- `docs/conversion-quality-checklist.md`: checklist audit trước khi commit/push.

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

for md in sorted(list((root / 'original').glob('*.md')) + list((root / 'vi').glob('*.md'))):
    text = md.read_text()
    for match in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', text):
        if not (md.parent / match.group(1)).resolve().exists():
            missing.append((str(md), match.group(1)))

summary = (root / 'vi/000-muc-luc-tom-tat.md').read_text()
readme = (root / 'README.md').read_text()

print('manifest_articles', manifest['article_count'])
print('originals', len(list((root / 'original').glob('*.md'))))
print('vi_articles', len(vi_articles))
print('summary_rows', len(re.findall(r'^\| \d{3} \|', summary, flags=re.M)))
print('readme_done_rows', sum('Đã dịch' in line for line in readme.splitlines()))
print('missing_image_links', len(missing))
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
```

