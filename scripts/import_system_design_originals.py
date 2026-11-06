#!/usr/bin/env python3
"""Xuất Markdown tiếng Anh tập 1 từ PDF local đã xác minh SHA-256."""

import argparse
import hashlib
import html
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "output/system-design-interview-vol-1"


def text_hash(text):
    return hashlib.sha256(" ".join(text.split()).encode("utf-8")).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_pdf", type=Path)
    args = parser.parse_args()
    manifest = json.loads((BOOK / "manifest/chapters.json").read_text())
    if hashlib.sha256(args.source_pdf.read_bytes()).hexdigest() != manifest["sha256"]:
        parser.error("PDF không khớp SHA-256 của tập 1 trong manifest")
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(args.source_pdf.resolve()), "-"],
        check=True, capture_output=True, text=True, encoding="utf-8",
    )
    pages = result.stdout.split("\f")
    if not pages[-1].strip():
        pages.pop()
    if len(pages) != manifest["pages"]:
        parser.error(f"Cần {manifest['pages']} trang, nhận được {len(pages)}")

    sections = [manifest["front_matter"], *manifest["chapters"], manifest["afterword"]]
    checks = {
        "source_sha256": manifest["sha256"],
        "extraction": "pdftotext -layout -enc UTF-8",
        "normalization": "Whitespace only; HTML entities decoded before comparison",
        "page_text_sha256": {str(n): text_hash(page) for n, page in enumerate(pages, 1)},
    }
    for index, section in enumerate(sections):
        target = BOOK / section["original_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        title = section["original_title"]
        if "chapter" in section:
            title = f"Chapter {section['chapter']}: {title}"
        vi_name = Path(section["output"]).name
        lines = [
            f"# {title}", "",
            f"[Tiếng Việt](../vi/{vi_name}) · [Mục lục / Contents](../README.md)", "",
            "- Source: System Design Interview: An Insider's Guide, Alex Xu",
            f"- PDF pages: {section['start']:03d}-{section['end']:03d}", "",
            "> Original English text extracted from the supplied PDF, not translated back from Vietnamese. "
            "Figures are grouped after the text of their PDF page. PDF line wrapping, "
            "tables and formulas may require viewing the accompanying original figures.", "",
            "## Original English Text", "",
        ]
        for number in range(section["start"], section["end"] + 1):
            lines.extend([f"<!-- trang-pdf:{number:03d} -->", ""])
            # Avoid accidental indented code blocks and HTML tags; retain every text token.
            text = "\n".join(line.strip() for line in pages[number - 1].strip().splitlines())
            if text:
                lines.extend([html.escape(text, quote=False), ""])
            for image_index, image in enumerate(manifest["images_by_page"].get(str(number), []), 1):
                lines.extend([f"![Original figure - PDF page {number:03d}, image {image_index}](../{image})", ""])
            lines.extend([f"<!-- /trang-pdf:{number:03d} -->", ""])
        navigation = []
        if index:
            navigation.append(f"[← Previous]({Path(sections[index - 1]['original_path']).name})")
        navigation.extend(["[Contents](../README.md)", f"[Tiếng Việt](../vi/{vi_name})"])
        if index + 1 < len(sections):
            navigation.append(f"[Next →]({Path(sections[index + 1]['original_path']).name})")
        lines.extend(["---", "", " · ".join(navigation), ""])
        target.write_text("\n".join(lines), encoding="utf-8")
    (BOOK / "manifest/original-text-checks.json").write_text(
        json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print(f"Đã xuất {len(sections)} file tiếng Anh, {len(pages)} trang nguồn")


if __name__ == "__main__":
    main()
