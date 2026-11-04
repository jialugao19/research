---
title: 'Rolling/purged validation: 登记证据汇总'
date: 2026-11-03
summary: 三个 rolling/purged fold 已记录验证 IC 0.0642117, 0.0647218, 0.0687591. 当前源报告和 run artifact 缺失, 不改变历史完成事实.
tags:
- prediction-nn
- registry-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** 三个 rolling/purged fold 已记录验证 IC 0.0642117, 0.0647218, 0.0687591. 当前源报告和 run artifact 缺失, 不改变历史完成事实.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

Test whether validation IC decays materially across three rolling periods. 本文是registry证据汇总, 不是失踪原报告的重建副本.

## 数据与方法

| 项目 | 登记值 |
| --- | --- |
| experiment_id | rolling-purged-val |
| method | Rolling purged validation |
| dataset | stock1m · three folds |
| result_scope | three-fold rolling/purged validation IC stability check |

## 主要结果

| 登记字段及scope | 历史值 |
| --- | --- |
| fold0.best_iter | 190000 |
| fold0.best_val_pooled_ic | 0.06421174678243569 |
| fold0.best_val_rank_ic | 0.04205629203562068 |
| fold0.train_rows | 509088469 |
| fold0.val_rows | 43992960 |
| fold0.test_rows | 21831260 |
| fold0.train_range | 20210104-20230130 |
| fold0.val_range | 20230201-20230328 |
| fold0.test_range | 20230330-20230427 |
| fold1.best_iter | 20000 |
| fold1.best_val_pooled_ic | 0.0647218410451898 |
| fold1.best_val_rank_ic | 0.04759681457109594 |
| fold1.train_rows | 547188069 |
| fold1.val_rows | 46985620 |
| fold1.test_rows | 23557380 |
| fold1.train_range | 20211108-20231127 |
| fold1.val_range | 20231129-20240124 |
| fold1.test_range | 20240126-20240301 |
| fold2.best_iter | 50000 |
| fold2.best_val_pooled_ic | 0.06875912907436735 |
| fold2.best_val_rank_ic | 0.0547268777345416 |
| fold2.train_rows | 575970120 |
| fold2.val_rows | 47189340 |
| fold2.test_rows | 23664300 |
| fold2.train_range | 20220906-20240927 |
| fold2.val_range | 20241008-20241202 |
| fold2.test_range | 20241204-20241231 |
| aggregate.validation_pooled_ic_mean | 0.065898 |
| aggregate.validation_pooled_ic_range | 0.004547 |
| aggregate.validation_pooled_ic_min | 0.064212 |
| aggregate.validation_pooled_ic_max | 0.068759 |
| aggregate.fold2_minus_fold0 | 0.004547 |

## 限制与适用边界

三个 rolling/purged fold 已记录验证 IC 0.0642117, 0.0647218, 0.0687591. 当前源报告和 run artifact 缺失, 不改变历史完成事实. 原始文件, 选模协议和样本口径不齐时, 只保留已经登记的历史事实. 不对缺失字段插值, 不重扫prediction artifact.

## 结论

保留已成功的实验或诊断事实, 不因当前材料缺失判为失败. 正式结果未确认的部分保持待核对. Do not replace the architecture solely for temporal decay; trading decisions still require portfolio-level validation.

## 附录

事实来源: `nn-registry/rolling-purged-val/results.yaml`, `manifest.yaml`, `experiment-summary.md`. [全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

| 输入 | SHA256 |
| --- | --- |
| manifest | 23a291c8756bf137fd996ba8c716afcc382254294428e032b682de9525c0630e |
| results | 09c5e0d8e16634c25bd69587bd392add4d41ea7b90c42b6161dbf2f7c63a959b |
| experiment_summary | 5669b84afa8d01ea1682ed7b07aecff1debf84ff88d24c9f6061260294434182 |
