from pathlib import Path

from research_site.audit import audit_report_ownership
from research_site.catalog import load_catalog


SITE_ROOT = Path(__file__).resolve().parents[1]


def test_audit_uses_manifest_for_selected_report() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    matches = audit_report_ownership(
        catalog,
        Path.home(),
        Path.home() / "0-report-html",
        Path.home() / "exp-nn/all-experiments-research-report/report/report-catalog.json",
    )
    by_name = {match.source_file: match for match in matches}
    assert by_name["0502-index-6backtest.html"].project == "index500-predict"
    assert by_name["0702-13_l2_ablation_vs_baseline_comparison_report.html"].subproject == "l2-features"
    assert by_name["0731-limit-report.html"].project == "limit-0729"
