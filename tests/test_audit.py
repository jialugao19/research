from pathlib import Path

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
    catalog = load_catalog(SITE_ROOT / "content")
    matches = audit_report_ownership(
        catalog,
        tmp_path / "workspace",
        archive_root,
        tmp_path / "report-catalog.json",
    )
    by_name = {match.source_file: match for match in matches}
    assert by_name["0502-index-6backtest.html"].project == "index500-predict"
    assert by_name["0702-13_l2_ablation_vs_baseline_comparison_report.html"].subproject is None
    assert by_name["0731-limit-report.html"].project == "limit-0729"
