from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path, PurePath
from typing import Any

import yaml

from .report_content import ReportContentError, load_report_source

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_MATCH_METHODS = {"sha256", "central-catalog", "path-evidence", "title-and-project-intent", "manual"}
ALLOWED_STUDY_STATUSES = {"doing", "completed", "archived"}
ALLOWED_MATURITIES = {"decision-ready", "signal-only", "developmental", "diagnostic", "blocked", "archived"}
ALLOWED_METRIC_FORMATS = {"decimal", "percent", "integer", "number", "bps"}


class CatalogError(ValueError):
    """Raised when project or report metadata violates the public contract."""


@dataclass(frozen=True)
class Category:
    id: str
    title: str
    description: str


@dataclass(frozen=True)
class Track:
    id: str
    title: str
    description: str
    objective: str
    objective_details: tuple[str, ...]
    data_structure: tuple[str, ...]
    conclusion: str


@dataclass(frozen=True)
class Subproject:
    id: str
    title: str
    track: str
    group: str
    description: str
    objective: str


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
    tracks: tuple[Track, ...] = field(default_factory=tuple)
    subprojects: tuple[Subproject, ...] = field(default_factory=tuple)

    def track(self, track_id: str) -> Track | None:
        return next((item for item in self.tracks if item.id == track_id), None)

    def subproject(self, subproject_id: str) -> Subproject | None:
        return next((item for item in self.subprojects if item.id == subproject_id), None)

    def subprojects_for_track(self, track_id: str) -> tuple[Subproject, ...]:
        return tuple(item for item in self.subprojects if item.track == track_id)


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
class Study:
    id: str
    project: str
    title: str
    status: str
    maturity: str
    updated_at: date
    objective: str
    summary: str
    decision: str
    caveats: tuple[str, ...]
    metrics: tuple[Metric, ...]
    report_ids: tuple[str, ...]
    evidence_ref: str
    featured: bool
    track: str | None = None
    subproject: str | None = None

    @property
    def display_date(self) -> str:
        return self.updated_at.isoformat()


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
    subproject: str | None = None
    format: str = "legacy-html"
    source_file: str | None = None
    source_sha256: str | None = None
    content_file: str | None = None
    bundle_sha256: str | None = None
    hero_image: str | None = None
    revision_of: str | None = None

    @property
    def display_date(self) -> str:
        return self.date.isoformat()

    @property
    def route(self) -> str:
        return f"reports/{self.project}/{self.id}/"

    @property
    def is_markdown(self) -> bool:
        return self.format == "markdown"


@dataclass(frozen=True)
class Catalog:
    categories: tuple[Category, ...]
    projects: tuple[Project, ...]
    reports: tuple[Report, ...]
    studies: tuple[Study, ...] = field(default_factory=tuple)

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
    def study_by_id(self) -> dict[str, Study]:
        return {study.id: study for study in self.studies}

    @property
    def current_reports(self) -> tuple[Report, ...]:
        superseded = {report.revision_of for report in self.reports if report.revision_of}
        return tuple(report for report in self.reports if report.id not in superseded)

    def reports_for_project(self, project_id: str) -> list[Report]:
        return sorted(
            (report for report in self.current_reports if report.project == project_id),
            key=lambda report: (report.date, report.id),
            reverse=True,
        )

    def all_reports_for_project(self, project_id: str) -> list[Report]:
        return sorted(
            (report for report in self.reports if report.project == project_id),
            key=lambda report: (report.date, report.id),
            reverse=True,
        )

    def studies_for_project(self, project_id: str) -> list[Study]:
        return sorted(
            (study for study in self.studies if study.project == project_id),
            key=lambda study: (study.updated_at, study.id),
            reverse=True,
        )

    def studies_for_track(self, project_id: str, track_id: str) -> list[Study]:
        return [study for study in self.studies_for_project(project_id) if study.track == track_id]

    def studies_for_subproject(self, project_id: str, subproject_id: str) -> list[Study]:
        return [study for study in self.studies_for_project(project_id) if study.subproject == subproject_id]


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


