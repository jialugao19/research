---
title: 41D latent-z 冻结模型 | 0903-model-full-report
date: 2026-11-03
summary: 41D latent-z selected iter105343 的full-test IC/RankIC为0.1270440556/0.1012013681. 10M净累计收益−93.66%, 仅支持冻结的shadow inference与研究比较.
tags:
- prediction-nn
- registry-sync
- historical-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** 41D latent-z selected iter105343 的full-test IC/RankIC为0.1270440556/0.1012013681. 10M净累计收益−93.66%, 仅支持冻结的shadow inference与研究比较.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

本报告围绕41D latent-z 冻结模型整理原始研究证据. 当前材料对应 registry report `0903-model-full-report`, 来源SHA256为 `8f54662edf549450ad665531e2ac8b3638134c7d03cbd254b446712cd370f73d`. 原报告的实验方法, 图表, 结果和解释保留在下文.

## 数据与方法

实验身份为 `0903-model`. Split, label, sampler, feature与checkpoint定义按原报告记录, 不从其他实验借用缺失字段. 汇总入口见[全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

## 主要结果

| 记录项 | 当前解释 |
| --- | --- |
| 实验 | 0903-model |
| 报告类型 | full_report_html |
| 历史状态 | 历史成功 |
| 证据 | 0903-model-full-report |

Current conclusion

Test pooled IC=0.127044, Rank IC=0.101201; 相对历史 off/off 的方向性差值为 +0.003751 / +0.008370. 10M AUM 成本后日均收益为 -1.341%, 因此本单 seed 结果不支持模型 promotion 或交易结论. 

01

Executive summary

### 绝对结果与参考差值

指标来自所选 checkpoint 的完整 test manifest; 差值只用于方向性描述. 

Test pooled IC

0.127044

n=176,134,322

Test Rank IC

0.101201

global average-tie ranks

Δ IC vs historical

+0.003751

different code commits

Δ Rank IC vs historical

+0.008370

different code commits

Gross daily return

1.008%

execution-aware, before cost

Net daily return · 10M

-1.341%

after configured spread + impact

02

Method

### 模型, 数据与实验控制

除 context 开关外, 三条 treatment 共享同一 41D 数据, 标签, split, normalization, market-panel batch, 优化器, 训练预算, 选择规则和评估口径. 

| Field | Value |
| --- | --- |
| Contexts | latent_z |
| Seed | 7 |
| Feature count | 41 |
| Dataset cache key | e74adc442d96d5ecfcd932bd39289a25be2366d12c20d78a83d8f9aeda2a3460 |
| Artifact ID | 6589947466234739b27e243d253a3c48 |
| Panel fingerprint | 28573283d9bba84f03cb51f8855fe97b16e99fba1912860c461e58084518926d |
| Artifact reused | true |

03

Checkpoint evidence

### Validation-only checkpoint selection

最终 test 只使用 validation 规则选出的 checkpoint; test 指标不参与选择. 

Selected iteration

105,343

early top-k rule

Validation IC

0.138962

selected checkpoint

Validation Rank IC

0.125709

selected checkpoint

| Selection score | Score rank | Checkpoint SHA-256 |
| --- | --- | --- |
| 0.077588 | 1 | 78a9c780724b64e69a62f0083cab8a0aabd85c9888f7e42b04a030c7b0ab05c4 |

04

Signal quality

### 完整 test 与历史参考

Pearson IC 与 Rank IC 均对完整 test 样本池计算. 历史行只提供量级和方向参考, 不是同一代码提交下的严格 off/off control. 

| Arm | Role | Pooled IC | Rank IC | Δ IC | Δ Rank IC | Count |
| --- | --- | --- | --- | --- | --- | --- |
| cs_rank_41d | historical reference | 0.123293 | 0.092832 | reference | reference | 176,134,322 |
| main_41d_latent_z | treatment | 0.127044 | 0.101201 | +0.003751 | +0.008370 | 176,134,322 |

05

Portfolio evidence

### Execution-aware 回测

相同 long/short, top 10%, 成交限制, spread, square-root impact 和 10M AUM 口径. gross 与 net 的反转表明容量/成本约束不可忽略. 

| Arm | Gross daily | Gross Sharpe | Net daily · 10M | Net Sharpe · 10M | Net max DD | Turnover | Fill | Capacity @10bps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cs_rank_41d | 0.872% | 45.395 | -1.500% | -39.748 | -95.437% | 11.556 | 94.011% | ¥94,529 |
| main_41d_latent_z | 1.008% | 45.417 | -1.341% | -36.958 | -93.659% | 11.812 | 94.016% | ¥96,729 |

06

Infrastructure

### 调度, 追踪与资源记录

本臂由 Prefect group flow 调度, 训练写入 MLflow, 并由独立资源监控器留痕. 

| Field | Value |
| --- | --- |
| Prefect flow run | 567993a4-bd83-4406-ba1a-56367920ff40 |
| MLflow run | 90b639c3b20642e8a973a74c326c8a21 |
| Training Git commit | d5b117691b44d01b8ec285ab99a98cb1e16bb1b4 |
| Report builder commit | 18d8ebedf4892482289a410dedf1bad2ca441e7f |
| Resource samples | 655 |
| Resource violations | 0 |
| Peak GPU memory | 9,298 MiB |

## 限制与适用边界

41D latent-z selected iter105343 的full-test IC/RankIC为0.1270440556/0.1012013681. 10M净累计收益−93.66%, 仅支持冻结的shadow inference与研究比较. 当前artifact可得性只影响复现, 不作为历史成功/失败判据. 只有matched合同内的结果可以直接比较.

## 结论

本次归档保留上述历史事实. 研究结论, 推广门槛和执行限制分别解释, 不把模型无增益或净收益为负改写成实验流程失败.
