from pathlib import Path

import pytest

from research_site.catalog import CatalogError, load_catalog


SITE_ROOT = Path(__file__).resolve().parents[1]


def test_repository_catalog_is_valid() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    assert len(catalog.projects) == 14
    assert len(catalog.reports) == 6
    assert catalog.project_by_id["prediction-nn"].subproject("l2-features") is not None


def test_report_routes_are_unique() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    routes = [report.route for report in catalog.reports]
    assert len(routes) == len(set(routes))


def test_source_file_cannot_escape_archive(tmp_path: Path) -> None:
    (tmp_path / "projects.yaml").write_text((SITE_ROOT / "content" / "projects.yaml").read_text(), encoding="utf-8")
    reports = (SITE_ROOT / "content" / "reports.yaml").read_text(encoding="utf-8")
    (tmp_path / "reports.yaml").write_text(reports.replace("0502-index-6backtest.html", "../secret.html", 1), encoding="utf-8")
    with pytest.raises(CatalogError, match="basename"):
        load_catalog(tmp_path)
