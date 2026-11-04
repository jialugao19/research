---
title: B+VWAP paired baseline | reference-baseline-v2-bvwap-comparison-0717
date: 2026-11-03
summary: 相同 paired_vwap_valid 样本上 VWAP 相对 close 的三个 paired seed IC 增量均为正. seed13 为 0.0744533729 vs 0.0605061430. 成本后结果仍负.
tags:
- prediction-nn
- registry-sync
- historical-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** 相同 paired_vwap_valid 样本上 VWAP 相对 close 的三个 paired seed IC 增量均为正. seed13 为 0.0744533729 vs 0.0605061430. 成本后结果仍负.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

### Executive Summary

candidate

B+VWAP candidate seed13

candidate_test_pooled_ic

0.074453

candidate_test_rank_ic

0.045022

seed13_delta_vs_close_pooled_ic

0.013947

seed13_delta_vs_close_relative

23.05%

frozen_reference_test_pooled_ic

0.070345

portfolio_input

eval_test projection compatibility manifest; no native inference_test manifest in source runs

- B+VWAP 的核心判断应看 paired close-control: seed7/11/13 的 pooled IC 与 rank IC 全部为正增益. 
- Frozen reference baseline 是稳定锚点, 但 B+VWAP paired universe 过滤了 VWAP-invalid rows, 不能把 headline IC 直接解释成全样本 total uplift. 
- Portfolio backtest 回答 execution 后是否仍成立; 本报告标注 compat input, 是因为源 run 没有原生 inference_test manifest. 

## 研究背景与目标

本报告围绕B+VWAP paired baseline整理原始研究证据. 当前材料对应 registry report `reference-baseline-v2-bvwap-comparison-0717`, 来源SHA256为 `002ee26e931016f342447e39a9b182f2126d3453f32c3e1b7813de35e44dd3b2`. 原报告的实验方法, 图表, 结果和解释保留在下文.

## 数据与方法

