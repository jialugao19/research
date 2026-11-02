from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path, PurePath
from typing import TYPE_CHECKING, Any

import yaml

from research_site.report_content import ReportContentError, load_report_source

if TYPE_CHECKING:
    from research_site.knowledge import KnowledgeCatalog

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_MATCH_METHODS = {"sha256", "central-catalog", "path-evidence", "title-and-project-intent", "manual"}
ALLOWED_EXPERIMENT_STATUSES = {"doing", "completed", "archived"}
ALLOWED_MATURITIES = {"decision-ready", "signal-only", "developmental", "diagnostic", "blocked", "archived"}
ALLOWED_METRIC_FORMATS = {"decimal", "percent", "integer", "number", "bps"}
ALLOWED_DECISION_STATES = {
    "promote",
    "retain",
    "iterate",
    "reject",
    "diagnostic",
    "blocked",
    "archived",
    "observe",
}
ALLOWED_HIGHLIGHT_STATES = {"positive", "warning", "negative"}
ALLOWED_HOMEPAGE_METRIC_CATEGORIES = {"quality", "method", "scale", "coverage"}
ALLOWED_HOMEPAGE_VALUE_FORMATS = {"raw", "compact-1", "compact-2"}
ALLOWED_PROJECT_SECTIONS = {"research", "infrastructure", "knowledge"}
ALLOWED_STAGE_STATES = {"documented", "in-progress", "gap", "not-applicable"}


class CatalogError(ValueError):
    """Raised when project or report metadata violates the public contract."""


@dataclass(frozen=True)
class Category:
    id: str
    title: str
    description: str


@dataclass(frozen=True)
class ResearchStageDefinition:
    id: str
    title: str
    short_title: str
    description: str


@dataclass(frozen=True)
class ProjectStage:
    id: str
    state: str
    summary: str


