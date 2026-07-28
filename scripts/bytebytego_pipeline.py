#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path

import pdfplumber
from PIL import Image


PDF_PATH = Path("/Users/aiot/Downloads/Bytebytego_Big_Archive_System_Design_2025.pdf")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PROJECT_ROOT / "output" / "bytebytego-2025"
MANIFEST_DIR = OUTPUT_ROOT / "manifest"
ORIGINAL_DIR = OUTPUT_ROOT / "original"
VI_DIR = OUTPUT_ROOT / "vi"
ASSET_DIR = OUTPUT_ROOT / "assets"
WORK_DIR = PROJECT_ROOT / ".work" / "bytebytego"
FIRST_ARTICLE_PAGE = 8
TITLE_MIN_SIZE = 17.0
TITLE_TOP_MIN = 55.0
TITLE_TOP_MAX = 150.0
MIN_IMAGE_AREA = 50_000
MIN_IMAGE_SIDE = 120


@dataclass
class Article:
    id: int
    title: str
    slug: str
    start_page: int
    end_page: int
    original_path: str
    vi_path: str
    asset_dir: str
    image_count: int = 0


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    ascii_text = re.sub(r"-+", "-", ascii_text).strip("-")
    return ascii_text or "article"


def normalize_text(value: str) -> str:
    value = value.replace("\u200b", "")
    value = value.replace("\ufeff", "")
    value = value.replace("\xa0", " ")
    value = value.replace("\u2011", "-")
    value = value.replace("\u2013", "-")
    value = value.replace("\u2014", "-")
    value = value.replace("\u2018", "'")
    value = value.replace("\u2019", "'")
    value = value.replace("\u201c", '"')
    value = value.replace("\u201d", '"')
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def extract_title_from_page(page: pdfplumber.page.Page) -> str | None:
    words = page.extract_words(
        extra_attrs=["size", "fontname"],
        keep_blank_chars=False,
        use_text_flow=True,
    ) or []
    title_words = []
    for word in words:
        size = float(word.get("size") or 0)
        font = word.get("fontname", "")
        top = float(word.get("top") or 0)
        if TITLE_TOP_MIN <= top <= TITLE_TOP_MAX and size >= TITLE_MIN_SIZE and "Bold" in font:
            title_words.append(word)
    if not title_words:
        return None

    lines: list[tuple[float, list[dict]]] = []
    for word in sorted(title_words, key=lambda item: (round(float(item["top"]) / 4) * 4, float(item["x0"]))):
        top = round(float(word["top"]) / 4) * 4
        if not lines or abs(lines[-1][0] - top) > 4:
            lines.append((top, [word]))
        else:
            lines[-1][1].append(word)

    parts = []
    for _, line_words in lines:
        parts.append(" ".join(word["text"] for word in sorted(line_words, key=lambda item: float(item["x0"]))))
    title = re.sub(r"\s+", " ", " ".join(parts)).strip()
    return title or None


def build_manifest() -> list[Article]:
    with pdfplumber.open(str(PDF_PATH)) as document:
        starts: list[tuple[int, str]] = []
        for page_number, page in enumerate(document.pages, start=1):
            if page_number < FIRST_ARTICLE_PAGE:
                continue
            title = extract_title_from_page(page)
            if title:
                starts.append((page_number, normalize_text(title)))
        total_pages = len(document.pages)

    articles: list[Article] = []
    for index, (start_page, title) in enumerate(starts, start=1):
        end_page = starts[index][0] - 1 if index < len(starts) else total_pages
        slug = slugify(title)
        filename = f"{index:03d}-{slug}.md"
        article = Article(
            id=index,
            title=title,
            slug=slug,
            start_page=start_page,
            end_page=end_page,
            original_path=str((ORIGINAL_DIR / filename).relative_to(OUTPUT_ROOT)),
            vi_path=str((VI_DIR / filename).relative_to(OUTPUT_ROOT)),
            asset_dir=str((ASSET_DIR / f"{index:03d}").relative_to(OUTPUT_ROOT)),
        )
        articles.append(article)
    return articles


