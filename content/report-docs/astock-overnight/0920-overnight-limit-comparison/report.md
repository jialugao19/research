---
title: Signal-time 锁板过滤对照研究
date: 2026-09-20
summary: 直接过滤影响极小, retraining 改变 extreme tail, 单 seed evidence 不支持 performance upgrade.
tags:
- overnight
- research
featured: false
---

## 摘要

直接过滤影响极小, retraining 改变 extreme tail, 单 seed evidence 不支持 performance upgrade.

后续独立 ledger audit 已确认旧 Validation gross ledger 未排除 split boundary positions. 13:58 baseline 的 corrected gross return 为 20.1322%, Sharpe 为 1.552499; 13:50 为 10.7110%, Sharpe 为 0.838975. 旧表、旧图作为历史 evidence 保留, 相应 Validation long-only 数值以 [ledger audit](/reports/astock-overnight/1016-overnight-ledger-audit/) 为准. 未对未审计的 CSI1800、其他 tail 或方案 A 结果推算更正值.

## 研究背景与目标

研究问题与数据合同以保留的源报告为准. 本页将既有研究证据登记为独立 publication, 关联对应 Study 与 Experiment.

## 数据与方法

2021-2023 为 Train; 2024 Validation 排除 9-10 月. 历史报告中的 2025 one-shot Test 已被查看, 当前仅能作为 historical confirmation, 不支持再次用其选择配置. 本次同步仅整理既有 evidence, 未训练、推理或重跑回测.

## 主要结果


### 1. Executive summary

本研究检验一个明确问题: baseline 将 D 13:58 锁涨跌停股票保留在 prediction group, 是否高估了现有报告结果. 方案 A 在 factor-complete 后, 从 Train, Validation 和 Test prediction group 中统一排除这些 stock-day, 再使用相同模型配置重新训练和评价.

核心结论如下:

1. Baseline 与方案 A 的唯一主动实验变量是 D 13:58 锁涨跌停 sample policy. Raw data, factor, factor context universe, split, normalization 方法, Dual-GRU, loss, hyperparameters, seed 和 evaluation 规则保持一致.
2. 方案 A 只删除 140 个 prediction rows, 占 baseline 的 0.0178%. 其中 Train 实际减少 68 个 trainable observations.
3. 使用 baseline predictions 直接删除这些样本并重新排序后, Test RankIC, decile 和 Top-tail 几乎不变. 因此, baseline 没有因这些样本直接留在报告中而产生可见的 performance 高估.
4. 方案 A 重训后, Test RankIC 略降. All-market Q10 和极端 Top-tail 提高, 但 CSI1800 Q10-Q1 未提高. 这是 mixed result, 不能解释为方案 A 稳定优于 baseline.
5. Top 1% 和 Top 0.5% 的较大改善来自 retraining 后的 ranking 变化, 不是机械删除锁涨跌停股票. 单 seed 不足以证明该 tail 改善可复现.

因此, 是否采用方案 A 应由 prediction universe 的语义决定, 不应由本次单次训练的 tail return 决定.

---

### 2. Baseline 与方案 A 的核心区别

### 2.1 实验变量

| 维度 | Baseline | 方案 A | 影响 |
| --- | --- | --- | --- |
| D 13:58 locked-up | 保留在 prediction group | 排除 | 改变 Train, Validation, Test 样本池 |
| D 13:58 locked-down | 保留在 prediction group | 排除 | 即使 14:00 可买, 仍不参与 prediction |
| Locked-up 定义 | 不用于样本过滤 | `Low >= up_limit - 0.01` | 使用 D 13:58 bar |
| Locked-down 定义 | 不用于样本过滤 | `High <= down_limit + 0.01` | 使用 D 13:58 bar |
| 14:00 entry feasibility | 锁涨停不可买 | 完全相同 | 不属于本实验变量 |
| Factor context universe | 原 universe | 完全相同 | 横截面因子计算口径不变 |
| Factor completeness | 缺 factor 的 stock-day 删除 | 完全相同 | 先完成 factor 检查, 再应用方案 A |
| Target z-score | 在 baseline trainable rows 内按日计算 | 过滤后在剩余 trainable rows 内按日重算 | 训练 label 有轻微变化 |
| Model 与训练配置 | Dual-GRU, seed 42 | 完全相同, 从头重训 | 不复用 baseline checkpoint |
| Evaluation population | 包含 factor-complete 的 13:58 锁板样本 | 不包含这些样本 | 报告 population 随 policy 改变 |

实现位于 `astock_overnight/sample_filter.py` 和 `astock_overnight/feature_pipeline.py`. Baseline 使用 `configs/dataset-pipeline.yaml`; 方案 A 使用 `configs/dataset-pipeline-exclude-signal-limits.yaml`, `configs/experiment-exclude-signal-limits.yaml` 和 `configs/evaluation-exclude-signal-limits.yaml`.

