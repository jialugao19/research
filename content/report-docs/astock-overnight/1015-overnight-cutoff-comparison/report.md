---
title: 13:50 与 13:58 cutoff 对照
date: 2026-10-15
summary: Full-arm 与 matched RankIC 均下降, 保留 13:58 baseline; 2025 tail 改善不能用于反向选择.
tags:
- overnight
- research
featured: false
---

## 摘要

Full-arm 与 matched RankIC 均下降, 保留 13:58 baseline; 2025 tail 改善不能用于反向选择.

后续独立 ledger audit 已确认旧 Validation gross ledger 未排除 split boundary positions. 13:58 baseline 的 corrected gross return 为 20.1322%, Sharpe 为 1.552499; 13:50 为 10.7110%, Sharpe 为 0.838975. 旧表、旧图作为历史 evidence 保留, 相应 Validation long-only 数值以 [ledger audit](/reports/astock-overnight/1016-overnight-ledger-audit/) 为准. 未对未审计的 CSI1800、其他 tail 或方案 A 结果推算更正值.

## 研究背景与目标

研究问题与数据合同以保留的源报告为准. 本页将既有研究证据登记为独立 publication, 关联对应 Study 与 Experiment.

## 数据与方法

2021-2023 为 Train; 2024 Validation 排除 9-10 月. 历史报告中的 2025 one-shot Test 已被查看, 当前仅能作为 historical confirmation, 不支持再次用其选择配置. 本次同步仅整理既有 evidence, 未训练、推理或重跑回测.

## 主要结果


### 1. 结论

13:50 不替换 13:58 baseline. Validation primary metrics 同时下降: daily mean RankIC 变化 `-0.014724`, Q10-Q1 变化 `-0.000613`, event-driven long-only total return 变化 `-7.98%`. Test 的 long-only total return 变化 `14.01%`, 但 daily mean RankIC 变化 `-0.010586`. 这说明 2025 的部分 tail PnL 改善没有伴随更强的整体横截面排序, 且没有在 Validation 重现.

13:50 可以保留为后续 tail research candidate, 但当前证据不支持 promotion. 2025 是 one-shot Test, 不能用该年度结果反向选择 cutoff.

### 2. 实验边界

- Baseline: `13:58`, minute sequence `59..178`, evaluation `[artifact-root]/astock-overnight/evaluations/20260918T141822Z`.
- Variant: `13:50`, minute sequence `51..170`, evaluation `[artifact-root]/astock-overnight/evaluations/20261015T164233Z`.
- Entry 与 label 不变: `D 14:00` 买入, 下一交易日 `10:00` 或原 delayed-exit rule 卖出.
- Model structure、training hyperparameters、seed、factor set、normalization 与 evaluation contract 不变, 两个 arm 各自训练.
- Daily factor 与全日 raw factor panel 相同. Minute GRU window 向前平移 8 分钟, cutoff universe 也随之变化.
- 因此 full-arm 差异包含 `cutoff + minute window + cutoff universe + retraining` 的共同影响, 不是孤立的 8 分钟因果效应.

### 3. Full-arm OOS

每个 arm 使用自身 cutoff 定义的完整 prediction group. Decile 与 Top-tail 不在两个 arm 之间强制使用相同股票.

| scope | period | prediction_rows_baseline | prediction_rows_variant | prediction_rows_delta | mean_rank_ic_baseline | mean_rank_ic_variant | mean_rank_ic_delta | q10_mean_return_baseline | q10_mean_return_variant | q10_mean_return_delta | q10_q1_mean_return_baseline | q10_q1_mean_return_variant | q10_q1_mean_return_delta | long_only_total_return_baseline | long_only_total_return_variant | long_only_total_return_delta | long_only_maximum_drawdown_baseline | long_only_maximum_drawdown_variant | long_only_maximum_drawdown_delta | terminal_break_even_bps_baseline | terminal_break_even_bps_variant | terminal_break_even_bps_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all_market | validation | 131,881 | 135,684 | 3,803 | 0.147947 | 0.133224 | -0.014724 | 0.000936 | 0.000538 | -0.000398 | 0.013610 | 0.012997 | -0.000613 | 0.167240 | 0.087437 | -0.079803 | -0.047105 | -0.081666 | -0.034561 | 3.627193 | 2.013352 | -1.613841 |
| all_market | test | 212,159 | 217,722 | 5,563 | 0.114489 | 0.103903 | -0.010586 | 0.000912 | 0.001357 | 0.000445 | 0.007652 | 0.007796 | 0.000144 | 0.237166 | 0.377233 | 0.140067 | -0.069367 | -0.059134 | 0.010233 | 4.289307 | 6.632521 | 2.343214 |

