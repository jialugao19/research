---
title: 'Mainline baseline 待核对: 登记证据汇总'
date: 2026-11-03
summary: 在 REPORT, 网站及当前 checkout 中未定位到可归属于该实验的独立正式报告. 历史 capacity 报告引用它的数据目录, 不能据此确认其自身训练成功或失败.
tags:
- prediction-nn
- registry-evidence
featured: false
---

## 摘要

**历史结果: 待核对.** 在 REPORT, 网站及当前 checkout 中未定位到可归属于该实验的独立正式报告. 历史 capacity 报告引用它的数据目录, 不能据此确认其自身训练成功或失败.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

Register configuration, run, and artifact facts for the mainline baseline. 本文是registry证据汇总, 不是失踪原报告的重建副本.

## 数据与方法

| 项目 | 登记值 |
| --- | --- |
| experiment_id | baseline-main-20260622 |
| method | Baseline registration audit |
| dataset | Mainline artifacts |
| result_scope | placeholder registration only; no completed run result |

## 主要结果

| 登记字段及scope | 历史值 |
| --- | --- |
| 正式模型结果 | 未定位到可确认身份的报告; 不判定成功或失败 |

## 限制与适用边界

在 REPORT, 网站及当前 checkout 中未定位到可归属于该实验的独立正式报告. 历史 capacity 报告引用它的数据目录, 不能据此确认其自身训练成功或失败. 原始文件, 选模协议和样本口径不齐时, 只保留已经登记的历史事实. 不对缺失字段插值, 不重扫prediction artifact.

## 结论

保留已成功的实验或诊断事实, 不因当前材料缺失判为失败. 正式结果未确认的部分保持待核对. Exclude from all comparisons until registration is complete.

## 附录

事实来源: `nn-registry/baseline-main-20260622/results.yaml`, `manifest.yaml`, `experiment-summary.md`. [全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

| 输入 | SHA256 |
| --- | --- |
| manifest | 41717dea7e6934671ca091444e77f832d61997edea8c054c80ab5f6e0112377d |
| results | 301642ed1db1e44cc9b0a239fdd90f8379722c18f4daaaa987495e3406f6f43b |
| experiment_summary | 53f7422a48027ba9b738744e436f42d2ccf93a7c23156ce7e6e91d30a4e18a3c |