### 2.2 13:58 sample policy 与 14:00 execution rule 是两个边界

```text
Baseline:
factor-complete
  -> prediction group
  -> 14:00 entry audit
  -> tradable / not tradable

方案 A:
factor-complete
  -> exclude D 13:58 locked-up and locked-down
  -> prediction group
  -> same 14:00 entry audit
  -> tradable / not tradable
```

Baseline 在 13:58 生成 prediction, 之后由 14:00 execution bar 判断能否建立 position. 股票可能在 13:58 锁涨停, 但在 14:00 已打开涨停, 此时 baseline 仍允许买入. 方案 A 会更早删除该样本, 不再考虑 14:00 是否已经打开.

差异对 locked-down 更明显. 当前 14:00 entry rule 只禁止锁涨停买入, 不禁止跌停附近买入. 方案 A 则在 13:58 直接排除 locked-down stock-day. 因而, 方案 A 不是单纯修正 execution feasibility, 而是在定义一个更保守的 signal-time prediction universe.

### 2.3 保持不变的研究边界

- Signal time 固定为 D 13:58 bar 结束, 即 `MinuteIndex=178`.
- Entry time 固定为 D 14:00 execution bar.
- Raw data run, factor run 和 cross-sectional factor context 不变.
- Train 为 2021-2023, Validation 为 2024 且排除 9-10 月, Test 为 2025.
- 模型结构, loss, optimizer, batching, hyperparameters 和 random seed 不变.
- Decile, Top-tail, IC 和 event-driven long-only evaluation 规则不变.

这些控制使结果只反映 sample policy 变化及其下游 retraining effect.

---

### 3. Artifact 与样本变化

| 项目 | Baseline | 方案 A |
| --- | ---: | ---: |
| Dataset | `20260917T162415Z` | `20260919T174500Z` |
| Experiment | `20260918T082705Z` | `20260920T030509Z` |
| Evaluation | `20260918T141822Z` | `20260920T031000Z` |
| Prediction rows | 786,169 | 786,029 |
| Train prediction rows | 442,129 | 442,037 |
| Train trainable rows | 441,574 | 441,506 |
| Validation prediction rows | 131,881 | 131,866 |
| Test prediction rows | 212,159 | 212,126 |

Raw candidate 层识别出 56,738 个 locked-up 和 11,982 个 locked-down rows. 大部分在此前已经因 factor incomplete 被删除. 最终进入本实验差异的只有 35 个 locked-up 和 105 个 locked-down rows, 合计 140 行, 占 baseline prediction rows 的 0.0178%.

| Year | 删除 prediction rows | 删除 trainable/evaluable rows | 占对应 split prediction rows 的比例 |
| --- | ---: | ---: | ---: |
| 2021 | 33 | 18 | Train 三年合计 0.0208% |
| 2022 | 38 | 32 | Train 三年合计 0.0208% |
| 2023 | 21 | 18 | Train 三年合计 0.0208% |
| 2024 | 15 | 13 | 0.0114% |
| 2025 | 33 | 31 | 0.0156% |

11 个 raw candidates 缺少同日 daily price-limit row, 被标记为 `unavailable`. 它们全部 factor-incomplete, 未进入 baseline 或方案 A 的最终 prediction rows. Pipeline 对 factor-complete 且 `unavailable` 的行直接报错.

---

### 4. OOS 核心结果

表中 bps 表示 daily mean cohort return. Total return 和 maximum drawdown 来自 event-driven long-only ledger, 未扣 transaction cost. `Delta` 为方案 A 减 baseline.

### 4.1 All-market

| Metric | Baseline | 方案 A | Delta |
| --- | ---: | ---: | ---: |
| Validation RankIC | 0.147947 | 0.144927 | -0.003020 |
| Validation Q10-Q1, bps | 136.103 | 135.855 | -0.249 |
| Test RankIC | 0.114489 | 0.113206 | -0.001283 |
| Test Q10, bps | 9.120 | 10.709 | +1.589 |
| Test Q10-Q1, bps | 76.523 | 79.057 | +2.533 |
| Test decile monotonicity | 0.7333 | 0.6606 | -0.0727 |
| Test event long-only total return | 23.72% | 28.56% | +4.84 pp |
| Test event long-only maximum drawdown | -6.94% | -6.47% | +0.47 pp |
| Test terminal break-even | 4.289 bps | 5.116 bps | +0.826 bps |

All-market 中, 方案 A 的 Test Q10 和 Q10-Q1 提高, 但 RankIC 与 decile monotonicity 下降. Long-only total return 提高 4.84 pp, 同时 break-even cost 提高 0.826 bps. 这不是所有排序指标一致改善.

