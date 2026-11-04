---
title: 'Native v2 sanity 与正式结果核对: 登记证据汇总'
date: 2026-11-03
summary: Native v2 的 causal/shuffled/shifted synthetic sanity 已成功, R²为0.999700/−0.445876/−0.083254. 独立正式63D模型报告仍未定位, 不写成训练失败.
tags:
- prediction-nn
- registry-evidence
featured: false
---

## 摘要

**历史结果: 历史成功, 限 sanity.** Native v2 的 causal/shuffled/shifted synthetic sanity 已成功, R²为0.999700/−0.445876/−0.083254. 独立正式63D模型报告仍未定位, 不写成训练失败.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

Validate the production-chain v2 contract and leakage checks before running a formal 63-feature prediction baseline. 本文是registry证据汇总, 不是失踪原报告的重建副本.

## 数据与方法

| 项目 | 登记值 |
| --- | --- |
| experiment_id | baseline-1min-0813 |
| method | Native 63-feature contract and maintained synthetic leakage checks |
| dataset | synthetic causal diagnostic · formal stock1m run not started |
| result_scope | engineering refactor and maintained synthetic sanity only; no formal prediction evaluation |

## 主要结果

| 登记字段及scope | 历史值 |
| --- | --- |
| diagnostic_only.proper_causal_test_r_squared | 0.9997001664479347 |
| diagnostic_only.shuffled_train_label_test_r_squared | -0.44587555651939614 |
| diagnostic_only.shifted_train_label_test_r_squared | -0.08325392440243395 |

## 限制与适用边界

Native v2 的 causal/shuffled/shifted synthetic sanity 已成功, R²为0.999700/−0.445876/−0.083254. 独立正式63D模型报告仍未定位, 不写成训练失败. 原始文件, 选模协议和样本口径不齐时, 只保留已经登记的历史事实. 不对缺失字段插值, 不重扫prediction artifact.

## 结论

保留已成功的实验或诊断事实, 不因当前材料缺失判为失败. 正式结果未确认的部分保持待核对. Keep this entry engineering-only and exclude it from model-quality and trading comparisons until a formal native v2 run is registered.

## 附录

事实来源: `nn-registry/baseline-1min-0813/results.yaml`, `manifest.yaml`, `experiment-summary.md`. [全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

| 输入 | SHA256 |
| --- | --- |
| manifest | 4e53d3b3cf007b04d748da27ebf7495e80e37beb391d845fbb864cdbb419573e |
| results | ffb9687b4623472e416fc5c44d799117b8488cd4a50b2a8f46d9ae47337a3a60 |
| experiment_summary | a050e813e6399cea791b87d18e861e26dbd0ac8d23b89f205e94771fdd365a09 |
