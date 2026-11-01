import json
import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

from research_site.build import build_site
from research_site.build_research import featured_chart_view
from research_site.build_output import build_atomically
from research_site.catalog import load_catalog
from research_site.validation import validate_built_site
from research_site.styles import site_stylesheet

SITE_ROOT = Path(__file__).resolve().parents[1]



@pytest.fixture(scope="module")
def root_build(tmp_path_factory):
    # Reuse one verified root-path build for independent read-only assertions.
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path_factory.mktemp("root-build") / "site"
    build_site(catalog, SITE_ROOT, output, "/")
    return catalog, output


@pytest.fixture(scope="module")
def production_build(tmp_path_factory):
    # Keep production-prefix coverage separate from the root-path fixture.
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path_factory.mktemp("production-build") / "site"
    build_site(catalog, SITE_ROOT, output, "/research/")
    return catalog, output


def test_sidebar_groups_do_not_use_exclusive_accordion_behavior() -> None:
    javascript = (SITE_ROOT / "assets" / "site.js").read_text(encoding="utf-8")

    assert 'querySelectorAll(".sidebar-group[open]")' not in javascript
    assert "sibling.open = false" not in javascript


def test_research_taxonomy_navigation_behaviors_are_bundled() -> None:
    javascript = (SITE_ROOT / "assets" / "site.js").read_text(encoding="utf-8")

    assert 'querySelectorAll("[data-taxonomy-toggle]")' in javascript
    assert 'button.setAttribute("aria-expanded", String(expanded))' in javascript
    assert "branch.hidden = !expanded" in javascript
    assert 'hash.startsWith("#topic-")' in javascript
    assert "openTaxonomyAncestors(window.location.hash)" in javascript
    assert "sibling" not in javascript


def test_subtopic_filter_and_anchor_behaviors_are_bundled() -> None:
    javascript = (SITE_ROOT / "assets" / "site.js").read_text(encoding="utf-8")

    assert "savedOpenState.set(group, group.open)" in javascript
    assert "group.open = savedOpenState.get(group)" in javascript
    assert "group.hidden = groupVisible === 0" in javascript
    assert 'hash.startsWith("#subtopic-")' in javascript
    assert "target.open = true" in javascript


def test_publication_filter_includes_research_stage() -> None:
    javascript = (SITE_ROOT / "assets" / "site.js").read_text(encoding="utf-8")
    template = (SITE_ROOT / "templates" / "reports.html").read_text(encoding="utf-8")

    assert 'querySelector("#stage-filter")' in javascript
    assert "card.dataset.stage === stageId" in javascript
    assert 'querySelectorAll("#report-catalog .publication-row")' in javascript
    assert 'data-stage="{{ report.stage }}"' in template


def test_inherited_documentation_tokens_and_typography() -> None:
    # Protect the x99/Docusaurus contract rather than later visual overrides.
    stylesheet = site_stylesheet(SITE_ROOT)
    assert "--header-height: 60px;" in stylesheet
    assert "--sidebar-width: 300px;" in stylesheet
    assert "--toc-width: 252px;" in stylesheet
    assert "--accent: var(--action);" in stylesheet
    assert "--action: #2e8555;" in stylesheet
    assert '--sans: system-ui, -apple-system, "Segoe UI"' in stylesheet
    assert "--research-body-size" not in stylesheet
    assert "font-size: 3rem !important" not in stylesheet
    assert "data-auto-hide" not in (SITE_ROOT / "templates/base.html").read_text()


def test_research_detail_pages_reuse_the_knowledge_catalog_shell() -> None:
    for template_name in ("project.html", "stage.html", "infrastructure.html"):
        template = (SITE_ROOT / "templates" / template_name).read_text(encoding="utf-8")

        assert "{% block body_class %}knowledge-page knowledge-catalog-page" in template
        assert "catalog-hero knowledge-domain-hero" in template
        assert 'class="knowledge-breadcrumb"' in template
        assert 'class="knowledge-section' in template
        assert 'class="page-hero shell"' not in template
        assert 'class="shell section compact' not in template
        assert 'class="page-stats"' not in template
        assert "knowledge-next-page" not in template
        assert "article-badges" not in template
        assert "article-source-note" not in template


