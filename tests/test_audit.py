from pathlib import Path

import pytest
import yaml

from research_site.audit import audit_report_ownership
from research_site.catalog import load_catalog


SITE_ROOT = Path(__file__).resolve().parents[1]


def test_audit_uses_manifest_for_selected_report(tmp_path: Path) -> None:
    # Build the smallest archive fixture needed to exercise manual ownership.
    archive_root = tmp_path / "archive"
    archive_root.mkdir()
    for filename in (
        "0502-index-6backtest.html",
        "0702-13_l2_ablation_vs_baseline_comparison_report.html",
        "0731-limit-report.html",
    ):
        (archive_root / filename).write_text(filename, encoding="utf-8")

    # Audit the fixture without relying on machine-local research archives.
    registry_root = tmp_path / "registry"
    registry_root.mkdir()
    (registry_root / "report-index.yaml").write_text("reports: []\n", encoding="utf-8")
    catalog = load_catalog(SITE_ROOT / "content")
    matches = audit_report_ownership(
        catalog,
        tmp_path / "workspace",
        archive_root,
        registry_root,
    )
    by_name = {match.source_file: match for match in matches}
    assert by_name["0502-index-6backtest.html"].project == "index500-predict"
    assert by_name["0702-13_l2_ablation_vs_baseline_comparison_report.html"].subproject is None
    assert by_name["0731-limit-report.html"].project == "limit-0729"


@pytest.mark.parametrize("source_key", ["path", "repo_mirror_path"])
def test_audit_matches_registered_external_report(tmp_path: Path, source_key: str) -> None:
    # Keep report artifacts outside the workspace and omit the retired checkout.
    archive_root = tmp_path / "archive"
    archive_root.mkdir()
    artifact = tmp_path / "data-cache" / "run" / "report.html"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("<html>registered report</html>", encoding="utf-8")
    (archive_root / "registered.html").write_bytes(artifact.read_bytes())
    (archive_root / "different.html").write_text("different bytes", encoding="utf-8")

    # A missing primary location does not invalidate an existing registered mirror.
    registry_root = tmp_path / "relocated-repo" / "registry"
    registry_root.mkdir(parents=True)
    report = {
        "id": "baseline-report", "experiment_id": "reference-baseline",
        "status": "missing", "path": str(tmp_path / "missing.html"),
        source_key: str(artifact),
    }
    (registry_root / "report-index.yaml").write_text(
        yaml.safe_dump({"reports": [report]}), encoding="utf-8",
    )

    # Match exact bytes and emit logical evidence independent of machine paths.
    matches = audit_report_ownership(
        load_catalog(SITE_ROOT / "content"), tmp_path / "workspace",
        archive_root, registry_root,
    )
    by_name = {match.source_file: match for match in matches}
    assert by_name["registered.html"].project == "prediction-nn-1min"
    assert by_name["registered.html"].subproject == "reference-baseline"
    assert by_name["registered.html"].match_method == "sha256"
    assert by_name["registered.html"].evidence == ("nn-registry/reference-baseline/baseline-report",)
    assert by_name["different.html"].project is None


def test_registry_matches_preserve_approved_ownership(tmp_path: Path) -> None:
    # Give identical bytes to an approved report and two different NN projects.
    archive_root = tmp_path / "archive"
    archive_root.mkdir()
    artifact = tmp_path / "report.html"
    artifact.write_text("identical report bytes", encoding="utf-8")
    for name in ("0502-index-6backtest.html", "ambiguous.html"):
        (archive_root / name).write_bytes(artifact.read_bytes())
    registry_root = tmp_path / "registry"
    registry_root.mkdir()
    reports = [
        {"id": experiment_id, "experiment_id": experiment_id, "path": str(artifact)}
        for experiment_id in ("reference-baseline", "baseline-1s-0720")
    ]
    (registry_root / "report-index.yaml").write_text(
        yaml.safe_dump({"reports": reports}), encoding="utf-8",
    )

    # Keep curated ownership and leave cross-project hash collisions unresolved.
    matches = audit_report_ownership(
        load_catalog(SITE_ROOT / "content"), tmp_path / "workspace",
        archive_root, registry_root,
    )
    by_name = {match.source_file: match for match in matches}
    assert by_name["0502-index-6backtest.html"].project == "index500-predict"
    assert by_name["0502-index-6backtest.html"].match_method == "manual-manifest"
    assert by_name["ambiguous.html"].project is None
    assert by_name["ambiguous.html"].subproject is None


def test_missing_registry_is_an_error(tmp_path: Path) -> None:
    # A configured registry must exist even when its artifacts have been removed.
    with pytest.raises(FileNotFoundError, match="report-index.yaml"):
        audit_report_ownership(
            load_catalog(SITE_ROOT / "content"), tmp_path / "workspace",
            tmp_path / "archive", tmp_path / "missing-registry",
        )
