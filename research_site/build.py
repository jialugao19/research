from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from .catalog import Catalog, Project, Report


def normalize_base_url(value: str) -> str:
    stripped = value.strip("/")
    return "/" if not stripped else f"/{stripped}/"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _report_payload(report: Report, base_url: str) -> dict[str, object]:
    return {
        "id": report.id,
        "project": report.project,
        "subproject": report.subproject,
        "title": report.title,
        "date": report.display_date,
        "summary": report.summary,
        "tags": list(report.tags),
        "featured": report.featured,
        "url": f"{base_url}{report.route}",
    }


def build_site(
    catalog: Catalog,
    site_root: Path,
    output_root: Path,
    base_url: str,
) -> None:
    """Render all catalog pages and copy approved public static files."""
    base_url = normalize_base_url(base_url)
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)

    environment = Environment(
        loader=FileSystemLoader(site_root / "templates"),
        autoescape=select_autoescape(("html", "xml")),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    category_projects: dict[str, list[Project]] = defaultdict(list)
    for project in catalog.projects:
        category_projects[project.category].append(project)
    reports_by_project = {project.id: catalog.reports_for_project(project.id) for project in catalog.projects}
    featured_reports = sorted(
        (report for report in catalog.reports if report.featured),
        key=lambda report: (report.date, report.id),
        reverse=True,
    )
    common = {
        "base_url": base_url,
        "catalog": catalog,
        "report_count": len(catalog.reports),
        "project_count": len(catalog.projects),
    }

    index = environment.get_template("index.html").render(
        **common,
        category_projects=category_projects,
        featured_reports=featured_reports,
        reports_by_project=reports_by_project,
    )
    _write(output_root / "index.html", index)

    report_index = environment.get_template("reports.html").render(
        **common,
        reports=sorted(catalog.reports, key=lambda report: (report.date, report.id), reverse=True),
        projects=catalog.project_by_id,
    )
    _write(output_root / "reports" / "index.html", report_index)

    project_template = environment.get_template("project.html")
    subproject_template = environment.get_template("subproject.html")
    for project in catalog.projects:
        reports = reports_by_project[project.id]
        project_page = project_template.render(**common, project=project, reports=reports)
        _write(output_root / "projects" / project.id / "index.html", project_page)
        for subproject in project.subprojects:
            subproject_reports = [report for report in reports if report.subproject == subproject.id]
            subproject_page = subproject_template.render(
                **common,
                project=project,
                subproject=subproject,
                reports=subproject_reports,
            )
            _write(output_root / "projects" / project.id / subproject.id / "index.html", subproject_page)

    shutil.copytree(site_root / "assets", output_root / "assets", dirs_exist_ok=True)
    shutil.copytree(site_root / "public" / "reports", output_root / "reports", dirs_exist_ok=True)
    _write(output_root / ".nojekyll", "")
    payload = {
        "schema_version": 1,
        "base_url": base_url,
        "projects": [
            {
                "id": project.id,
                "title": project.title,
                "category": project.category,
                "status": project.status,
                "url": f"{base_url}projects/{project.id}/",
                "report_count": len(reports_by_project[project.id]),
            }
            for project in catalog.projects
        ],
        "reports": [_report_payload(report, base_url) for report in catalog.reports],
    }
    _write(output_root / "catalog.json", json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