### 4. 2021-2025 年度结果

2021-2023 为 train in-sample, 2024 为 checkpoint selection Validation 且排除 9-10 月, 2025 为 one-shot Test.

| period | modeling_role | prediction_rows_baseline | prediction_rows_variant | prediction_rows_delta | mean_rank_ic_baseline | mean_rank_ic_variant | mean_rank_ic_delta | q10_q1_mean_return_baseline | q10_q1_mean_return_variant | q10_q1_mean_return_delta | long_only_total_return_baseline | long_only_total_return_variant | long_only_total_return_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | train_in_sample | 159,769 | 163,063 | 3,294 | 0.103713 | 0.098916 | -0.004797 | 0.009369 | 0.009119 | -0.000250 | 0.410203 | 0.350648 | -0.059555 |
| 2022 | train_in_sample | 153,006 | 156,565 | 3,559 | 0.122798 | 0.116460 | -0.006339 | 0.011115 | 0.010700 | -0.000415 | 0.112927 | 0.016906 | -0.096021 |
| 2023 | train_in_sample | 129,354 | 133,112 | 3,758 | 0.135692 | 0.128106 | -0.007586 | 0.010062 | 0.009838 | -0.000224 | 0.208418 | 0.220241 | 0.011823 |
| 2024 | validation_selected_excludes_sep_oct | 131,881 | 135,684 | 3,803 | 0.147947 | 0.133224 | -0.014724 | 0.013610 | 0.012997 | -0.000613 | 0.167240 | 0.087437 | -0.079803 |
| 2025 | test_one_shot | 212,159 | 217,722 | 5,563 | 0.114489 | 0.103903 | -0.010586 | 0.007652 | 0.007796 | 0.000144 | 0.237166 | 0.377233 | 0.140067 |

### 5. CSI1800 与 Top-tail

CSI1800 在 date-effective pool 内重新排序. Top-tail 使用各 arm 已发布的 selection, 不 rerank 或 refill.

| scope | period | prediction_rows_baseline | prediction_rows_variant | prediction_rows_delta | mean_rank_ic_baseline | mean_rank_ic_variant | mean_rank_ic_delta | q10_q1_mean_return_baseline | q10_q1_mean_return_variant | q10_q1_mean_return_delta | long_only_total_return_baseline | long_only_total_return_variant | long_only_total_return_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| csi1800 | validation | 97,660 | 99,845 | 2,185 | 0.084555 | 0.066778 | -0.017777 | 0.004522 | 0.004127 | -0.000395 | 0.132396 | 0.098838 | -0.033558 |
| csi1800 | test | 142,378 | 145,007 | 2,629 | 0.060210 | 0.048953 | -0.011257 | 0.003014 | 0.002980 | -0.000033 | 0.229790 | 0.382067 | 0.152277 |

Test Top-tail:

