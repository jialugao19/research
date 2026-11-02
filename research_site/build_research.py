from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from jinja2 import Environment

from research_site.build_output import write_text
from research_site.catalog import (
    Catalog,
    CatalogError,
    FeaturedChart,
    Metric,
    Project,
    Report,
    ResearchTaxonomyNode,
    Experiment,
    taxonomy_anchor,
)


def _taxonomy_node_views(
    nodes: tuple[ResearchTaxonomyNode, ...],
    stage_id: str,
    experiments_by_path: dict[tuple[str, ...], list[Experiment]],
    parent_path: tuple[str, ...] = (),
    depth: int = 1,
) -> list[dict[str, object]]:
    views: list[dict[str, object]] = []
    for node in nodes:
        relative_path = (*parent_path, node.id)
        taxonomy_path = (stage_id, *relative_path)
        views.append(
            {
                "node": node,
                "path": taxonomy_path,
                "path_string": "/".join(taxonomy_path),
                "anchor": taxonomy_anchor(taxonomy_path),
                "depth": depth,
                "heading_level": min(depth + 1, 6),
                "experiments": experiments_by_path.get(taxonomy_path, []),
                "children": _taxonomy_node_views(
                    node.children,
                    stage_id,
                    experiments_by_path,
                    relative_path,
                    depth + 1,
                ),
            }
        )
    return views


def _stage_taxonomy_views(
    catalog: Catalog,
    project: Project,
    stage_id: str,
) -> tuple[list[dict[str, object]], list[Experiment]]:
    experiments = catalog.experiments_for_stage(project.id, stage_id)
    experiments_by_path: dict[tuple[str, ...], list[Experiment]] = {}
    for experiment in experiments:
        experiments_by_path.setdefault(experiment.taxonomy_path, []).append(experiment)
    taxonomy_stage = catalog.taxonomy_by_stage[stage_id]
    return (
        _taxonomy_node_views(taxonomy_stage.nodes, stage_id, experiments_by_path),
        experiments_by_path.get((stage_id,), []),
    )


def _stage_views(
    catalog: Catalog,
    project: Project,
    base_url: str,
    experiments: list[Experiment],
    reports: list[Report],
) -> list[dict[str, object]]:
    experiments_by_stage = {
        stage.id: [experiment for experiment in experiments if experiment.stage == stage.id]
        for stage in catalog.research_stages
    }
    reports_by_stage = {
        stage.id: [report for report in reports if report.stage == stage.id]
        for stage in catalog.research_stages
    }
    return [
        {
            "definition": definition,
            "assessment": project.stage(definition.id),
            "occupied_topics": len(
                {experiment.taxonomy_path for experiment in experiments_by_stage[definition.id] if len(experiment.taxonomy_path) > 1}
            ),
            "experiments": experiments_by_stage[definition.id],
            "reports": reports_by_stage[definition.id],
            "url": f"{base_url}projects/{project.id}/{definition.id}/",
        }
        for definition in catalog.research_stages
    ]


def _select_project_evidence(experiments: list[Experiment]) -> Experiment | None:
    metric_experiments = [experiment for experiment in experiments if experiment.metrics]
    featured = [experiment for experiment in metric_experiments if experiment.featured]
    if featured:
        return featured[0]
    if metric_experiments:
        return metric_experiments[0]
    return experiments[0] if experiments else None


def _required_metric(catalog: Catalog, experiment_id: str, metric_id: str) -> Metric:
    experiment = catalog.experiment_by_id.get(experiment_id)
    if experiment is None:
        raise CatalogError(f"homepage references unknown experiment {experiment_id}")
    metric = next((item for item in experiment.metrics if item.id == metric_id), None)
    if metric is None:
        raise CatalogError(f"homepage references unknown metric {experiment_id}/{metric_id}")
    return metric


def _compact_number(value: float, decimals: int) -> str:
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
            if spec.experiment is None or spec.metric is None:
                raise CatalogError(f"homepage metric {spec.id} is missing its metric reference")
            metric = _required_metric(catalog, spec.experiment, spec.metric)
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


def featured_chart_view(chart: FeaturedChart) -> dict[str, object]:
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

    y_ticks = [
        {"value": value, "y": round(y_position(value), 1)}
        for value in range(y_min, y_max + 1, 5)
    ]
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
            {"bin": bin_value, "value": value, "x": round(x, 1), "y": round(y_position(value), 1)}
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
            {"id": series.id, "label": series.label, "values": series.values, "points": points, "paths": paths}
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
        experiment = catalog.experiment_by_id[idea.experiment]
        metric_by_id = {metric.id: metric for metric in experiment.metrics}
        views.append(
            {
                "title": idea.title,
                "state": idea.state,
                "reason": idea.reason,
                "experiment": experiment,
                "metrics": tuple(metric_by_id[metric_id] for metric_id in idea.metric_ids),
            }
        )
    return views


def _featured_metrics(report: Report | None, experiment: Experiment | None) -> tuple[Metric, ...]:
    if experiment is None:
        return ()
    preferred_by_report = {
        "0802-stock1s-gru384-v2": ("test-pooled-ic", "test-rank-ic", "evaluation-rows", "net-sharpe")
    }
    preferred = preferred_by_report.get(report.id if report else "", ())
    by_id = {metric.id: metric for metric in experiment.metrics}
    selected = tuple(by_id[metric_id] for metric_id in preferred if metric_id in by_id)
    return selected or experiment.metrics[:4]