def _load_projects(path: Path) -> tuple[tuple[Category, ...], tuple[Project, ...]]:
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
        category = _require_slug(item.get("category"), f"projects[{index}].category")
        if category not in category_ids:
            raise CatalogError(f"project {project_id} references unknown category {category}")
        raw_refs = item.get("source_refs", [])
        raw_tracks = item.get("tracks", [])
        raw_subprojects = item.get("subprojects", [])
        if not isinstance(raw_refs, list):
            raise CatalogError(f"project {project_id} source_refs must be a list of names")
        source_refs = tuple(
            _require_relative_reference(ref, f"project {project_id} source_refs[{ref_index}]")
            for ref_index, ref in enumerate(raw_refs)
        )
        if not isinstance(raw_tracks, list):
            raise CatalogError(f"project {project_id} tracks must be a list")
        tracks: list[Track] = []
        for track_index, track in enumerate(raw_tracks):
            if not isinstance(track, dict):
                raise CatalogError(f"project {project_id} tracks[{track_index}] must be a mapping")
            tracks.append(
                Track(
                    id=_require_slug(track.get("id"), f"project {project_id} track id"),
                    title=_require_text(track.get("title"), f"project {project_id} track title"),
                    description=_require_text(track.get("description"), f"project {project_id} track description"),
                    objective=_require_text(track.get("objective"), f"project {project_id} track objective"),
                    objective_details=_require_text_list(
                        track.get("objective_details"), f"project {project_id} track objective_details"
                    ),
                    data_structure=_require_text_list(
                        track.get("data_structure"), f"project {project_id} track data_structure"
                    ),
                    conclusion=_require_text(
                        track.get("conclusion"), f"project {project_id} track conclusion"
                    ),
                )
            )
        _unique([track.id for track in tracks], f"track ids in {project_id}")
        track_ids = {track.id for track in tracks}
        if not isinstance(raw_subprojects, list):
            raise CatalogError(f"project {project_id} subprojects must be a list")
        subprojects: list[Subproject] = []
        for sub_index, sub in enumerate(raw_subprojects):
            if not isinstance(sub, dict):
                raise CatalogError(f"project {project_id} subprojects[{sub_index}] must be a mapping")
            track = _require_slug(sub.get("track"), f"project {project_id} subproject track")
            if track not in track_ids:
                raise CatalogError(f"project {project_id} subproject references unknown track {track}")
            subprojects.append(
                Subproject(
                    id=_require_slug(sub.get("id"), f"project {project_id} subproject id"),
                    title=_require_text(sub.get("title"), f"project {project_id} subproject title"),
                    track=track,
                    group=_require_text(sub.get("group"), f"project {project_id} subproject group"),
                    description=_require_text(sub.get("description"), f"project {project_id} subproject description"),
                    objective=_require_text(sub.get("objective"), f"project {project_id} subproject objective"),
                )
            )
        _unique([sub.id for sub in subprojects], f"subproject ids in {project_id}")
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
                tracks=tuple(tracks),
                subprojects=tuple(subprojects),
            )
        )
    _unique([item.id for item in projects], "project ids")
    return tuple(categories), tuple(projects)


