---
title: '学习率与 scheduler: 登记证据汇总'
date: 2026-11-03
summary: 固定 final iter110000 协议支持 warmup_cosine, lr=0.009, seeds 7/11/19 平均 test IC 为 0.0735400370. 更高学习率中的发散臂单列为失败.
tags:
- prediction-nn
- registry-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** 固定 final iter110000 协议支持 warmup_cosine, lr=0.009, seeds 7/11/19 平均 test IC 为 0.0735400370. 更高学习率中的发散臂单列为失败.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

Select a stable learning rate and scheduler under a fixed final-step protocol. 本文是registry证据汇总, 不是失踪原报告的重建副本.

## 数据与方法

| 项目 | 登记值 |
| --- | --- |
| experiment_id | learning-rate |
| method | Learning-rate / scheduler screen |
| dataset | stock1m · seeds 7/11/19 |
| result_scope | fixed final-step LR sweep, multi-seed validation, and scheduler/annealing seed-7 screening |

## 主要结果

| 登记字段及scope | 历史值 |
| --- | --- |
| protocol.final_iter | 110000 |
| protocol.approx_epoch | 1.6021206251183384 |
| protocol.train_batches_per_epoch | 68659 |
| protocol.test_count | 176945440 |
| recommended_config.scheduler | warmup_cosine |
| recommended_config.lr | 0.009 |
| recommended_config.seeds | 7 11 19 |
| recommended_config.invalid_seeds |  |
| recommended_config.mean_test_pearson_ic | 0.0735400370212493 |
| recommended_config.std_test_pearson_ic | 0.0019912444849537834 |
| recommended_config.min_test_pearson_ic | 0.07128834135462554 |
| recommended_config.max_test_pearson_ic | 0.07506894138600524 |
| recommended_single_runs.seed7_test_pearson_ic | 0.07506894138600524 |
| recommended_single_runs.seed11_test_pearson_ic | 0.07128834135462554 |
| recommended_single_runs.seed19_test_pearson_ic | 0.07426282832311709 |
| high_lr_caveats.lr_0p010_seed7_test_pearson_ic | 0.07513202884357204 |
| high_lr_caveats.lr_0p010_invalid_seeds | 11 |
| high_lr_caveats.lr_0p011_seed7_test_pearson_ic | 0.07471914814261545 |
| high_lr_caveats.lr_0p011_seed11_status | training divergence in logs; no final summary used |
| scheduler_screening.best_non_default_scheduler | warmup_constant |
| scheduler_screening.best_non_default_lr | 0.0015 |
| scheduler_screening.best_non_default_seed7_test_pearson_ic | 0.0723194489502549 |
| scheduler_screening.best_constant_lr | 0.0025 |
| scheduler_screening.best_constant_seed7_test_pearson_ic | 0.0702394020521372 |
| scheduler_screening.cosine_lr_0p008_seed7_test_pearson_ic | -4.3900240920652816e-05 |
| scheduler_screening.cosine_lr_0p009_seed7_test_pearson_ic | nan |
| scheduler_screening.warmup_cosine_slow_best_seed7_test_pearson_ic | 0.06378339703189607 |

## 限制与适用边界

固定 final iter110000 协议支持 warmup_cosine, lr=0.009, seeds 7/11/19 平均 test IC 为 0.0735400370. 更高学习率中的发散臂单列为失败. 原始文件, 选模协议和样本口径不齐时, 只保留已经登记的历史事实. 不对缺失字段插值, 不重扫prediction artifact.

## 结论

保留已成功的实验或诊断事实, 不因当前材料缺失判为失败. 正式结果未确认的部分保持待核对. Use warmup_cosine + 0.009 for later runs with the same model, batch, data, and training length.

## 附录

事实来源: `nn-registry/learning-rate/results.yaml`, `manifest.yaml`, `experiment-summary.md`. [全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

| 输入 | SHA256 |
| --- | --- |
| manifest | cb3e65262a1b121e15c1530a5caccad4015ee2aaf9302c2dee1e0830ac54b1c7 |
| results | eaed5f49ead36fa316cfef5dd6cfea82ce216079c17011e58bf804823a99897c |
| experiment_summary | 3b2ec8fedd4610fcd1565ccc2cf79482c3d8a4832078b56322ec4bf8089ce8bd |
