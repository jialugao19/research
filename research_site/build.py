from __future__ import annotations

import base64
import json
import math
import shutil
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup

from .catalog import (
    Catalog,
    CatalogError,
    FeaturedChart,
    Metric,
    Project,
    Report,
    Study,
    Subproject,
)
from .knowledge import KnowledgeCatalog, knowledge_payload, render_knowledge_node_markdown
from .report_content import load_report_source, render_report_source

def normalize_base_url(value: str) -> str:
    stripped = value.strip("/")
    return "/" if not stripped else f"/{stripped}/"


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _inline_report_stylesheet(site_root: Path) -> str:
    """Embed local fonts so generated report HTML remains a single-file artifact."""
    stylesheet = (site_root / "assets" / "site.css").read_text(encoding="utf-8")
    font_root = site_root / "assets" / "fonts"
    for font_path in sorted(font_root.glob("*.woff2")):
        reference = f'url("fonts/{font_path.name}")'
        if reference not in stylesheet:
            continue
        encoded = base64.b64encode(font_path.read_bytes()).decode("ascii")
        stylesheet = stylesheet.replace(reference, f'url("data:font/woff2;base64,{encoded}")')
    return stylesheet


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


def _project_url(project: Project, base_url: str) -> str:
    if project.section == "knowledge":
        return f"{base_url}knowledge/"
    return f"{base_url}projects/{project.id}/"


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


def _related_concept_rows(
    knowledge: KnowledgeCatalog,
    node_id: str,
    source_groups: tuple[tuple[str, ...], ...],
) -> tuple[tuple[dict[str, str], ...], ...]:
    groups = source_groups
    if not groups:
        groups = tuple(
            tuple(item.title for item in items)
            for items in (
                knowledge.prerequisite_nodes_for(node_id),
                knowledge.related_nodes_for(node_id),
                knowledge.next_nodes_for(node_id),
            )
            if items
        )

    rows: list[tuple[dict[str, str], ...]] = []
    for group in groups[:3]:
        cards: list[dict[str, str]] = []
        for title in group:
            target = knowledge.node_for_title(title)
            if target is not None and target.id == node_id:
                continue
            cards.append({"title": title, "route": target.route if target is not None else ""})
        if cards:
            rows.append(tuple(cards))
    return tuple(rows)


def _select_project_evidence(studies: list[Study]) -> Study | None:
    """Choose the newest metric-bearing featured study, then the newest available evidence."""
    metric_studies = [study for study in studies if study.metrics]
    featured = [study for study in metric_studies if study.featured]
    if featured:
        return featured[0]
    if metric_studies:
        return metric_studies[0]
    return studies[0] if studies else None


def _required_metric(catalog: Catalog, study_id: str, metric_id: str) -> Metric:
    study = catalog.study_by_id.get(study_id)
    if study is None:
        raise CatalogError(f"homepage references unknown study {study_id}")
    metric = next((item for item in study.metrics if item.id == metric_id), None)
    if metric is None:
        raise CatalogError(f"homepage references unknown metric {study_id}/{metric_id}")
    return metric


def _compact_number(value: int | float, decimals: int) -> str:
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.{decimals}f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.{decimals}f}K"
    return f"{value:,.0f}"


def _homepage_metrics(catalog: Catalog) -> list[dict[str, str]]:
    if catalog.homepage is None:
        raise CatalogError("catalog is missing homepage highlights")
    rendered: list[dict[str, str]] = []
    for spec in catalog.homepage.metrics:
        if spec.display_value is not None:
            value = spec.display_value
        else:
            if spec.study is None or spec.metric is None:
                raise CatalogError(f"homepage metric {spec.id} is missing its metric reference")
            metric = _required_metric(catalog, spec.study, spec.metric)
            if spec.display_format == "compact-1":
                value = _compact_number(metric.value, 1)
            elif spec.display_format == "compact-2":
                value = _compact_number(metric.value, 2)
            else:
                value = metric.display_value
        rendered.append(
            {
                "id": spec.id,
                "value": value,
                "label": spec.label,
                "category": spec.category,
                "scope": spec.scope,
            }
        )
    return rendered


