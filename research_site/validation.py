from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from .catalog import Catalog, CatalogError
from .build import normalize_base_url
from .publication import FORBIDDEN_PUBLIC_BYTES, validate_public_reports


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
    expected = [output_root / "index.html", output_root / "reports" / "index.html", output_root / "catalog.json"]
    expected.extend(output_root / "projects" / project.id / "index.html" for project in catalog.projects)
    expected.extend(
        output_root / "projects" / project.id / track.id / "index.html"
        for project in catalog.projects
        for track in project.tracks
    )
    expected.extend(
        output_root / "projects" / project.id / subproject.id / "index.html"
        for project in catalog.projects
        for subproject in project.subprojects
    )
    expected.extend(output_root / report.route / "index.html" for report in catalog.reports)
    missing = [path for path in expected if not path.is_file()]
    if missing:
        raise CatalogError("missing built site files: " + ", ".join(str(path) for path in missing[:5]))

    catalog_data = (output_root / "catalog.json").read_bytes()
    for forbidden in FORBIDDEN_PUBLIC_BYTES:
        if forbidden in catalog_data:
            raise CatalogError(f"catalog.json contains forbidden public token {forbidden!r}")

    link_errors: list[str] = []
    for html_path in output_root.rglob("*.html"):
        data = html_path.read_bytes()
        for forbidden in FORBIDDEN_PUBLIC_BYTES:
            if forbidden in data:
                raise CatalogError(f"{html_path} contains forbidden public token {forbidden!r}")
        relative_parts = html_path.relative_to(output_root).parts
        if len(relative_parts) == 4 and relative_parts[0] == "reports":
            continue
        parser = _LinkParser()
        parser.feed(data.decode("utf-8", errors="ignore"))
        for link in parser.links:
            target = _target_for_link(link, html_path, output_root, base_url)
            if target is not None and not target.exists():
                link_errors.append(f"{html_path.relative_to(output_root)} -> {link}")
    if link_errors:
        raise CatalogError("broken local links: " + "; ".join(link_errors[:10]))
