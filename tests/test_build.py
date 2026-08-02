from pathlib import Path

from research_site.build import build_site
from research_site.catalog import load_catalog
from research_site.validation import validate_built_site


SITE_ROOT = Path(__file__).resolve().parents[1]


def test_build_produces_project_and_report_routes(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/research/")
    assert (output / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "l2-features" / "index.html").is_file()
    assert (output / "reports" / "prediction-nn" / "0702-l2-ablation" / "index.html").is_file()
    validate_built_site(catalog, SITE_ROOT, output, "/research/")