| scope | period | selection | cohort_mean_return_baseline | cohort_mean_return_variant | cohort_mean_return_delta | portfolio_total_return_baseline | portfolio_total_return_variant | portfolio_total_return_delta | portfolio_maximum_drawdown_baseline | portfolio_maximum_drawdown_variant | portfolio_maximum_drawdown_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| all_market | test | top_5pct | 0.000941 | 0.001241 | 0.000300 | 0.249051 | 0.339333 | 0.090282 | -0.064958 | -0.058974 | 0.005984 |
| all_market | test | top_1pct | 0.001336 | 0.001065 | -0.000271 | 0.372569 | 0.281558 | -0.091011 | -0.068972 | -0.074218 | -0.005246 |
| all_market | test | top_0p5pct | 0.001537 | 0.000826 | -0.000711 | 0.437690 | 0.204727 | -0.232963 | -0.064262 | -0.143361 | -0.079099 |
| csi1800 | test | top_5pct | 0.000755 | 0.001236 | 0.000481 | 0.194130 | 0.337394 | 0.143264 | -0.055175 | -0.061657 | -0.006482 |
| csi1800 | test | top_1pct | 0.001256 | 0.001139 | -0.000116 | 0.345739 | 0.303005 | -0.042733 | -0.077308 | -0.071373 | 0.005935 |
| csi1800 | test | top_0p5pct | 0.001280 | 0.001185 | -0.000095 | 0.349502 | 0.312856 | -0.036646 | -0.077060 | -0.099721 | -0.022661 |

### 6. Sample membership

13:50 cutoff 改变了 eligible prediction group. `common_rows` 是同一 `signal_date + canonical_stock_code` 同时存在于两个 arm 的 rows.

| scope | baseline_rows | variant_rows | common_rows | baseline_only_rows | variant_only_rows | variant_minus_baseline | common_share_baseline | common_share_variant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 159,769 | 163,063 | 158,253 | 1,516 | 4,810 | 3,294 | 0.990511 | 0.970502 |
| 2022 | 153,006 | 156,565 | 151,114 | 1,892 | 5,451 | 3,559 | 0.987634 | 0.965184 |
| 2023 | 129,354 | 133,112 | 127,532 | 1,822 | 5,580 | 3,758 | 0.985915 | 0.958080 |
| 2024 | 131,881 | 135,684 | 130,147 | 1,734 | 5,537 | 3,803 | 0.986852 | 0.959192 |
| 2025 | 212,159 | 217,722 | 209,668 | 2,491 | 8,054 | 5,563 | 0.988259 | 0.963008 |
| train_2021_2023 | 442,129 | 452,740 | 436,899 | 5,230 | 15,841 | 10,611 | 0.988171 | 0.965011 |
| validation_2024 | 131,881 | 135,684 | 130,147 | 1,734 | 5,537 | 3,803 | 0.986852 | 0.959192 |
| test_2025 | 212,159 | 217,722 | 209,668 | 2,491 | 8,054 | 5,563 | 0.988259 | 0.963008 |
| all_2021_2025 | 786,169 | 806,146 | 776,714 | 9,455 | 29,432 | 19,977 | 0.987973 | 0.963490 |

共同样本 outcome 对账: `{"common_rows": 776714, "y_raw_maximum_absolute_difference": 0.0, "realized_return_maximum_absolute_difference": 0.0, "evaluable_mismatch_rows": 0, "tradable_mismatch_rows": 0}`. `y_raw`、`realized_return`、`evaluable` 与 `tradable` 在共同样本上完全一致.

### 7. Matched intersection

Matched view 仅保留两个 arm 都存在且都 evaluable 的 stock-day. 每日使用同一 realized return 分别计算两个模型的 RankIC. `rank_ic_delta = 13:50 - 13:58`; 95% interval 使用 20-day circular moving-block bootstrap, 5,000 resamples, seed 42.

| scope | days | mean_matched_rows | baseline_mean_rank_ic | variant_mean_rank_ic | rank_ic_delta | delta_confidence_95_lower | delta_confidence_95_upper | bootstrap_probability_positive | mean_score_rank_correlation | mean_score_pearson_correlation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train_2021_2023 | 726 | 601.035813 | 0.120697 | 0.114521 | -0.006176 | -0.010566 | -0.001699 | 0.004800 | 0.848969 | 0.935313 |
| validation_2024 | 203 | 633.147783 | 0.147958 | 0.134214 | -0.013744 | -0.021458 | -0.005722 | 0.000400 | 0.861321 | 0.943324 |
| test_2025 | 243 | 862.687243 | 0.114479 | 0.103392 | -0.011087 | -0.016522 | -0.005207 | 0.000000 | 0.831634 | 0.927808 |
| all_2021_2025 | 1,172 | 660.848123 | 0.124129 | 0.115624 | -0.008505 | -0.011804 | -0.005064 | 0.000000 | 0.847514 | 0.935144 |