def _featured_chart_view(chart: FeaturedChart) -> dict[str, object]:
    """Map audited chart values into deterministic responsive SVG geometry."""
    width = 820.0
    height = 420.0
    left = 64.0
    right = 126.0
    top = 42.0
    bottom = 58.0
    plot_width = width - left - right
    plot_height = height - top - bottom

    slots = [0]
    for previous, current in zip(chart.bins, chart.bins[1:]):
        slots.append(slots[-1] + (2 if current - previous > 1 else 1))
    max_slot = max(slots) or 1
    x_positions = [left + plot_width * slot / max_slot for slot in slots]

    max_abs = max(abs(value) for series in chart.series for value in series.values)
    extent = max(5, int(math.ceil(max_abs / 5.0) * 5))
    y_min = -extent
    y_max = extent

    def y_position(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * plot_height

    y_ticks = []
    for value in range(y_min, y_max + 1, 5):
        y_ticks.append({"value": value, "y": round(y_position(value), 1)})
    x_ticks = [
        {"bin": bin_value, "x": round(x, 1)}
        for bin_value, x in zip(chart.bins, x_positions)
    ]
    gap_after = next(
        (
            index
            for index, (previous, current) in enumerate(zip(chart.bins, chart.bins[1:]))
            if current - previous > 1
        ),
        None,
    )
    axis_break_x = None
    if gap_after is not None:
        axis_break_x = round((x_positions[gap_after] + x_positions[gap_after + 1]) / 2, 1)

    rendered_series: list[dict[str, object]] = []
    for series in chart.series:
        points = [
            {
                "bin": bin_value,
                "value": value,
                "x": round(x, 1),
                "y": round(y_position(value), 1),
            }
            for bin_value, value, x in zip(chart.bins, series.values, x_positions)
        ]
        segments: list[list[dict[str, float | int]]] = [[]]
        for index, point in enumerate(points):
            if index and chart.bins[index] - chart.bins[index - 1] > 1:
                segments.append([])
            segments[-1].append(point)
        paths = [
            " ".join(
                ("M" if index == 0 else "L") + f" {point['x']} {point['y']}"
                for index, point in enumerate(segment)
            )
            for segment in segments
        ]
        rendered_series.append(
            {
                "id": series.id,
                "label": series.label,
                "values": series.values,
                "points": points,
                "paths": paths,
            }
        )
    return {
        "width": int(width),
        "height": int(height),
        "plot_left": left,
        "plot_right": width - right,
        "plot_top": top,
        "plot_bottom": height - bottom,
        "zero_y": round(y_position(0), 1),
        "x_ticks": x_ticks,
        "y_ticks": y_ticks,
        "axis_break_x": axis_break_x,
        "series": rendered_series,
    }


def _rejected_idea_views(catalog: Catalog) -> list[dict[str, object]]:
    if catalog.homepage is None:
        raise CatalogError("catalog is missing homepage highlights")
    views: list[dict[str, object]] = []
    for idea in catalog.homepage.rejected_ideas:
        study = catalog.study_by_id[idea.study]
        metric_by_id = {metric.id: metric for metric in study.metrics}
        views.append(
            {
                "title": idea.title,
                "state": idea.state,
                "reason": idea.reason,
                "study": study,
                "metrics": tuple(metric_by_id[metric_id] for metric_id in idea.metric_ids),
            }
        )
    return views


def _featured_metrics(report: Report | None, study: Study | None) -> tuple[Metric, ...]:
    if study is None:
        return ()
    preferred_by_report = {
        "0802-stock1s-gru384-v2": (
            "test-pooled-ic",
            "test-rank-ic",
            "evaluation-rows",
            "net-sharpe",
        )
    }
    preferred = preferred_by_report.get(report.id if report else "", ())
    by_id = {metric.id: metric for metric in study.metrics}
    selected = tuple(by_id[metric_id] for metric_id in preferred if metric_id in by_id)
    return selected or study.metrics[:4]


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
    for project in catalog.research_projects:
        category_projects[project.category].append(project)
    reports_by_project = {project.id: catalog.reports_for_project(project.id) for project in catalog.projects}
    studies_by_project = {project.id: catalog.studies_for_project(project.id) for project in catalog.projects}
    project_evidence = {
        project.id: _select_project_evidence(studies_by_project[project.id])
        for project in catalog.research_projects
    }
    latest_project_reports = [
        project_reports[0]
        for project in catalog.research_projects
        if (project_reports := reports_by_project[project.id])
    ]
    featured_report = catalog.featured_report
    if catalog.homepage is None:
        raise CatalogError("catalog is missing homepage highlights")
    featured_study = catalog.study_by_id[catalog.homepage.featured.study]
    project_latest = {
        project.id: (studies_by_project[project.id][0] if studies_by_project[project.id] else None)
        for project in catalog.projects
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

    index = environment.get_template("index.html").render(
        **common,
        active_project=None,
        active_report=None,
        category_projects=category_projects,
        latest_project_reports=latest_project_reports,
        reports_by_project=reports_by_project,
        studies_by_project=studies_by_project,
        project_evidence=project_evidence,
        project_latest=project_latest,
        homepage_metrics=_homepage_metrics(catalog),
        homepage=catalog.homepage,
        featured_report=featured_report,
        featured_project=(
            catalog.project_by_id[featured_report.project] if featured_report else None
        ),
        featured_study=featured_study,
        featured_metrics=_featured_metrics(featured_report, featured_study),
        featured_chart=_featured_chart_view(catalog.homepage.featured.chart),
        rejected_ideas=_rejected_idea_views(catalog),
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
    for project in catalog.research_projects:
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

    if catalog.knowledge is None:
        raise CatalogError("catalog is missing the knowledge graph snapshot")
    knowledge = catalog.knowledge
    knowledge_home = environment.get_template("knowledge.html").render(
        **common,
        active_project=None,
        active_report=None,
        active_domain=None,
        active_topic=None,
        active_subtopic=None,
        nav_section="knowledge",
    )
    _write(output_root / "knowledge" / "index.html", knowledge_home)
    domain_template = environment.get_template("knowledge_domain.html")
    topic_template = environment.get_template("knowledge_topic.html")
    node_template = environment.get_template("knowledge_node.html")
    for domain in knowledge.ontology_domains:
        domain_page = domain_template.render(
            **common,
            active_project=None,
            active_report=None,
            active_domain=domain.id,
            active_topic=None,
            active_subtopic=None,
            nav_section="knowledge",
            domain=domain,
            nodes=knowledge.nodes_for_domain(domain.id),
            research_links=knowledge.research_links_for(domain.id),
        )
        _write(output_root / domain.route / "index.html", domain_page)
        for topic in domain.topics:
            topic_nodes = knowledge.nodes_for_topic(domain.id, topic.id)
            learning_path = (
                knowledge.path_by_id.get("deep-learning-engineer")
                if domain.id == "machine-intelligence" and topic.id == "deep-learning"
                else None
            )
            deep_learning_chapters = (
                tuple(
                    chapter
                    for chapter in knowledge.chapters
                    if chapter.section_id == "06-deep-learning" and chapter.part_title
                )
                if learning_path is not None
                else ()
            )
            chapter_parts = tuple(
                sorted(
                    {
                        chapter.part_title: sum(
                            1 for item in deep_learning_chapters if item.part_title == chapter.part_title
                        )
                        for chapter in deep_learning_chapters
                    }.items()
                )
            )
            topic_page = topic_template.render(
                **common,
                active_project=None,
                active_report=None,
                active_domain=domain.id,
                active_topic=topic.id,
                active_subtopic=None,
                nav_section="knowledge",
                domain=domain,
                topic=topic,
                nodes=topic_nodes,
                learning_path=learning_path,
                chapter_parts=chapter_parts,
                research_links=knowledge.research_links_for(domain.id, topic.id),
            )
            _write(output_root / topic.route / "index.html", topic_page)
    for node in knowledge.nodes:
        rendered = render_knowledge_node_markdown(node)
        node_page = node_template.render(
            **common,
            active_project=None,
            active_report=None,
            active_domain=node.domain_id,
            active_topic=node.topic_id,
            active_subtopic=node.subtopic_id or None,
            nav_section="knowledge",
            node=node,
            next_page=knowledge.next_page_for(node.id),
            related_rows=_related_concept_rows(knowledge, node.id, rendered.related_groups),
            research_links=knowledge.research_links_for(node.domain_id, node.topic_id),
            body_html=Markup(rendered.html),
            toc=rendered.toc,
        )
        _write(output_root / node.route / "index.html", node_page)

    shutil.copytree(site_root / "assets", output_root / "assets", dirs_exist_ok=True)
    shutil.copytree(site_root / "public" / "reports", output_root / "reports", dirs_exist_ok=True)
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
                "section": project.section,
                "status": project.status,
                "url": _project_url(project, base_url),
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
    _write(output_root / "knowledge.json", json.dumps(knowledge_payload(knowledge, base_url), ensure_ascii=False, indent=2) + "\n")
