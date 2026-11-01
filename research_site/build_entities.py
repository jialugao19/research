from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment

from research_site.build_output import write_text
from research_site.catalog import Catalog, Experiment
from research_site.research_assets import build_research_figures


def comparison_view(experiment: Experiment) -> dict[str, Any]:
    # Compare arms only inside the experiment's declared matched contract.
    labels = {metric.id: metric.label for arm in experiment.arms for metric in arm.metrics}
    return {
        "columns": list(labels.items()),
        "rows": [{"arm": arm, "metrics": {m.id: m for m in arm.metrics}} for arm in experiment.arms],
    }


def render_entity_pages(
    catalog: Catalog, environment: Environment, site_root: Path,
    output_root: Path, base_url: str, common: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    # Publish curated figures once for both experiment and question pages.
    figures = build_research_figures(catalog, site_root, output_root)
    experiment_template = environment.get_template("experiment.html")
    study_template = environment.get_template("study.html")
    for experiment in catalog.experiments:
        write_text(output_root / experiment.route / "index.html", experiment_template.render(
            **common, active_project=experiment.project, active_report=None,
            experiment=experiment, project=catalog.project_by_id[experiment.project],
            studies=catalog.studies_for_experiment(experiment.id),
            figures=figures[experiment.id], comparison=comparison_view(experiment),
        ))
    for study in catalog.studies:
        write_text(output_root / study.route / "index.html", study_template.render(
            **common, active_project=study.project_ids[0], active_report=None,
            study=study, experiments=catalog.experiments_for_study(study.id),
            figures=figures,
        ))

    # Make every experiment discoverable independently of project navigation.
    write_text(output_root / "experiments" / "index.html", environment.get_template("experiments.html").render(
        **common, active_project=None, active_report=None, experiments=catalog.experiments,
    ))
    write_text(output_root / "studies" / "index.html", environment.get_template("studies.html").render(
        **common, active_project=None, active_report=None, studies=catalog.studies,
    ))
    return figures