Matched view 消除了 prediction-group membership 差异, 但没有消除 minute window 与模型重新训练的影响.

### 8. Published-tail membership overlap

Overlap 在两个完整 prediction group 的 union 上计算. `mean_jaccard = intersection / union`; `mean_overlap_of_smaller = intersection / min(size_baseline, size_variant)`.

| scope | selection | days | mean_baseline_selected | mean_variant_selected | mean_jaccard | mean_overlap_of_smaller |
| --- | --- | --- | --- | --- | --- | --- |
| validation_2024 | Q10 | 205 | 63.887805 | 65.721951 | 0.381088 | 0.552681 |
| validation_2024 | Top 5% | 205 | 32.678049 | 33.565854 | 0.310535 | 0.470245 |
| validation_2024 | Top 1% | 205 | 6.912195 | 7.126829 | 0.207431 | 0.329399 |
| validation_2024 | Top 0.5% | 205 | 3.692683 | 3.814634 | 0.189661 | 0.291572 |
| test_2025 | Q10 | 243 | 86.868313 | 89.144033 | 0.331680 | 0.495778 |
| test_2025 | Top 5% | 243 | 44.123457 | 45.263374 | 0.271161 | 0.421737 |
| test_2025 | Top 1% | 243 | 9.234568 | 9.452675 | 0.206523 | 0.328174 |
| test_2025 | Top 0.5% | 243 | 4.872428 | 4.967078 | 0.200097 | 0.303233 |

### 9. 研究判断

1. Validation 是 cutoff 选择依据. 13:50 在 RankIC、Q10-Q1 和 executable long-only return 上均弱于 baseline, 因此不通过替换门槛.
2. Test 中 13:50 的 Q10 与 Top 5% 有改善, 但 Top 1% 和 Top 0.5% 不稳定, 整体 RankIC 下降. 该模式更像 tail concentration 的年度差异, 不是稳健的全排序改善.
3. Matched RankIC 与 tail overlap 用于区分 membership effect. 若 matched RankIC 仍下降, 主要问题不在新增股票, 而在 window/model ranking path.
4. 保留 13:58 作为正式 baseline. 不根据 2025 one-shot Test 调整 cutoff.

### 10. Reproducibility

Machine-readable evidence 位于同目录的 `signal-cutoff-1350-*.csv` 与 `signal-cutoff-1350-comparison-manifest.json`. 所有收益为 gross; short-only 与 long-short 仍是 non-executable signal proxy.

## 限制与适用边界

后续独立 ledger audit 已确认旧 Validation gross ledger 未排除 split boundary positions. 13:58 baseline 的 corrected gross return 为 20.1322%, Sharpe 为 1.552499; 13:50 为 10.7110%, Sharpe 为 0.838975. 旧表、旧图作为历史 evidence 保留, 相应 Validation long-only 数值以 [ledger audit](/reports/astock-overnight/1016-overnight-ledger-audit/) 为准. 未对未审计的 CSI1800、其他 tail 或方案 A 结果推算更正值.

2021-2023 为 Train; 2024 Validation 排除 9-10 月. 历史报告中的 2025 one-shot Test 已被查看, 当前仅能作为 historical confirmation, 不支持再次用其选择配置. 本次同步仅整理既有 evidence, 未训练、推理或重跑回测.

## 结论

Full-arm 与 matched RankIC 均下降, 保留 13:58 baseline; 2025 tail 改善不能用于反向选择.

## 附录

来源: `astock-overnight/reports/signal-cutoff-1350-comparison.md`.

Source SHA-256: `1d2c9daf2d7ef2a1dbc330946a81f4a448f222d514c9bc7ebc25f09e237bc969`.

同步日期: 2026-11-03. 原始归档保留源字节; 本内容包仅移除机器本地路径, 不重新计算研究指标.
