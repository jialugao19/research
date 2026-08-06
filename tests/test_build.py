import json
from pathlib import Path

from research_site.build import _featured_chart_view, build_site
from research_site.catalog import load_catalog
from research_site.validation import validate_built_site

SITE_ROOT = Path(__file__).resolve().parents[1]


def test_sidebar_groups_do_not_use_exclusive_accordion_behavior() -> None:
    javascript = (SITE_ROOT / "assets" / "site.js").read_text(encoding="utf-8")

    assert 'querySelectorAll(".sidebar-group[open]")' not in javascript
    assert "sibling.open = false" not in javascript


def test_subtopic_filter_and_anchor_behaviors_are_bundled() -> None:
    javascript = (SITE_ROOT / "assets" / "site.js").read_text(encoding="utf-8")

    assert "savedOpenState.set(group, group.open)" in javascript
    assert "group.open = savedOpenState.get(group)" in javascript
    assert "group.hidden = groupVisible === 0" in javascript
    assert 'hash.startsWith("#subtopic-")' in javascript
    assert "target.open = true" in javascript


def test_featured_chart_geometry_preserves_the_omitted_bin_gap() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    assert catalog.homepage is not None
    view = _featured_chart_view(catalog.homepage.featured.chart)

    assert view["axis_break_x"] is not None
    assert [tick["bin"] for tick in view["x_ticks"]] == [1, 2, 3, 18, 19, 20]
    assert all(len(series["paths"]) == 2 for series in view["series"])
    assert view["series"][0]["points"][0]["value"] == -8.054
    assert view["series"][0]["points"][-1]["value"] == 7.072


