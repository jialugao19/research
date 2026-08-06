import re
import shutil
from pathlib import Path

import pytest

from research_site.catalog import CatalogError, load_catalog
from research_site.knowledge_sync import KnowledgeSyncError, sync_quant_knowledge_snapshot

SITE_ROOT = Path(__file__).resolve().parents[1]


def _copy_catalog(tmp_path: Path) -> None:
    for name in ("projects.yaml", "studies.yaml", "reports.yaml", "highlights.yaml"):
        (tmp_path / name).write_text((SITE_ROOT / "content" / name).read_text(encoding="utf-8"), encoding="utf-8")
    shutil.copytree(SITE_ROOT / "content" / "report-docs", tmp_path / "report-docs")
    shutil.copytree(SITE_ROOT / "content" / "knowledge", tmp_path / "knowledge")


def test_repository_catalog_is_valid() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    assert len(catalog.projects) == 18
    assert len(catalog.research_projects) == 16
    assert len(catalog.knowledge_projects) == 2
    assert len(catalog.studies) == 38
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
    assert "net results" in one_minute.conclusion
    assert catalog.project_by_id["prediction-nn"].track("one-second") is not None
    assert catalog.project_by_id["prediction-nn"].subproject("l2-features").group == "Feature Extensions & Integration"
    assert catalog.study_by_id["baseline-1s-0720"].metrics[0].display_value == "0.09842"
    evaluation_rows = next(
        metric
        for metric in catalog.study_by_id["baseline-1s-0720"].metrics
        if metric.id == "evaluation-rows"
    )
    assert evaluation_rows.display_value == "7,947,567"
    assert all(study.method and study.dataset and study.decision_state for study in catalog.studies)
    assert all(not study.metrics or study.primary_metric is not None for study in catalog.studies)
    assert catalog.study_by_id["optimize-1min-model"].primary_metric_id == "test-pooled-ic"
    architecture_count = next(
        metric
        for metric in catalog.study_by_id["optimize-1min-model"].metrics
        if metric.id == "architecture-candidates"
    )
    assert architecture_count.display_value == "18"
    assert catalog.homepage is not None
    assert catalog.homepage.featured.study == "baseline-1s-0720"
    assert catalog.homepage.featured.chart.bins == (1, 2, 3, 18, 19, 20)
    assert len(catalog.homepage.metrics) == 8
    assert len(catalog.homepage.rejected_ideas) == 3
    assert catalog.project_by_id["deep-ml"].section == "knowledge"
    assert catalog.project_by_id["quant-knowledge"].section == "knowledge"
    assert catalog.knowledge is not None
    assert catalog.knowledge.counts == {
        "concepts": 735,
        "articles": 653,
        "relations": 2585,
        "paths": 18,
    }
    assert catalog.knowledge.aggregate_counts == {
        "sources": 2,
        "concepts": 735,
        "deepml_articles": 653,
        "quant_chapters": 136,
        "nodes": 871,
        "relations": 2585,
        "paths": 18,
    }
    assert len(catalog.knowledge.ontology_domains) == 5
    assert sum(len(domain.topics) for domain in catalog.knowledge.ontology_domains) == 25
    assert len(catalog.knowledge.nodes) == 871
    assert catalog.knowledge.node_by_slug["attention-mechanism"].route == (
        "knowledge/machine-intelligence/nlp-transformers/attention-mechanism/"
    )
    assert catalog.knowledge.node_by_slug["numpy-ndarray-dtype-shape"].route == (
        "knowledge/systems-engineering/python-data-stack/numpy-ndarray-dtype-shape/"
    )
    assert catalog.knowledge.node_by_slug["mm-market-impact"].route == (
        "knowledge/quantitative-research/market-microstructure/mm-market-impact/"
    )
    assert len(catalog.knowledge.quant_sections) == 8
    assert len(catalog.knowledge.chapters) == 136
    assert catalog.knowledge.article_by_slug["attention-mechanism"].review_state == "automated_editorial"
    assert catalog.knowledge.chapter_by_slug["numpy-ndarray-dtype-shape"].section_title == "Python & Data Stack"
    neural_network = catalog.knowledge.chapter_by_slug["ml-neural-network"]
    assert neural_network.section_title == "Deep Learning"
    assert neural_network.part_title == "Part 1 · Foundations & Correctness"
    assert neural_network.source_path == "booklet/06-deep-learning/01-foundations/108-ml-neural-network.md"
    deep_learning_path = catalog.knowledge.path_by_id["deep-learning-engineer"]
    assert len(deep_learning_path.stages) == 9
    assert deep_learning_path.organization == "part -> stage -> concept -> article"
    assert deep_learning_path.stages[0].title.startswith("Part 1")
    assert all(stage.summary for stage in deep_learning_path.stages)
    assert catalog.knowledge.node_by_slug["mm-market-impact"].level == "applied"
    assert catalog.knowledge.node_by_slug["cs-git-version-control"].level == "engineering"