@dataclass(frozen=True)
class ResearchTaxonomyNode:
    id: str
    title: str
    children: tuple[ResearchTaxonomyNode, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ResearchTaxonomyStage:
    id: str
    nodes: tuple[ResearchTaxonomyNode, ...]


@dataclass(frozen=True)
class LegacyTopicRedirect:
    id: str
    taxonomy_path: tuple[str, ...]

    @property
    def stage(self) -> str:
        return self.taxonomy_path[0]

    @property
    def anchor(self) -> str:
        return "topic-" + "--".join(self.taxonomy_path)


@dataclass(frozen=True)
class Project:
    id: str
    title: str
    category: str
    status: str
    description: str
    objective: str
    review_summary: str
    source_refs: tuple[str, ...]
    section: str = "research"
    stages: tuple[ProjectStage, ...] = field(default_factory=tuple)
    legacy_topic_redirects: tuple[LegacyTopicRedirect, ...] = field(default_factory=tuple)
    registry_experiments: tuple[str, ...] = field(default_factory=tuple)

    def stage(self, stage_id: str) -> ProjectStage | None:
        return next((item for item in self.stages if item.id == stage_id), None)

    def legacy_topic_redirect(self, topic_id: str) -> LegacyTopicRedirect | None:
        return next((item for item in self.legacy_topic_redirects if item.id == topic_id), None)


@dataclass(frozen=True)
class Metric:
    id: str
    label: str
    value: int | float
    format: str
    decimals: int
    context: str
    unit: str | None = None

    @property
    def display_value(self) -> str:
        value = float(self.value)
        if self.format == "integer":
            rendered = f"{value:,.0f}"
        elif self.format == "number":
            rendered = f"{value:,.{self.decimals}f}"
        elif self.format == "percent":
            rendered = f"{value:,.{self.decimals}f}%"
        elif self.format == "bps":
            rendered = f"{value:,.{self.decimals}f} bps"
        else:
            rendered = f"{value:.{self.decimals}f}"
        return f"{rendered} {self.unit}" if self.unit else rendered


@dataclass(frozen=True)
class ResearchFigure:
    report_id: str
    title: str
    asset: str | None
    image_index: int | None


@dataclass(frozen=True)
class ExperimentArm:
    id: str
    label: str
    status: str
    model: str
    metrics: tuple[Metric, ...]


@dataclass(frozen=True)
class Experiment:
    id: str
    project: str
    title: str
    status: str
    maturity: str
    updated_at: date
    method: str
    dataset: str
    decision_state: str
    primary_metric_id: str | None
    objective: str
    summary: str
    decision: str
    caveats: tuple[str, ...]
    metrics: tuple[Metric, ...]
    report_ids: tuple[str, ...]
    evidence_ref: str
    featured: bool
    taxonomy_path: tuple[str, ...] = field(default_factory=tuple)
    related_taxonomy_paths: tuple[tuple[str, ...], ...] = field(default_factory=tuple)
    related_project_ids: tuple[str, ...] = field(default_factory=tuple)
    experiment_type: str = "not-recorded"
    model: str = "not-recorded"
    comparison_scope: str | None = None
    arms: tuple[ExperimentArm, ...] = field(default_factory=tuple)
    figures: tuple[ResearchFigure, ...] = field(default_factory=tuple)

    @property
    def project_ids(self) -> tuple[str, ...]:
        # Keep one canonical home while permitting shared evidence.
        return (self.project, *self.related_project_ids)

    @property
    def route(self) -> str:
        # Give each experiment one stable detail route.
        return f"experiments/{self.id}/"

    @property
    def stage(self) -> str | None:
        return self.taxonomy_path[0] if self.taxonomy_path else None

    @property
    def taxonomy_path_string(self) -> str | None:
        return "/".join(self.taxonomy_path) if self.taxonomy_path else None

    @property
    def display_date(self) -> str:
        return self.updated_at.isoformat()

    @property
    def primary_metric(self) -> Metric | None:
        if self.primary_metric_id is None:
            return None
        return next(metric for metric in self.metrics if metric.id == self.primary_metric_id)


@dataclass(frozen=True)
class Report:
    id: str
    project: str
    title: str
    date: date
    summary: str
    tags: tuple[str, ...]
    featured: bool
    match_method: str
    match_evidence: str
    format: str = "legacy-html"
    source_file: str | None = None
    source_sha256: str | None = None
    published_sha256: str | None = None
    content_file: str | None = None
    bundle_sha256: str | None = None
    hero_image: str | None = None
    revision_of: str | None = None
    stage: str | None = None
    route_project: str | None = None
    related_project_ids: tuple[str, ...] = field(default_factory=tuple)

    @property
    def project_ids(self) -> tuple[str, ...]:
        # Preserve published ownership and URLs when evidence is shared.
        return (self.project, *self.related_project_ids)

    @property
    def display_date(self) -> str:
        return self.date.isoformat()

    @property
    def route(self) -> str:
        route_project = self.route_project or self.project
        return f"reports/{route_project}/{self.id}/"

    @property
    def is_markdown(self) -> bool:
        return self.format == "markdown"


@dataclass(frozen=True)
class Study:
    id: str
    title: str
    question: str
    conclusion: str
    caveats: tuple[str, ...]
    project_ids: tuple[str, ...]
    experiment_ids: tuple[str, ...]
    report_ids: tuple[str, ...]
    taxonomy_path: tuple[str, ...]

    @property
    def route(self) -> str:
        # Keep one public route for each research question.
        return f"studies/{self.id}/"

    @property
    def stage(self) -> str | None:
        # Infrastructure questions have no prediction-stage contract.
        return self.taxonomy_path[0] if self.taxonomy_path else None


@dataclass(frozen=True)
class HomepageMetricSpec:
    id: str
    label: str
    category: str
    scope: str
    display_format: str
    experiment: str | None = None
    metric: str | None = None
    display_value: str | None = None


@dataclass(frozen=True)
class HighlightGate:
    id: str
    label: str
    state: str
    value: str


@dataclass(frozen=True)
class ChartSeries:
    id: str
    label: str
    values: tuple[float, ...]


@dataclass(frozen=True)
class FeaturedChart:
    title: str
    description: str
    source_note: str
    bins: tuple[int, ...]
    series: tuple[ChartSeries, ...]


@dataclass(frozen=True)
class FeaturedHighlight:
    report: str
    experiment: str
    decision_label: str
    decision_summary: str
    gates: tuple[HighlightGate, ...]
    chart: FeaturedChart


@dataclass(frozen=True)
class RejectedIdea:
    title: str
    state: str
    reason: str
    experiment: str
    metric_ids: tuple[str, ...]


@dataclass(frozen=True)
class HomepageHighlights:
    metrics: tuple[HomepageMetricSpec, ...]
    featured: FeaturedHighlight
    rejected_ideas: tuple[RejectedIdea, ...]


@dataclass(frozen=True)
class Catalog:
    categories: tuple[Category, ...]
    projects: tuple[Project, ...]
    reports: tuple[Report, ...]
    research_stages: tuple[ResearchStageDefinition, ...] = field(default_factory=tuple)
    research_taxonomy: tuple[ResearchTaxonomyStage, ...] = field(default_factory=tuple)
    experiments: tuple[Experiment, ...] = field(default_factory=tuple)
    studies: tuple[Study, ...] = field(default_factory=tuple)
    featured_report_id: str | None = None
    homepage: HomepageHighlights | None = None
    knowledge: KnowledgeCatalog | None = None

    @property
    def research_projects(self) -> tuple[Project, ...]:
        return tuple(project for project in self.projects if project.section == "research")

    @property
    def knowledge_projects(self) -> tuple[Project, ...]:
        return tuple(project for project in self.projects if project.section == "knowledge")

    @property
    def infrastructure_projects(self) -> tuple[Project, ...]:
        return tuple(project for project in self.projects if project.section == "infrastructure")

    @property
    def stage_by_id(self) -> dict[str, ResearchStageDefinition]:
        return {stage.id: stage for stage in self.research_stages}

    @property
    def taxonomy_by_stage(self) -> dict[str, ResearchTaxonomyStage]:
        return {stage.id: stage for stage in self.research_taxonomy}

    @property
    def project_by_id(self) -> dict[str, Project]:
        return {project.id: project for project in self.projects}

    @property
    def category_by_id(self) -> dict[str, Category]:
        return {category.id: category for category in self.categories}

    @property
    def report_by_id(self) -> dict[str, Report]:
        return {report.id: report for report in self.reports}

    @property
    def experiment_by_id(self) -> dict[str, Experiment]:
        return {experiment.id: experiment for experiment in self.experiments}

    @property
    def study_by_id(self) -> dict[str, Study]:
        # Resolve research questions independently of experiment identities.
        return {study.id: study for study in self.studies}

    def studies_for_project(self, project_id: str) -> list[Study]:
        # Share a question across projects without duplicating its record.
        return [study for study in self.studies if project_id in study.project_ids]

    def studies_for_experiment(self, experiment_id: str) -> list[Study]:
        # Resolve the reverse side of the question/evidence relation.
        return [study for study in self.studies if experiment_id in study.experiment_ids]

    def experiments_for_study(self, study_id: str) -> list[Experiment]:
        # Retain the curated evidence order within each question.
        return [self.experiment_by_id[eid] for eid in self.study_by_id[study_id].experiment_ids]

    def studies_for_report(self, report_id: str) -> list[Study]:
        # Include direct publications and experiment-backed evidence.
        experiment_ids = {e.id for e in self.experiments if report_id in e.report_ids}
        return [s for s in self.studies if report_id in s.report_ids or experiment_ids.intersection(s.experiment_ids)]

    def experiments_for_report(self, report_id: str) -> list[Experiment]:
        # One publication may document several experiments.
        return [e for e in self.experiments if report_id in e.report_ids]

    @property
    def featured_report(self) -> Report | None:
        if self.featured_report_id is None:
            return None
        return self.report_by_id.get(self.featured_report_id)

    @property
    def current_reports(self) -> tuple[Report, ...]:
        superseded = {report.revision_of for report in self.reports if report.revision_of}
        return tuple(report for report in self.reports if report.id not in superseded)

    def reports_for_project(self, project_id: str) -> list[Report]:
        return sorted(
            (report for report in self.current_reports if project_id in report.project_ids),
            key=lambda report: (report.date, report.id),
            reverse=True,
        )

    def all_reports_for_project(self, project_id: str) -> list[Report]:
        return sorted(
            (report for report in self.reports if report.project == project_id),
            key=lambda report: (report.date, report.id),
            reverse=True,
        )

    def experiments_for_project(self, project_id: str) -> list[Experiment]:
        return sorted(
            (experiment for experiment in self.experiments if project_id in experiment.project_ids),
            key=lambda experiment: (experiment.updated_at, experiment.id),
            reverse=True,
        )

    def experiments_for_stage(self, project_id: str, stage_id: str) -> list[Experiment]:
        return [experiment for experiment in self.experiments_for_project(project_id) if experiment.stage == stage_id]

    def experiments_for_taxonomy_path(
        self,
        project_id: str,
        taxonomy_path: tuple[str, ...],
    ) -> list[Experiment]:
        return [
            experiment
            for experiment in self.experiments_for_project(project_id)
            if experiment.taxonomy_path == taxonomy_path
        ]

    def taxonomy_titles(self, taxonomy_path: tuple[str, ...]) -> tuple[str, ...]:
        if not taxonomy_path:
            return ()
        titles = [self.stage_by_id[taxonomy_path[0]].title]
        for length in range(2, len(taxonomy_path) + 1):
            node = taxonomy_node_for_path(self.research_taxonomy, taxonomy_path[:length])
            if node is None:
                break
            titles.append(node.title)
        return tuple(titles)


def _load_yaml(path: Path, supported_versions: tuple[int, ...] = (1,)) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CatalogError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CatalogError(f"{path} must contain a YAML mapping")
    if value.get("schema_version") not in supported_versions:
        raise CatalogError(f"{path} has unsupported schema_version")
    return value


def _require_slug(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not SLUG_RE.fullmatch(value):
        raise CatalogError(f"{field_name} must be a lowercase hyphenated slug: {value!r}")
    return value


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CatalogError(f"{field_name} must be non-empty text")
    return value.strip()


def _require_relative_reference(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    path = PurePath(text)
    if path.is_absolute() or ".." in path.parts:
        raise CatalogError(f"{field_name} must be relative without parent traversal")
    return text


def _unique(values: list[str], field_name: str) -> None:
    duplicates = sorted({value for value in values if values.count(value) > 1})
    if duplicates:
        raise CatalogError(f"duplicate {field_name}: {', '.join(duplicates)}")


def _parse_date(value: Any, field_name: str) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise CatalogError(f"{field_name} must be YYYY-MM-DD") from exc
    raise CatalogError(f"{field_name} must be a date")


def _require_text_list(value: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise CatalogError(f"{field_name} must be a list of text")
    return tuple(_require_text(item, f"{field_name}[{index}]") for index, item in enumerate(value))


def _require_number(value: Any, field_name: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise CatalogError(f"{field_name} must be a finite number")
    return value


def _require_taxonomy_path(value: Any, field_name: str) -> tuple[str, ...]:
    text = _require_text(value, field_name)
    parts = tuple(text.split("/"))
    if any(not SLUG_RE.fullmatch(part) for part in parts):
        raise CatalogError(f"{field_name} must be a slash-separated slug path: {value!r}")
    return parts


def taxonomy_anchor(taxonomy_path: tuple[str, ...]) -> str:
    return "topic-" + "--".join(taxonomy_path)


def taxonomy_node_for_path(
    taxonomy: tuple[ResearchTaxonomyStage, ...],
    taxonomy_path: tuple[str, ...],
) -> ResearchTaxonomyNode | None:
    if len(taxonomy_path) < 2:
        return None
    stage = next((item for item in taxonomy if item.id == taxonomy_path[0]), None)
    if stage is None:
        return None
    nodes = stage.nodes
    node: ResearchTaxonomyNode | None = None
    for part in taxonomy_path[1:]:
        node = next((item for item in nodes if item.id == part), None)
        if node is None:
            return None
        nodes = node.children
    return node


def taxonomy_path_exists(
    taxonomy: tuple[ResearchTaxonomyStage, ...],
    taxonomy_path: tuple[str, ...],
) -> bool:
    stage_ids = {stage.id for stage in taxonomy}
    return bool(taxonomy_path) and (
        (len(taxonomy_path) == 1 and taxonomy_path[0] in stage_ids)
        or taxonomy_node_for_path(taxonomy, taxonomy_path) is not None
    )


def _load_research_flow(path: Path) -> tuple[ResearchStageDefinition, ...]:
    raw = _load_yaml(path)
    raw_stages = raw.get("stages")
    if not isinstance(raw_stages, list) or not raw_stages:
        raise CatalogError(f"{path} must define a non-empty stages list")
    stages: list[ResearchStageDefinition] = []
    for index, item in enumerate(raw_stages):
        if not isinstance(item, dict):
            raise CatalogError(f"stages[{index}] must be a mapping")
        stages.append(
            ResearchStageDefinition(
                id=_require_slug(item.get("id"), f"stages[{index}].id"),
                title=_require_text(item.get("title"), f"stages[{index}].title"),
                short_title=_require_text(item.get("short_title"), f"stages[{index}].short_title"),
                description=_require_text(item.get("description"), f"stages[{index}].description"),
            )
        )
    _unique([stage.id for stage in stages], "research stage ids")
    return tuple(stages)


def _load_research_taxonomy(
    path: Path,
    research_stages: tuple[ResearchStageDefinition, ...],
) -> tuple[ResearchTaxonomyStage, ...]:
    raw = _load_yaml(path)
    _require_relative_reference(raw.get("source"), "research taxonomy source")
    raw_stages = raw.get("stages")
    if not isinstance(raw_stages, list) or not raw_stages:
        raise CatalogError(f"{path} must define a non-empty stages list")

    def load_nodes(raw_nodes: Any, field_name: str) -> tuple[ResearchTaxonomyNode, ...]:
        if not isinstance(raw_nodes, list):
            raise CatalogError(f"{field_name} must be a list")
        nodes: list[ResearchTaxonomyNode] = []
        for index, item in enumerate(raw_nodes):
            if not isinstance(item, dict):
                raise CatalogError(f"{field_name}[{index}] must be a mapping")
            node_id = _require_slug(item.get("id"), f"{field_name}[{index}].id")
            children = load_nodes(item.get("children", []), f"{field_name}[{index}].children")
            nodes.append(
                ResearchTaxonomyNode(
                    id=node_id,
                    title=_require_text(item.get("title"), f"{field_name}[{index}].title"),
                    children=children,
                )
            )
        _unique([node.id for node in nodes], f"{field_name} ids")
        return tuple(nodes)

    taxonomy: list[ResearchTaxonomyStage] = []
    for index, item in enumerate(raw_stages):
        if not isinstance(item, dict):
            raise CatalogError(f"taxonomy stages[{index}] must be a mapping")
        stage_id = _require_slug(item.get("id"), f"taxonomy stages[{index}].id")
        taxonomy.append(
            ResearchTaxonomyStage(
                id=stage_id,
                nodes=load_nodes(item.get("nodes"), f"taxonomy stage {stage_id}.nodes"),
            )
        )
    expected = [stage.id for stage in research_stages]
    actual = [stage.id for stage in taxonomy]
    if actual != expected:
        raise CatalogError("research taxonomy must declare all research stages in canonical order")
    return tuple(taxonomy)


def _load_projects(
    path: Path,
    research_stages: tuple[ResearchStageDefinition, ...],
    research_taxonomy: tuple[ResearchTaxonomyStage, ...],
) -> tuple[tuple[Category, ...], tuple[Project, ...]]:
    raw = _load_yaml(path)
    raw_categories = raw.get("categories")
    raw_projects = raw.get("projects")
    if not isinstance(raw_categories, list) or not isinstance(raw_projects, list):
        raise CatalogError(f"{path} must define categories and projects lists")

    categories: list[Category] = []
    for index, item in enumerate(raw_categories):
        if not isinstance(item, dict):
            raise CatalogError(f"categories[{index}] must be a mapping")
        categories.append(
            Category(
                id=_require_slug(item.get("id"), f"categories[{index}].id"),
                title=_require_text(item.get("title"), f"categories[{index}].title"),
                description=_require_text(item.get("description"), f"categories[{index}].description"),
            )
        )
    _unique([item.id for item in categories], "category ids")
    category_ids = {item.id for item in categories}

    projects: list[Project] = []
    for index, item in enumerate(raw_projects):
        if not isinstance(item, dict):
            raise CatalogError(f"projects[{index}] must be a mapping")
        project_id = _require_slug(item.get("id"), f"projects[{index}].id")
        section = _require_slug(item.get("section", "research"), f"projects[{index}].section")
        if section not in ALLOWED_PROJECT_SECTIONS:
            raise CatalogError(f"project {project_id} has unsupported section {section}")
        category = _require_slug(item.get("category"), f"projects[{index}].category")
        if category not in category_ids:
            raise CatalogError(f"project {project_id} references unknown category {category}")
        raw_refs = item.get("source_refs", [])
        raw_stages = item.get("stages", [])
        raw_legacy_redirects = item.get("legacy_topic_redirects", [])
        if not isinstance(raw_refs, list):
            raise CatalogError(f"project {project_id} source_refs must be a list of names")
        source_refs = tuple(
            _require_relative_reference(ref, f"project {project_id} source_refs[{ref_index}]")
            for ref_index, ref in enumerate(raw_refs)
        )
        # Keep registry ownership independent of local checkout paths.
        raw_experiments = item.get("registry_experiments", [])
        if not isinstance(raw_experiments, list):
            raise CatalogError(f"project {project_id} registry_experiments must be a list")
        registry_experiments = tuple(
            _require_slug(experiment_id, f"project {project_id} registry experiment id")
            for experiment_id in raw_experiments
        )
        if not isinstance(raw_stages, list):
            raise CatalogError(f"project {project_id} stages must be a list")
        stage_ids = {stage.id for stage in research_stages}
        stages: list[ProjectStage] = []
        for stage_index, stage in enumerate(raw_stages):
            if not isinstance(stage, dict):
                raise CatalogError(f"project {project_id} stages[{stage_index}] must be a mapping")
            stage_id = _require_slug(stage.get("id"), f"project {project_id} stage id")
            if stage_id not in stage_ids:
                raise CatalogError(f"project {project_id} references unknown stage {stage_id}")
            state = _require_slug(stage.get("state"), f"project {project_id} stage {stage_id}.state")
            if state not in ALLOWED_STAGE_STATES:
                raise CatalogError(f"project {project_id} stage {stage_id} has unsupported state {state}")
            stages.append(
                ProjectStage(
                    id=stage_id,
                    state=state,
                    summary=_require_text(stage.get("summary"), f"project {project_id} stage {stage_id}.summary"),
                )
            )
        _unique([stage.id for stage in stages], f"stage ids in {project_id}")
        declared_stage_ids = [stage.id for stage in stages]
        expected_stage_ids = [stage.id for stage in research_stages]
        if section == "research" and declared_stage_ids != expected_stage_ids:
            raise CatalogError(
                f"project {project_id} must declare all research stages in canonical order"
            )
        if section != "research" and stages:
            raise CatalogError(f"project {project_id} outside research must not declare stages")
        if not isinstance(raw_legacy_redirects, list):
            raise CatalogError(f"project {project_id} legacy_topic_redirects must be a list")
        if section != "research" and raw_legacy_redirects:
            raise CatalogError(
                f"project {project_id} outside research must not declare legacy topic redirects"
            )
        legacy_redirects: list[LegacyTopicRedirect] = []
        for redirect_index, redirect in enumerate(raw_legacy_redirects):
            if not isinstance(redirect, dict):
                raise CatalogError(
                    f"project {project_id} legacy_topic_redirects[{redirect_index}] must be a mapping"
                )
            taxonomy_path = _require_taxonomy_path(
                redirect.get("taxonomy_path"),
                f"project {project_id} legacy topic taxonomy_path",
            )
            if not taxonomy_path_exists(research_taxonomy, taxonomy_path):
                raise CatalogError(
                    f"project {project_id} legacy topic references unknown taxonomy path "
                    f"{'/'.join(taxonomy_path)}"
                )
            legacy_redirects.append(
                LegacyTopicRedirect(
                    id=_require_slug(redirect.get("id"), f"project {project_id} legacy topic id"),
                    taxonomy_path=taxonomy_path,
                )
            )
        _unique([redirect.id for redirect in legacy_redirects], f"legacy topic ids in {project_id}")
        projects.append(
            Project(
                id=project_id,
                title=_require_text(item.get("title"), f"projects[{index}].title"),
                category=category,
                status=_require_slug(item.get("status"), f"projects[{index}].status"),
                description=_require_text(item.get("description"), f"projects[{index}].description"),
                objective=_require_text(item.get("objective"), f"projects[{index}].objective"),
                review_summary=_require_text(item.get("review_summary"), f"projects[{index}].review_summary"),
                source_refs=source_refs,
                section=section,
                stages=tuple(stages),
                legacy_topic_redirects=tuple(legacy_redirects),
                registry_experiments=registry_experiments,
            )
        )
    _unique([item.id for item in projects], "project ids")
    # Each registered experiment belongs to exactly one site project.
    _unique(
        [experiment_id for project in projects for experiment_id in project.registry_experiments],
        "registry experiment ownership",
    )
    return tuple(categories), tuple(projects)


def _load_reports(
    path: Path,
    projects: tuple[Project, ...],
    research_stages: tuple[ResearchStageDefinition, ...],
) -> tuple[tuple[Report, ...], str]:
    raw = _load_yaml(path, supported_versions=(2,))
    featured_report_id = _require_slug(raw.get("featured_report"), "featured_report")
    raw_reports = raw.get("reports")
    if not isinstance(raw_reports, list):
        raise CatalogError(f"{path} must define a reports list")
    project_by_id = {project.id: project for project in projects}
    stage_ids = {stage.id for stage in research_stages}
    reports: list[Report] = []
    for index, item in enumerate(raw_reports):
        if not isinstance(item, dict):
            raise CatalogError(f"reports[{index}] must be a mapping")
        report_id = _require_slug(item.get("id"), f"reports[{index}].id")
        project_id = _require_slug(item.get("project"), f"report {report_id}.project")
        project = project_by_id.get(project_id)
        if project is None:
            raise CatalogError(f"report {report_id} references unknown project {project_id}")
        stage_value = item.get("stage")
        stage = None if stage_value is None else _require_slug(stage_value, f"report {report_id}.stage")
        if project.section == "research" and stage not in stage_ids:
            raise CatalogError(f"report {report_id} must reference a research stage")
        if project.section != "research" and stage is not None:
            raise CatalogError(f"report {report_id} outside research must not reference a stage")
        route_project_value = item.get("route_project")
        route_project = None if route_project_value is None else _require_slug(
            route_project_value, f"report {report_id}.route_project"
        )
        report_format = _require_slug(item.get("format", "legacy-html"), f"report {report_id}.format")
        if report_format not in {"legacy-html", "markdown"}:
            raise CatalogError(f"report {report_id} has unsupported format {report_format}")
        match_method = _require_text(item.get("match_method"), f"report {report_id}.match_method")
        if match_method not in ALLOWED_MATCH_METHODS:
            raise CatalogError(f"report {report_id} has unsupported match_method {match_method}")
        revision_value = item.get("revision_of")
        revision_of = None if revision_value is None else _require_slug(
            revision_value, f"report {report_id}.revision_of"
        )
        common = {
            "id": report_id,
            "project": project_id,
            "stage": stage,
            "route_project": route_project,
            "format": report_format,
            "match_method": match_method,
            "match_evidence": _require_relative_reference(
                item.get("match_evidence"), f"report {report_id}.match_evidence"
            ),
            "revision_of": revision_of,
            "related_project_ids": related_project_ids(item, project_id, project_by_id),
        }
        if report_format == "legacy-html":
            source_file = _require_relative_reference(
                item.get("source_file"), f"report {report_id}.source_file"
            )
            if Path(source_file).suffix.lower() != ".html":
                raise CatalogError(f"report {report_id} source_file must be a relative HTML path")
            tags = item.get("tags", [])
            if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
                raise CatalogError(f"report {report_id} tags must be a list of text")
            source_sha256 = _require_text(item.get("source_sha256"), f"report {report_id}.source_sha256")
            if not SHA256_RE.fullmatch(source_sha256):
                raise CatalogError(f"report {report_id} source_sha256 must be lowercase SHA-256")
            published_hash = _require_text(item["published_sha256"], f"report {report_id}.published_sha256")
            if not SHA256_RE.fullmatch(published_hash):
                raise CatalogError(f"report {report_id} published_sha256 must be lowercase SHA-256")
            report = Report(
                **common,
                title=_require_text(item.get("title"), f"report {report_id}.title"),
                source_file=source_file,
                source_sha256=source_sha256,
                published_sha256=published_hash,
                date=_parse_date(item.get("date"), f"report {report_id}.date"),
                summary=_require_text(item.get("summary"), f"report {report_id}.summary"),
                tags=tuple(tag.strip() for tag in tags),
                featured=bool(item.get("featured", False)),
            )
        else:
            content_file = _require_relative_reference(
                item.get("content_file"), f"report {report_id}.content_file"
            )
            content_project = route_project or project_id
            expected = PurePath("report-docs") / content_project / report_id / "report.md"
            if PurePath(content_file) != expected:
                raise CatalogError(f"report {report_id} content_file must be {expected.as_posix()}")
            bundle_sha256 = _require_text(item.get("bundle_sha256"), f"report {report_id}.bundle_sha256")
            if not SHA256_RE.fullmatch(bundle_sha256):
                raise CatalogError(f"report {report_id} bundle_sha256 must be lowercase SHA-256")
            try:
                source = load_report_source(path.parent / content_file)
            except ReportContentError as exc:
                raise CatalogError(str(exc)) from exc
            if source.bundle_sha256 != bundle_sha256:
                raise CatalogError(
                    f"report {report_id} bundle checksum changed: expected {bundle_sha256}, "
                    f"got {source.bundle_sha256}"
                )
            hero_image_value = item.get("hero_image")
            hero_image = None
            if hero_image_value is not None:
                hero_image = _require_relative_reference(
                    hero_image_value, f"report {report_id}.hero_image"
                )
                hero_path = PurePath(hero_image)
                if not hero_path.parts or hero_path.parts[0] != "images":
                    raise CatalogError(f"report {report_id} hero_image must stay below images/")
                resolved_hero = source.path.parent.joinpath(*hero_path.parts).resolve()
                if resolved_hero not in source.referenced_assets:
                    raise CatalogError(
                        f"report {report_id} hero_image must reference an image used by the report"
                    )
            report = Report(
                **common,
                title=source.front_matter.title,
                content_file=content_file,
                bundle_sha256=bundle_sha256,
                hero_image=hero_image,
                date=source.front_matter.date,
                summary=source.front_matter.summary,
                tags=source.front_matter.tags,
                featured=source.front_matter.featured,
            )
        reports.append(
            report
        )
    _unique([item.id for item in reports], "report ids")
    _unique([item.source_sha256 for item in reports if item.source_sha256], "report source hashes")
    _unique([item.bundle_sha256 for item in reports if item.bundle_sha256], "report bundle hashes")
    report_by_id = {report.id: report for report in reports}
    successors: dict[str, str] = {}
    for report in reports:
        if not report.revision_of:
            continue
        predecessor = report_by_id.get(report.revision_of)
        if predecessor is None:
            raise CatalogError(f"report {report.id} revision_of references unknown report {report.revision_of}")
        if (
            predecessor.project != report.project
            or predecessor.stage != report.stage
        ):
            raise CatalogError(
                f"report {report.id} revision_of must keep project ownership and stage"
            )
        if predecessor.id in successors:
            raise CatalogError(f"report {predecessor.id} has multiple current successors")
        successors[predecessor.id] = report.id
        seen = {report.id}
        cursor = predecessor
        while cursor.revision_of:
            if cursor.id in seen:
                raise CatalogError(f"report revision chain contains a cycle at {cursor.id}")
            seen.add(cursor.id)
            cursor = report_by_id.get(cursor.revision_of)  # type: ignore[assignment]
            if cursor is None:
                break
    featured_report = report_by_id.get(featured_report_id)
    if featured_report is None:
        raise CatalogError(f"featured_report references unknown report {featured_report_id}")
    if featured_report_id in successors:
        raise CatalogError(f"featured_report must select a current report, not {featured_report_id}")
    return tuple(reports), featured_report_id


def parse_metrics(values: Any, context: str) -> tuple[Metric, ...]:
    # Validate numeric values and retain their evaluation scope.
    raw_metrics = values
    if not isinstance(raw_metrics, list):
        raise CatalogError(f"experiment {context}.metrics must be a list")
    metrics: list[Metric] = []
    for metric_index, metric in enumerate(raw_metrics):
        if not isinstance(metric, dict):
            raise CatalogError(f"experiment {context}.metrics[{metric_index}] must be a mapping")
        metric_id = _require_slug(metric.get("id"), f"experiment {context} metric id")
        metric_format = _require_slug(metric.get("format"), f"experiment {context} metric {metric_id}.format")
        if metric_format not in ALLOWED_METRIC_FORMATS:
            raise CatalogError(f"experiment {context} metric {metric_id} has unsupported format {metric_format}")
        decimals = metric.get("decimals", 0)
        if isinstance(decimals, bool) or not isinstance(decimals, int) or not 0 <= decimals <= 6:
            raise CatalogError(f"experiment {context} metric {metric_id}.decimals must be between 0 and 6")
        unit_value = metric.get("unit")
        unit = None if unit_value is None else _require_text(unit_value, f"experiment {context} metric {metric_id}.unit")
        metrics.append(
            Metric(
                id=metric_id,
                label=_require_text(metric.get("label"), f"experiment {context} metric {metric_id}.label"),
                value=_require_number(metric.get("value"), f"experiment {context} metric {metric_id}.value"),
                format=metric_format,
                decimals=decimals,
                context=_require_text(metric.get("context"), f"experiment {context} metric {metric_id}.context"),
                unit=unit,
            )
        )
    _unique([metric.id for metric in metrics], f"metric ids in experiment {context}")
    return tuple(metrics)


def _load_experiments(
    path: Path,
    projects: tuple[Project, ...],
    reports: tuple[Report, ...],
    research_taxonomy: tuple[ResearchTaxonomyStage, ...],
) -> tuple[Experiment, ...]:
    raw = _load_yaml(path)
    raw_experiments = raw.get("experiments")
    if not isinstance(raw_experiments, list):
        raise CatalogError(f"{path} must define a experiments list")
    project_by_id = {project.id: project for project in projects}
    report_by_id = {report.id: report for report in reports}
    experiments: list[Experiment] = []
    for index, item in enumerate(raw_experiments):
        if not isinstance(item, dict):
            raise CatalogError(f"experiments[{index}] must be a mapping")
        experiment_id = _require_slug(item.get("id"), f"experiments[{index}].id")
        project_id = _require_slug(item.get("project"), f"experiment {experiment_id}.project")
        project = project_by_id.get(project_id)
        if project is None:
            raise CatalogError(f"experiment {experiment_id} references unknown project {project_id}")
        taxonomy_value = item.get("taxonomy_path")
        taxonomy_path = (
            ()
            if taxonomy_value is None
            else _require_taxonomy_path(taxonomy_value, f"experiment {experiment_id}.taxonomy_path")
        )
        raw_related_paths = item.get("related_taxonomy_paths", [])
        if not isinstance(raw_related_paths, list):
            raise CatalogError(f"experiment {experiment_id}.related_taxonomy_paths must be a list")
        related_taxonomy_paths = tuple(
            _require_taxonomy_path(value, f"experiment {experiment_id}.related_taxonomy_paths[{path_index}]")
            for path_index, value in enumerate(raw_related_paths)
        )
        if project.section == "research":
            if not taxonomy_path_exists(research_taxonomy, taxonomy_path):
                raise CatalogError(f"experiment {experiment_id} must reference a valid research taxonomy path")
            unknown_related = [
                value
                for value in related_taxonomy_paths
                if not taxonomy_path_exists(research_taxonomy, value)
            ]
            if unknown_related:
                raise CatalogError(
                    f"experiment {experiment_id} references unknown related taxonomy path "
                    f"{'/'.join(unknown_related[0])}"
                )
            if taxonomy_path in related_taxonomy_paths:
                raise CatalogError(f"experiment {experiment_id} repeats its primary taxonomy path as related")
            _unique(
                ["/".join(value) for value in related_taxonomy_paths],
                f"related taxonomy paths in experiment {experiment_id}",
            )
        elif taxonomy_path or related_taxonomy_paths:
            raise CatalogError(f"experiment {experiment_id} outside research must not reference taxonomy")
        status = _require_slug(item.get("status"), f"experiment {experiment_id}.status")
        if status not in ALLOWED_EXPERIMENT_STATUSES:
            raise CatalogError(f"experiment {experiment_id} has unsupported status {status}")
        maturity = _require_slug(item.get("maturity"), f"experiment {experiment_id}.maturity")
        if maturity not in ALLOWED_MATURITIES:
            raise CatalogError(f"experiment {experiment_id} has unsupported maturity {maturity}")
        decision_state = _require_slug(
            item.get("decision_state"), f"experiment {experiment_id}.decision_state"
        )
        if decision_state not in ALLOWED_DECISION_STATES:
            raise CatalogError(
                f"experiment {experiment_id} has unsupported decision_state {decision_state}"
            )
        metrics = parse_metrics(item.get("metrics", []), experiment_id)
        primary_metric_value = item.get("primary_metric")
        primary_metric_id = None
        if primary_metric_value is not None:
            primary_metric_id = _require_slug(
                primary_metric_value, f"experiment {experiment_id}.primary_metric"
            )
            if primary_metric_id not in {metric.id for metric in metrics}:
                raise CatalogError(
                    f"experiment {experiment_id}.primary_metric references unknown metric {primary_metric_id}"
                )
        if metrics and primary_metric_id is None:
            raise CatalogError(f"experiment {experiment_id} with metrics must define primary_metric")
        raw_report_ids = item.get("report_ids", [])
        if not isinstance(raw_report_ids, list):
            raise CatalogError(f"experiment {experiment_id}.report_ids must be a list")
        report_ids = tuple(
            _require_slug(report_id, f"experiment {experiment_id}.report_ids[{report_index}]")
            for report_index, report_id in enumerate(raw_report_ids)
        )
        _unique(list(report_ids), f"report ids in experiment {experiment_id}")
        related_projects = related_project_ids(item, project_id, project_by_id)
        for report_id in report_ids:
            report = report_by_id.get(report_id)
            if report is None:
                raise CatalogError(f"experiment {experiment_id} references unknown report {report_id}")
            if not set(report.project_ids).intersection((project_id, *related_projects)):
                raise CatalogError(f"experiment {experiment_id} report {report_id} belongs to another project")
        experiments.append(
            Experiment(
                id=experiment_id,
                project=project_id,
                taxonomy_path=taxonomy_path,
                related_taxonomy_paths=related_taxonomy_paths,
                title=_require_text(item.get("title"), f"experiment {experiment_id}.title"),
                status=status,
                maturity=maturity,
                updated_at=_parse_date(item.get("updated_at"), f"experiment {experiment_id}.updated_at"),
                method=_require_text(item.get("method"), f"experiment {experiment_id}.method"),
                dataset=_require_text(item.get("dataset"), f"experiment {experiment_id}.dataset"),
                decision_state=decision_state,
                primary_metric_id=primary_metric_id,
                objective=_require_text(item.get("objective"), f"experiment {experiment_id}.objective"),
                summary=_require_text(item.get("summary"), f"experiment {experiment_id}.summary"),
                decision=_require_text(item.get("decision"), f"experiment {experiment_id}.decision"),
                caveats=_require_text_list(item.get("caveats", []), f"experiment {experiment_id}.caveats"),
                metrics=tuple(metrics),
                report_ids=report_ids,
                evidence_ref=_require_relative_reference(item.get("evidence_ref"), f"experiment {experiment_id}.evidence_ref"),
                featured=bool(item.get("featured", False)),
                related_project_ids=related_projects,
                experiment_type=_require_slug(item["experiment_type"], f"experiment {experiment_id}.experiment_type"),
                model=_require_text(item["model"], f"experiment {experiment_id}.model"),
                comparison_scope=item.get("comparison_scope"),
                arms=parse_arms(item, experiment_id),
                figures=parse_figures(item, report_ids, report_by_id),
            )
        )
    _unique([experiment.id for experiment in experiments], "experiment ids")
    return tuple(experiments)


def _load_homepage(path: Path, catalog: Catalog) -> HomepageHighlights:
    """Load curated homepage evidence and validate every catalog reference."""
    raw = _load_yaml(path)
    experiment_by_id = catalog.experiment_by_id
    report_by_id = catalog.report_by_id

    raw_metrics = raw.get("metrics")
    if not isinstance(raw_metrics, list) or not raw_metrics:
        raise CatalogError(f"{path} must define a non-empty metrics list")
    metrics: list[HomepageMetricSpec] = []
    for index, item in enumerate(raw_metrics):
        if not isinstance(item, dict):
            raise CatalogError(f"homepage metrics[{index}] must be a mapping")
        metric_id = _require_slug(item.get("id"), f"homepage metrics[{index}].id")
        category = _require_slug(item.get("category"), f"homepage metric {metric_id}.category")
        if category not in ALLOWED_HOMEPAGE_METRIC_CATEGORIES:
            raise CatalogError(f"homepage metric {metric_id} has unsupported category {category}")
        display_format = _require_slug(
            item.get("display_format", "raw"), f"homepage metric {metric_id}.display_format"
        )
        if display_format not in ALLOWED_HOMEPAGE_VALUE_FORMATS:
            raise CatalogError(
                f"homepage metric {metric_id} has unsupported display_format {display_format}"
            )
        experiment_value = item.get("experiment")
        metric_value = item.get("metric")
        display_value_raw = item.get("display_value")
        has_reference = experiment_value is not None or metric_value is not None
        has_literal = display_value_raw is not None
        if has_reference == has_literal:
            raise CatalogError(
                f"homepage metric {metric_id} must define either a experiment/metric reference or display_value"
            )
        experiment_id = None
        referenced_metric_id = None
        display_value = None
        if has_reference:
            experiment_id = _require_slug(experiment_value, f"homepage metric {metric_id}.experiment")
            referenced_metric_id = _require_slug(
                metric_value, f"homepage metric {metric_id}.metric"
            )
            experiment = experiment_by_id.get(experiment_id)
            if experiment is None:
                raise CatalogError(f"homepage metric {metric_id} references unknown experiment {experiment_id}")
            if referenced_metric_id not in {metric.id for metric in experiment.metrics}:
                raise CatalogError(
                    f"homepage metric {metric_id} references unknown metric "
                    f"{experiment_id}/{referenced_metric_id}"
                )
        else:
            display_value = _require_text(
                display_value_raw, f"homepage metric {metric_id}.display_value"
            )
            if display_format != "raw":
                raise CatalogError(
                    f"homepage metric {metric_id} literal display_value must use raw format"
                )
        metrics.append(
            HomepageMetricSpec(
                id=metric_id,
                label=_require_text(item.get("label"), f"homepage metric {metric_id}.label"),
                category=category,
                scope=_require_text(item.get("scope"), f"homepage metric {metric_id}.scope"),
                display_format=display_format,
                experiment=experiment_id,
                metric=referenced_metric_id,
                display_value=display_value,
            )
        )
    _unique([item.id for item in metrics], "homepage metric ids")

    raw_featured = raw.get("featured")
    if not isinstance(raw_featured, dict):
        raise CatalogError(f"{path} must define featured as a mapping")
    featured_report_id = _require_slug(raw_featured.get("report"), "homepage featured.report")
    if featured_report_id != catalog.featured_report_id:
        raise CatalogError("homepage featured.report must match reports.yaml featured_report")
    featured_report = report_by_id.get(featured_report_id)
    if featured_report is None:
        raise CatalogError(f"homepage featured references unknown report {featured_report_id}")
    featured_experiment_id = _require_slug(raw_featured.get("experiment"), "homepage featured.experiment")
    featured_experiment = experiment_by_id.get(featured_experiment_id)
    if featured_experiment is None:
        raise CatalogError(f"homepage featured references unknown experiment {featured_experiment_id}")
    if featured_report_id not in featured_experiment.report_ids:
        raise CatalogError("homepage featured experiment must link the featured report")

    raw_gates = raw_featured.get("gates")
    if not isinstance(raw_gates, list) or not raw_gates:
        raise CatalogError("homepage featured.gates must be a non-empty list")
    gates: list[HighlightGate] = []
    for index, item in enumerate(raw_gates):
        if not isinstance(item, dict):
            raise CatalogError(f"homepage featured.gates[{index}] must be a mapping")
        gate_id = _require_slug(item.get("id"), f"homepage featured.gates[{index}].id")
        state = _require_slug(item.get("state"), f"homepage gate {gate_id}.state")
        if state not in ALLOWED_HIGHLIGHT_STATES:
            raise CatalogError(f"homepage gate {gate_id} has unsupported state {state}")
        gates.append(
            HighlightGate(
                id=gate_id,
                label=_require_text(item.get("label"), f"homepage gate {gate_id}.label"),
                state=state,
                value=_require_text(item.get("value"), f"homepage gate {gate_id}.value"),
            )
        )
    _unique([item.id for item in gates], "homepage gate ids")

    raw_chart = raw_featured.get("chart")
    if not isinstance(raw_chart, dict):
        raise CatalogError("homepage featured.chart must be a mapping")
    raw_bins = raw_chart.get("bins")
    if (
        not isinstance(raw_bins, list)
        or not raw_bins
        or any(isinstance(value, bool) or not isinstance(value, int) or value <= 0 for value in raw_bins)
    ):
        raise CatalogError("homepage featured.chart.bins must be positive integers")
    bins = tuple(raw_bins)
    if tuple(sorted(set(bins))) != bins:
        raise CatalogError("homepage featured.chart.bins must be unique and increasing")
    raw_series = raw_chart.get("series")
    if not isinstance(raw_series, list) or not raw_series:
        raise CatalogError("homepage featured.chart.series must be a non-empty list")
    series: list[ChartSeries] = []
    for index, item in enumerate(raw_series):
        if not isinstance(item, dict):
            raise CatalogError(f"homepage featured.chart.series[{index}] must be a mapping")
        series_id = _require_slug(item.get("id"), f"homepage chart series[{index}].id")
        raw_values = item.get("values")
        if not isinstance(raw_values, list) or len(raw_values) != len(bins):
            raise CatalogError(
                f"homepage chart series {series_id} must have one value for every bin"
            )
        values = tuple(
            float(_require_number(value, f"homepage chart series {series_id}.values[{value_index}]"))
            for value_index, value in enumerate(raw_values)
        )
        series.append(
            ChartSeries(
                id=series_id,
                label=_require_text(item.get("label"), f"homepage chart series {series_id}.label"),
                values=values,
            )
        )
    _unique([item.id for item in series], "homepage chart series ids")
    chart = FeaturedChart(
        title=_require_text(raw_chart.get("title"), "homepage featured.chart.title"),
        description=_require_text(
            raw_chart.get("description"), "homepage featured.chart.description"
        ),
        source_note=_require_text(
            raw_chart.get("source_note"), "homepage featured.chart.source_note"
        ),
        bins=bins,
        series=tuple(series),
    )
    featured = FeaturedHighlight(
        report=featured_report_id,
        experiment=featured_experiment_id,
        decision_label=_require_text(
            raw_featured.get("decision_label"), "homepage featured.decision_label"
        ),
        decision_summary=_require_text(
            raw_featured.get("decision_summary"), "homepage featured.decision_summary"
        ),
        gates=tuple(gates),
        chart=chart,
    )

    raw_rejections = raw.get("rejected_ideas")
    if not isinstance(raw_rejections, list) or not raw_rejections:
        raise CatalogError(f"{path} must define a non-empty rejected_ideas list")
    rejected_ideas: list[RejectedIdea] = []
    for index, item in enumerate(raw_rejections):
        if not isinstance(item, dict):
            raise CatalogError(f"homepage rejected_ideas[{index}] must be a mapping")
        title = _require_text(item.get("title"), f"homepage rejected_ideas[{index}].title")
        experiment_id = _require_slug(item.get("experiment"), f"rejected idea {title}.experiment")
        experiment = experiment_by_id.get(experiment_id)
        if experiment is None:
            raise CatalogError(f"rejected idea {title} references unknown experiment {experiment_id}")
        raw_metric_ids = item.get("metric_ids", [])
        if not isinstance(raw_metric_ids, list):
            raise CatalogError(f"rejected idea {title}.metric_ids must be a list")
        metric_ids = tuple(
            _require_slug(value, f"rejected idea {title}.metric_ids[{metric_index}]")
            for metric_index, value in enumerate(raw_metric_ids)
        )
        available_metric_ids = {metric.id for metric in experiment.metrics}
        unknown_metric_ids = [value for value in metric_ids if value not in available_metric_ids]
        if unknown_metric_ids:
            raise CatalogError(
                f"rejected idea {title} references unknown metrics in {experiment_id}: "
                + ", ".join(unknown_metric_ids)
            )
        rejected_ideas.append(
            RejectedIdea(
                title=title,
                state=_require_text(item.get("state"), f"rejected idea {title}.state"),
                reason=_require_text(item.get("reason"), f"rejected idea {title}.reason"),
                experiment=experiment_id,
                metric_ids=metric_ids,
            )
        )
    _unique([item.title for item in rejected_ideas], "homepage rejected idea titles")

    return HomepageHighlights(
        metrics=tuple(metrics),
        featured=featured,
        rejected_ideas=tuple(rejected_ideas),
    )


def related_project_ids(
    item: dict[str, Any], primary: str, projects: dict[str, Project],
) -> tuple[str, ...]:
    # Validate shared ownership without changing the canonical URL owner.
    values = _require_text_list(item.get("related_project_ids", []), "related_project_ids")
    _unique([primary, *values], "project associations")
    for project_id in values:
        if project_id not in projects or projects[project_id].section == "knowledge":
            raise CatalogError(f"unknown research/infrastructure project association {project_id}")
    return values


def parse_arms(item: dict[str, Any], experiment_id: str) -> tuple[ExperimentArm, ...]:
    # Keep matched comparisons local to their explicit evaluation contract.
    arms = tuple(
        ExperimentArm(
            id=_require_slug(arm["id"], "comparison arm id"),
            label=_require_text(arm["label"], "comparison arm label"),
            status=_require_slug(arm["status"], "comparison arm status"),
            model=_require_text(arm["model"], "comparison arm model"),
            metrics=parse_metrics(arm["metrics"], f"{experiment_id}/{arm['id']}"),
        )
        for arm in item.get("arms", [])
    )
    _unique([arm.id for arm in arms], f"arms in {experiment_id}")
    if arms and not item.get("comparison_scope"):
        raise CatalogError(f"experiment {experiment_id} requires comparison_scope for arms")
    for arm in arms:
        if arm.status not in {"completed", "failed-before-test", "gated"}:
            raise CatalogError(f"unknown arm status {arm.status}")
        if arm.status != "completed" and arm.metrics:
            raise CatalogError(f"non-completed arm {arm.id} must not contain comparison metrics")
    return arms


def parse_figures(
    item: dict[str, Any], report_ids: tuple[str, ...], reports: dict[str, Report],
) -> tuple[ResearchFigure, ...]:
    # Resolve figure references only within explicitly linked publications.
    figures: list[ResearchFigure] = []
    for value in item.get("figures", []):
        report_id = value["report_id"]
        if report_id not in report_ids:
            raise CatalogError(f"figure source {report_id} is not linked to its experiment")
        asset, image_index = value.get("asset"), value.get("image_index")
        if reports[report_id].is_markdown:
            if image_index is not None or asset is None:
                raise CatalogError("Markdown figure requires an asset path")
            asset = _require_relative_reference(asset, "figure asset")
            if not asset.startswith("images/"):
                raise CatalogError("figure asset must be inside its report images directory")
        elif asset is not None or type(image_index) is not int or image_index < 0:
            raise CatalogError("legacy figure requires a nonnegative image_index")
        figures.append(ResearchFigure(report_id, _require_text(value["title"], "figure title"), asset, image_index))
    _unique([(f.report_id, f.asset, f.image_index) for f in figures], "figure references")
    return tuple(figures)


def load_studies(
    path: Path, projects: tuple[Project, ...], experiments: tuple[Experiment, ...],
    reports: tuple[Report, ...], taxonomy: tuple[ResearchTaxonomyStage, ...],
) -> tuple[Study, ...]:
    # Validate one record per research question and all many-to-many links.
    values = _load_yaml(path, supported_versions=(2,))["studies"]
    project_by_id = {p.id: p for p in projects if p.section != "knowledge"}
    experiment_by_id = {e.id: e for e in experiments}
    report_by_id = {r.id: r for r in reports}
    studies: list[Study] = []
    for value in values:
        study_id = _require_slug(value["id"], "study id")
        project_ids = _require_text_list(value["project_ids"], f"study {study_id} projects")
        experiment_ids = _require_text_list(value["experiment_ids"], f"study {study_id} experiments")
        report_ids = _require_text_list(value["report_ids"], f"study {study_id} reports")
        for label, ids, registry in (
            ("projects", project_ids, project_by_id),
            ("experiments", experiment_ids, experiment_by_id),
            ("reports", report_ids, report_by_id),
        ):
            _unique(list(ids), f"{label} in study {study_id}")
            for identity in ids:
                if identity not in registry:
                    raise CatalogError(f"study {study_id} references unknown {label} {identity}")
        if not project_ids or not (experiment_ids or report_ids):
            raise CatalogError(f"study {study_id} needs projects and experiment/report evidence")
        evidence_records = [experiment_by_id[eid] for eid in experiment_ids]
        evidence_records.extend(report_by_id[rid] for rid in report_ids)
        for evidence in evidence_records:
            if not set(evidence.project_ids).intersection(project_ids):
                raise CatalogError(f"study {study_id} evidence {evidence.id} has no associated project")

        # Research uses problem taxonomy; infrastructure keeps its own organization.
        path_value = value.get("taxonomy_path")
        taxonomy_path = () if path_value is None else _require_taxonomy_path(path_value, "study taxonomy_path")
        research = any(project_by_id[pid].section == "research" for pid in project_ids)
        if research and not taxonomy_path_exists(taxonomy, taxonomy_path):
            raise CatalogError(f"study {study_id} requires a valid research taxonomy path")
        if not research and taxonomy_path:
            raise CatalogError(f"infrastructure study {study_id} must not declare prediction taxonomy")
        studies.append(Study(
            id=study_id, title=_require_text(value["title"], "study title"),
            question=_require_text(value["question"], "study question"),
            conclusion=_require_text(value["conclusion"], "study conclusion"),
            caveats=_require_text_list(value["caveats"], "study caveats"),
            project_ids=project_ids, experiment_ids=experiment_ids,
            report_ids=report_ids, taxonomy_path=taxonomy_path,
        ))
    _unique([s.id for s in studies], "study ids")
    linked = {eid for s in studies for eid in s.experiment_ids}
    missing = set(experiment_by_id) - linked
    if missing:
        raise CatalogError(f"experiments without a research question: {sorted(missing)}")
    return tuple(studies)


def load_catalog(content_root: Path) -> Catalog:
    """Load the canonical project, question, experiment, and publication graph."""
    # Validate independent content registries before joining their identities.
    research_stages = _load_research_flow(content_root / "research-flow.yaml")
    research_taxonomy = _load_research_taxonomy(
        content_root / "research-taxonomy.yaml", research_stages
    )
    categories, projects = _load_projects(
        content_root / "projects.yaml", research_stages, research_taxonomy
    )
    reports, featured_report_id = _load_reports(
        content_root / "reports.yaml", projects, research_stages
    )
    experiments = _load_experiments(
        content_root / "experiments.yaml", projects, reports, research_taxonomy
    )
    studies = load_studies(content_root / "studies.yaml", projects, experiments, reports, research_taxonomy)
    catalog = Catalog(
        categories=categories,
        research_stages=research_stages,
        research_taxonomy=research_taxonomy,
        projects=projects,
        reports=reports,
        experiments=experiments,
        studies=studies,
        featured_report_id=featured_report_id,
    )
    from research_site.knowledge import load_knowledge
    from research_site.knowledge_sync import KnowledgeSyncError

    try:
        knowledge = load_knowledge(
            content_root / "knowledge" / "deep-ml",
            content_root / "knowledge" / "quant-knowledge",
            content_root / "knowledge" / "ontology.yaml",
        )
    except KnowledgeSyncError as exc:
        raise CatalogError(str(exc)) from exc
    return Catalog(
        categories=catalog.categories,
        research_stages=catalog.research_stages,
        research_taxonomy=catalog.research_taxonomy,
        projects=catalog.projects,
        reports=catalog.reports,
        experiments=catalog.experiments,
        studies=catalog.studies,
        featured_report_id=catalog.featured_report_id,
        homepage=_load_homepage(content_root / "highlights.yaml", catalog),
        knowledge=knowledge,
    )
