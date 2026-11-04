---
title: '稳健 checkpoint selection: 登记证据汇总'
date: 2026-11-03
summary: 历史 full-grid audit 支持三 fold, 最后20个验证日, IC mean−0.5 std, earliest top2 的选择规则. 该 audit 的 test 已被查看, 不能视为新的盲选验证.
tags:
- prediction-nn
- registry-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** 历史 full-grid audit 支持三 fold, 最后20个验证日, IC mean−0.5 std, earliest top2 的选择规则. 该 audit 的 test 已被查看, 不能视为新的盲选验证.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

A single-window validation argmax can follow short-term noise and create hidden overfitting after repeated test inspection. This experiment scores checkpoints across three rolling/purged folds and the final 20 trading days using mean IC minus 0.5 standard deviations, then selects the earlier of the top two. 本文是registry证据汇总, 不是失踪原报告的重建副本.

## 数据与方法

| 项目 | 登记值 |
| --- | --- |
| experiment_id | val-select |
| method | Robust checkpoint selector |
| dataset | stock1m rolling / purged folds |
| result_scope | checkpoint selection validation design using rolling/purged folds and full-grid test audit |

## 主要结果

| 登记字段及scope | 历史值 |
| --- | --- |
| recommended_selector.validation_fold_set | 000+001+002 |
| recommended_selector.validation_window_days | 20 |
| recommended_selector.score_rule | ic_mean_minus_0.5std |
| recommended_selector.selection_policy | earliest_top2 |
| recommended_selector.selected_iter | 20000 |
| recommended_selector.test_score_regret | 0.0 |
| validation_argmax.selected_iter | 50000 |
| validation_argmax.test_score_regret | 0.002891 |
| validation_argmax.note | Validation argmax is not the robust test winner. |
| robust_test_winner.iter | 20000 |
| robust_test_winner.test_score_mean_minus_penalty_std | 0.053991 |
| robust_test_winner.mean_test_ic | 0.05922 |
| robust_test_winner.mean_test_top_decile_bps | 5.235391 |
| aggressive_candidate.iter | 30000 |
| aggressive_candidate.mean_test_ic | 0.062094 |
| aggressive_candidate.mean_test_rank_ic | 0.055983 |
| aggressive_candidate.mean_test_top_decile_bps | 5.976693 |
| aggressive_candidate.note | Best mean/rank/top-decile test candidate, but less robust than 20k. |
| validation_test_relationship.corr_fold_iter_val_ic_vs_test_ic | 0.663961 |
| validation_test_relationship.corr_iter_mean_val_ic_vs_test_ic | 0.706268 |
| validation_test_relationship.corr_iter_mean_val_score_vs_test_score | 0.898735 |

## 限制与适用边界

历史 full-grid audit 支持三 fold, 最后20个验证日, IC mean−0.5 std, earliest top2 的选择规则. 该 audit 的 test 已被查看, 不能视为新的盲选验证. 原始文件, 选模协议和样本口径不齐时, 只保留已经登记的历史事实. 不对缺失字段插值, 不重扫prediction artifact.

## 结论

保留已成功的实验或诊断事实, 不因当前材料缺失判为失败. 正式结果未确认的部分保持待核对. Use 20k as the robust default; retain 30k only as an aggressive comparison.

## 附录

事实来源: `nn-registry/val-select/results.yaml`, `manifest.yaml`, `experiment-summary.md`. [全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

| 输入 | SHA256 |
| --- | --- |
| manifest | 0c817a98a3abe311d98002515cf244d903ce19a3bea6bd006f4c3110c2e2186b |
| results | c86d87d48674b8d64e186a277be096785e21324077f0d4d7d6b6cc6f5089f8b4 |
| experiment_summary | 75096f29d10b20d44614df6c8587caf9aee9e768c0ffe55e5aa6137deae41f8e |