def write_manifest(articles: list[Article]) -> None:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_pdf": str(PDF_PATH),
        "article_count": len(articles),
        "articles": [asdict(article) for article in articles],
    }
    (MANIFEST_DIR / "articles.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    lines = ["# ByteByteGo Big Archive System Design 2025 - Manifest", ""]
    lines.append(f"- Source PDF: `{PDF_PATH}`")
    lines.append(f"- Article count: {len(articles)}")
    lines.append("")
    lines.append("| # | Pages | Title | Original | Vietnamese |")
    lines.append("|---:|---:|---|---|---|")
    for article in articles:
        lines.append(
            f"| {article.id:03d} | {article.start_page}-{article.end_page} | {article.title} | "
            f"[{Path(article.original_path).name}](../{article.original_path}) | "
            f"[{Path(article.vi_path).name}](../{article.vi_path}) |"
        )
    (MANIFEST_DIR / "toc.md").write_text("\n".join(lines) + "\n")


def load_manifest() -> list[Article]:
    manifest_path = MANIFEST_DIR / "articles.json"
    if not manifest_path.exists():
        articles = build_manifest()
        write_manifest(articles)
        return articles
    data = json.loads(manifest_path.read_text())
    return [Article(**article) for article in data["articles"]]


def extract_article_text(article: Article) -> str:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    text_path = WORK_DIR / f"{article.id:03d}.txt"
    run([
        "pdftotext",
        "-f",
        str(article.start_page),
        "-l",
        str(article.end_page),
        "-layout",
        str(PDF_PATH),
        str(text_path),
    ])
    text = normalize_text(text_path.read_text(errors="ignore"))
    title_pattern = re.escape(article.title).replace("\\ ", r"\s+")
    text = re.sub(rf"^\s*{title_pattern}\s*", "", text, count=1, flags=re.IGNORECASE | re.DOTALL).strip()
    return text


def extract_all_text_pages() -> list[str]:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    text_path = WORK_DIR / "all-pages.txt"
    if not text_path.exists():
        run(["pdftotext", "-layout", str(PDF_PATH), str(text_path)])
    return text_path.read_text(errors="ignore").split("\f")


def article_text_from_pages(article: Article, pages: list[str]) -> str:
    page_text = "\n".join(pages[article.start_page - 1 : article.end_page])
    text = normalize_text(page_text)
    title_pattern = re.escape(article.title).replace("\\ ", r"\s+")
    text = re.sub(rf"^\s*{title_pattern}\s*", "", text, count=1, flags=re.IGNORECASE | re.DOTALL).strip()
    return text


def retained_image_paths(article: Article) -> list[Path]:
    article_asset_dir = OUTPUT_ROOT / article.asset_dir
    if not article_asset_dir.exists():
        return []
    return sorted(article_asset_dir.glob("figure-*.*"))


def extract_images(article: Article, *, force: bool = False) -> int:
    article_asset_dir = OUTPUT_ROOT / article.asset_dir
    if article_asset_dir.exists() and retained_image_paths(article) and not force:
        return len(retained_image_paths(article))

    article_asset_dir.mkdir(parents=True, exist_ok=True)
    for existing in article_asset_dir.glob("figure-*.*"):
        existing.unlink()

    tmp_dir = WORK_DIR / "images" / f"{article.id:03d}"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    prefix = tmp_dir / "raw"
    run([
        "pdfimages",
        "-f",
        str(article.start_page),
        "-l",
        str(article.end_page),
        "-png",
        str(PDF_PATH),
        str(prefix),
    ])

    extracted = sorted(path for path in tmp_dir.iterdir() if path.is_file())
    figure_index = 1
    for image_path in extracted:
        try:
            with Image.open(image_path) as image:
                width, height = image.size
        except Exception:
            continue
        if width * height < MIN_IMAGE_AREA or min(width, height) < MIN_IMAGE_SIDE:
            continue
        suffix = image_path.suffix.lower() or ".png"
        target = article_asset_dir / f"figure-{figure_index:02d}{suffix}"
        shutil.copy2(image_path, target)
        figure_index += 1
    return figure_index - 1


def parse_pdfimages_list(output: str) -> list[dict[str, int]]:
    entries: list[dict[str, int]] = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 6 or not parts[0].isdigit() or not parts[1].isdigit():
            continue
        entries.append({
            "page": int(parts[0]),
            "num": int(parts[1]),
            "width": int(parts[3]),
            "height": int(parts[4]),
        })
    return entries


def article_for_page(articles: list[Article], page_number: int) -> Article | None:
    for article in articles:
        if article.start_page <= page_number <= article.end_page:
            return article
    return None


def extract_images_batch(articles: list[Article], *, force: bool = False) -> None:
    selected_ids = {article.id for article in articles}
    all_articles = load_manifest()
    for article in all_articles:
        article_asset_dir = OUTPUT_ROOT / article.asset_dir
        article_asset_dir.mkdir(parents=True, exist_ok=True)
        if article.id in selected_ids and force:
            for existing in article_asset_dir.glob("figure-*.*"):
                existing.unlink()

    if not force and all(retained_image_paths(article) for article in articles):
        return

    tmp_dir = WORK_DIR / "images" / "all"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    prefix = tmp_dir / "raw"
    listing = run(["pdfimages", "-list", str(PDF_PATH)]).stdout
    entries = parse_pdfimages_list(listing)
    run(["pdfimages", "-png", str(PDF_PATH), str(prefix)])
    extracted = sorted(path for path in tmp_dir.iterdir() if path.is_file())

    counters: dict[int, int] = {article.id: 0 for article in all_articles}
    for entry, image_path in zip(entries, extracted):
        article = article_for_page(all_articles, entry["page"])
        if article is None or article.id not in selected_ids:
            continue
        try:
            with Image.open(image_path) as image:
                width, height = image.size
        except Exception:
            continue
        if width * height < MIN_IMAGE_AREA or min(width, height) < MIN_IMAGE_SIDE:
            continue
        counters[article.id] += 1
        target_dir = OUTPUT_ROOT / article.asset_dir
        suffix = image_path.suffix.lower() or ".png"
        target = target_dir / f"figure-{counters[article.id]:02d}{suffix}"
        shutil.copy2(image_path, target)

    for article in all_articles:
        article.image_count = len(retained_image_paths(article))
    write_manifest(all_articles)


def markdown_image_links(article: Article, *, language: str) -> list[str]:
    links = []
    for image_path in retained_image_paths(article):
        relative = Path("../") / Path(article.asset_dir) / image_path.name
        alt = f"{article.title} - figure {len(links) + 1}"
        if language == "vi":
            alt = f"{article.title} - hình {len(links) + 1}"
        links.append(f"![{alt}]({relative.as_posix()})")
    return links


def write_original(article: Article, *, force: bool = False, pages: list[str] | None = None) -> None:
    original_path = OUTPUT_ROOT / article.original_path
    if original_path.exists() and not force:
        return
    ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
    if not retained_image_paths(article):
        extract_images(article, force=force)
    image_count = len(retained_image_paths(article))
    text = article_text_from_pages(article, pages) if pages is not None else extract_article_text(article)

    lines = [
        f"# {article.id:03d} - {article.title}",
        "",
        "- Source: ByteByteGo Big Archive System Design 2025",
        f"- PDF pages: {article.start_page}-{article.end_page}",
        f"- Figures: {image_count}",
        "",
    ]
    image_links = markdown_image_links(article, language="en")
    if image_links:
        lines.extend(["## Figures", "", *image_links, ""])
    lines.extend(["## Original Extracted Text", "", text, ""])
    original_path.write_text("\n".join(lines))


def write_readme(articles: list[Article]) -> None:
    lines = [
        "# ByteByteGo Big Archive System Design 2025 - Vietnamese Study Notes",
        "",
        "Bộ ghi chú này tách PDF thành từng bài. Mỗi bài có bản gốc tiếng Anh, bản dịch tiếng Việt, ảnh minh họa tách riêng, tóm tắt và ví dụ thực tế nếu cần.",
        "",
        "## Quy ước",
        "",
        "- `original/`: nội dung gốc tiếng Anh đã extract và làm sạch nhẹ.",
        "- `vi/`: bản dịch sát theo tư duy lập trình/system design.",
        "- `assets/`: ảnh/diagram được tách từ PDF và nhúng vào Markdown.",
        "- Các ví dụ do người dịch thêm sẽ được ghi rõ: `Ví dụ thực tế - không nằm trong tài liệu gốc`.",
        "- Mục lục tóm tắt tiếng Việt: [`vi/000-muc-luc-tom-tat.md`](vi/000-muc-luc-tom-tat.md).",
        "",
        "## Mục lục tiến độ",
        "",
        "| # | Trang | Tên bài | Gốc | Dịch | Trạng thái |",
        "|---:|---:|---|---|---|---|",
    ]
    for article in articles:
        original_exists = (OUTPUT_ROOT / article.original_path).exists()
        vi_exists = (OUTPUT_ROOT / article.vi_path).exists()
        status = "Đã dịch" if vi_exists else "Chưa dịch"
        original_link = f"[gốc]({article.original_path})" if original_exists else "-"
        vi_link = f"[vi]({article.vi_path})" if vi_exists else "-"
        lines.append(
            f"| {article.id:03d} | {article.start_page}-{article.end_page} | {article.title} | {original_link} | {vi_link} | {status} |"
        )
    (OUTPUT_ROOT / "README.md").write_text("\n".join(lines) + "\n")


def update_image_counts(articles: list[Article]) -> list[Article]:
    for article in articles:
        article.image_count = len(retained_image_paths(article))
    write_manifest(articles)
    return articles


def parse_ids(value: str | None, articles: list[Article]) -> set[int]:
    if not value:
        return {article.id for article in articles}
    result: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = [int(piece) for piece in part.split("-", 1)]
            result.update(range(start, end + 1))
        else:
            result.add(int(part))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract ByteByteGo archive articles to Markdown.")
    parser.add_argument("action", choices=["manifest", "images", "originals", "readme", "all"])
    parser.add_argument("--ids", help="Article ids, for example: 1,2,10-20")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    articles = build_manifest() if args.action == "manifest" else load_manifest()
    selected_ids = parse_ids(args.ids, articles)
    selected = [article for article in articles if article.id in selected_ids]

    if args.action in {"manifest", "all"}:
        write_manifest(articles)
    if args.action in {"images", "all"}:
        extract_images_batch(selected, force=args.force)
        articles = load_manifest()
    if args.action in {"originals", "all"}:
        pages = extract_all_text_pages()
        extract_images_batch(selected, force=args.force)
        for article in selected:
            write_original(article, force=args.force, pages=pages)
        update_image_counts(articles)
    if args.action in {"readme", "all"}:
        write_readme(articles)

    print(f"articles={len(articles)} selected={len(selected)} output={OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
