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
    assert (output / "projects" / "prediction-nn" / "one-minute" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "one-second" / "index.html").is_file()
    assert (output / "projects" / "prediction-nn" / "l2-features" / "index.html").is_file()
    assert (output / "projects" / "deep-ml" / "index.html").is_file()
    assert (output / "projects" / "tdx-data-source" / "index.html").is_file()
    assert not (output / "projects" / "tqo-data-source" / "index.html").exists()
    assert (output / "projects" / "live-predictor" / "index.html").is_file()
    assert (output / "reports" / "prediction-nn" / "0702-l2-ablation" / "index.html").is_file()
    assert (output / "reports" / "prediction-nn" / "0702-l2-ablation-v2" / "index.html").is_file()
    assert (output / "reports" / "live-predictor" / "0805-live-predictor-quality" / "index.html").is_file()
    assert (
        output / "assets" / "report-heroes" / "0802-stock1s-gru384-v2.png"
    ).is_file()
    validate_built_site(catalog, SITE_ROOT, output, "/research/")


def test_homepage_shows_latest_report_once_per_project(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")

    index = (output / "index.html").read_text(encoding="utf-8")
    reports = (output / "reports" / "index.html").read_text(encoding="utf-8")

    assert "FEATURED RESEARCH" in index
    assert '<h1><a href="/reports/prediction-nn/0802-stock1s-gru384-v2/">Stock1s GRU384 / MLP512×512 Evaluation</a></h1>' in index
    assert "assets/report-heroes/0802-stock1s-gru384-v2.png" in index
    assert "从研究问题到" not in index
    assert "尚无公开报告的项目仍保留项目入口。" in index
    assert "39</dt><dd>实验快照" in index
    assert "每项目最新报告" in index
    assert "Stock1s GRU384 / MLP512×512 Evaluation" in index
    assert "T+1 打板策略研究报告" in index
    assert "Index500 Predict 研究报告" in index
    assert "Live Predictor 实时预测质量报告" in index
    assert "L2 Features Ablation vs Stock1m Baseline" not in index
    assert "L2 Features Ablation vs Stock1m Baseline" in reports
    assert "0702-l2-ablation-v2" in reports
    assert "reports/prediction-nn/0702-l2-ablation/" not in reports


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
    assert "0.09842" in one_second
    assert "test 参与选择" in one_second
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
    assert "OBJECTIVE" not in one_minute
    assert "可支持决策" not in one_minute
    assert "数据结构" in one_minute
    assert "批次 × 时间步 × 特征" in one_minute
    assert "研究问题与方法" in one_minute
    assert "观察结果" in one_minute
    assert "分钟级模型结构最终评估" in one_minute
    assert "旧默认模型使用 GRU384×2" in one_minute
    assert "基线与模型设计" in one_minute
    assert "数据、标签与样本处理" in one_minute
    assert "验证、选择与稳健性" in one_minute
    assert "特征扩展与组合验证" in one_minute
    assert "数据与信号链路值得继续研究" in one_second


def test_catalog_json_keeps_internal_presentation_fields_private(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")
    payload = (output / "catalog.json").read_text(encoding="utf-8")
    assert '"charts"' not in payload
    assert '"schema_version": 2' in payload
    assert '"revision_of": "0702-l2-ablation"' in payload
    assert payload.count('"is_current": true') == 7


def test_catalog_json_excludes_private_evidence_paths(tmp_path: Path) -> None:
    catalog = load_catalog(SITE_ROOT / "content")
    output = tmp_path / "site"
    build_site(catalog, SITE_ROOT, output, "/")
    payload = (output / "catalog.json").read_text(encoding="utf-8")
    assert "/home/" not in payload
    assert "/data-cache/" not in payload
    assert "evidence_ref" not in payload