def test_research_overview_and_assessments_use_the_shared_document_template() -> None:
    overview = (SITE_ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    experiment = (SITE_ROOT / "templates" / "_experiment.html").read_text(encoding="utf-8")
    project = (SITE_ROOT / "templates" / "project.html").read_text(encoding="utf-8")
    stage = (SITE_ROOT / "templates" / "stage.html").read_text(encoding="utf-8")

    assert "knowledge-page knowledge-ontology-page research-overview-page" in overview
    assert "knowledge-hero knowledge-ontology-hero research-flow-hero" in overview
    assert 'class="research-project-list"' in overview
    assert "research_spine(project, catalog, base_url, true)" in overview
    assert "lab-hero" not in overview
    assert "metric-band" not in overview
    assert "featured-research" not in overview
    assert "quant-chart" not in overview
    assert "research-principles" not in overview
    assert "rejection-ledger" not in overview
    assert "project-ledger" not in overview
    assert "{% macro primary_evidence(" in experiment
    assert 'class="knowledge-section primary-evidence"' in experiment
    assert "<h2>Primary result</h2>" in experiment
    assert "primary_evidence(" in overview
    assert "experiment_table(experiments" in project
    assert "research-questions" in project
    assert "taxonomy_tree(" in stage
    assert "Additional publications" in stage
    assert "Current findings &amp; metrics" not in project


def test_research_templates_are_single_column_without_defensive_blocks() -> None:
    templates = "\n".join(
        (SITE_ROOT / "templates" / name).read_text(encoding="utf-8")
        for name in (
            "index.html",
            "project.html",
            "stage.html",
            "infrastructure.html",
            "prediction_split.html",
            "reports.html",
            "report.html",
            "_experiment.html",
            "_research_flow.html",
            "_research_taxonomy.html",
        )
    )
    stylesheet = site_stylesheet(SITE_ROOT)

    for forbidden in (
        "research-project-card",
        "stage-summary-grid",
        "subproject-grid",
        "experiment-card",
        "catalog-card",
        "infrastructure-grid",
        "split-project-grid",
        "Current boundary",
        "Current assessment",
        "Current decision",
        "Evidence boundary",
        "Evidence gap",
        "Not applicable",
        "experiment-toggle",
        '<details class="experiment-record',
    ):
        assert forbidden not in templates
    assert "--research-body-size" not in stylesheet
    assert ".research-project-list, .stage-summary-list" in stylesheet


def test_featured_chart_geometry_preserves_the_omitted_bin_gap() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    assert catalog.homepage is not None
    view = featured_chart_view(catalog.homepage.featured.chart)

    assert view["axis_break_x"] is not None
    assert [tick["bin"] for tick in view["x_ticks"]] == [1, 2, 3, 18, 19, 20]
    assert all(len(series["paths"]) == 2 for series in view["series"])
    assert view["series"][0]["points"][0]["value"] == -8.054
    assert view["series"][0]["points"][-1]["value"] == 7.072


def test_build_produces_project_and_report_routes(production_build) -> None:
    # Read the shared build without mutating its contents.
    catalog, output = production_build
    assert (output / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "one-minute" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "one-second" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "l2-features" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn-1min" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn-1min" / "model" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn-1min" / "l2-features" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn-1min" / "market-context-1min" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn-1min" / "feature-audit-1min" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn-1s" / "strategy" / "index.html").is_file()
    assert (output / "projects" / "snapshot-visualizer2" / "index.html").is_file()
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
    assert (output / "reports" / "prediction-nn" / "0831-market-cs-comparison" / "index.html").is_file()
    assert (output / "reports" / "live-predictor" / "0805-live-predictor-quality" / "index.html").is_file()
    assert not (output / "assets" / "report-heroes").exists()
    legacy_topic = (
        output / "projects" / "prediction-nn-1min" / "day-pure-batch-1min" / "index.html"
    ).read_text(encoding="utf-8")
    assert "/projects/prediction-nn-1min/model/#topic-model--batch" in legacy_topic
    stage_page = BeautifulSoup(
        (output / "projects" / "prediction-nn-1min" / "data-engineering" / "index.html").read_text(
            encoding="utf-8"
        ),
        "html.parser",
    )
    desktop_navigation = stage_page.select_one(".doc-sidebar .sidebar-nav")
    mobile_navigation = stage_page.select_one(".mobile-navigation .sidebar-nav")
    assert desktop_navigation is not None
    assert mobile_navigation is not None
    assert len(desktop_navigation.select(".sidebar-stage-item")) == len(catalog.research_stages)
    assert len(mobile_navigation.select(".sidebar-stage-item")) == len(catalog.research_stages)
    assert desktop_navigation.find("a", string="Outlier")["href"].endswith(
        "/data-engineering/#topic-data-engineering--data-clean--outlier"
    )
    toggles = stage_page.select("[data-taxonomy-toggle]")
    assert toggles
    assert all(toggle["aria-expanded"] == "false" for toggle in toggles)
    branches = stage_page.select(".sidebar-taxonomy-branch")
    assert branches
    assert all(branch.has_attr("hidden") for branch in branches)
    control_ids = [toggle["aria-controls"] for toggle in toggles]
    assert len(control_ids) == len(set(control_ids))
    validate_built_site(catalog, SITE_ROOT, output, "/research/")


def test_homepage_shows_latest_report_once_per_project(root_build) -> None:
    # Read the shared build without mutating its contents.
    catalog, output = root_build

    index = (output / "index.html").read_text(encoding="utf-8")
    reports = (output / "reports" / "index.html").read_text(encoding="utf-8")

    assert '<body class="knowledge-page knowledge-ontology-page research-overview-page">' in index
    assert "Research overview" in index
    assert "Follow the evidence<br>from data to strategy." in index
    assert "One project, one complete logic chain" in index
    assert index.count('class="research-project-row"') == 20
    assert "Prediction-NN 1min" in index
    assert "Prediction-NN 1s" in index
    assert "Research infrastructure" in index
    assert 'id="primary-result" class="knowledge-section primary-evidence"' in index
    assert "<h2>Primary result</h2>" in index
    assert "1s GRU384 Baseline Evaluation" in index
    assert "Stock1s Fold0 Corrected Full Evaluation" in index
    assert 'href="/reports/prediction-nn/0807-stock1s-fold0-full-evaluation/"' in index
    assert "assets/report-heroes/0802-stock1s-gru384-v2.png" not in index
    assert "quant-chart" not in index
    assert "research-metrics" not in index
    assert "0.09842" in index
    assert "0.09469" in index
    assert "7,947,567" in index
    assert "-18.27" in index
    assert "Rejected ideas" in index
    assert "Attention representation" in index
    assert "TCN architecture" in index
    assert "Large GRU / MLP capacity" in index
    assert "Data Engineering" in index
    assert "Feature Engineering" in index
    assert "Prediction Evaluation" in index
    assert "T+1 打板策略研究报告" in index
    assert "Index500 Predict 研究报告" in index
    assert "Live Predictor 实时预测质量报告" in index
    assert "L2 Features Ablation vs Stock1m Baseline" not in index
    assert "L2 Features Ablation vs Stock1m Baseline" in reports
    assert "0702-l2-ablation-v2" in reports
    assert "reports/prediction-nn/0702-l2-ablation/" not in reports


def test_knowledge_pages_publish_the_validated_deepml_snapshot(root_build) -> None:
    # Read the shared build without mutating its contents.
    catalog, output = root_build

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
    gradient_descent = (
        output
        / "knowledge"
        / "machine-intelligence"
        / "machine-learning"
        / "gradient-descent"
        / "index.html"
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
    green_book = (
        output
        / "knowledge"
        / "foundations"
        / "probability-statistics"
        / "brainteaser-expectation"
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
    assert "Related Readings" in index
    assert "Use these notes for theoretical background, standard notation" in index
    assert "Use this book to cross-check terminology, equations" in index
    assert index.rfind("Related Readings") > index.rfind("Research bridge")
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
    assert "Knowledge card" not in article
    assert "Machine Intelligence" in article
    assert "NLP &amp; Transformers" in article
    assert "Attention" in article
    assert '<p class="article-source-note">articles/attention-mechanism.md · source class nlp</p>' in article
    assert "关键词：" not in article
    assert article.count(catalog.knowledge.node_by_slug["attention-mechanism"].summary) == 1
    assert "#subtopic-attention" in article
    assert 'class="knowledge-next-page"' in article
    expected_next = catalog.knowledge.next_page_for("attention-mechanism")
    assert f'href="/{expected_next.route}"' in article
    assert f"Next page: {expected_next.title}" in article
    assert article.count('class="related-concept-row"') == 3
    assert 'href="/knowledge/foundations/linear-algebra/matrix-multiplication/"' in article
    assert "Prerequisites" not in article
    assert "Next concepts" not in article
    assert "延伸阅读" not in article
    assert "概念误解" not in article
    assert "数学误解" not in article
    assert "使用误区" not in article
    assert "DeepML" in article
    assert "<math" in article
    assert "matplotlib" not in article
    assert '<html lang="zh-CN">' in chapter
    assert "Knowledge card" not in chapter
    assert "Systems Engineering" in chapter
    assert "Python &amp; Data Stack" in chapter
    assert "Quant Knowledge" in chapter
    assert "<dt>Domain</dt>" not in chapter
    assert "numpy.ndarray 是 NumPy 最核心的数据结构" in chapter
    assert "Market Microstructure" in microstructure
    assert "Research bridge" in microstructure
    assert "Order-book data foundation" in microstructure
    assert "<h1>Expectation</h1>" in green_book
    assert "· Green Book</p>" in green_book
    assert "Brain Teaser / Green Book：期望" not in green_book
    assert "为什么需要它" not in gradient_descent
    assert "模型需要从错误中调整参数" in gradient_descent
    assert gradient_descent.index("数学定义") < gradient_descent.index("核心直觉")
    assert "CS229 Machine Learning Notes" not in gradient_descent
    assert "Deep Learning Book" not in gradient_descent
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


def test_project_pages_show_contextual_metrics_without_defensive_blocks(root_build) -> None:
    # Read the shared build without mutating its contents.
    catalog, output = root_build

    one_minute = (output / "projects" / "prediction-nn-1min" / "model" / "index.html").read_text(encoding="utf-8")
    one_second = (output / "projects" / "prediction-nn-1s" / "prediction-evaluation" / "index.html").read_text(encoding="utf-8")
    genetic = (output / "projects" / "genetic-factor-auto-3" / "index.html").read_text(encoding="utf-8")
    aq2 = (output / "projects" / "aq2" / "index.html").read_text(encoding="utf-8")

    assert "0.07895" in one_minute
    assert "seeds 7/11/13" in one_minute
    assert "Method" in one_minute
    assert "Dataset" in one_minute
    assert "Read result" not in one_minute
    assert "GRU / MLP architecture screen" in one_minute
    assert "stock1m · seeds 7/11/13" in one_minute
    assert 'id="experiment-optimize-1min-model"' in one_minute
    assert "0.09842" in one_second
    assert "used test during selection" in one_second
    assert "21,217.9 factors/s" in genetic
    assert "54,176,260" in aq2
    combined = one_minute + one_second + genetic + aq2
    assert "Current boundary" not in combined
    assert "Current decision" not in combined
    assert "Evidence boundary" not in combined


def test_stage_pages_follow_the_canonical_research_chain(root_build) -> None:
    # Read the shared build without mutating its contents.
    catalog, output = root_build

    one_minute = (output / "projects" / "prediction-nn-1min" / "data-engineering" / "index.html").read_text(
        encoding="utf-8"
    )
    one_second = (output / "projects" / "prediction-nn-1s" / "strategy" / "index.html").read_text(
        encoding="utf-8"
    )
    model = (output / "projects" / "prediction-nn-1min" / "model" / "index.html").read_text(
        encoding="utf-8"
    )

    assert '<figure class="result-chart' not in one_minute
    assert '<figure class="result-chart' not in one_second
    assert "STAGE 02 / 06" in one_minute
    assert "Label Noise and Prediction Calibration" in one_minute
    assert "Date-pure Batch Sampling" not in one_minute
    assert 'id="topic-data-engineering--label"' in one_minute
    assert "Key metric" in one_minute
    assert "Date-pure Batch 1min Full Evaluation" not in one_minute
    assert 'id="topic-model--batch"' in model
    assert "Date-pure Batch Sampling" in model
    assert "Date-pure Batch 1min Full Evaluation" in model
    assert "STAGE 06 / 06" in one_second
    assert "Stock1s Fold0 Cost and Turnover Sweep" in one_second
    assert "Signal conversion, portfolio rules, execution, turnover, costs" in one_second

    def node_count(nodes) -> int:
        return sum(1 + node_count(node.children) for node in nodes)

    for project in catalog.research_projects:
        rendered_stages = {
            stage.id: (
                output / "projects" / project.id / stage.id / "index.html"
            ).read_text(encoding="utf-8")
            for stage in catalog.research_stages
        }
        for stage in catalog.research_taxonomy:
            assert rendered_stages[stage.id].count('class="research-taxonomy-node ') == node_count(
                stage.nodes
            )
        combined_project = "\n".join(rendered_stages.values())
        for experiment in catalog.experiments_for_project(project.id):
            assert combined_project.count(f'id="experiment-{experiment.id}"') == 1

    empty_strategy = (
        output / "projects" / "get-data" / "strategy" / "index.html"
    ).read_text(encoding="utf-8")
    assert "<h2>execution</h2>" in empty_strategy
    assert "<h2>position</h2>" in empty_strategy
    assert "<h2>signal</h2>" in empty_strategy
    assert 'id="experiment-' not in empty_strategy
    assert "No experiments" not in empty_strategy


def test_catalog_json_keeps_internal_presentation_fields_private(root_build) -> None:
    # Read the shared build without mutating its contents.
    catalog, output = root_build
    payload = (output / "catalog.json").read_text(encoding="utf-8")
    assert '"charts"' not in payload
    assert '"schema_version": 5' in payload
    assert '"category": "forecasting-models"' in payload
    assert '"revision_of": "0702-l2-ablation"' in payload
    assert '"method": "GRU / MLP architecture screen"' in payload
    assert '"dataset": "stock1m · seeds 7/11/13"' in payload
    assert '"decision_state": "retain"' in payload
    assert '"primary_metric": "test-pooled-ic"' in payload
    assert '"stage": "feature-engineering"' in payload
    assert '"taxonomy_path": "feature-engineering/market"' in payload
    assert '"research_taxonomy"' in payload
    assert '"subproject"' not in payload
    assert '"tracks"' not in payload
    assert payload.count('"is_current": true') == 26


def test_atomic_build_preserves_previous_output_when_validation_fails(tmp_path: Path) -> None:
    output = tmp_path / "site"
    output.mkdir()
    (output / "marker.txt").write_text("old", encoding="utf-8")

    def render(staging: Path) -> None:
        (staging / "marker.txt").write_text("new", encoding="utf-8")

    def reject(_: Path) -> None:
        raise ValueError("invalid staging build")

    with pytest.raises(ValueError, match="invalid staging build"):
        build_atomically(output, render, reject)

    assert (output / "marker.txt").read_text(encoding="utf-8") == "old"
    assert not list(tmp_path.glob(".site.build-*"))
    assert not list(tmp_path.glob(".site.previous-*"))


def test_atomic_build_replaces_complete_output_without_stale_files(tmp_path: Path) -> None:
    output = tmp_path / "site"
    output.mkdir()
    (output / "stale.html").write_text("old", encoding="utf-8")

    def render(staging: Path) -> None:
        (staging / "index.html").write_text("new", encoding="utf-8")

    result = build_atomically(output, render, lambda _: None)

    assert result.output_root == output.resolve()
    assert result.file_count == 1
    assert result.output_root.stat().st_mode & 0o777 == 0o755
    assert (output / "index.html").read_text(encoding="utf-8") == "new"
    assert not (output / "stale.html").exists()
    assert not list(tmp_path.glob(".site.build-*"))
    assert not list(tmp_path.glob(".site.previous-*"))


def test_atomic_build_rolls_back_when_publish_rename_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "site"
    output.mkdir()
    (output / "marker.txt").write_text("old", encoding="utf-8")
    real_replace = os.replace
    calls = 0

    def fail_second_replace(source: Path, destination: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("publish rename failed")
        real_replace(source, destination)

    monkeypatch.setattr("research_site.build_output.os.replace", fail_second_replace)

    with pytest.raises(OSError, match="publish rename failed"):
        build_atomically(
            output,
            lambda staging: (staging / "marker.txt").write_text("new", encoding="utf-8"),
            lambda _: None,
        )

    assert (output / "marker.txt").read_text(encoding="utf-8") == "old"
    assert not list(tmp_path.glob(".site.build-*"))
    assert not list(tmp_path.glob(".site.previous-*"))


def test_catalog_json_excludes_private_evidence_paths(root_build) -> None:
    # Read the shared build without mutating its contents.
    catalog, output = root_build
    payload = (output / "catalog.json").read_text(encoding="utf-8")
    assert "/home/" not in payload
    assert "/data-cache/" not in payload
    assert "evidence_ref" not in payload