def _load_reports(path: Path, projects: tuple[Project, ...]) -> tuple[Report, ...]:
    raw = _load_yaml(path, supported_versions=(2,))
    raw_reports = raw.get("reports")
    if not isinstance(raw_reports, list):
        raise CatalogError(f"{path} must define a reports list")
    project_by_id = {project.id: project for project in projects}
    reports: list[Report] = []
    for index, item in enumerate(raw_reports):
        if not isinstance(item, dict):
            raise CatalogError(f"reports[{index}] must be a mapping")
        report_id = _require_slug(item.get("id"), f"reports[{index}].id")
        project_id = _require_slug(item.get("project"), f"report {report_id}.project")
        project = project_by_id.get(project_id)
        if project is None:
            raise CatalogError(f"report {report_id} references unknown project {project_id}")
        subproject_value = item.get("subproject")
        subproject = None if subproject_value is None else _require_slug(subproject_value, f"report {report_id}.subproject")
        if subproject and project.subproject(subproject) is None:
            raise CatalogError(f"report {report_id} references unknown subproject {project_id}/{subproject}")
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
            "subproject": subproject,
            "format": report_format,
            "match_method": match_method,
            "match_evidence": _require_relative_reference(
                item.get("match_evidence"), f"report {report_id}.match_evidence"
            ),
            "revision_of": revision_of,
        }
        if report_format == "legacy-html":
            source_file = _require_text(item.get("source_file"), f"report {report_id}.source_file")
            if PurePath(source_file).name != source_file or Path(source_file).suffix.lower() != ".html":
                raise CatalogError(f"report {report_id} source_file must be a basename ending in .html")
            tags = item.get("tags", [])
            if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
                raise CatalogError(f"report {report_id} tags must be a list of text")
            source_sha256 = _require_text(item.get("source_sha256"), f"report {report_id}.source_sha256")
            if not SHA256_RE.fullmatch(source_sha256):
                raise CatalogError(f"report {report_id} source_sha256 must be lowercase SHA-256")
            report = Report(
                **common,
                title=_require_text(item.get("title"), f"report {report_id}.title"),
                source_file=source_file,
                source_sha256=source_sha256,
                date=_parse_date(item.get("date"), f"report {report_id}.date"),
                summary=_require_text(item.get("summary"), f"report {report_id}.summary"),
                tags=tuple(tag.strip() for tag in tags),
                featured=bool(item.get("featured", False)),
            )
        else:
            content_file = _require_relative_reference(
                item.get("content_file"), f"report {report_id}.content_file"
            )
            expected = PurePath("report-docs") / project_id / report_id / "report.md"
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
        if predecessor.project != report.project or predecessor.subproject != report.subproject:
            raise CatalogError(f"report {report.id} revision_of must keep project and subproject ownership")
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
    return tuple(reports)