实验身份为 `reference-baseline-v2`. Split, label, sampler, feature与checkpoint定义按原报告记录, 不从其他实验借用缺失字段. 汇总入口见[全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

## 主要结果

| 记录项 | 当前解释 |
| --- | --- |
| 实验 | reference-baseline-v2 |
| 报告类型 | comparison_report_html |
| 历史状态 | 历史成功 |
| 证据 | reference-baseline-v2-bvwap-comparison-0717 |

Frozen reference metrics, paired VWAP label deltas, and execution-aware portfolio backtest evidence.

2026-07-17 23:28:19

### Frozen / Candidate Full-Report Metrics

| experiment | role | comparison_scope | label_endpoint | selected_iter | selection_value | train_full_pooled_ic | test_pooled_ic | test_rank_ic | test_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen reference baseline | historical_anchor | full reference test universe | close_close | 20,000 | 0.048036 | 0.196803 | 0.070345 | 0.051239 | 176,945,440 |
| B robust selector seed7 | reference-baseline-v2 B | full reference test universe | close_close | 20,000 | 0.048036 | 0.196803 | 0.070345 | 0.051239 | 176,945,440 |
| C lr=0.009 seed7 | negative LR arm | full reference test universe | close_close | 60,000 | 0.002133 | n/a | -0.000447 | -0.000183 | 176,945,440 |
| B+VWAP candidate seed13 | B+VWAP candidate | paired VWAP-valid rows | vwap_vwap | 10,000 | 0.043652 | 0.181864 | 0.074453 | 0.045022 | 108,670,112 |

```text
Comparability caveat: reference/B/C use the full reference test universe; B+VWAP uses paired VWAP-valid rows. Use this table for orientation, not as the sole promotion criterion.
```

### Paired VWAP Label Comparison

| seed | close_iter | vwap_iter | close_pooled_ic | vwap_pooled_ic | delta_pooled_ic | relative_pooled_ic | close_rank_ic | vwap_rank_ic | delta_rank_ic | test_rows | row_universe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7 | 10,000 | 30,000 | 0.061927 | 0.067067 | 0.005140 | 8.30% | 0.032660 | 0.043342 | 0.010683 | 108,670,112 | byte-match verified in task result |
| 11 | 10,000 | 10,000 | 0.061934 | 0.073977 | 0.012043 | 19.44% | 0.035684 | 0.043113 | 0.007429 | 108,670,112 | byte-match verified in task result |
| 13 | 10,000 | 10,000 | 0.060506 | 0.074453 | 0.013947 | 23.05% | 0.033809 | 0.045022 | 0.011213 | 108,670,112 | byte-match verified in task result |

### Full-Report Grouped Robustness Metrics

### Grouped pooled Pearson IC

| group | B_seed7 | close_paired_seed13 | reference | vwap_paired_seed13 |
| --- | --- | --- | --- | --- |
| liquidity_high | 0.068194 | 0.074797 | 0.068194 | 0.091370 |
| liquidity_low | 0.074946 | 0.032553 | 0.074946 | 0.039544 |
| prediction_high_p10 | 0.053991 | 0.053217 | 0.053991 | 0.072584 |
| prediction_low_p90 | 0.064751 | 0.057359 | 0.064751 | 0.067373 |
| regime_high | 0.072499 | 0.070720 | 0.072499 | 0.082577 |
| regime_low | 0.067108 | 0.050812 | 0.067108 | 0.066683 |
| regime_mid | 0.071006 | 0.057200 | 0.071006 | 0.072016 |
| volatility_high | 0.078884 | 0.067736 | 0.078884 | 0.084029 |
| volatility_low | 0.042855 | 0.030406 | 0.042855 | 0.037496 |

### Grouped pooled rank IC

| group | B_seed7 | close_paired_seed13 | reference | vwap_paired_seed13 |
| --- | --- | --- | --- | --- |
| liquidity_high | 0.046310 | 0.042300 | 0.046310 | 0.056590 |
| liquidity_low | 0.057002 | 0.024984 | 0.057002 | 0.032934 |
| prediction_high_p10 | 0.035894 | 0.010195 | 0.035894 | 0.025689 |
| prediction_low_p90 | 0.047115 | 0.034422 | 0.047115 | 0.043387 |
| regime_high | 0.050523 | 0.037702 | 0.050523 | 0.044834 |
| regime_low | 0.045748 | 0.029434 | 0.045748 | 0.041689 |
| regime_mid | 0.057355 | 0.032754 | 0.057355 | 0.047668 |
| volatility_high | 0.059820 | 0.042384 | 0.059820 | 0.057505 |
| volatility_low | 0.044316 | 0.024099 | 0.044316 | 0.030489 |

### Important Stock Pool Metrics

### Important-pool Pearson IC

| pool | B_seed7 | close_paired_seed13 | reference | vwap_paired_seed13 |
| --- | --- | --- | --- | --- |
| csi1000_etf_sh | 0.035256 | 0.038302 | 0.035256 | 0.048990 |
| csi300_etf_sh | 0.021147 | 0.022735 | 0.021147 | 0.032176 |
| csi500_etf_sh | 0.020211 | 0.024960 | 0.020211 | 0.031121 |

### Important-pool rank IC

| pool | B_seed7 | close_paired_seed13 | reference | vwap_paired_seed13 |
| --- | --- | --- | --- | --- |
| csi1000_etf_sh | 0.022304 | 0.019334 | 0.022304 | 0.028097 |
| csi300_etf_sh | 0.014949 | 0.012546 | 0.014949 | 0.021089 |
| csi500_etf_sh | 0.015544 | 0.013063 | 0.015544 | 0.020724 |

### Portfolio Execution-Aware Backtest

| experiment | status | gross_ann_return | gross_sharpe | gross_cum_return | gross_max_drawdown | net10m_ann_return | net10m_sharpe | mean_daily_turnover | mean_fill_ratio | capacity_10bps | portfolio_report_html |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Close-control paired seed13 | available | 454.24% | 54.042199 | 100.00% | 0.00% | -99.56% | -88.841105 | 1293.38% | 78.18% | 47939.999671 | [artifact-root]/nn/reference-baseline-v2/bvwap-candidate-comparison-0717/portfolio_backtests/B-close-paired-vwap-valid-seed13/research_report.html |
| B+VWAP candidate seed13 | available | 540.81% | 59.768036 | 112.10% | 0.00% | -99.48% | -87.490760 | 1311.66% | 78.10% | 47169.885050 | [artifact-root]/nn/reference-baseline-v2/bvwap-candidate-comparison-0717/portfolio_backtests/B-vwap-vwap-paired-seed13/research_report.html |

```text
Backtest contract: top/bottom 10%, long+short, VWAP entry/exit, entry_delay=1 bar, holding=10 bars, spread/impact model from portfolio_backtest default config. Input is eval_test projection compatibility manifest.
```

## 限制与适用边界

相同 paired_vwap_valid 样本上 VWAP 相对 close 的三个 paired seed IC 增量均为正. seed13 为 0.0744533729 vs 0.0605061430. 成本后结果仍负. 当前artifact可得性只影响复现, 不作为历史成功/失败判据. 只有matched合同内的结果可以直接比较.

## 结论

本次归档保留上述历史事实. 研究结论, 推广门槛和执行限制分别解释, 不把模型无增益或净收益为负改写成实验流程失败.

## 附录

### Artifacts And Reproducibility

artifact_root

[artifact-root]/nn/reference-baseline-v2/bvwap-candidate-comparison-0717

report_markdown

[artifact-root]/nn/reference-baseline-v2/bvwap-candidate-comparison-0717/research_report/bvwap_candidate_comparison_report.md

report_html

[artifact-root]/nn/reference-baseline-v2/bvwap-candidate-comparison-0717/research_report/bvwap_candidate_comparison_report.html

repo_html

[local-workspace]/exp-nn/baseline-0715/report/0717_bvwap_candidate_comparison_report.html

portfolio_root

[artifact-root]/nn/reference-baseline-v2/bvwap-candidate-comparison-0717/portfolio_backtests

candidate_full_report

[artifact-root]/nn/reference-baseline-v2/B-vwap-vwap-paired-seed13/research_report/071714_B-vwap-vwap-paired-seed13_full_evaluation_report.html

candidate_run_root

[artifact-root]/nn/reference-baseline-v2/B-vwap-vwap-paired-seed13/date_ranges

```text
Known limitation: source B+VWAP runs did not materialize native run/inference_test/<iter>/inference_manifest.yaml. The portfolio result should be read as an execution-aware check on selected test predictions, not a final frozen inference artifact.
```
