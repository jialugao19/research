#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from base64 import b64decode
from collections import OrderedDict
from hashlib import sha256
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

from research_site.catalog import CatalogError, Report, load_catalog
from research_site.report_content import REQUIRED_SECTIONS, load_report_source

MIGRATIONS = OrderedDict(
    (
        ("0502-index-6backtest", "0502-index-6backtest-v2"),
        ("0702-l2-ablation", "0702-l2-ablation-v2"),
        ("0725-1min-model-screening", "0725-1min-model-screening-v2"),
        ("0730-stock1s-feature-health", "0730-stock1s-feature-health-v2"),
        ("0731-limit-t1-strategy", "0731-limit-t1-strategy-v2"),
        ("0802-stock1s-gru384", "0802-stock1s-gru384-v2"),
    )
)
HOME_PATH_RE = re.compile(r"/home/[^/\s\"'<>]+/")


def _clean(value: str) -> str:
    value = HOME_PATH_RE.sub("[local-workspace]/", value)
    value = value.replace("/data-cache/", "[artifact-root]/")
    value = re.sub(r"https?://(?:localhost|127\.0\.0\.1)", "[local-service]", value)
    return re.sub(r"\s+", " ", value).strip()


def _escape_markdown(value: str) -> str:
    return _clean(value).replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def _bucket_for_heading(title: str, current: str) -> str:
    lowered = title.lower()
    if any(term in lowered for term in ("executive summary", "一页结论", "冻结测试验收", "health 状态")):
        return "摘要"
    if any(
        term in lowered
        for term in (
            "setup",
            "data pipeline",
            "data basics",
            "normalization",
            "clean benchmark",
            "输入与 split",
            "model and method",
            "退出状态机",
        )
    ):
        return "数据与方法"
    if any(
        term in lowered
        for term in ("comparability", "missing template", "interpretation limits", "数据边界", "限制")
    ):
        return "限制与适用边界"
    if any(term in lowered for term in ("appendix", "artifact", "manifest", "provenance", "78 维特征目录")):
        return "附录"
    if any(term in lowered for term in ("后续", "建议", "recommendation", "为什么不是继续改模型", "增删建议")):
        return "结论"
    return current if current in {"摘要", "数据与方法", "限制与适用边界", "结论", "附录"} else "主要结果"


def _table_markdown(table: Tag) -> str:
    rows: list[list[str]] = []
    for row in table.find_all("tr"):
        cells = [_clean(cell.get_text(" ", strip=True)).replace("|", "\\|") for cell in row.find_all(["th", "td"], recursive=False)]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    header = rows[0]
    result = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * width) + " |"]
    result.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join(result)


def _list_markdown(node: Tag) -> str:
    ordered = node.name == "ol"
    lines: list[str] = []
    for index, item in enumerate(node.find_all("li", recursive=False), start=1):
        prefix = f"{index}." if ordered else "-"
        lines.append(f"{prefix} {_clean(item.get_text(' ', strip=True))}")
    return "\n".join(lines)


def _paragraph_markdown(node: Tag) -> str:
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, NavigableString):
            parts.append(str(child))
        elif isinstance(child, Tag):
            text = child.get_text(" ", strip=True)
            if child.name == "code" and text:
                parts.append(f"`{text}`")
            elif child.name in {"strong", "b"} and text:
                parts.append(f"**{text}**")
            elif child.name in {"em", "i"} and text:
                parts.append(f"*{text}*")
            elif child.name == "br":
                parts.append("  \n")
            elif child.name != "img":
                parts.append(text)
    return _clean(" ".join(parts))


