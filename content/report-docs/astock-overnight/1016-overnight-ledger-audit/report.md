---
title: Long-only event ledger 独立审计与更正
date: 2026-10-16
summary: 修复 Validation split eligibility 与 initial-NAV drawdown; 发布 corrected ledger
  与 cost replay.
tags:
- overnight
- research
featured: false
---

## 摘要

修复 Validation split eligibility 与 initial-NAV drawdown; 发布 corrected ledger 与 cost replay.

更正范围限原文审计的 all-market Q10 arms. 没有对其他 cohort 或其他模型的历史指标做外推.

## 研究背景与目标

研究问题与数据合同以保留的源报告为准. 本页将既有研究证据登记为独立 publication, 关联对应 Study 与 Experiment.

## 数据与方法

2021-2023 为 Train; 2024 Validation 排除 9-10 月. 历史报告中的 2025 one-shot Test 已被查看, 当前仅能作为 historical confirmation, 不支持再次用其选择配置. 本次同步仅整理既有 evidence, 未训练、推理或重跑回测.

## 主要结果


### 结论

确认并修复两个问题.

1. High: 原 evaluation ledger 没有应用预先定义的 split eligibility, Validation 错误纳入 `purged_boundary` positions. 这些 positions 来自 2024-08-30 和 2024-12-31, 后者的退出收益跨入 2025. 修复后建仓条件为 `Q10 + tradable + is_split_eligible`; `realized_return` 是否 finite 只作为建仓集合固定后的 fail-fast invariant, 不再作为 entry filter.
2. Medium: gross ledger 的 drawdown running peak 未包含 initial NAV=1.0, 因此首个 ledger day 的亏损会被记为 0 drawdown. 修复后所有 event-driven ledger 共用 `initial capital + daily NAV` 的 running peak. 当前四条 OOS 路径的最终 MDD 均由后续更深 trough 决定, 所以该修复没有改变这四个已报告 MDD, 但修复了通用实现.

未发现额外的未来信息泄漏、买卖时序错序、现金或持仓不守恒、复权收益不一致、延迟退出提前释放资金等问题. 所有实际 Q10 exits 均早于 14:00, 因此不存在 exit 与当日 14:00 entry window 重叠.

### 修正影响

| Arm | Period | Purged positions | Published NAV | Corrected NAV | Published Sharpe | Corrected Sharpe | Published MDD | Corrected MDD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 13:58 baseline | validation | 161 | 1.167240 | 1.201322 | 1.309981 | 1.552499 | -4.71% | -4.71% |
| 13:58 baseline | test | 0 | 1.237166 | 1.237166 | 1.879994 | 1.879994 | -6.94% | -6.94% |
| 13:50 | validation | 163 | 1.087437 | 1.107110 | 0.699530 | 0.838975 | -8.17% | -8.17% |
| 13:50 | test | 0 | 1.377233 | 1.377233 | 2.497198 | 2.497198 | -5.91% | -5.91% |

`Test 2025` 没有 purged positions, 因此修正前后 gross 路径一致. `Validation 2024` 的 long-only 结果必须使用 corrected 值.

### 逐笔与时序检查

| Arm | Period | NAV identity error | Legacy replay NAV error | Return formula error | Published DD path error | Purged dates | Partial purge dates | Delayed exits | Max delay min | Exit >=14:00 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 13:58 baseline | validation | 0.000000 | 0.000000 | 0.000000 | 0.36% | 2024-08-30, 2024-12-31 | 0 | 2 | 452 | 0 |
| 13:58 baseline | test | 0.000000 | 0.000000 | 0.000000 | 0.78% | none | 0 | 9 | 2380 | 0 |
| 13:50 | validation | 0.000000 | 0.000000 | 0.000000 | 0.33% | 2024-08-30, 2024-12-31 | 0 | 3 | 452 | 0 |
| 13:50 | test | 0.000000 | 0.000000 | 0.000000 | 0.80% | none | 0 | 12 | 2380 | 0 |

`Purged dates` 只包含 2024-08-30 和 2024-12-31, 所有 purged Q10 positions 的 delay 均为 0, `Partial purge dates` 也均为 0. 因此修正等价于删除完整 boundary signal dates, 不会按个股未来 exit state 选择性保留 positions. `Delayed exits` 统计实际退出晚于 planned 10:00 window 的 positions. `Max delay min` 使用交易分钟, 午休和隔夜不计入. 独立 replay 仅在实际 exit event 到达后释放现金; 在此之前 position 按 raw daily `close * adj_factor` 估值. `Exit >=14:00` 用于识别退出与下一次 14:00 建仓的同日资金时序; 本次为 0.

### Cost replay

Cost grid 沿用 `configs/strategy-research.yaml` 的 `0/5/10/15/20/30/50 bps`. Cost 定义为每个 non-writeoff position 在退出时按 entry notional 一次性扣除 all-in round-trip cost; 不含额外 impact 或 minimum commission.

