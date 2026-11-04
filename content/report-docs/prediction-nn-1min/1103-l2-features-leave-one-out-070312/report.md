---
title: L2 历史结果与归因边界 | l2-features-leave-one-out-070312
date: 2026-11-03
summary: L2 训练和评估已产生历史结果, all_fast12 观察 test IC 为0.0805. Baseline/LOO 与 only/all_fast12 的 checkpoint 候选数为11 vs 1, 因而贡献归因无效, 不等于实验流程失败.
tags:
- prediction-nn
- registry-sync
- historical-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** L2 训练和评估已产生历史结果, all_fast12 观察 test IC 为0.0805. Baseline/LOO 与 only/all_fast12 的 checkpoint 候选数为11 vs 1, 因而贡献归因无效, 不等于实验流程失败.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

### 1. Executive Summary

### Opening Narrative

这份报告比较 4 个 leave-one-group-out 实验, 用于检查 all_fast12 在移除单组 L2 feature 后的 test IC, rank IC, top-bottom spread, important pool IC 与 portfolio/backtest proxy 表现. 

每一行表示 all_fast12 移除一组特征后的剩余模型表现; 较弱的 minus 实验通常意味着被移除组更可能有贡献, 但严格边际贡献仍需与 full all_fast12 同表计算差值. 

本报告不设置 baseline 行; 所有排名都是 configured experiments 之间的横向比较, 不等价于相对 full all_fast12 的边际贡献. 

- Test pooled IC 最高的是 minus_quality, 数值为 0.0843. 
- Test pooled rank IC 最高的是 minus_depth, 数值为 0.0634. 
- Top-bottom signal spread 最高的是 minus_depth, 数值为 11.12 bps. 
- 10-minute return realization 最高的是 minus_depth, 数值为 7.93 bps. 
- Test pooled IC 最低的是 minus_spread_mid, 数值为 0.0694. 
- Portfolio cost sensitivity 使用 test-only important-pool artifact; 10bps 单边成本下的结果主要作为交易摩擦压力测试, 不直接代表可部署收益. 
- 本报告只复用已生成 CSV, YAML 与 HTML provenance, 不运行 training, 也不重新生成单实验 evaluation. 

model_class

GruMlp

shared model class when available

train_range

20210104 - 20231229 (727 days)

train split date range

val_range

20240102 - 20240229 (37 days)

validation split date range

test_range

20240301 - 20241231 (205 days)

test split date range

![Executive IC Comparison](images/figure-001.png "Executive IC Comparison")

train/test pooled IC grouped bar. 

![Executive Hit Rate Comparison](images/figure-002.png "Executive Hit Rate Comparison")

top95_hit 与 etf_top95_hit grouped bar. 

![Executive Top Prediction Return](images/figure-003.png "Executive Top Prediction Return")

最高 prediction 分组 mean label bps. 

### Main Comparison Table

| experiment | selected_checkpoint | train_pooled_ic | test_pooled_ic | top_prediction_return_bps | top95_hit | etf_top95_hit | overfit_variance_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| minus_quality | 10,000 | 0.1826 | 0.0843 | 5.57 | 44.54% | 43.77% | n/a |
| minus_imbalance | 10,000 | 0.1733 | 0.0808 | 5.35 | 44.43% | 43.73% | n/a |
| minus_depth | 20,000 | 0.2211 | 0.0787 | 5.85 | 45.30% | 44.00% | n/a |
| minus_spread_mid | 10,000 | 0.1696 | 0.0694 | 4.80 | 43.24% | 43.03% | n/a |

### Field Definitions

| field | explanation |
| --- | --- |
| experiment | 实验标识.  |
| selected_checkpoint | 最终用于 evaluation 的 checkpoint iteration.  |
| train_pooled_ic | train split 上把所有样本合并后计算的 Pearson IC.  |
| test_pooled_ic | test split 上把所有样本合并后计算的 Pearson IC.  |
| top_prediction_return_bps | 最高 prediction 分组的平均 realized target, 单位 bps.  |
| top95_hit | test split 中 prediction 最高 5% 样本内 target > 0 的比例.  |
| etf_top95_hit | important pool prediction top 5% bin 内 ETF realized return > 0 的平均比例.  |
| overfit_variance_ratio | test split prediction 方差 / target 方差; 当前 L2 单实验 artifact 未稳定输出时为 n/a.  |

## 研究背景与目标

本报告围绕L2 历史结果与归因边界整理原始研究证据. 当前材料对应 registry report `l2-features-leave-one-out-070312`, 来源SHA256为 `464ff2e873eec56c6c1ff120e1dc192033de8cc20de42eb1a4e3905b9531f463`. 原报告的实验方法, 图表, 结果和解释保留在下文.

## 数据与方法

