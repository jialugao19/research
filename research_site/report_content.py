from __future__ import annotations

import re
import unicodedata
from base64 import b64encode
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from html import escape
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token
from PIL import Image, UnidentifiedImageError

MAX_REPORT_BYTES = 25 * 1024 * 1024
REQUIRED_SECTIONS = (
    "摘要",
    "研究背景与目标",
    "数据与方法",
    "主要结果",
    "限制与适用边界",
    "结论",
)
OPTIONAL_SECTION = "附录"
FRONT_MATTER_FIELDS = {"title", "date", "summary", "tags", "featured"}
ALLOWED_IMAGE_SUFFIXES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
FORBIDDEN_SOURCE_TEXT = (
    "/data-cache/",
    "file://",
    "http://localhost",
    "https://localhost",
    "http://127.0.0.1",
    "https://127.0.0.1",
)
HOME_PATH_RE = re.compile(r"/home/[^/\s\"'<>]+/")
SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[oprsu]_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"glpat-[A-Za-z0-9_-]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{32,}"),
    re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----"),
)


class ReportContentError(ValueError):
    """Raised when a Markdown report bundle violates the publication contract."""


@dataclass(frozen=True)
class ReportFrontMatter:
    title: str
    date: date
    summary: str
    tags: tuple[str, ...]
    featured: bool


@dataclass(frozen=True)
class ReportSource:
    path: Path
    front_matter: ReportFrontMatter
    body: str
    referenced_assets: tuple[Path, ...]
    bundle_sha256: str


@dataclass(frozen=True)
class TocItem:
    level: int
    title: str
    anchor: str


@dataclass(frozen=True)
class RenderedReport:
    body_html: str
    toc: tuple[TocItem, ...]
    figure_count: int


def _non_empty_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReportContentError(f"report front matter {field_name} must be non-empty text")
    return value.strip()


def _parse_front_matter(path: Path, text: str) -> tuple[ReportFrontMatter, str]:
    if not text.startswith("---\n"):
        raise ReportContentError(f"{path} must start with YAML front matter")
    marker = text.find("\n---\n", 4)
    if marker < 0:
        raise ReportContentError(f"{path} has unterminated YAML front matter")
    try:
        raw = yaml.safe_load(text[4:marker])
    except yaml.YAMLError as exc:
        raise ReportContentError(f"cannot parse {path} front matter: {exc}") from exc
    if not isinstance(raw, dict):
        raise ReportContentError(f"{path} front matter must be a mapping")
    missing = sorted(FRONT_MATTER_FIELDS - set(raw))
    unexpected = sorted(set(raw) - FRONT_MATTER_FIELDS)
    if missing:
        raise ReportContentError(f"{path} front matter is missing: {', '.join(missing)}")
    if unexpected:
        raise ReportContentError(f"{path} front matter has unsupported fields: {', '.join(unexpected)}")
    raw_date = raw.get("date")
    if isinstance(raw_date, date):
        parsed_date = raw_date
    elif isinstance(raw_date, str):
        try:
            parsed_date = date.fromisoformat(raw_date)
        except ValueError as exc:
            raise ReportContentError("report front matter date must be YYYY-MM-DD") from exc
    else:
        raise ReportContentError("report front matter date must be YYYY-MM-DD")
    raw_tags = raw["tags"]
    if not isinstance(raw_tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in raw_tags):
        raise ReportContentError("report front matter tags must be a list of text")
    if not isinstance(raw["featured"], bool):
        raise ReportContentError("report front matter featured must be true or false")
    return (
        ReportFrontMatter(
            title=_non_empty_text(raw.get("title"), "title"),
            date=parsed_date,
            summary=_non_empty_text(raw.get("summary"), "summary"),
            tags=tuple(tag.strip() for tag in raw_tags),
            featured=raw["featured"],
        ),
        text[marker + 5 :],
    )


def _markdown(*, allow_html: bool = False) -> MarkdownIt:
    return MarkdownIt(
        "commonmark",
        {"html": allow_html, "linkify": False, "typographer": False},
    ).enable("table")


def _inline_text(token: Token) -> str:
    if not token.children:
        return token.content.strip()
    return "".join(child.content for child in token.children if child.type in {"text", "code_inline"}).strip()


def _image_tokens(tokens: list[Token]) -> list[Token]:
    result: list[Token] = []
    for token in tokens:
        if token.type == "inline" and token.children:
            result.extend(child for child in token.children if child.type == "image")
    return result


