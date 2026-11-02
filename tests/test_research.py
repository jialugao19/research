from dataclasses import replace
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image
import pytest
import yaml

from research_site.build import build_site
from research_site.catalog import CatalogError, load_catalog, load_studies, parse_arms, parse_figures
from research_site.publication import validate_public_reports
from research_site.research_assets import figure_bytes, publish_image
from research_site.styles import site_stylesheet
from research_site.validation import validate_built_site

SITE_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def catalog():
    # Load immutable repository evidence once for relation and rendering checks.
    return load_catalog(SITE_ROOT / "content")


@pytest.fixture(scope="module")
def built(catalog, tmp_path_factory):
    # Share one complete build across independent assertions.
    output = tmp_path_factory.mktemp("research") / "site"
    build_site(catalog, SITE_ROOT, output, "/research/")
    return output


def test_questions_are_separate_and_cross_linked(catalog):
    # A canonical experiment can answer several questions across project contexts.
    assert len(catalog.experiments) == 49
    assert len(catalog.studies) == 31
    questions = catalog.studies_for_experiment("0827-market-cs")
    assert {s.id for s in questions} == {"feature-engineering-market", "prediction-evaluation-summary-ic"}
    shared = catalog.study_by_id["prediction-evaluation-summary-ic"]
    assert len(shared.project_ids) == 3
    assert "0831-market-cs-comparison" in {rid for e in catalog.experiments_for_study(shared.id) for rid in e.report_ids}
    assert len(catalog.studies_for_report("0831-market-cs-comparison")) == 2


@pytest.mark.parametrize("kind", ["unknown-experiment", "unknown-project", "unknown-report", "duplicate", "orphan"])
def test_question_integrity_rejects_broken_relations(catalog, tmp_path, kind):
    # Reject references and omissions before rendering public pages.
    data = yaml.safe_load((SITE_ROOT / "content/studies.yaml").read_text())
    if kind == "unknown-experiment":
        data["studies"][0]["experiment_ids"].append("missing-experiment")
    elif kind == "unknown-project":
        data["studies"][0]["project_ids"].append("missing-project")
    elif kind == "unknown-report":
        data["studies"][0]["report_ids"].append("missing-report")
    elif kind == "duplicate":
        data["studies"].append(data["studies"][0])
    else:
        data["studies"][0]["experiment_ids"].remove("us-route-top3-backtest-20261022")
    path = tmp_path / "studies.yaml"
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(CatalogError):
        load_studies(path, catalog.projects, catalog.experiments, catalog.reports, catalog.research_taxonomy)


def test_reports_and_experiments_support_shared_associations(catalog):
    # Resolve both sides of many-to-many links without copying entities.
    first = catalog.experiment_by_id["0827-market-cs"]
    second = replace(catalog.experiment_by_id["0825-feature-audit"], report_ids=first.report_ids)
    first = replace(first, related_project_ids=("prediction-nn-1s",))
    shared = replace(catalog, experiments=tuple(first if e.id == first.id else second if e.id == second.id else e for e in catalog.experiments))
    assert first in shared.experiments_for_project("prediction-nn-1s")
    assert {e.id for e in shared.experiments_for_report("0831-market-cs-comparison")} == {first.id, second.id}
    report = replace(catalog.report_by_id["0831-market-cs-comparison"], related_project_ids=("prediction-nn-1s",))
    shared = replace(shared, reports=tuple(report if r.id == report.id else r for r in catalog.reports))
    assert report in shared.reports_for_project("prediction-nn-1s")


def test_unmatched_or_failed_arm_cannot_publish_numeric_comparison():
    # A failed gate is visible but must not acquire an OOS score.
    arm = {"id": "failed", "label": "Failed", "model": "GRU", "status": "failed-before-test", "metrics": []}
    with pytest.raises(CatalogError, match="comparison_scope"):
        parse_arms({"arms": [arm]}, "example")
    arm["metrics"] = [{"id": "ic", "label": "IC", "value": .1, "format": "decimal", "context": "test"}]
    with pytest.raises(CatalogError, match="non-completed"):
        parse_arms({"comparison_scope": "matched test", "arms": [arm]}, "example")


