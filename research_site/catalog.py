from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path, PurePath
import re
from typing import Any

import yaml


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ALLOWED_MATCH_METHODS = {"sha256", "central-catalog", "path-evidence", "title-and-project-intent", "manual"}


class CatalogError(ValueError):
    """Raised when project or report metadata violates the public contract."""


@dataclass(frozen=True)
class Category:
    id: str
    title: str
    description: str


@dataclass(frozen=True)
class Subproject:
    id: str
    title: str


@dataclass(frozen=True)
class Project:
    id: str
    title: str
    category: str
    status: str
    description: str
    source_refs: tuple[str, ...]
    subprojects: tuple[Subproject, ...] = field(default_factory=tuple)

    def subproject(self, subproject_id: str) -> Subproject | None:
        return next((item for item in self.subprojects if item.id == subproject_id), None)


@dataclass(frozen=True)
class Report:
    id: str
    project: str
    title: str
    source_file: str
    date: date
    summary: str
    tags: tuple[str, ...]
    featured: bool
    match_method: str
    match_evidence: str
    source_sha256: str
    subproject: str | None = None

    @property
    def display_date(self) -> str:
        return self.date.isoformat()

    @property
    def route(self) -> str:
        return f"reports/{self.project}/{self.id}/"


@dataclass(frozen=True)
class Catalog:
    categories: tuple[Category, ...]
    projects: tuple[Project, ...]
    reports: tuple[Report, ...]

    @property
    def project_by_id(self) -> dict[str, Project]:
        return {project.id: project for project in self.projects}

    @property
    def category_by_id(self) -> dict[str, Category]:
        return {category.id: category for category in self.categories}

    def reports_for_project(self, project_id: str) -> list[Report]:
        return sorted(
            (report for report in self.reports if report.project == project_id),
            key=lambda report: (report.date, report.id),
            reverse=True,
        )


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CatalogError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CatalogError(f"{path} must contain a YAML mapping")
    if value.get("schema_version") != 1:
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
        raw_subprojects = item.get("subprojects", [])
        if not isinstance(raw_refs, list) or not all(isinstance(ref, str) and ref for ref in raw_refs):
            raise CatalogError(f"project {project_id} source_refs must be a list of names")
        if not isinstance(raw_subprojects, list):
            raise CatalogError(f"project {project_id} subprojects must be a list")
        subprojects: list[Subproject] = []
        for sub_index, sub in enumerate(raw_subprojects):
            if not isinstance(sub, dict):
                raise CatalogError(f"project {project_id} subprojects[{sub_index}] must be a mapping")
            subprojects.append(
                Subproject(
                    id=_require_slug(sub.get("id"), f"project {project_id} subproject id"),
                    title=_require_text(sub.get("title"), f"project {project_id} subproject title"),
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
                source_refs=tuple(raw_refs),
                subprojects=tuple(subprojects),
            )
        )
    _unique([item.id for item in projects], "project ids")
    return tuple(categories), tuple(projects)


def _load_reports(path: Path, projects: tuple[Project, ...]) -> tuple[Report, ...]:
    raw = _load_yaml(path)
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
        source_file = _require_text(item.get("source_file"), f"report {report_id}.source_file")
        if PurePath(source_file).name != source_file or Path(source_file).suffix.lower() != ".html":
            raise CatalogError(f"report {report_id} source_file must be a basename ending in .html")
        tags = item.get("tags", [])
        if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
            raise CatalogError(f"report {report_id} tags must be a list of text")
        match_method = _require_text(item.get("match_method"), f"report {report_id}.match_method")
        if match_method not in ALLOWED_MATCH_METHODS:
            raise CatalogError(f"report {report_id} has unsupported match_method {match_method}")
        source_sha256 = _require_text(item.get("source_sha256"), f"report {report_id}.source_sha256")
        if not SHA256_RE.fullmatch(source_sha256):
            raise CatalogError(f"report {report_id} source_sha256 must be lowercase SHA-256")
        reports.append(
            Report(
                id=report_id,
                project=project_id,
                subproject=subproject,
                title=_require_text(item.get("title"), f"report {report_id}.title"),
                source_file=source_file,
                date=_parse_date(item.get("date"), f"report {report_id}.date"),
                summary=_require_text(item.get("summary"), f"report {report_id}.summary"),
                tags=tuple(tag.strip() for tag in tags),
                featured=bool(item.get("featured", False)),
                match_method=match_method,
                match_evidence=_require_text(item.get("match_evidence"), f"report {report_id}.match_evidence"),
                source_sha256=source_sha256,
            )
        )
    _unique([item.id for item in reports], "report ids")
    _unique([item.source_sha256 for item in reports], "report source hashes")
    return tuple(reports)


def load_catalog(content_root: Path) -> Catalog:
    """Load and validate public project and report metadata."""
    categories, projects = _load_projects(content_root / "projects.yaml")
    reports = _load_reports(content_root / "reports.yaml", projects)
    return Catalog(categories=categories, projects=projects, reports=reports)