def _load_studies(
    path: Path,
    projects: tuple[Project, ...],
    reports: tuple[Report, ...],
) -> tuple[Study, ...]:
    raw = _load_yaml(path)
    raw_studies = raw.get("studies")
    if not isinstance(raw_studies, list):
        raise CatalogError(f"{path} must define a studies list")
    project_by_id = {project.id: project for project in projects}
    report_by_id = {report.id: report for report in reports}
    studies: list[Study] = []
    linked_report_ids: list[str] = []
    for index, item in enumerate(raw_studies):
        if not isinstance(item, dict):
            raise CatalogError(f"studies[{index}] must be a mapping")
        study_id = _require_slug(item.get("id"), f"studies[{index}].id")
        project_id = _require_slug(item.get("project"), f"study {study_id}.project")
        project = project_by_id.get(project_id)
        if project is None:
            raise CatalogError(f"study {study_id} references unknown project {project_id}")
        track_value = item.get("track")
        track = None if track_value is None else _require_slug(track_value, f"study {study_id}.track")
        if track and project.track(track) is None:
            raise CatalogError(f"study {study_id} references unknown track {project_id}/{track}")
        subproject_value = item.get("subproject")
        subproject = None if subproject_value is None else _require_slug(
            subproject_value, f"study {study_id}.subproject"
        )
        if subproject:
            topic = project.subproject(subproject)
            if topic is None:
                raise CatalogError(f"study {study_id} references unknown subproject {project_id}/{subproject}")
            if track != topic.track:
                raise CatalogError(f"study {study_id} track must match subproject {subproject}")
        status = _require_slug(item.get("status"), f"study {study_id}.status")
        if status not in ALLOWED_STUDY_STATUSES:
            raise CatalogError(f"study {study_id} has unsupported status {status}")
        maturity = _require_slug(item.get("maturity"), f"study {study_id}.maturity")
        if maturity not in ALLOWED_MATURITIES:
            raise CatalogError(f"study {study_id} has unsupported maturity {maturity}")
        raw_metrics = item.get("metrics", [])
        if not isinstance(raw_metrics, list):
            raise CatalogError(f"study {study_id}.metrics must be a list")
        metrics: list[Metric] = []
        for metric_index, metric in enumerate(raw_metrics):
            if not isinstance(metric, dict):
                raise CatalogError(f"study {study_id}.metrics[{metric_index}] must be a mapping")
            metric_id = _require_slug(metric.get("id"), f"study {study_id} metric id")
            metric_format = _require_slug(metric.get("format"), f"study {study_id} metric {metric_id}.format")
            if metric_format not in ALLOWED_METRIC_FORMATS:
                raise CatalogError(f"study {study_id} metric {metric_id} has unsupported format {metric_format}")
            decimals = metric.get("decimals", 0)
            if isinstance(decimals, bool) or not isinstance(decimals, int) or not 0 <= decimals <= 6:
                raise CatalogError(f"study {study_id} metric {metric_id}.decimals must be between 0 and 6")
            unit_value = metric.get("unit")
            unit = None if unit_value is None else _require_text(unit_value, f"study {study_id} metric {metric_id}.unit")
            metrics.append(
                Metric(
                    id=metric_id,
                    label=_require_text(metric.get("label"), f"study {study_id} metric {metric_id}.label"),
                    value=_require_number(metric.get("value"), f"study {study_id} metric {metric_id}.value"),
                    format=metric_format,
                    decimals=decimals,
                    context=_require_text(metric.get("context"), f"study {study_id} metric {metric_id}.context"),
                    unit=unit,
                )
            )
        _unique([metric.id for metric in metrics], f"metric ids in study {study_id}")
        raw_report_ids = item.get("report_ids", [])
        if not isinstance(raw_report_ids, list):
            raise CatalogError(f"study {study_id}.report_ids must be a list")
        report_ids = tuple(
            _require_slug(report_id, f"study {study_id}.report_ids[{report_index}]")
            for report_index, report_id in enumerate(raw_report_ids)
        )
        _unique(list(report_ids), f"report ids in study {study_id}")
        for report_id in report_ids:
            report = report_by_id.get(report_id)
            if report is None:
                raise CatalogError(f"study {study_id} references unknown report {report_id}")
            if report.project != project_id:
                raise CatalogError(f"study {study_id} report {report_id} belongs to another project")
            if subproject and report.subproject and report.subproject != subproject:
                raise CatalogError(f"study {study_id} report {report_id} belongs to another subproject")
        linked_report_ids.extend(report_ids)
        studies.append(
            Study(
                id=study_id,
                project=project_id,
                track=track,
                subproject=subproject,
                title=_require_text(item.get("title"), f"study {study_id}.title"),
                status=status,
                maturity=maturity,
                updated_at=_parse_date(item.get("updated_at"), f"study {study_id}.updated_at"),
                objective=_require_text(item.get("objective"), f"study {study_id}.objective"),
                summary=_require_text(item.get("summary"), f"study {study_id}.summary"),
                decision=_require_text(item.get("decision"), f"study {study_id}.decision"),
                caveats=_require_text_list(item.get("caveats", []), f"study {study_id}.caveats"),
                metrics=tuple(metrics),
                report_ids=report_ids,
                evidence_ref=_require_relative_reference(item.get("evidence_ref"), f"study {study_id}.evidence_ref"),
                featured=bool(item.get("featured", False)),
            )
        )
    _unique([study.id for study in studies], "study ids")
    _unique(linked_report_ids, "report links across studies")
    return tuple(studies)


def load_catalog(content_root: Path) -> Catalog:
    """Load and validate public project, study, and report metadata."""
    categories, projects = _load_projects(content_root / "projects.yaml")
    reports = _load_reports(content_root / "reports.yaml", projects)
    studies = _load_studies(content_root / "studies.yaml", projects, reports)
    return Catalog(categories=categories, projects=projects, reports=reports, studies=studies)
