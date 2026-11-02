from __future__ import annotations

import json
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

from research_site.build import normalize_base_url
from research_site.catalog import Catalog, CatalogError
from research_site.publication import (
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
        if tag in {"img", "source"} and values.get("srcset"):
            self.links.extend(candidate.strip().split()[0] for candidate in values["srcset"].split(","))


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
    expected.extend(
        output_root / "projects" / project.id / "index.html"
        for project in (*catalog.research_projects, *catalog.infrastructure_projects)
    )
    expected.extend(
        output_root / "projects" / project.id / stage.id / "index.html"
        for project in catalog.research_projects
        for stage in catalog.research_stages
    )
    expected.extend(
        output_root / "projects" / project.id / redirect.id / "index.html"
        for project in catalog.research_projects
        for redirect in project.legacy_topic_redirects
    )
    expected.extend(output_root / report.route / "index.html" for report in catalog.reports)
    expected.extend(output_root / e.route / "index.html" for e in catalog.experiments)
    expected.extend(output_root / study.route / "index.html" for study in catalog.studies)
    expected.extend(output_root / name / "index.html" for name in ("studies", "experiments"))
    expected.append(output_root / "research-images.json")
    expected.extend(
        (
            output_root / "projects" / "prediction-nn" / "index.html",
            output_root / "projects" / "prediction-nn" / "one-minute" / "index.html",
            output_root / "projects" / "prediction-nn" / "one-second" / "index.html",
        )
    )
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

    # Legacy pages must remain byte-identical to their committed public copies.
    for report in catalog.reports:
        if not report.is_markdown:
            original = (site_root / "public" / report.route / "index.html").read_bytes()
            if (output_root / report.route / "index.html").read_bytes() != original:
                raise CatalogError(f"legacy published bytes changed for {report.id}")
        if report.is_markdown:
            validate_rendered_markdown_report(report, (output_root / report.route / "index.html").read_bytes())

    for data_name in ("catalog.json", "knowledge.json"):
        public_data = (output_root / data_name).read_bytes()
        for forbidden in FORBIDDEN_PUBLIC_BYTES:
            if forbidden in public_data:
                raise CatalogError(f"{data_name} contains forbidden public token {forbidden!r}")

    # Validate original-image hashes and every responsive rendition.
    images = json.loads((output_root / "research-images.json").read_text())
    if set(images) != {e.id for e in catalog.experiments}:
        raise CatalogError("research image manifest does not cover all experiments")
    for eid, figures in images.items():
        if len(figures) != len(catalog.experiment_by_id[eid].figures):
            raise CatalogError(f"missing research figures for {eid}")
        for figure in figures:
            original = output_root / figure["original"]
            if sha256(original.read_bytes()).hexdigest() != figure["sha256"]:
                raise CatalogError(f"research figure checksum changed for {eid}")
            for rendition in figure["renditions"]:
                if not (output_root / rendition["path"]).is_file():
                    raise CatalogError(f"missing responsive image for {eid}")

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
