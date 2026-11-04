---
title: 标签与 prediction calibration | prediction-calibration-label-noise-070814
date: 2026-11-03
summary: 相同 paired_vwap_valid 总体上的 A2 VWAP endpoint 改动提高 IC, RankIC 和 spread. A3 robust-label 方案未通过 calibration promotion gate, 属于已完成的负结果.
tags:
- prediction-nn
- registry-sync
- historical-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** 相同 paired_vwap_valid 总体上的 A2 VWAP endpoint 改动提高 IC, RankIC 和 spread. A3 robust-label 方案未通过 calibration promotion gate, 属于已完成的负结果.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

### Executive Summary

本报告汇总当前 Stage A2/A3 标签噪声实验. 实验目标是判断更低噪声的监督标签或更稳健的标签处理, 能否改善 prediction-calibration, 同时不牺牲 held-out test pooled IC, rank IC 和 top-bottom signal spread. 

A2 使用 paired_vwap_valid universe, 把 close-close 和 vwap-vwap 放在完全相同的 supervised rows 上比较. A3 保留 close-close 标签定义, 测试 realized-vol normalized target, clip/floor 和高冲击样本 soft downweight. 

artifact completeness

6/6 complete

six configured variants have full reports and required summary artifacts

A2 pooled IC delta

+0.022878

vwap_vwap_intersection minus control_close_intersection

A2 calibration error delta

-0.164772

negative is better for abs(slope - 1)

A3 promoted candidates

0/3

candidate must improve calibration error without hurting IC, rank IC guardrail, or spread

- A2 paired VWAP is the only treatment that improves pooled IC, rank IC, spread, and calibration slope absolute error in this run.
- A3 robust-label treatments do not pass the promotion gate because calibration slope absolute error worsens for all three candidates.
- The Stage A2/A3 control is comparable to the Stage A baseline on split, rows, seed, horizon, label transform, and feature fingerprints.
- The current report is read-only over existing artifacts; it does not rerun training, evaluation, or report metrics.

## 研究背景与目标

本报告围绕标签与 prediction calibration整理原始研究证据. 当前材料对应 registry report `prediction-calibration-label-noise-070814`, 来源SHA256为 `5f5bbfe21a42c0873b1531249397762187d20a84399a90f220aa1bb3a42fa3ba`. 原报告的实验方法, 图表, 结果和解释保留在下文.

## 数据与方法