实验身份为 `l2-features`. Split, label, sampler, feature与checkpoint定义按原报告记录, 不从其他实验借用缺失字段. 汇总入口见[全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

### 2. Experiment Setup And Data Pipeline

### 2.1. Experiment Setup

selection_metric

checkpoint_selection/score

checkpoint selection metric

selection_rule

early_top_k

checkpoint selection rule

train_days

727

shared train day count

val_days

37

shared validation day count

test_days

205

shared test day count

![Checkpoint Selection Metric](images/figure-004.png "Checkpoint Selection Metric")

selection checkpoint curve. 

![Checkpoint Rank IC](images/figure-005.png "Checkpoint Rank IC")

validation rank IC checkpoint curve. 

![Checkpoint Objective MSE](images/figure-006.png "Checkpoint Objective MSE")

validation objective MSE checkpoint curve. 

| experiment | best_iter | selection_value | checkpoint_sha256 | candidate_count | mlflow_run_id | mlflow_tracking_uri |
| --- | --- | --- | --- | --- | --- | --- |
| minus_quality | 10,000 | 0.043832 | ec58a86e53030dd6 | 11 | f08c778403dd47f9 | http://192.168.0.102:5000 |
| minus_spread_mid | 10,000 | 0.030559 | aee247610cc35473 | 11 | 6741373b39c94e9d | http://192.168.0.102:5000 |
| minus_imbalance | 10,000 | 0.042761 | 3c0e10a9c11f202e | 11 | 14e2071a6bbf487d | http://192.168.0.102:5000 |
| minus_depth | 20,000 | 0.045121 | 0f459fb83b081a87 | 11 | 136964dd78744528 | http://192.168.0.102:5000 |

### 2.2. Data Basics

| experiment | train_rows | val_rows | test_rows | feature_dim | features | label_horizon_minutes | label_entry_lag_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| minus_quality | 768,564,829 | 43,553,840 | 241,788,800 | 23 | ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean, spread_bps_last, spread_bps_mean_60s, mid_ret_60s, mid_rv_60s, imb1_last, imb5_last, imb5_mean_60s, bid_depth10_log1p, ask_depth10_log1p, minute_norm, session_minute_norm | 10 | 1 |
| minus_spread_mid | 768,564,829 | 43,553,840 | 241,788,800 | 22 | ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean, l2_obs_count, l2_missing_ratio, l2_stale_seconds, imb1_last, imb5_last, imb5_mean_60s, bid_depth10_log1p, ask_depth10_log1p, minute_norm, session_minute_norm | 10 | 1 |
| minus_imbalance | 768,564,829 | 43,553,840 | 241,788,800 | 23 | ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean, l2_obs_count, l2_missing_ratio, l2_stale_seconds, spread_bps_last, spread_bps_mean_60s, mid_ret_60s, mid_rv_60s, bid_depth10_log1p, ask_depth10_log1p, minute_norm, session_minute_norm | 10 | 1 |
| minus_depth | 768,564,829 | 43,553,840 | 241,788,800 | 24 | ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean, l2_obs_count, l2_missing_ratio, l2_stale_seconds, spread_bps_last, spread_bps_mean_60s, mid_ret_60s, mid_rv_60s, imb1_last, imb5_last, imb5_mean_60s, minute_norm, session_minute_norm | 10 | 1 |

Feature Groups

| experiment | stock_features | l2_features | time_features |
| --- | --- | --- | --- |
| minus_quality | ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean | spread_bps_last, spread_bps_mean_60s, mid_ret_60s, mid_rv_60s, imb1_last, imb5_last, imb5_mean_60s, bid_depth10_log1p, ask_depth10_log1p | minute_norm, session_minute_norm |
| minus_spread_mid | ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean | l2_obs_count, l2_missing_ratio, l2_stale_seconds, imb1_last, imb5_last, imb5_mean_60s, bid_depth10_log1p, ask_depth10_log1p | minute_norm, session_minute_norm |
| minus_imbalance | ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean | l2_obs_count, l2_missing_ratio, l2_stale_seconds, spread_bps_last, spread_bps_mean_60s, mid_ret_60s, mid_rv_60s, bid_depth10_log1p, ask_depth10_log1p | minute_norm, session_minute_norm |
| minus_depth | ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean | l2_obs_count, l2_missing_ratio, l2_stale_seconds, spread_bps_last, spread_bps_mean_60s, mid_ret_60s, mid_rv_60s, imb1_last, imb5_last, imb5_mean_60s | minute_norm, session_minute_norm |

### 2.3. Data Normalization And Cleaning

| experiment | feature_normalization | label_normalization | train_kept_rate | val_kept_rate | test_kept_rate | max_invalid_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| minus_quality | pooled_zscore | pooled_zscore | 90.98% | 90.76% | 90.76% | 4.3478% |
| minus_spread_mid | pooled_zscore | pooled_zscore | 90.98% | 90.76% | 90.76% | 4.3478% |
| minus_imbalance | pooled_zscore | pooled_zscore | 90.98% | 90.76% | 90.76% | 4.3478% |
| minus_depth | pooled_zscore | pooled_zscore | 90.98% | 90.76% | 90.76% | 4.3478% |

## 主要结果

| 记录项 | 当前解释 |
| --- | --- |
| 实验 | l2-features |
| 报告类型 | comparison_report_html |
| 历史状态 | 历史成功 |
| 证据 | l2-features-leave-one-out-070312 |

all_fast12 分别移除 quality, spread_mid, imbalance, depth 四组 L2 feature 后的横向对比; 核心指标来自 4 个 formal LOO 实验 artifacts. 

Generated on 2026-07-03 12:08:29

### 3. Signal Quality Comparison

### 3.1. IC Summary

![Pooled IC Comparison](images/figure-007.png "Pooled IC Comparison")

train/test pooled Pearson IC. 

![Pooled Rank IC Comparison](images/figure-008.png "Pooled Rank IC Comparison")

train/test pooled rank IC. 

![Train Test IC Gap](images/figure-009.png "Train Test IC Gap")

train pooled IC - test pooled IC. 

| experiment | split | pooled_ic | pooled_rank_ic | count |
| --- | --- | --- | --- | --- |
| minus_depth | test | 0.0787 | 0.0634 | 176,945,440 |
| minus_depth | train | 0.2211 | 0.1798 | 7,968,768 |
| minus_imbalance | test | 0.0808 | 0.0591 | 176,945,440 |
| minus_imbalance | train | 0.1733 | 0.1580 | 7,968,768 |
| minus_quality | test | 0.0843 | 0.0617 | 176,945,440 |
| minus_quality | train | 0.1826 | 0.1616 | 7,968,768 |
| minus_spread_mid | test | 0.0694 | 0.0541 | 176,945,440 |
| minus_spread_mid | train | 0.1696 | 0.1567 | 7,968,768 |

| field | explanation |
| --- | --- |
| split | 数据 split.  |
| pooled_ic | 合并样本后计算的 Pearson IC.  |
| pooled_rank_ic | 合并样本后计算的 Rank IC.  |
| count | 参与计算的样本数.  |

### 3.2. Prediction Bucket Quality

![Bucket Mean Label Curve](images/figure-010.png "Bucket Mean Label Curve")

signal_bucket vs mean_label_bps. 

![Bucket Hit Rate Curve](images/figure-011.png "Bucket Hit Rate Curve")

signal_bucket vs hit_rate. 

![Top Bottom Spread](images/figure-012.png "Top Bottom Spread")

top bucket - bottom bucket. 

| experiment | signal_bucket | mean_prediction | mean_label_bps | t_stat | hit_rate | row_count | top_bottom_signal_spread_bps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| minus_depth | 1 | -0.001337 | -5.28 | -375.04 | 36.26% | 17,694,544 | 11.12 |
| minus_depth | 2 | -0.000568 | -1.47 | -155.75 | 37.79% | 17,694,544 | 11.12 |
| minus_depth | 3 | -0.000367 | -0.96 | -110.57 | 37.75% | 17,694,544 | 11.12 |
| minus_depth | 4 | -0.000230 | -0.65 | -77.01 | 37.53% | 17,694,544 | 11.12 |
| minus_depth | 5 | -0.000118 | -0.39 | -46.65 | 36.96% | 17,694,544 | 11.12 |
| minus_depth | 6 | -0.000015 | -0.07 | -8.83 | 36.38% | 17,694,544 | 11.12 |
| minus_depth | 7 | 0.000092 | 0.42 | 47.58 | 37.81% | 17,694,544 | 11.12 |
| minus_depth | 8 | 0.000228 | 1.22 | 134.33 | 40.10% | 17,694,544 | 11.12 |
| minus_depth | 9 | 0.000437 | 2.39 | 241.70 | 41.66% | 17,694,544 | 11.12 |
| minus_depth | 10 | 0.001211 | 5.85 | 423.98 | 44.21% | 17,694,544 | 11.12 |
| minus_imbalance | 1 | -0.000955 | -5.08 | -375.03 | 36.87% | 17,694,544 | 10.43 |
| minus_imbalance | 2 | -0.000423 | -1.27 | -133.14 | 38.34% | 17,694,544 | 10.43 |
| minus_imbalance | 3 | -0.000249 | -0.99 | -103.90 | 37.18% | 17,694,544 | 10.43 |
| minus_imbalance | 4 | -0.000132 | -1.10 | -121.12 | 34.34% | 17,694,544 | 10.43 |
| minus_imbalance | 5 | -0.000051 | -0.28 | -31.27 | 36.75% | 17,694,544 | 10.43 |
| minus_imbalance | 6 | 0.000044 | 0.22 | 25.89 | 38.84% | 17,694,544 | 10.43 |
| minus_imbalance | 7 | 0.000154 | 0.67 | 78.77 | 39.36% | 17,694,544 | 10.43 |
| minus_imbalance | 8 | 0.000284 | 1.29 | 144.52 | 40.09% | 17,694,544 | 10.43 |
| minus_imbalance | 9 | 0.000469 | 2.25 | 230.40 | 41.20% | 17,694,544 | 10.43 |
| minus_imbalance | 10 | 0.001115 | 5.35 | 398.05 | 43.49% | 17,694,544 | 10.43 |
| minus_quality | 1 | -0.000966 | -5.49 | -420.64 | 36.18% | 17,694,544 | 11.06 |
| minus_quality | 2 | -0.000436 | -1.66 | -179.48 | 37.54% | 17,694,544 | 11.06 |
| minus_quality | 3 | -0.000242 | -1.11 | -125.09 | 37.66% | 17,694,544 | 11.06 |
| minus_quality | 4 | -0.000111 | -1.06 | -121.48 | 35.85% | 17,694,544 | 11.06 |
| minus_quality | 5 | -0.000023 | -0.53 | -60.99 | 35.39% | 17,694,544 | 11.06 |
| minus_quality | 6 | 0.000069 | 0.35 | 38.49 | 38.32% | 17,694,544 | 11.06 |
| minus_quality | 7 | 0.000186 | 0.96 | 107.25 | 39.92% | 17,694,544 | 11.06 |
| minus_quality | 8 | 0.000326 | 1.56 | 173.39 | 40.54% | 17,694,544 | 11.06 |
| minus_quality | 9 | 0.000517 | 2.46 | 250.31 | 41.48% | 17,694,544 | 11.06 |
| minus_quality | 10 | 0.001261 | 5.57 | 393.16 | 43.57% | 17,694,544 | 11.06 |
| minus_spread_mid | 1 | -0.000947 | -4.46 | -355.48 | 37.26% | 17,694,544 | 9.25 |
| minus_spread_mid | 2 | -0.000414 | -1.46 | -158.05 | 37.88% | 17,694,544 | 9.25 |
| minus_spread_mid | 3 | -0.000231 | -1.15 | -125.54 | 37.62% | 17,694,544 | 9.25 |
| minus_spread_mid | 4 | -0.000107 | -1.17 | -126.48 | 36.25% | 17,694,544 | 9.25 |
| minus_spread_mid | 5 | -0.000030 | -0.29 | -32.44 | 34.49% | 17,694,544 | 9.25 |
| minus_spread_mid | 6 | 0.000051 | 0.52 | 57.65 | 38.92% | 17,694,544 | 9.25 |
| minus_spread_mid | 7 | 0.000157 | 0.77 | 89.45 | 39.73% | 17,694,544 | 9.25 |
| minus_spread_mid | 8 | 0.000285 | 1.32 | 148.27 | 40.38% | 17,694,544 | 9.25 |
| minus_spread_mid | 9 | 0.000475 | 2.17 | 222.94 | 41.28% | 17,694,544 | 9.25 |
| minus_spread_mid | 10 | 0.001154 | 4.80 | 335.41 | 42.65% | 17,694,544 | 9.25 |

### 3.3. Goodness Of Fit

![Test Goodness Of Fit](images/figure-013.png "Test Goodness Of Fit")

test split mean_prediction_bps vs mean_label_bps. 

![Train Goodness Of Fit](images/figure-014.png "Train Goodness Of Fit")

train split mean_prediction_bps vs mean_label_bps. 

Goodness Of Fit Table

| experiment | split | prediction_bin | mean_prediction_bps | mean_label_bps | label_p05_bps | label_p95_bps | row_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| minus_depth | test | 1 | -37.10 | -20.01 | -162.51 | 128.40 | 1,769,455 |
| minus_depth | test | 2 | -17.03 | -7.51 | -96.21 | 87.59 | 1,769,455 |
| minus_depth | test | 3 | -13.68 | -5.24 | -83.62 | 78.28 | 1,769,455 |
| minus_depth | test | 4 | -11.89 | -4.16 | -76.64 | 72.59 | 1,769,455 |
| minus_depth | test | 5 | -10.74 | -3.51 | -71.91 | 68.36 | 1,769,455 |
| minus_depth | test | 6 | -9.89 | -3.08 | -68.89 | 65.84 | 1,769,455 |
| minus_depth | test | 7 | -9.18 | -2.67 | -66.76 | 64.70 | 1,769,455 |
| minus_depth | test | 8 | -8.57 | -2.39 | -65.00 | 63.25 | 1,769,455 |
| minus_depth | test | 9 | -8.03 | -2.11 | -63.48 | 62.41 | 1,769,455 |
| minus_depth | test | 10 | -7.55 | -2.10 | -62.37 | 61.30 | 1,769,455 |
| minus_depth | test | 11 | -7.11 | -1.89 | -61.42 | 60.81 | 1,769,455 |
| minus_depth | test | 12 | -6.71 | -1.88 | -60.81 | 60.16 | 1,769,455 |
| minus_depth | test | 13 | -6.34 | -1.66 | -59.89 | 59.85 | 1,769,455 |
| minus_depth | test | 14 | -6.00 | -1.58 | -59.24 | 58.98 | 1,769,455 |
| minus_depth | test | 15 | -5.69 | -1.46 | -58.29 | 58.52 | 1,769,455 |
| minus_depth | test | 16 | -5.42 | -1.41 | -56.30 | 56.38 | 1,769,455 |
| minus_depth | test | 17 | -5.20 | -1.23 | -55.39 | 55.69 | 1,769,455 |
| minus_depth | test | 18 | -4.99 | -1.23 | -54.86 | 55.08 | 1,769,455 |
| minus_depth | test | 19 | -4.78 | -1.21 | -54.47 | 54.86 | 1,769,455 |
| minus_depth | test | 20 | -4.59 | -1.18 | -54.21 | 54.63 | 1,769,455 |
| minus_depth | test | 21 | -4.40 | -1.07 | -53.98 | 54.63 | 1,769,455 |
| minus_depth | test | 22 | -4.22 | -1.10 | -53.71 | 54.05 | 1,769,455 |
| minus_depth | test | 23 | -4.05 | -1.07 | -53.52 | 53.83 | 1,769,455 |
| minus_depth | test | 24 | -3.88 | -0.98 | -53.06 | 53.75 | 1,769,455 |
| minus_depth | test | 25 | -3.72 | -1.00 | -52.91 | 53.33 | 1,769,455 |
| minus_depth | test | 26 | -3.57 | -0.97 | -52.60 | 53.14 | 1,769,455 |
| minus_depth | test | 27 | -3.42 | -0.90 | -52.38 | 52.91 | 1,769,455 |
| minus_depth | test | 28 | -3.27 | -0.85 | -52.11 | 52.95 | 1,769,455 |
| minus_depth | test | 29 | -3.13 | -0.82 | -51.99 | 52.83 | 1,769,455 |
| minus_depth | test | 30 | -2.99 | -0.87 | -51.73 | 52.60 | 1,769,455 |
| minus_depth | test | 31 | -2.85 | -0.78 | -51.65 | 52.49 | 1,769,455 |
| minus_depth | test | 32 | -2.72 | -0.79 | -51.42 | 52.41 | 1,769,455 |
| minus_depth | test | 33 | -2.59 | -0.77 | -51.40 | 52.30 | 1,769,455 |
| minus_depth | test | 34 | -2.47 | -0.73 | -51.31 | 52.45 | 1,769,455 |
| minus_depth | test | 35 | -2.34 | -0.62 | -50.81 | 51.96 | 1,769,455 |
| minus_depth | test | 36 | -2.23 | -0.67 | -50.62 | 51.84 | 1,769,455 |
| minus_depth | test | 37 | -2.11 | -0.57 | -50.54 | 51.92 | 1,769,455 |
| minus_depth | test | 38 | -1.99 | -0.52 | -50.16 | 51.69 | 1,769,455 |
| minus_depth | test | 39 | -1.88 | -0.51 | -50.54 | 51.80 | 1,769,455 |
| minus_depth | test | 40 | -1.77 | -0.56 | -50.77 | 52.03 | 1,769,455 |
| minus_depth | test | 41 | -1.66 | -0.51 | -50.74 | 52.22 | 1,769,454 |
| minus_depth | test | 42 | -1.54 | -0.49 | -50.58 | 52.15 | 1,769,454 |
| minus_depth | test | 43 | -1.44 | -0.46 | -50.35 | 51.96 | 1,769,454 |
| minus_depth | test | 44 | -1.33 | -0.40 | -49.44 | 50.74 | 1,769,454 |
| minus_depth | test | 45 | -1.23 | -0.36 | -50.20 | 51.96 | 1,769,454 |
| minus_depth | test | 46 | -1.12 | -0.39 | -50.32 | 51.96 | 1,769,454 |
| minus_depth | test | 47 | -1.02 | -0.39 | -50.51 | 52.03 | 1,769,454 |
| minus_depth | test | 48 | -0.91 | -0.33 | -50.20 | 52.07 | 1,769,454 |
| minus_depth | test | 49 | -0.81 | -0.30 | -49.97 | 51.80 | 1,769,454 |
| minus_depth | test | 50 | -0.71 | -0.28 | -50.16 | 52.19 | 1,769,454 |
| minus_depth | test | 51 | -0.61 | -0.31 | -50.39 | 52.15 | 1,769,454 |
| minus_depth | test | 52 | -0.50 | -0.21 | -50.28 | 52.15 | 1,769,454 |
| minus_depth | test | 53 | -0.40 | -0.20 | -50.35 | 52.07 | 1,769,454 |
| minus_depth | test | 54 | -0.30 | -0.15 | -49.97 | 52.07 | 1,769,454 |
| minus_depth | test | 55 | -0.20 | -0.04 | -50.16 | 52.60 | 1,769,454 |
| minus_depth | test | 56 | -0.10 | -0.08 | -50.20 | 52.22 | 1,769,454 |
| minus_depth | test | 57 | 0.00 | -0.02 | -49.82 | 52.19 | 1,769,454 |
| minus_depth | test | 58 | 0.10 | 0.10 | -49.90 | 52.49 | 1,769,454 |
| minus_depth | test | 59 | 0.21 | 0.03 | -50.32 | 52.83 | 1,769,454 |
| minus_depth | test | 60 | 0.31 | 0.13 | -50.54 | 53.18 | 1,769,454 |
| minus_depth | test | 61 | 0.42 | 0.08 | -50.51 | 53.37 | 1,769,454 |
| minus_depth | test | 62 | 0.52 | 0.14 | -50.62 | 53.56 | 1,769,454 |
| minus_depth | test | 63 | 0.63 | 0.29 | -50.66 | 53.75 | 1,769,454 |
| minus_depth | test | 64 | 0.74 | 0.31 | -50.85 | 54.09 | 1,769,454 |
| minus_depth | test | 65 | 0.86 | 0.42 | -50.96 | 54.66 | 1,769,454 |
| minus_depth | test | 66 | 0.97 | 0.42 | -51.23 | 54.86 | 1,769,454 |
| minus_depth | test | 67 | 1.09 | 0.57 | -51.42 | 55.39 | 1,769,454 |
| minus_depth | test | 68 | 1.21 | 0.59 | -51.69 | 55.69 | 1,769,454 |
| minus_depth | test | 69 | 1.34 | 0.68 | -51.73 | 56.11 | 1,769,454 |
| minus_depth | test | 70 | 1.46 | 0.66 | -51.99 | 56.27 | 1,769,454 |
| minus_depth | test | 71 | 1.60 | 0.83 | -52.22 | 56.80 | 1,769,454 |
| minus_depth | test | 72 | 1.73 | 0.94 | -52.19 | 57.33 | 1,769,454 |
| minus_depth | test | 73 | 1.87 | 0.93 | -52.53 | 57.33 | 1,769,454 |
| minus_depth | test | 74 | 2.02 | 1.07 | -52.53 | 58.02 | 1,769,454 |
| minus_depth | test | 75 | 2.17 | 1.17 | -52.76 | 58.29 | 1,769,454 |
| minus_depth | test | 76 | 2.33 | 1.31 | -52.99 | 58.82 | 1,769,454 |
| minus_depth | test | 77 | 2.50 | 1.34 | -53.25 | 59.28 | 1,769,454 |
| minus_depth | test | 78 | 2.67 | 1.51 | -53.06 | 59.70 | 1,769,454 |
| minus_depth | test | 79 | 2.85 | 1.49 | -53.60 | 59.97 | 1,769,454 |
| minus_depth | test | 80 | 3.04 | 1.65 | -53.79 | 60.81 | 1,769,454 |
| minus_depth | test | 81 | 3.23 | 1.86 | -53.94 | 61.49 | 1,769,454 |
| minus_depth | test | 82 | 3.44 | 1.95 | -54.28 | 61.91 | 1,769,454 |
| minus_depth | test | 83 | 3.66 | 2.07 | -54.86 | 62.68 | 1,769,454 |
| minus_depth | test | 84 | 3.90 | 2.19 | -55.27 | 63.48 | 1,769,454 |
| minus_depth | test | 85 | 4.15 | 2.27 | -55.81 | 64.13 | 1,769,454 |
| minus_depth | test | 86 | 4.42 | 2.42 | -56.27 | 65.12 | 1,769,454 |
| minus_depth | test | 87 | 4.71 | 2.46 | -56.88 | 65.80 | 1,769,454 |
| minus_depth | test | 88 | 5.02 | 2.72 | -57.30 | 66.99 | 1,769,454 |
| minus_depth | test | 89 | 5.37 | 2.85 | -58.29 | 68.09 | 1,769,454 |
| minus_depth | test | 90 | 5.75 | 3.13 | -58.90 | 69.81 | 1,769,454 |
| minus_depth | test | 91 | 6.18 | 3.32 | -59.93 | 70.95 | 1,769,454 |
| minus_depth | test | 92 | 6.66 | 3.51 | -60.96 | 72.75 | 1,769,454 |
| minus_depth | test | 93 | 7.21 | 3.88 | -62.33 | 74.46 | 1,769,454 |
| minus_depth | test | 94 | 7.86 | 4.04 | -63.90 | 76.41 | 1,769,454 |
| minus_depth | test | 95 | 8.64 | 4.48 | -65.46 | 79.42 | 1,769,454 |
| minus_depth | test | 96 | 9.62 | 5.00 | -67.75 | 83.01 | 1,769,454 |
| minus_depth | test | 97 | 10.92 | 5.66 | -70.69 | 87.36 | 1,769,454 |
| minus_depth | test | 98 | 12.84 | 6.64 | -74.73 | 93.92 | 1,769,454 |
| minus_depth | test | 99 | 16.32 | 8.29 | -80.72 | 105.67 | 1,769,454 |
| minus_depth | test | 100 | 34.88 | 13.64 | -106.51 | 152.74 | 1,769,454 |
| minus_depth | train | 1 | -43.82 | -43.78 | -185.70 | 97.12 | 79,688 |
| minus_depth | train | 2 | -21.72 | -23.44 | -117.49 | 81.07 | 79,688 |
| minus_depth | train | 3 | -17.51 | -19.35 | -105.74 | 75.23 | 79,688 |
| minus_depth | train | 4 | -15.21 | -16.88 | -98.50 | 71.03 | 79,688 |
| minus_depth | train | 5 | -13.65 | -15.01 | -92.70 | 68.13 | 79,688 |
| minus_depth | train | 6 | -12.49 | -13.69 | -88.88 | 65.01 | 79,688 |
| minus_depth | train | 7 | -11.58 | -12.68 | -85.53 | 64.05 | 79,688 |
| minus_depth | train | 8 | -10.85 | -11.72 | -81.91 | 61.68 | 79,688 |
| minus_depth | train | 9 | -10.23 | -10.75 | -80.03 | 61.42 | 79,688 |
| minus_depth | train | 10 | -9.68 | -10.06 | -77.86 | 61.72 | 79,688 |
| minus_depth | train | 11 | -9.18 | -9.48 | -76.41 | 60.70 | 79,688 |
| minus_depth | train | 12 | -8.72 | -8.83 | -75.37 | 60.42 | 79,688 |
| minus_depth | train | 13 | -8.29 | -8.55 | -73.62 | 59.97 | 79,688 |
| minus_depth | train | 14 | -7.89 | -8.13 | -72.56 | 59.78 | 79,688 |
| minus_depth | train | 15 | -7.52 | -7.47 | -71.68 | 60.28 | 79,688 |
| minus_depth | train | 16 | -7.16 | -7.19 | -71.18 | 59.92 | 79,688 |
| minus_depth | train | 17 | -6.83 | -6.90 | -70.84 | 59.78 | 79,688 |
| minus_depth | train | 18 | -6.51 | -6.57 | -69.96 | 60.05 | 79,688 |
| minus_depth | train | 19 | -6.21 | -5.97 | -69.01 | 60.35 | 79,688 |
| minus_depth | train | 20 | -5.92 | -5.80 | -67.98 | 58.94 | 79,688 |
| minus_depth | train | 21 | -5.66 | -5.60 | -67.06 | 58.48 | 79,688 |
| minus_depth | train | 22 | -5.42 | -5.17 | -65.75 | 57.64 | 79,688 |
| minus_depth | train | 23 | -5.21 | -5.21 | -64.66 | 56.08 | 79,688 |
| minus_depth | train | 24 | -5.02 | -5.11 | -64.54 | 55.89 | 79,688 |
| minus_depth | train | 25 | -4.82 | -4.89 | -64.16 | 56.23 | 79,688 |
| minus_depth | train | 26 | -4.64 | -4.51 | -63.21 | 55.69 | 79,688 |
| minus_depth | train | 27 | -4.45 | -4.18 | -62.41 | 56.92 | 79,688 |
| minus_depth | train | 28 | -4.28 | -4.33 | -62.52 | 55.08 | 79,688 |
| minus_depth | train | 29 | -4.10 | -4.21 | -62.51 | 55.39 | 79,688 |
| minus_depth | train | 30 | -3.93 | -3.83 | -61.21 | 55.57 | 79,688 |
| minus_depth | train | 31 | -3.77 | -3.34 | -60.58 | 56.11 | 79,688 |
| minus_depth | train | 32 | -3.61 | -3.36 | -59.89 | 55.57 | 79,688 |
| minus_depth | train | 33 | -3.45 | -3.29 | -60.86 | 56.00 | 79,688 |
| minus_depth | train | 34 | -3.30 | -2.63 | -59.59 | 56.04 | 79,688 |
| minus_depth | train | 35 | -3.15 | -2.46 | -58.94 | 56.57 | 79,688 |
| minus_depth | train | 36 | -3.00 | -2.59 | -58.71 | 55.39 | 79,688 |
| minus_depth | train | 37 | -2.86 | -2.47 | -58.67 | 55.35 | 79,688 |
| minus_depth | train | 38 | -2.72 | -2.44 | -57.79 | 55.47 | 79,688 |
| minus_depth | train | 39 | -2.58 | -2.08 | -57.56 | 56.02 | 79,688 |
| minus_depth | train | 40 | -2.44 | -1.97 | -57.98 | 56.04 | 79,688 |
| minus_depth | train | 41 | -2.31 | -1.72 | -56.92 | 55.66 | 79,688 |
| minus_depth | train | 42 | -2.17 | -1.69 | -56.46 | 55.39 | 79,688 |
| minus_depth | train | 43 | -2.04 | -1.53 | -56.84 | 55.08 | 79,688 |
| minus_depth | train | 44 | -1.92 | -1.35 | -56.15 | 55.91 | 79,688 |
| minus_depth | train | 45 | -1.79 | -1.44 | -56.98 | 56.23 | 79,688 |
| minus_depth | train | 46 | -1.66 | -1.06 | -56.23 | 56.00 | 79,688 |
| minus_depth | train | 47 | -1.53 | -0.91 | -55.73 | 56.29 | 79,688 |
| minus_depth | train | 48 | -1.41 | -0.88 | -55.77 | 56.11 | 79,688 |
| minus_depth | train | 49 | -1.29 | -0.90 | -55.15 | 54.86 | 79,688 |
| minus_depth | train | 50 | -1.16 | -0.78 | -56.04 | 56.46 | 79,688 |
| minus_depth | train | 51 | -1.04 | -0.34 | -55.01 | 56.69 | 79,688 |
| minus_depth | train | 52 | -0.91 | -0.21 | -54.82 | 57.37 | 79,688 |
| minus_depth | train | 53 | -0.79 | -0.30 | -54.89 | 56.46 | 79,688 |
| minus_depth | train | 54 | -0.67 | 0.25 | -53.48 | 57.07 | 79,688 |
| minus_depth | train | 55 | -0.55 | 0.10 | -53.35 | 56.46 | 79,688 |
| minus_depth | train | 56 | -0.42 | 0.26 | -54.02 | 57.37 | 79,688 |
| minus_depth | train | 57 | -0.30 | 0.13 | -54.47 | 56.92 | 79,688 |
| minus_depth | train | 58 | -0.18 | 0.39 | -53.60 | 56.92 | 79,688 |
| minus_depth | train | 59 | -0.06 | 0.79 | -52.87 | 57.18 | 79,688 |
| minus_depth | train | 60 | 0.07 | 0.80 | -53.06 | 57.59 | 79,688 |
| minus_depth | train | 61 | 0.19 | 1.16 | -52.90 | 58.17 | 79,688 |
| minus_depth | train | 62 | 0.32 | 0.84 | -52.80 | 57.91 | 79,688 |
| minus_depth | train | 63 | 0.45 | 1.01 | -53.56 | 58.29 | 79,688 |
| minus_depth | train | 64 | 0.58 | 1.46 | -53.22 | 60.12 | 79,688 |
| minus_depth | train | 65 | 0.71 | 1.70 | -53.06 | 60.12 | 79,688 |
| minus_depth | train | 66 | 0.85 | 1.64 | -54.13 | 60.81 | 79,688 |
| minus_depth | train | 67 | 0.99 | 1.77 | -53.33 | 61.68 | 79,688 |
| minus_depth | train | 68 | 1.14 | 1.98 | -54.59 | 62.41 | 79,688 |
| minus_depth | train | 69 | 1.29 | 2.24 | -54.78 | 63.48 | 79,687 |
| minus_depth | train | 70 | 1.44 | 2.46 | -54.63 | 63.97 | 79,687 |
| minus_depth | train | 71 | 1.60 | 2.54 | -54.84 | 64.70 | 79,687 |
| minus_depth | train | 72 | 1.77 | 2.65 | -55.27 | 65.50 | 79,687 |
| minus_depth | train | 73 | 1.94 | 2.62 | -55.47 | 65.35 | 79,687 |
| minus_depth | train | 74 | 2.11 | 2.82 | -55.47 | 65.73 | 79,687 |
| minus_depth | train | 75 | 2.29 | 3.22 | -55.81 | 66.45 | 79,687 |
| minus_depth | train | 76 | 2.48 | 3.51 | -55.54 | 68.32 | 79,687 |
| minus_depth | train | 77 | 2.68 | 3.51 | -56.50 | 68.05 | 79,687 |
| minus_depth | train | 78 | 2.88 | 3.90 | -56.15 | 69.23 | 79,687 |
| minus_depth | train | 79 | 3.10 | 3.87 | -56.95 | 69.85 | 79,687 |
| minus_depth | train | 80 | 3.32 | 4.17 | -57.29 | 69.92 | 79,687 |
| minus_depth | train | 81 | 3.56 | 4.30 | -57.24 | 70.69 | 79,687 |
| minus_depth | train | 82 | 3.80 | 4.84 | -56.76 | 71.93 | 79,687 |
| minus_depth | train | 83 | 4.06 | 5.03 | -57.64 | 72.52 | 79,687 |
| minus_depth | train | 84 | 4.34 | 5.20 | -58.54 | 74.42 | 79,687 |
| minus_depth | train | 85 | 4.64 | 5.86 | -57.98 | 76.03 | 79,687 |
| minus_depth | train | 86 | 4.95 | 5.64 | -59.93 | 75.91 | 79,687 |
| minus_depth | train | 87 | 5.30 | 5.91 | -60.65 | 76.45 | 79,687 |
| minus_depth | train | 88 | 5.67 | 6.61 | -59.57 | 79.42 | 79,687 |
| minus_depth | train | 89 | 6.08 | 6.69 | -61.91 | 80.80 | 79,687 |
| minus_depth | train | 90 | 6.54 | 7.14 | -62.00 | 81.79 | 79,687 |
| minus_depth | train | 91 | 7.05 | 7.68 | -63.25 | 83.85 | 79,687 |
| minus_depth | train | 92 | 7.63 | 8.08 | -64.03 | 86.06 | 79,687 |
| minus_depth | train | 93 | 8.31 | 9.10 | -64.15 | 89.04 | 79,687 |
| minus_depth | train | 94 | 9.11 | 9.62 | -66.34 | 91.09 | 79,687 |
| minus_depth | train | 95 | 10.09 | 10.99 | -67.58 | 96.36 | 79,687 |
| minus_depth | train | 96 | 11.33 | 12.25 | -68.59 | 100.10 | 79,687 |
| minus_depth | train | 97 | 13.02 | 13.44 | -71.44 | 105.82 | 79,687 |
| minus_depth | train | 98 | 15.54 | 15.54 | -75.80 | 112.66 | 79,687 |
| minus_depth | train | 99 | 19.96 | 20.49 | -79.19 | 126.65 | 79,687 |
| minus_depth | train | 100 | 41.42 | 42.08 | -87.89 | 205.18 | 79,687 |
| minus_imbalance | test | 1 | -24.47 | -20.88 | -155.33 | 110.17 | 1,769,455 |
| minus_imbalance | test | 2 | -12.75 | -7.62 | -94.30 | 82.02 | 1,769,455 |
| minus_imbalance | test | 3 | -10.38 | -5.01 | -82.93 | 75.30 | 1,769,455 |
| minus_imbalance | test | 4 | -8.95 | -3.73 | -76.64 | 71.41 | 1,769,455 |
| minus_imbalance | test | 5 | -7.90 | -3.11 | -72.40 | 68.74 | 1,769,455 |
| minus_imbalance | test | 6 | -7.08 | -2.69 | -69.12 | 65.99 | 1,769,455 |
| minus_imbalance | test | 7 | -6.51 | -2.34 | -63.90 | 62.18 | 1,769,455 |
| minus_imbalance | test | 8 | -6.13 | -2.02 | -61.65 | 60.20 | 1,769,455 |
| minus_imbalance | test | 9 | -5.81 | -1.75 | -60.69 | 59.70 | 1,769,455 |
| minus_imbalance | test | 10 | -5.52 | -1.64 | -60.08 | 59.47 | 1,769,455 |
| minus_imbalance | test | 11 | -5.24 | -1.63 | -59.47 | 58.78 | 1,769,455 |
| minus_imbalance | test | 12 | -4.98 | -1.44 | -58.48 | 58.52 | 1,769,455 |
| minus_imbalance | test | 13 | -4.74 | -1.45 | -58.06 | 57.83 | 1,769,455 |
| minus_imbalance | test | 14 | -4.51 | -1.31 | -57.33 | 57.45 | 1,769,455 |
| minus_imbalance | test | 15 | -4.30 | -1.12 | -56.65 | 57.37 | 1,769,455 |
| minus_imbalance | test | 16 | -4.09 | -1.15 | -56.42 | 56.99 | 1,769,455 |
| minus_imbalance | test | 17 | -3.89 | -1.19 | -55.92 | 56.34 | 1,769,455 |
| minus_imbalance | test | 18 | -3.70 | -1.04 | -55.50 | 56.27 | 1,769,455 |
| minus_imbalance | test | 19 | -3.52 | -1.07 | -55.24 | 56.04 | 1,769,455 |
| minus_imbalance | test | 20 | -3.34 | -1.40 | -57.79 | 56.46 | 1,769,455 |
| minus_imbalance | test | 21 | -3.19 | -1.09 | -57.33 | 57.26 | 1,769,455 |
| minus_imbalance | test | 22 | -3.02 | -0.94 | -55.62 | 56.34 | 1,769,455 |
| minus_imbalance | test | 23 | -2.86 | -0.91 | -55.50 | 56.11 | 1,769,455 |
| minus_imbalance | test | 24 | -2.70 | -0.96 | -55.35 | 56.04 | 1,769,455 |
| minus_imbalance | test | 25 | -2.55 | -0.85 | -55.50 | 56.23 | 1,769,455 |
| minus_imbalance | test | 26 | -2.40 | -0.88 | -55.01 | 55.20 | 1,769,455 |
| minus_imbalance | test | 27 | -2.26 | -0.92 | -55.16 | 55.54 | 1,769,455 |
| minus_imbalance | test | 28 | -2.12 | -1.01 | -55.50 | 55.69 | 1,769,455 |
| minus_imbalance | test | 29 | -1.98 | -1.17 | -56.04 | 55.39 | 1,769,455 |
| minus_imbalance | test | 30 | -1.86 | -1.15 | -55.92 | 55.43 | 1,769,455 |
| minus_imbalance | test | 31 | -1.74 | -1.28 | -56.38 | 55.39 | 1,769,455 |
| minus_imbalance | test | 32 | -1.63 | -1.33 | -55.96 | 55.01 | 1,769,455 |
| minus_imbalance | test | 33 | -1.53 | -1.18 | -54.66 | 53.83 | 1,769,455 |
| minus_imbalance | test | 34 | -1.44 | -1.20 | -54.86 | 53.79 | 1,769,455 |
| minus_imbalance | test | 35 | -1.35 | -1.21 | -54.13 | 52.91 | 1,769,455 |
| minus_imbalance | test | 36 | -1.27 | -1.03 | -53.29 | 52.64 | 1,769,455 |
| minus_imbalance | test | 37 | -1.19 | -1.11 | -54.59 | 53.90 | 1,769,455 |
| minus_imbalance | test | 38 | -1.11 | -0.96 | -54.36 | 54.36 | 1,769,455 |
| minus_imbalance | test | 39 | -1.03 | -0.92 | -54.05 | 53.90 | 1,769,455 |
| minus_imbalance | test | 40 | -0.95 | -0.79 | -53.71 | 54.05 | 1,769,455 |
| minus_imbalance | test | 41 | -0.87 | -0.70 | -53.44 | 53.98 | 1,769,454 |
| minus_imbalance | test | 42 | -0.80 | -0.59 | -53.71 | 54.63 | 1,769,454 |
| minus_imbalance | test | 43 | -0.72 | -0.56 | -54.02 | 55.39 | 1,769,454 |
| minus_imbalance | test | 44 | -0.64 | -0.36 | -53.71 | 55.69 | 1,769,454 |
| minus_imbalance | test | 45 | -0.56 | -0.26 | -53.44 | 55.69 | 1,769,454 |
| minus_imbalance | test | 46 | -0.47 | -0.17 | -52.57 | 55.24 | 1,769,454 |
| minus_imbalance | test | 47 | -0.39 | -0.09 | -52.11 | 55.24 | 1,769,454 |
| minus_imbalance | test | 48 | -0.30 | -0.06 | -51.42 | 54.21 | 1,769,454 |
| minus_imbalance | test | 49 | -0.21 | 0.03 | -50.89 | 53.90 | 1,769,454 |
| minus_imbalance | test | 50 | -0.12 | -0.00 | -50.39 | 53.56 | 1,769,454 |
| minus_imbalance | test | 51 | -0.03 | 0.04 | -50.28 | 53.44 | 1,769,454 |
| minus_imbalance | test | 52 | 0.07 | 0.11 | -49.90 | 53.33 | 1,769,454 |
| minus_imbalance | test | 53 | 0.17 | 0.10 | -49.71 | 52.99 | 1,769,454 |
| minus_imbalance | test | 54 | 0.27 | 0.15 | -49.36 | 52.72 | 1,769,454 |
| minus_imbalance | test | 55 | 0.38 | 0.24 | -49.17 | 52.87 | 1,769,454 |
| minus_imbalance | test | 56 | 0.48 | 0.19 | -49.21 | 52.72 | 1,769,454 |
| minus_imbalance | test | 57 | 0.59 | 0.32 | -49.06 | 52.87 | 1,769,454 |
| minus_imbalance | test | 58 | 0.70 | 0.26 | -49.29 | 52.83 | 1,769,454 |
| minus_imbalance | test | 59 | 0.80 | 0.33 | -49.29 | 53.06 | 1,769,454 |
| minus_imbalance | test | 60 | 0.91 | 0.43 | -49.17 | 53.29 | 1,769,454 |
| minus_imbalance | test | 61 | 1.02 | 0.43 | -49.21 | 53.41 | 1,769,454 |
| minus_imbalance | test | 62 | 1.13 | 0.45 | -49.36 | 53.14 | 1,769,454 |
| minus_imbalance | test | 63 | 1.25 | 0.53 | -49.59 | 53.56 | 1,769,454 |
| minus_imbalance | test | 64 | 1.36 | 0.56 | -49.63 | 53.83 | 1,769,454 |
| minus_imbalance | test | 65 | 1.47 | 0.67 | -49.63 | 54.05 | 1,769,454 |
| minus_imbalance | test | 66 | 1.59 | 0.68 | -49.74 | 54.44 | 1,769,454 |
| minus_imbalance | test | 67 | 1.71 | 0.79 | -49.86 | 54.86 | 1,769,454 |
| minus_imbalance | test | 68 | 1.83 | 0.78 | -50.13 | 54.97 | 1,769,454 |
| minus_imbalance | test | 69 | 1.95 | 0.85 | -50.20 | 55.35 | 1,769,454 |
| minus_imbalance | test | 70 | 2.07 | 0.95 | -50.20 | 55.62 | 1,769,454 |
| minus_imbalance | test | 71 | 2.20 | 1.06 | -50.54 | 56.04 | 1,769,454 |
| minus_imbalance | test | 72 | 2.33 | 1.09 | -50.77 | 56.38 | 1,769,454 |
| minus_imbalance | test | 73 | 2.46 | 1.11 | -50.89 | 56.69 | 1,769,454 |
| minus_imbalance | test | 74 | 2.60 | 1.13 | -51.04 | 56.99 | 1,769,454 |
| minus_imbalance | test | 75 | 2.74 | 1.26 | -51.19 | 57.49 | 1,769,454 |
| minus_imbalance | test | 76 | 2.89 | 1.27 | -51.61 | 57.79 | 1,769,454 |
| minus_imbalance | test | 77 | 3.04 | 1.26 | -51.92 | 57.95 | 1,769,454 |
| minus_imbalance | test | 78 | 3.20 | 1.54 | -52.07 | 58.86 | 1,769,454 |
| minus_imbalance | test | 79 | 3.36 | 1.49 | -52.64 | 59.24 | 1,769,454 |
| minus_imbalance | test | 80 | 3.53 | 1.66 | -52.80 | 59.78 | 1,769,454 |
| minus_imbalance | test | 81 | 3.70 | 1.73 | -53.22 | 60.62 | 1,769,454 |
| minus_imbalance | test | 82 | 3.89 | 1.82 | -53.48 | 61.19 | 1,769,454 |
| minus_imbalance | test | 83 | 4.09 | 1.93 | -53.94 | 61.95 | 1,769,454 |
| minus_imbalance | test | 84 | 4.29 | 2.02 | -54.47 | 62.56 | 1,769,454 |
| minus_imbalance | test | 85 | 4.51 | 2.09 | -54.93 | 63.48 | 1,769,454 |
| minus_imbalance | test | 86 | 4.74 | 2.38 | -55.39 | 64.58 | 1,769,454 |
| minus_imbalance | test | 87 | 4.99 | 2.48 | -56.19 | 65.35 | 1,769,454 |
| minus_imbalance | test | 88 | 5.27 | 2.49 | -56.76 | 66.11 | 1,769,454 |
| minus_imbalance | test | 89 | 5.56 | 2.68 | -57.64 | 67.33 | 1,769,454 |
| minus_imbalance | test | 90 | 5.89 | 2.88 | -58.29 | 68.55 | 1,769,454 |
| minus_imbalance | test | 91 | 6.25 | 3.06 | -58.98 | 69.89 | 1,769,454 |
| minus_imbalance | test | 92 | 6.66 | 3.29 | -60.12 | 71.41 | 1,769,454 |
| minus_imbalance | test | 93 | 7.13 | 3.54 | -61.23 | 73.24 | 1,769,454 |
| minus_imbalance | test | 94 | 7.68 | 3.74 | -62.71 | 74.88 | 1,769,454 |
| minus_imbalance | test | 95 | 8.35 | 4.11 | -64.43 | 77.59 | 1,769,454 |
| minus_imbalance | test | 96 | 9.18 | 4.49 | -66.60 | 80.34 | 1,769,454 |
| minus_imbalance | test | 97 | 10.31 | 4.96 | -69.27 | 84.46 | 1,769,454 |
| minus_imbalance | test | 98 | 11.97 | 5.77 | -73.24 | 90.56 | 1,769,454 |
| minus_imbalance | test | 99 | 15.02 | 7.01 | -79.96 | 100.94 | 1,769,454 |
| minus_imbalance | test | 100 | 28.92 | 13.54 | -98.88 | 143.05 | 1,769,454 |
| minus_imbalance | train | 1 | -28.39 | -36.05 | -171.05 | 95.37 | 79,688 |
| minus_imbalance | train | 2 | -15.65 | -21.19 | -114.36 | 76.33 | 79,688 |
| minus_imbalance | train | 3 | -12.81 | -17.41 | -101.62 | 70.75 | 79,688 |
| minus_imbalance | train | 4 | -11.23 | -15.47 | -95.90 | 69.12 | 79,688 |
| minus_imbalance | train | 5 | -10.10 | -13.86 | -91.32 | 66.07 | 79,688 |
| minus_imbalance | train | 6 | -9.22 | -13.08 | -89.01 | 64.13 | 79,688 |
| minus_imbalance | train | 7 | -8.46 | -11.80 | -85.45 | 63.67 | 79,688 |
| minus_imbalance | train | 8 | -7.81 | -11.22 | -82.68 | 61.78 | 79,688 |
| minus_imbalance | train | 9 | -7.24 | -10.44 | -81.56 | 62.56 | 79,688 |
| minus_imbalance | train | 10 | -6.76 | -9.49 | -76.26 | 59.24 | 79,688 |
| minus_imbalance | train | 11 | -6.40 | -8.91 | -73.65 | 56.57 | 79,688 |
| minus_imbalance | train | 12 | -6.12 | -8.38 | -71.98 | 56.50 | 79,688 |
| minus_imbalance | train | 13 | -5.87 | -8.27 | -72.21 | 56.61 | 79,688 |
| minus_imbalance | train | 14 | -5.63 | -7.79 | -71.41 | 57.14 | 79,688 |
| minus_imbalance | train | 15 | -5.40 | -7.26 | -70.15 | 57.64 | 79,688 |
| minus_imbalance | train | 16 | -5.18 | -6.88 | -69.24 | 57.95 | 79,688 |
| minus_imbalance | train | 17 | -4.97 | -6.64 | -69.24 | 56.92 | 79,688 |
| minus_imbalance | train | 18 | -4.76 | -6.18 | -68.21 | 56.92 | 79,688 |
| minus_imbalance | train | 19 | -4.56 | -5.76 | -67.10 | 58.14 | 79,688 |
| minus_imbalance | train | 20 | -4.37 | -5.73 | -67.48 | 57.22 | 79,688 |
| minus_imbalance | train | 21 | -4.18 | -5.46 | -66.63 | 57.72 | 79,688 |
| minus_imbalance | train | 22 | -4.00 | -5.21 | -66.36 | 57.68 | 79,688 |
| minus_imbalance | train | 23 | -3.82 | -4.63 | -65.31 | 57.33 | 79,688 |
| minus_imbalance | train | 24 | -3.65 | -4.51 | -64.77 | 57.64 | 79,688 |
| minus_imbalance | train | 25 | -3.48 | -4.26 | -64.81 | 58.17 | 79,688 |
| minus_imbalance | train | 26 | -3.32 | -3.87 | -62.79 | 54.36 | 79,688 |
| minus_imbalance | train | 27 | -3.18 | -4.11 | -63.25 | 56.69 | 79,688 |
| minus_imbalance | train | 28 | -3.02 | -3.96 | -63.44 | 56.57 | 79,688 |
| minus_imbalance | train | 29 | -2.86 | -3.66 | -63.36 | 56.57 | 79,688 |
| minus_imbalance | train | 30 | -2.71 | -3.44 | -62.03 | 57.03 | 79,688 |
| minus_imbalance | train | 31 | -2.56 | -3.04 | -61.80 | 57.41 | 79,688 |
| minus_imbalance | train | 32 | -2.40 | -2.92 | -61.42 | 57.18 | 79,688 |
| minus_imbalance | train | 33 | -2.26 | -2.72 | -61.19 | 56.66 | 79,688 |
| minus_imbalance | train | 34 | -2.12 | -2.71 | -60.46 | 56.69 | 79,688 |
| minus_imbalance | train | 35 | -1.98 | -2.55 | -60.08 | 56.38 | 79,688 |
| minus_imbalance | train | 36 | -1.84 | -2.30 | -60.01 | 56.92 | 79,688 |
| minus_imbalance | train | 37 | -1.70 | -1.83 | -58.54 | 57.64 | 79,688 |
| minus_imbalance | train | 38 | -1.58 | -1.92 | -58.25 | 56.08 | 79,688 |
| minus_imbalance | train | 39 | -1.45 | -1.42 | -56.04 | 55.24 | 79,688 |
| minus_imbalance | train | 40 | -1.34 | -1.49 | -54.86 | 52.76 | 79,688 |
| minus_imbalance | train | 41 | -1.23 | -1.48 | -55.81 | 53.26 | 79,688 |
| minus_imbalance | train | 42 | -1.12 | -1.16 | -55.27 | 54.09 | 79,688 |
| minus_imbalance | train | 43 | -1.01 | -0.91 | -53.98 | 54.32 | 79,688 |
| minus_imbalance | train | 44 | -0.90 | -1.10 | -54.10 | 53.06 | 79,688 |
| minus_imbalance | train | 45 | -0.80 | -0.85 | -54.02 | 54.09 | 79,688 |
| minus_imbalance | train | 46 | -0.69 | -0.80 | -55.47 | 55.43 | 79,688 |
| minus_imbalance | train | 47 | -0.58 | -0.57 | -55.54 | 56.84 | 79,688 |
| minus_imbalance | train | 48 | -0.46 | -0.52 | -55.27 | 56.52 | 79,688 |
| minus_imbalance | train | 49 | -0.35 | -0.21 | -54.59 | 56.99 | 79,688 |
| minus_imbalance | train | 50 | -0.24 | -0.06 | -54.78 | 56.99 | 79,688 |
| minus_imbalance | train | 51 | -0.13 | -0.04 | -54.66 | 57.87 | 79,688 |
| minus_imbalance | train | 52 | -0.02 | -0.22 | -55.73 | 57.25 | 79,688 |
| minus_imbalance | train | 53 | 0.10 | 0.01 | -55.16 | 58.14 | 79,688 |
| minus_imbalance | train | 54 | 0.21 | 0.22 | -56.02 | 59.17 | 79,688 |
| minus_imbalance | train | 55 | 0.33 | 0.48 | -55.73 | 59.32 | 79,688 |
| minus_imbalance | train | 56 | 0.45 | 0.47 | -55.81 | 59.66 | 79,688 |
| minus_imbalance | train | 57 | 0.57 | 0.48 | -55.50 | 59.89 | 79,688 |
| minus_imbalance | train | 58 | 0.68 | 0.57 | -55.39 | 59.55 | 79,688 |
| minus_imbalance | train | 59 | 0.80 | 0.95 | -55.50 | 61.45 | 79,688 |
| minus_imbalance | train | 60 | 0.92 | 0.81 | -55.69 | 61.34 | 79,688 |
| minus_imbalance | train | 61 | 1.04 | 1.24 | -55.08 | 61.80 | 79,688 |
| minus_imbalance | train | 62 | 1.17 | 1.25 | -55.08 | 61.53 | 79,688 |
| minus_imbalance | train | 63 | 1.29 | 1.11 | -55.62 | 61.53 | 79,688 |
| minus_imbalance | train | 64 | 1.42 | 1.77 | -55.27 | 63.54 | 79,688 |
| minus_imbalance | train | 65 | 1.54 | 1.68 | -55.39 | 62.90 | 79,688 |
| minus_imbalance | train | 66 | 1.67 | 1.77 | -55.57 | 63.59 | 79,688 |
| minus_imbalance | train | 67 | 1.80 | 1.91 | -56.08 | 63.29 | 79,688 |
| minus_imbalance | train | 68 | 1.94 | 2.07 | -54.84 | 64.20 | 79,688 |
| minus_imbalance | train | 69 | 2.07 | 2.18 | -55.73 | 64.28 | 79,687 |
| minus_imbalance | train | 70 | 2.21 | 2.03 | -55.85 | 64.70 | 79,687 |
| minus_imbalance | train | 71 | 2.35 | 2.33 | -55.96 | 65.12 | 79,687 |
| minus_imbalance | train | 72 | 2.50 | 2.29 | -56.00 | 65.87 | 79,687 |
| minus_imbalance | train | 73 | 2.65 | 2.63 | -56.30 | 66.10 | 79,687 |
| minus_imbalance | train | 74 | 2.80 | 2.81 | -56.76 | 67.29 | 79,687 |
| minus_imbalance | train | 75 | 2.96 | 2.91 | -57.07 | 67.79 | 79,687 |
| minus_imbalance | train | 76 | 3.12 | 3.25 | -57.14 | 69.20 | 79,687 |
| minus_imbalance | train | 77 | 3.29 | 3.18 | -57.79 | 69.20 | 79,687 |
| minus_imbalance | train | 78 | 3.47 | 3.65 | -56.95 | 70.69 | 79,687 |
| minus_imbalance | train | 79 | 3.65 | 3.41 | -58.17 | 70.38 | 79,687 |
| minus_imbalance | train | 80 | 3.84 | 3.85 | -57.75 | 71.60 | 79,687 |
| minus_imbalance | train | 81 | 4.04 | 4.00 | -59.13 | 72.75 | 79,687 |
| minus_imbalance | train | 82 | 4.25 | 4.15 | -58.93 | 73.24 | 79,687 |
| minus_imbalance | train | 83 | 4.47 | 4.70 | -59.47 | 74.60 | 79,687 |
| minus_imbalance | train | 84 | 4.70 | 4.56 | -59.89 | 74.34 | 79,687 |
| minus_imbalance | train | 85 | 4.95 | 4.83 | -59.89 | 76.22 | 79,687 |
| minus_imbalance | train | 86 | 5.22 | 5.12 | -61.68 | 76.94 | 79,687 |
| minus_imbalance | train | 87 | 5.51 | 5.44 | -61.63 | 79.42 | 79,687 |
| minus_imbalance | train | 88 | 5.82 | 5.61 | -62.33 | 80.57 | 79,687 |
| minus_imbalance | train | 89 | 6.16 | 6.40 | -63.80 | 82.93 | 79,687 |
| minus_imbalance | train | 90 | 6.54 | 6.48 | -63.48 | 83.69 | 79,687 |
| minus_imbalance | train | 91 | 6.96 | 6.55 | -65.35 | 85.14 | 79,687 |
| minus_imbalance | train | 92 | 7.44 | 7.39 | -65.94 | 87.51 | 79,687 |
| minus_imbalance | train | 93 | 8.00 | 8.20 | -66.60 | 90.33 | 79,687 |
| minus_imbalance | train | 94 | 8.65 | 8.68 | -67.98 | 91.78 | 79,687 |
| minus_imbalance | train | 95 | 9.45 | 9.09 | -69.69 | 95.75 | 79,687 |
| minus_imbalance | train | 96 | 10.47 | 10.49 | -70.42 | 99.56 | 79,687 |
| minus_imbalance | train | 97 | 11.84 | 11.93 | -74.77 | 104.90 | 79,687 |
| minus_imbalance | train | 98 | 13.92 | 13.30 | -79.27 | 113.43 | 79,687 |
| minus_imbalance | train | 99 | 17.72 | 16.65 | -85.37 | 125.81 | 79,687 |
| minus_imbalance | train | 100 | 34.52 | 30.02 | -97.18 | 177.11 | 79,687 |
| minus_quality | test | 1 | -23.19 | -21.48 | -150.38 | 100.10 | 1,769,455 |
| minus_quality | test | 2 | -12.49 | -7.78 | -91.48 | 77.93 | 1,769,455 |
| minus_quality | test | 3 | -10.33 | -5.33 | -81.25 | 72.98 | 1,769,455 |
| minus_quality | test | 4 | -9.03 | -4.08 | -74.92 | 69.12 | 1,769,455 |
| minus_quality | test | 5 | -8.18 | -3.29 | -70.19 | 66.03 | 1,769,455 |
| minus_quality | test | 6 | -7.56 | -3.04 | -67.02 | 63.48 | 1,769,455 |
| minus_quality | test | 7 | -7.06 | -2.67 | -64.96 | 62.18 | 1,769,455 |
| minus_quality | test | 8 | -6.62 | -2.61 | -63.67 | 60.73 | 1,769,455 |
| minus_quality | test | 9 | -6.23 | -2.39 | -62.03 | 59.70 | 1,769,455 |
| minus_quality | test | 10 | -5.88 | -2.22 | -60.73 | 58.82 | 1,769,455 |
| minus_quality | test | 11 | -5.54 | -2.10 | -59.81 | 57.95 | 1,769,455 |
| minus_quality | test | 12 | -5.23 | -1.95 | -58.90 | 57.60 | 1,769,455 |
| minus_quality | test | 13 | -4.92 | -1.86 | -58.21 | 57.26 | 1,769,455 |
| minus_quality | test | 14 | -4.64 | -1.73 | -57.33 | 56.46 | 1,769,455 |
| minus_quality | test | 15 | -4.39 | -1.58 | -56.04 | 55.62 | 1,769,455 |
| minus_quality | test | 16 | -4.18 | -1.59 | -55.35 | 54.66 | 1,769,455 |
| minus_quality | test | 17 | -3.98 | -1.55 | -55.08 | 54.36 | 1,769,455 |
| minus_quality | test | 18 | -3.78 | -1.45 | -54.70 | 54.32 | 1,769,455 |
| minus_quality | test | 19 | -3.59 | -1.44 | -54.59 | 54.09 | 1,769,455 |
| minus_quality | test | 20 | -3.39 | -1.34 | -54.55 | 54.24 | 1,769,455 |
| minus_quality | test | 21 | -3.20 | -1.33 | -54.05 | 54.21 | 1,769,455 |
| minus_quality | test | 22 | -3.02 | -1.31 | -53.33 | 53.41 | 1,769,455 |
| minus_quality | test | 23 | -2.84 | -1.18 | -53.75 | 54.02 | 1,769,455 |
| minus_quality | test | 24 | -2.66 | -1.12 | -53.56 | 54.05 | 1,769,455 |
| minus_quality | test | 25 | -2.48 | -1.16 | -53.33 | 53.60 | 1,769,455 |
| minus_quality | test | 26 | -2.31 | -1.03 | -52.91 | 53.41 | 1,769,455 |
| minus_quality | test | 27 | -2.14 | -1.02 | -52.64 | 53.33 | 1,769,455 |
| minus_quality | test | 28 | -1.99 | -0.90 | -52.34 | 53.33 | 1,769,455 |
| minus_quality | test | 29 | -1.84 | -0.97 | -52.30 | 52.91 | 1,769,455 |
| minus_quality | test | 30 | -1.70 | -1.05 | -53.60 | 53.52 | 1,769,455 |
| minus_quality | test | 31 | -1.57 | -1.40 | -56.30 | 54.32 | 1,769,455 |
| minus_quality | test | 32 | -1.46 | -1.42 | -54.40 | 52.53 | 1,769,455 |
| minus_quality | test | 33 | -1.34 | -0.99 | -52.41 | 52.26 | 1,769,455 |
| minus_quality | test | 34 | -1.24 | -1.09 | -52.38 | 52.15 | 1,769,455 |
| minus_quality | test | 35 | -1.14 | -1.01 | -52.19 | 52.03 | 1,769,455 |
| minus_quality | test | 36 | -1.04 | -1.02 | -52.41 | 51.96 | 1,769,455 |
| minus_quality | test | 37 | -0.95 | -0.97 | -52.19 | 51.84 | 1,769,455 |
| minus_quality | test | 38 | -0.86 | -1.01 | -52.30 | 51.96 | 1,769,455 |
| minus_quality | test | 39 | -0.78 | -0.87 | -50.39 | 49.67 | 1,769,455 |
| minus_quality | test | 40 | -0.70 | -0.81 | -51.77 | 51.80 | 1,769,455 |
| minus_quality | test | 41 | -0.61 | -0.89 | -52.22 | 52.15 | 1,769,454 |
| minus_quality | test | 42 | -0.53 | -0.83 | -52.19 | 52.30 | 1,769,454 |
| minus_quality | test | 43 | -0.44 | -0.69 | -51.99 | 52.26 | 1,769,454 |
| minus_quality | test | 44 | -0.36 | -0.68 | -52.22 | 52.76 | 1,769,454 |
| minus_quality | test | 45 | -0.27 | -0.59 | -52.15 | 52.76 | 1,769,454 |
| minus_quality | test | 46 | -0.19 | -0.52 | -52.11 | 53.14 | 1,769,454 |
| minus_quality | test | 47 | -0.11 | -0.47 | -51.96 | 53.10 | 1,769,454 |
| minus_quality | test | 48 | -0.02 | -0.30 | -51.73 | 53.33 | 1,769,454 |
| minus_quality | test | 49 | 0.07 | -0.20 | -51.69 | 53.52 | 1,769,454 |
| minus_quality | test | 50 | 0.15 | -0.13 | -51.77 | 53.83 | 1,769,454 |
| minus_quality | test | 51 | 0.24 | -0.04 | -51.77 | 54.28 | 1,769,454 |
| minus_quality | test | 52 | 0.33 | 0.07 | -51.96 | 54.78 | 1,769,454 |
| minus_quality | test | 53 | 0.42 | 0.14 | -52.30 | 55.31 | 1,769,454 |
| minus_quality | test | 54 | 0.52 | 0.22 | -52.22 | 55.85 | 1,769,454 |
| minus_quality | test | 55 | 0.62 | 0.33 | -52.38 | 56.04 | 1,769,454 |
| minus_quality | test | 56 | 0.73 | 0.44 | -52.38 | 56.46 | 1,769,454 |
| minus_quality | test | 57 | 0.83 | 0.46 | -52.22 | 56.69 | 1,769,454 |
| minus_quality | test | 58 | 0.94 | 0.58 | -52.07 | 56.72 | 1,769,454 |
| minus_quality | test | 59 | 1.05 | 0.57 | -52.11 | 56.69 | 1,769,454 |
| minus_quality | test | 60 | 1.17 | 0.69 | -51.96 | 56.69 | 1,769,454 |
| minus_quality | test | 61 | 1.29 | 0.75 | -51.69 | 56.84 | 1,769,454 |
| minus_quality | test | 62 | 1.41 | 0.75 | -51.61 | 56.80 | 1,769,454 |
| minus_quality | test | 63 | 1.53 | 0.83 | -51.54 | 56.84 | 1,769,454 |
| minus_quality | test | 64 | 1.66 | 0.82 | -51.50 | 56.57 | 1,769,454 |
| minus_quality | test | 65 | 1.78 | 0.96 | -51.42 | 56.99 | 1,769,454 |
| minus_quality | test | 66 | 1.91 | 1.01 | -51.31 | 57.03 | 1,769,454 |
| minus_quality | test | 67 | 2.05 | 1.03 | -51.23 | 57.18 | 1,769,454 |
| minus_quality | test | 68 | 2.18 | 1.09 | -51.38 | 57.33 | 1,769,454 |
| minus_quality | test | 69 | 2.32 | 1.13 | -51.38 | 57.33 | 1,769,454 |
| minus_quality | test | 70 | 2.46 | 1.24 | -51.08 | 57.33 | 1,769,454 |
| minus_quality | test | 71 | 2.60 | 1.25 | -51.31 | 57.33 | 1,769,454 |
| minus_quality | test | 72 | 2.74 | 1.28 | -51.42 | 57.56 | 1,769,454 |
| minus_quality | test | 73 | 2.89 | 1.36 | -51.08 | 57.45 | 1,769,454 |
| minus_quality | test | 74 | 3.03 | 1.50 | -50.89 | 57.49 | 1,769,454 |
| minus_quality | test | 75 | 3.18 | 1.56 | -51.12 | 57.64 | 1,769,454 |
| minus_quality | test | 76 | 3.32 | 1.58 | -51.38 | 58.06 | 1,769,454 |
| minus_quality | test | 77 | 3.48 | 1.60 | -51.69 | 58.29 | 1,769,454 |
| minus_quality | test | 78 | 3.63 | 1.73 | -51.84 | 58.75 | 1,769,454 |
| minus_quality | test | 79 | 3.79 | 1.83 | -52.22 | 59.47 | 1,769,454 |
| minus_quality | test | 80 | 3.96 | 1.90 | -52.38 | 59.93 | 1,769,454 |
| minus_quality | test | 81 | 4.14 | 2.07 | -52.64 | 60.58 | 1,769,454 |
| minus_quality | test | 82 | 4.33 | 2.07 | -53.06 | 61.19 | 1,769,454 |
| minus_quality | test | 83 | 4.53 | 2.19 | -53.60 | 61.91 | 1,769,454 |
| minus_quality | test | 84 | 4.74 | 2.26 | -53.94 | 62.79 | 1,769,454 |
| minus_quality | test | 85 | 4.96 | 2.33 | -54.47 | 63.36 | 1,769,454 |
| minus_quality | test | 86 | 5.20 | 2.47 | -55.05 | 64.13 | 1,769,454 |
| minus_quality | test | 87 | 5.47 | 2.60 | -55.62 | 65.27 | 1,769,454 |
| minus_quality | test | 88 | 5.76 | 2.77 | -56.27 | 66.68 | 1,769,454 |
| minus_quality | test | 89 | 6.10 | 2.86 | -57.49 | 68.13 | 1,769,454 |
| minus_quality | test | 90 | 6.50 | 2.94 | -58.86 | 69.66 | 1,769,454 |
| minus_quality | test | 91 | 6.96 | 3.10 | -59.93 | 71.18 | 1,769,454 |
| minus_quality | test | 92 | 7.49 | 3.43 | -60.81 | 72.98 | 1,769,454 |
| minus_quality | test | 93 | 8.09 | 3.57 | -62.26 | 74.35 | 1,769,454 |
| minus_quality | test | 94 | 8.78 | 3.98 | -63.67 | 77.13 | 1,769,454 |
| minus_quality | test | 95 | 9.59 | 4.28 | -65.31 | 79.73 | 1,769,454 |
| minus_quality | test | 96 | 10.60 | 4.51 | -67.79 | 82.86 | 1,769,454 |
| minus_quality | test | 97 | 11.91 | 5.03 | -70.84 | 87.36 | 1,769,454 |
| minus_quality | test | 98 | 13.78 | 5.73 | -75.26 | 93.92 | 1,769,454 |
| minus_quality | test | 99 | 17.06 | 7.18 | -82.86 | 105.06 | 1,769,454 |
| minus_quality | test | 100 | 31.79 | 14.89 | -109.25 | 158.39 | 1,769,454 |
| minus_quality | train | 1 | -26.64 | -37.86 | -169.68 | 90.99 | 79,688 |
| minus_quality | train | 2 | -14.85 | -21.69 | -113.53 | 76.22 | 79,688 |
| minus_quality | train | 3 | -12.29 | -17.94 | -99.41 | 68.08 | 79,688 |
| minus_quality | train | 4 | -10.85 | -15.59 | -94.76 | 66.53 | 79,688 |
| minus_quality | train | 5 | -9.80 | -14.21 | -89.11 | 63.93 | 79,688 |
| minus_quality | train | 6 | -8.98 | -13.00 | -86.52 | 63.10 | 79,688 |
| minus_quality | train | 7 | -8.35 | -12.10 | -82.63 | 60.70 | 79,688 |
| minus_quality | train | 8 | -7.84 | -11.29 | -80.49 | 58.98 | 79,688 |
| minus_quality | train | 9 | -7.42 | -10.17 | -77.44 | 59.09 | 79,688 |
| minus_quality | train | 10 | -7.04 | -9.67 | -76.64 | 58.98 | 79,688 |
| minus_quality | train | 11 | -6.69 | -8.98 | -74.35 | 58.10 | 79,688 |
| minus_quality | train | 12 | -6.37 | -8.31 | -73.13 | 58.52 | 79,688 |
| minus_quality | train | 13 | -6.06 | -8.27 | -72.44 | 57.22 | 79,688 |
| minus_quality | train | 14 | -5.78 | -7.64 | -70.95 | 58.25 | 79,688 |
| minus_quality | train | 15 | -5.50 | -7.21 | -70.19 | 57.87 | 79,688 |
| minus_quality | train | 16 | -5.22 | -7.09 | -69.24 | 57.37 | 79,688 |
| minus_quality | train | 17 | -4.96 | -6.45 | -68.82 | 57.03 | 79,688 |
| minus_quality | train | 18 | -4.70 | -6.47 | -67.94 | 56.84 | 79,688 |
| minus_quality | train | 19 | -4.47 | -5.90 | -65.99 | 56.06 | 79,688 |
| minus_quality | train | 20 | -4.26 | -5.34 | -64.74 | 55.81 | 79,688 |
| minus_quality | train | 21 | -4.07 | -5.45 | -65.12 | 55.58 | 79,688 |
| minus_quality | train | 22 | -3.88 | -4.87 | -64.54 | 56.69 | 79,688 |
| minus_quality | train | 23 | -3.70 | -4.81 | -64.20 | 56.53 | 79,688 |
| minus_quality | train | 24 | -3.52 | -4.73 | -64.20 | 56.30 | 79,688 |
| minus_quality | train | 25 | -3.33 | -4.87 | -64.32 | 56.04 | 79,688 |
| minus_quality | train | 26 | -3.15 | -4.46 | -63.51 | 56.33 | 79,688 |
| minus_quality | train | 27 | -2.98 | -4.06 | -63.40 | 57.07 | 79,688 |
| minus_quality | train | 28 | -2.80 | -3.90 | -63.23 | 56.34 | 79,688 |
| minus_quality | train | 29 | -2.62 | -3.54 | -62.52 | 57.60 | 79,688 |
| minus_quality | train | 30 | -2.45 | -3.26 | -62.60 | 57.72 | 79,688 |
| minus_quality | train | 31 | -2.28 | -3.41 | -62.56 | 57.22 | 79,688 |
| minus_quality | train | 32 | -2.11 | -3.05 | -61.26 | 56.84 | 79,688 |
| minus_quality | train | 33 | -1.95 | -2.91 | -60.69 | 56.80 | 79,688 |
| minus_quality | train | 34 | -1.80 | -2.54 | -60.27 | 57.37 | 79,688 |
| minus_quality | train | 35 | -1.65 | -2.50 | -59.85 | 56.99 | 79,688 |
| minus_quality | train | 36 | -1.52 | -2.43 | -57.64 | 54.02 | 79,688 |
| minus_quality | train | 37 | -1.39 | -2.16 | -57.87 | 55.39 | 79,688 |
| minus_quality | train | 38 | -1.27 | -2.09 | -58.29 | 55.58 | 79,688 |
| minus_quality | train | 39 | -1.15 | -1.87 | -57.33 | 56.11 | 79,688 |
| minus_quality | train | 40 | -1.04 | -1.90 | -56.88 | 54.70 | 79,688 |
| minus_quality | train | 41 | -0.92 | -1.61 | -56.61 | 55.01 | 79,688 |
| minus_quality | train | 42 | -0.81 | -1.34 | -54.47 | 53.60 | 79,688 |
| minus_quality | train | 43 | -0.71 | -1.20 | -54.89 | 54.60 | 79,688 |
| minus_quality | train | 44 | -0.60 | -1.21 | -55.62 | 54.93 | 79,688 |
| minus_quality | train | 45 | -0.49 | -1.05 | -55.01 | 54.78 | 79,688 |
| minus_quality | train | 46 | -0.38 | -0.84 | -55.08 | 55.24 | 79,688 |
| minus_quality | train | 47 | -0.28 | -0.75 | -54.78 | 55.24 | 79,688 |
| minus_quality | train | 48 | -0.17 | -0.76 | -54.63 | 54.66 | 79,688 |
| minus_quality | train | 49 | -0.06 | -0.40 | -54.44 | 55.58 | 79,688 |
| minus_quality | train | 50 | 0.04 | -0.54 | -54.24 | 54.93 | 79,688 |
| minus_quality | train | 51 | 0.15 | -0.71 | -54.21 | 55.01 | 79,688 |
| minus_quality | train | 52 | 0.26 | -0.41 | -54.70 | 56.29 | 79,688 |
| minus_quality | train | 53 | 0.38 | -0.23 | -55.47 | 57.95 | 79,688 |
| minus_quality | train | 54 | 0.50 | 0.13 | -56.30 | 59.09 | 79,688 |
| minus_quality | train | 55 | 0.62 | 0.12 | -56.22 | 59.70 | 79,688 |
| minus_quality | train | 56 | 0.75 | 0.33 | -55.85 | 60.22 | 79,688 |
| minus_quality | train | 57 | 0.88 | 0.58 | -56.27 | 61.34 | 79,688 |
| minus_quality | train | 58 | 1.01 | 0.54 | -56.65 | 60.65 | 79,688 |
| minus_quality | train | 59 | 1.14 | 0.92 | -56.69 | 61.91 | 79,688 |
| minus_quality | train | 60 | 1.28 | 0.85 | -56.84 | 61.90 | 79,688 |
| minus_quality | train | 61 | 1.41 | 0.73 | -56.30 | 61.19 | 79,688 |
| minus_quality | train | 62 | 1.55 | 0.82 | -57.18 | 60.83 | 79,688 |
| minus_quality | train | 63 | 1.69 | 1.15 | -57.33 | 63.02 | 79,688 |
| minus_quality | train | 64 | 1.83 | 1.52 | -55.73 | 63.10 | 79,688 |
| minus_quality | train | 65 | 1.98 | 1.37 | -57.11 | 62.94 | 79,688 |
| minus_quality | train | 66 | 2.12 | 1.48 | -57.18 | 63.54 | 79,688 |
| minus_quality | train | 67 | 2.27 | 1.73 | -57.14 | 63.82 | 79,688 |
| minus_quality | train | 68 | 2.42 | 2.15 | -56.04 | 64.35 | 79,688 |
| minus_quality | train | 69 | 2.57 | 2.26 | -56.30 | 64.16 | 79,687 |
| minus_quality | train | 70 | 2.72 | 2.22 | -56.53 | 64.39 | 79,687 |
| minus_quality | train | 71 | 2.87 | 2.63 | -56.61 | 65.48 | 79,687 |
| minus_quality | train | 72 | 3.02 | 2.55 | -56.61 | 65.02 | 79,687 |
| minus_quality | train | 73 | 3.17 | 2.87 | -56.30 | 65.50 | 79,687 |
| minus_quality | train | 74 | 3.33 | 2.87 | -55.92 | 65.80 | 79,687 |
| minus_quality | train | 75 | 3.49 | 3.04 | -56.08 | 65.96 | 79,687 |
| minus_quality | train | 76 | 3.65 | 3.45 | -56.26 | 68.09 | 79,687 |
| minus_quality | train | 77 | 3.81 | 3.39 | -57.11 | 67.86 | 79,687 |
| minus_quality | train | 78 | 3.99 | 3.64 | -57.14 | 69.20 | 79,687 |
| minus_quality | train | 79 | 4.17 | 4.07 | -56.30 | 70.11 | 79,687 |
| minus_quality | train | 80 | 4.36 | 3.66 | -57.17 | 68.97 | 79,687 |
| minus_quality | train | 81 | 4.56 | 3.84 | -57.87 | 70.69 | 79,687 |
| minus_quality | train | 82 | 4.77 | 4.38 | -57.33 | 71.17 | 79,687 |
| minus_quality | train | 83 | 4.99 | 4.74 | -58.75 | 74.22 | 79,687 |
| minus_quality | train | 84 | 5.24 | 4.85 | -58.47 | 74.46 | 79,687 |
| minus_quality | train | 85 | 5.50 | 5.12 | -59.47 | 75.34 | 79,687 |
| minus_quality | train | 86 | 5.80 | 5.52 | -60.12 | 77.06 | 79,687 |
| minus_quality | train | 87 | 6.13 | 5.49 | -61.26 | 78.43 | 79,687 |
| minus_quality | train | 88 | 6.51 | 6.10 | -62.75 | 81.02 | 79,687 |
| minus_quality | train | 89 | 6.93 | 6.35 | -63.97 | 83.08 | 79,687 |
| minus_quality | train | 90 | 7.41 | 6.58 | -64.76 | 84.46 | 79,687 |
| minus_quality | train | 91 | 7.94 | 7.18 | -65.73 | 87.59 | 79,687 |
| minus_quality | train | 92 | 8.52 | 7.25 | -67.47 | 87.81 | 79,687 |
| minus_quality | train | 93 | 9.20 | 8.03 | -67.71 | 90.94 | 79,687 |
| minus_quality | train | 94 | 9.98 | 8.95 | -70.00 | 95.75 | 79,687 |
| minus_quality | train | 95 | 10.92 | 10.20 | -70.19 | 99.56 | 79,687 |
| minus_quality | train | 96 | 12.10 | 10.61 | -73.17 | 103.43 | 79,687 |
| minus_quality | train | 97 | 13.67 | 12.18 | -76.37 | 110.24 | 79,687 |
| minus_quality | train | 98 | 15.96 | 14.30 | -80.31 | 117.72 | 79,687 |
| minus_quality | train | 99 | 20.03 | 17.95 | -86.52 | 131.15 | 79,687 |
| minus_quality | train | 100 | 38.09 | 33.48 | -101.55 | 189.21 | 79,687 |
| minus_spread_mid | test | 1 | -22.78 | -17.13 | -135.96 | 94.45 | 1,769,455 |
| minus_spread_mid | test | 2 | -12.28 | -6.31 | -87.43 | 77.06 | 1,769,455 |
| minus_spread_mid | test | 3 | -10.13 | -4.37 | -76.83 | 70.69 | 1,769,455 |
| minus_spread_mid | test | 4 | -8.99 | -3.26 | -71.14 | 67.21 | 1,769,455 |
| minus_spread_mid | test | 5 | -8.17 | -2.81 | -68.24 | 64.89 | 1,769,455 |
| minus_spread_mid | test | 6 | -7.50 | -2.52 | -65.80 | 63.21 | 1,769,455 |
| minus_spread_mid | test | 7 | -6.93 | -2.24 | -64.05 | 61.91 | 1,769,455 |
| minus_spread_mid | test | 8 | -6.43 | -2.10 | -62.41 | 60.96 | 1,769,455 |
| minus_spread_mid | test | 9 | -5.97 | -1.97 | -61.38 | 60.08 | 1,769,455 |
| minus_spread_mid | test | 10 | -5.55 | -1.85 | -60.42 | 59.51 | 1,769,455 |
| minus_spread_mid | test | 11 | -5.16 | -1.70 | -58.67 | 57.91 | 1,769,455 |
| minus_spread_mid | test | 12 | -4.87 | -1.57 | -56.30 | 56.04 | 1,769,455 |
| minus_spread_mid | test | 13 | -4.63 | -1.49 | -55.62 | 55.58 | 1,769,455 |
| minus_spread_mid | test | 14 | -4.42 | -1.44 | -55.96 | 55.69 | 1,769,455 |
| minus_spread_mid | test | 15 | -4.21 | -1.44 | -56.30 | 56.15 | 1,769,455 |
| minus_spread_mid | test | 16 | -4.01 | -1.55 | -55.85 | 55.66 | 1,769,455 |
| minus_spread_mid | test | 17 | -3.81 | -1.43 | -55.05 | 55.08 | 1,769,455 |
| minus_spread_mid | test | 18 | -3.62 | -1.37 | -55.39 | 55.12 | 1,769,455 |
| minus_spread_mid | test | 19 | -3.43 | -1.28 | -55.39 | 55.39 | 1,769,455 |
| minus_spread_mid | test | 20 | -3.24 | -1.28 | -55.08 | 55.08 | 1,769,455 |
| minus_spread_mid | test | 21 | -3.05 | -1.24 | -54.66 | 54.70 | 1,769,455 |
| minus_spread_mid | test | 22 | -2.87 | -1.18 | -54.47 | 54.55 | 1,769,455 |
| minus_spread_mid | test | 23 | -2.70 | -1.18 | -54.21 | 54.44 | 1,769,455 |
| minus_spread_mid | test | 24 | -2.53 | -1.07 | -54.13 | 54.51 | 1,769,455 |
| minus_spread_mid | test | 25 | -2.37 | -1.16 | -54.21 | 54.21 | 1,769,455 |
| minus_spread_mid | test | 26 | -2.21 | -1.06 | -54.17 | 54.36 | 1,769,455 |
| minus_spread_mid | test | 27 | -2.06 | -1.10 | -54.44 | 54.28 | 1,769,455 |
| minus_spread_mid | test | 28 | -1.91 | -1.12 | -54.82 | 54.47 | 1,769,455 |
| minus_spread_mid | test | 29 | -1.77 | -1.20 | -55.08 | 54.66 | 1,769,455 |
| minus_spread_mid | test | 30 | -1.64 | -1.20 | -55.35 | 54.93 | 1,769,455 |
| minus_spread_mid | test | 31 | -1.51 | -1.24 | -55.62 | 55.08 | 1,769,455 |
| minus_spread_mid | test | 32 | -1.40 | -1.20 | -55.73 | 55.16 | 1,769,455 |
| minus_spread_mid | test | 33 | -1.29 | -1.24 | -55.85 | 55.24 | 1,769,455 |
| minus_spread_mid | test | 34 | -1.19 | -1.25 | -55.54 | 54.66 | 1,769,455 |
| minus_spread_mid | test | 35 | -1.09 | -1.25 | -55.47 | 54.47 | 1,769,455 |
| minus_spread_mid | test | 36 | -1.01 | -1.27 | -55.39 | 54.44 | 1,769,455 |
| minus_spread_mid | test | 37 | -0.92 | -1.14 | -55.62 | 54.97 | 1,769,455 |
| minus_spread_mid | test | 38 | -0.84 | -1.13 | -55.58 | 55.01 | 1,769,455 |
| minus_spread_mid | test | 39 | -0.76 | -1.03 | -55.12 | 55.08 | 1,769,455 |
| minus_spread_mid | test | 40 | -0.69 | -0.96 | -54.93 | 54.78 | 1,769,455 |
| minus_spread_mid | test | 41 | -0.61 | -0.87 | -54.40 | 54.32 | 1,769,454 |
| minus_spread_mid | test | 42 | -0.54 | -0.70 | -54.13 | 54.47 | 1,769,454 |
| minus_spread_mid | test | 43 | -0.47 | -0.72 | -53.94 | 54.47 | 1,769,454 |
| minus_spread_mid | test | 44 | -0.40 | -0.39 | -53.22 | 54.51 | 1,769,454 |
| minus_spread_mid | test | 45 | -0.34 | -0.29 | -52.91 | 54.78 | 1,769,454 |
| minus_spread_mid | test | 46 | -0.27 | -0.24 | -52.30 | 54.21 | 1,769,454 |
| minus_spread_mid | test | 47 | -0.20 | -0.10 | -52.11 | 54.47 | 1,769,454 |
| minus_spread_mid | test | 48 | -0.13 | 0.04 | -51.88 | 54.78 | 1,769,454 |
| minus_spread_mid | test | 49 | -0.06 | 0.09 | -51.12 | 53.98 | 1,769,454 |
| minus_spread_mid | test | 50 | 0.02 | 0.26 | -51.50 | 55.01 | 1,769,454 |
| minus_spread_mid | test | 51 | 0.09 | 0.39 | -51.99 | 56.27 | 1,769,454 |
| minus_spread_mid | test | 52 | 0.18 | 0.42 | -52.53 | 56.99 | 1,769,454 |
| minus_spread_mid | test | 53 | 0.27 | 0.42 | -52.38 | 56.84 | 1,769,454 |
| minus_spread_mid | test | 54 | 0.36 | 0.46 | -52.19 | 56.84 | 1,769,454 |
| minus_spread_mid | test | 55 | 0.45 | 0.59 | -51.84 | 56.92 | 1,769,454 |
| minus_spread_mid | test | 56 | 0.55 | 0.60 | -51.42 | 56.57 | 1,769,454 |
| minus_spread_mid | test | 57 | 0.65 | 0.58 | -51.38 | 56.27 | 1,769,454 |
| minus_spread_mid | test | 58 | 0.75 | 0.53 | -51.19 | 56.00 | 1,769,454 |
| minus_spread_mid | test | 59 | 0.85 | 0.54 | -51.08 | 55.69 | 1,769,454 |
| minus_spread_mid | test | 60 | 0.96 | 0.63 | -50.74 | 55.35 | 1,769,454 |
| minus_spread_mid | test | 61 | 1.06 | 0.58 | -50.62 | 55.35 | 1,769,454 |
| minus_spread_mid | test | 62 | 1.17 | 0.69 | -50.39 | 55.35 | 1,769,454 |
| minus_spread_mid | test | 63 | 1.28 | 0.70 | -50.28 | 55.24 | 1,769,454 |
| minus_spread_mid | test | 64 | 1.39 | 0.71 | -50.39 | 55.35 | 1,769,454 |
| minus_spread_mid | test | 65 | 1.50 | 0.75 | -50.13 | 55.08 | 1,769,454 |
| minus_spread_mid | test | 66 | 1.61 | 0.74 | -50.20 | 55.08 | 1,769,454 |
| minus_spread_mid | test | 67 | 1.73 | 0.84 | -50.16 | 55.31 | 1,769,454 |
| minus_spread_mid | test | 68 | 1.85 | 0.86 | -50.39 | 55.39 | 1,769,454 |
| minus_spread_mid | test | 69 | 1.97 | 0.96 | -50.35 | 55.62 | 1,769,454 |
| minus_spread_mid | test | 70 | 2.09 | 0.93 | -50.39 | 55.62 | 1,769,454 |
| minus_spread_mid | test | 71 | 2.22 | 1.03 | -50.43 | 55.89 | 1,769,454 |
| minus_spread_mid | test | 72 | 2.34 | 1.10 | -50.58 | 56.15 | 1,769,454 |
| minus_spread_mid | test | 73 | 2.48 | 1.22 | -50.62 | 56.46 | 1,769,454 |
| minus_spread_mid | test | 74 | 2.61 | 1.17 | -50.81 | 56.69 | 1,769,454 |
| minus_spread_mid | test | 75 | 2.75 | 1.21 | -51.08 | 56.80 | 1,769,454 |
| minus_spread_mid | test | 76 | 2.90 | 1.39 | -51.12 | 57.33 | 1,769,454 |
| minus_spread_mid | test | 77 | 3.05 | 1.46 | -51.31 | 57.79 | 1,769,454 |
| minus_spread_mid | test | 78 | 3.20 | 1.40 | -51.69 | 57.72 | 1,769,454 |
| minus_spread_mid | test | 79 | 3.37 | 1.56 | -51.88 | 58.29 | 1,769,454 |
| minus_spread_mid | test | 80 | 3.54 | 1.61 | -52.22 | 58.86 | 1,769,454 |
| minus_spread_mid | test | 81 | 3.72 | 1.76 | -52.57 | 59.51 | 1,769,454 |
| minus_spread_mid | test | 82 | 3.91 | 1.81 | -52.83 | 60.08 | 1,769,454 |
| minus_spread_mid | test | 83 | 4.11 | 1.91 | -53.52 | 60.84 | 1,769,454 |
| minus_spread_mid | test | 84 | 4.32 | 1.95 | -54.02 | 61.19 | 1,769,454 |
| minus_spread_mid | test | 85 | 4.55 | 2.09 | -54.40 | 62.26 | 1,769,454 |
| minus_spread_mid | test | 86 | 4.79 | 2.12 | -55.39 | 63.10 | 1,769,454 |
| minus_spread_mid | test | 87 | 5.05 | 2.37 | -55.81 | 64.16 | 1,769,454 |
| minus_spread_mid | test | 88 | 5.34 | 2.39 | -56.76 | 65.42 | 1,769,454 |
| minus_spread_mid | test | 89 | 5.66 | 2.58 | -57.64 | 66.45 | 1,769,454 |
| minus_spread_mid | test | 90 | 6.01 | 2.74 | -58.67 | 67.98 | 1,769,454 |
| minus_spread_mid | test | 91 | 6.41 | 2.89 | -59.66 | 69.43 | 1,769,454 |
| minus_spread_mid | test | 92 | 6.85 | 3.01 | -61.23 | 71.30 | 1,769,454 |
| minus_spread_mid | test | 93 | 7.37 | 3.28 | -62.64 | 73.47 | 1,769,454 |
| minus_spread_mid | test | 94 | 7.98 | 3.46 | -64.51 | 75.76 | 1,769,454 |
| minus_spread_mid | test | 95 | 8.73 | 3.67 | -66.87 | 78.74 | 1,769,454 |
| minus_spread_mid | test | 96 | 9.67 | 4.04 | -69.69 | 82.78 | 1,769,454 |
| minus_spread_mid | test | 97 | 10.93 | 4.50 | -73.24 | 87.66 | 1,769,454 |
| minus_spread_mid | test | 98 | 12.78 | 5.29 | -78.74 | 95.52 | 1,769,454 |
| minus_spread_mid | test | 99 | 16.07 | 6.32 | -87.28 | 108.49 | 1,769,454 |
| minus_spread_mid | test | 100 | 28.60 | 11.51 | -112.92 | 156.40 | 1,769,454 |
| minus_spread_mid | train | 1 | -26.76 | -35.56 | -158.54 | 80.34 | 79,688 |
| minus_spread_mid | train | 2 | -15.43 | -21.48 | -113.17 | 72.75 | 79,688 |
| minus_spread_mid | train | 3 | -12.44 | -17.42 | -100.40 | 69.20 | 79,688 |
| minus_spread_mid | train | 4 | -10.91 | -14.98 | -93.00 | 66.11 | 79,688 |
| minus_spread_mid | train | 5 | -9.89 | -13.70 | -88.12 | 63.25 | 79,688 |
| minus_spread_mid | train | 6 | -9.16 | -12.45 | -85.22 | 62.24 | 79,688 |
| minus_spread_mid | train | 7 | -8.54 | -11.44 | -82.55 | 62.68 | 79,688 |
| minus_spread_mid | train | 8 | -8.00 | -10.81 | -81.33 | 61.49 | 79,688 |
| minus_spread_mid | train | 9 | -7.51 | -9.76 | -78.43 | 60.87 | 79,688 |
| minus_spread_mid | train | 10 | -7.06 | -9.46 | -77.29 | 61.29 | 79,688 |
| minus_spread_mid | train | 11 | -6.65 | -8.80 | -75.91 | 60.11 | 79,688 |
| minus_spread_mid | train | 12 | -6.26 | -8.30 | -74.35 | 59.55 | 79,688 |
| minus_spread_mid | train | 13 | -5.89 | -7.90 | -73.38 | 59.39 | 79,688 |
| minus_spread_mid | train | 14 | -5.54 | -7.06 | -71.91 | 60.81 | 79,688 |
| minus_spread_mid | train | 15 | -5.21 | -7.07 | -71.53 | 58.98 | 79,688 |
| minus_spread_mid | train | 16 | -4.93 | -6.49 | -68.13 | 56.53 | 79,688 |
| minus_spread_mid | train | 17 | -4.71 | -6.17 | -67.77 | 57.64 | 79,688 |
| minus_spread_mid | train | 18 | -4.51 | -5.97 | -66.53 | 56.99 | 79,688 |
| minus_spread_mid | train | 19 | -4.31 | -5.80 | -66.87 | 57.33 | 79,688 |
| minus_spread_mid | train | 20 | -4.13 | -5.48 | -66.60 | 57.79 | 79,688 |
| minus_spread_mid | train | 21 | -3.95 | -5.21 | -65.90 | 56.80 | 79,688 |
| minus_spread_mid | train | 22 | -3.77 | -4.89 | -65.19 | 56.61 | 79,688 |
| minus_spread_mid | train | 23 | -3.59 | -4.59 | -64.74 | 58.54 | 79,688 |
| minus_spread_mid | train | 24 | -3.42 | -4.35 | -64.96 | 57.72 | 79,688 |
| minus_spread_mid | train | 25 | -3.24 | -4.37 | -64.57 | 57.49 | 79,688 |
| minus_spread_mid | train | 26 | -3.06 | -4.27 | -64.16 | 57.64 | 79,688 |
| minus_spread_mid | train | 27 | -2.89 | -3.78 | -63.67 | 57.47 | 79,688 |
| minus_spread_mid | train | 28 | -2.72 | -3.73 | -63.25 | 57.72 | 79,688 |
| minus_spread_mid | train | 29 | -2.56 | -3.45 | -62.33 | 57.95 | 79,688 |
| minus_spread_mid | train | 30 | -2.40 | -3.39 | -62.18 | 57.22 | 79,688 |
| minus_spread_mid | train | 31 | -2.25 | -2.85 | -60.58 | 57.91 | 79,688 |
| minus_spread_mid | train | 32 | -2.10 | -3.06 | -61.19 | 56.95 | 79,688 |
| minus_spread_mid | train | 33 | -1.95 | -3.13 | -60.54 | 56.66 | 79,688 |
| minus_spread_mid | train | 34 | -1.81 | -2.87 | -60.35 | 57.31 | 79,688 |
| minus_spread_mid | train | 35 | -1.67 | -2.45 | -60.69 | 57.60 | 79,688 |
| minus_spread_mid | train | 36 | -1.54 | -2.63 | -60.73 | 57.87 | 79,688 |
| minus_spread_mid | train | 37 | -1.41 | -2.25 | -59.66 | 57.37 | 79,688 |
| minus_spread_mid | train | 38 | -1.29 | -1.82 | -58.06 | 57.77 | 79,688 |
| minus_spread_mid | train | 39 | -1.17 | -1.98 | -58.67 | 55.62 | 79,688 |
| minus_spread_mid | train | 40 | -1.07 | -1.65 | -56.95 | 55.39 | 79,688 |
| minus_spread_mid | train | 41 | -0.96 | -1.34 | -55.92 | 55.47 | 79,688 |
| minus_spread_mid | train | 42 | -0.86 | -1.28 | -56.15 | 56.02 | 79,688 |
| minus_spread_mid | train | 43 | -0.76 | -1.42 | -55.85 | 54.92 | 79,688 |
| minus_spread_mid | train | 44 | -0.67 | -1.07 | -54.55 | 55.01 | 79,688 |
| minus_spread_mid | train | 45 | -0.58 | -1.11 | -54.63 | 54.51 | 79,688 |
| minus_spread_mid | train | 46 | -0.49 | -0.94 | -54.86 | 54.36 | 79,688 |
| minus_spread_mid | train | 47 | -0.39 | -0.70 | -54.46 | 54.97 | 79,688 |
| minus_spread_mid | train | 48 | -0.30 | -0.76 | -54.47 | 55.01 | 79,688 |
| minus_spread_mid | train | 49 | -0.21 | -0.44 | -53.94 | 55.68 | 79,688 |
| minus_spread_mid | train | 50 | -0.11 | -0.42 | -54.28 | 55.58 | 79,688 |
| minus_spread_mid | train | 51 | -0.02 | -0.45 | -55.15 | 56.79 | 79,688 |
| minus_spread_mid | train | 52 | 0.08 | -0.28 | -55.39 | 57.22 | 79,688 |
| minus_spread_mid | train | 53 | 0.18 | 0.05 | -55.81 | 59.09 | 79,688 |
| minus_spread_mid | train | 54 | 0.29 | -0.19 | -56.53 | 59.78 | 79,688 |
| minus_spread_mid | train | 55 | 0.40 | 0.02 | -56.72 | 60.31 | 79,688 |
| minus_spread_mid | train | 56 | 0.51 | 0.17 | -56.61 | 59.74 | 79,688 |
| minus_spread_mid | train | 57 | 0.63 | 0.18 | -56.50 | 60.41 | 79,688 |
| minus_spread_mid | train | 58 | 0.74 | 0.39 | -56.50 | 60.58 | 79,688 |
| minus_spread_mid | train | 59 | 0.85 | 0.76 | -56.23 | 61.19 | 79,688 |
| minus_spread_mid | train | 60 | 0.97 | 0.85 | -56.52 | 62.68 | 79,688 |
| minus_spread_mid | train | 61 | 1.09 | 0.86 | -56.19 | 61.99 | 79,688 |
| minus_spread_mid | train | 62 | 1.21 | 0.91 | -56.23 | 62.01 | 79,688 |
| minus_spread_mid | train | 63 | 1.33 | 0.95 | -56.30 | 62.68 | 79,688 |
| minus_spread_mid | train | 64 | 1.45 | 1.18 | -56.95 | 62.41 | 79,688 |
| minus_spread_mid | train | 65 | 1.57 | 1.32 | -56.42 | 63.48 | 79,688 |
| minus_spread_mid | train | 66 | 1.70 | 1.52 | -55.73 | 62.87 | 79,688 |
| minus_spread_mid | train | 67 | 1.83 | 1.74 | -56.72 | 64.35 | 79,688 |
| minus_spread_mid | train | 68 | 1.96 | 1.71 | -57.14 | 64.28 | 79,688 |
| minus_spread_mid | train | 69 | 2.09 | 1.93 | -56.08 | 64.51 | 79,687 |
| minus_spread_mid | train | 70 | 2.23 | 2.16 | -55.92 | 64.39 | 79,687 |
| minus_spread_mid | train | 71 | 2.37 | 2.14 | -56.08 | 63.78 | 79,687 |
| minus_spread_mid | train | 72 | 2.51 | 2.63 | -55.27 | 65.12 | 79,687 |
| minus_spread_mid | train | 73 | 2.66 | 2.66 | -55.77 | 65.54 | 79,687 |
| minus_spread_mid | train | 74 | 2.82 | 2.57 | -56.30 | 65.57 | 79,687 |
| minus_spread_mid | train | 75 | 2.97 | 2.85 | -56.46 | 66.45 | 79,687 |
| minus_spread_mid | train | 76 | 3.14 | 3.05 | -55.96 | 66.71 | 79,687 |
| minus_spread_mid | train | 77 | 3.31 | 3.40 | -56.65 | 67.90 | 79,687 |
| minus_spread_mid | train | 78 | 3.49 | 3.47 | -57.33 | 68.92 | 79,687 |
| minus_spread_mid | train | 79 | 3.68 | 3.51 | -57.14 | 69.43 | 79,687 |
| minus_spread_mid | train | 80 | 3.87 | 3.65 | -57.26 | 69.77 | 79,687 |
| minus_spread_mid | train | 81 | 4.08 | 3.90 | -57.98 | 70.69 | 79,687 |
| minus_spread_mid | train | 82 | 4.30 | 4.37 | -58.24 | 71.95 | 79,687 |
| minus_spread_mid | train | 83 | 4.53 | 4.35 | -59.17 | 72.59 | 79,687 |
| minus_spread_mid | train | 84 | 4.78 | 4.58 | -59.47 | 73.89 | 79,687 |
| minus_spread_mid | train | 85 | 5.05 | 5.14 | -59.66 | 75.26 | 79,687 |
| minus_spread_mid | train | 86 | 5.33 | 5.31 | -60.58 | 76.79 | 79,687 |
| minus_spread_mid | train | 87 | 5.65 | 5.50 | -61.42 | 76.64 | 79,687 |
| minus_spread_mid | train | 88 | 5.98 | 5.98 | -61.34 | 79.42 | 79,687 |
| minus_spread_mid | train | 89 | 6.36 | 6.28 | -63.21 | 81.02 | 79,687 |
| minus_spread_mid | train | 90 | 6.78 | 6.52 | -64.16 | 82.86 | 79,687 |
| minus_spread_mid | train | 91 | 7.24 | 6.98 | -65.12 | 84.46 | 79,687 |
| minus_spread_mid | train | 92 | 7.78 | 7.23 | -67.29 | 86.75 | 79,687 |
| minus_spread_mid | train | 93 | 8.40 | 8.12 | -67.67 | 90.33 | 79,687 |
| minus_spread_mid | train | 94 | 9.14 | 8.74 | -70.04 | 93.77 | 79,687 |
| minus_spread_mid | train | 95 | 10.04 | 9.32 | -72.05 | 97.58 | 79,687 |
| minus_spread_mid | train | 96 | 11.19 | 10.61 | -74.46 | 102.16 | 79,687 |
| minus_spread_mid | train | 97 | 12.73 | 11.41 | -78.74 | 106.81 | 79,687 |
| minus_spread_mid | train | 98 | 15.03 | 14.07 | -82.93 | 117.87 | 79,687 |
| minus_spread_mid | train | 99 | 19.12 | 17.46 | -89.62 | 133.67 | 79,687 |
| minus_spread_mid | train | 100 | 34.91 | 29.92 | -106.12 | 186.46 | 79,687 |

### 3.4. Top-k Robustness

![Top-k Mean Label](images/figure-015.png "Top-k Mean Label")

test split k_pct vs mean_label_bps. 

![Top-k Hit Rate](images/figure-016.png "Top-k Hit Rate")

test split k_pct vs hit_rate. 

![Top-k Selected Fraction](images/figure-017.png "Top-k Selected Fraction")

test split k_pct vs selected_fraction. 

| experiment | split | selection_method | k_pct | universe_count | selected_count | selected_fraction | prediction_threshold | mean_label_bps | median_label_bps | label_std_bps | hit_rate | day_count | timestamp_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| minus_depth | test | approx_quantile_threshold | 1 | 176,945,440 | 1,741,750 | 0.98% | 0.001941 | 13.70 | 0.01 | 94.75 | 47.44% | 100 | 16,100 |
| minus_depth | test | approx_quantile_threshold | 2 | 176,945,440 | 3,491,698 | 1.97% | 0.001425 | 11.01 | 0.00 | 81.54 | 46.52% | 100 | 16,100 |
| minus_depth | test | approx_quantile_threshold | 3 | 176,945,440 | 5,292,443 | 2.99% | 0.001176 | 9.53 | 0.00 | 74.67 | 46.01% | 100 | 16,100 |
| minus_depth | test | approx_quantile_threshold | 5 | 176,945,440 | 8,804,608 | 4.98% | 0.000911 | 7.86 | 0.00 | 67.03 | 45.30% | 100 | 16,100 |
| minus_depth | test | approx_quantile_threshold | 10 | 176,945,440 | 17,693,128 | 10.00% | 0.000595 | 5.85 | 0.00 | 58.00 | 44.21% | 100 | 16,100 |
| minus_depth | test | approx_quantile_threshold | 15 | 176,945,440 | 26,547,716 | 15.00% | 0.000428 | 4.80 | 0.00 | 53.44 | 43.48% | 100 | 16,100 |
| minus_depth | test | approx_quantile_threshold | 20 | 176,945,440 | 35,393,088 | 20.00% | 0.000313 | 4.12 | 0.00 | 50.52 | 42.94% | 100 | 16,100 |
| minus_depth | train | approx_quantile_threshold | 1 | 7,968,768 | 79,612 | 1.00% | 0.002358 | 42.08 | 29.74 | 103.46 | 63.52% | 12 | 1,932 |
| minus_depth | train | approx_quantile_threshold | 2 | 7,968,768 | 158,328 | 1.99% | 0.001732 | 31.38 | 21.47 | 88.78 | 59.64% | 12 | 1,932 |
| minus_depth | train | approx_quantile_threshold | 3 | 7,968,768 | 238,415 | 2.99% | 0.001411 | 26.06 | 17.28 | 81.51 | 57.44% | 12 | 1,932 |
| minus_depth | train | approx_quantile_threshold | 5 | 7,968,768 | 395,824 | 4.97% | 0.001069 | 20.82 | 12.50 | 73.52 | 54.91% | 12 | 1,932 |
| minus_depth | train | approx_quantile_threshold | 10 | 7,968,768 | 793,359 | 9.96% | 0.000681 | 14.96 | 6.04 | 63.87 | 51.70% | 12 | 1,932 |
| minus_depth | train | approx_quantile_threshold | 15 | 7,968,768 | 1,192,410 | 14.96% | 0.000480 | 12.10 | 1.72 | 58.89 | 49.78% | 12 | 1,932 |
| minus_depth | train | approx_quantile_threshold | 20 | 7,968,768 | 1,589,588 | 19.95% | 0.000345 | 10.34 | 0.16 | 55.68 | 48.44% | 12 | 1,932 |
| minus_imbalance | test | approx_quantile_threshold | 1 | 176,945,440 | 1,748,814 | 0.99% | 0.001773 | 13.61 | 0.00 | 90.43 | 46.83% | 100 | 16,100 |
| minus_imbalance | test | approx_quantile_threshold | 2 | 176,945,440 | 3,502,602 | 1.98% | 0.001318 | 10.31 | 0.00 | 78.53 | 45.68% | 100 | 16,100 |
| minus_imbalance | test | approx_quantile_threshold | 3 | 176,945,440 | 5,280,660 | 2.98% | 0.001104 | 8.79 | 0.00 | 72.22 | 45.12% | 100 | 16,100 |
| minus_imbalance | test | approx_quantile_threshold | 5 | 176,945,440 | 8,864,812 | 5.01% | 0.000872 | 7.15 | 0.00 | 64.97 | 44.43% | 100 | 16,100 |
| minus_imbalance | test | approx_quantile_threshold | 10 | 176,945,440 | 17,660,216 | 9.98% | 0.000607 | 5.36 | 0.00 | 56.57 | 43.50% | 100 | 16,100 |
| minus_imbalance | test | approx_quantile_threshold | 15 | 176,945,440 | 26,518,231 | 14.99% | 0.000463 | 4.43 | 0.00 | 52.25 | 42.86% | 100 | 16,100 |
| minus_imbalance | test | approx_quantile_threshold | 20 | 176,945,440 | 35,408,583 | 20.01% | 0.000361 | 3.80 | 0.00 | 49.44 | 42.35% | 100 | 16,100 |
| minus_imbalance | train | approx_quantile_threshold | 1 | 7,968,768 | 78,662 | 0.99% | 0.002100 | 30.15 | 19.62 | 91.98 | 56.59% | 12 | 1,932 |
| minus_imbalance | train | approx_quantile_threshold | 2 | 7,968,768 | 158,129 | 1.98% | 0.001543 | 23.40 | 13.08 | 82.49 | 54.03% | 12 | 1,932 |
| minus_imbalance | train | approx_quantile_threshold | 3 | 7,968,768 | 237,031 | 2.97% | 0.001277 | 20.07 | 9.32 | 77.48 | 52.65% | 12 | 1,932 |
| minus_imbalance | train | approx_quantile_threshold | 5 | 7,968,768 | 398,635 | 5.00% | 0.000991 | 16.47 | 5.07 | 70.83 | 51.19% | 12 | 1,932 |
| minus_imbalance | train | approx_quantile_threshold | 10 | 7,968,768 | 795,107 | 9.98% | 0.000675 | 12.24 | 0.57 | 62.82 | 48.96% | 12 | 1,932 |
| minus_imbalance | train | approx_quantile_threshold | 15 | 7,968,768 | 1,193,067 | 14.97% | 0.000509 | 10.10 | 0.00 | 58.51 | 47.57% | 12 | 1,932 |
| minus_imbalance | train | approx_quantile_threshold | 20 | 7,968,768 | 1,593,453 | 20.00% | 0.000394 | 8.68 | 0.00 | 55.60 | 46.50% | 12 | 1,932 |
| minus_quality | test | approx_quantile_threshold | 1 | 176,945,440 | 1,749,382 | 0.99% | 0.001986 | 14.97 | 0.05 | 98.87 | 47.91% | 100 | 16,100 |
| minus_quality | test | approx_quantile_threshold | 2 | 176,945,440 | 3,510,240 | 1.98% | 0.001511 | 11.08 | 0.00 | 84.77 | 46.20% | 100 | 16,100 |
| minus_quality | test | approx_quantile_threshold | 3 | 176,945,440 | 5,268,920 | 2.98% | 0.001276 | 9.30 | 0.00 | 77.55 | 45.38% | 100 | 16,100 |
| minus_quality | test | approx_quantile_threshold | 5 | 176,945,440 | 8,833,948 | 4.99% | 0.001006 | 7.47 | 0.00 | 69.19 | 44.54% | 100 | 16,100 |
| minus_quality | test | approx_quantile_threshold | 10 | 176,945,440 | 17,684,020 | 9.99% | 0.000673 | 5.57 | 0.00 | 59.59 | 43.57% | 100 | 16,100 |
| minus_quality | test | approx_quantile_threshold | 15 | 176,945,440 | 26,499,938 | 14.98% | 0.000508 | 4.63 | 0.00 | 54.58 | 42.98% | 100 | 16,100 |
| minus_quality | test | approx_quantile_threshold | 20 | 176,945,440 | 35,366,928 | 19.99% | 0.000405 | 4.01 | 0.00 | 51.29 | 42.53% | 100 | 16,100 |
| minus_quality | train | approx_quantile_threshold | 1 | 7,968,768 | 78,062 | 0.98% | 0.002359 | 33.78 | 24.36 | 99.53 | 59.32% | 12 | 1,932 |
| minus_quality | train | approx_quantile_threshold | 2 | 7,968,768 | 158,575 | 1.99% | 0.001757 | 25.77 | 16.52 | 87.85 | 55.95% | 12 | 1,932 |
| minus_quality | train | approx_quantile_threshold | 3 | 7,968,768 | 236,643 | 2.97% | 0.001471 | 22.00 | 12.58 | 81.86 | 54.21% | 12 | 1,932 |
| minus_quality | train | approx_quantile_threshold | 5 | 7,968,768 | 394,981 | 4.96% | 0.001151 | 17.78 | 7.56 | 74.73 | 52.13% | 12 | 1,932 |
| minus_quality | train | approx_quantile_threshold | 10 | 7,968,768 | 794,250 | 9.97% | 0.000768 | 13.03 | 1.26 | 65.47 | 49.54% | 12 | 1,932 |
| minus_quality | train | approx_quantile_threshold | 15 | 7,968,768 | 1,192,805 | 14.97% | 0.000565 | 10.69 | 0.05 | 60.43 | 48.06% | 12 | 1,932 |
| minus_quality | train | approx_quantile_threshold | 20 | 7,968,768 | 1,592,197 | 19.98% | 0.000446 | 9.16 | 0.01 | 56.94 | 46.92% | 12 | 1,932 |
| minus_spread_mid | test | approx_quantile_threshold | 1 | 176,945,440 | 1,721,380 | 0.97% | 0.001901 | 11.64 | 0.00 | 99.74 | 45.31% | 100 | 16,100 |
| minus_spread_mid | test | approx_quantile_threshold | 2 | 176,945,440 | 3,510,368 | 1.98% | 0.001410 | 8.94 | 0.00 | 86.03 | 44.29% | 100 | 16,100 |
| minus_spread_mid | test | approx_quantile_threshold | 3 | 176,945,440 | 5,254,615 | 2.97% | 0.001177 | 7.74 | 0.00 | 78.90 | 43.79% | 100 | 16,100 |
| minus_spread_mid | test | approx_quantile_threshold | 5 | 176,945,440 | 8,810,405 | 4.98% | 0.000917 | 6.34 | 0.00 | 70.41 | 43.24% | 100 | 16,100 |
| minus_spread_mid | test | approx_quantile_threshold | 10 | 176,945,440 | 17,644,208 | 9.97% | 0.000621 | 4.80 | 0.00 | 60.19 | 42.65% | 100 | 16,100 |
| minus_spread_mid | test | approx_quantile_threshold | 15 | 176,945,440 | 26,532,732 | 14.99% | 0.000467 | 4.01 | 0.00 | 54.90 | 42.28% | 100 | 16,100 |
| minus_spread_mid | test | approx_quantile_threshold | 20 | 176,945,440 | 35,354,135 | 19.98% | 0.000363 | 3.49 | 0.00 | 51.51 | 41.97% | 100 | 16,100 |
| minus_spread_mid | train | approx_quantile_threshold | 1 | 7,968,768 | 79,137 | 0.99% | 0.002257 | 30.01 | 20.33 | 99.91 | 57.05% | 12 | 1,932 |
| minus_spread_mid | train | approx_quantile_threshold | 2 | 7,968,768 | 157,830 | 1.98% | 0.001667 | 23.75 | 14.45 | 88.79 | 54.70% | 12 | 1,932 |
| minus_spread_mid | train | approx_quantile_threshold | 3 | 7,968,768 | 238,428 | 2.99% | 0.001373 | 20.51 | 11.20 | 82.65 | 53.38% | 12 | 1,932 |
| minus_spread_mid | train | approx_quantile_threshold | 5 | 7,968,768 | 397,793 | 4.99% | 0.001057 | 16.70 | 6.52 | 75.22 | 51.55% | 12 | 1,932 |
| minus_spread_mid | train | approx_quantile_threshold | 10 | 7,968,768 | 796,271 | 9.99% | 0.000701 | 12.38 | 0.80 | 65.55 | 49.16% | 12 | 1,932 |
| minus_spread_mid | train | approx_quantile_threshold | 15 | 7,968,768 | 1,194,127 | 14.99% | 0.000519 | 10.24 | 0.12 | 60.36 | 47.82% | 12 | 1,932 |
| minus_spread_mid | train | approx_quantile_threshold | 20 | 7,968,768 | 1,592,429 | 19.98% | 0.000398 | 8.79 | 0.00 | 56.92 | 46.79% | 12 | 1,932 |

### 4. Important Stock Pool And Liquidity

### 4.1. Important Stock Pool

![Important Pool Pearson IC](images/figure-018.png "Important Pool Pearson IC")

pool x experiment Pearson IC. 

![Important Pool Rank IC](images/figure-019.png "Important Pool Rank IC")

pool x experiment rank IC. 

![Important Pool Mean Real Return](images/figure-020.png "Important Pool Mean Real Return")

pool x experiment mean realized return. 

| experiment | pool | display_name | etf_code | index_code | pearson_ic | rank_ic | count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| minus_depth | csi1000_etf_sh | 1000 ETF | 512100.SH | 000852.SH | 0.0557 | 0.0421 | 33,009,991 |
| minus_imbalance | csi1000_etf_sh | 1000 ETF | 512100.SH | 000852.SH | 0.0538 | 0.0374 | 33,009,991 |
| minus_quality | csi1000_etf_sh | 1000 ETF | 512100.SH | 000852.SH | 0.0590 | 0.0415 | 33,009,991 |
| minus_spread_mid | csi1000_etf_sh | 1000 ETF | 512100.SH | 000852.SH | 0.0482 | 0.0376 | 33,009,991 |
| minus_depth | csi300_etf_sh | 沪深300 ETF(沪) | 510300.SH | 000300.SH | 0.0409 | 0.0335 | 9,903,593 |
| minus_imbalance | csi300_etf_sh | 沪深300 ETF(沪) | 510300.SH | 000300.SH | 0.0392 | 0.0286 | 9,903,593 |
| minus_quality | csi300_etf_sh | 沪深300 ETF(沪) | 510300.SH | 000300.SH | 0.0465 | 0.0381 | 9,903,593 |
| minus_spread_mid | csi300_etf_sh | 沪深300 ETF(沪) | 510300.SH | 000300.SH | 0.0392 | 0.0374 | 9,903,593 |
| minus_depth | csi500_etf_sh | 中证500 ETF(沪) | 510500.SH | 000905.SH | 0.0444 | 0.0371 | 16,505,559 |
| minus_imbalance | csi500_etf_sh | 中证500 ETF(沪) | 510500.SH | 000905.SH | 0.0417 | 0.0321 | 16,505,559 |
| minus_quality | csi500_etf_sh | 中证500 ETF(沪) | 510500.SH | 000905.SH | 0.0500 | 0.0401 | 16,505,559 |
| minus_spread_mid | csi500_etf_sh | 中证500 ETF(沪) | 510500.SH | 000905.SH | 0.0431 | 0.0386 | 16,505,559 |

### 4.2. Important Pool Prediction Curve

![Important Pool Prediction Curve](images/figure-021.png "Important Pool Prediction Curve")

prediction_bin vs mean_real_return. 

![Important Pool Prediction Positive Ratio](images/figure-022.png "Important Pool Prediction Positive Ratio")

prediction_bin vs real_return_positive_ratio. 

Important Pool Prediction Curve Table

| experiment | pool | prediction_bin | mean_prediction_return | mean_real_return | real_return_positive_ratio | count |
| --- | --- | --- | --- | --- | --- | --- |
| minus_depth | csi1000_etf_sh | 1 | -0.001399 | -0.000381 | 38.25% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 2 | -0.000767 | -0.000162 | 38.74% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 3 | -0.000583 | -0.000112 | 38.77% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 4 | -0.000477 | -0.000094 | 38.51% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 5 | -0.000398 | -0.000083 | 38.51% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 6 | -0.000330 | -0.000069 | 38.47% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 7 | -0.000271 | -0.000062 | 38.50% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 8 | -0.000218 | -0.000048 | 38.43% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 9 | -0.000168 | -0.000031 | 38.83% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 10 | -0.000120 | -0.000015 | 38.71% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 11 | -0.000072 | -0.000001 | 38.82% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 12 | -0.000023 | 0.000019 | 38.77% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 13 | 0.000028 | 0.000030 | 38.77% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 14 | 0.000082 | 0.000057 | 39.34% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 15 | 0.000143 | 0.000075 | 39.85% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 16 | 0.000213 | 0.000103 | 40.35% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 17 | 0.000297 | 0.000138 | 40.98% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 18 | 0.000409 | 0.000175 | 41.51% | 1,650,404 |
| minus_depth | csi1000_etf_sh | 19 | 0.000584 | 0.000243 | 42.29% | 1,650,403 |
| minus_depth | csi1000_etf_sh | 20 | 0.001199 | 0.000448 | 44.02% | 1,650,403 |
| minus_imbalance | csi1000_etf_sh | 1 | -0.000943 | -0.000395 | 38.94% | 1,650,477 |
| minus_imbalance | csi1000_etf_sh | 2 | -0.000535 | -0.000122 | 39.66% | 1,650,477 |
| minus_imbalance | csi1000_etf_sh | 3 | -0.000420 | -0.000099 | 39.23% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 4 | -0.000333 | -0.000101 | 38.52% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 5 | -0.000259 | -0.000075 | 38.61% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 6 | -0.000194 | -0.000067 | 38.23% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 7 | -0.000139 | -0.000068 | 37.39% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 8 | -0.000092 | -0.000051 | 37.46% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 9 | -0.000049 | -0.000033 | 38.35% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 10 | -0.000006 | -0.000014 | 38.78% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 11 | 0.000037 | 0.000010 | 39.23% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 12 | 0.000082 | 0.000020 | 39.30% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 13 | 0.000128 | 0.000039 | 39.45% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 14 | 0.000178 | 0.000054 | 39.60% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 15 | 0.000232 | 0.000087 | 40.05% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 16 | 0.000294 | 0.000103 | 40.27% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 17 | 0.000368 | 0.000132 | 40.57% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 18 | 0.000465 | 0.000178 | 41.23% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 19 | 0.000611 | 0.000223 | 41.97% | 1,650,476 |
| minus_imbalance | csi1000_etf_sh | 20 | 0.001097 | 0.000406 | 43.58% | 1,650,476 |
| minus_quality | csi1000_etf_sh | 1 | -0.000992 | -0.000440 | 38.07% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 2 | -0.000594 | -0.000178 | 38.40% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 3 | -0.000450 | -0.000142 | 38.25% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 4 | -0.000356 | -0.000121 | 38.25% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 5 | -0.000275 | -0.000105 | 38.07% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 6 | -0.000203 | -0.000076 | 38.38% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 7 | -0.000144 | -0.000061 | 38.25% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 8 | -0.000097 | -0.000045 | 38.50% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 9 | -0.000054 | -0.000026 | 38.30% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 10 | -0.000009 | -0.000008 | 38.28% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 11 | 0.000038 | 0.000022 | 38.88% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 12 | 0.000088 | 0.000036 | 39.62% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 13 | 0.000142 | 0.000047 | 39.85% | 1,650,390 |
| minus_quality | csi1000_etf_sh | 14 | 0.000201 | 0.000077 | 40.23% | 1,650,389 |
| minus_quality | csi1000_etf_sh | 15 | 0.000264 | 0.000097 | 40.37% | 1,650,389 |
| minus_quality | csi1000_etf_sh | 16 | 0.000331 | 0.000129 | 40.60% | 1,650,389 |
| minus_quality | csi1000_etf_sh | 17 | 0.000407 | 0.000154 | 41.02% | 1,650,389 |
| minus_quality | csi1000_etf_sh | 18 | 0.000507 | 0.000192 | 41.38% | 1,650,389 |
| minus_quality | csi1000_etf_sh | 19 | 0.000680 | 0.000242 | 42.16% | 1,650,389 |
| minus_quality | csi1000_etf_sh | 20 | 0.001282 | 0.000435 | 43.57% | 1,650,389 |
| minus_spread_mid | csi1000_etf_sh | 1 | -0.001039 | -0.000355 | 38.71% | 1,650,391 |
| minus_spread_mid | csi1000_etf_sh | 2 | -0.000597 | -0.000149 | 39.35% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 3 | -0.000451 | -0.000115 | 38.83% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 4 | -0.000359 | -0.000109 | 38.27% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 5 | -0.000275 | -0.000085 | 38.40% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 6 | -0.000202 | -0.000065 | 38.56% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 7 | -0.000140 | -0.000055 | 38.45% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 8 | -0.000092 | -0.000042 | 37.57% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 9 | -0.000049 | -0.000028 | 37.35% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 10 | -0.000007 | -0.000009 | 38.18% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 11 | 0.000037 | 0.000012 | 39.46% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 12 | 0.000083 | 0.000024 | 39.64% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 13 | 0.000130 | 0.000051 | 39.96% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 14 | 0.000180 | 0.000063 | 40.04% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 15 | 0.000235 | 0.000087 | 40.40% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 16 | 0.000297 | 0.000104 | 40.57% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 17 | 0.000372 | 0.000135 | 40.93% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 18 | 0.000472 | 0.000172 | 41.47% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 19 | 0.000630 | 0.000218 | 41.74% | 1,650,390 |
| minus_spread_mid | csi1000_etf_sh | 20 | 0.001201 | 0.000374 | 42.51% | 1,650,390 |
| minus_depth | csi300_etf_sh | 1 | -0.000995 | -0.000227 | 40.12% | 495,142 |
| minus_depth | csi300_etf_sh | 2 | -0.000559 | -0.000072 | 40.75% | 495,142 |
| minus_depth | csi300_etf_sh | 3 | -0.000431 | -0.000064 | 40.14% | 495,142 |
| minus_depth | csi300_etf_sh | 4 | -0.000350 | -0.000043 | 40.19% | 495,142 |
| minus_depth | csi300_etf_sh | 5 | -0.000288 | -0.000035 | 40.28% | 495,142 |
| minus_depth | csi300_etf_sh | 6 | -0.000236 | -0.000023 | 40.51% | 495,142 |
| minus_depth | csi300_etf_sh | 7 | -0.000190 | -0.000020 | 40.62% | 495,142 |
| minus_depth | csi300_etf_sh | 8 | -0.000148 | -0.000011 | 40.55% | 495,142 |
| minus_depth | csi300_etf_sh | 9 | -0.000108 | -0.000004 | 40.88% | 495,142 |
| minus_depth | csi300_etf_sh | 10 | -0.000069 | 0.000009 | 40.93% | 495,142 |
| minus_depth | csi300_etf_sh | 11 | -0.000030 | 0.000014 | 41.06% | 495,141 |
| minus_depth | csi300_etf_sh | 12 | 0.000010 | 0.000024 | 41.21% | 495,141 |
| minus_depth | csi300_etf_sh | 13 | 0.000052 | 0.000035 | 41.50% | 495,141 |
| minus_depth | csi300_etf_sh | 14 | 0.000097 | 0.000049 | 41.64% | 495,141 |
| minus_depth | csi300_etf_sh | 15 | 0.000146 | 0.000059 | 41.78% | 495,141 |
| minus_depth | csi300_etf_sh | 16 | 0.000203 | 0.000076 | 42.00% | 495,141 |
| minus_depth | csi300_etf_sh | 17 | 0.000270 | 0.000090 | 42.16% | 495,141 |
| minus_depth | csi300_etf_sh | 18 | 0.000358 | 0.000121 | 42.72% | 495,141 |
| minus_depth | csi300_etf_sh | 19 | 0.000494 | 0.000167 | 43.19% | 495,141 |
| minus_depth | csi300_etf_sh | 20 | 0.000907 | 0.000309 | 45.50% | 495,141 |
| minus_imbalance | csi300_etf_sh | 1 | -0.000658 | -0.000198 | 41.96% | 495,178 |
| minus_imbalance | csi300_etf_sh | 2 | -0.000405 | -0.000070 | 41.57% | 495,178 |
| minus_imbalance | csi300_etf_sh | 3 | -0.000305 | -0.000064 | 40.52% | 495,178 |
| minus_imbalance | csi300_etf_sh | 4 | -0.000229 | -0.000035 | 40.69% | 495,178 |
| minus_imbalance | csi300_etf_sh | 5 | -0.000170 | -0.000045 | 40.63% | 495,178 |
| minus_imbalance | csi300_etf_sh | 6 | -0.000126 | -0.000034 | 40.48% | 495,178 |
| minus_imbalance | csi300_etf_sh | 7 | -0.000087 | -0.000032 | 40.67% | 495,177 |
| minus_imbalance | csi300_etf_sh | 8 | -0.000049 | -0.000018 | 40.70% | 495,177 |
| minus_imbalance | csi300_etf_sh | 9 | -0.000012 | -0.000010 | 40.76% | 495,177 |
| minus_imbalance | csi300_etf_sh | 10 | 0.000025 | 0.000015 | 41.01% | 495,177 |
| minus_imbalance | csi300_etf_sh | 11 | 0.000063 | 0.000028 | 40.92% | 495,177 |
| minus_imbalance | csi300_etf_sh | 12 | 0.000101 | 0.000042 | 41.02% | 495,177 |
| minus_imbalance | csi300_etf_sh | 13 | 0.000142 | 0.000042 | 40.89% | 495,177 |
| minus_imbalance | csi300_etf_sh | 14 | 0.000184 | 0.000050 | 41.04% | 495,177 |
| minus_imbalance | csi300_etf_sh | 15 | 0.000231 | 0.000065 | 41.10% | 495,177 |
| minus_imbalance | csi300_etf_sh | 16 | 0.000283 | 0.000072 | 41.41% | 495,177 |
| minus_imbalance | csi300_etf_sh | 17 | 0.000344 | 0.000097 | 41.80% | 495,177 |
| minus_imbalance | csi300_etf_sh | 18 | 0.000421 | 0.000121 | 42.20% | 495,177 |
| minus_imbalance | csi300_etf_sh | 19 | 0.000535 | 0.000152 | 43.01% | 495,177 |
| minus_imbalance | csi300_etf_sh | 20 | 0.000858 | 0.000277 | 45.33% | 495,177 |
| minus_quality | csi300_etf_sh | 1 | -0.000728 | -0.000243 | 40.62% | 495,142 |
| minus_quality | csi300_etf_sh | 2 | -0.000429 | -0.000114 | 40.30% | 495,142 |
| minus_quality | csi300_etf_sh | 3 | -0.000318 | -0.000098 | 39.78% | 495,142 |
| minus_quality | csi300_etf_sh | 4 | -0.000234 | -0.000077 | 39.73% | 495,142 |
| minus_quality | csi300_etf_sh | 5 | -0.000171 | -0.000057 | 39.73% | 495,142 |
| minus_quality | csi300_etf_sh | 6 | -0.000126 | -0.000042 | 40.24% | 495,142 |
| minus_quality | csi300_etf_sh | 7 | -0.000088 | -0.000030 | 40.49% | 495,142 |
| minus_quality | csi300_etf_sh | 8 | -0.000050 | -0.000022 | 40.62% | 495,142 |
| minus_quality | csi300_etf_sh | 9 | -0.000013 | -0.000023 | 40.81% | 495,141 |
| minus_quality | csi300_etf_sh | 10 | 0.000026 | 0.000002 | 40.92% | 495,141 |
| minus_quality | csi300_etf_sh | 11 | 0.000067 | 0.000025 | 41.19% | 495,141 |
| minus_quality | csi300_etf_sh | 12 | 0.000109 | 0.000042 | 41.32% | 495,141 |
| minus_quality | csi300_etf_sh | 13 | 0.000154 | 0.000042 | 41.32% | 495,141 |
| minus_quality | csi300_etf_sh | 14 | 0.000201 | 0.000066 | 41.54% | 495,141 |
| minus_quality | csi300_etf_sh | 15 | 0.000252 | 0.000081 | 41.79% | 495,141 |
| minus_quality | csi300_etf_sh | 16 | 0.000305 | 0.000121 | 42.16% | 495,141 |
| minus_quality | csi300_etf_sh | 17 | 0.000365 | 0.000140 | 42.64% | 495,141 |
| minus_quality | csi300_etf_sh | 18 | 0.000443 | 0.000160 | 43.25% | 495,141 |
| minus_quality | csi300_etf_sh | 19 | 0.000574 | 0.000189 | 43.93% | 495,141 |
| minus_quality | csi300_etf_sh | 20 | 0.000997 | 0.000293 | 45.33% | 495,141 |
| minus_spread_mid | csi300_etf_sh | 1 | -0.000849 | -0.000195 | 41.57% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 2 | -0.000508 | -0.000093 | 41.24% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 3 | -0.000402 | -0.000082 | 40.48% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 4 | -0.000317 | -0.000065 | 40.37% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 5 | -0.000245 | -0.000052 | 40.24% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 6 | -0.000185 | -0.000048 | 40.15% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 7 | -0.000136 | -0.000029 | 40.19% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 8 | -0.000096 | -0.000026 | 40.04% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 9 | -0.000060 | -0.000008 | 40.29% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 10 | -0.000024 | 0.000009 | 40.54% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 11 | 0.000013 | 0.000008 | 40.58% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 12 | 0.000051 | 0.000031 | 41.02% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 13 | 0.000090 | 0.000045 | 41.12% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 14 | 0.000132 | 0.000062 | 41.22% | 495,140 |
| minus_spread_mid | csi300_etf_sh | 15 | 0.000177 | 0.000084 | 41.73% | 495,139 |
| minus_spread_mid | csi300_etf_sh | 16 | 0.000228 | 0.000102 | 42.06% | 495,139 |
| minus_spread_mid | csi300_etf_sh | 17 | 0.000288 | 0.000116 | 42.51% | 495,139 |
| minus_spread_mid | csi300_etf_sh | 18 | 0.000365 | 0.000142 | 43.18% | 495,139 |
| minus_spread_mid | csi300_etf_sh | 19 | 0.000480 | 0.000178 | 43.89% | 495,139 |
| minus_spread_mid | csi300_etf_sh | 20 | 0.000838 | 0.000276 | 45.29% | 495,139 |
| minus_depth | csi500_etf_sh | 1 | -0.001117 | -0.000268 | 38.67% | 825,226 |
| minus_depth | csi500_etf_sh | 2 | -0.000641 | -0.000129 | 38.79% | 825,226 |
| minus_depth | csi500_etf_sh | 3 | -0.000493 | -0.000118 | 38.03% | 825,226 |
| minus_depth | csi500_etf_sh | 4 | -0.000406 | -0.000099 | 37.94% | 825,226 |
| minus_depth | csi500_etf_sh | 5 | -0.000337 | -0.000088 | 37.91% | 825,226 |
| minus_depth | csi500_etf_sh | 6 | -0.000279 | -0.000078 | 37.94% | 825,226 |
| minus_depth | csi500_etf_sh | 7 | -0.000228 | -0.000068 | 38.08% | 825,226 |
| minus_depth | csi500_etf_sh | 8 | -0.000182 | -0.000050 | 38.45% | 825,226 |
| minus_depth | csi500_etf_sh | 9 | -0.000138 | -0.000037 | 38.43% | 825,226 |
| minus_depth | csi500_etf_sh | 10 | -0.000095 | -0.000026 | 38.65% | 825,226 |
| minus_depth | csi500_etf_sh | 11 | -0.000052 | -0.000018 | 38.70% | 825,226 |
| minus_depth | csi500_etf_sh | 12 | -0.000008 | 0.000011 | 38.99% | 825,226 |
| minus_depth | csi500_etf_sh | 13 | 0.000038 | 0.000016 | 39.21% | 825,226 |
| minus_depth | csi500_etf_sh | 14 | 0.000087 | 0.000037 | 39.54% | 825,226 |
| minus_depth | csi500_etf_sh | 15 | 0.000142 | 0.000053 | 39.66% | 825,226 |
| minus_depth | csi500_etf_sh | 16 | 0.000205 | 0.000069 | 39.87% | 825,226 |
| minus_depth | csi500_etf_sh | 17 | 0.000280 | 0.000107 | 40.26% | 825,225 |
| minus_depth | csi500_etf_sh | 18 | 0.000378 | 0.000133 | 40.55% | 825,225 |
| minus_depth | csi500_etf_sh | 19 | 0.000528 | 0.000187 | 41.05% | 825,225 |
| minus_depth | csi500_etf_sh | 20 | 0.000986 | 0.000339 | 42.48% | 825,225 |
| minus_imbalance | csi500_etf_sh | 1 | -0.000735 | -0.000256 | 39.98% | 825,272 |
| minus_imbalance | csi500_etf_sh | 2 | -0.000447 | -0.000110 | 39.70% | 825,272 |
| minus_imbalance | csi500_etf_sh | 3 | -0.000341 | -0.000108 | 38.76% | 825,272 |
| minus_imbalance | csi500_etf_sh | 4 | -0.000260 | -0.000085 | 38.62% | 825,272 |
| minus_imbalance | csi500_etf_sh | 5 | -0.000193 | -0.000088 | 38.37% | 825,271 |
| minus_imbalance | csi500_etf_sh | 6 | -0.000142 | -0.000078 | 38.23% | 825,271 |
| minus_imbalance | csi500_etf_sh | 7 | -0.000099 | -0.000073 | 38.12% | 825,271 |
| minus_imbalance | csi500_etf_sh | 8 | -0.000059 | -0.000054 | 38.50% | 825,271 |
| minus_imbalance | csi500_etf_sh | 9 | -0.000021 | -0.000051 | 38.41% | 825,271 |
| minus_imbalance | csi500_etf_sh | 10 | 0.000017 | -0.000019 | 38.81% | 825,271 |
| minus_imbalance | csi500_etf_sh | 11 | 0.000056 | -0.000009 | 38.75% | 825,271 |
| minus_imbalance | csi500_etf_sh | 12 | 0.000096 | 0.000009 | 38.74% | 825,271 |
| minus_imbalance | csi500_etf_sh | 13 | 0.000138 | 0.000024 | 38.77% | 825,271 |
| minus_imbalance | csi500_etf_sh | 14 | 0.000182 | 0.000044 | 38.93% | 825,271 |
| minus_imbalance | csi500_etf_sh | 15 | 0.000231 | 0.000063 | 39.16% | 825,271 |
| minus_imbalance | csi500_etf_sh | 16 | 0.000286 | 0.000074 | 39.16% | 825,271 |
| minus_imbalance | csi500_etf_sh | 17 | 0.000352 | 0.000088 | 39.38% | 825,271 |
| minus_imbalance | csi500_etf_sh | 18 | 0.000435 | 0.000132 | 39.92% | 825,271 |
| minus_imbalance | csi500_etf_sh | 19 | 0.000558 | 0.000176 | 40.60% | 825,271 |
| minus_imbalance | csi500_etf_sh | 20 | 0.000915 | 0.000293 | 42.28% | 825,271 |
| minus_quality | csi500_etf_sh | 1 | -0.000831 | -0.000330 | 38.08% | 825,219 |
| minus_quality | csi500_etf_sh | 2 | -0.000507 | -0.000174 | 38.09% | 825,219 |
| minus_quality | csi500_etf_sh | 3 | -0.000383 | -0.000141 | 38.05% | 825,219 |
| minus_quality | csi500_etf_sh | 4 | -0.000295 | -0.000126 | 37.70% | 825,218 |
| minus_quality | csi500_etf_sh | 5 | -0.000219 | -0.000108 | 37.94% | 825,218 |
| minus_quality | csi500_etf_sh | 6 | -0.000159 | -0.000085 | 38.04% | 825,218 |
| minus_quality | csi500_etf_sh | 7 | -0.000114 | -0.000071 | 38.46% | 825,218 |
| minus_quality | csi500_etf_sh | 8 | -0.000073 | -0.000051 | 38.54% | 825,218 |
| minus_quality | csi500_etf_sh | 9 | -0.000033 | -0.000039 | 38.59% | 825,218 |
| minus_quality | csi500_etf_sh | 10 | 0.000009 | -0.000033 | 38.61% | 825,218 |
| minus_quality | csi500_etf_sh | 11 | 0.000054 | -0.000006 | 39.03% | 825,218 |
| minus_quality | csi500_etf_sh | 12 | 0.000100 | 0.000019 | 39.34% | 825,218 |
| minus_quality | csi500_etf_sh | 13 | 0.000150 | 0.000030 | 39.33% | 825,218 |
| minus_quality | csi500_etf_sh | 14 | 0.000203 | 0.000060 | 39.54% | 825,218 |
| minus_quality | csi500_etf_sh | 15 | 0.000260 | 0.000082 | 39.69% | 825,218 |
| minus_quality | csi500_etf_sh | 16 | 0.000320 | 0.000112 | 39.82% | 825,218 |
| minus_quality | csi500_etf_sh | 17 | 0.000387 | 0.000131 | 40.11% | 825,218 |
| minus_quality | csi500_etf_sh | 18 | 0.000474 | 0.000166 | 40.54% | 825,218 |
| minus_quality | csi500_etf_sh | 19 | 0.000618 | 0.000212 | 41.29% | 825,218 |
| minus_quality | csi500_etf_sh | 20 | 0.001084 | 0.000325 | 42.41% | 825,218 |
| minus_spread_mid | csi500_etf_sh | 1 | -0.000895 | -0.000255 | 39.36% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 2 | -0.000528 | -0.000141 | 39.08% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 3 | -0.000409 | -0.000135 | 38.31% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 4 | -0.000318 | -0.000116 | 38.02% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 5 | -0.000239 | -0.000092 | 37.99% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 6 | -0.000174 | -0.000080 | 38.21% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 7 | -0.000121 | -0.000072 | 38.05% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 8 | -0.000079 | -0.000056 | 37.85% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 9 | -0.000039 | -0.000039 | 38.38% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 10 | 0.000001 | -0.000024 | 38.39% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 11 | 0.000042 | -0.000010 | 38.92% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 12 | 0.000083 | 0.000003 | 39.01% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 13 | 0.000127 | 0.000023 | 39.21% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 14 | 0.000173 | 0.000039 | 39.51% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 15 | 0.000223 | 0.000060 | 39.66% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 16 | 0.000279 | 0.000087 | 40.02% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 17 | 0.000346 | 0.000119 | 40.38% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 18 | 0.000434 | 0.000145 | 40.54% | 825,220 |
| minus_spread_mid | csi500_etf_sh | 19 | 0.000566 | 0.000201 | 41.01% | 825,219 |
| minus_spread_mid | csi500_etf_sh | 20 | 0.000987 | 0.000313 | 41.30% | 825,219 |

### 4.3. Liquidity By ADV

![ADV Bucket IC](images/figure-023.png "ADV Bucket IC")

adv_bucket vs mean_ic. 

![ADV Bucket Rank IC](images/figure-024.png "ADV Bucket Rank IC")

adv_bucket vs mean_rank_ic. 

![ADV Bucket Top5 Return](images/figure-025.png "ADV Bucket Top5 Return")

adv_bucket vs top5_return_bps. 

![ADV Bucket Top5 Hit Rate](images/figure-026.png "ADV Bucket Top5 Hit Rate")

adv_bucket vs top5_hit_rate. 

| experiment | adv_bucket | bucket_label | row_count | day_count | mean_adv_amount | median_adv_amount | mean_ic | mean_rank_ic | icir | rank_icir | top5_return_bps | top5_hit_rate | top5_row_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| minus_depth | 1 | Bottom20% | 33,213,495 | 100 | 22436.36 | 23206.28 | 0.1207 | 0.1004 | 4.3632 | 6.2246 | 9.87 | 44.04% | 1,667,316 |
| minus_depth | 2 | 20~40% | 33,714,849 | 100 | 46291.44 | 45970.54 | 0.0834 | 0.0688 | 4.0821 | 5.2337 | 5.81 | 42.39% | 1,693,237 |
| minus_depth | 3 | 40~60% | 33,822,880 | 100 | 78908.09 | 77696.15 | 0.0910 | 0.0710 | 3.8299 | 4.7398 | 6.28 | 43.82% | 1,698,228 |
| minus_depth | 4 | 60~80% | 33,743,507 | 100 | 145624.17 | 141032.77 | 0.0969 | 0.0766 | 4.7060 | 4.2715 | 7.22 | 45.25% | 1,694,364 |
| minus_depth | 5 | Top20% | 33,697,783 | 100 | 553370.17 | 359596.79 | 0.1000 | 0.0806 | 3.8978 | 3.8417 | 7.33 | 47.41% | 1,692,110 |
| minus_imbalance | 1 | Bottom20% | 33,213,495 | 100 | 22436.36 | 23206.28 | 0.1162 | 0.0910 | 4.6240 | 5.7302 | 9.35 | 43.12% | 1,667,316 |
| minus_imbalance | 2 | 20~40% | 33,714,849 | 100 | 46291.44 | 45970.54 | 0.0759 | 0.0571 | 4.1198 | 3.9381 | 5.23 | 41.89% | 1,693,237 |
| minus_imbalance | 3 | 40~60% | 33,822,880 | 100 | 78908.09 | 77696.15 | 0.0825 | 0.0585 | 4.2255 | 3.5271 | 5.80 | 43.43% | 1,698,228 |
| minus_imbalance | 4 | 60~80% | 33,743,507 | 100 | 145624.17 | 141032.77 | 0.0990 | 0.0642 | 4.4697 | 3.5237 | 6.85 | 44.78% | 1,694,364 |
| minus_imbalance | 5 | Top20% | 33,697,783 | 100 | 553370.17 | 359596.79 | 0.1078 | 0.0717 | 3.9794 | 2.9797 | 7.45 | 47.21% | 1,692,110 |
| minus_quality | 1 | Bottom20% | 33,213,495 | 100 | 22436.36 | 23206.28 | 0.1182 | 0.0902 | 5.2662 | 6.1792 | 9.81 | 43.64% | 1,667,316 |
| minus_quality | 2 | 20~40% | 33,714,849 | 100 | 46291.44 | 45970.54 | 0.0801 | 0.0594 | 4.2780 | 4.7254 | 5.89 | 42.01% | 1,693,237 |
| minus_quality | 3 | 40~60% | 33,822,880 | 100 | 78908.09 | 77696.15 | 0.0875 | 0.0630 | 4.9930 | 4.1537 | 6.42 | 43.44% | 1,698,228 |
| minus_quality | 4 | 60~80% | 33,743,507 | 100 | 145624.17 | 141032.77 | 0.1032 | 0.0704 | 5.0490 | 4.1272 | 7.63 | 44.99% | 1,694,364 |
| minus_quality | 5 | Top20% | 33,697,783 | 100 | 553370.17 | 359596.79 | 0.1110 | 0.0764 | 4.2372 | 3.4379 | 8.04 | 47.22% | 1,692,110 |
| minus_spread_mid | 1 | Bottom20% | 33,213,495 | 100 | 22436.36 | 23206.28 | 0.1080 | 0.0828 | 4.2664 | 5.2479 | 8.67 | 42.23% | 1,667,316 |
| minus_spread_mid | 2 | 20~40% | 33,714,849 | 100 | 46291.44 | 45970.54 | 0.0693 | 0.0574 | 4.4115 | 4.6320 | 5.25 | 40.56% | 1,693,237 |
| minus_spread_mid | 3 | 40~60% | 33,822,880 | 100 | 78908.09 | 77696.15 | 0.0756 | 0.0609 | 4.5611 | 4.4375 | 5.65 | 42.09% | 1,698,228 |
| minus_spread_mid | 4 | 60~80% | 33,743,507 | 100 | 145624.17 | 141032.77 | 0.0874 | 0.0664 | 4.6632 | 4.4702 | 6.61 | 43.87% | 1,694,364 |
| minus_spread_mid | 5 | Top20% | 33,697,783 | 100 | 553370.17 | 359596.79 | 0.0886 | 0.0659 | 4.0214 | 3.6269 | 6.38 | 46.15% | 1,692,110 |

### 5. Trading And Cost Proxy

### 5.1. Strategy And Benchmark Summary

![Test Strategy NAV By Pool](images/figure-027.png "Test Strategy NAV By Pool")

test split-rebased strategy NAV. 

![Val/Test Strategy Return By Pool](images/figure-028.png "Val/Test Strategy Return By Pool")

val/test split strategy_return_bps; 不拼接为连续 NAV. 

![Test Full-Hold Benchmark By Pool](images/figure-029.png "Test Full-Hold Benchmark By Pool")

test split full-hold benchmark rebased NAV. 

![Strategy Return By Pool](images/figure-030.png "Strategy Return By Pool")

pool x experiment strategy return. 

![Excess Vs Full-Hold Benchmark By Pool](images/figure-031.png "Excess Vs Full-Hold Benchmark By Pool")

pool x experiment strategy return minus full-hold benchmark return. 

![Position Rate By Pool](images/figure-032.png "Position Rate By Pool")

pool x experiment position rate. 

Strategy NAV 只在 test split 内画连续路径, 并按 test 首个有效 NAV rebased 到 1.0; val 与 test 不是同一条可交易路径, 因此不再把两段拼成一张 NAV 图. Val/Test 对比改用 split 内 strategy_return_bps 柱状图, val 作为验证期诊断, test 作为 OOS 评估. Full-hold benchmark 单独作为 market context 展示. 本节表格的 strategy/full-hold benchmark/expected return 均按 test split 的 end/start - 1 计算. excess_vs_full_hold_benchmark_bps 是稀疏持仓策略相对全程持有 benchmark 的差, 不应直接解读为 alpha. 

| experiment | pool | strategy_return_bps | full_hold_benchmark_return_bps | excess_vs_full_hold_benchmark_bps | expected_return_bps | position_rate | open_count | open_per_day |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| minus_depth | csi1000_etf_sh | -244.29 | 1585.00 | -1829.29 | 614.88 | 4.60% | 118 | 1.18 |
| minus_imbalance | csi1000_etf_sh | 124.17 | 1585.00 | -1460.83 | 839.20 | 4.75% | 111 | 1.11 |
| minus_quality | csi1000_etf_sh | -80.50 | 1585.00 | -1665.50 | 832.60 | 4.60% | 111 | 1.11 |
| minus_spread_mid | csi1000_etf_sh | -45.10 | 1585.00 | -1630.10 | 763.16 | 4.50% | 111 | 1.11 |
| minus_depth | csi300_etf_sh | 207.72 | 4304.38 | -4096.66 | 597.42 | 4.63% | 128 | 1.28 |
| minus_imbalance | csi300_etf_sh | 177.54 | 4304.38 | -4126.84 | 820.91 | 5.12% | 132 | 1.32 |
| minus_quality | csi300_etf_sh | 348.58 | 4304.38 | -3955.80 | 786.54 | 4.81% | 142 | 1.42 |
| minus_spread_mid | csi300_etf_sh | 124.34 | 4304.38 | -4180.04 | 628.82 | 4.66% | 132 | 1.32 |
| minus_depth | csi500_etf_sh | -55.00 | -361.75 | 306.76 | 545.19 | 4.44% | 120 | 1.20 |
| minus_imbalance | csi500_etf_sh | 6.44 | -361.75 | 368.20 | 764.32 | 4.63% | 114 | 1.14 |
| minus_quality | csi500_etf_sh | 139.24 | -361.75 | 500.99 | 821.98 | 4.78% | 126 | 1.26 |
| minus_spread_mid | csi500_etf_sh | -108.10 | -361.75 | 253.65 | 722.37 | 4.75% | 126 | 1.26 |

### 5.2. Cost Sensitivity

![Cost Sensitivity By Experiment](images/figure-033.png "Cost Sensitivity By Experiment")

single_side_cost_bps vs test_net_strategy_return_bps by pool. 

![Cost Sensitivity Average](images/figure-034.png "Cost Sensitivity Average")

cross-pool average test cost sensitivity. 

Cost sensitivity 使用 test-only cost sensitivity artifact; 0 bps cost 的 test_net_strategy_return_bps 与 5.1 的 test strategy_return_bps 口径一致. 

| experiment | pool | single_side_cost_bps | test_net_strategy_return_bps |
| --- | --- | --- | --- |
| minus_depth | csi1000_etf_sh | 0.0 | -244.29 |
| minus_imbalance | csi1000_etf_sh | 0.0 | 124.17 |
| minus_quality | csi1000_etf_sh | 0.0 | -80.50 |
| minus_spread_mid | csi1000_etf_sh | 0.0 | -45.10 |
| minus_depth | csi1000_etf_sh | 1.0 | -471.86 |
| minus_imbalance | csi1000_etf_sh | 1.0 | -97.11 |
| minus_quality | csi1000_etf_sh | 1.0 | -298.30 |
| minus_spread_mid | csi1000_etf_sh | 1.0 | -263.66 |
| minus_depth | csi1000_etf_sh | 2.0 | -694.14 |
| minus_imbalance | csi1000_etf_sh | 2.0 | -313.57 |
| minus_quality | csi1000_etf_sh | 2.0 | -511.33 |
| minus_spread_mid | csi1000_etf_sh | 2.0 | -477.45 |
| minus_depth | csi1000_etf_sh | 5.0 | -1330.47 |
| minus_imbalance | csi1000_etf_sh | 5.0 | -935.11 |
| minus_quality | csi1000_etf_sh | 5.0 | -1122.88 |
| minus_spread_mid | csi1000_etf_sh | 5.0 | -1091.18 |
| minus_depth | csi1000_etf_sh | 10.0 | -2296.17 |
| minus_imbalance | csi1000_etf_sh | 10.0 | -1884.01 |
| minus_quality | csi1000_etf_sh | 10.0 | -2056.16 |
| minus_spread_mid | csi1000_etf_sh | 10.0 | -2027.79 |
| minus_depth | csi300_etf_sh | 0.0 | 207.72 |
| minus_imbalance | csi300_etf_sh | 0.0 | 177.54 |
| minus_quality | csi300_etf_sh | 0.0 | 348.58 |
| minus_spread_mid | csi300_etf_sh | 0.0 | 124.34 |
| minus_depth | csi300_etf_sh | 1.0 | -50.27 |
| minus_imbalance | csi300_etf_sh | 1.0 | -87.64 |
| minus_quality | csi300_etf_sh | 1.0 | 58.83 |
| minus_spread_mid | csi300_etf_sh | 1.0 | -139.45 |
| minus_depth | csi300_etf_sh | 2.0 | -301.76 |
| minus_imbalance | csi300_etf_sh | 2.0 | -345.93 |
| minus_quality | csi300_etf_sh | 2.0 | -222.84 |
| minus_spread_mid | csi300_etf_sh | 2.0 | -396.39 |
| minus_depth | csi300_etf_sh | 5.0 | -1018.86 |
| minus_imbalance | csi300_etf_sh | 5.0 | -1081.26 |
| minus_quality | csi300_etf_sh | 5.0 | -1021.55 |
| minus_spread_mid | csi300_etf_sh | 5.0 | -1127.89 |
| minus_depth | csi300_etf_sh | 10.0 | -2098.56 |
| minus_imbalance | csi300_etf_sh | 10.0 | -2184.88 |
| minus_quality | csi300_etf_sh | 10.0 | -2210.83 |
| minus_spread_mid | csi300_etf_sh | 10.0 | -2225.75 |
| minus_depth | csi500_etf_sh | 0.0 | -55.00 |
| minus_imbalance | csi500_etf_sh | 0.0 | 6.44 |
| minus_quality | csi500_etf_sh | 0.0 | 139.24 |
| minus_spread_mid | csi500_etf_sh | 0.0 | -108.10 |
| minus_depth | csi500_etf_sh | 1.0 | -290.86 |
| minus_imbalance | csi500_etf_sh | 1.0 | -220.13 |
| minus_quality | csi500_etf_sh | 1.0 | -113.09 |
| minus_spread_mid | csi500_etf_sh | 1.0 | -354.29 |
| minus_depth | csi500_etf_sh | 2.0 | -521.16 |
| minus_imbalance | csi500_etf_sh | 2.0 | -441.59 |
| minus_quality | csi500_etf_sh | 2.0 | -359.16 |
| minus_spread_mid | csi500_etf_sh | 2.0 | -594.37 |
| minus_depth | csi500_etf_sh | 5.0 | -1179.90 |
| minus_imbalance | csi500_etf_sh | 5.0 | -1076.45 |
| minus_quality | csi500_etf_sh | 5.0 | -1061.37 |
| minus_spread_mid | csi500_etf_sh | 5.0 | -1279.49 |
| minus_depth | csi500_etf_sh | 10.0 | -2178.04 |
| minus_imbalance | csi500_etf_sh | 10.0 | -2042.62 |
| minus_quality | csi500_etf_sh | 10.0 | -2120.31 |
| minus_spread_mid | csi500_etf_sh | 10.0 | -2312.64 |

### 5.3. Trade Return Distribution

![Test Split Trade Return Box Plot](images/figure-035.png "Test Split Trade Return Box Plot")

test split trade_return_bps box plot. 

![Trade Hit Rate](images/figure-036.png "Trade Hit Rate")

pool x experiment trade hit rate. 

Trade return distribution 图, hit-rate 图和主表均使用 test scope; box plot 隐藏 fliers, 菱形 marker 为 mean, x 轴标签中的 n 为 test trades 数量. 包含 train_val_test 聚合 scope 的完整 summary 仍保留在 CSV artifact 中. 

| experiment | pool | scope | trade_count | mean_trade_return_bps | median_trade_return_bps | hit_rate | p05_trade_return_bps | p95_trade_return_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| minus_depth | csi1000_etf_sh | test | 118 | -2.05 | 0.24 | 50.85% | -39.03 | 32.81 |
| minus_imbalance | csi1000_etf_sh | test | 111 | 1.15 | 3.52 | 60.36% | -43.55 | 39.09 |
| minus_quality | csi1000_etf_sh | test | 111 | -0.68 | 2.27 | 55.86% | -47.01 | 33.57 |
| minus_spread_mid | csi1000_etf_sh | test | 111 | -0.37 | 1.34 | 55.86% | -44.38 | 32.53 |
| minus_depth | csi300_etf_sh | test | 128 | 1.62 | 2.00 | 59.38% | -25.98 | 23.94 |
| minus_imbalance | csi300_etf_sh | test | 133 | 1.33 | 1.37 | 57.89% | -26.09 | 21.43 |
| minus_quality | csi300_etf_sh | test | 142 | 2.43 | 1.79 | 59.15% | -21.10 | 27.00 |
| minus_spread_mid | csi300_etf_sh | test | 132 | 0.95 | 1.79 | 58.33% | -21.95 | 23.00 |
| minus_depth | csi500_etf_sh | test | 120 | -0.44 | -0.52 | 47.50% | -35.19 | 27.78 |
| minus_imbalance | csi500_etf_sh | test | 115 | 0.08 | 1.64 | 53.04% | -39.37 | 30.51 |
| minus_quality | csi500_etf_sh | test | 126 | 1.13 | 1.38 | 53.17% | -34.32 | 30.94 |
| minus_spread_mid | csi500_etf_sh | test | 126 | -0.84 | 0.02 | 50.00% | -33.03 | 20.61 |

### 6. Robustness Diagnostics

### 6.1. Return Realization

![Return Realization Curve](images/figure-037.png "Return Realization Curve")

holding_minutes vs mean_return_bps. 

![Return Realization Row Count](images/figure-038.png "Return Realization Row Count")

holding_minutes vs row_count. 

| experiment | holding_minutes | mean_return | mean_return_bps | row_count | prediction_p95 |
| --- | --- | --- | --- | --- | --- |
| minus_depth | 1 | 0.000326 | 3.26 | 8,856,791 | 0.000908 |
| minus_depth | 2 | 0.000491 | 4.91 | 8,856,791 | 0.000908 |
| minus_depth | 3 | 0.000585 | 5.85 | 8,856,791 | 0.000908 |
| minus_depth | 4 | 0.000645 | 6.45 | 8,856,791 | 0.000908 |
| minus_depth | 5 | 0.000687 | 6.87 | 8,856,791 | 0.000908 |
| minus_depth | 6 | 0.000718 | 7.18 | 8,856,791 | 0.000908 |
| minus_depth | 7 | 0.000748 | 7.48 | 8,856,791 | 0.000908 |
| minus_depth | 8 | 0.000770 | 7.70 | 8,856,791 | 0.000908 |
| minus_depth | 9 | 0.000784 | 7.84 | 8,856,791 | 0.000908 |
| minus_depth | 10 | 0.000793 | 7.93 | 8,856,791 | 0.000908 |
| minus_depth | 11 | 0.000797 | 7.97 | 8,635,243 | 0.000908 |
| minus_depth | 12 | 0.000795 | 7.95 | 8,455,298 | 0.000908 |
| minus_depth | 13 | 0.000793 | 7.93 | 8,312,423 | 0.000908 |
| minus_depth | 14 | 0.000790 | 7.90 | 8,200,991 | 0.000908 |
| minus_depth | 15 | 0.000791 | 7.91 | 8,113,347 | 0.000908 |
| minus_depth | 16 | 0.000794 | 7.94 | 8,044,662 | 0.000908 |
| minus_depth | 17 | 0.000791 | 7.91 | 7,991,794 | 0.000908 |
| minus_depth | 18 | 0.000784 | 7.84 | 7,950,557 | 0.000908 |
| minus_depth | 19 | 0.000772 | 7.72 | 7,917,265 | 0.000908 |
| minus_depth | 20 | 0.000758 | 7.58 | 7,890,638 | 0.000908 |
| minus_imbalance | 1 | 0.000311 | 3.11 | 8,864,812 | 0.000872 |
| minus_imbalance | 2 | 0.000458 | 4.58 | 8,864,812 | 0.000872 |
| minus_imbalance | 3 | 0.000538 | 5.38 | 8,864,812 | 0.000872 |
| minus_imbalance | 4 | 0.000588 | 5.88 | 8,864,812 | 0.000872 |
| minus_imbalance | 5 | 0.000625 | 6.25 | 8,864,812 | 0.000872 |
| minus_imbalance | 6 | 0.000652 | 6.52 | 8,864,812 | 0.000872 |
| minus_imbalance | 7 | 0.000680 | 6.80 | 8,864,812 | 0.000872 |
| minus_imbalance | 8 | 0.000700 | 7.00 | 8,864,812 | 0.000872 |
| minus_imbalance | 9 | 0.000715 | 7.15 | 8,864,812 | 0.000872 |
| minus_imbalance | 10 | 0.000723 | 7.23 | 8,864,812 | 0.000872 |
| minus_imbalance | 11 | 0.000720 | 7.20 | 8,626,462 | 0.000872 |
| minus_imbalance | 12 | 0.000712 | 7.12 | 8,428,961 | 0.000872 |
| minus_imbalance | 13 | 0.000704 | 7.04 | 8,270,683 | 0.000872 |
| minus_imbalance | 14 | 0.000695 | 6.95 | 8,150,666 | 0.000872 |
| minus_imbalance | 15 | 0.000692 | 6.92 | 8,058,127 | 0.000872 |
| minus_imbalance | 16 | 0.000688 | 6.88 | 7,984,254 | 0.000872 |
| minus_imbalance | 17 | 0.000678 | 6.78 | 7,926,639 | 0.000872 |
| minus_imbalance | 18 | 0.000660 | 6.60 | 7,880,954 | 0.000872 |
| minus_imbalance | 19 | 0.000641 | 6.41 | 7,844,489 | 0.000872 |
| minus_imbalance | 20 | 0.000624 | 6.24 | 7,814,674 | 0.000872 |
| minus_quality | 1 | 0.000343 | 3.43 | 8,854,293 | 0.001006 |
| minus_quality | 2 | 0.000495 | 4.95 | 8,854,293 | 0.001006 |
| minus_quality | 3 | 0.000577 | 5.77 | 8,854,293 | 0.001006 |
| minus_quality | 4 | 0.000628 | 6.28 | 8,854,293 | 0.001006 |
| minus_quality | 5 | 0.000662 | 6.62 | 8,854,293 | 0.001006 |
| minus_quality | 6 | 0.000689 | 6.89 | 8,854,293 | 0.001006 |
| minus_quality | 7 | 0.000714 | 7.14 | 8,854,293 | 0.001006 |
| minus_quality | 8 | 0.000734 | 7.34 | 8,854,293 | 0.001006 |
| minus_quality | 9 | 0.000746 | 7.46 | 8,854,293 | 0.001006 |
| minus_quality | 10 | 0.000754 | 7.54 | 8,854,293 | 0.001006 |
| minus_quality | 11 | 0.000751 | 7.51 | 8,662,934 | 0.001006 |
| minus_quality | 12 | 0.000745 | 7.45 | 8,509,614 | 0.001006 |
| minus_quality | 13 | 0.000742 | 7.42 | 8,388,885 | 0.001006 |
| minus_quality | 14 | 0.000739 | 7.39 | 8,294,161 | 0.001006 |
| minus_quality | 15 | 0.000738 | 7.38 | 8,219,945 | 0.001006 |
| minus_quality | 16 | 0.000737 | 7.37 | 8,159,523 | 0.001006 |
| minus_quality | 17 | 0.000730 | 7.30 | 8,110,992 | 0.001006 |
| minus_quality | 18 | 0.000719 | 7.19 | 8,071,627 | 0.001006 |
| minus_quality | 19 | 0.000704 | 7.04 | 8,039,336 | 0.001006 |
| minus_quality | 20 | 0.000689 | 6.89 | 8,012,527 | 0.001006 |
| minus_spread_mid | 1 | 0.000255 | 2.55 | 8,853,901 | 0.000916 |
| minus_spread_mid | 2 | 0.000379 | 3.79 | 8,853,901 | 0.000916 |
| minus_spread_mid | 3 | 0.000453 | 4.53 | 8,853,901 | 0.000916 |
| minus_spread_mid | 4 | 0.000504 | 5.04 | 8,853,901 | 0.000916 |
| minus_spread_mid | 5 | 0.000540 | 5.40 | 8,853,901 | 0.000916 |
| minus_spread_mid | 6 | 0.000570 | 5.70 | 8,853,901 | 0.000916 |
| minus_spread_mid | 7 | 0.000597 | 5.97 | 8,853,901 | 0.000916 |
| minus_spread_mid | 8 | 0.000618 | 6.18 | 8,853,901 | 0.000916 |
| minus_spread_mid | 9 | 0.000633 | 6.33 | 8,853,901 | 0.000916 |
| minus_spread_mid | 10 | 0.000641 | 6.41 | 8,853,901 | 0.000916 |
| minus_spread_mid | 11 | 0.000640 | 6.40 | 8,674,948 | 0.000916 |
| minus_spread_mid | 12 | 0.000634 | 6.34 | 8,532,830 | 0.000916 |
| minus_spread_mid | 13 | 0.000632 | 6.32 | 8,419,585 | 0.000916 |
| minus_spread_mid | 14 | 0.000628 | 6.28 | 8,329,928 | 0.000916 |
| minus_spread_mid | 15 | 0.000626 | 6.26 | 8,256,776 | 0.000916 |
| minus_spread_mid | 16 | 0.000622 | 6.22 | 8,196,864 | 0.000916 |
| minus_spread_mid | 17 | 0.000613 | 6.13 | 8,147,601 | 0.000916 |
| minus_spread_mid | 18 | 0.000597 | 5.97 | 8,106,443 | 0.000916 |
| minus_spread_mid | 19 | 0.000579 | 5.79 | 8,071,966 | 0.000916 |
| minus_spread_mid | 20 | 0.000559 | 5.59 | 8,041,842 | 0.000916 |

### 6.2. Monthly IC

![Monthly Pearson IC](images/figure-039.png "Monthly Pearson IC")

month vs pearson_ic. 

![Monthly Rank IC](images/figure-040.png "Monthly Rank IC")

month vs rank_ic. 

| experiment | month | pearson_ic | rank_ic | sample_count |
| --- | --- | --- | --- | --- |
| minus_depth | 2024/03 | 0.0803 | 0.0596 | 40,561,535 |
| minus_depth | 2024/04 | 0.0914 | 0.0834 | 34,533,212 |
| minus_depth | 2024/05 | 0.0781 | 0.0643 | 34,535,788 |
| minus_depth | 2024/06 | 0.0740 | 0.0563 | 32,818,884 |
| minus_depth | 2024/07 | 0.0666 | 0.0524 | 34,496,021 |
| minus_imbalance | 2024/03 | 0.0845 | 0.0545 | 40,561,535 |
| minus_imbalance | 2024/04 | 0.0878 | 0.0742 | 34,533,212 |
| minus_imbalance | 2024/05 | 0.0749 | 0.0590 | 34,535,788 |
| minus_imbalance | 2024/06 | 0.0807 | 0.0508 | 32,818,884 |
| minus_imbalance | 2024/07 | 0.0718 | 0.0562 | 34,496,021 |
| minus_quality | 2024/03 | 0.0839 | 0.0567 | 40,561,535 |
| minus_quality | 2024/04 | 0.0908 | 0.0751 | 34,533,212 |
| minus_quality | 2024/05 | 0.0789 | 0.0611 | 34,535,788 |
| minus_quality | 2024/06 | 0.0843 | 0.0535 | 32,818,884 |
| minus_quality | 2024/07 | 0.0814 | 0.0608 | 34,496,021 |
| minus_spread_mid | 2024/03 | 0.0652 | 0.0473 | 40,561,535 |
| minus_spread_mid | 2024/04 | 0.0827 | 0.0732 | 34,533,212 |
| minus_spread_mid | 2024/05 | 0.0652 | 0.0566 | 34,535,788 |
| minus_spread_mid | 2024/06 | 0.0698 | 0.0444 | 32,818,884 |
| minus_spread_mid | 2024/07 | 0.0627 | 0.0484 | 34,496,021 |

### 6.3. Intraday IC

![Intraday Pearson IC](images/figure-041.png "Intraday Pearson IC")

test split time_bucket vs pearson_ic. 

Intraday IC Table

| experiment | split | time_bucket | pearson_ic | rank_ic | sample_count |
| --- | --- | --- | --- | --- | --- |
| minus_depth | test | 103900.0 | 0.0689 | n/a | 1,099,040 |
| minus_depth | test | 104000.0 | 0.0687 | n/a | 1,099,040 |
| minus_depth | test | 104100.0 | 0.0760 | n/a | 1,099,040 |
| minus_depth | test | 104200.0 | 0.0848 | n/a | 1,099,040 |
| minus_depth | test | 104300.0 | 0.0871 | n/a | 1,099,040 |
| minus_depth | test | 104400.0 | 0.0792 | n/a | 1,099,040 |
| minus_depth | test | 104500.0 | 0.0741 | n/a | 1,099,040 |
| minus_depth | test | 104600.0 | 0.0947 | n/a | 1,099,040 |
| minus_depth | test | 104700.0 | 0.0893 | n/a | 1,099,040 |
| minus_depth | test | 104800.0 | 0.0957 | n/a | 1,099,040 |
| minus_depth | test | 104900.0 | 0.0908 | n/a | 1,099,040 |
| minus_depth | test | 105000.0 | 0.0829 | n/a | 1,099,040 |
| minus_depth | test | 105100.0 | 0.0943 | n/a | 1,099,040 |
| minus_depth | test | 105200.0 | 0.0795 | n/a | 1,099,040 |
| minus_depth | test | 105300.0 | 0.0815 | n/a | 1,099,040 |
| minus_depth | test | 105400.0 | 0.0858 | n/a | 1,099,040 |
| minus_depth | test | 105500.0 | 0.0759 | n/a | 1,099,040 |
| minus_depth | test | 105600.0 | 0.0652 | n/a | 1,099,040 |
| minus_depth | test | 105700.0 | 0.0716 | n/a | 1,099,040 |
| minus_depth | test | 105800.0 | 0.0781 | n/a | 1,099,040 |
| minus_depth | test | 105900.0 | 0.0795 | n/a | 1,099,040 |
| minus_depth | test | 110000.0 | 0.0739 | n/a | 1,099,040 |
| minus_depth | test | 110100.0 | 0.0540 | n/a | 1,099,040 |
| minus_depth | test | 110200.0 | 0.0705 | n/a | 1,099,040 |
| minus_depth | test | 110300.0 | 0.0703 | n/a | 1,099,040 |
| minus_depth | test | 110400.0 | 0.0719 | n/a | 1,099,040 |
| minus_depth | test | 110500.0 | 0.0757 | n/a | 1,099,040 |
| minus_depth | test | 110600.0 | 0.0667 | n/a | 1,099,040 |
| minus_depth | test | 110700.0 | 0.0588 | n/a | 1,099,040 |
| minus_depth | test | 110800.0 | 0.0490 | n/a | 1,099,040 |
| minus_depth | test | 110900.0 | 0.0610 | n/a | 1,099,040 |
| minus_depth | test | 111000.0 | 0.0627 | n/a | 1,099,040 |
| minus_depth | test | 111100.0 | 0.0578 | n/a | 1,099,040 |
| minus_depth | test | 111200.0 | 0.0580 | n/a | 1,099,040 |
| minus_depth | test | 111300.0 | 0.0618 | n/a | 1,099,040 |
| minus_depth | test | 111400.0 | 0.0704 | n/a | 1,099,040 |
| minus_depth | test | 111500.0 | 0.0715 | n/a | 1,099,040 |
| minus_depth | test | 111600.0 | 0.0748 | n/a | 1,099,040 |
| minus_depth | test | 111700.0 | 0.0783 | n/a | 1,099,040 |
| minus_depth | test | 111800.0 | 0.0817 | n/a | 1,099,040 |
| minus_depth | test | 111900.0 | 0.0864 | n/a | 1,099,040 |
| minus_depth | test | 112000.0 | 0.0775 | n/a | 1,099,040 |
| minus_depth | test | 112100.0 | 0.0707 | n/a | 1,099,040 |
| minus_depth | test | 112200.0 | 0.0596 | n/a | 1,099,040 |
| minus_depth | test | 112300.0 | 0.0540 | n/a | 1,099,040 |
| minus_depth | test | 112400.0 | 0.0514 | n/a | 1,099,040 |
| minus_depth | test | 112500.0 | 0.0527 | n/a | 1,099,040 |
| minus_depth | test | 112600.0 | 0.0529 | n/a | 1,099,040 |
| minus_depth | test | 112700.0 | 0.0550 | n/a | 1,099,040 |
| minus_depth | test | 112800.0 | 0.0455 | n/a | 1,099,040 |
| minus_depth | test | 112900.0 | 0.0400 | n/a | 1,099,040 |
| minus_depth | test | 113000.0 | 0.0904 | n/a | 1,099,040 |
| minus_depth | test | 130100.0 | 0.0837 | n/a | 1,099,040 |
| minus_depth | test | 130200.0 | 0.0755 | n/a | 1,099,040 |
| minus_depth | test | 130300.0 | 0.0783 | n/a | 1,099,040 |
| minus_depth | test | 130400.0 | 0.0717 | n/a | 1,099,040 |
| minus_depth | test | 130500.0 | 0.0558 | n/a | 1,099,040 |
| minus_depth | test | 130600.0 | 0.0583 | n/a | 1,099,040 |
| minus_depth | test | 130700.0 | 0.0585 | n/a | 1,099,040 |
| minus_depth | test | 130800.0 | 0.0606 | n/a | 1,099,040 |
| minus_depth | test | 130900.0 | 0.0605 | n/a | 1,099,040 |
| minus_depth | test | 131000.0 | 0.0514 | n/a | 1,099,040 |
| minus_depth | test | 131100.0 | 0.0507 | n/a | 1,099,040 |
| minus_depth | test | 131200.0 | 0.0660 | n/a | 1,099,040 |
| minus_depth | test | 131300.0 | 0.0621 | n/a | 1,099,040 |
| minus_depth | test | 131400.0 | 0.0678 | n/a | 1,099,040 |
| minus_depth | test | 131500.0 | 0.0681 | n/a | 1,099,040 |
| minus_depth | test | 131600.0 | 0.0799 | n/a | 1,099,040 |
| minus_depth | test | 131700.0 | 0.0861 | n/a | 1,099,040 |
| minus_depth | test | 131800.0 | 0.0699 | n/a | 1,099,040 |
| minus_depth | test | 131900.0 | 0.0792 | n/a | 1,099,040 |
| minus_depth | test | 132000.0 | 0.0682 | n/a | 1,099,040 |
| minus_depth | test | 132100.0 | 0.0628 | n/a | 1,099,040 |
| minus_depth | test | 132200.0 | 0.0666 | n/a | 1,099,040 |
| minus_depth | test | 132300.0 | 0.0651 | n/a | 1,099,040 |
| minus_depth | test | 132400.0 | 0.0706 | n/a | 1,099,040 |
| minus_depth | test | 132500.0 | 0.0691 | n/a | 1,099,040 |
| minus_depth | test | 132600.0 | 0.0686 | n/a | 1,099,040 |
| minus_depth | test | 132700.0 | 0.0788 | n/a | 1,099,040 |
| minus_depth | test | 132800.0 | 0.0755 | n/a | 1,099,040 |
| minus_depth | test | 132900.0 | 0.0755 | n/a | 1,099,040 |
| minus_depth | test | 133000.0 | 0.0699 | n/a | 1,099,040 |
| minus_depth | test | 133100.0 | 0.0624 | n/a | 1,099,040 |
| minus_depth | test | 133200.0 | 0.0733 | n/a | 1,099,040 |
| minus_depth | test | 133300.0 | 0.0758 | n/a | 1,099,040 |
| minus_depth | test | 133400.0 | 0.0769 | n/a | 1,099,040 |
| minus_depth | test | 133500.0 | 0.0749 | n/a | 1,099,040 |
| minus_depth | test | 133600.0 | 0.0785 | n/a | 1,099,040 |
| minus_depth | test | 133700.0 | 0.0932 | n/a | 1,099,040 |
| minus_depth | test | 133800.0 | 0.0859 | n/a | 1,099,040 |
| minus_depth | test | 133900.0 | 0.0782 | n/a | 1,099,040 |
| minus_depth | test | 134000.0 | 0.0619 | n/a | 1,099,040 |
| minus_depth | test | 134100.0 | 0.0481 | n/a | 1,099,040 |
| minus_depth | test | 134200.0 | 0.0667 | n/a | 1,099,040 |
| minus_depth | test | 134300.0 | 0.0780 | n/a | 1,099,040 |
| minus_depth | test | 134400.0 | 0.0721 | n/a | 1,099,040 |
| minus_depth | test | 134500.0 | 0.0678 | n/a | 1,099,040 |
| minus_depth | test | 134600.0 | 0.0812 | n/a | 1,099,040 |
| minus_depth | test | 134700.0 | 0.0736 | n/a | 1,099,040 |
| minus_depth | test | 134800.0 | 0.0763 | n/a | 1,099,040 |
| minus_depth | test | 134900.0 | 0.0786 | n/a | 1,099,040 |
| minus_depth | test | 135000.0 | 0.0835 | n/a | 1,099,040 |
| minus_depth | test | 135100.0 | 0.0882 | n/a | 1,099,040 |
| minus_depth | test | 135200.0 | 0.0858 | n/a | 1,099,040 |
| minus_depth | test | 135300.0 | 0.0965 | n/a | 1,099,040 |
| minus_depth | test | 135400.0 | 0.0968 | n/a | 1,099,040 |
| minus_depth | test | 135500.0 | 0.0976 | n/a | 1,099,040 |
| minus_depth | test | 135600.0 | 0.1011 | n/a | 1,099,040 |
| minus_depth | test | 135700.0 | 0.1081 | n/a | 1,099,040 |
| minus_depth | test | 135800.0 | 0.1180 | n/a | 1,099,040 |
| minus_depth | test | 135900.0 | 0.1178 | n/a | 1,099,040 |
| minus_depth | test | 140000.0 | 0.0975 | n/a | 1,099,040 |
| minus_depth | test | 140100.0 | 0.1009 | n/a | 1,099,040 |
| minus_depth | test | 140200.0 | 0.1043 | n/a | 1,099,040 |
| minus_depth | test | 140300.0 | 0.1039 | n/a | 1,099,040 |
| minus_depth | test | 140400.0 | 0.1021 | n/a | 1,099,040 |
| minus_depth | test | 140500.0 | 0.0922 | n/a | 1,099,040 |
| minus_depth | test | 140600.0 | 0.1035 | n/a | 1,099,040 |
| minus_depth | test | 140700.0 | 0.1030 | n/a | 1,099,040 |
| minus_depth | test | 140800.0 | 0.0883 | n/a | 1,099,040 |
| minus_depth | test | 140900.0 | 0.0879 | n/a | 1,099,040 |
| minus_depth | test | 141000.0 | 0.0694 | n/a | 1,099,040 |
| minus_depth | test | 141100.0 | 0.0503 | n/a | 1,099,040 |
| minus_depth | test | 141200.0 | 0.0463 | n/a | 1,099,040 |
| minus_depth | test | 141300.0 | 0.0469 | n/a | 1,099,040 |
| minus_depth | test | 141400.0 | 0.0520 | n/a | 1,099,040 |
| minus_depth | test | 141500.0 | 0.0602 | n/a | 1,099,040 |
| minus_depth | test | 141600.0 | 0.0749 | n/a | 1,099,040 |
| minus_depth | test | 141700.0 | 0.0783 | n/a | 1,099,040 |
| minus_depth | test | 141800.0 | 0.0797 | n/a | 1,099,040 |
| minus_depth | test | 141900.0 | 0.0815 | n/a | 1,099,040 |
| minus_depth | test | 142000.0 | 0.0868 | n/a | 1,099,040 |
| minus_depth | test | 142100.0 | 0.0900 | n/a | 1,099,040 |
| minus_depth | test | 142200.0 | 0.1025 | n/a | 1,099,040 |
| minus_depth | test | 142300.0 | 0.0994 | n/a | 1,099,040 |
| minus_depth | test | 142400.0 | 0.1065 | n/a | 1,099,040 |
| minus_depth | test | 142500.0 | 0.1008 | n/a | 1,099,040 |
| minus_depth | test | 142600.0 | 0.1064 | n/a | 1,099,040 |
| minus_depth | test | 142700.0 | 0.1073 | n/a | 1,099,040 |
| minus_depth | test | 142800.0 | 0.1192 | n/a | 1,099,040 |
| minus_depth | test | 142900.0 | 0.1210 | n/a | 1,099,040 |
| minus_depth | test | 143000.0 | 0.1191 | n/a | 1,099,040 |
| minus_depth | test | 143100.0 | 0.1061 | n/a | 1,099,040 |
| minus_depth | test | 143200.0 | 0.1003 | n/a | 1,099,040 |
| minus_depth | test | 143300.0 | 0.0965 | n/a | 1,099,040 |
| minus_depth | test | 143400.0 | 0.0956 | n/a | 1,099,040 |
| minus_depth | test | 143500.0 | 0.1066 | n/a | 1,099,040 |
| minus_depth | test | 143600.0 | 0.1151 | n/a | 1,099,040 |
| minus_depth | test | 143700.0 | 0.1241 | n/a | 1,099,040 |
| minus_depth | test | 143800.0 | 0.1303 | n/a | 1,099,040 |
| minus_depth | test | 143900.0 | 0.1220 | n/a | 1,099,040 |
| minus_depth | test | 144000.0 | 0.1172 | n/a | 1,099,040 |
| minus_depth | test | 144100.0 | 0.1053 | n/a | 1,099,040 |
| minus_depth | test | 144200.0 | 0.1001 | n/a | 1,099,040 |
| minus_depth | test | 144300.0 | 0.0988 | n/a | 1,099,040 |
| minus_depth | test | 144400.0 | 0.0925 | n/a | 1,099,040 |
| minus_depth | test | 144500.0 | 0.0790 | n/a | 1,099,040 |
| minus_depth | test | 144600.0 | 0.0816 | n/a | 1,099,040 |
| minus_depth | test | 144700.0 | 0.0930 | n/a | 1,099,040 |
| minus_depth | test | 144800.0 | 0.0843 | n/a | 1,099,040 |
| minus_depth | test | 144900.0 | 0.0930 | n/a | 1,099,040 |
| minus_depth | train | 103900.0 | 0.1548 | n/a | 49,496 |
| minus_depth | train | 104000.0 | 0.1466 | n/a | 49,496 |
| minus_depth | train | 104100.0 | 0.1458 | n/a | 49,496 |
| minus_depth | train | 104200.0 | 0.1557 | n/a | 49,496 |
| minus_depth | train | 104300.0 | 0.1608 | n/a | 49,496 |
| minus_depth | train | 104400.0 | 0.1658 | n/a | 49,496 |
| minus_depth | train | 104500.0 | 0.1673 | n/a | 49,496 |
| minus_depth | train | 104600.0 | 0.1856 | n/a | 49,496 |
| minus_depth | train | 104700.0 | 0.1848 | n/a | 49,496 |
| minus_depth | train | 104800.0 | 0.1731 | n/a | 49,496 |
| minus_depth | train | 104900.0 | 0.1863 | n/a | 49,496 |
| minus_depth | train | 105000.0 | 0.1700 | n/a | 49,496 |
| minus_depth | train | 105100.0 | 0.1657 | n/a | 49,496 |
| minus_depth | train | 105200.0 | 0.1883 | n/a | 49,496 |
| minus_depth | train | 105300.0 | 0.1857 | n/a | 49,496 |
| minus_depth | train | 105400.0 | 0.1933 | n/a | 49,496 |
| minus_depth | train | 105500.0 | 0.2002 | n/a | 49,496 |
| minus_depth | train | 105600.0 | 0.2085 | n/a | 49,496 |
| minus_depth | train | 105700.0 | 0.2118 | n/a | 49,496 |
| minus_depth | train | 105800.0 | 0.2212 | n/a | 49,496 |
| minus_depth | train | 105900.0 | 0.2382 | n/a | 49,496 |
| minus_depth | train | 110000.0 | 0.2252 | n/a | 49,496 |
| minus_depth | train | 110100.0 | 0.2105 | n/a | 49,496 |
| minus_depth | train | 110200.0 | 0.2051 | n/a | 49,496 |
| minus_depth | train | 110300.0 | 0.1813 | n/a | 49,496 |
| minus_depth | train | 110400.0 | 0.1726 | n/a | 49,496 |
| minus_depth | train | 110500.0 | 0.1674 | n/a | 49,496 |
| minus_depth | train | 110600.0 | 0.1980 | n/a | 49,496 |
| minus_depth | train | 110700.0 | 0.2147 | n/a | 49,496 |
| minus_depth | train | 110800.0 | 0.2206 | n/a | 49,496 |
| minus_depth | train | 110900.0 | 0.2288 | n/a | 49,496 |
| minus_depth | train | 111000.0 | 0.2067 | n/a | 49,496 |
| minus_depth | train | 111100.0 | 0.2005 | n/a | 49,496 |
| minus_depth | train | 111200.0 | 0.2155 | n/a | 49,496 |
| minus_depth | train | 111300.0 | 0.2225 | n/a | 49,496 |
| minus_depth | train | 111400.0 | 0.2134 | n/a | 49,496 |
| minus_depth | train | 111500.0 | 0.2021 | n/a | 49,496 |
| minus_depth | train | 111600.0 | 0.2145 | n/a | 49,496 |
| minus_depth | train | 111700.0 | 0.2038 | n/a | 49,496 |
| minus_depth | train | 111800.0 | 0.2001 | n/a | 49,496 |
| minus_depth | train | 111900.0 | 0.1970 | n/a | 49,496 |
| minus_depth | train | 112000.0 | 0.1822 | n/a | 49,496 |
| minus_depth | train | 112100.0 | 0.2234 | n/a | 49,496 |
| minus_depth | train | 112200.0 | 0.2369 | n/a | 49,496 |
| minus_depth | train | 112300.0 | 0.2083 | n/a | 49,496 |
| minus_depth | train | 112400.0 | 0.2205 | n/a | 49,496 |
| minus_depth | train | 112500.0 | 0.2130 | n/a | 49,496 |
| minus_depth | train | 112600.0 | 0.2018 | n/a | 49,496 |
| minus_depth | train | 112700.0 | 0.2145 | n/a | 49,496 |
| minus_depth | train | 112800.0 | 0.1967 | n/a | 49,496 |
| minus_depth | train | 112900.0 | 0.1825 | n/a | 49,496 |
| minus_depth | train | 113000.0 | 0.2024 | n/a | 49,496 |
| minus_depth | train | 130100.0 | 0.2006 | n/a | 49,496 |
| minus_depth | train | 130200.0 | 0.1902 | n/a | 49,496 |
| minus_depth | train | 130300.0 | 0.1828 | n/a | 49,496 |
| minus_depth | train | 130400.0 | 0.1674 | n/a | 49,496 |
| minus_depth | train | 130500.0 | 0.1772 | n/a | 49,496 |
| minus_depth | train | 130600.0 | 0.1772 | n/a | 49,496 |
| minus_depth | train | 130700.0 | 0.1808 | n/a | 49,496 |
| minus_depth | train | 130800.0 | 0.2008 | n/a | 49,496 |
| minus_depth | train | 130900.0 | 0.2034 | n/a | 49,496 |
| minus_depth | train | 131000.0 | 0.2052 | n/a | 49,496 |
| minus_depth | train | 131100.0 | 0.2000 | n/a | 49,496 |
| minus_depth | train | 131200.0 | 0.2226 | n/a | 49,496 |
| minus_depth | train | 131300.0 | 0.2102 | n/a | 49,496 |
| minus_depth | train | 131400.0 | 0.2097 | n/a | 49,496 |
| minus_depth | train | 131500.0 | 0.2132 | n/a | 49,496 |
| minus_depth | train | 131600.0 | 0.2047 | n/a | 49,496 |
| minus_depth | train | 131700.0 | 0.1998 | n/a | 49,496 |
| minus_depth | train | 131800.0 | 0.1937 | n/a | 49,496 |
| minus_depth | train | 131900.0 | 0.1932 | n/a | 49,496 |
| minus_depth | train | 132000.0 | 0.1753 | n/a | 49,496 |
| minus_depth | train | 132100.0 | 0.1861 | n/a | 49,496 |
| minus_depth | train | 132200.0 | 0.1991 | n/a | 49,495 |
| minus_depth | train | 132300.0 | 0.1917 | n/a | 49,495 |
| minus_depth | train | 132400.0 | 0.2018 | n/a | 49,495 |
| minus_depth | train | 132500.0 | 0.1939 | n/a | 49,495 |
| minus_depth | train | 132600.0 | 0.2135 | n/a | 49,495 |
| minus_depth | train | 132700.0 | 0.2191 | n/a | 49,495 |
| minus_depth | train | 132800.0 | 0.2202 | n/a | 49,495 |
| minus_depth | train | 132900.0 | 0.2362 | n/a | 49,495 |
| minus_depth | train | 133000.0 | 0.2009 | n/a | 49,495 |
| minus_depth | train | 133100.0 | 0.1936 | n/a | 49,495 |
| minus_depth | train | 133200.0 | 0.1895 | n/a | 49,495 |
| minus_depth | train | 133300.0 | 0.2317 | n/a | 49,495 |
| minus_depth | train | 133400.0 | 0.2288 | n/a | 49,495 |
| minus_depth | train | 133500.0 | 0.2055 | n/a | 49,495 |
| minus_depth | train | 133600.0 | 0.2055 | n/a | 49,495 |
| minus_depth | train | 133700.0 | 0.1971 | n/a | 49,495 |
| minus_depth | train | 133800.0 | 0.1979 | n/a | 49,495 |
| minus_depth | train | 133900.0 | 0.2198 | n/a | 49,495 |
| minus_depth | train | 134000.0 | 0.1919 | n/a | 49,495 |
| minus_depth | train | 134100.0 | 0.1983 | n/a | 49,495 |
| minus_depth | train | 134200.0 | 0.2003 | n/a | 49,495 |
| minus_depth | train | 134300.0 | 0.2087 | n/a | 49,495 |
| minus_depth | train | 134400.0 | 0.2120 | n/a | 49,495 |
| minus_depth | train | 134500.0 | 0.2101 | n/a | 49,495 |
| minus_depth | train | 134600.0 | 0.1989 | n/a | 49,495 |
| minus_depth | train | 134700.0 | 0.2130 | n/a | 49,495 |
| minus_depth | train | 134800.0 | 0.2097 | n/a | 49,495 |
| minus_depth | train | 134900.0 | 0.2239 | n/a | 49,495 |
| minus_depth | train | 135000.0 | 0.2120 | n/a | 49,495 |
| minus_depth | train | 135100.0 | 0.2135 | n/a | 49,495 |
| minus_depth | train | 135200.0 | 0.2157 | n/a | 49,495 |
| minus_depth | train | 135300.0 | 0.2131 | n/a | 49,495 |
| minus_depth | train | 135400.0 | 0.2048 | n/a | 49,495 |
| minus_depth | train | 135500.0 | 0.2030 | n/a | 49,495 |
| minus_depth | train | 135600.0 | 0.2233 | n/a | 49,495 |
| minus_depth | train | 135700.0 | 0.2070 | n/a | 49,495 |
| minus_depth | train | 135800.0 | 0.2024 | n/a | 49,495 |
| minus_depth | train | 135900.0 | 0.2051 | n/a | 49,495 |
| minus_depth | train | 140000.0 | 0.1972 | n/a | 49,495 |
| minus_depth | train | 140100.0 | 0.2425 | n/a | 49,495 |
| minus_depth | train | 140200.0 | 0.2337 | n/a | 49,495 |
| minus_depth | train | 140300.0 | 0.2377 | n/a | 49,495 |
| minus_depth | train | 140400.0 | 0.2536 | n/a | 49,495 |
| minus_depth | train | 140500.0 | 0.2444 | n/a | 49,495 |
| minus_depth | train | 140600.0 | 0.2236 | n/a | 49,495 |
| minus_depth | train | 140700.0 | 0.2215 | n/a | 49,495 |
| minus_depth | train | 140800.0 | 0.2207 | n/a | 49,495 |
| minus_depth | train | 140900.0 | 0.2223 | n/a | 49,495 |
| minus_depth | train | 141000.0 | 0.2361 | n/a | 49,495 |
| minus_depth | train | 141100.0 | 0.2944 | n/a | 49,495 |
| minus_depth | train | 141200.0 | 0.3083 | n/a | 49,495 |
| minus_depth | train | 141300.0 | 0.3367 | n/a | 49,495 |
| minus_depth | train | 141400.0 | 0.3230 | n/a | 49,495 |
| minus_depth | train | 141500.0 | 0.2928 | n/a | 49,495 |
| minus_depth | train | 141600.0 | 0.2865 | n/a | 49,495 |
| minus_depth | train | 141700.0 | 0.2665 | n/a | 49,495 |
| minus_depth | train | 141800.0 | 0.2639 | n/a | 49,495 |
| minus_depth | train | 141900.0 | 0.2641 | n/a | 49,495 |
| minus_depth | train | 142000.0 | 0.2134 | n/a | 49,495 |
| minus_depth | train | 142100.0 | 0.2409 | n/a | 49,495 |
| minus_depth | train | 142200.0 | 0.2667 | n/a | 49,495 |
| minus_depth | train | 142300.0 | 0.2703 | n/a | 49,495 |
| minus_depth | train | 142400.0 | 0.2773 | n/a | 49,495 |
| minus_depth | train | 142500.0 | 0.2812 | n/a | 49,495 |
| minus_depth | train | 142600.0 | 0.2939 | n/a | 49,495 |
| minus_depth | train | 142700.0 | 0.2830 | n/a | 49,495 |
| minus_depth | train | 142800.0 | 0.2589 | n/a | 49,495 |
| minus_depth | train | 142900.0 | 0.2577 | n/a | 49,495 |
| minus_depth | train | 143000.0 | 0.2110 | n/a | 49,495 |
| minus_depth | train | 143100.0 | 0.2171 | n/a | 49,495 |
| minus_depth | train | 143200.0 | 0.2356 | n/a | 49,495 |
| minus_depth | train | 143300.0 | 0.2391 | n/a | 49,495 |
| minus_depth | train | 143400.0 | 0.2530 | n/a | 49,495 |
| minus_depth | train | 143500.0 | 0.2666 | n/a | 49,495 |
| minus_depth | train | 143600.0 | 0.2930 | n/a | 49,495 |
| minus_depth | train | 143700.0 | 0.2861 | n/a | 49,495 |
| minus_depth | train | 143800.0 | 0.2488 | n/a | 49,495 |
| minus_depth | train | 143900.0 | 0.2433 | n/a | 49,495 |
| minus_depth | train | 144000.0 | 0.2265 | n/a | 49,495 |
| minus_depth | train | 144100.0 | 0.2446 | n/a | 49,495 |
| minus_depth | train | 144200.0 | 0.2258 | n/a | 49,495 |
| minus_depth | train | 144300.0 | 0.2320 | n/a | 49,495 |
| minus_depth | train | 144400.0 | 0.2347 | n/a | 49,495 |
| minus_depth | train | 144500.0 | 0.2199 | n/a | 49,495 |
| minus_depth | train | 144600.0 | 0.2274 | n/a | 49,495 |
| minus_depth | train | 144700.0 | 0.2310 | n/a | 49,495 |
| minus_depth | train | 144800.0 | 0.2271 | n/a | 49,495 |
| minus_depth | train | 144900.0 | 0.2231 | n/a | 49,495 |
| minus_imbalance | test | 103900.0 | 0.0656 | n/a | 1,099,040 |
| minus_imbalance | test | 104000.0 | 0.0674 | n/a | 1,099,040 |
| minus_imbalance | test | 104100.0 | 0.0801 | n/a | 1,099,040 |
| minus_imbalance | test | 104200.0 | 0.0903 | n/a | 1,099,040 |
| minus_imbalance | test | 104300.0 | 0.0952 | n/a | 1,099,040 |
| minus_imbalance | test | 104400.0 | 0.0777 | n/a | 1,099,040 |
| minus_imbalance | test | 104500.0 | 0.0756 | n/a | 1,099,040 |
| minus_imbalance | test | 104600.0 | 0.0898 | n/a | 1,099,040 |
| minus_imbalance | test | 104700.0 | 0.0789 | n/a | 1,099,040 |
| minus_imbalance | test | 104800.0 | 0.0825 | n/a | 1,099,040 |
| minus_imbalance | test | 104900.0 | 0.0802 | n/a | 1,099,040 |
| minus_imbalance | test | 105000.0 | 0.0645 | n/a | 1,099,040 |
| minus_imbalance | test | 105100.0 | 0.0725 | n/a | 1,099,040 |
| minus_imbalance | test | 105200.0 | 0.0597 | n/a | 1,099,040 |
| minus_imbalance | test | 105300.0 | 0.0690 | n/a | 1,099,040 |
| minus_imbalance | test | 105400.0 | 0.0717 | n/a | 1,099,040 |
| minus_imbalance | test | 105500.0 | 0.0675 | n/a | 1,099,040 |
| minus_imbalance | test | 105600.0 | 0.0538 | n/a | 1,099,040 |
| minus_imbalance | test | 105700.0 | 0.0606 | n/a | 1,099,040 |
| minus_imbalance | test | 105800.0 | 0.0661 | n/a | 1,099,040 |
| minus_imbalance | test | 105900.0 | 0.0637 | n/a | 1,099,040 |
| minus_imbalance | test | 110000.0 | 0.0606 | n/a | 1,099,040 |
| minus_imbalance | test | 110100.0 | 0.0436 | n/a | 1,099,040 |
| minus_imbalance | test | 110200.0 | 0.0644 | n/a | 1,099,040 |
| minus_imbalance | test | 110300.0 | 0.0686 | n/a | 1,099,040 |
| minus_imbalance | test | 110400.0 | 0.0693 | n/a | 1,099,040 |
| minus_imbalance | test | 110500.0 | 0.0674 | n/a | 1,099,040 |
| minus_imbalance | test | 110600.0 | 0.0600 | n/a | 1,099,040 |
| minus_imbalance | test | 110700.0 | 0.0520 | n/a | 1,099,040 |
| minus_imbalance | test | 110800.0 | 0.0499 | n/a | 1,099,040 |
| minus_imbalance | test | 110900.0 | 0.0662 | n/a | 1,099,040 |
| minus_imbalance | test | 111000.0 | 0.0664 | n/a | 1,099,040 |
| minus_imbalance | test | 111100.0 | 0.0605 | n/a | 1,099,040 |
| minus_imbalance | test | 111200.0 | 0.0586 | n/a | 1,099,040 |
| minus_imbalance | test | 111300.0 | 0.0611 | n/a | 1,099,040 |
| minus_imbalance | test | 111400.0 | 0.0687 | n/a | 1,099,040 |
| minus_imbalance | test | 111500.0 | 0.0761 | n/a | 1,099,040 |
| minus_imbalance | test | 111600.0 | 0.0799 | n/a | 1,099,040 |
| minus_imbalance | test | 111700.0 | 0.0843 | n/a | 1,099,040 |
| minus_imbalance | test | 111800.0 | 0.0785 | n/a | 1,099,040 |
| minus_imbalance | test | 111900.0 | 0.0776 | n/a | 1,099,040 |
| minus_imbalance | test | 112000.0 | 0.0624 | n/a | 1,099,040 |
| minus_imbalance | test | 112100.0 | 0.0529 | n/a | 1,099,040 |
| minus_imbalance | test | 112200.0 | 0.0368 | n/a | 1,099,040 |
| minus_imbalance | test | 112300.0 | 0.0343 | n/a | 1,099,040 |
| minus_imbalance | test | 112400.0 | 0.0334 | n/a | 1,099,040 |
| minus_imbalance | test | 112500.0 | 0.0457 | n/a | 1,099,040 |
| minus_imbalance | test | 112600.0 | 0.0478 | n/a | 1,099,040 |
| minus_imbalance | test | 112700.0 | 0.0507 | n/a | 1,099,040 |
| minus_imbalance | test | 112800.0 | 0.0383 | n/a | 1,099,040 |
| minus_imbalance | test | 112900.0 | 0.0295 | n/a | 1,099,040 |
| minus_imbalance | test | 113000.0 | 0.0794 | n/a | 1,099,040 |
| minus_imbalance | test | 130100.0 | 0.0755 | n/a | 1,099,040 |
| minus_imbalance | test | 130200.0 | 0.0684 | n/a | 1,099,040 |
| minus_imbalance | test | 130300.0 | 0.0789 | n/a | 1,099,040 |
| minus_imbalance | test | 130400.0 | 0.0769 | n/a | 1,099,040 |
| minus_imbalance | test | 130500.0 | 0.0676 | n/a | 1,099,040 |
| minus_imbalance | test | 130600.0 | 0.0617 | n/a | 1,099,040 |
| minus_imbalance | test | 130700.0 | 0.0658 | n/a | 1,099,040 |
| minus_imbalance | test | 130800.0 | 0.0719 | n/a | 1,099,040 |
| minus_imbalance | test | 130900.0 | 0.0742 | n/a | 1,099,040 |
| minus_imbalance | test | 131000.0 | 0.0635 | n/a | 1,099,040 |
| minus_imbalance | test | 131100.0 | 0.0612 | n/a | 1,099,040 |
| minus_imbalance | test | 131200.0 | 0.0766 | n/a | 1,099,040 |
| minus_imbalance | test | 131300.0 | 0.0731 | n/a | 1,099,040 |
| minus_imbalance | test | 131400.0 | 0.0733 | n/a | 1,099,040 |
| minus_imbalance | test | 131500.0 | 0.0865 | n/a | 1,099,040 |
| minus_imbalance | test | 131600.0 | 0.0894 | n/a | 1,099,040 |
| minus_imbalance | test | 131700.0 | 0.0945 | n/a | 1,099,040 |
| minus_imbalance | test | 131800.0 | 0.0787 | n/a | 1,099,040 |
| minus_imbalance | test | 131900.0 | 0.0791 | n/a | 1,099,040 |
| minus_imbalance | test | 132000.0 | 0.0733 | n/a | 1,099,040 |
| minus_imbalance | test | 132100.0 | 0.0693 | n/a | 1,099,040 |
| minus_imbalance | test | 132200.0 | 0.0624 | n/a | 1,099,040 |
| minus_imbalance | test | 132300.0 | 0.0590 | n/a | 1,099,040 |
| minus_imbalance | test | 132400.0 | 0.0513 | n/a | 1,099,040 |
| minus_imbalance | test | 132500.0 | 0.0598 | n/a | 1,099,040 |
| minus_imbalance | test | 132600.0 | 0.0689 | n/a | 1,099,040 |
| minus_imbalance | test | 132700.0 | 0.0757 | n/a | 1,099,040 |
| minus_imbalance | test | 132800.0 | 0.0771 | n/a | 1,099,040 |
| minus_imbalance | test | 132900.0 | 0.0844 | n/a | 1,099,040 |
| minus_imbalance | test | 133000.0 | 0.0665 | n/a | 1,099,040 |
| minus_imbalance | test | 133100.0 | 0.0617 | n/a | 1,099,040 |
| minus_imbalance | test | 133200.0 | 0.0783 | n/a | 1,099,040 |
| minus_imbalance | test | 133300.0 | 0.0823 | n/a | 1,099,040 |
| minus_imbalance | test | 133400.0 | 0.0858 | n/a | 1,099,040 |
| minus_imbalance | test | 133500.0 | 0.0768 | n/a | 1,099,040 |
| minus_imbalance | test | 133600.0 | 0.0834 | n/a | 1,099,040 |
| minus_imbalance | test | 133700.0 | 0.0995 | n/a | 1,099,040 |
| minus_imbalance | test | 133800.0 | 0.0939 | n/a | 1,099,040 |
| minus_imbalance | test | 133900.0 | 0.0934 | n/a | 1,099,040 |
| minus_imbalance | test | 134000.0 | 0.0723 | n/a | 1,099,040 |
| minus_imbalance | test | 134100.0 | 0.0616 | n/a | 1,099,040 |
| minus_imbalance | test | 134200.0 | 0.0818 | n/a | 1,099,040 |
| minus_imbalance | test | 134300.0 | 0.0853 | n/a | 1,099,040 |
| minus_imbalance | test | 134400.0 | 0.0820 | n/a | 1,099,040 |
| minus_imbalance | test | 134500.0 | 0.0675 | n/a | 1,099,040 |
| minus_imbalance | test | 134600.0 | 0.0816 | n/a | 1,099,040 |
| minus_imbalance | test | 134700.0 | 0.0789 | n/a | 1,099,040 |
| minus_imbalance | test | 134800.0 | 0.0873 | n/a | 1,099,040 |
| minus_imbalance | test | 134900.0 | 0.0931 | n/a | 1,099,040 |
| minus_imbalance | test | 135000.0 | 0.0937 | n/a | 1,099,040 |
| minus_imbalance | test | 135100.0 | 0.0960 | n/a | 1,099,040 |
| minus_imbalance | test | 135200.0 | 0.0981 | n/a | 1,099,040 |
| minus_imbalance | test | 135300.0 | 0.1050 | n/a | 1,099,040 |
| minus_imbalance | test | 135400.0 | 0.1018 | n/a | 1,099,040 |
| minus_imbalance | test | 135500.0 | 0.1101 | n/a | 1,099,040 |
| minus_imbalance | test | 135600.0 | 0.1029 | n/a | 1,099,040 |
| minus_imbalance | test | 135700.0 | 0.1138 | n/a | 1,099,040 |
| minus_imbalance | test | 135800.0 | 0.1218 | n/a | 1,099,040 |
| minus_imbalance | test | 135900.0 | 0.1228 | n/a | 1,099,040 |
| minus_imbalance | test | 140000.0 | 0.1036 | n/a | 1,099,040 |
| minus_imbalance | test | 140100.0 | 0.1107 | n/a | 1,099,040 |
| minus_imbalance | test | 140200.0 | 0.1175 | n/a | 1,099,040 |
| minus_imbalance | test | 140300.0 | 0.1118 | n/a | 1,099,040 |
| minus_imbalance | test | 140400.0 | 0.1124 | n/a | 1,099,040 |
| minus_imbalance | test | 140500.0 | 0.1022 | n/a | 1,099,040 |
| minus_imbalance | test | 140600.0 | 0.1113 | n/a | 1,099,040 |
| minus_imbalance | test | 140700.0 | 0.1100 | n/a | 1,099,040 |
| minus_imbalance | test | 140800.0 | 0.0994 | n/a | 1,099,040 |
| minus_imbalance | test | 140900.0 | 0.0988 | n/a | 1,099,040 |
| minus_imbalance | test | 141000.0 | 0.0769 | n/a | 1,099,040 |
| minus_imbalance | test | 141100.0 | 0.0633 | n/a | 1,099,040 |
| minus_imbalance | test | 141200.0 | 0.0582 | n/a | 1,099,040 |
| minus_imbalance | test | 141300.0 | 0.0546 | n/a | 1,099,040 |
| minus_imbalance | test | 141400.0 | 0.0642 | n/a | 1,099,040 |
| minus_imbalance | test | 141500.0 | 0.0661 | n/a | 1,099,040 |
| minus_imbalance | test | 141600.0 | 0.0774 | n/a | 1,099,040 |
| minus_imbalance | test | 141700.0 | 0.0814 | n/a | 1,099,040 |
| minus_imbalance | test | 141800.0 | 0.0764 | n/a | 1,099,040 |
| minus_imbalance | test | 141900.0 | 0.0792 | n/a | 1,099,040 |
| minus_imbalance | test | 142000.0 | 0.0896 | n/a | 1,099,040 |
| minus_imbalance | test | 142100.0 | 0.0984 | n/a | 1,099,040 |
| minus_imbalance | test | 142200.0 | 0.1163 | n/a | 1,099,040 |
| minus_imbalance | test | 142300.0 | 0.1152 | n/a | 1,099,040 |
| minus_imbalance | test | 142400.0 | 0.1170 | n/a | 1,099,040 |
| minus_imbalance | test | 142500.0 | 0.1079 | n/a | 1,099,040 |
| minus_imbalance | test | 142600.0 | 0.1060 | n/a | 1,099,040 |
| minus_imbalance | test | 142700.0 | 0.1108 | n/a | 1,099,040 |
| minus_imbalance | test | 142800.0 | 0.1193 | n/a | 1,099,040 |
| minus_imbalance | test | 142900.0 | 0.1207 | n/a | 1,099,040 |
| minus_imbalance | test | 143000.0 | 0.1135 | n/a | 1,099,040 |
| minus_imbalance | test | 143100.0 | 0.1105 | n/a | 1,099,040 |
| minus_imbalance | test | 143200.0 | 0.1105 | n/a | 1,099,040 |
| minus_imbalance | test | 143300.0 | 0.1092 | n/a | 1,099,040 |
| minus_imbalance | test | 143400.0 | 0.1117 | n/a | 1,099,040 |
| minus_imbalance | test | 143500.0 | 0.1313 | n/a | 1,099,040 |
| minus_imbalance | test | 143600.0 | 0.1326 | n/a | 1,099,040 |
| minus_imbalance | test | 143700.0 | 0.1445 | n/a | 1,099,040 |
| minus_imbalance | test | 143800.0 | 0.1575 | n/a | 1,099,040 |
| minus_imbalance | test | 143900.0 | 0.1440 | n/a | 1,099,040 |
| minus_imbalance | test | 144000.0 | 0.1318 | n/a | 1,099,040 |
| minus_imbalance | test | 144100.0 | 0.1197 | n/a | 1,099,040 |
| minus_imbalance | test | 144200.0 | 0.1163 | n/a | 1,099,040 |
| minus_imbalance | test | 144300.0 | 0.1158 | n/a | 1,099,040 |
| minus_imbalance | test | 144400.0 | 0.1050 | n/a | 1,099,040 |
| minus_imbalance | test | 144500.0 | 0.0973 | n/a | 1,099,040 |
| minus_imbalance | test | 144600.0 | 0.0985 | n/a | 1,099,040 |
| minus_imbalance | test | 144700.0 | 0.1068 | n/a | 1,099,040 |
| minus_imbalance | test | 144800.0 | 0.1024 | n/a | 1,099,040 |
| minus_imbalance | test | 144900.0 | 0.1090 | n/a | 1,099,040 |
| minus_imbalance | train | 103900.0 | 0.1422 | n/a | 49,496 |
| minus_imbalance | train | 104000.0 | 0.1306 | n/a | 49,496 |
| minus_imbalance | train | 104100.0 | 0.1247 | n/a | 49,496 |
| minus_imbalance | train | 104200.0 | 0.1237 | n/a | 49,496 |
| minus_imbalance | train | 104300.0 | 0.1217 | n/a | 49,496 |
| minus_imbalance | train | 104400.0 | 0.1309 | n/a | 49,496 |
| minus_imbalance | train | 104500.0 | 0.1429 | n/a | 49,496 |
| minus_imbalance | train | 104600.0 | 0.1453 | n/a | 49,496 |
| minus_imbalance | train | 104700.0 | 0.1574 | n/a | 49,496 |
| minus_imbalance | train | 104800.0 | 0.1478 | n/a | 49,496 |
| minus_imbalance | train | 104900.0 | 0.1702 | n/a | 49,496 |
| minus_imbalance | train | 105000.0 | 0.1589 | n/a | 49,496 |
| minus_imbalance | train | 105100.0 | 0.1597 | n/a | 49,496 |
| minus_imbalance | train | 105200.0 | 0.1743 | n/a | 49,496 |
| minus_imbalance | train | 105300.0 | 0.1638 | n/a | 49,496 |
| minus_imbalance | train | 105400.0 | 0.1659 | n/a | 49,496 |
| minus_imbalance | train | 105500.0 | 0.1805 | n/a | 49,496 |
| minus_imbalance | train | 105600.0 | 0.1922 | n/a | 49,496 |
| minus_imbalance | train | 105700.0 | 0.1900 | n/a | 49,496 |
| minus_imbalance | train | 105800.0 | 0.1950 | n/a | 49,496 |
| minus_imbalance | train | 105900.0 | 0.2054 | n/a | 49,496 |
| minus_imbalance | train | 110000.0 | 0.1689 | n/a | 49,496 |
| minus_imbalance | train | 110100.0 | 0.1586 | n/a | 49,496 |
| minus_imbalance | train | 110200.0 | 0.1456 | n/a | 49,496 |
| minus_imbalance | train | 110300.0 | 0.1349 | n/a | 49,496 |
| minus_imbalance | train | 110400.0 | 0.1470 | n/a | 49,496 |
| minus_imbalance | train | 110500.0 | 0.1329 | n/a | 49,496 |
| minus_imbalance | train | 110600.0 | 0.1539 | n/a | 49,496 |
| minus_imbalance | train | 110700.0 | 0.1695 | n/a | 49,496 |
| minus_imbalance | train | 110800.0 | 0.1724 | n/a | 49,496 |
| minus_imbalance | train | 110900.0 | 0.1967 | n/a | 49,496 |
| minus_imbalance | train | 111000.0 | 0.1750 | n/a | 49,496 |
| minus_imbalance | train | 111100.0 | 0.1813 | n/a | 49,496 |
| minus_imbalance | train | 111200.0 | 0.1961 | n/a | 49,496 |
| minus_imbalance | train | 111300.0 | 0.2009 | n/a | 49,496 |
| minus_imbalance | train | 111400.0 | 0.1975 | n/a | 49,496 |
| minus_imbalance | train | 111500.0 | 0.1778 | n/a | 49,496 |
| minus_imbalance | train | 111600.0 | 0.1758 | n/a | 49,496 |
| minus_imbalance | train | 111700.0 | 0.1715 | n/a | 49,496 |
| minus_imbalance | train | 111800.0 | 0.1708 | n/a | 49,496 |
| minus_imbalance | train | 111900.0 | 0.1604 | n/a | 49,496 |
| minus_imbalance | train | 112000.0 | 0.1448 | n/a | 49,496 |
| minus_imbalance | train | 112100.0 | 0.1544 | n/a | 49,496 |
| minus_imbalance | train | 112200.0 | 0.1557 | n/a | 49,496 |
| minus_imbalance | train | 112300.0 | 0.1412 | n/a | 49,496 |
| minus_imbalance | train | 112400.0 | 0.1456 | n/a | 49,496 |
| minus_imbalance | train | 112500.0 | 0.1328 | n/a | 49,496 |
| minus_imbalance | train | 112600.0 | 0.1318 | n/a | 49,496 |
| minus_imbalance | train | 112700.0 | 0.1332 | n/a | 49,496 |
| minus_imbalance | train | 112800.0 | 0.1276 | n/a | 49,496 |
| minus_imbalance | train | 112900.0 | 0.1162 | n/a | 49,496 |
| minus_imbalance | train | 113000.0 | 0.1624 | n/a | 49,496 |
| minus_imbalance | train | 130100.0 | 0.1588 | n/a | 49,496 |
| minus_imbalance | train | 130200.0 | 0.1492 | n/a | 49,496 |
| minus_imbalance | train | 130300.0 | 0.1410 | n/a | 49,496 |
| minus_imbalance | train | 130400.0 | 0.1260 | n/a | 49,496 |
| minus_imbalance | train | 130500.0 | 0.1461 | n/a | 49,496 |
| minus_imbalance | train | 130600.0 | 0.1421 | n/a | 49,496 |
| minus_imbalance | train | 130700.0 | 0.1452 | n/a | 49,496 |
| minus_imbalance | train | 130800.0 | 0.1536 | n/a | 49,496 |
| minus_imbalance | train | 130900.0 | 0.1485 | n/a | 49,496 |
| minus_imbalance | train | 131000.0 | 0.1548 | n/a | 49,496 |
| minus_imbalance | train | 131100.0 | 0.1510 | n/a | 49,496 |
| minus_imbalance | train | 131200.0 | 0.1622 | n/a | 49,496 |
| minus_imbalance | train | 131300.0 | 0.1718 | n/a | 49,496 |
| minus_imbalance | train | 131400.0 | 0.1739 | n/a | 49,496 |
| minus_imbalance | train | 131500.0 | 0.1639 | n/a | 49,496 |
| minus_imbalance | train | 131600.0 | 0.1540 | n/a | 49,496 |
| minus_imbalance | train | 131700.0 | 0.1621 | n/a | 49,496 |
| minus_imbalance | train | 131800.0 | 0.1475 | n/a | 49,496 |
| minus_imbalance | train | 131900.0 | 0.1394 | n/a | 49,496 |
| minus_imbalance | train | 132000.0 | 0.1234 | n/a | 49,496 |
| minus_imbalance | train | 132100.0 | 0.1290 | n/a | 49,496 |
| minus_imbalance | train | 132200.0 | 0.1515 | n/a | 49,495 |
| minus_imbalance | train | 132300.0 | 0.1574 | n/a | 49,495 |
| minus_imbalance | train | 132400.0 | 0.1606 | n/a | 49,495 |
| minus_imbalance | train | 132500.0 | 0.1491 | n/a | 49,495 |
| minus_imbalance | train | 132600.0 | 0.1727 | n/a | 49,495 |
| minus_imbalance | train | 132700.0 | 0.1741 | n/a | 49,495 |
| minus_imbalance | train | 132800.0 | 0.1773 | n/a | 49,495 |
| minus_imbalance | train | 132900.0 | 0.1838 | n/a | 49,495 |
| minus_imbalance | train | 133000.0 | 0.1644 | n/a | 49,495 |
| minus_imbalance | train | 133100.0 | 0.1543 | n/a | 49,495 |
| minus_imbalance | train | 133200.0 | 0.1475 | n/a | 49,495 |
| minus_imbalance | train | 133300.0 | 0.1888 | n/a | 49,495 |
| minus_imbalance | train | 133400.0 | 0.1725 | n/a | 49,495 |
| minus_imbalance | train | 133500.0 | 0.1525 | n/a | 49,495 |
| minus_imbalance | train | 133600.0 | 0.1496 | n/a | 49,495 |
| minus_imbalance | train | 133700.0 | 0.1517 | n/a | 49,495 |
| minus_imbalance | train | 133800.0 | 0.1652 | n/a | 49,495 |
| minus_imbalance | train | 133900.0 | 0.1851 | n/a | 49,495 |
| minus_imbalance | train | 134000.0 | 0.1549 | n/a | 49,495 |
| minus_imbalance | train | 134100.0 | 0.1564 | n/a | 49,495 |
| minus_imbalance | train | 134200.0 | 0.1686 | n/a | 49,495 |
| minus_imbalance | train | 134300.0 | 0.1664 | n/a | 49,495 |
| minus_imbalance | train | 134400.0 | 0.1664 | n/a | 49,495 |
| minus_imbalance | train | 134500.0 | 0.1781 | n/a | 49,495 |
| minus_imbalance | train | 134600.0 | 0.1748 | n/a | 49,495 |
| minus_imbalance | train | 134700.0 | 0.1586 | n/a | 49,495 |
| minus_imbalance | train | 134800.0 | 0.1579 | n/a | 49,495 |
| minus_imbalance | train | 134900.0 | 0.1733 | n/a | 49,495 |
| minus_imbalance | train | 135000.0 | 0.1591 | n/a | 49,495 |
| minus_imbalance | train | 135100.0 | 0.1805 | n/a | 49,495 |
| minus_imbalance | train | 135200.0 | 0.1906 | n/a | 49,495 |
| minus_imbalance | train | 135300.0 | 0.1852 | n/a | 49,495 |
| minus_imbalance | train | 135400.0 | 0.1660 | n/a | 49,495 |
| minus_imbalance | train | 135500.0 | 0.1485 | n/a | 49,495 |
| minus_imbalance | train | 135600.0 | 0.1707 | n/a | 49,495 |
| minus_imbalance | train | 135700.0 | 0.1509 | n/a | 49,495 |
| minus_imbalance | train | 135800.0 | 0.1412 | n/a | 49,495 |
| minus_imbalance | train | 135900.0 | 0.1424 | n/a | 49,495 |
| minus_imbalance | train | 140000.0 | 0.1172 | n/a | 49,495 |
| minus_imbalance | train | 140100.0 | 0.1523 | n/a | 49,495 |
| minus_imbalance | train | 140200.0 | 0.1555 | n/a | 49,495 |
| minus_imbalance | train | 140300.0 | 0.1595 | n/a | 49,495 |
| minus_imbalance | train | 140400.0 | 0.1815 | n/a | 49,495 |
| minus_imbalance | train | 140500.0 | 0.1743 | n/a | 49,495 |
| minus_imbalance | train | 140600.0 | 0.1576 | n/a | 49,495 |
| minus_imbalance | train | 140700.0 | 0.1736 | n/a | 49,495 |
| minus_imbalance | train | 140800.0 | 0.1711 | n/a | 49,495 |
| minus_imbalance | train | 140900.0 | 0.1752 | n/a | 49,495 |
| minus_imbalance | train | 141000.0 | 0.1881 | n/a | 49,495 |
| minus_imbalance | train | 141100.0 | 0.2190 | n/a | 49,495 |
| minus_imbalance | train | 141200.0 | 0.2367 | n/a | 49,495 |
| minus_imbalance | train | 141300.0 | 0.2701 | n/a | 49,495 |
| minus_imbalance | train | 141400.0 | 0.2737 | n/a | 49,495 |
| minus_imbalance | train | 141500.0 | 0.2538 | n/a | 49,495 |
| minus_imbalance | train | 141600.0 | 0.2359 | n/a | 49,495 |
| minus_imbalance | train | 141700.0 | 0.2155 | n/a | 49,495 |
| minus_imbalance | train | 141800.0 | 0.2060 | n/a | 49,495 |
| minus_imbalance | train | 141900.0 | 0.1962 | n/a | 49,495 |
| minus_imbalance | train | 142000.0 | 0.1696 | n/a | 49,495 |
| minus_imbalance | train | 142100.0 | 0.1797 | n/a | 49,495 |
| minus_imbalance | train | 142200.0 | 0.1877 | n/a | 49,495 |
| minus_imbalance | train | 142300.0 | 0.1887 | n/a | 49,495 |
| minus_imbalance | train | 142400.0 | 0.1833 | n/a | 49,495 |
| minus_imbalance | train | 142500.0 | 0.1815 | n/a | 49,495 |
| minus_imbalance | train | 142600.0 | 0.2006 | n/a | 49,495 |
| minus_imbalance | train | 142700.0 | 0.1941 | n/a | 49,495 |
| minus_imbalance | train | 142800.0 | 0.1696 | n/a | 49,495 |
| minus_imbalance | train | 142900.0 | 0.1720 | n/a | 49,495 |
| minus_imbalance | train | 143000.0 | 0.1404 | n/a | 49,495 |
| minus_imbalance | train | 143100.0 | 0.1633 | n/a | 49,495 |
| minus_imbalance | train | 143200.0 | 0.1899 | n/a | 49,495 |
| minus_imbalance | train | 143300.0 | 0.2038 | n/a | 49,495 |
| minus_imbalance | train | 143400.0 | 0.2216 | n/a | 49,495 |
| minus_imbalance | train | 143500.0 | 0.2417 | n/a | 49,495 |
| minus_imbalance | train | 143600.0 | 0.2508 | n/a | 49,495 |
| minus_imbalance | train | 143700.0 | 0.2495 | n/a | 49,495 |
| minus_imbalance | train | 143800.0 | 0.2105 | n/a | 49,495 |
| minus_imbalance | train | 143900.0 | 0.2067 | n/a | 49,495 |
| minus_imbalance | train | 144000.0 | 0.1956 | n/a | 49,495 |
| minus_imbalance | train | 144100.0 | 0.1858 | n/a | 49,495 |
| minus_imbalance | train | 144200.0 | 0.1640 | n/a | 49,495 |
| minus_imbalance | train | 144300.0 | 0.1589 | n/a | 49,495 |
| minus_imbalance | train | 144400.0 | 0.1649 | n/a | 49,495 |
| minus_imbalance | train | 144500.0 | 0.1517 | n/a | 49,495 |
| minus_imbalance | train | 144600.0 | 0.1606 | n/a | 49,495 |
| minus_imbalance | train | 144700.0 | 0.1672 | n/a | 49,495 |
| minus_imbalance | train | 144800.0 | 0.1739 | n/a | 49,495 |
| minus_imbalance | train | 144900.0 | 0.1835 | n/a | 49,495 |
| minus_quality | test | 103900.0 | 0.0712 | n/a | 1,099,040 |
| minus_quality | test | 104000.0 | 0.0752 | n/a | 1,099,040 |
| minus_quality | test | 104100.0 | 0.0860 | n/a | 1,099,040 |
| minus_quality | test | 104200.0 | 0.0944 | n/a | 1,099,040 |
| minus_quality | test | 104300.0 | 0.0954 | n/a | 1,099,040 |
| minus_quality | test | 104400.0 | 0.0807 | n/a | 1,099,040 |
| minus_quality | test | 104500.0 | 0.0798 | n/a | 1,099,040 |
| minus_quality | test | 104600.0 | 0.0913 | n/a | 1,099,040 |
| minus_quality | test | 104700.0 | 0.0845 | n/a | 1,099,040 |
| minus_quality | test | 104800.0 | 0.0891 | n/a | 1,099,040 |
| minus_quality | test | 104900.0 | 0.0844 | n/a | 1,099,040 |
| minus_quality | test | 105000.0 | 0.0696 | n/a | 1,099,040 |
| minus_quality | test | 105100.0 | 0.0756 | n/a | 1,099,040 |
| minus_quality | test | 105200.0 | 0.0675 | n/a | 1,099,040 |
| minus_quality | test | 105300.0 | 0.0707 | n/a | 1,099,040 |
| minus_quality | test | 105400.0 | 0.0721 | n/a | 1,099,040 |
| minus_quality | test | 105500.0 | 0.0623 | n/a | 1,099,040 |
| minus_quality | test | 105600.0 | 0.0518 | n/a | 1,099,040 |
| minus_quality | test | 105700.0 | 0.0497 | n/a | 1,099,040 |
| minus_quality | test | 105800.0 | 0.0571 | n/a | 1,099,040 |
| minus_quality | test | 105900.0 | 0.0554 | n/a | 1,099,040 |
| minus_quality | test | 110000.0 | 0.0553 | n/a | 1,099,040 |
| minus_quality | test | 110100.0 | 0.0466 | n/a | 1,099,040 |
| minus_quality | test | 110200.0 | 0.0626 | n/a | 1,099,040 |
| minus_quality | test | 110300.0 | 0.0667 | n/a | 1,099,040 |
| minus_quality | test | 110400.0 | 0.0687 | n/a | 1,099,040 |
| minus_quality | test | 110500.0 | 0.0690 | n/a | 1,099,040 |
| minus_quality | test | 110600.0 | 0.0639 | n/a | 1,099,040 |
| minus_quality | test | 110700.0 | 0.0569 | n/a | 1,099,040 |
| minus_quality | test | 110800.0 | 0.0534 | n/a | 1,099,040 |
| minus_quality | test | 110900.0 | 0.0713 | n/a | 1,099,040 |
| minus_quality | test | 111000.0 | 0.0717 | n/a | 1,099,040 |
| minus_quality | test | 111100.0 | 0.0667 | n/a | 1,099,040 |
| minus_quality | test | 111200.0 | 0.0712 | n/a | 1,099,040 |
| minus_quality | test | 111300.0 | 0.0735 | n/a | 1,099,040 |
| minus_quality | test | 111400.0 | 0.0798 | n/a | 1,099,040 |
| minus_quality | test | 111500.0 | 0.0875 | n/a | 1,099,040 |
| minus_quality | test | 111600.0 | 0.0855 | n/a | 1,099,040 |
| minus_quality | test | 111700.0 | 0.0844 | n/a | 1,099,040 |
| minus_quality | test | 111800.0 | 0.0849 | n/a | 1,099,040 |
| minus_quality | test | 111900.0 | 0.0857 | n/a | 1,099,040 |
| minus_quality | test | 112000.0 | 0.0707 | n/a | 1,099,040 |
| minus_quality | test | 112100.0 | 0.0629 | n/a | 1,099,040 |
| minus_quality | test | 112200.0 | 0.0464 | n/a | 1,099,040 |
| minus_quality | test | 112300.0 | 0.0463 | n/a | 1,099,040 |
| minus_quality | test | 112400.0 | 0.0405 | n/a | 1,099,040 |
| minus_quality | test | 112500.0 | 0.0509 | n/a | 1,099,040 |
| minus_quality | test | 112600.0 | 0.0559 | n/a | 1,099,040 |
| minus_quality | test | 112700.0 | 0.0613 | n/a | 1,099,040 |
| minus_quality | test | 112800.0 | 0.0491 | n/a | 1,099,040 |
| minus_quality | test | 112900.0 | 0.0399 | n/a | 1,099,040 |
| minus_quality | test | 113000.0 | 0.0827 | n/a | 1,099,040 |
| minus_quality | test | 130100.0 | 0.0736 | n/a | 1,099,040 |
| minus_quality | test | 130200.0 | 0.0723 | n/a | 1,099,040 |
| minus_quality | test | 130300.0 | 0.0814 | n/a | 1,099,040 |
| minus_quality | test | 130400.0 | 0.0773 | n/a | 1,099,040 |
| minus_quality | test | 130500.0 | 0.0675 | n/a | 1,099,040 |
| minus_quality | test | 130600.0 | 0.0542 | n/a | 1,099,040 |
| minus_quality | test | 130700.0 | 0.0537 | n/a | 1,099,040 |
| minus_quality | test | 130800.0 | 0.0585 | n/a | 1,099,040 |
| minus_quality | test | 130900.0 | 0.0596 | n/a | 1,099,040 |
| minus_quality | test | 131000.0 | 0.0561 | n/a | 1,099,040 |
| minus_quality | test | 131100.0 | 0.0607 | n/a | 1,099,040 |
| minus_quality | test | 131200.0 | 0.0791 | n/a | 1,099,040 |
| minus_quality | test | 131300.0 | 0.0779 | n/a | 1,099,040 |
| minus_quality | test | 131400.0 | 0.0775 | n/a | 1,099,040 |
| minus_quality | test | 131500.0 | 0.0844 | n/a | 1,099,040 |
| minus_quality | test | 131600.0 | 0.0976 | n/a | 1,099,040 |
| minus_quality | test | 131700.0 | 0.0934 | n/a | 1,099,040 |
| minus_quality | test | 131800.0 | 0.0788 | n/a | 1,099,040 |
| minus_quality | test | 131900.0 | 0.0865 | n/a | 1,099,040 |
| minus_quality | test | 132000.0 | 0.0810 | n/a | 1,099,040 |
| minus_quality | test | 132100.0 | 0.0754 | n/a | 1,099,040 |
| minus_quality | test | 132200.0 | 0.0736 | n/a | 1,099,040 |
| minus_quality | test | 132300.0 | 0.0732 | n/a | 1,099,040 |
| minus_quality | test | 132400.0 | 0.0610 | n/a | 1,099,040 |
| minus_quality | test | 132500.0 | 0.0685 | n/a | 1,099,040 |
| minus_quality | test | 132600.0 | 0.0768 | n/a | 1,099,040 |
| minus_quality | test | 132700.0 | 0.0872 | n/a | 1,099,040 |
| minus_quality | test | 132800.0 | 0.0817 | n/a | 1,099,040 |
| minus_quality | test | 132900.0 | 0.0905 | n/a | 1,099,040 |
| minus_quality | test | 133000.0 | 0.0720 | n/a | 1,099,040 |
| minus_quality | test | 133100.0 | 0.0658 | n/a | 1,099,040 |
| minus_quality | test | 133200.0 | 0.0841 | n/a | 1,099,040 |
| minus_quality | test | 133300.0 | 0.0911 | n/a | 1,099,040 |
| minus_quality | test | 133400.0 | 0.0976 | n/a | 1,099,040 |
| minus_quality | test | 133500.0 | 0.0921 | n/a | 1,099,040 |
| minus_quality | test | 133600.0 | 0.0985 | n/a | 1,099,040 |
| minus_quality | test | 133700.0 | 0.1145 | n/a | 1,099,040 |
| minus_quality | test | 133800.0 | 0.1095 | n/a | 1,099,040 |
| minus_quality | test | 133900.0 | 0.1011 | n/a | 1,099,040 |
| minus_quality | test | 134000.0 | 0.0822 | n/a | 1,099,040 |
| minus_quality | test | 134100.0 | 0.0697 | n/a | 1,099,040 |
| minus_quality | test | 134200.0 | 0.0851 | n/a | 1,099,040 |
| minus_quality | test | 134300.0 | 0.0921 | n/a | 1,099,040 |
| minus_quality | test | 134400.0 | 0.0901 | n/a | 1,099,040 |
| minus_quality | test | 134500.0 | 0.0714 | n/a | 1,099,040 |
| minus_quality | test | 134600.0 | 0.0798 | n/a | 1,099,040 |
| minus_quality | test | 134700.0 | 0.0804 | n/a | 1,099,040 |
| minus_quality | test | 134800.0 | 0.0925 | n/a | 1,099,040 |
| minus_quality | test | 134900.0 | 0.0964 | n/a | 1,099,040 |
| minus_quality | test | 135000.0 | 0.0957 | n/a | 1,099,040 |
| minus_quality | test | 135100.0 | 0.0974 | n/a | 1,099,040 |
| minus_quality | test | 135200.0 | 0.0937 | n/a | 1,099,040 |
| minus_quality | test | 135300.0 | 0.0974 | n/a | 1,099,040 |
| minus_quality | test | 135400.0 | 0.0969 | n/a | 1,099,040 |
| minus_quality | test | 135500.0 | 0.1049 | n/a | 1,099,040 |
| minus_quality | test | 135600.0 | 0.1036 | n/a | 1,099,040 |
| minus_quality | test | 135700.0 | 0.1184 | n/a | 1,099,040 |
| minus_quality | test | 135800.0 | 0.1287 | n/a | 1,099,040 |
| minus_quality | test | 135900.0 | 0.1218 | n/a | 1,099,040 |
| minus_quality | test | 140000.0 | 0.0984 | n/a | 1,099,040 |
| minus_quality | test | 140100.0 | 0.0992 | n/a | 1,099,040 |
| minus_quality | test | 140200.0 | 0.1077 | n/a | 1,099,040 |
| minus_quality | test | 140300.0 | 0.1085 | n/a | 1,099,040 |
| minus_quality | test | 140400.0 | 0.1154 | n/a | 1,099,040 |
| minus_quality | test | 140500.0 | 0.1038 | n/a | 1,099,040 |
| minus_quality | test | 140600.0 | 0.1125 | n/a | 1,099,040 |
| minus_quality | test | 140700.0 | 0.1160 | n/a | 1,099,040 |
| minus_quality | test | 140800.0 | 0.0987 | n/a | 1,099,040 |
| minus_quality | test | 140900.0 | 0.1009 | n/a | 1,099,040 |
| minus_quality | test | 141000.0 | 0.0815 | n/a | 1,099,040 |
| minus_quality | test | 141100.0 | 0.0676 | n/a | 1,099,040 |
| minus_quality | test | 141200.0 | 0.0641 | n/a | 1,099,040 |
| minus_quality | test | 141300.0 | 0.0591 | n/a | 1,099,040 |
| minus_quality | test | 141400.0 | 0.0659 | n/a | 1,099,040 |
| minus_quality | test | 141500.0 | 0.0701 | n/a | 1,099,040 |
| minus_quality | test | 141600.0 | 0.0752 | n/a | 1,099,040 |
| minus_quality | test | 141700.0 | 0.0779 | n/a | 1,099,040 |
| minus_quality | test | 141800.0 | 0.0711 | n/a | 1,099,040 |
| minus_quality | test | 141900.0 | 0.0830 | n/a | 1,099,040 |
| minus_quality | test | 142000.0 | 0.0963 | n/a | 1,099,040 |
| minus_quality | test | 142100.0 | 0.0995 | n/a | 1,099,040 |
| minus_quality | test | 142200.0 | 0.1170 | n/a | 1,099,040 |
| minus_quality | test | 142300.0 | 0.1123 | n/a | 1,099,040 |
| minus_quality | test | 142400.0 | 0.1124 | n/a | 1,099,040 |
| minus_quality | test | 142500.0 | 0.1049 | n/a | 1,099,040 |
| minus_quality | test | 142600.0 | 0.1018 | n/a | 1,099,040 |
| minus_quality | test | 142700.0 | 0.1027 | n/a | 1,099,040 |
| minus_quality | test | 142800.0 | 0.1207 | n/a | 1,099,040 |
| minus_quality | test | 142900.0 | 0.1292 | n/a | 1,099,040 |
| minus_quality | test | 143000.0 | 0.1210 | n/a | 1,099,040 |
| minus_quality | test | 143100.0 | 0.1117 | n/a | 1,099,040 |
| minus_quality | test | 143200.0 | 0.1090 | n/a | 1,099,040 |
| minus_quality | test | 143300.0 | 0.1085 | n/a | 1,099,040 |
| minus_quality | test | 143400.0 | 0.1044 | n/a | 1,099,040 |
| minus_quality | test | 143500.0 | 0.1162 | n/a | 1,099,040 |
| minus_quality | test | 143600.0 | 0.1234 | n/a | 1,099,040 |
| minus_quality | test | 143700.0 | 0.1394 | n/a | 1,099,040 |
| minus_quality | test | 143800.0 | 0.1488 | n/a | 1,099,040 |
| minus_quality | test | 143900.0 | 0.1466 | n/a | 1,099,040 |
| minus_quality | test | 144000.0 | 0.1376 | n/a | 1,099,040 |
| minus_quality | test | 144100.0 | 0.1284 | n/a | 1,099,040 |
| minus_quality | test | 144200.0 | 0.1227 | n/a | 1,099,040 |
| minus_quality | test | 144300.0 | 0.1253 | n/a | 1,099,040 |
| minus_quality | test | 144400.0 | 0.1206 | n/a | 1,099,040 |
| minus_quality | test | 144500.0 | 0.1115 | n/a | 1,099,040 |
| minus_quality | test | 144600.0 | 0.1132 | n/a | 1,099,040 |
| minus_quality | test | 144700.0 | 0.1193 | n/a | 1,099,040 |
| minus_quality | test | 144800.0 | 0.1125 | n/a | 1,099,040 |
| minus_quality | test | 144900.0 | 0.1227 | n/a | 1,099,040 |
| minus_quality | train | 103900.0 | 0.1459 | n/a | 49,496 |
| minus_quality | train | 104000.0 | 0.1355 | n/a | 49,496 |
| minus_quality | train | 104100.0 | 0.1375 | n/a | 49,496 |
| minus_quality | train | 104200.0 | 0.1328 | n/a | 49,496 |
| minus_quality | train | 104300.0 | 0.1296 | n/a | 49,496 |
| minus_quality | train | 104400.0 | 0.1328 | n/a | 49,496 |
| minus_quality | train | 104500.0 | 0.1371 | n/a | 49,496 |
| minus_quality | train | 104600.0 | 0.1525 | n/a | 49,496 |
| minus_quality | train | 104700.0 | 0.1547 | n/a | 49,496 |
| minus_quality | train | 104800.0 | 0.1505 | n/a | 49,496 |
| minus_quality | train | 104900.0 | 0.1699 | n/a | 49,496 |
| minus_quality | train | 105000.0 | 0.1463 | n/a | 49,496 |
| minus_quality | train | 105100.0 | 0.1514 | n/a | 49,496 |
| minus_quality | train | 105200.0 | 0.1637 | n/a | 49,496 |
| minus_quality | train | 105300.0 | 0.1572 | n/a | 49,496 |
| minus_quality | train | 105400.0 | 0.1643 | n/a | 49,496 |
| minus_quality | train | 105500.0 | 0.1769 | n/a | 49,496 |
| minus_quality | train | 105600.0 | 0.1869 | n/a | 49,496 |
| minus_quality | train | 105700.0 | 0.1925 | n/a | 49,496 |
| minus_quality | train | 105800.0 | 0.2027 | n/a | 49,496 |
| minus_quality | train | 105900.0 | 0.2229 | n/a | 49,496 |
| minus_quality | train | 110000.0 | 0.1768 | n/a | 49,496 |
| minus_quality | train | 110100.0 | 0.1635 | n/a | 49,496 |
| minus_quality | train | 110200.0 | 0.1539 | n/a | 49,496 |
| minus_quality | train | 110300.0 | 0.1449 | n/a | 49,496 |
| minus_quality | train | 110400.0 | 0.1513 | n/a | 49,496 |
| minus_quality | train | 110500.0 | 0.1510 | n/a | 49,496 |
| minus_quality | train | 110600.0 | 0.1613 | n/a | 49,496 |
| minus_quality | train | 110700.0 | 0.1871 | n/a | 49,496 |
| minus_quality | train | 110800.0 | 0.1917 | n/a | 49,496 |
| minus_quality | train | 110900.0 | 0.2098 | n/a | 49,496 |
| minus_quality | train | 111000.0 | 0.2024 | n/a | 49,496 |
| minus_quality | train | 111100.0 | 0.1959 | n/a | 49,496 |
| minus_quality | train | 111200.0 | 0.2111 | n/a | 49,496 |
| minus_quality | train | 111300.0 | 0.2069 | n/a | 49,496 |
| minus_quality | train | 111400.0 | 0.2056 | n/a | 49,496 |
| minus_quality | train | 111500.0 | 0.1865 | n/a | 49,496 |
| minus_quality | train | 111600.0 | 0.1919 | n/a | 49,496 |
| minus_quality | train | 111700.0 | 0.1803 | n/a | 49,496 |
| minus_quality | train | 111800.0 | 0.1753 | n/a | 49,496 |
| minus_quality | train | 111900.0 | 0.1678 | n/a | 49,496 |
| minus_quality | train | 112000.0 | 0.1490 | n/a | 49,496 |
| minus_quality | train | 112100.0 | 0.1658 | n/a | 49,496 |
| minus_quality | train | 112200.0 | 0.1657 | n/a | 49,496 |
| minus_quality | train | 112300.0 | 0.1464 | n/a | 49,496 |
| minus_quality | train | 112400.0 | 0.1520 | n/a | 49,496 |
| minus_quality | train | 112500.0 | 0.1439 | n/a | 49,496 |
| minus_quality | train | 112600.0 | 0.1412 | n/a | 49,496 |
| minus_quality | train | 112700.0 | 0.1406 | n/a | 49,496 |
| minus_quality | train | 112800.0 | 0.1434 | n/a | 49,496 |
| minus_quality | train | 112900.0 | 0.1294 | n/a | 49,496 |
| minus_quality | train | 113000.0 | 0.1743 | n/a | 49,496 |
| minus_quality | train | 130100.0 | 0.1741 | n/a | 49,496 |
| minus_quality | train | 130200.0 | 0.1618 | n/a | 49,496 |
| minus_quality | train | 130300.0 | 0.1542 | n/a | 49,496 |
| minus_quality | train | 130400.0 | 0.1368 | n/a | 49,496 |
| minus_quality | train | 130500.0 | 0.1536 | n/a | 49,496 |
| minus_quality | train | 130600.0 | 0.1528 | n/a | 49,496 |
| minus_quality | train | 130700.0 | 0.1474 | n/a | 49,496 |
| minus_quality | train | 130800.0 | 0.1527 | n/a | 49,496 |
| minus_quality | train | 130900.0 | 0.1560 | n/a | 49,496 |
| minus_quality | train | 131000.0 | 0.1723 | n/a | 49,496 |
| minus_quality | train | 131100.0 | 0.1617 | n/a | 49,496 |
| minus_quality | train | 131200.0 | 0.1732 | n/a | 49,496 |
| minus_quality | train | 131300.0 | 0.1802 | n/a | 49,496 |
| minus_quality | train | 131400.0 | 0.1840 | n/a | 49,496 |
| minus_quality | train | 131500.0 | 0.1821 | n/a | 49,496 |
| minus_quality | train | 131600.0 | 0.1684 | n/a | 49,496 |
| minus_quality | train | 131700.0 | 0.1733 | n/a | 49,496 |
| minus_quality | train | 131800.0 | 0.1699 | n/a | 49,496 |
| minus_quality | train | 131900.0 | 0.1610 | n/a | 49,496 |
| minus_quality | train | 132000.0 | 0.1459 | n/a | 49,496 |
| minus_quality | train | 132100.0 | 0.1553 | n/a | 49,496 |
| minus_quality | train | 132200.0 | 0.1603 | n/a | 49,495 |
| minus_quality | train | 132300.0 | 0.1571 | n/a | 49,495 |
| minus_quality | train | 132400.0 | 0.1664 | n/a | 49,495 |
| minus_quality | train | 132500.0 | 0.1579 | n/a | 49,495 |
| minus_quality | train | 132600.0 | 0.1749 | n/a | 49,495 |
| minus_quality | train | 132700.0 | 0.1776 | n/a | 49,495 |
| minus_quality | train | 132800.0 | 0.1727 | n/a | 49,495 |
| minus_quality | train | 132900.0 | 0.1820 | n/a | 49,495 |
| minus_quality | train | 133000.0 | 0.1518 | n/a | 49,495 |
| minus_quality | train | 133100.0 | 0.1457 | n/a | 49,495 |
| minus_quality | train | 133200.0 | 0.1440 | n/a | 49,495 |
| minus_quality | train | 133300.0 | 0.1898 | n/a | 49,495 |
| minus_quality | train | 133400.0 | 0.1658 | n/a | 49,495 |
| minus_quality | train | 133500.0 | 0.1401 | n/a | 49,495 |
| minus_quality | train | 133600.0 | 0.1404 | n/a | 49,495 |
| minus_quality | train | 133700.0 | 0.1556 | n/a | 49,495 |
| minus_quality | train | 133800.0 | 0.1744 | n/a | 49,495 |
| minus_quality | train | 133900.0 | 0.1953 | n/a | 49,495 |
| minus_quality | train | 134000.0 | 0.1725 | n/a | 49,495 |
| minus_quality | train | 134100.0 | 0.1913 | n/a | 49,495 |
| minus_quality | train | 134200.0 | 0.1937 | n/a | 49,495 |
| minus_quality | train | 134300.0 | 0.1980 | n/a | 49,495 |
| minus_quality | train | 134400.0 | 0.1985 | n/a | 49,495 |
| minus_quality | train | 134500.0 | 0.1925 | n/a | 49,495 |
| minus_quality | train | 134600.0 | 0.1798 | n/a | 49,495 |
| minus_quality | train | 134700.0 | 0.1711 | n/a | 49,495 |
| minus_quality | train | 134800.0 | 0.1831 | n/a | 49,495 |
| minus_quality | train | 134900.0 | 0.2074 | n/a | 49,495 |
| minus_quality | train | 135000.0 | 0.1857 | n/a | 49,495 |
| minus_quality | train | 135100.0 | 0.1931 | n/a | 49,495 |
| minus_quality | train | 135200.0 | 0.1997 | n/a | 49,495 |
| minus_quality | train | 135300.0 | 0.1922 | n/a | 49,495 |
| minus_quality | train | 135400.0 | 0.1822 | n/a | 49,495 |
| minus_quality | train | 135500.0 | 0.1649 | n/a | 49,495 |
| minus_quality | train | 135600.0 | 0.1839 | n/a | 49,495 |
| minus_quality | train | 135700.0 | 0.1728 | n/a | 49,495 |
| minus_quality | train | 135800.0 | 0.1672 | n/a | 49,495 |
| minus_quality | train | 135900.0 | 0.1671 | n/a | 49,495 |
| minus_quality | train | 140000.0 | 0.1379 | n/a | 49,495 |
| minus_quality | train | 140100.0 | 0.1627 | n/a | 49,495 |
| minus_quality | train | 140200.0 | 0.1599 | n/a | 49,495 |
| minus_quality | train | 140300.0 | 0.1555 | n/a | 49,495 |
| minus_quality | train | 140400.0 | 0.1854 | n/a | 49,495 |
| minus_quality | train | 140500.0 | 0.1865 | n/a | 49,495 |
| minus_quality | train | 140600.0 | 0.1765 | n/a | 49,495 |
| minus_quality | train | 140700.0 | 0.1857 | n/a | 49,495 |
| minus_quality | train | 140800.0 | 0.1811 | n/a | 49,495 |
| minus_quality | train | 140900.0 | 0.1916 | n/a | 49,495 |
| minus_quality | train | 141000.0 | 0.2029 | n/a | 49,495 |
| minus_quality | train | 141100.0 | 0.2308 | n/a | 49,495 |
| minus_quality | train | 141200.0 | 0.2471 | n/a | 49,495 |
| minus_quality | train | 141300.0 | 0.2794 | n/a | 49,495 |
| minus_quality | train | 141400.0 | 0.2736 | n/a | 49,495 |
| minus_quality | train | 141500.0 | 0.2454 | n/a | 49,495 |
| minus_quality | train | 141600.0 | 0.2165 | n/a | 49,495 |
| minus_quality | train | 141700.0 | 0.2028 | n/a | 49,495 |
| minus_quality | train | 141800.0 | 0.1913 | n/a | 49,495 |
| minus_quality | train | 141900.0 | 0.1873 | n/a | 49,495 |
| minus_quality | train | 142000.0 | 0.1572 | n/a | 49,495 |
| minus_quality | train | 142100.0 | 0.1713 | n/a | 49,495 |
| minus_quality | train | 142200.0 | 0.1888 | n/a | 49,495 |
| minus_quality | train | 142300.0 | 0.1925 | n/a | 49,495 |
| minus_quality | train | 142400.0 | 0.2040 | n/a | 49,495 |
| minus_quality | train | 142500.0 | 0.2220 | n/a | 49,495 |
| minus_quality | train | 142600.0 | 0.2520 | n/a | 49,495 |
| minus_quality | train | 142700.0 | 0.2439 | n/a | 49,495 |
| minus_quality | train | 142800.0 | 0.2197 | n/a | 49,495 |
| minus_quality | train | 142900.0 | 0.2045 | n/a | 49,495 |
| minus_quality | train | 143000.0 | 0.1638 | n/a | 49,495 |
| minus_quality | train | 143100.0 | 0.1737 | n/a | 49,495 |
| minus_quality | train | 143200.0 | 0.1867 | n/a | 49,495 |
| minus_quality | train | 143300.0 | 0.2027 | n/a | 49,495 |
| minus_quality | train | 143400.0 | 0.2271 | n/a | 49,495 |
| minus_quality | train | 143500.0 | 0.2466 | n/a | 49,495 |
| minus_quality | train | 143600.0 | 0.2597 | n/a | 49,495 |
| minus_quality | train | 143700.0 | 0.2692 | n/a | 49,495 |
| minus_quality | train | 143800.0 | 0.2435 | n/a | 49,495 |
| minus_quality | train | 143900.0 | 0.2422 | n/a | 49,495 |
| minus_quality | train | 144000.0 | 0.2198 | n/a | 49,495 |
| minus_quality | train | 144100.0 | 0.2173 | n/a | 49,495 |
| minus_quality | train | 144200.0 | 0.1937 | n/a | 49,495 |
| minus_quality | train | 144300.0 | 0.2000 | n/a | 49,495 |
| minus_quality | train | 144400.0 | 0.2008 | n/a | 49,495 |
| minus_quality | train | 144500.0 | 0.1778 | n/a | 49,495 |
| minus_quality | train | 144600.0 | 0.1792 | n/a | 49,495 |
| minus_quality | train | 144700.0 | 0.1887 | n/a | 49,495 |
| minus_quality | train | 144800.0 | 0.1979 | n/a | 49,495 |
| minus_quality | train | 144900.0 | 0.1954 | n/a | 49,495 |
| minus_spread_mid | test | 103900.0 | 0.0576 | n/a | 1,099,040 |
| minus_spread_mid | test | 104000.0 | 0.0596 | n/a | 1,099,040 |
| minus_spread_mid | test | 104100.0 | 0.0728 | n/a | 1,099,040 |
| minus_spread_mid | test | 104200.0 | 0.0835 | n/a | 1,099,040 |
| minus_spread_mid | test | 104300.0 | 0.0864 | n/a | 1,099,040 |
| minus_spread_mid | test | 104400.0 | 0.0732 | n/a | 1,099,040 |
| minus_spread_mid | test | 104500.0 | 0.0742 | n/a | 1,099,040 |
| minus_spread_mid | test | 104600.0 | 0.0801 | n/a | 1,099,040 |
| minus_spread_mid | test | 104700.0 | 0.0764 | n/a | 1,099,040 |
| minus_spread_mid | test | 104800.0 | 0.0816 | n/a | 1,099,040 |
| minus_spread_mid | test | 104900.0 | 0.0805 | n/a | 1,099,040 |
| minus_spread_mid | test | 105000.0 | 0.0650 | n/a | 1,099,040 |
| minus_spread_mid | test | 105100.0 | 0.0647 | n/a | 1,099,040 |
| minus_spread_mid | test | 105200.0 | 0.0552 | n/a | 1,099,040 |
| minus_spread_mid | test | 105300.0 | 0.0532 | n/a | 1,099,040 |
| minus_spread_mid | test | 105400.0 | 0.0517 | n/a | 1,099,040 |
| minus_spread_mid | test | 105500.0 | 0.0526 | n/a | 1,099,040 |
| minus_spread_mid | test | 105600.0 | 0.0388 | n/a | 1,099,040 |
| minus_spread_mid | test | 105700.0 | 0.0391 | n/a | 1,099,040 |
| minus_spread_mid | test | 105800.0 | 0.0420 | n/a | 1,099,040 |
| minus_spread_mid | test | 105900.0 | 0.0440 | n/a | 1,099,040 |
| minus_spread_mid | test | 110000.0 | 0.0353 | n/a | 1,099,040 |
| minus_spread_mid | test | 110100.0 | 0.0287 | n/a | 1,099,040 |
| minus_spread_mid | test | 110200.0 | 0.0472 | n/a | 1,099,040 |
| minus_spread_mid | test | 110300.0 | 0.0525 | n/a | 1,099,040 |
| minus_spread_mid | test | 110400.0 | 0.0530 | n/a | 1,099,040 |
| minus_spread_mid | test | 110500.0 | 0.0490 | n/a | 1,099,040 |
| minus_spread_mid | test | 110600.0 | 0.0348 | n/a | 1,099,040 |
| minus_spread_mid | test | 110700.0 | 0.0267 | n/a | 1,099,040 |
| minus_spread_mid | test | 110800.0 | 0.0317 | n/a | 1,099,040 |
| minus_spread_mid | test | 110900.0 | 0.0455 | n/a | 1,099,040 |
| minus_spread_mid | test | 111000.0 | 0.0452 | n/a | 1,099,040 |
| minus_spread_mid | test | 111100.0 | 0.0367 | n/a | 1,099,040 |
| minus_spread_mid | test | 111200.0 | 0.0411 | n/a | 1,099,040 |
| minus_spread_mid | test | 111300.0 | 0.0421 | n/a | 1,099,040 |
| minus_spread_mid | test | 111400.0 | 0.0515 | n/a | 1,099,040 |
| minus_spread_mid | test | 111500.0 | 0.0574 | n/a | 1,099,040 |
| minus_spread_mid | test | 111600.0 | 0.0683 | n/a | 1,099,040 |
| minus_spread_mid | test | 111700.0 | 0.0691 | n/a | 1,099,040 |
| minus_spread_mid | test | 111800.0 | 0.0739 | n/a | 1,099,040 |
| minus_spread_mid | test | 111900.0 | 0.0746 | n/a | 1,099,040 |
| minus_spread_mid | test | 112000.0 | 0.0681 | n/a | 1,099,040 |
| minus_spread_mid | test | 112100.0 | 0.0610 | n/a | 1,099,040 |
| minus_spread_mid | test | 112200.0 | 0.0445 | n/a | 1,099,040 |
| minus_spread_mid | test | 112300.0 | 0.0381 | n/a | 1,099,040 |
| minus_spread_mid | test | 112400.0 | 0.0306 | n/a | 1,099,040 |
| minus_spread_mid | test | 112500.0 | 0.0371 | n/a | 1,099,040 |
| minus_spread_mid | test | 112600.0 | 0.0389 | n/a | 1,099,040 |
| minus_spread_mid | test | 112700.0 | 0.0416 | n/a | 1,099,040 |
| minus_spread_mid | test | 112800.0 | 0.0392 | n/a | 1,099,040 |
| minus_spread_mid | test | 112900.0 | 0.0274 | n/a | 1,099,040 |
| minus_spread_mid | test | 113000.0 | 0.0546 | n/a | 1,099,040 |
| minus_spread_mid | test | 130100.0 | 0.0573 | n/a | 1,099,040 |
| minus_spread_mid | test | 130200.0 | 0.0527 | n/a | 1,099,040 |
| minus_spread_mid | test | 130300.0 | 0.0600 | n/a | 1,099,040 |
| minus_spread_mid | test | 130400.0 | 0.0552 | n/a | 1,099,040 |
| minus_spread_mid | test | 130500.0 | 0.0491 | n/a | 1,099,040 |
| minus_spread_mid | test | 130600.0 | 0.0361 | n/a | 1,099,040 |
| minus_spread_mid | test | 130700.0 | 0.0269 | n/a | 1,099,040 |
| minus_spread_mid | test | 130800.0 | 0.0384 | n/a | 1,099,040 |
| minus_spread_mid | test | 130900.0 | 0.0469 | n/a | 1,099,040 |
| minus_spread_mid | test | 131000.0 | 0.0433 | n/a | 1,099,040 |
| minus_spread_mid | test | 131100.0 | 0.0598 | n/a | 1,099,040 |
| minus_spread_mid | test | 131200.0 | 0.0619 | n/a | 1,099,040 |
| minus_spread_mid | test | 131300.0 | 0.0672 | n/a | 1,099,040 |
| minus_spread_mid | test | 131400.0 | 0.0661 | n/a | 1,099,040 |
| minus_spread_mid | test | 131500.0 | 0.0609 | n/a | 1,099,040 |
| minus_spread_mid | test | 131600.0 | 0.0730 | n/a | 1,099,040 |
| minus_spread_mid | test | 131700.0 | 0.0723 | n/a | 1,099,040 |
| minus_spread_mid | test | 131800.0 | 0.0681 | n/a | 1,099,040 |
| minus_spread_mid | test | 131900.0 | 0.0673 | n/a | 1,099,040 |
| minus_spread_mid | test | 132000.0 | 0.0608 | n/a | 1,099,040 |
| minus_spread_mid | test | 132100.0 | 0.0530 | n/a | 1,099,040 |
| minus_spread_mid | test | 132200.0 | 0.0505 | n/a | 1,099,040 |
| minus_spread_mid | test | 132300.0 | 0.0526 | n/a | 1,099,040 |
| minus_spread_mid | test | 132400.0 | 0.0505 | n/a | 1,099,040 |
| minus_spread_mid | test | 132500.0 | 0.0557 | n/a | 1,099,040 |
| minus_spread_mid | test | 132600.0 | 0.0654 | n/a | 1,099,040 |
| minus_spread_mid | test | 132700.0 | 0.0687 | n/a | 1,099,040 |
| minus_spread_mid | test | 132800.0 | 0.0610 | n/a | 1,099,040 |
| minus_spread_mid | test | 132900.0 | 0.0701 | n/a | 1,099,040 |
| minus_spread_mid | test | 133000.0 | 0.0572 | n/a | 1,099,040 |
| minus_spread_mid | test | 133100.0 | 0.0574 | n/a | 1,099,040 |
| minus_spread_mid | test | 133200.0 | 0.0701 | n/a | 1,099,040 |
| minus_spread_mid | test | 133300.0 | 0.0743 | n/a | 1,099,040 |
| minus_spread_mid | test | 133400.0 | 0.0777 | n/a | 1,099,040 |
| minus_spread_mid | test | 133500.0 | 0.0727 | n/a | 1,099,040 |
| minus_spread_mid | test | 133600.0 | 0.0780 | n/a | 1,099,040 |
| minus_spread_mid | test | 133700.0 | 0.0896 | n/a | 1,099,040 |
| minus_spread_mid | test | 133800.0 | 0.0915 | n/a | 1,099,040 |
| minus_spread_mid | test | 133900.0 | 0.0839 | n/a | 1,099,040 |
| minus_spread_mid | test | 134000.0 | 0.0728 | n/a | 1,099,040 |
| minus_spread_mid | test | 134100.0 | 0.0579 | n/a | 1,099,040 |
| minus_spread_mid | test | 134200.0 | 0.0663 | n/a | 1,099,040 |
| minus_spread_mid | test | 134300.0 | 0.0717 | n/a | 1,099,040 |
| minus_spread_mid | test | 134400.0 | 0.0724 | n/a | 1,099,040 |
| minus_spread_mid | test | 134500.0 | 0.0632 | n/a | 1,099,040 |
| minus_spread_mid | test | 134600.0 | 0.0665 | n/a | 1,099,040 |
| minus_spread_mid | test | 134700.0 | 0.0701 | n/a | 1,099,040 |
| minus_spread_mid | test | 134800.0 | 0.0760 | n/a | 1,099,040 |
| minus_spread_mid | test | 134900.0 | 0.0823 | n/a | 1,099,040 |
| minus_spread_mid | test | 135000.0 | 0.0814 | n/a | 1,099,040 |
| minus_spread_mid | test | 135100.0 | 0.0802 | n/a | 1,099,040 |
| minus_spread_mid | test | 135200.0 | 0.0835 | n/a | 1,099,040 |
| minus_spread_mid | test | 135300.0 | 0.0895 | n/a | 1,099,040 |
| minus_spread_mid | test | 135400.0 | 0.0907 | n/a | 1,099,040 |
| minus_spread_mid | test | 135500.0 | 0.0935 | n/a | 1,099,040 |
| minus_spread_mid | test | 135600.0 | 0.0908 | n/a | 1,099,040 |
| minus_spread_mid | test | 135700.0 | 0.1075 | n/a | 1,099,040 |
| minus_spread_mid | test | 135800.0 | 0.1187 | n/a | 1,099,040 |
| minus_spread_mid | test | 135900.0 | 0.1217 | n/a | 1,099,040 |
| minus_spread_mid | test | 140000.0 | 0.1019 | n/a | 1,099,040 |
| minus_spread_mid | test | 140100.0 | 0.1097 | n/a | 1,099,040 |
| minus_spread_mid | test | 140200.0 | 0.1146 | n/a | 1,099,040 |
| minus_spread_mid | test | 140300.0 | 0.1173 | n/a | 1,099,040 |
| minus_spread_mid | test | 140400.0 | 0.1199 | n/a | 1,099,040 |
| minus_spread_mid | test | 140500.0 | 0.1049 | n/a | 1,099,040 |
| minus_spread_mid | test | 140600.0 | 0.1009 | n/a | 1,099,040 |
| minus_spread_mid | test | 140700.0 | 0.1009 | n/a | 1,099,040 |
| minus_spread_mid | test | 140800.0 | 0.0932 | n/a | 1,099,040 |
| minus_spread_mid | test | 140900.0 | 0.0857 | n/a | 1,099,040 |
| minus_spread_mid | test | 141000.0 | 0.0595 | n/a | 1,099,040 |
| minus_spread_mid | test | 141100.0 | 0.0444 | n/a | 1,099,040 |
| minus_spread_mid | test | 141200.0 | 0.0365 | n/a | 1,099,040 |
| minus_spread_mid | test | 141300.0 | 0.0257 | n/a | 1,099,040 |
| minus_spread_mid | test | 141400.0 | 0.0328 | n/a | 1,099,040 |
| minus_spread_mid | test | 141500.0 | 0.0416 | n/a | 1,099,040 |
| minus_spread_mid | test | 141600.0 | 0.0535 | n/a | 1,099,040 |
| minus_spread_mid | test | 141700.0 | 0.0642 | n/a | 1,099,040 |
| minus_spread_mid | test | 141800.0 | 0.0543 | n/a | 1,099,040 |
| minus_spread_mid | test | 141900.0 | 0.0589 | n/a | 1,099,040 |
| minus_spread_mid | test | 142000.0 | 0.0684 | n/a | 1,099,040 |
| minus_spread_mid | test | 142100.0 | 0.0718 | n/a | 1,099,040 |
| minus_spread_mid | test | 142200.0 | 0.1016 | n/a | 1,099,040 |
| minus_spread_mid | test | 142300.0 | 0.1025 | n/a | 1,099,040 |
| minus_spread_mid | test | 142400.0 | 0.1070 | n/a | 1,099,040 |
| minus_spread_mid | test | 142500.0 | 0.1020 | n/a | 1,099,040 |
| minus_spread_mid | test | 142600.0 | 0.1065 | n/a | 1,099,040 |
| minus_spread_mid | test | 142700.0 | 0.1169 | n/a | 1,099,040 |
| minus_spread_mid | test | 142800.0 | 0.1323 | n/a | 1,099,040 |
| minus_spread_mid | test | 142900.0 | 0.1376 | n/a | 1,099,040 |
| minus_spread_mid | test | 143000.0 | 0.1194 | n/a | 1,099,040 |
| minus_spread_mid | test | 143100.0 | 0.1154 | n/a | 1,099,040 |
| minus_spread_mid | test | 143200.0 | 0.1046 | n/a | 1,099,040 |
| minus_spread_mid | test | 143300.0 | 0.0943 | n/a | 1,099,040 |
| minus_spread_mid | test | 143400.0 | 0.0886 | n/a | 1,099,040 |
| minus_spread_mid | test | 143500.0 | 0.0971 | n/a | 1,099,040 |
| minus_spread_mid | test | 143600.0 | 0.1073 | n/a | 1,099,040 |
| minus_spread_mid | test | 143700.0 | 0.1209 | n/a | 1,099,040 |
| minus_spread_mid | test | 143800.0 | 0.1360 | n/a | 1,099,040 |
| minus_spread_mid | test | 143900.0 | 0.1337 | n/a | 1,099,040 |
| minus_spread_mid | test | 144000.0 | 0.1305 | n/a | 1,099,040 |
| minus_spread_mid | test | 144100.0 | 0.1207 | n/a | 1,099,040 |
| minus_spread_mid | test | 144200.0 | 0.1116 | n/a | 1,099,040 |
| minus_spread_mid | test | 144300.0 | 0.1068 | n/a | 1,099,040 |
| minus_spread_mid | test | 144400.0 | 0.1014 | n/a | 1,099,040 |
| minus_spread_mid | test | 144500.0 | 0.0914 | n/a | 1,099,040 |
| minus_spread_mid | test | 144600.0 | 0.0900 | n/a | 1,099,040 |
| minus_spread_mid | test | 144700.0 | 0.1039 | n/a | 1,099,040 |
| minus_spread_mid | test | 144800.0 | 0.1069 | n/a | 1,099,040 |
| minus_spread_mid | test | 144900.0 | 0.1035 | n/a | 1,099,040 |
| minus_spread_mid | train | 103900.0 | 0.1256 | n/a | 49,496 |
| minus_spread_mid | train | 104000.0 | 0.1114 | n/a | 49,496 |
| minus_spread_mid | train | 104100.0 | 0.1112 | n/a | 49,496 |
| minus_spread_mid | train | 104200.0 | 0.1190 | n/a | 49,496 |
| minus_spread_mid | train | 104300.0 | 0.1133 | n/a | 49,496 |
| minus_spread_mid | train | 104400.0 | 0.1238 | n/a | 49,496 |
| minus_spread_mid | train | 104500.0 | 0.1329 | n/a | 49,496 |
| minus_spread_mid | train | 104600.0 | 0.1380 | n/a | 49,496 |
| minus_spread_mid | train | 104700.0 | 0.1488 | n/a | 49,496 |
| minus_spread_mid | train | 104800.0 | 0.1492 | n/a | 49,496 |
| minus_spread_mid | train | 104900.0 | 0.1581 | n/a | 49,496 |
| minus_spread_mid | train | 105000.0 | 0.1425 | n/a | 49,496 |
| minus_spread_mid | train | 105100.0 | 0.1459 | n/a | 49,496 |
| minus_spread_mid | train | 105200.0 | 0.1647 | n/a | 49,496 |
| minus_spread_mid | train | 105300.0 | 0.1475 | n/a | 49,496 |
| minus_spread_mid | train | 105400.0 | 0.1513 | n/a | 49,496 |
| minus_spread_mid | train | 105500.0 | 0.1642 | n/a | 49,496 |
| minus_spread_mid | train | 105600.0 | 0.1669 | n/a | 49,496 |
| minus_spread_mid | train | 105700.0 | 0.1815 | n/a | 49,496 |
| minus_spread_mid | train | 105800.0 | 0.1934 | n/a | 49,496 |
| minus_spread_mid | train | 105900.0 | 0.2056 | n/a | 49,496 |
| minus_spread_mid | train | 110000.0 | 0.1792 | n/a | 49,496 |
| minus_spread_mid | train | 110100.0 | 0.1472 | n/a | 49,496 |
| minus_spread_mid | train | 110200.0 | 0.1323 | n/a | 49,496 |
| minus_spread_mid | train | 110300.0 | 0.1292 | n/a | 49,496 |
| minus_spread_mid | train | 110400.0 | 0.1301 | n/a | 49,496 |
| minus_spread_mid | train | 110500.0 | 0.1252 | n/a | 49,496 |
| minus_spread_mid | train | 110600.0 | 0.1399 | n/a | 49,496 |
| minus_spread_mid | train | 110700.0 | 0.1655 | n/a | 49,496 |
| minus_spread_mid | train | 110800.0 | 0.1818 | n/a | 49,496 |
| minus_spread_mid | train | 110900.0 | 0.1950 | n/a | 49,496 |
| minus_spread_mid | train | 111000.0 | 0.1829 | n/a | 49,496 |
| minus_spread_mid | train | 111100.0 | 0.1856 | n/a | 49,496 |
| minus_spread_mid | train | 111200.0 | 0.1951 | n/a | 49,496 |
| minus_spread_mid | train | 111300.0 | 0.1795 | n/a | 49,496 |
| minus_spread_mid | train | 111400.0 | 0.1915 | n/a | 49,496 |
| minus_spread_mid | train | 111500.0 | 0.1753 | n/a | 49,496 |
| minus_spread_mid | train | 111600.0 | 0.1746 | n/a | 49,496 |
| minus_spread_mid | train | 111700.0 | 0.1541 | n/a | 49,496 |
| minus_spread_mid | train | 111800.0 | 0.1516 | n/a | 49,496 |
| minus_spread_mid | train | 111900.0 | 0.1494 | n/a | 49,496 |
| minus_spread_mid | train | 112000.0 | 0.1356 | n/a | 49,496 |
| minus_spread_mid | train | 112100.0 | 0.1510 | n/a | 49,496 |
| minus_spread_mid | train | 112200.0 | 0.1418 | n/a | 49,496 |
| minus_spread_mid | train | 112300.0 | 0.1277 | n/a | 49,496 |
| minus_spread_mid | train | 112400.0 | 0.1318 | n/a | 49,496 |
| minus_spread_mid | train | 112500.0 | 0.1306 | n/a | 49,496 |
| minus_spread_mid | train | 112600.0 | 0.1212 | n/a | 49,496 |
| minus_spread_mid | train | 112700.0 | 0.1341 | n/a | 49,496 |
| minus_spread_mid | train | 112800.0 | 0.1204 | n/a | 49,496 |
| minus_spread_mid | train | 112900.0 | 0.1054 | n/a | 49,496 |
| minus_spread_mid | train | 113000.0 | 0.1423 | n/a | 49,496 |
| minus_spread_mid | train | 130100.0 | 0.1452 | n/a | 49,496 |
| minus_spread_mid | train | 130200.0 | 0.1343 | n/a | 49,496 |
| minus_spread_mid | train | 130300.0 | 0.1338 | n/a | 49,496 |
| minus_spread_mid | train | 130400.0 | 0.1160 | n/a | 49,496 |
| minus_spread_mid | train | 130500.0 | 0.1155 | n/a | 49,496 |
| minus_spread_mid | train | 130600.0 | 0.1303 | n/a | 49,496 |
| minus_spread_mid | train | 130700.0 | 0.1336 | n/a | 49,496 |
| minus_spread_mid | train | 130800.0 | 0.1372 | n/a | 49,496 |
| minus_spread_mid | train | 130900.0 | 0.1333 | n/a | 49,496 |
| minus_spread_mid | train | 131000.0 | 0.1484 | n/a | 49,496 |
| minus_spread_mid | train | 131100.0 | 0.1570 | n/a | 49,496 |
| minus_spread_mid | train | 131200.0 | 0.1729 | n/a | 49,496 |
| minus_spread_mid | train | 131300.0 | 0.1775 | n/a | 49,496 |
| minus_spread_mid | train | 131400.0 | 0.1779 | n/a | 49,496 |
| minus_spread_mid | train | 131500.0 | 0.1649 | n/a | 49,496 |
| minus_spread_mid | train | 131600.0 | 0.1564 | n/a | 49,496 |
| minus_spread_mid | train | 131700.0 | 0.1624 | n/a | 49,496 |
| minus_spread_mid | train | 131800.0 | 0.1580 | n/a | 49,496 |
| minus_spread_mid | train | 131900.0 | 0.1519 | n/a | 49,496 |
| minus_spread_mid | train | 132000.0 | 0.1320 | n/a | 49,496 |
| minus_spread_mid | train | 132100.0 | 0.1391 | n/a | 49,496 |
| minus_spread_mid | train | 132200.0 | 0.1539 | n/a | 49,495 |
| minus_spread_mid | train | 132300.0 | 0.1545 | n/a | 49,495 |
| minus_spread_mid | train | 132400.0 | 0.1584 | n/a | 49,495 |
| minus_spread_mid | train | 132500.0 | 0.1478 | n/a | 49,495 |
| minus_spread_mid | train | 132600.0 | 0.1641 | n/a | 49,495 |
| minus_spread_mid | train | 132700.0 | 0.1742 | n/a | 49,495 |
| minus_spread_mid | train | 132800.0 | 0.1752 | n/a | 49,495 |
| minus_spread_mid | train | 132900.0 | 0.1873 | n/a | 49,495 |
| minus_spread_mid | train | 133000.0 | 0.1703 | n/a | 49,495 |
| minus_spread_mid | train | 133100.0 | 0.1652 | n/a | 49,495 |
| minus_spread_mid | train | 133200.0 | 0.1509 | n/a | 49,495 |
| minus_spread_mid | train | 133300.0 | 0.1608 | n/a | 49,495 |
| minus_spread_mid | train | 133400.0 | 0.1597 | n/a | 49,495 |
| minus_spread_mid | train | 133500.0 | 0.1511 | n/a | 49,495 |
| minus_spread_mid | train | 133600.0 | 0.1406 | n/a | 49,495 |
| minus_spread_mid | train | 133700.0 | 0.1393 | n/a | 49,495 |
| minus_spread_mid | train | 133800.0 | 0.1481 | n/a | 49,495 |
| minus_spread_mid | train | 133900.0 | 0.1530 | n/a | 49,495 |
| minus_spread_mid | train | 134000.0 | 0.1581 | n/a | 49,495 |
| minus_spread_mid | train | 134100.0 | 0.1720 | n/a | 49,495 |
| minus_spread_mid | train | 134200.0 | 0.1705 | n/a | 49,495 |
| minus_spread_mid | train | 134300.0 | 0.1742 | n/a | 49,495 |
| minus_spread_mid | train | 134400.0 | 0.1699 | n/a | 49,495 |
| minus_spread_mid | train | 134500.0 | 0.1672 | n/a | 49,495 |
| minus_spread_mid | train | 134600.0 | 0.1572 | n/a | 49,495 |
| minus_spread_mid | train | 134700.0 | 0.1472 | n/a | 49,495 |
| minus_spread_mid | train | 134800.0 | 0.1558 | n/a | 49,495 |
| minus_spread_mid | train | 134900.0 | 0.1745 | n/a | 49,495 |
| minus_spread_mid | train | 135000.0 | 0.1519 | n/a | 49,495 |
| minus_spread_mid | train | 135100.0 | 0.1704 | n/a | 49,495 |
| minus_spread_mid | train | 135200.0 | 0.1680 | n/a | 49,495 |
| minus_spread_mid | train | 135300.0 | 0.1744 | n/a | 49,495 |
| minus_spread_mid | train | 135400.0 | 0.1740 | n/a | 49,495 |
| minus_spread_mid | train | 135500.0 | 0.1538 | n/a | 49,495 |
| minus_spread_mid | train | 135600.0 | 0.1626 | n/a | 49,495 |
| minus_spread_mid | train | 135700.0 | 0.1524 | n/a | 49,495 |
| minus_spread_mid | train | 135800.0 | 0.1417 | n/a | 49,495 |
| minus_spread_mid | train | 135900.0 | 0.1309 | n/a | 49,495 |
| minus_spread_mid | train | 140000.0 | 0.0988 | n/a | 49,495 |
| minus_spread_mid | train | 140100.0 | 0.1184 | n/a | 49,495 |
| minus_spread_mid | train | 140200.0 | 0.1277 | n/a | 49,495 |
| minus_spread_mid | train | 140300.0 | 0.1382 | n/a | 49,495 |
| minus_spread_mid | train | 140400.0 | 0.1509 | n/a | 49,495 |
| minus_spread_mid | train | 140500.0 | 0.1630 | n/a | 49,495 |
| minus_spread_mid | train | 140600.0 | 0.1614 | n/a | 49,495 |
| minus_spread_mid | train | 140700.0 | 0.1626 | n/a | 49,495 |
| minus_spread_mid | train | 140800.0 | 0.1585 | n/a | 49,495 |
| minus_spread_mid | train | 140900.0 | 0.1621 | n/a | 49,495 |
| minus_spread_mid | train | 141000.0 | 0.1766 | n/a | 49,495 |
| minus_spread_mid | train | 141100.0 | 0.2044 | n/a | 49,495 |
| minus_spread_mid | train | 141200.0 | 0.2305 | n/a | 49,495 |
| minus_spread_mid | train | 141300.0 | 0.2672 | n/a | 49,495 |
| minus_spread_mid | train | 141400.0 | 0.2893 | n/a | 49,495 |
| minus_spread_mid | train | 141500.0 | 0.2534 | n/a | 49,495 |
| minus_spread_mid | train | 141600.0 | 0.2263 | n/a | 49,495 |
| minus_spread_mid | train | 141700.0 | 0.2127 | n/a | 49,495 |
| minus_spread_mid | train | 141800.0 | 0.2085 | n/a | 49,495 |
| minus_spread_mid | train | 141900.0 | 0.1873 | n/a | 49,495 |
| minus_spread_mid | train | 142000.0 | 0.1434 | n/a | 49,495 |
| minus_spread_mid | train | 142100.0 | 0.1638 | n/a | 49,495 |
| minus_spread_mid | train | 142200.0 | 0.1705 | n/a | 49,495 |
| minus_spread_mid | train | 142300.0 | 0.1775 | n/a | 49,495 |
| minus_spread_mid | train | 142400.0 | 0.1837 | n/a | 49,495 |
| minus_spread_mid | train | 142500.0 | 0.2095 | n/a | 49,495 |
| minus_spread_mid | train | 142600.0 | 0.2333 | n/a | 49,495 |
| minus_spread_mid | train | 142700.0 | 0.2355 | n/a | 49,495 |
| minus_spread_mid | train | 142800.0 | 0.2206 | n/a | 49,495 |
| minus_spread_mid | train | 142900.0 | 0.2042 | n/a | 49,495 |
| minus_spread_mid | train | 143000.0 | 0.1577 | n/a | 49,495 |
| minus_spread_mid | train | 143100.0 | 0.1594 | n/a | 49,495 |
| minus_spread_mid | train | 143200.0 | 0.1773 | n/a | 49,495 |
| minus_spread_mid | train | 143300.0 | 0.1888 | n/a | 49,495 |
| minus_spread_mid | train | 143400.0 | 0.2035 | n/a | 49,495 |
| minus_spread_mid | train | 143500.0 | 0.2282 | n/a | 49,495 |
| minus_spread_mid | train | 143600.0 | 0.2444 | n/a | 49,495 |
| minus_spread_mid | train | 143700.0 | 0.2444 | n/a | 49,495 |
| minus_spread_mid | train | 143800.0 | 0.2072 | n/a | 49,495 |
| minus_spread_mid | train | 143900.0 | 0.2033 | n/a | 49,495 |
| minus_spread_mid | train | 144000.0 | 0.1878 | n/a | 49,495 |
| minus_spread_mid | train | 144100.0 | 0.1797 | n/a | 49,495 |
| minus_spread_mid | train | 144200.0 | 0.1662 | n/a | 49,495 |
| minus_spread_mid | train | 144300.0 | 0.1725 | n/a | 49,495 |
| minus_spread_mid | train | 144400.0 | 0.1700 | n/a | 49,495 |
| minus_spread_mid | train | 144500.0 | 0.1623 | n/a | 49,495 |
| minus_spread_mid | train | 144600.0 | 0.1582 | n/a | 49,495 |
| minus_spread_mid | train | 144700.0 | 0.1656 | n/a | 49,495 |
| minus_spread_mid | train | 144800.0 | 0.1623 | n/a | 49,495 |
| minus_spread_mid | train | 144900.0 | 0.1655 | n/a | 49,495 |

## 限制与适用边界

L2 训练和评估已产生历史结果, all_fast12 观察 test IC 为0.0805. Baseline/LOO 与 only/all_fast12 的 checkpoint 候选数为11 vs 1, 因而贡献归因无效, 不等于实验流程失败. 当前artifact可得性只影响复现, 不作为历史成功/失败判据. 只有matched合同内的结果可以直接比较.

## 结论

本次归档保留上述历史事实. 研究结论, 推广门槛和执行限制分别解释, 不把模型无增益或净收益为负改写成实验流程失败.

## 附录

### 7. Appendix

### 7.1. Source Artifacts

Source Artifact Table

| experiment | artifact | path | exists | row_count | mtime |
| --- | --- | --- | --- | --- | --- |
| minus_depth | adv_liquidity_bucket_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/liquidity_by_adv/adv_liquidity_bucket_metrics.csv | True | 5 | 2026-07-03 07:33:40 |
| minus_depth | best_checkpoint_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/date_ranges/run/checkpoint_metadata/best_checkpoint.yaml | True | n/a | 2026-07-03 07:10:41 |
| minus_depth | checkpoint_selector_table | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/checkpoint_selector_table.csv | True | 11 | 2026-07-03 07:31:39 |
| minus_depth | core_ic_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/core_ic_metrics.csv | True | 2 | 2026-07-03 07:32:10 |
| minus_depth | goodness_of_fit_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/signal_quality/goodness_of_fit_metrics.csv | True | 200 | 2026-07-03 07:32:25 |
| minus_depth | important_pool_cost_sensitivity | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/important_pool/important_pool_test_cost_sensitivity_returns.csv | True | 241,500 | 2026-07-03 07:33:48 |
| minus_depth | important_pool_cumulative_returns | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/important_pool/important_pool_train_val_test_cumulative_returns.csv | True | 71,967 | 2026-07-03 07:31:55 |
| minus_depth | important_pool_pooled_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/important_pool/important_pool_pooled_ic.csv | True | 3 | 2026-07-03 07:31:09 |
| minus_depth | important_pool_prediction_curve | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/important_pool/prediction_real_return_curve.csv | True | 60 | 2026-07-03 07:31:39 |
| minus_depth | important_pool_trade_return_distribution | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/important_pool/important_pool_trade_return_distribution.csv | True | 818 | 2026-07-03 07:33:51 |
| minus_depth | meta_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/date_ranges/artifacts/npz/meta.yaml | True | n/a | 2026-07-03 02:19:01 |
| minus_depth | monthly_ic_rank_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/robustness/monthly_ic_rank_ic.csv | True | 5 | 2026-07-03 07:34:48 |
| minus_depth | perf_audit_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/date_ranges/perf_audit.yaml | True | n/a | 2026-07-03 07:29:27 |
| minus_depth | return_realization | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/robustness/return_realization.csv | True | 20 | 2026-07-03 07:36:29 |
| minus_depth | signal_bucket_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/signal_quality/signal_bucket_metrics.csv | True | 10 | 2026-07-03 07:32:15 |
| minus_depth | single_report_html | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/070307_all_fast12_minus_depth_l2_full_evaluation_report.html | True | n/a | 2026-07-03 07:36:37 |
| minus_depth | topk_robustness | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/robustness/topk_robustness.csv | True | 14 | 2026-07-03 07:36:36 |
| minus_depth | train_test_intraday_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_depth_l2/research_report/robustness/train_test_intraday_ic.csv | True | 161 | 2026-07-03 07:34:32 |
| minus_imbalance | adv_liquidity_bucket_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/liquidity_by_adv/adv_liquidity_bucket_metrics.csv | True | 5 | 2026-07-03 01:01:33 |
| minus_imbalance | best_checkpoint_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/date_ranges/run/checkpoint_metadata/best_checkpoint.yaml | True | n/a | 2026-07-02 19:02:31 |
| minus_imbalance | checkpoint_selector_table | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/checkpoint_selector_table.csv | True | 11 | 2026-07-02 21:39:09 |
| minus_imbalance | core_ic_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/core_ic_metrics.csv | True | 2 | 2026-07-03 00:58:26 |
| minus_imbalance | goodness_of_fit_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/signal_quality/goodness_of_fit_metrics.csv | True | 200 | 2026-07-03 00:58:50 |
| minus_imbalance | important_pool_cost_sensitivity | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/important_pool/important_pool_test_cost_sensitivity_returns.csv | True | 241,500 | 2026-07-03 01:01:48 |
| minus_imbalance | important_pool_cumulative_returns | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/important_pool/important_pool_train_val_test_cumulative_returns.csv | True | 71,967 | 2026-07-03 00:57:58 |
| minus_imbalance | important_pool_pooled_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/important_pool/important_pool_pooled_ic.csv | True | 3 | 2026-07-02 21:38:31 |
| minus_imbalance | important_pool_prediction_curve | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/important_pool/prediction_real_return_curve.csv | True | 60 | 2026-07-02 21:39:07 |
| minus_imbalance | important_pool_trade_return_distribution | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/important_pool/important_pool_trade_return_distribution.csv | True | 802 | 2026-07-03 01:01:56 |
| minus_imbalance | meta_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/date_ranges/artifacts/npz/meta.yaml | True | n/a | 2026-07-02 13:42:52 |
| minus_imbalance | monthly_ic_rank_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/robustness/monthly_ic_rank_ic.csv | True | 5 | 2026-07-03 01:03:43 |
| minus_imbalance | perf_audit_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/date_ranges/perf_audit.yaml | True | n/a | 2026-07-02 21:34:36 |
| minus_imbalance | return_realization | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/robustness/return_realization.csv | True | 20 | 2026-07-03 01:17:54 |
| minus_imbalance | signal_bucket_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/signal_quality/signal_bucket_metrics.csv | True | 10 | 2026-07-03 00:58:34 |
| minus_imbalance | single_report_html | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/070301_all_fast12_minus_imbalance_l2_full_evaluation_report.html | True | n/a | 2026-07-03 01:18:03 |
| minus_imbalance | topk_robustness | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/robustness/topk_robustness.csv | True | 14 | 2026-07-03 01:18:03 |
| minus_imbalance | train_test_intraday_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_imbalance_l2/research_report/robustness/train_test_intraday_ic.csv | True | 161 | 2026-07-03 01:03:20 |
| minus_quality | adv_liquidity_bucket_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/liquidity_by_adv/adv_liquidity_bucket_metrics.csv | True | 5 | 2026-07-03 01:31:20 |
| minus_quality | best_checkpoint_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/date_ranges/run/checkpoint_metadata/best_checkpoint.yaml | True | n/a | 2026-07-02 19:10:01 |
| minus_quality | checkpoint_selector_table | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/checkpoint_selector_table.csv | True | 11 | 2026-07-03 01:27:52 |
| minus_quality | core_ic_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/core_ic_metrics.csv | True | 2 | 2026-07-03 01:29:11 |
| minus_quality | goodness_of_fit_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/signal_quality/goodness_of_fit_metrics.csv | True | 200 | 2026-07-03 01:29:29 |
| minus_quality | important_pool_cost_sensitivity | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/important_pool/important_pool_test_cost_sensitivity_returns.csv | True | 241,500 | 2026-07-03 01:31:35 |
| minus_quality | important_pool_cumulative_returns | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/important_pool/important_pool_train_val_test_cumulative_returns.csv | True | 71,967 | 2026-07-03 01:28:38 |
| minus_quality | important_pool_pooled_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/important_pool/important_pool_pooled_ic.csv | True | 3 | 2026-07-03 01:27:16 |
| minus_quality | important_pool_prediction_curve | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/important_pool/prediction_real_return_curve.csv | True | 60 | 2026-07-03 01:27:51 |
| minus_quality | important_pool_trade_return_distribution | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/important_pool/important_pool_trade_return_distribution.csv | True | 851 | 2026-07-03 01:31:41 |
| minus_quality | meta_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/date_ranges/artifacts/npz/meta.yaml | True | n/a | 2026-07-02 13:43:33 |
| minus_quality | monthly_ic_rank_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/robustness/monthly_ic_rank_ic.csv | True | 5 | 2026-07-03 01:33:34 |
| minus_quality | perf_audit_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/date_ranges/perf_audit.yaml | True | n/a | 2026-07-03 01:23:26 |
| minus_quality | return_realization | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/robustness/return_realization.csv | True | 20 | 2026-07-03 01:37:35 |
| minus_quality | signal_bucket_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/signal_quality/signal_bucket_metrics.csv | True | 10 | 2026-07-03 01:29:17 |
| minus_quality | single_report_html | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/070301_all_fast12_minus_quality_l2_full_evaluation_report.html | True | n/a | 2026-07-03 01:37:49 |
| minus_quality | topk_robustness | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/robustness/topk_robustness.csv | True | 14 | 2026-07-03 01:37:48 |
| minus_quality | train_test_intraday_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_quality_l2/research_report/robustness/train_test_intraday_ic.csv | True | 161 | 2026-07-03 01:33:14 |
| minus_spread_mid | adv_liquidity_bucket_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/liquidity_by_adv/adv_liquidity_bucket_metrics.csv | True | 5 | 2026-07-03 01:44:19 |
| minus_spread_mid | best_checkpoint_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/date_ranges/run/checkpoint_metadata/best_checkpoint.yaml | True | n/a | 2026-07-03 01:18:26 |
| minus_spread_mid | checkpoint_selector_table | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/checkpoint_selector_table.csv | True | 11 | 2026-07-03 01:41:58 |
| minus_spread_mid | core_ic_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/core_ic_metrics.csv | True | 2 | 2026-07-03 01:42:37 |
| minus_spread_mid | goodness_of_fit_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/signal_quality/goodness_of_fit_metrics.csv | True | 200 | 2026-07-03 01:42:55 |
| minus_spread_mid | important_pool_cost_sensitivity | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/important_pool/important_pool_test_cost_sensitivity_returns.csv | True | 241,500 | 2026-07-03 01:44:26 |
| minus_spread_mid | important_pool_cumulative_returns | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/important_pool/important_pool_train_val_test_cumulative_returns.csv | True | 71,967 | 2026-07-03 01:42:19 |
| minus_spread_mid | important_pool_pooled_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/important_pool/important_pool_pooled_ic.csv | True | 3 | 2026-07-03 01:41:31 |
| minus_spread_mid | important_pool_prediction_curve | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/important_pool/prediction_real_return_curve.csv | True | 60 | 2026-07-03 01:41:58 |
| minus_spread_mid | important_pool_trade_return_distribution | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/important_pool/important_pool_trade_return_distribution.csv | True | 816 | 2026-07-03 01:44:29 |
| minus_spread_mid | meta_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/date_ranges/artifacts/npz/meta.yaml | True | n/a | 2026-07-02 13:42:36 |
| minus_spread_mid | monthly_ic_rank_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/robustness/monthly_ic_rank_ic.csv | True | 5 | 2026-07-03 01:45:34 |
| minus_spread_mid | perf_audit_yaml | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/date_ranges/perf_audit.yaml | True | n/a | 2026-07-03 01:39:33 |
| minus_spread_mid | return_realization | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/robustness/return_realization.csv | True | 20 | 2026-07-03 01:47:31 |
| minus_spread_mid | signal_bucket_metrics | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/signal_quality/signal_bucket_metrics.csv | True | 10 | 2026-07-03 01:42:43 |
| minus_spread_mid | single_report_html | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/070301_all_fast12_minus_spread_mid_l2_full_evaluation_report.html | True | n/a | 2026-07-03 01:47:38 |
| minus_spread_mid | topk_robustness | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/robustness/topk_robustness.csv | True | 14 | 2026-07-03 01:47:38 |
| minus_spread_mid | train_test_intraday_ic | [artifact-root]/nn/l2-features/formal/all_fast12_minus_spread_mid_l2/research_report/robustness/train_test_intraday_ic.csv | True | 161 | 2026-07-03 01:45:16 |

### 7.2. Generated Artifacts

| artifact | path | description |
| --- | --- | --- |
| comparison_report_html | [artifact-root]/nn/l2-features/formal/loo_comparison_report/070312_l2_leave_one_group_out_comparison_report.html | 完整对比报告.  |
| timestamped_report_html | [artifact-root]/nn/l2-features/formal/loo_comparison_report/070312_l2_leave_one_group_out_comparison_report.html | 带 timestamp 的完整对比报告.  |
| repo_report_html | [local-workspace]/exp-nn/l2-features/report/070312_l2_leave_one_group_out_comparison_report.html | repo mirror.  |
| repo_timestamped_report_html | [local-workspace]/exp-nn/l2-features/report/070312_l2_leave_one_group_out_comparison_report.html | 带 timestamp 的 repo mirror.  |
| section_html_root | [artifact-root]/nn/l2-features/formal/loo_comparison_report/section_html | standalone section HTML.  |
| comparison_artifact_root | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts | comparison-only CSV artifacts.  |
| figure_root | [artifact-root]/nn/l2-features/formal/loo_comparison_report/figures | generated comparison figures.  |
| checkpoint_selector_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/checkpoint_selector_comparison.csv | generated CSV artifact |
| core_ic_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/core_ic_comparison.csv | generated CSV artifact |
| experiment_summary | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/experiment_summary.csv | generated CSV artifact |
| goodness_of_fit_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/goodness_of_fit_comparison.csv | generated CSV artifact |
| important_pool_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/important_pool_comparison.csv | generated CSV artifact |
| important_pool_prediction_curve_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/important_pool_prediction_curve_comparison.csv | generated CSV artifact |
| intraday_ic_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/intraday_ic_comparison.csv | generated CSV artifact |
| liquidity_by_adv_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/liquidity_by_adv_comparison.csv | generated CSV artifact |
| monthly_ic_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/monthly_ic_comparison.csv | generated CSV artifact |
| portfolio_cost_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/portfolio_cost_comparison.csv | generated CSV artifact |
| return_realization_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/return_realization_comparison.csv | generated CSV artifact |
| setup_checkpoint_mlflow | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/setup_checkpoint_mlflow.csv | generated CSV artifact |
| setup_data_contract | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/setup_data_contract.csv | generated CSV artifact |
| setup_feature_groups | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/setup_feature_groups.csv | generated CSV artifact |
| signal_bucket_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/signal_bucket_comparison.csv | generated CSV artifact |
| source_artifacts | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/source_artifacts.csv | generated CSV artifact |
| strategy_benchmark_summary | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/strategy_benchmark_summary.csv | generated CSV artifact |
| topk_robustness_comparison | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/topk_robustness_comparison.csv | generated CSV artifact |
| trade_return_distribution_summary | [artifact-root]/nn/l2-features/formal/loo_comparison_report/artifacts/trade_return_distribution_summary.csv | generated CSV artifact |

### Template Provenance

config

[local-workspace]/exp-nn/l2-features/configs/reports/l2_leave_one_group_out_comparison.yaml

template

[local-workspace]/exp-nn/l2-features/docs/reports/l2-leave-one-group-out-comparison-report-outline.md

legacy comparison template

[local-workspace]/exp-nn/l2-features/docs/reports/comparison-report-outline.md

comparison out_root

[artifact-root]/nn/l2-features/formal/loo_comparison_report

generator

[local-workspace]/exp-nn/l2-features/experiments/l2_features/render_ablation_comparison_report.py
