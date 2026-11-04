---
title: '跨交易日窗口诊断: 登记证据汇总'
date: 2026-11-03
summary: A/B/C synthetic 与3日×128股票诊断成功. 真实 matched A/B差值为0, A/C最大差0.968504, B减少5120个 feature rows. 正式模型比较报告仍未定位.
tags:
- prediction-nn
- registry-evidence
featured: false
---

## 摘要

**历史结果: 历史成功, 限 boundary diagnostics.** A/B/C synthetic 与3日×128股票诊断成功. 真实 matched A/B差值为0, A/C最大差0.968504, B减少5120个 feature rows. 正式模型比较报告仍未定位.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

Verify that carry and drop treatments match on common valid rows, that drop reduces coverage, and that shifted history is observably distinct before formal training. 本文是registry证据汇总, 不是失踪原报告的重建副本.

## 数据与方法

| 项目 | 登记值 |
| --- | --- |
| experiment_id | crossday-rolling |
| method | A/B/C session-boundary identity, coverage, and distinctness gates |
| dataset | synthetic plus bounded real sample · 3 days × 128 stocks |
| result_scope | contract, synthetic gate, and bounded real-data diagnostic only |

## 主要结果

| 登记字段及scope | 历史值 |
| --- | --- |
| synthetic_gate.rows | 2892 |
| synthetic_gate.ab_matched_rows | 2732 |
| synthetic_gate.ab_max_abs_diff | 0.0 |
| synthetic_gate.ac_max_abs_diff | 0.2509521842 |
| synthetic_gate.b_deleted_feature_rows | 160 |
| synthetic_gate.a_sequences | 728 |
| synthetic_gate.b_sequences | 648 |
| synthetic_gate.c_sequences | 728 |
| bounded_real_gate.rows | 92544 |
| bounded_real_gate.valid_boundaries | 254 |
| bounded_real_gate.invalid_boundaries | 2 |
| bounded_real_gate.ab_matched_rows | 87424 |
| bounded_real_gate.ab_max_abs_diff | 0.0 |
| bounded_real_gate.ac_max_abs_diff | 0.9685039409 |
| bounded_real_gate.b_deleted_feature_rows | 5120 |
| bounded_real_gate.a_sequences | 23114 |
| bounded_real_gate.b_sequences | 20574 |
| bounded_real_gate.c_sequences | 23114 |

## 限制与适用边界

A/B/C synthetic 与3日×128股票诊断成功. 真实 matched A/B差值为0, A/C最大差0.968504, B减少5120个 feature rows. 正式模型比较报告仍未定位. 原始文件, 选模协议和样本口径不齐时, 只保留已经登记的历史事实. 不对缺失字段插值, 不重扫prediction artifact.

## 结论

保留已成功的实验或诊断事实, 不因当前材料缺失判为失败. 正式结果未确认的部分保持待核对. Retain the boundary implementation as a passed pre-training gate, but do not choose an arm or claim model quality until matched formal runs exist.

## 附录

事实来源: `nn-registry/crossday-rolling/results.yaml`, `manifest.yaml`, `experiment-summary.md`. [全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

| 输入 | SHA256 |
| --- | --- |
| manifest | 5c51e92da98c03d9a961589c440dfd94e0df62d446709fae80231a6537ef6670 |
| results | fefb3a6dfe0b0d279d429a432ec44c5be550fde34813beae063ed1aa16cf2be3 |
| experiment_summary | 5a783e9f25d61d092b30818c3f1013930286cce2505d2e7631c9fbda786d730c |
