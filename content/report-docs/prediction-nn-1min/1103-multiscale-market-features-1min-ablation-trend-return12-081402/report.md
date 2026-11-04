---
title: Multiscale 特征与 family ablation | multiscale-market-features-1min-ablation-trend-return12-081402
date: 2026-11-03
summary: 修正 mixed-normalization 评估后 full63 test IC/RankIC 为0.061496/0.051659. Matched family ablation 中 relative/liquidity9 为0.098183/0.075886; market16 在训练 gate 停止, 未读取 test.
tags:
- prediction-nn
- registry-sync
- historical-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** 修正 mixed-normalization 评估后 full63 test IC/RankIC 为0.061496/0.051659. Matched family ablation 中 relative/liquidity9 为0.098183/0.075886; market16 在训练 gate 停止, 未读取 test.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

### 1. Executive Summary

benchmark

seed7

current experiment

selected_checkpoint

30,000

checkpoint used for evaluation

train_pooled_ic

0.154549

pooled IC on train report sample

test_pooled_ic

0.096908

corr(all test prediction, all test target)

top_prediction_return_bps

13.1234

mean top-bin prediction return

top95_hit

47.70%

test top 5% prediction label > 0

etf_top95_hit

63.30%

test ETF top 5% prediction label > 0

overfit_variance_ratio

0.026326

test prediction var / label var

model_class

GruMlpRegressor

prediction model

train_range

20210104 -> 20231229 (727 days)

npz split

val_range

20240102 -> 20240229 (37 days)

npz split

test_range

20240301 -> 20241231 (205 days)

npz split

字段解释

| field | explanation |
| --- | --- |
| benchmark | 实验标识.  |
| selected_checkpoint | 最终用于 evaluation 的 checkpoint iteration.  |
| train_pooled_ic | core_ic_summary_train.yaml 当前覆盖的 train-report 样本合并后计算的 Pearson IC; 启用 train report sample 时不是 full-train 指标.  |
| test_pooled_ic | test split 上把所有样本合并后计算的 Pearson IC.  |
| top_prediction_return_bps | 最高 prediction 分组的平均 prediction return, 单位 bps.  |
| top95_hit | test split 中按 prediction 从高到低排序后取最高 5% 样本, 即 prediction >= test prediction 的 95% 分位; 该子样本内 target > 0 的比例.  |
| etf_top95_hit | test split 中先按重要股票池合成 ETF minute-level prediction/real return, 再按 etf_prediction 从高到低排序后取最高 5% 样本; 该子样本内 etf_real_return > 0 的比例.  |
| overfit_variance_ratio | test split 中 prediction 样本方差 / target 样本方差, 用作 overfit 系数; 数值越大表示 prediction 方差相对 label 越高.  |
| model_class | 模型类名.  |
| train_range | 训练集交易日范围.  |
| val_range | 验证集交易日范围.  |
| test_range | 测试集交易日范围.  |

## 研究背景与目标

本报告围绕Multiscale 特征与 family ablation整理原始研究证据. 当前材料对应 registry report `multiscale-market-features-1min-ablation-trend-return12-081402`, 来源SHA256为 `5a4879b07b518f9ee8472684c8b8c2710b79d3daa072ef8487dc8238d2791b29`. 原报告的实验方法, 图表, 结果和解释保留在下文.

## 数据与方法