class Converter:
    def __init__(self, output_root: Path) -> None:
        self.output_root = output_root
        self.images_root = output_root / "images"
        self.images_root.mkdir(parents=True, exist_ok=True)
        self.sections: dict[str, list[str]] = {section: [] for section in (*REQUIRED_SECTIONS, "附录")}
        self.current_section = "主要结果"
        self.seen_blocks: set[int] = set()
        self.seen_images: set[int] = set()
        self.image_count = 0

    def _image(self, image: Tag, caption_hint: str = "") -> str:
        marker = id(image)
        if marker in self.seen_images:
            return ""
        self.seen_images.add(marker)
        source = image.get("src", "")
        match = re.fullmatch(r"data:image/(png|jpeg|webp);base64,(.+)", source, flags=re.DOTALL)
        if not match:
            raise CatalogError(f"legacy report image is not an embedded raster image: {source[:80]}")
        suffix = {"png": ".png", "jpeg": ".jpg", "webp": ".webp"}[match.group(1)]
        self.image_count += 1
        name = f"figure-{self.image_count:03d}{suffix}"
        data = b64decode(re.sub(r"\s+", "", match.group(2)), validate=True)
        (self.images_root / name).write_bytes(data)
        caption = _clean(caption_hint or image.get("alt", "") or f"原报告图表 {self.image_count}")
        alt = _escape_markdown(image.get("alt", "") or caption)
        quoted_caption = caption.replace('"', "'")
        return f'![{alt}](images/{name} "{quoted_caption}")'

    def convert(self, root: Tag) -> None:
        for node in root.descendants:
            if not isinstance(node, Tag):
                continue
            if node.name in {"script", "style", "nav", "footer"}:
                continue
            if node.find_parent(["script", "style", "nav", "footer"]):
                continue
            if node.name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                title = _clean(node.get_text(" ", strip=True))
                if node.name == "h1" or not title:
                    continue
                if node.name == "h2":
                    self.current_section = _bucket_for_heading(title, "主要结果")
                self.sections[self.current_section].append(f"### {title}")
                continue
            if node.name == "figure":
                marker = id(node)
                if marker in self.seen_blocks:
                    continue
                self.seen_blocks.add(marker)
                caption_node = node.find("figcaption")
                caption = caption_node.get_text(" ", strip=True) if caption_node else ""
                for image in node.find_all("img"):
                    rendered = self._image(image, caption)
                    if rendered:
                        self.sections[self.current_section].append(rendered)
                continue
            if node.name == "img" and not node.find_parent("figure"):
                rendered = self._image(node)
                if rendered:
                    self.sections[self.current_section].append(rendered)
                continue
            if node.find_parent(["table", "figure", "pre", "ul", "ol"]):
                continue
            if node.name == "table":
                rendered = _table_markdown(node)
            elif node.name in {"ul", "ol"} and not node.find_parent(["ul", "ol"]):
                rendered = _list_markdown(node)
            elif node.name == "pre":
                rendered = f"```text\n{node.get_text(chr(10), strip=False).strip()}\n```"
            elif node.name == "blockquote":
                rendered = "\n".join(f"> {line}" for line in _clean(node.get_text(" ", strip=True)).splitlines())
            elif node.name == "p":
                rendered = _paragraph_markdown(node)
            elif node.name == "dl":
                rendered = "\n".join(
                    f"- **{_clean(term.get_text(' ', strip=True))}**: "
                    f"{_clean(term.find_next_sibling('dd').get_text(' ', strip=True)) if term.find_next_sibling('dd') else ''}"
                    for term in node.find_all("dt", recursive=False)
                )
            else:
                continue
            marker = id(node)
            if marker not in self.seen_blocks and rendered.strip():
                self.seen_blocks.add(marker)
                self.sections[self.current_section].append(rendered.strip())


def _front_matter(report: Report) -> str:
    tags = ", ".join(report.tags)
    title = report.title.replace('"', "\\\"")
    summary = report.summary.replace('"', "\\\"")
    return (
        "---\n"
        f'title: "{title}"\n'
        f"date: {report.display_date}\n"
        f'summary: "{summary}"\n'
        f"tags: [{tags}]\n"
        f"featured: {'true' if report.featured else 'false'}\n"
        "---\n\n"
    )


def migrate(site_root: Path, archive_root: Path) -> None:
    catalog = load_catalog(site_root / "content")
    for old_id, new_id in MIGRATIONS.items():
        report = catalog.report_by_id[old_id]
        if not report.source_file or not report.source_sha256:
            raise CatalogError(f"legacy report {old_id} has no immutable HTML source")
        source_path = archive_root / report.source_file
        data = source_path.read_bytes()
        actual_hash = sha256(data).hexdigest()
        if actual_hash != report.source_sha256:
            raise CatalogError(
                f"legacy report {old_id} source checksum changed: expected {report.source_sha256}, got {actual_hash}"
            )
        output_root = site_root / "content" / "report-docs" / report.project / new_id
        if output_root.exists():
            raise CatalogError(f"refusing to overwrite existing migration target {output_root}")
        output_root.mkdir(parents=True)
        soup = BeautifulSoup(data.decode("utf-8"), "html.parser")
        root = soup.find("main") or soup.body
        if root is None:
            raise CatalogError(f"legacy report {old_id} has no renderable body")
        converter = Converter(output_root)
        converter.convert(root)
        converter.sections["摘要"].insert(0, report.summary)
        converter.sections["研究背景与目标"].insert(
            0,
            "本页是历史研究报告的统一模板版本。研究问题、实验定义、数据口径、表格和图像证据均沿用已校验的历史原版。",
        )
        if not converter.sections["数据与方法"]:
            converter.sections["数据与方法"].append("数据、实验协议与评价方法保留在下方对应的原报告小节中。")
        if not converter.sections["限制与适用边界"]:
            converter.sections["限制与适用边界"].append("解释边界与可比性限制沿用历史原版中的原始说明。")
        if not converter.sections["结论"]:
            converter.sections["结论"].append("结论与后续事项以历史原版已记录的结果为准，本次迁移不新增研究判断。")
        sections: list[str] = []
        for section in REQUIRED_SECTIONS:
            sections.append(f"## {section}\n\n" + "\n\n".join(converter.sections[section]))
        if converter.sections["附录"]:
            sections.append("## 附录\n\n" + "\n\n".join(converter.sections["附录"]))
        report_path = output_root / "report.md"
        report_path.write_text(_front_matter(report) + "\n\n".join(sections).strip() + "\n", encoding="utf-8")
        source = load_report_source(report_path)
        print(f"{old_id}\t{new_id}\t{converter.image_count}\t{source.bundle_sha256}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate immutable legacy HTML reports to Markdown v2 bundles")
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--archive-root", type=Path, default=Path.home() / "0-report-html")
    args = parser.parse_args()
    migrate(args.site_root.resolve(), args.archive_root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