def test_long_knowledge_topics_have_complete_bounded_subtopics() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    assert catalog.knowledge is not None
    grouped_topics = {
        (domain.id, topic.id): topic
        for domain in catalog.knowledge.ontology_domains
        for topic in domain.topics
        if topic.subtopics
    }
    assert set(grouped_topics) == {
        ("foundations", "probability-statistics"),
        ("foundations", "linear-algebra"),
        ("machine-intelligence", "machine-learning"),
        ("machine-intelligence", "deep-learning"),
        ("machine-intelligence", "nlp-transformers"),
        ("machine-intelligence", "reinforcement-learning"),
        ("machine-intelligence", "computer-vision"),
        ("machine-intelligence", "mlops-inference"),
        ("computer-science", "algorithms"),
        ("computer-science", "databases"),
        ("systems-engineering", "python-data-stack"),
    }
    for (domain_id, topic_id), topic in grouped_topics.items():
        topic_nodes = catalog.knowledge.nodes_for_topic(domain_id, topic_id)
        subtopic_nodes = [
            catalog.knowledge.nodes_for_subtopic(domain_id, topic_id, subtopic.id)
            for subtopic in topic.subtopics
        ]
        assert all(0 < len(nodes) <= 30 for nodes in subtopic_nodes)
        assert sum(len(nodes) for nodes in subtopic_nodes) == len(topic_nodes)
        assert {node.id for nodes in subtopic_nodes for node in nodes} == {node.id for node in topic_nodes}
    for domain in catalog.knowledge.ontology_domains:
        for topic in domain.topics:
            if not topic.subtopics:
                assert len(catalog.knowledge.nodes_for_topic(domain.id, topic.id)) <= 30


def test_quant_chapter_titles_do_not_repeat_filename_sequences() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    assert catalog.knowledge is not None
    assert all(not re.match(r"^\d+\.\s", chapter.title) for chapter in catalog.knowledge.chapters)
    assert all(not re.match(r"^#\s+\d+\.\s", chapter.body) for chapter in catalog.knowledge.chapters)


def test_report_routes_are_unique() -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    routes = [report.route for report in catalog.reports]
    assert len(routes) == len(set(routes))


def test_knowledge_snapshot_checksum_is_enforced(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    article = tmp_path / "knowledge" / "deep-ml" / "articles" / "attention-mechanism.md"
    article.write_text(article.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")

    with pytest.raises(CatalogError, match="knowledge snapshot checksum mismatch"):
        load_catalog(tmp_path)


def test_quant_knowledge_snapshot_checksum_is_enforced(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    chapter = tmp_path / "knowledge" / "quant-knowledge" / "booklet" / "01-python" / "01-numpy-ndarray-dtype-shape.md"
    chapter.write_text(chapter.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")

    with pytest.raises(CatalogError, match="quant knowledge snapshot checksum mismatch"):
        load_catalog(tmp_path)


def test_quant_sync_rejects_numbered_h1_titles(tmp_path: Path) -> None:
    source = tmp_path / "source"
    shutil.copytree(SITE_ROOT / "content" / "knowledge" / "quant-knowledge", source)
    chapter = source / "booklet" / "01-python" / "01-numpy-ndarray-dtype-shape.md"
    text = chapter.read_text(encoding="utf-8")
    chapter.write_text(text.replace("# ", "# 1. ", 1), encoding="utf-8")

    with pytest.raises(KnowledgeSyncError, match="must not repeat its filename sequence"):
        sync_quant_knowledge_snapshot(source, tmp_path / "destination")


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


def test_study_decision_state_must_be_supported(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    studies = (tmp_path / "studies.yaml").read_text(encoding="utf-8")
    studies = studies.replace("decision_state: retain", "decision_state: uncertain", 1)
    (tmp_path / "studies.yaml").write_text(studies, encoding="utf-8")
    with pytest.raises(CatalogError, match="unsupported decision_state uncertain"):
        load_catalog(tmp_path)


def test_metric_bearing_study_requires_valid_primary_metric(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    studies = (tmp_path / "studies.yaml").read_text(encoding="utf-8")
    studies = studies.replace("primary_metric: test-pooled-ic", "primary_metric: missing-metric", 1)
    (tmp_path / "studies.yaml").write_text(studies, encoding="utf-8")
    with pytest.raises(CatalogError, match="primary_metric references unknown metric missing-metric"):
        load_catalog(tmp_path)


def test_homepage_metric_reference_must_resolve(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    highlights = (tmp_path / "highlights.yaml").read_text(encoding="utf-8")
    highlights = highlights.replace("metric: etf-test-ic", "metric: missing-metric", 1)
    (tmp_path / "highlights.yaml").write_text(highlights, encoding="utf-8")
    with pytest.raises(CatalogError, match="references unknown metric index500-clean-benchmark/missing-metric"):
        load_catalog(tmp_path)


def test_homepage_chart_series_must_match_bins(tmp_path: Path) -> None:
    _copy_catalog(tmp_path)
    highlights = (tmp_path / "highlights.yaml").read_text(encoding="utf-8")
    highlights = highlights.replace(
        "values: [-8.054, -3.855, -2.834, 3.612, 4.521, 7.072]",
        "values: [-8.054, -3.855]",
        1,
    )
    (tmp_path / "highlights.yaml").write_text(highlights, encoding="utf-8")
    with pytest.raises(CatalogError, match="one value for every bin"):
        load_catalog(tmp_path)