| Arm | Period | Cost bps | NAV | Return | Sharpe | MDD |
| --- | --- | --- | --- | --- | --- | --- |
| 13:58 baseline | validation | 0.0 | 1.201322 | 20.13% | 1.552499 | -4.71% |
| 13:58 baseline | validation | 5.0 | 1.085456 | 8.55% | 0.728568 | -5.91% |
| 13:58 baseline | validation | 10.0 | 0.980715 | -1.93% | -0.097474 | -8.01% |
| 13:58 baseline | validation | 15.0 | 0.886037 | -11.40% | -0.924284 | -14.63% |
| 13:58 baseline | validation | 20.0 | 0.800458 | -19.95% | -1.750510 | -21.05% |
| 13:58 baseline | validation | 30.0 | 0.653199 | -34.68% | -3.395838 | -34.68% |
| 13:58 baseline | validation | 50.0 | 0.434705 | -56.53% | -6.621739 | -56.53% |
| 13:58 baseline | test | 0.0 | 1.237166 | 23.72% | 1.879994 | -6.94% |
| 13:58 baseline | test | 5.0 | 1.095994 | 9.60% | 0.843171 | -9.44% |
| 13:58 baseline | test | 10.0 | 0.970873 | -2.91% | -0.194780 | -12.59% |
| 13:58 baseline | test | 15.0 | 0.859986 | -14.00% | -1.233803 | -15.68% |
| 13:58 baseline | test | 20.0 | 0.761717 | -23.83% | -2.273844 | -24.41% |
| 13:58 baseline | test | 30.0 | 0.597477 | -40.25% | -4.356754 | -40.65% |
| 13:58 baseline | test | 50.0 | 0.367338 | -63.27% | -8.532293 | -63.44% |
| 13:50 | validation | 0.0 | 1.107110 | 10.71% | 0.838975 | -8.17% |
| 13:50 | validation | 5.0 | 1.000289 | 0.03% | 0.067596 | -10.85% |
| 13:50 | validation | 10.0 | 0.903729 | -9.63% | -0.704782 | -14.65% |
| 13:50 | validation | 15.0 | 0.816449 | -18.36% | -1.477059 | -19.56% |
| 13:50 | validation | 20.0 | 0.737560 | -26.24% | -2.248135 | -26.24% |
| 13:50 | validation | 30.0 | 0.601822 | -39.82% | -3.782318 | -39.82% |
| 13:50 | validation | 50.0 | 0.400446 | -59.96% | -6.789539 | -59.96% |
| 13:50 | test | 0.0 | 1.377233 | 37.72% | 2.497198 | -5.91% |
| 13:50 | test | 5.0 | 1.219997 | 22.00% | 1.576664 | -7.13% |
| 13:50 | test | 10.0 | 1.080648 | 8.06% | 0.655134 | -8.76% |
| 13:50 | test | 15.0 | 0.957157 | -4.28% | -0.267355 | -10.56% |
| 13:50 | test | 20.0 | 0.847727 | -15.23% | -1.190762 | -16.14% |
| 13:50 | test | 30.0 | 0.664850 | -33.52% | -3.040179 | -34.17% |
| 13:50 | test | 50.0 | 0.408643 | -59.14% | -6.748320 | -59.46% |

### 可复现证据

- Independent legacy replay 对原 positions 和 daily ledger 的 sample ids、entry/exit notional、cash、invested value 和 NAV 逐笔/逐日复算, 最大误差不超过 `1e-12`.
- Corrected replay 从 frozen predictions、raw daily close、adj_factor 和 trade calendar 重建, 不读取 published NAV 作为输入.
- `realized_return` 逐行按 `(exit_price * exit_adj_factor) / (entry_price * entry_adj_factor) - 1` 复算.
- Cash identity 固定为 `NAV = cash + invested_value`; delayed positions 在实际 exit event 前保留在 active state.
- Machine-readable evidence: `long-only-event-ledger-audit-evidence.json`, `long-only-event-ledger-cost-grid.csv`, `long-only-event-ledger-cost-daily.parquet`, `long-only-event-ledger-corrected-positions.parquet`.
- One-command rebuild: `python scripts/audit_event_portfolio.py`.

## 限制与适用边界

更正范围限原文审计的 all-market Q10 arms. 没有对其他 cohort 或其他模型的历史指标做外推.

2021-2023 为 Train; 2024 Validation 排除 9-10 月. 历史报告中的 2025 one-shot Test 已被查看, 当前仅能作为 historical confirmation, 不支持再次用其选择配置. 本次同步仅整理既有 evidence, 未训练、推理或重跑回测.

## 结论

修复 Validation split eligibility 与 initial-NAV drawdown; 发布 corrected ledger 与 cost replay.

## 附录

来源: `astock-overnight/reports/long-only-event-ledger-audit.md`.

Source SHA-256: `6422313ec8fd678879f198fa1ba2e0d8e87e35f9d6735e5577d925ab51d85fd8`.

同步日期: 2026-11-03. 原始归档保留源字节; 本内容包仅移除机器本地路径, 不重新计算研究指标.
