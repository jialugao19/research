---
title: 36D feature-set evaluation | 0825-feature-audit-model-report-0827
date: 2026-11-03
summary: 36D单臂完成全链路, iter6762覆盖176134322行test. Gross累计收益260.18%, 10M net累计收益−96.58%. 无 matched旧特征control, 中央结果未记录pooled IC scalar.
tags:
- prediction-nn
- registry-sync
- historical-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** 36D单臂完成全链路, iter6762覆盖176134322行test. Gross累计收益260.18%, 10M net累计收益−96.58%. 无 matched旧特征control, 中央结果未记录pooled IC scalar.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

本报告围绕36D feature-set evaluation整理原始研究证据. 当前材料对应 registry report `0825-feature-audit-model-report-0827`, 来源SHA256为 `db7f7513162250627a845994f4c78ba23739a7732d4a730cac196030c3dc494b`. 原报告的实验方法, 图表, 结果和解释保留在下文.

## 数据与方法

实验身份为 `0825-feature-audit`. Split, label, sampler, feature与checkpoint定义按原报告记录, 不从其他实验借用缺失字段. 汇总入口见[全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

## 主要结果

| 记录项 | 当前解释 |
| --- | --- |
| 实验 | 0825-feature-audit |
| 报告类型 | full_report_html |
| 历史状态 | 历史成功 |
| 证据 | 0825-feature-audit-model-report-0827 |

Current conclusion

预测数据, 训练 checkpoint 与正式评估均已形成版本化证据; 组合收益结论需在 backtest stage 完成后单独判断. 

01

Decision snapshot

### 当前证据覆盖到哪里

此页只总结已完成且能由 manifest 追溯的事实, 不把缺失的组合回测解释为零收益. 

Features

36

0827_features

Label

log_close[t+11] - log_close[t+1]

forward log return

Best checkpoint

6762

validation-selected

02

Data & model contract

### 输入, 模型与训练语义

日期切分, 特征顺序, 标签端点和一个 epoch 的 global shuffle 都属于 run 身份; 改变任一项都必须使用新 run. 

Train rows

553895223

prepared samples

Validation rows

31737447

prepared samples

Test rows

176134322

prepared samples

GRU

384 × 2

hidden × layers

MLP

512 → 512

hidden dimensions

Training

1 epoch

global_shuffle

03

Evaluation evidence

### 正式预测产物

evaluation manifest 固定所选 checkpoint 及 test/inference 入口. Rank IC 的 ties 采用 average rank; 未定义统计量显示为 —. 

| Artifact | Value |
| --- | --- |
| best_iteration | 6762 |
| test_manifest | [artifact-root]/nn/baseline-1min-0813/0827-features-seed7-full-71b01ce-backtestfix/prediction/run/eval_test/iter_6762/predict_manifest.yaml |
| inference_manifest | [artifact-root]/nn/baseline-1min-0813/0827-features-seed7-full-71b01ce-backtestfix/prediction/run/inference_test/iter_6762/inference_manifest.yaml |

04

Reproducibility

### Stage checkpoint

每个 stage 由 schema, 配置摘要和上游 manifest 摘要串联; 不满足身份校验时恢复会失败. 

| Stage | Status | Completed UTC | Schema |
| --- | --- | --- | --- |
| prepare | complete | 2026-08-27T13:59:42.862410+00:00 | prediction-nn/dataset-v2 |
| train | complete | 2026-08-27T18:36:17.399134+00:00 | prediction-nn/training-v2 |
| evaluate | complete | 2026-08-27T19:08:30.240484+00:00 | prediction-nn/evaluation-v2 |

## 限制与适用边界

36D单臂完成全链路, iter6762覆盖176134322行test. Gross累计收益260.18%, 10M net累计收益−96.58%. 无 matched旧特征control, 中央结果未记录pooled IC scalar. 当前artifact可得性只影响复现, 不作为历史成功/失败判据. 只有matched合同内的结果可以直接比较.

## 结论

本次归档保留上述历史事实. 研究结论, 推广门槛和执行限制分别解释, 不把模型无增益或净收益为负改写成实验流程失败.
