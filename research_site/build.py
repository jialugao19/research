from __future__ import annotations

import json
import shutil
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup

from .catalog import Catalog, Project, Report, Study, Subproject
from .report_content import load_report_source, render_report_source

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
        "format": report.format,
        "revision_of": report.revision_of,
        "url": f"{base_url}{report.route}",
    }


def _study_payload(study: Study) -> dict[str, object]:
    return {
        "id": study.id,
        "project": study.project,
        "track": study.track,
        "subproject": study.subproject,
        "title": study.title,
        "status": study.status,
        "maturity": study.maturity,
        "updated_at": study.display_date,
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


def _group_subprojects(subprojects: tuple[Subproject, ...]) -> list[dict[str, object]]:
    """Preserve catalog order while collecting related experiment topics."""
    groups: list[dict[str, object]] = []
    by_title: dict[str, list[Subproject]] = {}
    for subproject in subprojects:
        if subproject.group not in by_title:
            items: list[Subproject] = []
            by_title[subproject.group] = items
            groups.append({"title": subproject.group, "subprojects": items})
        by_title[subproject.group].append(subproject)
    return groups


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
    studies_by_project = {project.id: catalog.studies_for_project(project.id) for project in catalog.projects}
    latest_project_reports = [
        project_reports[0]
        for project in catalog.projects
        if (project_reports := reports_by_project[project.id])
    ]
    featured_candidates = sorted(
        (report for report in catalog.current_reports if report.featured),
        key=lambda report: (report.date, report.id),
        reverse=True,
    )
    if not featured_candidates:
        featured_candidates = sorted(
            catalog.current_reports,
            key=lambda report: (report.date, report.id),
            reverse=True,
        )
    featured_report = featured_candidates[0] if featured_candidates else None
    featured_hero_url = None
    if featured_report and featured_report.is_markdown:
        featured_source = load_report_source(site_root / "content" / str(featured_report.content_file))
        if featured_report.hero_image:
            featured_hero_source = (
                featured_source.path.parent / featured_report.hero_image
            ).resolve()
        else:
            featured_hero_source = featured_source.referenced_assets[0]
        featured_hero_name = f"{featured_report.id}{featured_hero_source.suffix.lower()}"
        featured_hero_target = output_root / "assets" / "report-heroes" / featured_hero_name
        featured_hero_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(featured_hero_source, featured_hero_target)
        featured_hero_url = f"{base_url}assets/report-heroes/{featured_hero_name}"
    dated_items = [report.date for report in catalog.current_reports]
    dated_items.extend(study.updated_at for study in catalog.studies)
    common = {
        "base_url": base_url,
        "catalog": catalog,
        "report_count": len(catalog.current_reports),
        "project_count": len(catalog.projects),
        "study_count": len(catalog.studies),
        "site_updated": max(dated_items).isoformat() if dated_items else "",
    }

    index = environment.get_template("index.html").render(
        **common,
        active_project=None,
        active_report=None,
        category_projects=category_projects,
        latest_project_reports=latest_project_reports,
        reports_by_project=reports_by_project,
        studies_by_project=studies_by_project,
        featured_report=featured_report,
        featured_project=(
            catalog.project_by_id[featured_report.project] if featured_report else None
        ),
        featured_hero_url=featured_hero_url,
    )
    _write(output_root / "index.html", index)

    report_index = environment.get_template("reports.html").render(
        **common,
        active_project=None,
        active_report=None,
        reports=sorted(catalog.current_reports, key=lambda report: (report.date, report.id), reverse=True),
        projects=catalog.project_by_id,
    )
    _write(output_root / "reports" / "index.html", report_index)

    project_template = environment.get_template("project.html")
    track_template = environment.get_template("track.html")
    subproject_template = environment.get_template("subproject.html")
    for project in catalog.projects:
        reports = reports_by_project[project.id]
        studies = studies_by_project[project.id]
        featured_studies = [study for study in studies if study.featured] or studies[:1]
        project_page = project_template.render(
            **common,
            active_project=project.id,
            active_report=None,
            project=project,
            reports=reports,
            studies=studies,
            featured_studies=featured_studies,
        )
        _write(output_root / "projects" / project.id / "index.html", project_page)
        for track in project.tracks:
            track_studies = catalog.studies_for_track(project.id, track.id)
            track_featured_studies = [study for study in track_studies if study.featured] or track_studies[:1]
            subprojects = project.subprojects_for_track(track.id)
            subproject_ids = {subproject.id for subproject in subprojects}
            track_reports = [report for report in reports if report.subproject in subproject_ids]
            track_page = track_template.render(
                **common,
                active_project=project.id,
                active_report=None,
                project=project,
                track=track,
                subprojects=subprojects,
                subproject_groups=_group_subprojects(subprojects),
                reports=track_reports,
                studies=track_studies,
                featured_studies=track_featured_studies,
            )
            _write(output_root / "projects" / project.id / track.id / "index.html", track_page)
        for subproject in project.subprojects:
            subproject_reports = [report for report in reports if report.subproject == subproject.id]
            subproject_studies = catalog.studies_for_subproject(project.id, subproject.id)
            subproject_page = subproject_template.render(
                **common,
                active_project=project.id,
                active_report=None,
                project=project,
                subproject=subproject,
                reports=subproject_reports,
                studies=subproject_studies,
            )
            _write(output_root / "projects" / project.id / subproject.id / "index.html", subproject_page)

    shutil.copytree(site_root / "assets", output_root / "assets", dirs_exist_ok=True)
    shutil.copytree(site_root / "public" / "reports", output_root / "reports", dirs_exist_ok=True)
    report_template = environment.get_template("report.html")
    inline_css = (site_root / "assets" / "site.css").read_text(encoding="utf-8")
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
        _write(output_root / report.route / "index.html", report_html)
    _write(output_root / ".nojekyll", "")
    payload = {
        "schema_version": 2,
        "base_url": base_url,
        "projects": [
            {
                "id": project.id,
                "title": project.title,
                "category": project.category,
                "status": project.status,
                "url": f"{base_url}projects/{project.id}/",
                "report_count": len(reports_by_project[project.id]),
                "study_count": len(studies_by_project[project.id]),
                "tracks": [
                    {
                        "id": track.id,
                        "title": track.title,
                        "url": f"{base_url}projects/{project.id}/{track.id}/",
                    }
                    for track in project.tracks
                ],
            }
            for project in catalog.projects
        ],
        "studies": [_study_payload(study) for study in catalog.studies],
        "reports": [
            {
                **_report_payload(report, base_url),
                "is_current": report in catalog.current_reports,
            }
            for report in catalog.reports
        ],
    }
    _write(output_root / "catalog.json", json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