实验身份为 `multiscale-market-features-1min`. Split, label, sampler, feature与checkpoint定义按原报告记录, 不从其他实验借用缺失字段. 汇总入口见[全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

### 2. Data Pipeline

### 2.1. Data Basics

train_days

727 days

val_days

37 days

test_days

205 days

feature_dim

63

features

ret_1m, ret_5m, ret_2m, ret_3m, ret_10m, hl, oc, log_vol, log_amount, vol_10m, log_vol_5m_mean, log_amount_5m_mean, minute_norm, session_minute_norm, csi300_ret_10m, csi300_ret_60m, csi300_ret_120m, csi300_ret_240m, csi500_ret_10m, csi500_ret_60m, csi500_ret_120m, csi500_ret_240m, csi1000_ret_10m, csi1000_ret_60m, csi1000_ret_120m, csi1000_ret_240m, csi300_rv_60m, csi500_rv_60m, csi1000_rv_60m, market_cs_ret_60m_dispersion, stock_ret_60m_cs_rank, vol_same_minute_60d_pct, amount_same_minute_60d_pct, vol_trailing_5m_pct, vol_trailing_20m_pct, vol_trailing_60m_pct, amount_trailing_5m_pct, amount_trailing_20m_pct, amount_trailing_60m_pct, state_realized_vol_5m, state_realized_vol_20m, state_realized_vol_60m, state_realized_vol_120m, state_realized_vol_240m, state_realized_vol_480m, state_range_5m, state_range_20m, state_range_60m, state_range_120m, state_range_240m, state_range_480m, state_trend_5m, state_trend_20m, state_trend_60m, state_trend_120m, state_trend_240m, state_trend_480m, state_return_5m, state_return_20m, state_return_60m, state_return_120m, state_return_240m, state_return_480m

label_holding_minutes

10

label_exit_offset_minutes

11

label_entry_lag_minutes

1

字段解释

| field | explanation |
| --- | --- |
| features | 模型输入 feature 列表.  |
| feature_dim | 模型输入 feature 维度.  |
| label_holding_minutes | entry 到 exit 的实际持有期, 单位 minutes.  |
| label_exit_offset_minutes | 相对样本时点 t 的 exit 偏移, 单位 minutes.  |
| label_entry_lag_minutes | label entry lag, 单位 minutes.  |

### 2.2. Data Normalization

feature_normalization

pooled_zscore / scope=train_only

label_normalization

pooled_zscore / scope=train_only

label_holding_minutes

10

label_exit_offset_minutes

11

label_entry_lag_minutes

1

train_kept_rate

94.3300%

val_kept_rate

95.4382%

test_kept_rate

95.4104%

max_invalid_ratio

4.1494%

![Data Clean Distribution Overview](images/figure-001.png "Data Clean Distribution Overview")

Data clean stage pooled feature distribution overview.

Invalid Feature Stats

| field | total_count | finite_count | nan_count | nan_ratio | inf_ratio | invalid_ratio | mean_finite | std_finite | skew_finite | kurtosis_finite | min_finite | max_finite |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ret_10m | 1,154,507,748 | 1,106,602,848 | 47,904,900 | 0.041494 | 0.000e+00 | 0.041494 | 1.156e-05 | 0.005543 | 1.6163 | 78.3080 | -1.6727 | 0.865563 |
| ret_5m | 1,154,507,748 | 1,130,555,298 | 23,952,450 | 0.020747 | 0.000e+00 | 0.020747 | 1.144e-05 | 0.004185 | 1.4880 | 125.8855 | -1.6727 | 0.798906 |
| ret_3m | 1,154,507,748 | 1,140,136,278 | 14,371,470 | 0.012448 | 0.000e+00 | 0.012448 | 7.312e-06 | 0.003416 | 1.2200 | 185.0343 | -1.6727 | 0.798906 |
| vol_10m | 1,154,507,748 | 1,144,926,768 | 9,580,980 | 0.008299 | 0.000e+00 | 0.008299 | 5.704e-04 | 5.162e-04 | 16.3785 | 9,073 | 0.000e+00 | 0.617598 |
| ret_2m | 1,154,507,748 | 1,144,926,768 | 9,580,980 | 0.008299 | 0.000e+00 | 0.008299 | 4.388e-06 | 0.002928 | 0.933046 | 267.1997 | -1.6727 | 0.798906 |
| state_trend_480m | 1,154,507,748 | 1,145,880,151 | 8,627,597 | 0.007473 | 0.000e+00 | 0.007473 | -1.708e-04 | 0.048678 | 0.825669 | 12.2462 | -1.4409 | 2.7698 |
| state_realized_vol_480m | 1,154,507,748 | 1,145,880,151 | 8,627,597 | 0.007473 | 0.000e+00 | 0.007473 | 0.047298 | 0.025484 | 3.7558 | 56.4574 | 0.000e+00 | 4.4568 |
| state_return_480m | 1,154,507,748 | 1,145,880,151 | 8,627,597 | 0.007473 | 0.000e+00 | 0.007473 | -1.725e-04 | 0.044855 | 0.789490 | 11.1986 | -3.2540 | 2.2282 |
| state_range_480m | 1,154,507,748 | 1,145,881,986 | 8,625,762 | 0.007471 | 0.000e+00 | 0.007471 | 0.060320 | 0.041866 | 2.6613 | 18.6129 | 0.000e+00 | 4.3267 |
| state_realized_vol_240m | 1,154,507,748 | 1,146,702,411 | 7,805,337 | 0.006761 | 0.000e+00 | 0.006761 | 0.033111 | 0.018812 | 4.3772 | 94.2240 | 0.000e+00 | 4.4489 |
| state_trend_240m | 1,154,507,748 | 1,146,702,411 | 7,805,337 | 0.006761 | 0.000e+00 | 0.006761 | -1.035e-04 | 0.033436 | 0.901790 | 18.6618 | -1.0788 | 2.7436 |
| state_return_240m | 1,154,507,748 | 1,146,702,411 | 7,805,337 | 0.006761 | 0.000e+00 | 0.006761 | -1.028e-04 | 0.030899 | 0.802987 | 14.8048 | -3.3363 | 1.8915 |
| state_range_240m | 1,154,507,748 | 1,146,704,492 | 7,803,256 | 0.006759 | 0.000e+00 | 0.006759 | 0.041697 | 0.029430 | 2.9076 | 31.1754 | 0.000e+00 | 4.3267 |
| state_realized_vol_120m | 1,154,507,748 | 1,147,129,011 | 7,378,737 | 0.006391 | 0.000e+00 | 0.006391 | 0.022659 | 0.014601 | 4.8702 | 130.1542 | 0.000e+00 | 4.4078 |
| state_trend_120m | 1,154,507,748 | 1,147,129,011 | 7,378,737 | 0.006391 | 0.000e+00 | 0.006391 | -5.497e-05 | 0.023507 | 1.1668 | 34.7462 | -1.1401 | 2.7261 |
| state_return_120m | 1,154,507,748 | 1,147,129,011 | 7,378,737 | 0.006391 | 0.000e+00 | 0.006391 | -5.460e-05 | 0.021642 | 0.992154 | 26.8210 | -3.3951 | 1.9106 |
| state_range_120m | 1,154,507,748 | 1,147,131,092 | 7,376,656 | 0.006389 | 0.000e+00 | 0.006389 | 0.028234 | 0.022304 | 3.3597 | 44.6815 | 0.000e+00 | 4.3267 |
| state_realized_vol_60m | 1,154,507,748 | 1,147,342,311 | 7,165,437 | 0.006206 | 0.000e+00 | 0.006206 | 0.015417 | 0.011231 | 5.6205 | 192.4926 | 0.000e+00 | 4.4038 |
| stock_ret_60m_cs_rank | 1,154,507,748 | 1,147,342,311 | 7,165,437 | 0.006206 | 0.000e+00 | 0.006206 | 0.500102 | 0.288583 | -7.133e-05 | -1.1987 | 1.862e-04 | 1.0000 |
| state_trend_60m | 1,154,507,748 | 1,147,342,311 | 7,165,437 | 0.006206 | 0.000e+00 | 0.006206 | -2.801e-05 | 0.016644 | 1.5965 | 64.7632 | -1.1703 | 2.6991 |
| state_return_60m | 1,154,507,748 | 1,147,342,311 | 7,165,437 | 0.006206 | 0.000e+00 | 0.006206 | -2.807e-05 | 0.015402 | 1.3202 | 50.5849 | -3.5243 | 1.8384 |
| state_range_60m | 1,154,507,748 | 1,147,344,392 | 7,163,356 | 0.006205 | 0.000e+00 | 0.006205 | 0.019035 | 0.016810 | 4.0298 | 66.2231 | 0.000e+00 | 4.3267 |
| state_return_20m | 1,154,507,748 | 1,147,484,511 | 7,023,237 | 0.006083 | 0.000e+00 | 0.006083 | -9.326e-06 | 0.009067 | 1.8585 | 143.5154 | -3.3363 | 1.8334 |
| state_realized_vol_20m | 1,154,507,748 | 1,147,484,511 | 7,023,237 | 0.006083 | 0.000e+00 | 0.006083 | 0.008391 | 0.007146 | 7.5579 | 457.2699 | 0.000e+00 | 4.3919 |
| state_trend_20m | 1,154,507,748 | 1,147,484,511 | 7,023,237 | 0.006083 | 0.000e+00 | 0.006083 | -9.306e-06 | 0.009637 | 2.2141 | 167.1458 | -1.3879 | 2.6150 |
| state_range_20m | 1,154,507,748 | 1,147,486,592 | 7,021,156 | 0.006082 | 0.000e+00 | 0.006082 | 0.010356 | 0.010229 | 5.4750 | 153.4727 | 0.000e+00 | 4.3267 |
| state_trend_5m | 1,154,507,748 | 1,147,537,841 | 6,969,907 | 0.006037 | 0.000e+00 | 0.006037 | -2.417e-06 | 0.004903 | 2.3417 | 595.7968 | -3.0905 | 2.3547 |
| state_return_5m | 1,154,507,748 | 1,147,537,841 | 6,969,907 | 0.006037 | 0.000e+00 | 0.006037 | -2.415e-06 | 0.004819 | 1.6681 | 988.4079 | -4.3267 | 1.8334 |
| state_realized_vol_5m | 1,154,507,748 | 1,147,537,841 | 6,969,907 | 0.006037 | 0.000e+00 | 0.006037 | 0.003817 | 0.003982 | 11.5091 | 2,100 | 0.000e+00 | 4.3267 |
| state_range_5m | 1,154,507,748 | 1,147,539,923 | 6,967,825 | 0.006035 | 0.000e+00 | 0.006035 | 0.004887 | 0.005183 | 8.1373 | 795.7123 | 0.000e+00 | 4.3267 |
| amount_same_minute_60d_pct | 1,154,507,748 | 1,147,653,949 | 6,853,799 | 0.005937 | 0.000e+00 | 0.005937 | 0.497584 | 0.299023 | 0.023598 | -1.2295 | 0.000e+00 | 1.0000 |
| vol_same_minute_60d_pct | 1,154,507,748 | 1,147,653,949 | 6,853,799 | 0.005937 | 0.000e+00 | 0.005937 | 0.500500 | 0.297900 | 0.010469 | -1.2244 | 0.000e+00 | 1.0000 |
| ret_1m | 1,154,507,748 | 1,149,717,258 | 4,790,490 | 0.004149 | 0.000e+00 | 0.004149 | 1.353e-06 | 0.002284 | 0.332178 | 524.6048 | -1.6727 | 0.759663 |
| vol_trailing_60m_pct | 1,154,507,748 | 1,154,394,888 | 112,860 | 9.776e-05 | 0.000e+00 | 9.776e-05 | 0.492990 | 0.304162 | 0.040254 | -1.2615 | 0.000e+00 | 1.0000 |
| amount_trailing_60m_pct | 1,154,507,748 | 1,154,394,888 | 112,860 | 9.776e-05 | 0.000e+00 | 9.776e-05 | 0.492823 | 0.304257 | 0.040368 | -1.2616 | 0.000e+00 | 1.0000 |
| vol_trailing_20m_pct | 1,154,507,748 | 1,154,470,128 | 37,620 | 3.259e-05 | 0.000e+00 | 3.259e-05 | 0.493187 | 0.309097 | 0.038864 | -1.2381 | 0.000e+00 | 1.0000 |
| amount_trailing_20m_pct | 1,154,507,748 | 1,154,470,128 | 37,620 | 3.259e-05 | 0.000e+00 | 3.259e-05 | 0.493058 | 0.309245 | 0.038454 | -1.2381 | 0.000e+00 | 1.0000 |
| amount_trailing_5m_pct | 1,154,507,748 | 1,154,498,343 | 9,405 | 8.146e-06 | 0.000e+00 | 8.146e-06 | 0.493761 | 0.343533 | 0.038037 | -1.2806 | 0.000e+00 | 1.0000 |
| vol_trailing_5m_pct | 1,154,507,748 | 1,154,498,343 | 9,405 | 8.146e-06 | 0.000e+00 | 8.146e-06 | 0.493844 | 0.343189 | 0.039355 | -1.2805 | 0.000e+00 | 1.0000 |
| log_amount_5m_mean | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 11.4836 | 2.7379 | -1.6409 | 4.0784 | 0.000e+00 | 21.9334 |
| csi300_ret_10m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -1.478e-05 | 0.002313 | 3.8863 | 155.4279 | -0.048251 | 0.103755 |
| session_minute_norm | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.493776 | 0.289824 | 5.194e-04 | -1.2009 | 0.000e+00 | 0.991667 |
| minute_norm | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.500000 | 0.289875 | -1.373e-07 | -1.2000 | 0.000e+00 | 1.0000 |
| log_vol | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 9.0413 | 2.8688 | -1.6155 | 3.2278 | 0.000e+00 | 20.3408 |
| log_vol_5m_mean | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 9.0800 | 2.3960 | -1.1786 | 2.3900 | 0.000e+00 | 20.1280 |
| log_amount | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 11.4358 | 3.3520 | -2.1437 | 5.1304 | 0.000e+00 | 22.6198 |
| csi300_ret_120m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -1.727e-04 | 0.007806 | 0.828607 | 9.0171 | -0.074354 | 0.119413 |
| oc | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 4.718e-06 | 7.159e-04 | 0.807232 | 305.3296 | -0.312980 | 0.353188 |
| hl | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 6.217e-04 | 7.591e-04 | 6.6258 | 384.2352 | 0.000e+00 | 0.434688 |
| csi300_ret_60m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -8.761e-05 | 0.005515 | 1.1950 | 18.5202 | -0.067646 | 0.101166 |
| market_cs_ret_60m_dispersion | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.012717 | 0.005468 | 1.3443 | 2.5501 | 0.004631 | 0.056040 |
| csi300_ret_240m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -3.412e-04 | 0.011430 | 0.978299 | 8.0478 | -0.086401 | 0.137105 |
| csi500_ret_10m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -1.272e-05 | 0.002477 | 3.9748 | 154.2897 | -0.050518 | 0.112549 |
| csi500_ret_60m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -7.537e-05 | 0.006123 | 1.3528 | 19.9641 | -0.069577 | 0.109966 |
| csi500_ret_240m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -2.902e-04 | 0.012961 | 1.1169 | 10.3339 | -0.085051 | 0.153507 |
| csi1000_ret_10m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -1.645e-05 | 0.002769 | 3.2529 | 126.3830 | -0.051145 | 0.120919 |
| csi1000_ret_60m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -9.754e-05 | 0.006981 | 0.865910 | 17.1892 | -0.078297 | 0.116933 |
| csi1000_ret_120m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -1.927e-04 | 0.010015 | 0.498933 | 9.0144 | -0.081850 | 0.133210 |
| csi1000_ret_240m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -3.773e-04 | 0.014963 | 0.596401 | 8.2321 | -0.120203 | 0.165821 |
| csi300_rv_60m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.004328 | 0.003258 | 10.8424 | 257.2810 | 9.309e-04 | 0.102853 |
| csi500_rv_60m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.004559 | 0.003445 | 11.2045 | 276.6439 | 0.001017 | 0.110987 |
| csi1000_rv_60m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | 0.004822 | 0.003732 | 10.6276 | 263.1252 | 7.997e-04 | 0.119361 |
| csi500_ret_120m | 1,154,507,748 | 1,154,507,748 | 0 | 0.000e+00 | 0.000e+00 | 0.000e+00 | -1.484e-04 | 0.008732 | 0.904930 | 10.5283 | -0.074420 | 0.124283 |

字段解释

| field | explanation |
| --- | --- |
| feature_normalization | feature normalization 方法和 fit scope.  |
| label_normalization | label normalization 方法和 fit scope.  |
| kept_rate | 清洗后保留样本数 / 清洗前样本数.  |
| max_invalid_ratio | 单个字段中 invalid 样本占比的最大值.  |

### 2.3. Label Distribution

![Label Distribution By Split](images/figure-002.png "Label Distribution By Split")

Normalized label distributions for train/val/test using train-only fit parameters; the table reports raw log-return moments after inverse transformation.

| split | count | mean_raw_bps | std_raw_bps | zero_ratio | abs_raw_gt_1pct_ratio |
| --- | --- | --- | --- | --- | --- |
| train | 553,898,121 | -0.074716 | 42.2281 | 0.186762 | 0.028168 |
| val | 31,737,447 | -0.863159 | 62.4642 | 0.147426 | 0.076608 |
| test | 176,134,322 | -0.035505 | 50.2074 | 0.174398 | 0.039702 |

字段解释

| field | explanation |
| --- | --- |
| label_distribution | train-only z-score 参数下的 train/val/test 标签分布; 图中使用标准化标签, 表格同时报告还原后的收益率 bps.  |

## 主要结果

| 记录项 | 当前解释 |
| --- | --- |
| 实验 | multiscale-market-features-1min |
| 报告类型 | full_report_html |
| 历史状态 | 历史成功 |
| 证据 | multiscale-market-features-1min-ablation-trend-return12-081402 |

训练监控, 信号质量, 交易成本与稳健性评估. 

生成日期: 2026-08-14

### 3. Evaluation

### 3.1. IC Summary

| split | pooled_ic | pooled_rank_ic | count |
| --- | --- | --- | --- |
| train | 0.154549 | 0.137121 | 31,875,072 |
| test | 0.096908 | 0.067951 | 176,134,322 |

![Checkpoint Train/Test Pooled IC](images/figure-003.png "Checkpoint Train/Test Pooled IC")

Validation checkpoint pooled IC with selected train/test pooled IC references.

### core_ic_metrics.csv

| split | pooled_ic | pooled_rank_ic | count |
| --- | --- | --- | --- |
| train | 0.154549 | 0.137121 | 31,875,072 |
| test | 0.096908 | 0.067951 | 176,134,322 |

字段解释

| field | explanation |
| --- | --- |
| pooled_ic | 合并样本后计算的 Pearson IC.  |
| pooled_rank_ic | 合并样本后计算的 Rank IC.  |
| pearson_ic | corr(prediction, target).  |
| rank_ic | corr(rank(prediction), rank(target)).  |

### 3.2. Signal Quality 1: bucket (10)

字段解释

| field | explanation |
| --- | --- |
| signal_bucket | 按 prediction 从低到高切分的分组编号.  |
| mean_prediction | 分组内 prediction 均值.  |
| mean_label_bps | 分组内 target 均值, 单位 bps.  |
| t_stat | 分组 mean_label_bps 相对 0 的 t-stat.  |
| hit_rate | 分组内 target > 0 的比例.  |
| top_bottom_signal_spread_bps | Top bucket 平均 target return 减 bottom bucket 平均 target return, 单位 bps.  |
| Daily top-minus-bottom signal spread | 每天内部按 prediction 排序, 用 ntile(10) 分 bucket. 对每天的 top decile 和 bottom decile 计算 realized return.  |

| signal_bucket | mean_prediction | mean_label_bps | t_stat | hit_rate | row_count | top_bottom_signal_spread_bps |
| --- | --- | --- | --- | --- | --- | --- |
| 1.0000 | -0.001408 | -6.9298 | -395.4074 | 0.359548 | 17,613,433 | 15.0124 |
| 2.0000 | -4.665e-04 | -2.2928 | -201.8669 | 0.371114 | 17,613,433 | 15.0124 |
| 3.0000 | -2.722e-04 | -1.4767 | -145.3750 | 0.373064 | 17,613,432 | 15.0124 |
| 4.0000 | -1.486e-04 | -0.972934 | -102.3353 | 0.371665 | 17,613,432 | 15.0124 |
| 5.0000 | -5.420e-05 | -0.562600 | -61.9606 | 0.367889 | 17,613,432 | 15.0124 |
| 6.0000 | 3.104e-05 | -0.181883 | -19.9374 | 0.374887 | 17,613,432 | 15.0124 |
| 7.0000 | 1.260e-04 | 0.323297 | 33.8106 | 0.390409 | 17,613,432 | 15.0124 |
| 8.0000 | 2.490e-04 | 1.1203 | 109.6588 | 0.403904 | 17,613,432 | 15.0124 |
| 9.0000 | 4.503e-04 | 2.5341 | 221.1233 | 0.423317 | 17,613,432 | 15.0124 |
| 10.0000 | 0.001268 | 8.0825 | 465.5526 | 0.461312 | 17,613,432 | 15.0124 |

![Daily Top-Minus-Bottom Signal Spread](images/figure-004.png "Daily Top-Minus-Bottom Signal Spread")

Daily top decile target return minus bottom decile target return on the test split.

### 3.3. Signal Quality 2: Important Stock Pool

prediction != 0 metrics dataset

test split, [artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/date_ranges/run/eval_test/iter_30000/predict_manifest.yaml

checkpoint IC dataset

val split checkpoints, [artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/date_ranges/run/eval_val

cumulative return dataset

train + val + test, shown in 5. Trading And Cost

### prediction != 0 metrics

| pool | etf_code | pearson_ic | rank_ic | mean_prediction_return | mean_real_return | prediction_positive_ratio | real_return_positive_ratio | count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000 ETF | 512100.SH | 0.076880 | 0.046561 | -9.674e-06 | -8.214e-06 | 0.481814 | 0.395829 | 32,953,526 |
| 沪深300 ETF(沪) | 510300.SH | 0.077675 | 0.043727 | 9.894e-06 | 1.427e-05 | 0.488372 | 0.413562 | 9,884,956 |
| 中证500 ETF(沪) | 510500.SH | 0.068164 | 0.042623 | 4.554e-06 | -1.311e-05 | 0.489186 | 0.393434 | 16,487,993 |

![Prediction Return vs Real Return](images/figure-005.png "Prediction Return vs Real Return")

Important-pool mean prediction return and real return by prediction rank bin.

![Important Pool Checkpoint IC](images/figure-006.png "Important Pool Checkpoint IC")

Checkpoint IC for CSI500 and CSI300 important pools.

字段解释

| field | explanation |
| --- | --- |
| prediction != 0 metrics | 按 date, code join prediction rows, 过滤 isfinite(prediction), isfinite(target), prediction != 0. 按 pool 聚合各项指标.  |
| Prediction Return vs Real Return 图 | 每个 pool 内按 prediction 排序, 用 ntile(20) 分 prediction_bin, 单位显示为 bps.  |
| pearson_ic | corr(prediction, target).  |
| rank_ic | corr(rank(prediction), rank(target)).  |
| mean_prediction_return | prediction 的样本均值.  |
| mean_real_return | target 的样本均值.  |
| real_return_positive_ratio | target > 0 的样本占比.  |
| prediction_positive_ratio | prediction > 0 的样本占比.  |

### 3.4. Goodness Of Fit

![Train/Test Goodness Of Fit](images/figure-007.png "Train/Test Goodness Of Fit")

Train/test are separately sorted by prediction and cut into 100 equal-frequency bins; x is bin mean prediction, y is label, and transparent bands show the p5-p95 target range within each prediction bin.

### goodness_of_fit_metrics.csv edge bins

| split | prediction_bin | mean_prediction | mean_label | label_p05 | label_p95 | row_count |
| --- | --- | --- | --- | --- | --- | --- |
| train | 1 | -0.004652 | -0.004880 | -0.016129 | 0.004787 | 5,538,982 |
| train | 2 | -0.002193 | -0.002288 | -0.011375 | 0.006802 | 5,538,982 |
| train | 3 | -0.001540 | -0.001599 | -0.009834 | 0.006855 | 5,538,982 |
| train | 4 | -0.001213 | -0.001252 | -0.008888 | 0.006691 | 5,538,982 |
| train | 5 | -9.998e-04 | -0.001044 | -0.008286 | 0.006516 | 5,538,982 |
| train | 96 | 9.468e-04 | 9.524e-04 | -0.006504 | 0.008949 | 5,538,981 |
| train | 97 | 0.001110 | 0.001130 | -0.006760 | 0.009590 | 5,538,981 |
| train | 98 | 0.001372 | 0.001413 | -0.007099 | 0.010529 | 5,538,981 |
| train | 99 | 0.001912 | 0.002008 | -0.007435 | 0.011993 | 5,538,981 |
| train | 100 | 0.004536 | 0.004973 | -0.005856 | 0.017075 | 5,538,981 |
| test | 1 | -0.004141 | -0.002278 | -0.020920 | 0.015602 | 1,761,344 |
| test | 2 | -0.002064 | -9.828e-04 | -0.012825 | 0.011322 | 1,761,344 |
| test | 3 | -0.001567 | -7.252e-04 | -0.010872 | 0.009819 | 1,761,344 |
| test | 4 | -0.001292 | -5.949e-04 | -0.009842 | 0.009003 | 1,761,344 |
| test | 5 | -0.001102 | -5.012e-04 | -0.009178 | 0.008530 | 1,761,344 |
| test | 96 | 0.001019 | 6.504e-04 | -0.007732 | 0.009796 | 1,761,343 |
| test | 97 | 0.001167 | 7.426e-04 | -0.008156 | 0.010536 | 1,761,343 |
| test | 98 | 0.001388 | 8.731e-04 | -0.008797 | 0.011650 | 1,761,343 |
| test | 99 | 0.001793 | 0.001075 | -0.010010 | 0.013748 | 1,761,343 |
| test | 100 | 0.003501 | 0.002381 | -0.014008 | 0.023575 | 1,761,343 |

字段解释

| field | explanation |
| --- | --- |
| Goodness Of Fit | 按 split 全局对 prediction 从低到高排序并切成 100 个等频分段, 检查每段 mean_prediction 与 mean_label 是否接近.  |
| prediction_bin | 按 prediction 从低到高排序后的等频分段编号, 1 为最低 prediction 段.  |
| mean_prediction | 分组内 prediction 均值.  |
| mean_label | 分组内 target 均值, 保持原始 target 单位.  |
| label_std | 分组内 target 的样本标准差.  |
| label_se | 分组 mean_label 的标准误, 计算为 label_std / sqrt(row_count).  |
| label_p05 | 分组内 target 的 5% 分位, 用作中间 90% 散点位置阴影下界.  |
| label_p95 | 分组内 target 的 95% 分位, 用作中间 90% 散点位置阴影上界.  |
| label_ci90_low | mean_label 的 90% 正态近似置信区间下界, mean_label - 1.64485 * label_se.  |
| label_ci90_high | mean_label 的 90% 正态近似置信区间上界, mean_label + 1.64485 * label_se.  |
| row_count | 分组内有限 prediction/target 样本数.  |

### 3.5. Liquidity By ADV

ADV uses a shifted 20-trading-day mean of stock1d amount. Buckets are formed globally over the full test-universe date-code pool, not within each date. The current day's full daily_amount is not used to bucket current-day predictions.

![ADV Liquidity Bucket Metrics](images/figure-008.png "ADV Liquidity Bucket Metrics")

Left: Pearson IC and Rank IC by date-level ADV bucket. Right: prediction top 5% target return by ADV bucket.

### adv_liquidity_bucket_metrics.csv

| adv_bucket | bucket_label | row_count | day_count | mean_adv_amount | median_adv_amount | mean_ic | mean_rank_ic | icir | rank_icir | top5_return_bps | top5_hit_rate | top5_row_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Bottom20% | 33,579,609 | 205 | 22,043 | 22,558 | 0.081276 | 0.064153 | 3.5675 | 3.5172 | 6.2422 | 0.418181 | 1,694,847 |
| 2 | 20~40% | 33,579,609 | 205 | 49,378 | 48,887 | 0.056861 | 0.039904 | 2.8722 | 2.2887 | 3.8808 | 0.415578 | 1,695,008 |
| 3 | 40~60% | 33,579,609 | 205 | 89,103 | 87,560 | 0.066884 | 0.040846 | 2.9303 | 2.1662 | 4.4442 | 0.427436 | 1,694,203 |
| 4 | 60~80% | 33,579,448 | 205 | 170,680 | 165,081 | 0.079698 | 0.046906 | 3.1722 | 2.0686 | 5.6881 | 0.444935 | 1,695,008 |
| 5 | Top20% | 33,579,448 | 205 | 714,122 | 442,449 | 0.094985 | 0.056146 | 3.0283 | 2.0386 | 7.1444 | 0.459892 | 1,695,008 |

字段解释

| field | explanation |
| --- | --- |
| Liquidity By ADV | 按完整 test universe 的 date-code 样本池, 用 shifted/trailing ADV 全局分五桶, 检查不同流动性股票上的 IC 与 prediction top 5% return.  |
| adv_bucket | 按完整 test universe date-code 样本池的 adv_amount 排序后的全局五分桶编号; 1 为 Bottom20%, 5 为 Top20%.  |
| bucket_label | ADV 五分桶可读标签.  |
| row_count | 分组内有限 prediction/target 样本数.  |
| day_count | 入选样本覆盖的交易日数量.  |
| mean_adv_amount | 当前 ADV 桶内 date-code 层面的平均 shifted/trailing ADV.  |
| median_adv_amount | 当前 ADV 桶内 date-code 层面的中位 shifted/trailing ADV.  |
| mean_ic | 当前 ADV 桶内先按 date,time 横截面计算 Pearson IC, 再按 date 聚合后的均值.  |
| mean_rank_ic | 当前 ADV 桶内先按 date,time 横截面计算 Rank IC, 再按 date 聚合后的均值.  |
| icir | 当前 ADV 桶 daily IC 的 mean/std.  |
| rank_icir | 当前 ADV 桶 daily Rank IC 的 mean/std.  |
| top5_return_bps | 当前 ADV 桶内每个 date,time 截面 prediction 最高 5% 样本的平均 target return, 单位 bps.  |
| top5_hit_rate | 当前 ADV 桶内 prediction 最高 5% 样本 target > 0 的比例.  |
| top5_row_count | 当前 ADV 桶内进入 prediction top 5% return 统计的样本数.  |

### 4. Train Metrics

### 4.1. Checkpoint Selection

| key | value |
| --- | --- |
| best_iter | 30,000 |
| selection_metric | checkpoint_selection/score |
| selection_rule | early_top_k |
| selection_value | 0.080076 |
| candidate_count | 8 |

checkpoint_selector_table.csv

| iter | selected | val/objective/mse | val/quality/global_ic | val/quality/rank_ic | val/dist/pred_std_over_target_std | decision | metric_rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | False | 3.901e-05 | 0.032833 | 0.035354 | nan | reject | 8.0000 |
| 10,000 | False | 3.836e-05 | 0.134721 | 0.093353 | nan | reject | 1.0000 |
| 20,000 | False | 3.857e-05 | 0.119452 | 0.084856 | nan | reject | 2.0000 |
| 30,000 | True | 3.867e-05 | 0.114592 | 0.085865 | nan | promote | 3.0000 |
| 40,000 | False | 3.893e-05 | 0.114465 | 0.082797 | nan | reject | 4.0000 |
| 50,000 | False | 3.943e-05 | 0.094365 | 0.073442 | nan | reject | 5.0000 |
| 60,000 | False | 3.956e-05 | 0.090565 | 0.071552 | nan | reject | 6.0000 |
| 67,615 | False | 3.959e-05 | 0.088950 | 0.071513 | nan | reject | 7.0000 |

![Checkpoint Selection Metrics](images/figure-009.png "Checkpoint Selection Metrics")

Validation objective and IC metrics by checkpoint iteration.

![Fixed-Sample Train Global IC By Checkpoint](images/figure-010.png "Fixed-Sample Train Global IC By Checkpoint")

Every checkpoint is evaluated on the same deterministic 3,891-batch / 31,875,072-row train sample.

| iter | pooled_ic | pooled_rank_ic | count | scope |
| --- | --- | --- | --- | --- |
| 0 | 0.003439 | -0.002850 | 31,875,072 | fixed train sample: 3891 batches |
| 10,000 | 0.115377 | 0.109670 | 31,875,072 | fixed train sample: 3891 batches |
| 20,000 | 0.133872 | 0.124369 | 31,875,072 | fixed train sample: 3891 batches |
| 30,000 | 0.154555 | 0.137121 | 31,875,072 | fixed train sample: 3891 batches |
| 40,000 | 0.169269 | 0.149478 | 31,875,072 | fixed train sample: 3891 batches |
| 50,000 | 0.187389 | 0.159193 | 31,875,072 | fixed train sample: 3891 batches |
| 60,000 | 0.198039 | 0.164250 | 31,875,072 | fixed train sample: 3891 batches |
| 67,615 | 0.198039 | 0.164250 | 31,875,072 | fixed train sample: 3891 batches |

字段解释

| field | explanation |
| --- | --- |
| train_checkpoint_sample_ic | 每个 checkpoint 在同一固定 3,891-batch 训练样本上的 pooled Pearson/Rank IC; 不是 full-train 指标.  |

### 4.2. Model And Method

### Model

model_class

GruMlpRegressor

model class

trainable_parameter

1,864,577

trainable parameter count

input_tensor

batch, window, 63

GRU input

prediction_target

log_close[t+11] - log_close[t+1]

raw target

label_holding_minutes

10

entry-to-exit holding period

label_exit_offset_minutes

11

exit offset from t

label_entry_lag_minutes

1

entry lag

gru_hidden_size

384

GRU hidden size

gru_num_layers

2

GRU layers

gru_bidirectional

False

GRU direction

gru_dropout

0.0

GRU dropout

mlp_effective_hidden_width

512

MLP effective hidden width

mlp_dropout

0.0

MLP dropout

optimizer

AdamW

optimizer

learning_rate

0.001000

base LR

lr_scheduler/type

LinearWarmup + CosineAnnealing

qmodel scheduler

approx_total_epochs

0.443692

through selected checkpoint

### 4.2.1. GRU

| field | value |
| --- | --- |
| input_tensor | batch, window, 63 |
| gru_hidden_size | 384 |
| gru_num_layers | 2 |
| gru_bidirectional | False |
| gru_dropout | 0.0 |

### 4.2.2. MLP

| field | value |
| --- | --- |
| mlp_effective_hidden_width | 512 |
| mlp_dropout | 0.0 |

### 4.2.3. Method

| field | value |
| --- | --- |
| parameter_initialization | PyTorch default GRU and Linear initialization |
| lr_scheduler/type | LinearWarmup + CosineAnnealing |
| optimizer | AdamW |
| approx_total_epochs | 0.443692 |
| final_iter | 67,615 |
| checkpoint_selection | early_top_k checkpoint_selection/score |

字段解释

| field | explanation |
| --- | --- |
| model_class | 模型类名.  |
| trainable_parameter | 可训练参数数量.  |
| gru_bidirectional | GRU 是否使用 bidirectional 结构.  |
| parameter_initialization | 模型参数初始化方式.  |
| selected_checkpoint | 最终用于 evaluation 的 checkpoint iteration.  |

### 4.3. Training Monitoring

![Train Loss](images/figure-011.png "Train Loss")

Train loss with step=0 and the top 10% loss outliers removed, log y-axis, and a rolling mean smoothing curve.

![Train Monitoring Curves](images/figure-012.png "Train Monitoring Curves")

MLflow-backed train diagnostics plus local validation scalar curves for loss, LR, batch composition, IC, and prediction scale; grad norm retains every positive observation without p99 clipping and uses a log y-axis.

字段解释

| field | explanation |
| --- | --- |
| Train loss | 读取 TensorBoard scalar parquet, 过滤 step > 0, 删除最高 10% loss outlier, 用 rolling(window=200, min_periods=20, center=True) 计算 smoothed_loss, y-axis 使用 log scale.  |
| train/objective/loss_mean | MLflow 中记录的 train objective loss rolling mean.  |
| train/optim/lr | MLflow 中记录的 optimizer learning rate.  |
| train/norm/grad/global | MLflow 中记录的所有可训练参数梯度拼接后的 L2 norm; 监控图保留全部正值观测, 不做 p99 截断, 并使用 log y-axis 展示.  |
| train/batch/unique_dates | MLflow 中记录的一个 batch 内覆盖的不同交易日数量.  |
| train/batch/top_date_share | MLflow 中记录的一个 batch 内样本最多交易日的样本占比.  |
| val/objective/mse | validation split 上的 objective MSE.  |
| val/quality/global_ic | validation split 上的 global Pearson IC.  |
| val/quality/rank_ic | validation split 上的 rank IC.  |
| val/dist/pred_std_over_target_std | validation prediction std / target std.  |

### 5. Trading And Cost

### 5.0. Cost Model Status

Cost model artifact status

status

pending real cost artifact

available_metric

simple ETF prediction-threshold long/flat compound backtest by important stock pool

### 5.1. Cumulative Prediction, Real, And Excess Returns

![Important Pool Train-Val-Test Compound Backtest](images/figure-013.png "Important Pool Train-Val-Test Compound Backtest")

Benchmark is continuous full-hold ETF real return; strategy uses the 4800-minute trailing 95% ETF prediction threshold and 5-minute trading rule; excess line is strategy real % minus benchmark full-hold real %.

| pool | days | final_cum_prediction_bps | final_cum_real_bps | final_benchmark_real_bps | final_cum_excess_bps | 平均每天开仓次数 | 平均每天return_bps | 平均每次开仓return_bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000 ETF | 969 | 38,826 | 125,768 | -9,468 | 2,542,784 | 0.954592 | 27.3973 | 28.5060 |
| 沪深300 ETF(沪) | 969 | 23,142 | 64,186 | -4,615 | 127,772 | 0.979360 | 21.0041 | 21.3282 |
| 中证500 ETF(沪) | 969 | 33,400 | 92,697 | -8,487 | 668,792 | 0.974200 | 24.4583 | 24.9448 |

### Backtest risk/trading metrics

| pool | max_drawdown_pct | exposure_ratio | win_rate_by_trade | avg_holding_minutes |
| --- | --- | --- | --- | --- |
| 1000 ETF | -5.1287 | 0.049613 | 0.779459 | 8.3676 |
| 沪深300 ETF(沪) | -3.7854 | 0.049164 | 0.724974 | 8.0822 |
| 中证500 ETF(沪) | -4.1327 | 0.050221 | 0.738347 | 8.2998 |

### Test-only backtest metrics

| pool | test_days | test_cum_strategy_bps | test_cum_benchmark_bps | test_excess_bps | max_drawdown_pct | exposure_ratio | win_rate_by_trade | avg_holding_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000 ETF | 205 | 2,819 | -3,172 | 8,773 | -4.5010 | 0.047144 | 0.629442 | 7.8985 |
| 沪深300 ETF(沪) | 205 | 3,214 | 5,005 | -1,193 | -3.7854 | 0.050932 | 0.616438 | 7.6758 |
| 中证500 ETF(沪) | 205 | 2,646 | -4,043 | 11,230 | -4.1327 | 0.051841 | 0.574163 | 8.1866 |

字段解释

| field | explanation |
| --- | --- |
| model | benchmark 为 ETF 每分钟一直满仓持有得到 real return; strategy 按 pool 合成分钟级 ETF prediction, 用过去 4800 分钟的 95% 分位做开仓阈值, 每 5 分钟开平仓并复利交易.  |
| strategy real % | 按 5 分钟开平仓规则, 用真实 etf_real_return 复利得到的策略实际收益.  |
| benchmark full-hold real % | 不做择时, ETF/pool 每分钟一直满仓持有, 用 etf_real_return 连续复利得到的 benchmark 收益.  |
| strategy - benchmark % | strategy real % - benchmark full-hold real %.  |
| max_drawdown_pct | strategy_nav 相对历史高点的最大回撤, 单位 %.  |
| exposure_ratio | position > 0 的分钟数 / 总分钟数.  |
| win_rate_by_trade | 按 trade_id 聚合每次开仓复利收益, 收益大于 0 的比例.  |
| avg_holding_minutes | 每个 trade_id 覆盖的分钟数均值.  |
| test_cum_strategy_bps | test split 内 strategy_minute_return 从 1 重新复利后的累计收益, 单位 bps.  |
| test_cum_benchmark_bps | test split 内 benchmark_minute_return 从 1 重新复利后的累计收益, 单位 bps.  |
| test_excess_bps | (1 + test_cum_strategy_return) / (1 + test_cum_benchmark_return) - 1, 单位 bps.  |

### 5.2. Single-Side Cost Sensitivity

![Train-Val-Test Net Strategy Cost Sensitivity](images/figure-014.png "Train-Val-Test Net Strategy Cost Sensitivity")

train, val, and test shown on the same axis as 5.1; trading rule is the same as 5.1; cost is deducted as abs(position - prev_position) * single-side cost bps / 10000.

### Test-only cost model metrics

| pool | single_side_cost_bps | test_days | test_cum_net_strategy_bps | test_cum_benchmark_bps | test_net_excess_bps | total_turnover | total_cost_bps | max_drawdown_pct | exposure_ratio | win_rate_by_trade | avg_holding_minutes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000 ETF | 0.000e+00 | 205 | 2,819 | -3,172 | 8,773 | 393.0000 | 0.000e+00 | -4.5010 | 0.047144 | 0.629442 | 7.8985 |
| 1000 ETF | 1.0000 | 205 | 2,325 | -3,172 | 8,050 | 393.0000 | 393.0000 | -4.5488 | 0.047144 | 0.598985 | 7.8985 |
| 1000 ETF | 2.0000 | 205 | 1,850 | -3,172 | 7,354 | 393.0000 | 786.0000 | -4.5966 | 0.047144 | 0.558376 | 7.8985 |
| 1000 ETF | 5.0000 | 205 | 532.0659 | -3,172 | 5,424 | 393.0000 | 1,965 | -10.4857 | 0.047144 | 0.421320 | 7.8985 |
| 1000 ETF | 10.0000 | 205 | -1,348 | -3,172 | 2,671 | 393.0000 | 3,930 | -21.2086 | 0.047144 | 0.258883 | 7.8985 |
| 沪深300 ETF(沪) | 0.000e+00 | 205 | 3,214 | 5,005 | -1,193 | 437.0000 | 0.000e+00 | -3.7854 | 0.050932 | 0.616438 | 7.6758 |
| 沪深300 ETF(沪) | 1.0000 | 205 | 2,649 | 5,005 | -1,570 | 437.0000 | 437.0000 | -3.8528 | 0.050932 | 0.547945 | 7.6758 |
| 沪深300 ETF(沪) | 2.0000 | 205 | 2,109 | 5,005 | -1,930 | 437.0000 | 874.0000 | -3.9201 | 0.050932 | 0.488584 | 7.6758 |
| 沪深300 ETF(沪) | 5.0000 | 205 | 620.6751 | 5,005 | -2,922 | 437.0000 | 2,185 | -9.6478 | 0.050932 | 0.365297 | 7.6758 |
| 沪深300 ETF(沪) | 10.0000 | 205 | -1,465 | 5,005 | -4,312 | 437.0000 | 4,370 | -21.7339 | 0.050932 | 0.191781 | 7.6758 |
| 中证500 ETF(沪) | 0.000e+00 | 205 | 2,646 | -4,043 | 11,230 | 417.0000 | 0.000e+00 | -4.1327 | 0.051841 | 0.574163 | 8.1866 |
| 中证500 ETF(沪) | 1.0000 | 205 | 2,130 | -4,043 | 10,363 | 417.0000 | 417.0000 | -4.1519 | 0.051841 | 0.535885 | 8.1866 |
| 中证500 ETF(沪) | 2.0000 | 205 | 1,634 | -4,043 | 9,532 | 417.0000 | 834.0000 | -4.9283 | 0.051841 | 0.511962 | 8.1866 |
| 中证500 ETF(沪) | 5.0000 | 205 | 266.0210 | -4,043 | 7,235 | 417.0000 | 2,085 | -11.9560 | 0.051841 | 0.373206 | 8.1866 |
| 中证500 ETF(沪) | 10.0000 | 205 | -1,667 | -4,043 | 3,990 | 417.0000 | 4,170 | -23.1213 | 0.051841 | 0.215311 | 8.1866 |

Test date range: 2024/03/01 -> 2024/12/31 (205 trading days), including 2024/09 and 2024/10.

![Test Net Strategy Cost Sensitivity](images/figure-015.png "Test Net Strategy Cost Sensitivity")

test split only; trading rule is the same as 5.1; cost is deducted as abs(position - prev_position) * single-side cost bps / 10000.

![Test Net Strategy Cost Sensitivity Excluding 2024/09-2024/10](images/figure-016.png "Test Net Strategy Cost Sensitivity Excluding 2024/09-2024/10")

test split only with 2024/09 and 2024/10 removed before recompounding; trading rule and single-side cost deduction match the other 5.2 figures.

字段解释

| field | explanation |
| --- | --- |
| single_side_cost_bps | 单边交易成本, 按 abs(position - prev_position) * cost_bps / 10000 从 strategy_minute_return 中扣减.  |
| test_cum_net_strategy_bps | test split 内扣除单边交易成本后的 strategy_minute_return 从 1 重新复利后的累计收益, 单位 bps.  |
| test_cum_benchmark_bps | test split 内 benchmark_minute_return 从 1 重新复利后的累计收益, 单位 bps.  |
| test_net_excess_bps | (1 + test_cum_net_strategy_return) / (1 + test_cum_benchmark_return) - 1, 单位 bps.  |
| total_turnover | test split 内 abs(position - prev_position) 的合计.  |
| total_cost_bps | test split 内累计扣除的交易成本, 近似为 sum(turnover_event * single_side_cost_bps).  |
| max_drawdown_pct | strategy_nav 相对历史高点的最大回撤, 单位 %.  |
| exposure_ratio | position > 0 的分钟数 / 总分钟数.  |
| win_rate_by_trade | 按 trade_id 聚合每次开仓复利收益, 收益大于 0 的比例.  |
| avg_holding_minutes | 每个 trade_id 覆盖的分钟数均值.  |
| net_strategy_cumulative_return | test split 内扣除单边交易成本后的 strategy return 从 1 重新复利得到的累计收益.  |
| position | 调仓分钟 ETF prediction > baseline_threshold 时为 1, 否则为 0; 非调仓分钟沿用上一分钟持仓.  |
| prev_position | 同一个 pool 上一分钟的 position, 成本分析中用于计算 abs(position - prev_position).  |
| strategy_minute_return | return_event 为 true 时等于 position * etf_real_return, 否则为 0.  |

### 5.3. ETF Trade Return Distribution

![Train-Val-Test ETF Trade Return Distribution](images/figure-017.png "Train-Val-Test ETF Trade Return Distribution")

Each observation is one pool + trade_id from the 5.1 ETF long/flat strategy. For each trade_id, trade return is compounded across the rebalance return events while the position is active, using strategy_minute_return.

![Test ETF Trade Return Distribution](images/figure-018.png "Test ETF Trade Return Distribution")

Test split only; each observation is one pool + trade_id observed inside test. For each trade_id, trade return is compounded across the rebalance return events while the position is active, using strategy_minute_return.

字段解释

| field | explanation |
| --- | --- |
| trade_return_bps | 按 pool + trade_id 聚合 strategy_minute_return 复利后的单笔交易收益, 单位 bps.  |
| trade_id | 每次开仓生成一个 trade id, 持仓期间沿用该 id, 空仓时为 0.  |
| holding_minutes | 持仓分钟数; 交易分布中表示同一个 trade_id 覆盖的分钟行数, 6.5 中表示 future holding horizon.  |
| strategy_minute_return | return_event 为 true 时等于 position * etf_real_return, 否则为 0.  |

### 5.4. Entry Delay Decay Experiment

![Train-Val-Test Entry Delay Decay](images/figure-019.png "Train-Val-Test Entry Delay Decay")

Delay levels are 0, 1, 2, and 3 minutes; only the entry timestamp is delayed, while the original exit timestamp and 5.1 trading rule stay unchanged.

![Test Entry Delay Decay](images/figure-020.png "Test Entry Delay Decay")

Test split only; delay levels are 0, 1, 2, and 3 minutes; trades shorter than the delay are skipped for that delayed path.

字段解释

| field | explanation |
| --- | --- |
| delay_minutes | entry delay decay 实验中相对原始开仓时间延后的分钟数.  |
| delayed_strategy_cumulative_return | 只延后开仓, 不延后平仓后, strategy return 从 1 重新复利得到的累计收益.  |
| open_event | 调仓分钟 position 从 0 切换到 1 时记为一次开仓.  |
| return_event | 只有调仓分钟入账一次 realized/expected return, 非调仓分钟为 0, 避免 forward label 每分钟重叠复利.  |
| position | 调仓分钟 ETF prediction > baseline_threshold 时为 1, 否则为 0; 非调仓分钟沿用上一分钟持仓.  |
| strategy_minute_return | return_event 为 true 时等于 position * etf_real_return, 否则为 0.  |

### 6. Robustness Diagnostics

### 6.1. IC by volatility rank

![全 test 数据池按 volatility_label 排序切成 20 个等样本量分组, 每组计算 corr(prediction, target) 和 corr(rank(prediction), rank(target)). ](images/figure-021.png "全 test 数据池按 volatility_label 排序切成 20 个等样本量分组, 每组计算 corr(prediction, target) 和 corr(rank(prediction), rank(target)). ")

全 test 数据池按 volatility_label 排序切成 20 个等样本量分组, 每组计算 corr(prediction, target) 和 corr(rank(prediction), rank(target)). 

### 6.2. IC by price rank

![全 test 数据池按 price_label 排序切成 20 个等样本量分组, 每组计算 corr(prediction, target) 和 corr(rank(prediction), rank(target)). ](images/figure-022.png "全 test 数据池按 price_label 排序切成 20 个等样本量分组, 每组计算 corr(prediction, target) 和 corr(rank(prediction), rank(target)). ")

全 test 数据池按 price_label 排序切成 20 个等样本量分组, 每组计算 corr(prediction, target) 和 corr(rank(prediction), rank(target)). 

### 6.3. Train/test intraday IC curve

![Train/Test Intraday IC](images/figure-023.png "Train/Test Intraday IC")

对 train/test 分别按 intraday time 分组, 将所有日期同一分钟的样本合并后计算一次 Pearson IC. 

### 6.4. Monthly signal spread and net efficiency

![Monthly Signal Spread And Strategy Efficiency](images/figure-024.png "Monthly Signal Spread And Strategy Efficiency")

按月展示 test top-minus-bottom signal spread, 以及 5.1 strategy proxy 的三 pool 等权平均 bps per turnover. 

![Monthly IC And Rank IC](images/figure-025.png "Monthly IC And Rank IC")

按月合并当前 test manifest 的所有样本, 分别计算 Pearson IC 和 Rank IC. 

### 6.5. Return Realization

![Return Realization](images/figure-026.png "Return Realization")

Selected test rows use prediction >= p95(prediction). For holding n minutes, realized return is log_close[t + 1 + n] - log_close[t + 1].

| holding_minutes | mean_return | mean_return_bps | row_count | prediction_p95 |
| --- | --- | --- | --- | --- |
| 1.0000 | 2.207e-04 | 2.2071 | 8,811,040 | 9.594e-04 |
| 2.0000 | 3.973e-04 | 3.9729 | 8,811,040 | 9.594e-04 |
| 3.0000 | 5.388e-04 | 5.3876 | 8,811,040 | 9.594e-04 |
| 4.0000 | 6.555e-04 | 6.5548 | 8,811,040 | 9.594e-04 |
| 5.0000 | 7.584e-04 | 7.5838 | 8,811,040 | 9.594e-04 |
| 6.0000 | 8.487e-04 | 8.4870 | 8,811,040 | 9.594e-04 |
| 7.0000 | 9.343e-04 | 9.3426 | 8,811,040 | 9.594e-04 |
| 8.0000 | 0.001008 | 10.0750 | 8,811,040 | 9.594e-04 |
| 9.0000 | 0.001075 | 10.7545 | 8,811,040 | 9.594e-04 |
| 10.0000 | 0.001144 | 11.4374 | 8,811,040 | 9.594e-04 |
| 11.0000 | 0.001209 | 12.0943 | 8,597,395 | 9.594e-04 |
| 12.0000 | 0.001270 | 12.7044 | 8,404,993 | 9.594e-04 |
| 13.0000 | 0.001324 | 13.2437 | 8,233,630 | 9.594e-04 |
| 14.0000 | 0.001368 | 13.6810 | 8,084,875 | 9.594e-04 |
| 15.0000 | 0.001405 | 14.0537 | 7,953,534 | 9.594e-04 |
| 16.0000 | 0.001432 | 14.3239 | 7,839,301 | 9.594e-04 |
| 17.0000 | 0.001448 | 14.4777 | 7,744,768 | 9.594e-04 |
| 18.0000 | 0.001453 | 14.5300 | 7,667,501 | 9.594e-04 |
| 19.0000 | 0.001450 | 14.4950 | 7,604,066 | 9.594e-04 |
| 20.0000 | 0.001440 | 14.3985 | 7,551,539 | 9.594e-04 |

字段解释

| field | explanation |
| --- | --- |
| Return Realization | 当前 selected test prediction 最高 5% 样本的未来持仓收益实现曲线.  |
| holding_minutes | 持仓分钟数; 交易分布中表示同一个 trade_id 覆盖的分钟行数, 6.5 中表示 future holding horizon.  |
| mean_return | 分组内 realized raw log return 的均值.  |
| mean_return_bps | 分组内 realized return 均值, 单位 bps.  |
| prediction_p95 | test split finite prediction 的 95% 分位阈值; 6.5 只保留 prediction >= prediction_p95 的样本.  |
| row_count | 该 holding horizon 下成功对齐 entry/exit close 且 realized raw log return finite 的样本数.  |

### 6.6. Top-k% Robustness

![Top-k% Robustness](images/figure-027.png "Top-k% Robustness")

Top k% selected by approximate prediction quantile threshold within each split; k = 1, 2, 3, 5, 10, 15, 20.

| split | selection_method | k_pct | universe_count | selected_count | selected_fraction | prediction_threshold | mean_label_bps | median_label_bps | label_std_bps | hit_rate | day_count | timestamp_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | approx_quantile_threshold | 1 | 553,898,121 | 5,515,403 | 0.009957 | 0.002419 | 49.8360 | 43.9701 | 83.7722 | 0.774122 | 727 | 116,230 |
| train | approx_quantile_threshold | 2 | 553,898,121 | 10,918,473 | 0.019712 | 0.001580 | 35.1788 | 29.5979 | 78.3092 | 0.684209 | 727 | 117,038 |
| train | approx_quantile_threshold | 3 | 553,898,121 | 16,694,859 | 0.030141 | 0.001213 | 27.9098 | 22.2551 | 73.8740 | 0.634900 | 727 | 117,047 |
| train | approx_quantile_threshold | 5 | 553,898,121 | 27,562,367 | 0.049761 | 8.859e-04 | 21.0112 | 15.2610 | 67.9672 | 0.585859 | 727 | 117,047 |
| train | approx_quantile_threshold | 10 | 553,898,121 | 55,289,916 | 0.099820 | 5.391e-04 | 13.9121 | 7.6493 | 59.5574 | 0.531341 | 727 | 117,047 |
| train | approx_quantile_threshold | 15 | 553,898,121 | 82,981,029 | 0.149813 | 3.785e-04 | 10.7999 | 2.9466 | 54.8773 | 0.504808 | 727 | 117,047 |
| train | approx_quantile_threshold | 20 | 553,898,121 | 110,621,563 | 0.199715 | 2.795e-04 | 8.9371 | 0.114838 | 51.7013 | 0.487321 | 727 | 117,047 |
| test | approx_quantile_threshold | 1 | 176,134,322 | 1,727,123 | 0.009806 | 0.002156 | 24.0202 | 5.7699 | 127.8472 | 0.509488 | 205 | 32,996 |
| test | approx_quantile_threshold | 2 | 176,134,322 | 3,489,193 | 0.019810 | 0.001549 | 17.3525 | 1.1823 | 108.1547 | 0.494052 | 205 | 33,005 |
| test | approx_quantile_threshold | 3 | 176,134,322 | 5,229,632 | 0.029691 | 0.001267 | 14.4974 | 0.132107 | 98.0425 | 0.486784 | 205 | 33,005 |
| test | approx_quantile_threshold | 5 | 176,134,322 | 8,769,236 | 0.049787 | 9.615e-04 | 11.4647 | 0.028194 | 86.3244 | 0.477056 | 205 | 33,005 |
| test | approx_quantile_threshold | 10 | 176,134,322 | 17,587,778 | 0.099854 | 6.157e-04 | 8.0893 | 3.691e-05 | 72.8887 | 0.461349 | 205 | 33,005 |
| test | approx_quantile_threshold | 15 | 176,134,322 | 26,429,844 | 0.150055 | 4.401e-04 | 6.3937 | 0.000e+00 | 66.1409 | 0.450561 | 205 | 33,005 |
| test | approx_quantile_threshold | 20 | 176,134,322 | 35,246,681 | 0.200113 | 3.277e-04 | 5.3063 | 0.000e+00 | 61.7884 | 0.442298 | 205 | 33,005 |

字段解释

| field | explanation |
| --- | --- |
| Top-k Robustness | train/test 各自样本池内用近似 prediction 分位阈值选择最高 k% 样本, 检查集中高 prediction 样本的 realized return.  |
| split | 样本池名称, 6.6 中为 train 或 test.  |
| selection_method | Top-k% 选择方法; 6.6 使用 approx_quantile_threshold, 即 DuckDB approx_quantile 给出的近似 prediction 分位阈值.  |
| k_pct | 按 prediction 全局降序选择的样本池顶部百分比.  |
| universe_count | 该 split 中 finite prediction/target 样本总数.  |
| selected_count | 该 split,k_pct 下 prediction >= prediction_threshold 的实际入选样本数.  |
| selected_fraction | selected_count / universe_count; 近似阈值口径下可能略偏离 k_pct / 100.  |
| prediction_threshold | DuckDB approx_quantile(prediction, 1 - k_pct / 100) 得到的近似入选阈值.  |
| mean_label_bps | 分组内 target 均值, 单位 bps.  |
| median_label_bps | Top-k% 样本 target 近似中位数, 使用 DuckDB approx_quantile(target, 0.5), 单位 bps.  |
| label_std_bps | Top-k% 样本 target 样本标准差, 单位 bps.  |
| hit_rate | 分组内 target > 0 的比例.  |
| day_count | 入选样本覆盖的交易日数量.  |
| timestamp_count | 入选样本覆盖的 date,time 截面数量.  |

## 限制与适用边界

修正 mixed-normalization 评估后 full63 test IC/RankIC 为0.061496/0.051659. Matched family ablation 中 relative/liquidity9 为0.098183/0.075886; market16 在训练 gate 停止, 未读取 test. 当前artifact可得性只影响复现, 不作为历史成功/失败判据. 只有matched合同内的结果可以直接比较.

## 结论

本次归档保留上述历史事实. 研究结论, 推广门槛和执行限制分别解释, 不把模型无增益或净收益为负改写成实验流程失败.

## 附录

### 7. Appendix Diagnostics

Artifact Paths

run_root

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/date_ranges

research_report_root

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report

npz_meta

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/date_ranges/artifacts/npz/meta.yaml

data_clean_invalid_stats

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/date_ranges/artifacts/data_clean/invalid_feature_stats.csv

core_ic_metrics

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/core_ic_metrics.csv

signal_bucket_metrics

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/signal_quality/signal_bucket_metrics.csv

daily_top_bottom_signal_spread

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/signal_quality/daily_top_bottom_signal_spread.csv

goodness_of_fit_metrics

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/signal_quality/goodness_of_fit_metrics.csv

goodness_of_fit_png

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/signal_quality/goodness_of_fit.png

label_distribution_summary

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/data_pipeline/label_distribution_summary.csv

label_distribution_png

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/data_pipeline/label_distribution_by_split.png

important_pool_pooled_ic

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/important_pool/important_pool_pooled_ic.csv

important_pool_nonzero_metrics

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/important_pool/important_pool_nonzero_metrics.csv

important_pool_cumulative_returns

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/important_pool/important_pool_train_val_test_cumulative_returns.csv

train_test_intraday_ic

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/robustness/train_test_intraday_ic.csv

monthly_signal_spread_strategy_efficiency

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/robustness/monthly_signal_spread_strategy_efficiency.csv

monthly_ic_rank_ic

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/robustness/monthly_ic_rank_ic.csv

topk_robustness

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/robustness/topk_robustness.csv

topk_robustness_png

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/robustness/topk_robustness.png

train_loss_log_png

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/figures/train_loss_no_step0_smoothed_log.png

train_checkpoint_sample_ic

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/train_metrics/train_checkpoint_sample_ic.csv

train_checkpoint_sample_ic_png

[artifact-root]/nn/multiscale-market-features-1min-ablation/legacy14_trend_return12/seed7/research_report/train_metrics/train_checkpoint_sample_ic.png

Extreme Value Metrics

| metric | value |
| --- | --- |
| val/dist/mean/pred | nan |
| val/dist/mean/target | nan |
| val/dist/abs_mean/pred | nan |
| val/dist/abs_mean/target | nan |
| val/dist/std/pred | nan |
| val/dist/std/target | nan |
| val/dist/pred_std_over_target_std | nan |
| val/dist/p01/pred | nan |
| val/dist/p01/target | nan |
| val/dist/p50/pred | nan |
| val/dist/p50/target | nan |
| val/dist/p99/pred | nan |
| val/dist/p99/target | nan |

Label Availability Coverage

| split | raw_rows | kept_rows | sampled_rows | out_rows | kept_rate |
| --- | --- | --- | --- | --- | --- |
| train | 842,496,476 | 794,726,723 | 553,898,121 | 553,898,121 | 0.943300 |
| val | 47,712,939 | 45,536,385 | 31,737,447 | 31,737,447 | 0.954382 |
| test | 264,871,532 | 252,715,072 | 176,134,322 | 176,134,322 | 0.954104 |

Pending Diagnostics

| diagnostic | status |
| --- | --- |
| turnover_decomposition | pending backtest/trading artifact |
| capacity_sensitivity | pending capacity artifact |
| short_side_diagnostics | pending long/short-side artifact |
