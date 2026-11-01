from base64 import b64decode
from pathlib import Path

import pytest

from research_site.report_content import (
    ReportContentError,
    load_report_source,
    render_report_source,
)

SITE_ROOT = Path(__file__).resolve().parents[1]
PNG_1X1 = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def _write_report(
    tmp_path: Path, body: str, image_names: tuple[str, ...] = ("one.png", "two.png"),
) -> Path:
    # Create only the image assets required by this fixture.
    images = tmp_path / "images"
    images.mkdir()
    for name in image_names:
        (images / name).write_bytes(PNG_1X1)
    # Write the report with the normal authoring metadata.
    report = tmp_path / "report.md"
    report.write_text(
        "---\n"
        'title: "Test"\n'
        "date: 2026-08-05\n"
        'summary: "Summary"\n'
        "tags: [test]\n"
        "featured: false\n"
        "---\n\n"
        + body,
        encoding="utf-8",
    )
    return report


def _body(images: str = '![one](images/one.png "One")\n\n![two](images/two.png "Two")') -> str:
    return (
        "## 摘要\n\nSummary.\n\n"
        "## 研究背景与目标\n\nGoal.\n\n"
        "## 数据与方法\n\nMethod.\n\n"
        f"## 主要结果\n\n{images}\n\n"
        "## 限制与适用边界\n\nLimits.\n\n"
        "## 结论\n\nConclusion.\n"
    )


def test_repository_markdown_reports_keep_all_figures() -> None:
    expected = {
        "0502-index-6backtest-v2": 6,
        "0702-l2-ablation-v2": 42,
        "0725-1min-model-screening-v2": 16,
        "0730-stock1s-feature-health-v2": 96,
        "0731-limit-t1-strategy-v2": 3,
        "0802-stock1s-gru384-v2": 3,
        "0805-live-predictor-quality": 3,
    }
    for report_id, count in expected.items():
        paths = list((SITE_ROOT / "content" / "report-docs").glob(f"*/{report_id}/report.md"))
        assert len(paths) == 1
        rendered = render_report_source(load_report_source(paths[0]))
        assert rendered.figure_count == count
        assert rendered.body_html.count("data:image/") == count


def test_consecutive_images_render_as_single_column_figures(tmp_path: Path) -> None:
    source = load_report_source(_write_report(tmp_path, _body()))
    rendered = render_report_source(source)
    assert rendered.figure_count == 2
    assert '<div class="report-figure-group">' not in rendered.body_html
    assert "图 1 · One" in rendered.body_html
    assert "图 2 · Two" in rendered.body_html


def test_tables_receive_document_order_numbers(tmp_path: Path) -> None:
    result = (
        '![one](images/one.png "One")\n\n'
        "| Metric | Value |\n| --- | ---: |\n| A | 1 |\n\n"
        "| Metric | Value |\n| --- | ---: |\n| B | 2 |\n\n"
        '![two](images/two.png "Two")'
    )
    source = load_report_source(_write_report(tmp_path, _body(result)))
    rendered = render_report_source(source)
    assert '<div class="table-caption">表 1</div>' in rendered.body_html
    assert '<div class="table-caption">表 2</div>' in rendered.body_html


def test_report_requires_fixed_section_order(tmp_path: Path) -> None:
    path = _write_report(tmp_path, _body().replace("## 数据与方法", "## 主要结果", 1))
    with pytest.raises(ReportContentError, match="H2 sections must be exactly"):
        load_report_source(path)


def test_report_rejects_raw_html_and_remote_images(tmp_path: Path) -> None:
    path = _write_report(tmp_path, _body("text with <span>unsafe</span> markup\n\n![one](images/one.png)"))
    with pytest.raises(ReportContentError, match="raw HTML"):
        load_report_source(path)


def test_report_rejects_remote_images(tmp_path: Path) -> None:
    path = _write_report(tmp_path, _body("![remote](https://example.com/x.png)"))
    with pytest.raises(ReportContentError, match="local relative file"):
        load_report_source(path)


def test_report_requires_exact_front_matter_fields(tmp_path: Path) -> None:
    path = _write_report(tmp_path, _body())
    original = path.read_text(encoding="utf-8")
    path.write_text(original.replace("tags: [test]\n", ""), encoding="utf-8")
    with pytest.raises(ReportContentError, match="front matter is missing: tags"):
        load_report_source(path)

    path.write_text(
        original.replace('summary: "Summary"\n', 'summary: "Summary"\nowner: private\n'),
        encoding="utf-8",
    )
    with pytest.raises(ReportContentError, match="front matter has unsupported fields: owner"):
        load_report_source(path)


def test_report_rejects_unreferenced_assets(tmp_path: Path) -> None:
    path = _write_report(tmp_path, _body('![one](images/one.png "One")'))
    with pytest.raises(ReportContentError, match="unreferenced image assets"):
        load_report_source(path)


def test_table_only_report_preserves_cells_and_hash(tmp_path: Path) -> None:
    # Create a valid report containing a table and no images.
    table = "| Metric | Value |\n| --- | ---: |\n| IC | -0.0123 |\n| Return | 2.50% |"
    path = _write_report(tmp_path, _body(table), image_names=())
    source = load_report_source(path)
    rendered = render_report_source(source)

    # Verify table content survives rendering and participates in the bundle hash.
    assert source.referenced_assets == ()
    assert rendered.figure_count == 0
    assert '<div class="table-caption">表 1</div>' in rendered.body_html
    assert "<td>IC</td>" in rendered.body_html
    assert "-0.0123" in rendered.body_html
    assert "2.50%" in rendered.body_html
    path.write_text(path.read_text().replace("-0.0123", "-0.0124"), encoding="utf-8")
    assert load_report_source(path).bundle_sha256 != source.bundle_sha256


@pytest.mark.parametrize("result", ["Text only.", "| Metric | Value |\n| IC | 0.1 |"])
def test_report_requires_a_real_image_or_table(tmp_path: Path, result: str) -> None:
    # Reject plain text and pipe text that does not parse as a Markdown table.
    path = _write_report(tmp_path, _body(result), image_names=())
    with pytest.raises(ReportContentError, match="at least one raster report image or Markdown table"):
        load_report_source(path)


def test_table_does_not_hide_corrupt_images(tmp_path: Path) -> None:
    # Combine a valid table with a corrupt referenced image.
    result = "| Metric | Value |\n| --- | --- |\n| IC | 0.1 |\n\n![one](images/one.png)"
    path = _write_report(tmp_path, _body(result), image_names=("one.png",))
    (tmp_path / "images" / "one.png").write_bytes(b"invalid PNG")

    # Require image validation even though the report already has a table.
    with pytest.raises(ReportContentError, match="image cannot be decoded"):
        load_report_source(path)
