# Checklist kiểm chất lượng convert PDF sang Markdown

Checklist này dùng trước khi báo hoàn tất, commit hoặc push repo.

## Trước khi convert

- [ ] Đường dẫn PDF đúng và đọc được.
- [ ] Tên output folder không dấu, dạng `kebab-case`.
- [ ] Đã xác định chủ đề tài liệu và người đọc chính.
- [ ] Đã chốt tách theo bài/chương/heading/page.
- [ ] Đã chốt có giữ bản gốc `original/` hay không.
- [ ] Đã chốt có tách ảnh/diagram và nhúng lại hay không.
- [ ] Đã chốt repo/output private hay public nếu nội dung có bản quyền.

## Manifest

- [ ] Có `manifest/articles.json` hoặc manifest tương đương.
- [ ] Mỗi item có `id`, `title`, `slug`, `start_page`, `end_page`.
- [ ] Page range không overlap sai.
- [ ] Không thiếu bài/chương so với mục lục PDF.
- [ ] Tên file có số thứ tự ổn định: `001-title.md`.

## Ảnh/diagram

- [ ] Ảnh nằm trong `assets/<id>/`.
- [ ] Tên ảnh ổn định: `figure-01.png`, `figure-02.png`.
- [ ] Đã lọc icon/logo nhỏ không cần thiết.
- [ ] Markdown dùng relative link, không dùng absolute local path.
- [ ] Không có link ảnh bị gãy.

## Bản gốc Markdown

- [ ] Mỗi bài/chương có file trong `original/`.
- [ ] Có source và page range.
- [ ] Text được làm sạch khoảng trắng/page break cơ bản.
- [ ] Không tự ý dịch hoặc thêm diễn giải vào bản gốc.
- [ ] Có hình minh họa nếu bài gốc phụ thuộc diagram.

## Bản dịch tiếng Việt

- [ ] Mỗi bài/chương có file tương ứng trong `vi/`.
- [ ] Phần `Dịch sát` không thêm ý ngoài tài liệu.
- [ ] Thuật ngữ kỹ thuật được giữ tiếng Anh khi hợp lý.
- [ ] Có `Tóm tắt` giúp người đọc hiểu nhanh.
- [ ] Ví dụ tự thêm nằm trong `Ví dụ thực tế - không nằm trong tài liệu gốc`.
- [ ] Có bảng hoặc danh sách `Thuật ngữ chính` nếu bài có nhiều thuật ngữ.
- [ ] Không còn placeholder như `TODO`, `TBD`, `dịch sau`, `fix later`.

## README và mục lục

- [ ] README gốc mô tả repo, cấu trúc, cách đọc, cách audit.
- [ ] README trong output có bảng link gốc/dịch cho từng bài.
- [ ] Có mục lục tóm tắt tiếng Việt.
- [ ] Số dòng mục lục khớp số bài/chương.
- [ ] Có ghi chú bản quyền/phạm vi sử dụng nếu tài liệu không phải do mình sở hữu.

## Audit command mẫu

```zsh
python3 - <<'PY'
from pathlib import Path
import json
import re

root = Path('output/<project-slug>')
manifest = json.loads((root / 'manifest/articles.json').read_text())
originals = sorted((root / 'original').glob('*.md'))
translations = sorted(p for p in (root / 'vi').glob('*.md') if not p.name.startswith('000-'))
missing_images = []
missing_sections = []
bad_placeholders = []
required_sections = [
    '## Hình minh họa',
    '## Dịch sát',
    '## Tóm tắt',
    '## Ví dụ thực tế - không nằm trong tài liệu gốc',
    '## Thuật ngữ chính',
]

for md in sorted(list(root.rglob('*.md'))):
    text = md.read_text()
    for match in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', text):
        if not (md.parent / match.group(1)).resolve().exists():
            missing_images.append((str(md), match.group(1)))
    if re.search(r'\b(TODO|TBD|dịch sau|fix later)\b', text, flags=re.I):
        bad_placeholders.append(str(md))

for md in translations:
    text = md.read_text()
    missed = [section for section in required_sections if section not in text]
    if missed:
        missing_sections.append((str(md), missed))

print('manifest_articles', manifest['article_count'])
print('originals', len(originals))
print('translations', len(translations))
print('missing_images', len(missing_images))
print('missing_sections', len(missing_sections))
print('bad_placeholders', len(bad_placeholders))

if missing_images:
    print('missing_images_sample', missing_images[:10])
if missing_sections:
    print('missing_sections_sample', missing_sections[:5])
if bad_placeholders:
    print('bad_placeholders_sample', bad_placeholders[:10])
PY
```

## Trước khi push Git

- [ ] `git status` chỉ có file mình muốn commit.
- [ ] `.work/`, cache, file tạm đã được ignore.
- [ ] Nếu repo public, không push full text/ảnh/dịch của sách có bản quyền khi chưa có quyền phân phối.
- [ ] Nếu cần lưu full output, chuyển repo sang private trước.
- [ ] Commit message mô tả đúng nội dung, ví dụ `Initial commit` hoặc `Add PDF conversion workflow and notes`.

