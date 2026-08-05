import shutil
from pathlib import Path

import pytest

from research_site.catalog import CatalogError, load_catalog

SITE_ROOT = Path(__file__).resolve().parents[1]


def _copy_catalog(tmp_path: Path) -> None:
    for name in ("projects.yaml", "studies.yaml", "reports.yaml"):
        (tmp_path / name).write_text((SITE_ROOT / "content" / name).read_text(encoding="utf-8"), encoding="utf-8")
    shutil.copytree(SITE_ROOT / "content" / "report-docs", tmp_path / "report-docs")


def test_repository_catalog_is_valid() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    assert len(catalog.projects) == 17
    assert len(catalog.studies) == 39
    assert len(catalog.reports) == 13
    assert len(catalog.current_reports) == 7
    assert catalog.featured_report_id == "0802-stock1s-gru384-v2"
    assert catalog.featured_report is catalog.report_by_id["0802-stock1s-gru384-v2"]
    assert catalog.report_by_id["0802-stock1s-gru384-v2"].revision_of == "0802-stock1s-gru384"
    assert catalog.report_by_id["0805-live-predictor-quality"].project == "live-predictor"
    assert catalog.report_by_id["0805-live-predictor-quality"].hero_image == (
        "images/extreme-tail-performance.png"
    )
    assert "tqo-data-source" not in catalog.project_by_id
    assert "tqo-reference-backend" not in catalog.study_by_id
    one_minute = catalog.project_by_id["prediction-nn"].track("one-minute")
    assert one_minute is not None
    assert len(one_minute.objective_details) == 3
    assert len(one_minute.data_structure) == 4
    assert "成本后结果" in one_minute.conclusion
    assert catalog.project_by_id["prediction-nn"].track("one-second") is not None
    assert catalog.project_by_id["prediction-nn"].subproject("l2-features").group == "特征扩展与组合验证"
    assert catalog.study_by_id["baseline-1s-0720"].metrics[0].display_value == "0.09842"


def test_report_routes_are_unique() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    routes = [report.route for report in catalog.reports]
    assert len(routes) == len(set(routes))


def test_featured_report_must_be_current(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    reports = (tmp_path / "reports.yaml").read_text(encoding="utf-8")
    reports = reports.replace(
        "featured_report: 0802-stock1s-gru384-v2",
        "featured_report: 0802-stock1s-gru384",
        1,
    )
    (tmp_path / "reports.yaml").write_text(reports, encoding="utf-8")
    with pytest.raises(CatalogError, match="must select a current report"):
        load_catalog(tmp_path)


def test_report_bundle_hash_is_immutable(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    report_path = tmp_path / "report-docs" / "index500-predict" / "0502-index-6backtest-v2" / "report.md"
    report_path.write_text(report_path.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
    with pytest.raises(CatalogError, match="bundle checksum changed"):
        load_catalog(tmp_path)


def test_report_hero_image_must_be_a_referenced_bundle_image(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    reports = (tmp_path / "reports.yaml").read_text(encoding="utf-8")
    reports = reports.replace(
        "hero_image: images/extreme-tail-performance.png",
        "hero_image: images/missing.png",
        1,
    )
    (tmp_path / "reports.yaml").write_text(reports, encoding="utf-8")
    with pytest.raises(CatalogError, match="must reference an image used by the report"):
        load_catalog(tmp_path)


def test_revision_must_keep_ownership(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    reports = (tmp_path / "reports.yaml").read_text(encoding="utf-8")
    reports = reports.replace(
        "revision_of: 0731-limit-t1-strategy",
        "revision_of: 0502-index-6backtest",
        1,
    )
    (tmp_path / "reports.yaml").write_text(reports, encoding="utf-8")
    with pytest.raises(CatalogError, match="must keep project and subproject ownership"):
        load_catalog(tmp_path)


def test_source_file_cannot_escape_archive(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    reports = (SITE_ROOT / "content" / "reports.yaml").read_text(encoding="utf-8")
    (tmp_path / "reports.yaml").write_text(reports.replace("0502-index-6backtest.html", "../secret.html", 1), encoding="utf-8")
    with pytest.raises(CatalogError, match="basename"):
        load_catalog(tmp_path)


def test_source_ref_cannot_escape_workspace(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    projects = (SITE_ROOT / "content" / "projects.yaml").read_text(encoding="utf-8")
    projects = projects.replace("source_refs: [prediction-NN-main, exp-nn]", "source_refs: [../prediction-NN-main]", 1)
    (tmp_path / "projects.yaml").write_text(projects, encoding="utf-8")
    with pytest.raises(CatalogError, match="relative without parent traversal"):
        load_catalog(tmp_path)


def test_match_evidence_must_be_relative(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    reports = (SITE_ROOT / "content" / "reports.yaml").read_text(encoding="utf-8")
    reports = reports.replace(
        "match_evidence: index500-predict/report/0502/index.html",
        "match_evidence: /home/maomao/index500-predict/report/0502/index.html",
        1,
    )
    (tmp_path / "reports.yaml").write_text(reports, encoding="utf-8")
    with pytest.raises(CatalogError, match="relative without parent traversal"):
        load_catalog(tmp_path)


def test_study_track_must_match_subproject(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    studies = (tmp_path / "studies.yaml").read_text(encoding="utf-8")
    studies = studies.replace("track: one-minute\n    subproject: reference-baseline", "track: one-second\n    subproject: reference-baseline", 1)
    (tmp_path / "studies.yaml").write_text(studies, encoding="utf-8")
    with pytest.raises(CatalogError, match="track must match subproject"):
        load_catalog(tmp_path)


def test_study_report_must_belong_to_same_project(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    studies = (tmp_path / "studies.yaml").read_text(encoding="utf-8")
    studies = studies.replace(
        "report_ids: [0502-index-6backtest-v2]",
        "report_ids: [0731-limit-t1-strategy-v2]",
        1,
    )
    (tmp_path / "studies.yaml").write_text(studies, encoding="utf-8")
    with pytest.raises(CatalogError, match="belongs to another project"):
        load_catalog(tmp_path)