def _validate_structure(path: Path, tokens: list[Token]) -> None:
    headings: list[tuple[int, str]] = []
    for index, token in enumerate(tokens):
        has_inline_html = token.children and any(child.type == "html_inline" for child in token.children)
        if token.type in {"html_block", "html_inline"} or has_inline_html:
            raise ReportContentError(f"{path} raw HTML is not allowed")
        if token.type == "heading_open":
            level = int(token.tag[1:])
            title = _inline_text(tokens[index + 1])
            headings.append((level, title))
    if any(level == 1 for level, _ in headings):
        raise ReportContentError(f"{path} must not contain an H1; the template renders the report title")
    h2_titles = tuple(title for level, title in headings if level == 2)
    allowed = (REQUIRED_SECTIONS, REQUIRED_SECTIONS + (OPTIONAL_SECTION,))
    if h2_titles not in allowed:
        expected = " -> ".join(REQUIRED_SECTIONS) + f" [-> {OPTIONAL_SECTION}]"
        raise ReportContentError(f"{path} H2 sections must be exactly: {expected}")
    for level, title in headings:
        if level > 3:
            raise ReportContentError(f"{path} heading {title!r} must use H2 or H3")


def _validate_link(token: Token, path: Path) -> None:
    href = token.attrGet("href") or ""
    parsed = urlparse(href)
    if parsed.scheme and parsed.scheme not in {"http", "https", "mailto"}:
        raise ReportContentError(f"{path} contains unsupported link scheme: {href}")
    if parsed.hostname in {"localhost", "127.0.0.1"}:
        raise ReportContentError(f"{path} contains a local-service link: {href}")


def _resolve_image(report_path: Path, token: Token) -> Path:
    source = token.attrGet("src") or ""
    alt = token.content.strip()
    if not alt:
        raise ReportContentError(f"{report_path} image {source!r} must have non-empty alt text")
    parsed = urlparse(source)
    if parsed.scheme or parsed.netloc or source.startswith(("/", "data:")):
        raise ReportContentError(f"{report_path} image must be a local relative file: {source}")
    pure = PurePosixPath(parsed.path)
    if ".." in pure.parts or not pure.parts or pure.parts[0] != "images":
        raise ReportContentError(f"{report_path} image must stay below its images directory: {source}")
    candidate = report_path.parent.joinpath(*pure.parts).resolve()
    image_root = (report_path.parent / "images").resolve()
    if candidate.parent != image_root and image_root not in candidate.parents:
        raise ReportContentError(f"{report_path} image escapes its bundle: {source}")
    if candidate.suffix.lower() not in ALLOWED_IMAGE_SUFFIXES:
        raise ReportContentError(f"{report_path} image has unsupported format: {source}")
    if not candidate.is_file():
        raise ReportContentError(f"{report_path} image is missing: {source}")
    try:
        with Image.open(candidate) as image:
            image.verify()
            expected = {".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG", ".webp": "WEBP"}[candidate.suffix.lower()]
            if image.format != expected:
                raise ReportContentError(
                    f"{report_path} image extension disagrees with decoded format: {source}"
                )
    except (OSError, UnidentifiedImageError) as exc:
        raise ReportContentError(f"{report_path} image cannot be decoded: {source}") from exc
    return candidate


def _bundle_hash(report_path: Path, assets: tuple[Path, ...]) -> str:
    digest = sha256()
    for path in (report_path, *assets):
        relative = path.relative_to(report_path.parent).as_posix()
        content_hash = sha256(path.read_bytes()).hexdigest()
        digest.update(relative.encode("utf-8") + b"\0" + content_hash.encode("ascii") + b"\n")
    return digest.hexdigest()


def load_report_source(path: Path) -> ReportSource:
    """Load and validate one immutable Markdown report bundle."""
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ReportContentError(f"cannot read Markdown report {path}: {exc}") from exc
    for forbidden in FORBIDDEN_SOURCE_TEXT:
        if forbidden in text:
            raise ReportContentError(f"{path} contains forbidden token {forbidden!r}")
    if HOME_PATH_RE.search(text):
        raise ReportContentError(f"{path} contains a home-directory path")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            raise ReportContentError(f"{path} contains a credential-like value")
    front_matter, body = _parse_front_matter(path, text)
    # Parse with HTML recognition enabled so raw tags cannot be silently treated
    # as ordinary text and slip past the authoring contract.
    tokens = _markdown(allow_html=True).parse(body)
    _validate_structure(path, tokens)
    for token in tokens:
        if token.type == "inline" and token.children:
            for child in token.children:
                if child.type == "link_open":
                    _validate_link(child, path)
    # Require a real image or a parsed Markdown table without skipping image validation.
    assets = tuple(sorted({_resolve_image(path, token) for token in _image_tokens(tokens)}))
    has_table = any(token.type == "table_open" for token in tokens)
    if not assets and not has_table:
        raise ReportContentError(f"{path} must contain at least one raster report image or Markdown table")
    image_root = path.parent / "images"
    actual_assets = tuple(
        sorted(
            candidate.resolve()
            for candidate in image_root.rglob("*")
            if candidate.is_file() and not candidate.name.startswith(".")
        )
    ) if image_root.is_dir() else ()
    unreferenced = sorted(set(actual_assets) - set(assets))
    if unreferenced:
        names = ", ".join(item.relative_to(path.parent).as_posix() for item in unreferenced[:5])
        raise ReportContentError(f"{path} has unreferenced image assets: {names}")
    size_bytes = len(data) + sum(asset.stat().st_size for asset in assets)
    if size_bytes > MAX_REPORT_BYTES:
        raise ReportContentError(f"{path} bundle exceeds the 25 MiB publication limit")
    return ReportSource(
        path=path,
        front_matter=front_matter,
        body=body,
        referenced_assets=assets,
        bundle_sha256=_bundle_hash(path, assets),
    )