实验身份为 `prediction-calibration`. Split, label, sampler, feature与checkpoint定义按原报告记录, 不从其他实验借用缺失字段. 汇总入口见[全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

## 主要结果

| 记录项 | 当前解释 |
| --- | --- |
| 实验 | prediction-calibration |
| 报告类型 | comparison_report_html |
| 历史状态 | 历史成功 |
| 证据 | prediction-calibration-label-noise-070814 |

Stage A2/A3: lowering label noise while preserving ranking quality and tradable spread

Generated on 2026-07-08 16:15:49 CST

### 实验设计

### A2 成对样本空间标签测试

本组实验从原始 close-close baseline 出发, 先定义基准样本空间 `U_close = {i: Close_entry(i), Close_exit(i) finite}` , 对应标签为 `y_close_i = log(Close_exit(i)) - log(Close_entry(i))` . 为了测试 VWAP 端点是否降低标签噪声, 再定义 `VWAP_t = Amount_t / Vol_t` (要求 `Vol_t > 0` ), 以及 `U_vwap = {i: VWAP_entry(i), VWAP_exit(i) finite}` . A2 实际比较空间固定为 `U_pair = U_close ∩ U_vwap` . 

因此 A2 不直接把完整 baseline `U_close` 与 VWAP 标签比较, 而是先把 close 对照组也裁剪到 `U_pair` . 这样两个 A2 变体的 train/val/test rows 完全一致, 指标差异主要来自端点价格定义, 而不是 VWAP 有效性筛选带来的样本空间差异. 

实验组构成: 

- control_close_intersection : A2 对照组. 它继承 baseline 的 close-close 标签 y_close , 但样本空间从完整 U_close 收缩到 U_pair . 被删除的是 close 标签有效, 但 VWAP entry 或 exit 端点无效的 rows. 这个组用于估计"只做 paired universe 裁剪"后的 close baseline. 
- vwap_vwap_intersection : A2 实验组. 样本空间与 control_close_intersection 完全相同, 仍是 U_pair , 不额外删除样本, 不改变样本权重; 唯一变化是训练和评估标签换成 y_vwap_i = log(VWAP_exit(i)) - log(VWAP_entry(i)) . 因此它隔离的是 endpoint label noise, 而不是 sample selection. 

| 实验组 | 相对 baseline 的样本空间处理 | 标签/权重处理 | 可比性含义 |
| --- | --- | --- | --- |
| control_close_intersection | U_close -> U_pair = U_close ∩ U_vwap; 删除 VWAP 端点无效 rows | 保留 y_close; w_i = 1 | A2 close 对照组, row universe 与 VWAP 实验组一致 |
| vwap_vwap_intersection | 继续使用同一个 U_pair; 不再做额外过滤 | 改用 y_vwap; w_i = 1 | 与 A2 对照组 rows 一致, 差异集中在端点标签 |

### A3 稳健标签处理

本组实验以同一输出根目录下的 `control_close` 作为 A3 baseline. A3 不改变价格端点, 仍使用 raw close-close 标签 `y_raw = y_close` 做最终 raw-scale evaluation; 候选只在训练目标或训练样本权重上做稳健化处理. 候选只有在 calibration slope absolute error 下降, pooled IC 与 top-bottom spread 不下降, 且 rank IC delta 不低于预设 guardrail 时, 才会进入后续多 seed 验证. 

对涉及波动率归一化的实验, 定义 60 分钟 realized-vol scale 为 `sigma_60(i)` , 有效样本空间为 `U_vol = {i in U_close: sigma_60(i) finite}` , 训练目标为 `z_i = clip(y_raw_i / max(sigma_60(i), 1e-4), -5, 5)` . evaluation 仍使用 raw `label_raw` , 所以 report 中的 IC, spread 和 calibration 仍可回到原始收益率尺度解释. 

实验组构成: 

- control_close : A3 基准组. 样本空间为完整 U_close , 不做额外 sample filter, 不做 sample downweight,  w_i = 1 . 它保留 baseline 的 close-close 标签和 pooled z-score 训练方式, 用于衡量 robust label treatment 是否真的改善 raw-scale evaluation. 
- volnorm60_floor_clip : A3 实验组 1. 样本空间从 U_close 收缩到 U_vol , 即删除无法计算 60 分钟 realized-vol scale 的 rows; 不做样本降权,  w_i = 1 . 训练目标改为 z_i , scale floor 设为 1e-4 , normalized label clip 到 [-5, 5] , 但 evaluation 仍回到 raw label_raw . 
- impact_downweight : A3 实验组 2. 样本空间保持完整 U_close , 不删除低 ADV/高 impact rows; 标签仍为 y_close . 处理方式是把这些疑似高噪声样本的 loss 权重降为 w_i in [0.25, 1] , 即 soft treatment, 而不是 hard filtering. 
- volnorm60_floor_clip_impact_downweight : A3 实验组 3. 样本空间同波动率实验, 为 U_vol ; 训练目标同 volnorm60_floor_clip 的 z_i ; 同时叠加 adv20_impact_soft 权重 w_i in [0.25, 1] . 它检验"缩小到 volatility-scale-valid rows + 稳健目标 + 高冲击样本降权"是否互补. 

| 实验组 | 相对 baseline 的样本空间处理 | 训练目标 | 样本权重 | 与 baseline 对比时的注意点 |
| --- | --- | --- | --- | --- |
| control_close | U_close; 无额外过滤 | y_close / pooled z-score | w_i = 1 | A3 same-root baseline, rows 与原 close baseline 一致 |
| volnorm60_floor_clip | U_close -> U_vol; 删除 sigma_60 无效 rows | z_i = clip(y_raw / max(sigma_60, 1e-4), -5, 5) | w_i = 1 | 同时改变 row universe 和 target scale, 需避免把筛样本效果误判为纯标签变换效果 |
| impact_downweight | 仍为 U_close; 不删除样本 | y_close / pooled z-score | w_i in [0.25, 1] | rows 与 control_close 一致, 主要隔离 soft sample-quality weighting |
| volnorm60_floor_clip_impact_downweight | U_close -> U_vol; 同 volnorm valid subset | z_i = clip(y_raw / max(sigma_60, 1e-4), -5, 5) | w_i in [0.25, 1] | 组合变体同时改变样本空间, 训练目标和权重, 解释时需拆分归因 |

### Detailed Experiment Methods

下表把每个实验的可操作方法展开到同一张表里. 核心区分是: A2 只改 endpoint price 并固定 supervised universe; A3 只保留 close-close price label, 改训练 target 或样本权重. 

| variant | stage | comparison_role | hypothesis | supervised_universe | label_definition | label_treatment | sample_weight | evaluation_target | test_rows | selected_iter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| control_close | Baseline | same-root A3 baseline and Stage A2/A3 implementation-drift control | Keep the production close-close label unchanged. | all valid close-close supervised rows | log Close[t+horizon] - log Close[t+entry_lag] | pooled z-score target; no volatility scaling; no clipping | all weights 1.0 | raw close-close forward return via label_raw support fields | 241,788,800 | 90,000 |
| control_close_intersection | A2 control | paired control for vwap_vwap_intersection | Hold the paired VWAP-valid row universe fixed while retaining close-close labels. | paired_vwap_valid rows where close and VWAP endpoints are both valid | log Close[t+horizon] - log Close[t+entry_lag] | pooled z-score target; no volatility scaling; no clipping | all weights 1.0 | raw close-close forward return | 221,224,041 | 30,000 |
| vwap_vwap_intersection | A2 candidate | endpoint-noise candidate | VWAP endpoints reduce microstructure noise relative to close endpoints. | same paired_vwap_valid rows as control_close_intersection | log VWAP[t+horizon] - log VWAP[t+entry_lag] | pooled z-score target; no volatility scaling; no clipping | all weights 1.0 | raw VWAP forward return | 221,224,041 | 10,000 |
| volnorm60_floor_clip | A3 candidate | robust target candidate | Normalize returns by recent realized volatility to stabilize noisy targets. | rows with valid realized-vol scale and close-close label | close-close raw return divided by 60-minute realized volatility | realized_vol_60m scale, floor 1e-4, normalized label clipped at +/-5 | all weights 1.0 | raw unscaled close-close label_raw | 227,855,689 | 10,000 |
| impact_downweight | A3 candidate | soft sample-quality candidate | Low-ADV/high-impact samples are noisier and should contribute less to training. | all valid close-close supervised rows | log Close[t+horizon] - log Close[t+entry_lag] | pooled z-score target; no volatility scaling; no clipping | adv20_impact_soft; low-ADV/high-impact rows downweighted to min 0.25 | raw close-close forward return | 241,788,800 | 10,000 |
| volnorm60_floor_clip_impact_downweight | A3 candidate | combined robust target plus soft sample-quality candidate | Combine volatility-normalized clipped targets with high-impact sample downweighting. | rows with valid realized-vol scale and close-close label | close-close raw return divided by 60-minute realized volatility | realized_vol_60m scale, floor 1e-4, normalized label clipped at +/-5 | adv20_impact_soft; low-ADV/high-impact rows downweighted to min 0.25 | raw unscaled close-close label_raw | 227,855,689 | 10,000 |

### Screening Method And Comparison Results

筛选逻辑分两层: A2 先回答 VWAP endpoint 是否在 paired universe 下优于 close endpoint; A3 则要求 robust label treatment 同时改善 calibration 且不损伤排序和 spread. 负的 calibration error delta 表示改善. 

| screen | baseline | candidate | selection_method | pass_rule | test_ic_delta | rank_ic_delta | spread_delta_bps | calibration_error_delta | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A2 paired VWAP endpoint | control_close_intersection | vwap_vwap_intersection | compare on identical paired_vwap_valid supervised rows | useful if IC/rank IC/spread improve and calibration abs error declines | +0.022878 | +0.011093 | +1.978282 | -0.164772 | PASS |
| A3 robust label treatment | control_close | volnorm60_floor_clip | compare each candidate against same-root control_close | promote only if calibration abs error improves without hurting IC, rank IC guardrail, or spread | -0.001392 | -0.000388 | +0.803454 | +0.322365 | FAIL |
| A3 robust label treatment | control_close | impact_downweight | compare each candidate against same-root control_close | promote only if calibration abs error improves without hurting IC, rank IC guardrail, or spread | +0.004629 | +0.000332 | +1.092505 | +0.244175 | FAIL |
| A3 robust label treatment | control_close | volnorm60_floor_clip_impact_downweight | compare each candidate against same-root control_close | promote only if calibration abs error improves without hurting IC, rank IC guardrail, or spread | -0.002962 | -0.000222 | +0.715641 | +0.3195 | FAIL |

### Results

### Six-variant summary

| variant | status | selected_iter | label_price_mode | label_scale_type | label_scale_floor | label_clip_abs | sample_filter_mode | sample_weight_mode | train_rows | val_rows | test_rows | test_pooled_ic | test_pooled_rank_ic | signal_top_bottom_spread_bps | calibration_slope | calibration_slope_abs_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| control_close | complete | 90,000 | close_close | none |  | 0 | none | none | 768,564,829 | 43,553,840 | 241,788,800 | 0.066487 | 0.046637 | 8.100271 | 0.749732 | 0.250268 |
| control_close_intersection | complete | 30,000 | close_close | none |  | 0 | paired_vwap_valid | none | 696,407,167 | 41,098,436 | 221,224,041 | 0.053277 | 0.033709 | 7.507986 | 0.314561 | 0.685439 |
| vwap_vwap_intersection | complete | 10,000 | vwap_vwap | none |  | 0 | paired_vwap_valid | none | 696,407,167 | 41,098,436 | 221,224,041 | 0.076156 | 0.044802 | 9.486268 | 0.479333 | 0.520667 |
| volnorm60_floor_clip | complete | 10,000 | close_close | realized_vol_60m | 0.0001 | 5 | none | none | 722,043,909 | 41,063,624 | 227,855,689 | 0.065095 | 0.046249 | 8.903724 | 0.427367 | 0.572633 |
| impact_downweight | complete | 10,000 | close_close | none |  | 0 | none | adv20_impact_soft | 768,564,829 | 43,553,840 | 241,788,800 | 0.071116 | 0.046969 | 9.192775 | 0.505557 | 0.494443 |
| volnorm60_floor_clip_impact_downweight | complete | 10,000 | close_close | realized_vol_60m | 0.0001 | 5 | none | adv20_impact_soft | 722,043,909 | 41,063,624 | 227,855,689 | 0.063525 | 0.046415 | 8.815911 | 0.430232 | 0.569768 |

### A2 paired delta

| baseline | candidate | baseline_test_rows | candidate_test_rows | test_pooled_ic_delta | test_pooled_rank_ic_delta | signal_top_bottom_spread_bps_delta | calibration_slope_abs_error_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| control_close_intersection | vwap_vwap_intersection | 221,224,041 | 221,224,041 | +0.022878 | +0.011093 | +1.978282 | -0.164772 |

### A3 candidate deltas

| baseline | candidate | baseline_test_rows | candidate_test_rows | test_pooled_ic_delta | test_pooled_rank_ic_delta | signal_top_bottom_spread_bps_delta | calibration_slope_abs_error_delta | gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| control_close | volnorm60_floor_clip | 241,788,800 | 227,855,689 | -0.001392 | -0.000388 | +0.803454 | +0.322365 | FAIL |
| control_close | impact_downweight | 241,788,800 | 241,788,800 | +0.004629 | +0.000332 | +1.092505 | +0.244175 | FAIL |
| control_close | volnorm60_floor_clip_impact_downweight | 241,788,800 | 227,855,689 | -0.002962 | -0.000222 | +0.715641 | +0.3195 | FAIL |

### Interpretation

**Observed A2 result:** `vwap_vwap_intersection` beats its paired close-control on pooled IC, rank IC, top-bottom signal spread, and calibration slope absolute error. This supports VWAP endpoints as the current promising label-noise direction.

**Observed A3 result:** `impact_downweight` improves IC and spread, but its calibration slope absolute error worsens. The vol-normalized variants also worsen calibration error and do not improve pooled IC. None should be promoted under the configured gate.

**Scope:** This report is a current artifact summary for Stage A2/A3. It does not claim statistical significance across seeds; multi-seed robustness remains the next evidence layer if A2 is promoted.

### Config Snapshot

```text
title: Prediction Calibration Label-Noise Research Report
subtitle: 'Stage A2/A3: lowering label noise while preserving ranking quality and
  tradable spread'
stage_a2_a3_root: [artifact-root]/nn/prediction-calibration-stage-a2-a3
comparison_dir: [artifact-root]/nn/prediction-calibration-stage-a2-a3/stage_a2_a3_comparison
output_dir: [artifact-root]/nn/prediction-calibration-stage-a2-a3/label_noise_research_report
repo_report_dir: report
stable_filename: label_noise_prediction_calibration_report.html
manifest_filename: label_noise_prediction_calibration_report_manifest.yaml
baseline_stage_a_control_meta: [artifact-root]/nn/prediction-calibration-stage-a/control_close/date_ranges/artifacts/npz/meta.yaml
stage_a2_a3_control_meta: [artifact-root]/nn/prediction-calibration-stage-a2-a3/control_close/date_ranges/artifacts/npz/meta.yaml
baseline_comparability_doc: experiments/prediction_calibration/STAGE_A2_A3_BASELINE_COMPARABILITY.md
outline_path: experiments/prediction_calibration/LABEL_NOISE_REPORT_OUTLINE.md
variants:
- control_close
- control_close_intersection
- vwap_vwap_intersection
- volnorm60_floor_clip
- impact_downweight
- volnorm60_floor_clip_impact_downweight
a2_pair:
  control: control_close_intersection
  candidate: vwap_vwap_intersection
a3_baseline: control_close
a3_candidates:
- volnorm60_floor_clip
- impact_downweight
- volnorm60_floor_clip_impact_downweight
rank_ic_guardrail: -0.005
```

## 限制与适用边界

相同 paired_vwap_valid 总体上的 A2 VWAP endpoint 改动提高 IC, RankIC 和 spread. A3 robust-label 方案未通过 calibration promotion gate, 属于已完成的负结果. 当前artifact可得性只影响复现, 不作为历史成功/失败判据. 只有matched合同内的结果可以直接比较.

### Comparability Audit

### Stage A baseline control vs Stage A2/A3 control

| field | stage_a_control | stage_a2_a3_control | status |
| --- | --- | --- | --- |
| start_trade_date | 20210104 | 20210104 | match |
| end_trade_date | 20241231 | 20241231 | match |
| train_days | 727 | 727 | match |
| val_days | 37 | 37 | match |
| test_days | 205 | 205 | match |
| seed | 7 | 7 | match |
| horizon_minutes | 10 | 10 | match |
| label_entry_lag_minutes | 1 | 1 | match |
| sample_stocks_per_minute | 0 | 0 | match |
| label_norm | pooled_zscore | pooled_zscore | match |
| norm_fit_scope | train_only | train_only | match |
| train_rows | 768564829 | 768564829 | match |
| val_rows | 43553840 | 43553840 | match |
| test_rows | 241788800 | 241788800 | match |
| feature_names_hash | 04dc970f1211 | 04dc970f1211 | match |
| feature_transform_hash | 19ed4e5f99cb | 19ed4e5f99cb | match |

### Shared Stage A2/A3 invariants

| field | value | stage_a2_a3_variants |
| --- | --- | --- |
| start_trade_date | 20210104 | all match |
| end_trade_date | 20241231 | all match |
| train_days | 727 | all match |
| val_days | 37 | all match |
| test_days | 205 | all match |
| seed | 7 | all match |
| horizon_minutes | 10 | all match |
| label_entry_lag_minutes | 1 | all match |
| sample_stocks_per_minute | 0 | all match |
| label_norm | pooled_zscore | all match |
| norm_fit_scope | train_only | all match |
| feature_names_hash | 04dc970f1211 | all match |
| feature_transform_hash | 19ed4e5f99cb | all match |

Rows can differ across A2/A3 variants when the design intentionally changes endpoint validity, label scale availability, or sample treatment. The invariant table verifies the common data/model controls, not equality of every supervised row count across all designs.

## 结论

本次归档保留上述历史事实. 研究结论, 推广门槛和执行限制分别解释, 不把模型无增益或净收益为负改写成实验流程失败.

## 附录

### Artifact Completeness

| variant | status | missing_count | full_report_count | full_report_path |
| --- | --- | --- | --- | --- |
| control_close | complete | 0 | 1 | [artifact-root]/nn/prediction-calibration-stage-a2-a3/control_close/research_report/070723_control_close_full_evaluation_report.html |
| control_close_intersection | complete | 0 | 1 | [artifact-root]/nn/prediction-calibration-stage-a2-a3/control_close_intersection/research_report/070810_control_close_intersection_full_evaluation_report.html |
| vwap_vwap_intersection | complete | 0 | 1 | [artifact-root]/nn/prediction-calibration-stage-a2-a3/vwap_vwap_intersection/research_report/070804_vwap_vwap_intersection_full_evaluation_report.html |
| volnorm60_floor_clip | complete | 0 | 1 | [artifact-root]/nn/prediction-calibration-stage-a2-a3/volnorm60_floor_clip/research_report/070805_volnorm60_floor_clip_full_evaluation_report.html |
| impact_downweight | complete | 0 | 1 | [artifact-root]/nn/prediction-calibration-stage-a2-a3/impact_downweight/research_report/070801_impact_downweight_full_evaluation_report.html |
| volnorm60_floor_clip_impact_downweight | complete | 0 | 1 | [artifact-root]/nn/prediction-calibration-stage-a2-a3/volnorm60_floor_clip_impact_downweight/research_report/070811_volnorm60_floor_clip_impact_downweight_full_evaluation_report.html |

### Artifact Index

- comparison csv: [artifact-root]/nn/prediction-calibration-stage-a2-a3/stage_a2_a3_comparison/stage_a_summary.csv
- comparison markdown: [artifact-root]/nn/prediction-calibration-stage-a2-a3/stage_a2_a3_comparison/stage_a_summary.md
- comparison yaml: [artifact-root]/nn/prediction-calibration-stage-a2-a3/stage_a2_a3_comparison/stage_a_summary.yaml
- baseline comparability doc: experiments/prediction_calibration/STAGE_A2_A3_BASELINE_COMPARABILITY.md
- report outline: experiments/prediction_calibration/LABEL_NOISE_REPORT_OUTLINE.md
- report config: [local-workspace]/exp-nn/prediction-calibration/experiments/prediction_calibration/label_noise_report.yaml
- stable html: [artifact-root]/nn/prediction-calibration-stage-a2-a3/label_noise_research_report/label_noise_prediction_calibration_report.html
- timestamped html: [artifact-root]/nn/prediction-calibration-stage-a2-a3/label_noise_research_report/070814_label_noise_prediction_calibration_report.html
- repo stable mirror: [local-workspace]/exp-nn/prediction-calibration/report/label_noise_prediction_calibration_report.html
- repo timestamped mirror: [local-workspace]/exp-nn/prediction-calibration/report/070814_label_noise_prediction_calibration_report.html
- manifest: [artifact-root]/nn/prediction-calibration-stage-a2-a3/label_noise_research_report/label_noise_prediction_calibration_report_manifest.yaml
- control_close full report: [artifact-root]/nn/prediction-calibration-stage-a2-a3/control_close/research_report/070723_control_close_full_evaluation_report.html
- control_close_intersection full report: [artifact-root]/nn/prediction-calibration-stage-a2-a3/control_close_intersection/research_report/070810_control_close_intersection_full_evaluation_report.html
- vwap_vwap_intersection full report: [artifact-root]/nn/prediction-calibration-stage-a2-a3/vwap_vwap_intersection/research_report/070804_vwap_vwap_intersection_full_evaluation_report.html
- volnorm60_floor_clip full report: [artifact-root]/nn/prediction-calibration-stage-a2-a3/volnorm60_floor_clip/research_report/070805_volnorm60_floor_clip_full_evaluation_report.html
- impact_downweight full report: [artifact-root]/nn/prediction-calibration-stage-a2-a3/impact_downweight/research_report/070801_impact_downweight_full_evaluation_report.html
- volnorm60_floor_clip_impact_downweight full report: [artifact-root]/nn/prediction-calibration-stage-a2-a3/volnorm60_floor_clip_impact_downweight/research_report/070811_volnorm60_floor_clip_impact_downweight_full_evaluation_report.html