def test_figure_source_must_be_linked_and_registered(catalog):
    # Figure provenance is part of the publication allowlist.
    with pytest.raises(CatalogError, match="not linked"):
        parse_figures({"figures": [{"report_id": "unknown"}]}, (), catalog.report_by_id)
    with pytest.raises(CatalogError, match="nonnegative"):
        parse_figures({"figures": [{"report_id": "0831-market-cs-comparison", "title": "IC", "image_index": -1}]}, ("0831-market-cs-comparison",), catalog.report_by_id)


def test_responsive_images_preserve_original_pixels_and_bytes(tmp_path):
    # Lossless derived images retain chart content and original access.
    source = BytesIO()
    Image.new("RGB", (1200, 600), "white").save(source, "PNG")
    asset = publish_image(source.getvalue(), tmp_path)
    assert (tmp_path / asset["original"]).read_bytes() == source.getvalue()
    assert asset["sha256"] == sha256(source.getvalue()).hexdigest()
    assert [r["width"] for r in asset["renditions"]] == [480, 960, 1200]
    for rendition in asset["renditions"]:
        with Image.open(tmp_path / rendition["path"]) as image:
            assert image.format == "WEBP"
            assert image.size == (rendition["width"], rendition["width"] // 2)


def test_entity_routes_payload_and_reverse_publication_links(catalog, built):
    # Assert complete identity coverage, not just totals.
    payload = json.loads((built / "catalog.json").read_text())
    assert {e["id"] for e in payload["experiments"]} == set(catalog.experiment_by_id)
    assert {s["id"] for s in payload["studies"]} == set(catalog.study_by_id)
    for entity in (*catalog.experiments, *catalog.studies):
        assert (built / entity.route / "index.html").is_file()
    page = BeautifulSoup((built / "experiments/0827-market-cs/index.html").read_text(), "html.parser")
    assert len(page.select("#matched-comparison tbody tr")) == 5
    failed = page.select("#matched-comparison tbody tr")[-1]
    assert "failed-before-test" in failed.get_text()
    assert all(cell.get_text(strip=True) == "—" for cell in failed.select("td.numeric"))
    report = (built / catalog.report_by_id["0805-live-predictor-quality"].route / "index.html").read_text()
    assert "/studies/prediction-evaluation-summary-ic/" in report
    assert "/experiments/live-predictor-live-quality/" in report


def test_figures_keep_provenance_srcset_and_originals(catalog, built):
    # Every registered figure has a source-identical original and responsive HTML.
    manifest = json.loads((built / "research-images.json").read_text())
    legacy_images = {}
    for experiment in catalog.experiments:
        if not experiment.figures:
            continue
        soup = BeautifulSoup((built / experiment.route / "index.html").read_text(), "html.parser")
        images = soup.select(".research-figure img")
        assert len(images) == len(experiment.figures)
        for reference, figure, image in zip(experiment.figures, manifest[experiment.id], images):
            expected = figure_bytes(reference, catalog, SITE_ROOT, legacy_images)
            assert (built / figure["original"]).read_bytes() == expected
            assert image["loading"] == "lazy" and image["decoding"] == "async"
            assert image["srcset"] and image["sizes"] and image["width"] and image["height"]
            assert image.parent["href"] == "/research/" + figure["original"]


def test_legacy_bytes_and_standalone_styles_remain_consistent(catalog, built):
    # Freeze legacy bytes while sharing presentation code with Markdown reports.
    for report in catalog.reports:
        if not report.is_markdown:
            assert (built / report.route / "index.html").read_bytes() == (SITE_ROOT / "public" / report.route / "index.html").read_bytes()
    css = site_stylesheet(SITE_ROOT)
    assert (built / "assets/site.css").read_text() == css
    report = (built / catalog.report_by_id["0805-live-predictor-quality"].route / "index.html").read_text()
    assert "--sidebar-width: 300px;" in report
    assert "--research-body-size" not in report
    assert "public, max-age=31536000, immutable" in (SITE_ROOT / "deploy/nginx.conf").read_text()
