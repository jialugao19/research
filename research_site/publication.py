from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re

from .catalog import Catalog, CatalogError, Report


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
    re.compile(rb"ghp_[A-Za-z0-9]{30,}"),
    re.compile(rb"sk-[A-Za-z0-9_-]{32,}"),
)
HOME_PATH_RE = re.compile(rb"/home/[^/\s\"'<>]+/")


class _RenderingResourceScanner(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        candidates: list[tuple[str, str | None]] = []
        if tag in {"img", "script", "iframe", "source", "video", "audio"}:
            candidates.append(("src", values.get("src")))
        if tag == "link" and (values.get("rel") or "").lower() == "stylesheet":
            candidates.append(("href", values.get("href")))
        for attribute, value in candidates:
            if not value or value.startswith(("data:", "#")):
                continue
            self.errors.append(f"external rendering resource <{tag}> {attribute}={value!r}")


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


def publish_reports(catalog: Catalog, archive_root: Path, public_root: Path) -> list[PublicationResult]:
    """Create deterministic, sanitized public copies for every manifest report."""
    results: list[PublicationResult] = []
    for report in catalog.reports:
        source_path = archive_root / report.source_file
        try:
            source_data = source_path.read_bytes()
        except OSError as exc:
            raise CatalogError(f"cannot read source report {source_path}: {exc}") from exc
        _validate_source(report, source_path, source_data)
        published_data = sanitize_report(source_data)
        _validate_public_copy(report, published_data)
        destination_path = public_root / report.project / report.id / "index.html"
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
        destination_path = public_root / report.project / report.id / "index.html"
        try:
            data = destination_path.read_bytes()
        except OSError as exc:
            raise CatalogError(f"missing public report {destination_path}: {exc}") from exc
        _validate_public_copy(report, data)
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