def render_research_pages(
    catalog: Catalog,
    environment: Environment,
    output_root: Path,
    base_url: str,
    common: dict[str, Any],
    reports_by_project: dict[str, list[Report]],
    experiments_by_project: dict[str, list[Experiment]],
) -> None:
    project_evidence = {
        project.id: _select_project_evidence(experiments_by_project[project.id])
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
    featured_experiment = catalog.experiment_by_id[catalog.homepage.featured.experiment]
    project_latest = {
        project.id: (experiments_by_project[project.id][0] if experiments_by_project[project.id] else None)
        for project in catalog.projects
    }
    index = environment.get_template("index.html").render(
        **common,
        active_project=None,
        active_report=None,
        research_projects=catalog.research_projects,
        infrastructure_projects=catalog.infrastructure_projects,
        latest_project_reports=latest_project_reports,
        reports_by_project=reports_by_project,
        experiments_by_project=experiments_by_project,
        project_evidence=project_evidence,
        project_latest=project_latest,
        homepage_metrics=_homepage_metrics(catalog),
        homepage=catalog.homepage,
        featured_report=featured_report,
        featured_project=catalog.project_by_id[featured_report.project] if featured_report else None,
        featured_experiment=featured_experiment,
        featured_metrics=_featured_metrics(featured_report, featured_experiment),
        featured_chart=featured_chart_view(catalog.homepage.featured.chart),
        rejected_ideas=_rejected_idea_views(catalog),
    )
    write_text(output_root / "index.html", index)
    report_index = environment.get_template("reports.html").render(
        **common,
        active_project=None,
        active_report=None,
        reports=sorted(catalog.current_reports, key=lambda report: (report.date, report.id), reverse=True),
        projects=catalog.project_by_id,
    )
    write_text(output_root / "reports" / "index.html", report_index)

    project_template = environment.get_template("project.html")
    stage_template = environment.get_template("stage.html")
    redirect_template = environment.get_template("redirect.html")
    linked_reports_by_stage = {
        (experiment.stage, report_id)
        for experiment in catalog.experiments
        for report_id in experiment.report_ids
    }
    for project in catalog.research_projects:
        reports = reports_by_project[project.id]
        experiments = experiments_by_project[project.id]
        featured_experiments = [experiment for experiment in experiments if experiment.featured] or experiments[:1]
        write_text(
            output_root / "projects" / project.id / "index.html",
            project_template.render(
                **common,
                active_project=project.id,
                active_report=None,
                project=project,
                reports=reports,
                experiments=experiments,
                featured_experiments=featured_experiments,
                research_studies=catalog.studies_for_project(project.id),
                stage_views=_stage_views(catalog, project, base_url, experiments, reports),
            ),
        )
        for stage_index, definition in enumerate(catalog.research_stages):
            stage_experiments = catalog.experiments_for_stage(project.id, definition.id)
            taxonomy_views, stage_root_experiments = _stage_taxonomy_views(
                catalog, project, definition.id
            )
            stage_reports = [
                report
                for report in reports
                if report.stage == definition.id
                and (definition.id, report.id) not in linked_reports_by_stage
            ]
            write_text(
                output_root / "projects" / project.id / definition.id / "index.html",
                stage_template.render(
                    **common,
                    active_project=project.id,
                    active_stage=definition.id,
                    active_report=None,
                    project=project,
                    stage=definition,
                    stage_number=stage_index + 1,
                    assessment=project.stage(definition.id),
                    taxonomy_views=taxonomy_views,
                    taxonomy_stage=catalog.taxonomy_by_stage[definition.id],
                    stage_root_experiments=stage_root_experiments,
                    reports=stage_reports,
                    experiments=stage_experiments,
                    previous_stage=catalog.research_stages[stage_index - 1] if stage_index > 0 else None,
                    next_stage=(catalog.research_stages[stage_index + 1] if stage_index + 1 < len(catalog.research_stages) else None),
                ),
            )
        for redirect in project.legacy_topic_redirects:
            target_url = (
                f"{base_url}projects/{project.id}/{redirect.stage}/#{redirect.anchor}"
            )
            write_text(
                output_root / "projects" / project.id / redirect.id / "index.html",
                redirect_template.render(target_url=target_url),
            )

    infrastructure_template = environment.get_template("infrastructure.html")
    for project in catalog.infrastructure_projects:
        experiments = experiments_by_project[project.id]
        reports = reports_by_project[project.id]
        write_text(
            output_root / "projects" / project.id / "index.html",
            infrastructure_template.render(
                **common,
                active_project=project.id,
                active_report=None,
                project=project,
                experiments=experiments,
                reports=reports,
                featured_experiments=[experiment for experiment in experiments if experiment.featured] or experiments[:1],
            ),
        )

    split_template = environment.get_template("prediction_split.html")
    write_text(
        output_root / "projects" / "prediction-nn" / "index.html",
        split_template.render(
            **common,
            active_project=None,
            active_report=None,
            minute_project=catalog.project_by_id["prediction-nn-1min"],
            second_project=catalog.project_by_id["prediction-nn-1s"],
        ),
    )
    legacy_redirects = {"one-minute": "prediction-nn-1min", "one-second": "prediction-nn-1s"}
    for new_project_id in ("prediction-nn-1min", "prediction-nn-1s"):
        for redirect in catalog.project_by_id[new_project_id].legacy_topic_redirects:
            legacy_redirects[redirect.id] = f"{new_project_id}/{redirect.stage}/#{redirect.anchor}"
    for legacy_slug, target_suffix in legacy_redirects.items():
        target_url = f"{base_url}projects/{target_suffix}"
        if "#" not in target_suffix:
            target_url += "/"
        write_text(
            output_root / "projects" / "prediction-nn" / legacy_slug / "index.html",
            redirect_template.render(target_url=target_url),
        )
