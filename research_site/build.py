from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from .build_knowledge import render_knowledge_pages
from .build_output import BuildResult, build_atomically, write_text
from .build_reports import render_report_pages
from .build_research import featured_chart_view as _featured_chart_view
from .build_research import render_research_pages
from .catalog import (
    Catalog,
    Project,
    Report,
    ResearchTaxonomyNode,
    Study,
    taxonomy_anchor,
)
from .knowledge import knowledge_payload

__all__ = ["_featured_chart_view", "build_site"]


def normalize_base_url(value: str) -> str:
    stripped = value.strip("/")
    return "/" if not stripped else f"/{stripped}/"


def _report_payload(report: Report, base_url: str) -> dict[str, object]:
    return {
        "id": report.id,
        "project": report.project,
        "stage": report.stage,
        "title": report.title,
        "date": report.display_date,
        "summary": report.summary,
        "tags": list(report.tags),
        "featured": report.featured,
        "format": report.format,
        "revision_of": report.revision_of,
        "url": f"{base_url}{report.route}",
    }


def _project_url(project: Project, base_url: str) -> str:
    if project.section == "knowledge":
        return f"{base_url}knowledge/"
    return f"{base_url}projects/{project.id}/"


def _study_payload(study: Study) -> dict[str, object]:
    return {
        "id": study.id,
        "project": study.project,
        "stage": study.stage,
        "taxonomy_path": study.taxonomy_path_string,
        "related_taxonomy_paths": ["/".join(path) for path in study.related_taxonomy_paths],
        "title": study.title,
        "status": study.status,
        "maturity": study.maturity,
        "updated_at": study.display_date,
        "method": study.method,
        "dataset": study.dataset,
        "decision_state": study.decision_state,
        "primary_metric": study.primary_metric_id,
        "summary": study.summary,
        "decision": study.decision,
        "metrics": [
            {
                "id": metric.id,
                "label": metric.label,
                "value": metric.value,
                "display_value": metric.display_value,
                "context": metric.context,
            }
            for metric in study.metrics
        ],
        "report_ids": list(study.report_ids),
    }


def _taxonomy_node_payload(
    node: ResearchTaxonomyNode,
    parent_path: tuple[str, ...],
) -> dict[str, object]:
    path = (*parent_path, node.id)
    return {
        "id": node.id,
        "title": node.title,
        "path": "/".join(path),
        "anchor": taxonomy_anchor(path),
        "children": [_taxonomy_node_payload(child, path) for child in node.children],
    }


def _render_site(
    catalog: Catalog,
    site_root: Path,
    output_root: Path,
    base_url: str,
) -> None:
    environment = Environment(
        loader=FileSystemLoader(site_root / "templates"),
        autoescape=select_autoescape(("html", "xml")),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.globals["taxonomy_anchor"] = taxonomy_anchor
    reports_by_project = {
        project.id: catalog.reports_for_project(project.id) for project in catalog.projects
    }
    studies_by_project = {
        project.id: catalog.studies_for_project(project.id) for project in catalog.projects
    }
    dated_items = [report.date for report in catalog.current_reports]
    dated_items.extend(study.updated_at for study in catalog.studies)
    common = {
        "base_url": base_url,
        "catalog": catalog,
        "knowledge": catalog.knowledge,
        "report_count": len(catalog.current_reports),
        "project_count": len(catalog.research_projects),
        "study_count": len(catalog.studies),
        "site_updated": max(dated_items).isoformat() if dated_items else "",
    }
    render_research_pages(
        catalog,
        environment,
        output_root,
        base_url,
        common,
        reports_by_project,
        studies_by_project,
    )
    knowledge = render_knowledge_pages(catalog, environment, output_root, base_url, common)
    render_report_pages(catalog, environment, site_root, output_root, common)
    write_text(output_root / ".nojekyll", "")
    catalog_data = {
        "schema_version": 4,
        "base_url": base_url,
        "research_taxonomy": [
            {
                "id": stage.id,
                "title": catalog.stage_by_id[stage.id].title,
                "nodes": [
                    _taxonomy_node_payload(node, (stage.id,)) for node in stage.nodes
                ],
            }
            for stage in catalog.research_taxonomy
        ],
        "projects": [
            {
                "id": project.id,
                "title": project.title,
                "category": project.category,
                "section": project.section,
                "status": project.status,
                "url": _project_url(project, base_url),
                "report_count": len(reports_by_project[project.id]),
                "study_count": len(studies_by_project[project.id]),
                "stages": [
                    {
                        "id": stage.id,
                        "title": catalog.stage_by_id[stage.id].title,
                        "state": stage.state,
                        "summary": stage.summary,
                        "url": f"{base_url}projects/{project.id}/{stage.id}/",
                    }
                    for stage in project.stages
                ],
            }
            for project in catalog.projects
        ],
        "studies": [_study_payload(study) for study in catalog.studies],
        "reports": [
            {**_report_payload(report, base_url), "is_current": report in catalog.current_reports}
            for report in catalog.reports
        ],
    }
    write_text(
        output_root / "catalog.json",
        json.dumps(catalog_data, ensure_ascii=False, indent=2) + "\n",
    )
    write_text(
        output_root / "knowledge.json",
        json.dumps(knowledge_payload(knowledge, base_url), ensure_ascii=False, indent=2) + "\n",
    )


def build_site(
    catalog: Catalog,
    site_root: Path,
    output_root: Path,
    base_url: str,
) -> BuildResult:
    """Build into staging, validate it, and atomically replace the active output."""
    normalized_base_url = normalize_base_url(base_url)
    site_root = site_root.resolve()
    output_root = output_root.resolve()

    def render(staging: Path) -> None:
        _render_site(catalog, site_root, staging, normalized_base_url)

    def validate(staging: Path) -> None:
        from .validation import validate_built_site

        validate_built_site(catalog, site_root, staging, normalized_base_url)

    return build_atomically(output_root, render, validate)
