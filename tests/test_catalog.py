from pathlib import Path

import pytest

from research_site.catalog import CatalogError, load_catalog


SITE_ROOT = Path(__file__).resolve().parents[1]


def _copy_catalog(tmp_path: Path) -> None:
    for name in ("projects.yaml", "studies.yaml", "reports.yaml"):
        (tmp_path / name).write_text((SITE_ROOT / "content" / name).read_text(encoding="utf-8"), encoding="utf-8")


def test_repository_catalog_is_valid() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    assert len(catalog.projects) == 16
    assert len(catalog.studies) == 38
    assert len(catalog.reports) == 6
    assert catalog.project_by_id["prediction-nn"].track("one-minute") is not None
    assert catalog.project_by_id["prediction-nn"].track("one-second") is not None
    assert catalog.project_by_id["prediction-nn"].subproject("l2-features") is not None
    assert catalog.study_by_id["baseline-1s-0720"].metrics[0].display_value == "0.09842"


def test_report_routes_are_unique() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    routes = [report.route for report in catalog.reports]
    assert len(routes) == len(set(routes))


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
    studies = studies.replace("report_ids: [0502-index-6backtest]", "report_ids: [0731-limit-t1-strategy]", 1)
    (tmp_path / "studies.yaml").write_text(studies, encoding="utf-8")
    with pytest.raises(CatalogError, match="belongs to another project"):
        load_catalog(tmp_path)
