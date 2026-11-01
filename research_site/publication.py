from __future__ import annotations

import re
from dataclasses import dataclass
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path

from research_site.catalog import Catalog, CatalogError, Report

MAX_REPORT_BYTES = 25 * 1024 * 1024
FORBIDDEN_PUBLIC_BYTES = (
    b"/data-cache/",
    b"file://",
    b"http://localhost",
    b"https://localhost",
    b"http://127.0.0.1",
    b"https://127.0.0.1",
)
SANITIZE_REPLACEMENTS = (
    (b"/data-cache/", b"[artifact-root]/"),
    (b"http://localhost", b"[local-service]"),
    (b"https://localhost", b"[local-service]"),
    (b"http://127.0.0.1", b"[local-service]"),
    (b"https://127.0.0.1", b"[local-service]"),
)
SECRET_PATTERNS = (
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(rb"gh[oprsu]_[A-Za-z0-9]{30,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(rb"glpat-[A-Za-z0-9_-]{20,}"),
    re.compile(rb"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(rb"sk-[A-Za-z0-9_-]{32,}"),
    re.compile(rb"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----"),
)
HOME_PATH_RE = re.compile(rb"/home/[^/\s\"'<>]+/")
CSS_URL_RE = re.compile(r"url\(\s*([\"']?)(.*?)\1\s*\)", re.IGNORECASE | re.DOTALL)
RESOURCE_ATTRIBUTES = {
    "audio": ("src",),
    "base": ("href",),
    "embed": ("src",),
    "iframe": ("src",),
    "image": ("href", "xlink:href"),
    "img": ("src", "srcset"),
    "input": ("src",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "track": ("src",),
    "use": ("href", "xlink:href"),
    "video": ("src", "poster"),
}
RENDERING_LINK_RELS = {"icon", "manifest", "modulepreload", "prefetch", "preload", "stylesheet"}
PUBLIC_REPORT_STYLE_ID = b"research-site-document-layout"
PUBLIC_REPORT_STYLE = b"""<style id="research-site-document-layout">
:root { --research-report-accent: #2e8555; --research-report-muted: #606770; }
html { font-size: 16px; }
body { margin: 0 auto; max-width: 960px; padding: 48px 32px 80px; color: #1c1e21; background: #fff; font-family: system-ui, -apple-system, \"Segoe UI\", Roboto, Ubuntu, Cantarell, \"Noto Sans\", \"Helvetica Neue\", Arial, sans-serif; font-size: 16px; line-height: 1.65; }
body :is(h2, h3, h4, h5, h6, p, li, dt, dd, span, small, strong, a, button, input, select, label, time, summary, figcaption, th, td, pre, code) { font-size: 16px !important; line-height: 1.65; }
body h1 { margin: 0 0 24px; font-size: 3rem !important; line-height: 1.2; letter-spacing: -.025em; }
body :is(h2, h3, h4, h5, h6) { margin: 32px 0 10px; font-weight: 700; letter-spacing: 0; }
body a { color: var(--research-report-accent); }
body hr { display: none !important; }
body :is(header, footer, article, section, .card, .panel, .metric-card, .summary-card, .report-card, .callout, .divider) { border: 0 !important; border-radius: 0 !important; box-shadow: none !important; }
body :is(article, section, .card, .panel, .metric-card, .summary-card, .report-card, .callout) { background: transparent !important; }
body :is(.grid, .cards, .metric-grid, .summary-grid, .report-grid, .two-column, .two-columns) { display: block !important; }
body :is(.grid, .cards, .metric-grid, .summary-grid, .report-grid, .two-column, .two-columns) > * { width: 100% !important; max-width: none !important; margin: 0 0 24px !important; }
body table { max-width: 100%; border-collapse: collapse; }
body :is(svg, canvas, img) { max-width: 100%; }
@media (max-width: 996px) { body { padding: 32px 20px 64px; } body h1 { font-size: 2rem !important; } }
</style>"""


class _RenderingResourceScanner(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []
        self._in_style = False

    def _check_resource(self, tag: str, attribute: str, value: str | None) -> None:
        if not value:
            return
        normalized = value.strip()
        if not normalized or normalized.lower().startswith("data:") or normalized.startswith("#"):
            return
        self.errors.append(f"external rendering resource <{tag}> {attribute}={value!r}")

    def _check_css(self, tag: str, css: str | None) -> None:
        if not css:
            return
        for match in CSS_URL_RE.finditer(css):
            self._check_resource(tag, "url", match.group(2))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attribute in RESOURCE_ATTRIBUTES.get(tag, ()):
            self._check_resource(tag, attribute, values.get(attribute))
        if tag == "link":
            rels = set((values.get("rel") or "").lower().split())
            if rels & RENDERING_LINK_RELS:
                self._check_resource(tag, "href", values.get("href"))
        if tag == "meta" and (values.get("http-equiv") or "").lower() == "refresh":
            content = values.get("content") or ""
            match = re.search(r"(?:^|;)\s*url\s*=\s*(.+)", content, re.IGNORECASE)
            if match:
                self._check_resource(tag, "content", match.group(1).strip(" \t\"'"))
        self._check_css(tag, values.get("style"))
        if tag == "style":
            self._in_style = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self._check_css("style", data)


@dataclass(frozen=True)
class PublicationResult:
    report_id: str
    source_path: Path
    destination_path: Path
    source_sha256: str
    published_sha256: str
    size_bytes: int


def hash_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize_report(data: bytes) -> bytes:
    """Redact local path prefixes without changing report structure or figures."""
    data = HOME_PATH_RE.sub(b"[local-workspace]/", data)
    for source, replacement in SANITIZE_REPLACEMENTS:
        data = data.replace(source, replacement)
    return b"\n".join(line.rstrip(b" \t") for line in data.split(b"\n"))


def apply_public_report_style(data: bytes) -> bytes:
    """Inject the shared Research typography without changing the immutable archive source."""
    if PUBLIC_REPORT_STYLE_ID in data:
        return data
    lower = data.lower()
    head_end = lower.find(b"</head>")
    if head_end >= 0:
        return data[:head_end] + PUBLIC_REPORT_STYLE + b"\n" + data[head_end:]
    body_start = lower.find(b"<body")
    if body_start >= 0:
        return data[:body_start] + PUBLIC_REPORT_STYLE + b"\n" + data[body_start:]
    return PUBLIC_REPORT_STYLE + b"\n" + data


def _validate_source(report: Report, source_path: Path, data: bytes) -> None:
    if not source_path.is_file():
        raise CatalogError(f"missing source report: {source_path}")
    if len(data) > MAX_REPORT_BYTES:
        raise CatalogError(f"report {report.id} exceeds the 25 MiB publication limit")
    actual_hash = sha256(data).hexdigest()
    if actual_hash != report.source_sha256:
        raise CatalogError(
            f"report {report.id} source checksum changed: expected {report.source_sha256}, got {actual_hash}"
        )
    scanner = _RenderingResourceScanner()
    scanner.feed(data.decode("utf-8", errors="ignore"))
    if scanner.errors:
        raise CatalogError(f"report {report.id}: {scanner.errors[0]}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(data):
            raise CatalogError(f"report {report.id} contains a credential-like value")


def _validate_public_copy(report: Report, data: bytes) -> None:
    if HOME_PATH_RE.search(data):
        raise CatalogError(f"report {report.id} public copy contains a home-directory path")
    for forbidden in FORBIDDEN_PUBLIC_BYTES:
        if forbidden in data:
            raise CatalogError(f"report {report.id} public copy contains forbidden token {forbidden!r}")


def validate_rendered_markdown_report(report: Report, data: bytes) -> None:
    """Validate one generated Markdown report as a self-contained HTML document."""
    _validate_public_copy(report, data)
    scanner = _RenderingResourceScanner()
    scanner.feed(data.decode("utf-8", errors="ignore"))
    if scanner.errors:
        raise CatalogError(f"report {report.id}: {scanner.errors[0]}")
    # Apply the same image-or-table contract to generated reports.
    has_image = b"<img " in data and b"data:image/" in data
    has_table = b"<table>" in data
    if not has_image and not has_table:
        raise CatalogError(f"report {report.id} generated page has no embedded raster report images or tables")


def publish_reports(catalog: Catalog, archive_root: Path, public_root: Path) -> list[PublicationResult]:
    """Create deterministic, sanitized public copies for every manifest report."""
    results: list[PublicationResult] = []
    for report in catalog.reports:
        if report.is_markdown:
            continue
        assert report.source_file is not None and report.source_sha256 is not None
        source_path = archive_root / report.source_file
        try:
            source_data = source_path.read_bytes()
        except OSError as exc:
            raise CatalogError(f"cannot read source report {source_path}: {exc}") from exc
        _validate_source(report, source_path, source_data)
        published_data = apply_public_report_style(sanitize_report(source_data))
        _validate_public_copy(report, published_data)
        destination_path = public_root / (report.route_project or report.project) / report.id / "index.html"
        if report.published_sha256 is not None and sha256(published_data).hexdigest() != report.published_sha256:
            raise CatalogError(f"report {report.id} immutable public checksum changed; create a revision")
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        destination_path.write_bytes(published_data)
        results.append(
            PublicationResult(
                report_id=report.id,
                source_path=source_path,
                destination_path=destination_path,
                source_sha256=report.source_sha256,
                published_sha256=sha256(published_data).hexdigest(),
                size_bytes=len(published_data),
            )
        )
    return results


def validate_public_reports(catalog: Catalog, public_root: Path) -> list[PublicationResult]:
    """Validate committed public copies against the immutable source hashes contract."""
    results: list[PublicationResult] = []
    for report in catalog.reports:
        if report.is_markdown:
            continue
        assert report.source_file is not None and report.source_sha256 is not None
        destination_path = public_root / (report.route_project or report.project) / report.id / "index.html"
        try:
            data = destination_path.read_bytes()
        except OSError as exc:
            raise CatalogError(f"missing public report {destination_path}: {exc}") from exc
        _validate_public_copy(report, data)
        if report.published_sha256 is not None and sha256(data).hexdigest() != report.published_sha256:
            raise CatalogError(f"report {report.id} immutable public checksum changed")
        if PUBLIC_REPORT_STYLE_ID not in data:
            raise CatalogError(f"report {report.id} public copy is missing the Research layout style")
        results.append(
            PublicationResult(
                report_id=report.id,
                source_path=Path(report.source_file),
                destination_path=destination_path,
                source_sha256=report.source_sha256,
                published_sha256=sha256(data).hexdigest(),
                size_bytes=len(data),
            )
        )
    return results