def test_build_produces_project_and_report_routes(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/research/")
    assert (output / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "one-minute" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "one-second" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "l2-features" / "index.html").is_file()
    assert (output / "knowledge" / "index.html").is_file()
    assert (output / "knowledge" / "foundations" / "index.html").is_file()
    assert (output / "knowledge" / "machine-intelligence" / "index.html").is_file()
    assert (output / "knowledge" / "machine-intelligence" / "nlp-transformers" / "index.html").is_file()
    assert (
        output / "knowledge" / "machine-intelligence" / "nlp-transformers" / "attention-mechanism" / "index.html"
    ).is_file()
    assert (
        output
        / "knowledge"
        / "systems-engineering"
        / "python-data-stack"
        / "numpy-ndarray-dtype-shape"
        / "index.html"
    ).is_file()
    assert (
        output
        / "knowledge"
        / "quantitative-research"
        / "market-microstructure"
        / "mm-market-impact"
        / "index.html"
    ).is_file()
    assert not (output / "projects" / "deep-ml" / "index.html").exists()
    assert not (output / "projects" / "quant-knowledge" / "index.html").exists()
    assert not (output / "knowledge" / "deep-ml" / "index.html").exists()
    assert not (output / "knowledge" / "quant" / "index.html").exists()
    assert not (output / "knowledge" / "concepts" / "index.html").exists()
    assert not (output / "knowledge" / "articles" / "index.html").exists()
    assert not (output / "knowledge" / "paths" / "index.html").exists()
    assert not (output / "knowledge" / "chapters" / "index.html").exists()
    assert (output / "knowledge.json").is_file()
    assert (output / "projects" / "tdx-data-source" / "index.html").is_file()
    assert not (output / "projects" / "tqo-data-source" / "index.html").exists()
    assert (output / "projects" / "live-predictor" / "index.html").is_file()
    assert (output / "reports" / "prediction-nn" / "0702-l2-ablation" / "index.html").is_file()
    assert (output / "reports" / "prediction-nn" / "0702-l2-ablation-v2" / "index.html").is_file()
    assert (output / "reports" / "live-predictor" / "0805-live-predictor-quality" / "index.html").is_file()
    assert not (output / "assets" / "report-heroes").exists()
    validate_built_site(catalog, SITE_ROOT, output, "/research/")


def test_homepage_shows_latest_report_once_per_project(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")

    index = (output / "index.html").read_text(encoding="utf-8")
    reports = (output / "reports" / "index.html").read_text(encoding="utf-8")

    assert "JG RESEARCH LAB" in index
    assert "Systematic Alpha<br>Research Infrastructure" in index
    assert "Building reproducible evidence pipelines<br>for machine learning alpha research." in index
    assert "EVIDENCE CHAIN" in index
    assert "FEATURED RESEARCH" in index
    assert "Stock1s GRU384 / MLP512×512 Evaluation" in index
    assert 'href="/reports/prediction-nn/0802-stock1s-gru384-v2/"' in index
    assert "assets/report-heroes/0802-stock1s-gru384-v2.png" not in index
    assert '<svg viewBox="0 0 820 420"' in index
    assert "Q01" in index
    assert "Q20" in index
    assert "-8.054 bps" in index
    assert "7.072 bps" in index
    assert "16</dt><dd>Research projects" in index
    assert "38</dt><dd>Experiments" in index
    assert "7</dt><dd>Published evaluations" in index
    assert "0.10765</dt><dd>Best reported test IC" in index
    assert "0.07895</dt><dd>Multi-seed test IC" in index
    assert "-18.27</dt><dd>Featured net Sharpe" in index
    assert "18</dt><dd>Architectures screened" in index
    assert "54.2M</dt><dd>Order-book ticks" in index
    assert "7.95M</dt><dd>1s evaluation rows" in index
    assert "2021–2026</dt><dd>Evidence windows" in index
    assert "A-share / ETF / Crypto</dt><dd>Research universe" in index
    assert "MODEL STATUS" in index
    assert "Fold0 validated" in index
    assert "Requires clean rerun" in index
    assert "Not promoted" in index
    assert "KEEP IN RESEARCH" in index
    assert "RESEARCH PHILOSOPHY" in index
    assert "REJECTED IDEAS" in index
    assert "Attention representation" in index
    assert "TCN architecture" in index
    assert "Large GRU / MLP capacity" in index
    assert "Primary metrics" in index
    assert "Forecasting Models" in index
    assert "Factor Discovery" in index
    assert "Portfolio &amp; Execution" in index
    assert "Market Data" in index
    assert "Research Systems" in index
    assert "T+1 打板策略研究报告" in index
    assert "Index500 Predict 研究报告" in index
    assert "Live Predictor 实时预测质量报告" in index
    assert "L2 Features Ablation vs Stock1m Baseline" not in index
    assert "L2 Features Ablation vs Stock1m Baseline" in reports
    assert "0702-l2-ablation-v2" in reports
    assert "reports/prediction-nn/0702-l2-ablation/" not in reports


def test_knowledge_pages_publish_the_validated_deepml_snapshot(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")

    index = (output / "knowledge" / "index.html").read_text(encoding="utf-8")
    domain = (output / "knowledge" / "machine-intelligence" / "index.html").read_text(encoding="utf-8")
    topic = (
        output / "knowledge" / "machine-intelligence" / "nlp-transformers" / "index.html"
    ).read_text(encoding="utf-8")
    deep_learning_topic = (
        output / "knowledge" / "machine-intelligence" / "deep-learning" / "index.html"
    ).read_text(encoding="utf-8")
    article = (
        output / "knowledge" / "machine-intelligence" / "nlp-transformers" / "attention-mechanism" / "index.html"
    ).read_text(encoding="utf-8")
    chapter = (
        output
        / "knowledge"
        / "systems-engineering"
        / "python-data-stack"
        / "numpy-ndarray-dtype-shape"
        / "index.html"
    ).read_text(encoding="utf-8")
    microstructure = (
        output
        / "knowledge"
        / "quantitative-research"
        / "market-microstructure"
        / "mm-market-impact"
        / "index.html"
    ).read_text(encoding="utf-8")
    payload = (output / "knowledge.json").read_text(encoding="utf-8")

    assert "Knowledge Graph" in index
    assert "A structured knowledge system<br>for research and engineering." in index
    assert "Knowledge architecture" in index
    assert "Browse by domain, then topic" in index
    assert "The source layer is metadata" in index
    assert "Machine Intelligence" in index
    assert "Quantitative Research" in index
    assert "Systems Engineering" in index
    assert "Independent sources" not in index
    assert "DeepML concepts" not in index
    assert "Quant chapters" not in index
    assert "Domain 02" in domain
    assert "Learning algorithms, neural architectures, optimization, and model operations." in domain
    assert "NLP &amp; Transformers" in topic
    assert "data-knowledge-search" in topic
    assert 'id="subtopic-tokenization-representation"' in topic
    assert 'id="subtopic-context-serving"' in topic
    assert topic.count('class="knowledge-subtopic"') == 10
    assert topic.count('class="knowledge-subtopic" id=') == 10
    assert topic.count("data-knowledge-group") == 10
    assert topic.count("data-knowledge-group data-subtopic-id") == 10
    assert topic.count("data-subtopic-id=") == 10
    assert topic.count("<details class=\"knowledge-subtopic\"") == 10
    assert topic.count("<details class=\"knowledge-subtopic\" id=") == 10
    assert topic.count(" open>") == 3  # desktop + mobile navigation domain, plus the first subtopic
    assert "Fine-Tuning &amp; Alignment" in topic
    assert "Retrieval &amp; Document Processing" in topic
    assert "Attention Mechanism" in topic
    assert "DeepML learning path" in deep_learning_topic
    assert "Part 1 · Foundations and differentiable computation" in deep_learning_topic
    assert "Five applied deep-learning parts" in deep_learning_topic
    assert "Part 5 · Efficient Systems" in deep_learning_topic
    assert '<html lang="zh-CN">' in article
    assert "Knowledge card" in article
    assert "Machine Intelligence" in article
    assert "NLP &amp; Transformers" in article
    assert "Attention" in article
    assert "<dt>Subtopic</dt>" in article
    assert "#subtopic-attention" in article
    assert "DeepML" in article
    assert "<math" in article
    assert "matplotlib" not in article
    assert '<html lang="zh-CN">' in chapter
    assert "Knowledge card" in chapter
    assert "Systems Engineering" in chapter
    assert "Python &amp; Data Stack" in chapter
    assert "Quant Knowledge" in chapter
    assert "numpy.ndarray 是 NumPy 最核心的数据结构" in chapter
    assert "Market Microstructure" in microstructure
    assert "Research bridge" in microstructure
    assert "Order-book data foundation" in microstructure
    assert '"schema_version": 4' in payload
    assert '"nodes": 871' in payload
    parsed_payload = json.loads(payload)
    nlp_topic = next(item for item in parsed_payload["topics"] if item["id"] == "nlp-transformers")
    attention_node = next(item for item in parsed_payload["nodes"] if item["id"] == "attention-mechanism")
    assert len(nlp_topic["subtopics"]) == 10
    assert sum(item["node_count"] for item in nlp_topic["subtopics"]) == nlp_topic["node_count"]
    assert attention_node["subtopic"] == "attention"
    assert '"/knowledge/machine-intelligence/nlp-transformers/attention-mechanism/"' in payload
    assert '"/knowledge/deep-ml/' not in payload
    assert '"/knowledge/chapters/' not in payload


def test_project_pages_show_contextual_metrics_and_caveats(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")

    one_minute = (output / "projects" / "prediction-nn" / "one-minute" / "index.html").read_text(encoding="utf-8")
    one_second = (output / "projects" / "prediction-nn" / "one-second" / "index.html").read_text(encoding="utf-8")
    genetic = (output / "projects" / "genetic-factor-auto-3" / "index.html").read_text(encoding="utf-8")
    aq2 = (output / "projects" / "aq2" / "index.html").read_text(encoding="utf-8")

    assert "0.07895" in one_minute
    assert "seeds 7/11/13" in one_minute
    assert "Experiment ID" in one_minute
    assert "Hypothesis" in one_minute
    assert "Method" in one_minute
    assert "Dataset" in one_minute
    assert "Primary metric" in one_minute
    assert "GRU / MLP architecture screen" in one_minute
    assert "stock1m · seeds 7/11/13" in one_minute
    assert 'id="study-optimize-1min-model"' in one_minute
    assert "0.09842" in one_second
    assert "used test during selection" in one_second
    assert "21,217.9 factors/s" in genetic
    assert "54,176,260" in aq2


def test_track_pages_use_explanatory_structure_without_summary_charts(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")

    one_minute = (output / "projects" / "prediction-nn" / "one-minute" / "index.html").read_text(
        encoding="utf-8"
    )
    one_second = (output / "projects" / "prediction-nn" / "one-second" / "index.html").read_text(
        encoding="utf-8"
    )

    assert '<figure class="result-chart' not in one_minute
    assert '<figure class="result-chart' not in one_second
    assert '<p class="eyebrow">one-minute</p>' not in one_minute
    assert "Data structure" in one_minute
    assert "batch × time-step × feature" in one_minute
    assert "Research question &amp; method" in one_minute
    assert "Observed result" in one_minute
    assert "Final 1min Architecture Evaluation" in one_minute
    assert "old model" in one_minute
    assert "Baselines &amp; Model Design" in one_minute
    assert "Data, Labels &amp; Sampling" in one_minute
    assert "Validation, Selection &amp; Robustness" in one_minute
    assert "Feature Extensions &amp; Integration" in one_minute
    assert "data and signal chain merit further research" in one_second


def test_catalog_json_keeps_internal_presentation_fields_private(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")
    payload = (output / "catalog.json").read_text(encoding="utf-8")
    assert '"charts"' not in payload
    assert '"schema_version": 2' in payload
    assert '"category": "forecasting-models"' in payload
    assert '"revision_of": "0702-l2-ablation"' in payload
    assert '"method": "GRU / MLP architecture screen"' in payload
    assert '"dataset": "stock1m · seeds 7/11/13"' in payload
    assert '"decision_state": "retain"' in payload
    assert '"primary_metric": "test-pooled-ic"' in payload
    assert payload.count('"is_current": true') == 7


def test_catalog_json_excludes_private_evidence_paths(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")
    payload = (output / "catalog.json").read_text(encoding="utf-8")
    assert "/home/" not in payload
    assert "/data-cache/" not in payload
    assert "evidence_ref" not in payload