def _slugify(value: str, counts: dict[str, int]) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip().lower()
    base = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", normalized, flags=re.UNICODE).strip("-") or "section"
    counts[base] = counts.get(base, 0) + 1
    return base if counts[base] == 1 else f"{base}-{counts[base]}"


def _is_image_paragraph(tokens: list[Token], index: int) -> bool:
    if index + 2 >= len(tokens) or tokens[index].type != "paragraph_open":
        return False
    inline = tokens[index + 1]
    return (
        inline.type == "inline"
        and bool(inline.children)
        and len(inline.children or []) == 1
        and (inline.children or [])[0].type == "image"
        and tokens[index + 2].type == "paragraph_close"
    )


def _prepare_tokens(tokens: list[Token]) -> tuple[list[Token], tuple[TocItem, ...]]:
    toc: list[TocItem] = []
    counts: dict[str, int] = {}
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            title = _inline_text(tokens[index + 1])
            anchor = _slugify(title, counts)
            token.attrSet("id", anchor)
            level = int(token.tag[1:])
            toc.append(TocItem(level=level, title=title, anchor=anchor))
    prepared: list[Token] = []
    index = 0
    while index < len(tokens):
        if not _is_image_paragraph(tokens, index):
            prepared.append(tokens[index])
            index += 1
            continue
        tokens[index].meta["image_only"] = True
        tokens[index + 2].meta["image_only"] = True
        prepared.extend(tokens[index : index + 3])
        index += 3
    return prepared, tuple(toc)


def render_report_source(source: ReportSource) -> RenderedReport:
    """Render a validated source to self-contained report body HTML."""
    markdown = _markdown()
    tokens, toc = _prepare_tokens(markdown.parse(source.body))
    environment: dict[str, object] = {"figure_index": 0, "table_index": 0}

    def render_image(tokens: list[Token], index: int, _options: dict[str, object], env: dict[str, object]) -> str:
        token = tokens[index]
        image_path = _resolve_image(source.path, token)
        mime = ALLOWED_IMAGE_SUFFIXES[image_path.suffix.lower()]
        encoded = b64encode(image_path.read_bytes()).decode("ascii")
        env["figure_index"] = int(env["figure_index"]) + 1
        caption = (token.attrGet("title") or token.content).strip()
        alt = token.content.strip()
        return (
            '<figure class="report-figure">'
            f'<img src="data:{mime};base64,{encoded}" alt="{escape(alt, quote=True)}" loading="lazy">'
            f'<figcaption>图 {env["figure_index"]} · {escape(caption)}</figcaption>'
            "</figure>"
        )

    def paragraph_open(tokens: list[Token], index: int, *_args: object) -> str:
        return "" if tokens[index].meta.get("image_only") else "<p>"

    def paragraph_close(tokens: list[Token], index: int, *_args: object) -> str:
        return "" if tokens[index].meta.get("image_only") else "</p>\n"

    def table_open(
        _tokens: list[Token],
        _index: int,
        _options: dict[str, object],
        env: dict[str, object],
    ) -> str:
        env["table_index"] = int(env["table_index"]) + 1
        return (
            '<div class="table-scroll">'
            f'<div class="table-caption">表 {env["table_index"]}</div>'
            "<table>\n"
        )

    markdown.renderer.rules["image"] = render_image
    markdown.renderer.rules["paragraph_open"] = paragraph_open
    markdown.renderer.rules["paragraph_close"] = paragraph_close
    markdown.renderer.rules["table_open"] = table_open
    markdown.renderer.rules["table_close"] = lambda *_args: "</table></div>\n"
    body_html = markdown.renderer.render(tokens, markdown.options, environment)
    return RenderedReport(
        body_html=body_html,
        toc=toc,
        figure_count=int(environment["figure_index"]),
    )
