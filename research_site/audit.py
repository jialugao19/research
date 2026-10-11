from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import os
from pathlib import Path

from .catalog import Catalog


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


def _hash(path: Path) -> str:
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


def _central_catalog_by_hash(path: Path) -> dict[str, list[dict[str, object]]]:
    if not path.is_file():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, list[dict[str, object]]] = defaultdict(list)
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and isinstance(item.get("sha256"), str):
                result[item["sha256"]].append(item)
    return result


def audit_report_ownership(
    catalog: Catalog,
    workspace_root: Path,
    archive_root: Path,
    central_catalog: Path,
    max_bytes: int = 25 * 1024 * 1024,
) -> list[AuditMatch]:
    """Match archive reports to current projects without modifying either source."""
    current_by_hash: dict[str, list[tuple[str, Path]]] = defaultdict(list)
    for project in catalog.projects:
        for source_ref in project.source_refs:
            for path in _html_files(workspace_root / source_ref, max_bytes=max_bytes):
                current_by_hash[_hash(path)].append((project.id, path))
    central_by_hash = _central_catalog_by_hash(central_catalog)
    manifest_by_file = {report.source_file: report for report in catalog.reports if report.source_file}
    matches: list[AuditMatch] = []
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
        exact = current_by_hash.get(digest, [])
        if exact:
            exact_projects = sorted({item[0] for item in exact})
            if len(exact_projects) == 1:
                project = exact_projects[0]
                match_method = "sha256"
            evidence.extend(str(path.relative_to(workspace_root)) for _, path in exact)
        central = central_by_hash.get(digest, [])
        if central:
            experiment_ids = sorted(
                {str(item.get("experiment_id")) for item in central if item.get("experiment_id")}
            )
            if project is None:
                project = "prediction-nn"
                subproject = experiment_ids[0] if len(experiment_ids) == 1 else None
                match_method = "central-catalog"
            evidence.extend(f"exp-nn:{experiment_id}" for experiment_id in experiment_ids)
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
