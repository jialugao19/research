from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from .build import normalize_base_url
from .catalog import Catalog, CatalogError
from .publication import (
    FORBIDDEN_PUBLIC_BYTES,
    validate_public_reports,
    validate_rendered_markdown_report,
)


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"a", "link"} and values.get("href"):
            self.links.append(values["href"] or "")
        if tag in {"script", "img"} and values.get("src"):
            self.links.append(values["src"] or "")


def _target_for_link(link: str, source: Path, output_root: Path, base_url: str) -> Path | None:
    if not link or link.startswith(("#", "mailto:", "data:", "javascript:")):
        return None
    parsed = urlparse(link)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if path.startswith(base_url):
        target = output_root / path.removeprefix(base_url)
    elif path.startswith("/"):
        return None
    else:
        target = source.parent / path
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def validate_built_site(catalog: Catalog, site_root: Path, output_root: Path, base_url: str) -> None:
    """Validate public copies, expected routes, local links, and path redaction."""
    base_url = normalize_base_url(base_url)
    validate_public_reports(catalog, site_root / "public" / "reports")
    expected = [
        output_root / "index.html",
        output_root / "reports" / "index.html",
        output_root / "catalog.json",
        output_root / "knowledge.json",
        output_root / "knowledge" / "index.html",
    ]
    expected.extend(output_root / "projects" / project.id / "index.html" for project in catalog.research_projects)
    expected.extend(
        output_root / "projects" / project.id / track.id / "index.html"
        for project in catalog.research_projects
        for track in project.tracks
    )
    expected.extend(
        output_root / "projects" / project.id / subproject.id / "index.html"
        for project in catalog.research_projects
        for subproject in project.subprojects
    )
    expected.extend(output_root / report.route / "index.html" for report in catalog.reports)
    if catalog.knowledge is None:
        raise CatalogError("catalog is missing knowledge data")
    expected.extend(output_root / domain.route / "index.html" for domain in catalog.knowledge.ontology_domains)
    expected.extend(
        output_root / topic.route / "index.html"
        for domain in catalog.knowledge.ontology_domains
        for topic in domain.topics
    )
    expected.extend(output_root / node.route / "index.html" for node in catalog.knowledge.nodes)
    forbidden_routes = [
        output_root / "knowledge" / "deep-ml" / "index.html",
        output_root / "knowledge" / "quant" / "index.html",
        output_root / "knowledge" / "concepts" / "index.html",
        output_root / "knowledge" / "articles" / "index.html",
        output_root / "knowledge" / "paths" / "index.html",
        output_root / "knowledge" / "chapters" / "index.html",
        output_root / "projects" / "deep-ml" / "index.html",
        output_root / "projects" / "quant-knowledge" / "index.html",
    ]
    unexpected = [path for path in forbidden_routes if path.exists()]
    if unexpected:
        raise CatalogError("obsolete knowledge routes were built: " + ", ".join(str(path) for path in unexpected[:5]))
    missing = [path for path in expected if not path.is_file()]
    if missing:
        raise CatalogError("missing built site files: " + ", ".join(str(path) for path in missing[:5]))

    for report in catalog.reports:
        if report.is_markdown:
            validate_rendered_markdown_report(report, (output_root / report.route / "index.html").read_bytes())

    for data_name in ("catalog.json", "knowledge.json"):
        public_data = (output_root / data_name).read_bytes()
        for forbidden in FORBIDDEN_PUBLIC_BYTES:
            if forbidden in public_data:
                raise CatalogError(f"{data_name} contains forbidden public token {forbidden!r}")

    link_errors: list[str] = []
    for html_path in output_root.rglob("*.html"):
        data = html_path.read_bytes()
        for forbidden in FORBIDDEN_PUBLIC_BYTES:
            if forbidden in data:
                raise CatalogError(f"{html_path} contains forbidden public token {forbidden!r}")
        relative_parts = html_path.relative_to(output_root).parts
        report_id = relative_parts[2] if len(relative_parts) == 4 and relative_parts[0] == "reports" else None
        report = catalog.report_by_id.get(report_id) if report_id else None
        if report is not None and not report.is_markdown:
            continue
        parser = _LinkParser()
        parser.feed(data.decode("utf-8", errors="ignore"))
        for link in parser.links:
            target = _target_for_link(link, html_path, output_root, base_url)
            if target is not None and not target.exists():
                link_errors.append(f"{html_path.relative_to(output_root)} -> {link}")
    if link_errors:
        raise CatalogError("broken local links: " + "; ".join(link_errors[:10]))
