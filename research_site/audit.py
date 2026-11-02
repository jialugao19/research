from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from hashlib import sha256
import os
from pathlib import Path

import yaml

from research_site.catalog import Catalog


SKIP_DIRECTORIES = {
    ".git",
    ".cache",
    ".pytest_cache",
    "node_modules",
    "all-experiments-research-report",
    "0-select&report",
}


@dataclass(frozen=True)
class AuditMatch:
    source_file: str
    source_sha256: str
    project: str | None
    subproject: str | None
    match_method: str
    evidence: tuple[str, ...]


@dataclass(frozen=True)
class AuditSource:
    project: str
    evidence: str
    experiment_id: str | None


def _hash(path: Path) -> str:
    # Hash source bytes without loading whole reports into memory.
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _html_files(root: Path, max_bytes: int) -> list[Path]:
    if not root.is_dir():
        return []
    result: list[Path] = []
    for base, directories, files in os.walk(root):
        directories[:] = [name for name in directories if name not in SKIP_DIRECTORIES]
        for filename in files:
            path = Path(base) / filename
            if path.suffix.lower() != ".html":
                continue
            try:
                if path.stat().st_size <= max_bytes:
                    result.append(path)
            except OSError:
                continue
    return result


def _registry_reports_by_hash(
    catalog: Catalog, registry_root: Path, max_bytes: int,
) -> dict[str, list[AuditSource]]:
    # Resolve project ownership from explicit experiment identifiers.
    owners = {
        experiment_id: project.id
        for project in catalog.projects
        for experiment_id in project.registry_experiments
    }
    report_index = yaml.safe_load((registry_root / "report-index.yaml").read_text(encoding="utf-8"))
    result: dict[str, list[AuditSource]] = defaultdict(list)
    for report in report_index["reports"]:
        experiment_id = report["experiment_id"]
        if experiment_id not in owners:
            continue

        # Inspect registered primary and mirror files; missing artifacts are expected.
        for key in ("path", "repo_mirror_path"):
            if key not in report:
                continue
            path = Path(report[key])
            if path.suffix.lower() not in {".html", ".mhtml"} or not path.is_file():
                continue
            if path.stat().st_size > max_bytes:
                continue
            result[_hash(path)].append(
                AuditSource(
                    project=owners[experiment_id],
                    evidence=f"nn-registry/{experiment_id}/{report['id']}",
                    experiment_id=experiment_id,
                )
            )
    return result


def audit_report_ownership(
    catalog: Catalog,
    workspace_root: Path,
    archive_root: Path,
    registry_root: Path,
    max_bytes: int = 25 * 1024 * 1024,
) -> list[AuditMatch]:
    """Match archive reports to current projects without modifying either source."""
    # Discover workspace reports and explicitly registered external artifacts.
    current_by_hash: dict[str, list[AuditSource]] = defaultdict(list)
    for project in catalog.projects:
        for source_ref in project.source_refs:
            for path in _html_files(workspace_root / source_ref, max_bytes=max_bytes):
                current_by_hash[_hash(path)].append(
                    AuditSource(project.id, str(path.relative_to(workspace_root)), None)
                )
    registry_by_hash = _registry_reports_by_hash(catalog, registry_root, max_bytes)
    manifest_by_file = {report.source_file: report for report in catalog.reports if report.source_file}
    matches: list[AuditMatch] = []
    # Preserve approved ownership and add current hash evidence.
    for source_path in sorted(archive_root.iterdir(), key=lambda path: path.name):
        if not source_path.is_file() or source_path.suffix.lower() not in {".html", ".mhtml"}:
            continue
        digest = _hash(source_path)
        evidence: list[str] = []
        project: str | None = None
        subproject: str | None = None
        match_method = "unassigned"
        manifest_report = manifest_by_file.get(source_path.name)
        if manifest_report is not None:
            project = manifest_report.project
            match_method = "manual-manifest"
            evidence.append(manifest_report.match_evidence)
        exact = current_by_hash.get(digest, []) + registry_by_hash.get(digest, [])
        if exact:
            exact_projects = sorted({source.project for source in exact})
            if project is None and len(exact_projects) == 1:
                project = exact_projects[0]
                match_method = "sha256"
            experiment_ids = {
                source.experiment_id for source in exact
                if source.project == project and source.experiment_id is not None
            }
            if len(experiment_ids) == 1:
                subproject = next(iter(experiment_ids))
            evidence.extend(source.evidence for source in exact)
        matches.append(
            AuditMatch(
                source_file=source_path.name,
                source_sha256=digest,
                project=project,
                subproject=subproject,
                match_method=match_method,
                evidence=tuple(dict.fromkeys(evidence)),
            )
        )
    return matches


def audit_payload(matches: list[AuditMatch]) -> dict[str, object]:
    assigned = sum(match.project is not None for match in matches)
    return {
        "schema_version": 1,
        "report_count": len(matches),
        "assigned_count": assigned,
        "unassigned_count": len(matches) - assigned,
        "reports": [asdict(match) for match in matches],
    }
