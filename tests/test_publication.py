from datetime import date
from hashlib import sha256
from pathlib import Path

import pytest

from research_site.catalog import Catalog, CatalogError, Report, load_catalog
from research_site.publication import (
    publish_reports,
    sanitize_report,
    validate_public_reports,
)

SITE_ROOT = Path(__file__).resolve().parents[1]


def _publish_test_report(tmp_path: Path, data: bytes) -> None:
    archive_root = tmp_path / "archive"
    archive_root.mkdir()
    (archive_root / "report.html").write_bytes(data)
    report = Report(
        id="test-report",
        project="test-project",
        title="Test report",
        source_file="report.html",
        date=date(2026, 8, 2),
        summary="Test report",
        tags=(),
        featured=False,
        match_method="manual",
        match_evidence="test-project/report.html",
        source_sha256=sha256(data).hexdigest(),
    )
    catalog = Catalog(categories=(), projects=(), reports=(report,))
    publish_reports(catalog, archive_root, tmp_path / "public")


def test_sanitize_report_redacts_local_roots() -> None:
    source = b"/home/maomao/project/a /data-cache/nn/run http://127.0.0.1:5000  \n"
    public = sanitize_report(source)
    assert b"/home/" not in public
    assert b"/data-cache/" not in public
    assert public == b"[local-workspace]/project/a [artifact-root]/nn/run [local-service]:5000\n"


def test_committed_public_reports_are_safe() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    results = validate_public_reports(catalog, SITE_ROOT / "public" / "reports")
    assert {result.report_id for result in results} == {
        report.id for report in catalog.reports if not report.is_markdown
    }
    assert all(len(result.published_sha256) == 64 for result in results)


def test_public_report_path_leak_is_rejected(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    report = catalog.reports[0]
    destination = tmp_path / report.project / report.id / "index.html"
    destination.parent.mkdir(parents=True)
    destination.write_text("<html>/home/maomao/private</html>", encoding="utf-8")
    with pytest.raises(CatalogError, match="home-directory"):
        validate_public_reports(catalog, tmp_path)


@pytest.mark.parametrize(
    "resource",
    [
        b'<img srcset="https://example.com/image.png 1x">',
        b"<style>body { background: url(https://example.com/image.png); }</style>",
        b'<object data="assets/chart.svg"></object>',
        b'<svg><use href="https://example.com/icons.svg#chart"></use></svg>',
        b'<meta http-equiv="refresh" content="0; url=https://example.com/report">',
    ],
)
def test_external_rendering_resources_are_rejected(tmp_path: Path, resource: bytes) -> None:
    with pytest.raises(CatalogError, match="external rendering resource"):
        _publish_test_report(tmp_path, b"<html>" + resource + b"</html>")


@pytest.mark.parametrize(
    "credential",
    [
        b"github_pat_" + b"A" * 30,
        b"-----BEGIN PRIVATE KEY-----",
    ],
)
def test_credential_like_values_are_rejected(tmp_path: Path, credential: bytes) -> None:
    with pytest.raises(CatalogError, match="credential-like"):
        _publish_test_report(tmp_path, b"<html>" + credential + b"</html>")