### 4.2 CSI1800

| Metric | Baseline | 方案 A | Delta |
| --- | ---: | ---: | ---: |
| Validation RankIC | 0.084555 | 0.080629 | -0.003926 |
| Validation Q10-Q1, bps | 45.220 | 45.252 | +0.032 |
| Test RankIC | 0.060210 | 0.059486 | -0.000723 |
| Test Q10, bps | 8.787 | 8.839 | +0.052 |
| Test Q10-Q1, bps | 30.136 | 29.388 | -0.748 |
| Test decile monotonicity | 0.2242 | 0.3576 | +0.1333 |
| Test event long-only total return | 22.98% | 23.03% | +0.05 pp |
| Test event long-only maximum drawdown | -6.56% | -7.08% | -0.52 pp |
| Test terminal break-even | 4.174 bps | 4.198 bps | +0.025 bps |

CSI1800 中, Test RankIC 和 Q10-Q1 均下降, Q10 与 total return 基本不变, maximum drawdown 变差. 方案 A 在 all-market 的收益改善没有稳定扩展到 CSI1800.

### 4.3 2021-2025 all-market

2021-2023 是 train in-sample, 2024 是 selected Validation, 2025 是 one-shot Test.

| Year | RankIC, Baseline -> A | Q10, Baseline -> A | Q10-Q1, Baseline -> A | Event long total return, Baseline -> A |
| --- | ---: | ---: | ---: | ---: |
| 2021 | 0.103713 -> 0.103658 | 14.450 -> 15.325 bps | 93.693 -> 94.151 bps | 41.02% -> 43.90% |
| 2022 | 0.122798 -> 0.124364 | 4.823 -> 6.689 bps | 111.150 -> 113.802 bps | 11.29% -> 16.28% |
| 2023 | 0.135692 -> 0.133586 | 7.797 -> 8.874 bps | 100.618 -> 103.198 bps | 20.84% -> 24.01% |
| 2024 | 0.147947 -> 0.144927 | 9.359 -> 9.705 bps | 136.103 -> 135.855 bps | 16.72% -> 17.56% |
| 2025 | 0.114489 -> 0.113206 | 9.120 -> 10.709 bps | 76.523 -> 79.057 bps | 23.72% -> 28.56% |

年度结果同样表现为 RankIC 与 long-only return 不同步. 方案 A 的收益曲线在多年度提高, 但 Validation 和 Test RankIC 均下降.

---

### 5. Test Top-tail 结果

| Scope | Selection | Cohort mean, Baseline -> A | Event total return, Baseline -> A |
| --- | --- | ---: | ---: |
| All-market | Top 5% | 9.409 -> 9.286 bps | 24.91% -> 24.34% |
| All-market | Top 1% | 13.363 -> 16.176 bps | 37.26% -> 46.81% |
| All-market | Top 0.5% | 15.368 -> 19.659 bps | 43.77% -> 59.22% |
| CSI1800 | Top 5% | 7.551 -> 9.747 bps | 19.41% -> 25.85% |
| CSI1800 | Top 1% | 12.556 -> 15.600 bps | 34.57% -> 44.76% |
| CSI1800 | Top 0.5% | 12.801 -> 15.389 bps | 34.95% -> 43.38% |

方案 A 的 Top 1% 和 Top 0.5% 明显提高, 但 Top 5% 并未在 all-market 改善. 该形态说明变化集中在极端 tail, 需要通过 decomposition 判断来源.

---

### 6. 直接过滤效应与重新训练效应

`Baseline filtered` 使用 baseline checkpoint 的原 predictions, 只删除方案 A 的样本并重新计算 decile 和 Top-tail. `方案 A retrained` 则使用过滤后的 Train dataset 从头训练. 两者分别回答以下问题:

1. 直接过滤效应: baseline 报告是否因为保留锁涨跌停行而被机械高估.
2. 重新训练效应: 删除少量训练 observations 后, 模型参数和 ranking 如何变化.

### 6.1 All-market Test

| Metric | Baseline | Baseline filtered | 方案 A retrained |
| --- | ---: | ---: | ---: |
| RankIC | 0.114489 | 0.114460 | 0.113206 |
| Q10, bps | 9.120 | 9.144 | 10.709 |
| Q10-Q1, bps | 76.523 | 76.627 | 79.057 |
| Top 5%, bps | 9.409 | 9.418 | 9.286 |
| Top 1%, bps | 13.363 | 13.363 | 16.176 |
| Top 0.5%, bps | 15.368 | 15.368 | 19.659 |

### 6.2 CSI1800 Test

