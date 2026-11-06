#!/usr/bin/env python3
"""Audit portable: liên kết Markdown, tập 1 và cấu trúc ByteByteGo."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "output/system-design-interview-vol-1"
BYTEBYTEGO = ROOT / "output/bytebytego-2025"


def markdown_links(text):
    """Bỏ ví dụ trong code; lấy đường dẫn của inline links và ảnh."""
    text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", "", text)
    return re.findall(r"!?\[[^\]]*\]\((<[^>]+>|[^)\n]+)\)", text)


def audit():
    errors = []
    markdown_files = sorted(ROOT.glob("*.md"))
    markdown_files += sorted((ROOT / "docs").rglob("*.md"))
    markdown_files += sorted((ROOT / "output").rglob("*.md"))
    links_checked = 0
    for path in markdown_files:
        for link in markdown_links(path.read_text()):
            target = link.strip("<>").split("#", 1)[0]
            if not target or urlsplit(target).scheme:
                continue
            links_checked += 1
            if not (path.parent / unquote(target)).exists():
                errors.append(f"{path.relative_to(ROOT)}: link không tồn tại: {link}")

    manifest = json.loads((BOOK / "manifest/chapters.json").read_text())
    chapters = manifest["chapters"]
    if [c["chapter"] for c in chapters] != list(range(1, 17)):
        errors.append("Manifest tập 1 phải có đúng chương 1-16 theo thứ tự")

    targets = [("vi/00-loi-mo-dau.md", 1, 4)]
    targets += [(c["output"], c["start"], c["end"]) for c in chapters]
    targets += [("vi/17-loi-ket.md", 269, 269)]
    markers_total = 0
    images_total = 0
    all_pages = []
    for filename, first, last in targets:
        path = BOOK / filename
        if not path.exists():
            errors.append(f"Tập 1 thiếu file {filename}")
            continue
        text = path.read_text()
        expected_pages = list(range(first, last + 1))
        markers = [int(v) for v in re.findall(r"<!-- trang-pdf:(\d{3}) -->", text)]
        markers_total += len(markers)
        all_pages.extend(markers)
        if markers != expected_pages:
            errors.append(f"{filename}: marker trang không khớp {first}-{last}")
        expected_images = [
            image for page in expected_pages
            for image in manifest["images_by_page"].get(str(page), [])
        ]
        actual_images = []
        for image in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
            try:
                actual_images.append((path.parent / image).resolve().relative_to(BOOK).as_posix())
            except ValueError:
                errors.append(f"{filename}: ảnh nằm ngoài bộ sách: {image}")
        images_total += len(actual_images)
        if actual_images != expected_images:
            errors.append(f"{filename}: ảnh thiếu, thừa hoặc không đúng thứ tự")
        if len(re.findall(r"^# ", text, re.M)) != 1:
            errors.append(f"{filename}: cần đúng một H1")
        if len(re.findall(r"^```", text, re.M)) % 2:
            errors.append(f"{filename}: code fence chưa đóng")

    if all_pages != list(range(1, 270)):
        errors.append("Tập 1 không bao phủ đúng 269 trang nguồn")
    assets = sorted(p for p in (BOOK / "assets").rglob("*") if p.is_file())
    vi_files = sorted((BOOK / "vi").glob("*.md"))
    if len(assets) != 226 or images_total != 226 or len(vi_files) != 19:
        errors.append("Tập 1 cần 19 file vi (kể cả thuật ngữ) và 226 ảnh")
    if list(BOOK.rglob("*.pdf")) or list(BOOK.rglob("*.txt")) or (BOOK / "nguon").exists():
        errors.append("Bộ sách đóng gói chứa PDF hoặc văn bản nguồn local")

    byte_manifest = json.loads((BYTEBYTEGO / "manifest/articles.json").read_text())
    articles = byte_manifest["articles"]
    original_count = len(list((BYTEBYTEGO / "original").glob("*.md")))
    vi_count = len([p for p in (BYTEBYTEGO / "vi").glob("*.md") if not p.name.startswith("000-")])
    byte_images = len([p for p in (BYTEBYTEGO / "assets").rglob("*") if p.is_file()])
    if len(articles) != 217 or byte_manifest["article_count"] != 217:
        errors.append("Manifest ByteByteGo không đủ 217 bài")
    if (original_count, vi_count, byte_images) != (217, 217, 226):
        errors.append("ByteByteGo không còn đủ 217 bản gốc/217 bản Việt/226 ảnh")
    for article in articles:
        for key in ("original_path", "vi_path"):
            if not (BYTEBYTEGO / article[key]).exists():
                errors.append(f"ByteByteGo thiếu {article[key]}")

    return {
        "markdown_files": len(markdown_files),
        "local_links_checked": links_checked,
        "system_design_interview": {
            "chapters": len(chapters), "content_files": len(targets),
            "vi_files_with_glossary": len(vi_files),
            "source_page_markers": markers_total,
            "images": len(assets), "image_links": images_total,
        },
        "bytebytego": {"originals": original_count, "translations": vi_count, "images": byte_images},
        "errors": errors,
        "passed": not errors,
    }


if __name__ == "__main__":
    try:
        result = audit()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Không thể audit tài liệu: {exc}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["passed"] else 1)
