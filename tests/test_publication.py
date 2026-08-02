from hashlib import sha256
from pathlib import Path

import pytest

from research_site.catalog import CatalogError, load_catalog
from research_site.publication import sanitize_report, validate_public_reports


SITE_ROOT = Path(__file__).resolve().parents[1]


def test_sanitize_report_redacts_local_roots() -> None:
    source = b"/home/maomao/project/a /data-cache/nn/run http://127.0.0.1:5000  \n"
    public = sanitize_report(source)
    assert b"/home/" not in public
    assert b"/data-cache/" not in public
    assert public == b"[local-workspace]/project/a [artifact-root]/nn/run [local-service]:5000\n"


def test_committed_public_reports_are_safe() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    results = validate_public_reports(catalog, SITE_ROOT / "public" / "reports")
    assert {result.report_id for result in results} == {report.id for report in catalog.reports}
    assert all(len(result.published_sha256) == 64 for result in results)


def test_public_report_path_leak_is_rejected(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    report = catalog.reports[0]
    destination = tmp_path / report.project / report.id / "index.html"
    destination.parent.mkdir(parents=True)
    destination.write_text("<html>/home/maomao/private</html>", encoding="utf-8")
    with pytest.raises(CatalogError, match="home-directory"):
        validate_public_reports(catalog, tmp_path)