| Metric | Baseline | Baseline filtered | 方案 A retrained |
| --- | ---: | ---: | ---: |
| RankIC | 0.060210 | 0.060208 | 0.059486 |
| Q10, bps | 8.787 | 8.792 | 8.839 |
| Q10-Q1, bps | 30.136 | 30.092 | 29.388 |
| Top 5%, bps | 7.551 | 7.567 | 9.747 |
| Top 1%, bps | 12.556 | 12.556 | 15.600 |
| Top 0.5%, bps | 12.801 | 12.801 | 15.389 |

直接过滤对 Test 指标几乎没有影响. All-market Test 删除的 33 行中, baseline 只有 1 行位于 Q10/Top 5%, 没有行位于 Top 1% 或 Top 0.5%. 因此, Top 1% 和 Top 0.5% 的改善完全来自 retraining 后的 ranking 变化, 不是删除高收益或低收益股票的机械结果.

共同样本上的 daily mean prediction Rank correlation 为 Train 0.9819, Validation 0.9851, Test 0.9835. Test Top 5%/1%/0.5% 对 baseline 成员的保留率分别为 83.0%, 78.4%, 77.2%. 模型整体 ranking 高度相近, 但 extreme tail membership 对这次轻微训练集变化较敏感.

---

### 7. 结果解释与方案选择

### 7.1 Baseline 是否高估表现

没有观察到可见的直接高估. `Baseline filtered` 与 baseline 的 Test 指标几乎一致, 且被删除样本很少进入 baseline 的高分组. 方案 A 重训后的收益差异不能作为 baseline 被高估的证据.

### 7.2 方案 A 是否更好

当前证据不支持把方案 A 定义为 performance upgrade:

- Validation 和 Test RankIC 都下降.
- All-market Q10, Q10-Q1 和 long-only return 提高.
- CSI1800 Q10-Q1 下降, total return 基本不变, drawdown 变差.
- Top 1% 和 Top 0.5% 提高, 但来自 retraining-induced reranking.
- 实验只有一个 deterministic seed, 未验证 tail improvement 对训练扰动的稳定性.

### 7.3 两个方案各自对应的研究语义

| 研究目标 | 更匹配的方案 | 原因 |
| --- | --- | --- |
| 13:58 对全部 eligible stocks 预测, 14:00 再判断能否成交 | Baseline | 允许 13:58 锁板但 14:00 已打开的股票参与交易 |
| Signal time 即排除所有锁涨跌停状态 | 方案 A | 使用更保守的 prediction universe, 不等待 14:00 状态变化 |

方案 A 同时排除 locked-up 和 locked-down, 语义强于现有 14:00 entry feasibility. 如果采用方案 A, 应将其视为 prediction universe policy, 而不是 execution rule 的修复.

---

### 8. 最终结论

1. 本次对照没有发现 baseline 因保留 D 13:58 锁涨跌停样本而直接高估 IC, decile 或 Top-tail performance.
2. 方案 A 对样本量的直接影响极小, 但少量训练样本变化足以改变 extreme tail membership 和收益. 这说明当前 tail result 对 training path 存在敏感性.
3. 方案 A 的结果是 mixed: IC 略降, all-market tail 改善, CSI1800 spread 未改善. 单次结果不足以支持 performance 层面的替换.
4. 最终选择应固定在研究语义上. Baseline 表达 "13:58 预测, 14:00 决定能否买入"; 方案 A 表达 "13:58 锁涨跌停股票不属于 prediction universe".

方案 A 的完整 self-contained HTML report 已复制到 `reports/signal-limit-sample-filter-plan-a.html`, 已通过 `scripts/validate_html_report.py`.

## 限制与适用边界

后续独立 ledger audit 已确认旧 Validation gross ledger 未排除 split boundary positions. 13:58 baseline 的 corrected gross return 为 20.1322%, Sharpe 为 1.552499; 13:50 为 10.7110%, Sharpe 为 0.838975. 旧表、旧图作为历史 evidence 保留, 相应 Validation long-only 数值以 [ledger audit](/reports/astock-overnight/1016-overnight-ledger-audit/) 为准. 未对未审计的 CSI1800、其他 tail 或方案 A 结果推算更正值.

2021-2023 为 Train; 2024 Validation 排除 9-10 月. 历史报告中的 2025 one-shot Test 已被查看, 当前仅能作为 historical confirmation, 不支持再次用其选择配置. 本次同步仅整理既有 evidence, 未训练、推理或重跑回测.

## 结论

直接过滤影响极小, retraining 改变 extreme tail, 单 seed evidence 不支持 performance upgrade.

## 附录

来源: `astock-overnight/reports/signal-limit-sample-filter-comparison.md`.

Source SHA-256: `0eed27399b3658e4fcdc31a05f976c0984f530fd15b036964c4ecaeb5a65cdaa`.

同步日期: 2026-11-03. 原始归档保留源字节; 本内容包仅移除机器本地路径, 不重新计算研究指标.
