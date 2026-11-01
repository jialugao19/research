from __future__ import annotations

import base64
import shutil
from pathlib import Path
from typing import Any

from jinja2 import Environment
from markupsafe import Markup

from research_site.build_output import write_text
from research_site.catalog import Catalog
from research_site.report_content import load_report_source, render_report_source
from research_site.styles import site_stylesheet


def _inline_report_stylesheet(site_root: Path) -> str:
    """Embed local fonts so generated report HTML remains a single-file artifact."""
    stylesheet = site_stylesheet(site_root)
    font_root = site_root / "assets" / "fonts"
    for font_path in sorted(font_root.glob("*.woff2")):
        reference = f'url("fonts/{font_path.name}")'
        if reference not in stylesheet:
            continue
        encoded = base64.b64encode(font_path.read_bytes()).decode("ascii")
        stylesheet = stylesheet.replace(reference, f'url("data:font/woff2;base64,{encoded}")')
    return stylesheet


def render_report_pages(
    catalog: Catalog,
    environment: Environment,
    site_root: Path,
    output_root: Path,
    common: dict[str, Any],
) -> None:
    shutil.copytree(site_root / "assets", output_root / "assets", dirs_exist_ok=True)
    # Copy only approved immutable legacy bytes, preserving every published route.
    (output_root / "assets" / "site.css").write_text(site_stylesheet(site_root), encoding="utf-8")
    for report in catalog.reports:
        if report.is_markdown:
            continue
        destination = output_root / report.route / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(site_root / "public" / report.route / "index.html", destination)
    report_template = environment.get_template("report.html")
    inline_css = _inline_report_stylesheet(site_root)
    inline_js = (site_root / "assets" / "site.js").read_text(encoding="utf-8")
    for report in catalog.reports:
        if not report.is_markdown:
            continue
        source = load_report_source(site_root / "content" / str(report.content_file))
        rendered = render_report_source(source)
        predecessor = catalog.report_by_id.get(report.revision_of) if report.revision_of else None
        report_html = report_template.render(
            **common,
            report=report,
            project=catalog.project_by_id[report.project],
            predecessor=predecessor,
            body_html=Markup(rendered.body_html),
            toc=rendered.toc,
            inline_css=Markup(inline_css),
            inline_js=Markup(inline_js),
            root_url="../../../",
        )
        write_text(output_root / report.route / "index.html", report_html)
