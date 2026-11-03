---
title: Overnight strategy independent review
date: 2026-10-14
summary: 独立重放验证 purge fix、cost 与 capacity; 仍有三项 MEDIUM evidence gap.
tags:
- overnight
- research
featured: false
---

## 摘要

独立重放验证 purge fix、cost 与 capacity; 仍有三项 MEDIUM evidence gap.

这是独立 review 当时的状态快照. 原文 finalizer 尚未运行的描述不覆盖后续 formal HTML 已完成的事实.

## 研究背景与目标

研究问题与数据合同以保留的源报告为准. 本页将既有研究证据登记为独立 publication, 关联对应 Study 与 Experiment.

## 数据与方法

2021-2023 为 Train; 2024 Validation 排除 9-10 月. 历史报告中的 2025 one-shot Test 已被查看, 当前仅能作为 historical confirmation, 不支持再次用其选择配置. 本次同步仅整理既有 evidence, 未训练、推理或重跑回测.

## 主要结果


### 1. 结论

新 formal artifact 通过 independent review. Commit `15a023a20b14ab50e8dd0e5483542f2e575a6791` 已完整修复上一轮 HIGH finding. Strategy weights, gross/cost portfolio, alpha, capacity 和 exposure 均排除 `evaluable=false`, ranking coverage 则继续保留完整 signal-date universe.

本次发现 0 个 CRITICAL, 0 个 HIGH, 3 个 MEDIUM, 2 个 LOW. 没有阻止 finalizer 的 correctness finding. Artifact 的 `CONTINUE_RESEARCH` verdict 与独立复算一致: gross alpha 存在, 但 reference costs 和 100-share lot granularity 使 preregistered AUM grid 中不存在 validation/test 同时满足 `net return > 0` 且 `fill ratio >= 80%` 的共同区域. 当前 evidence 不支持 production promotion, 仍需要 future forward evidence.

### 2. 审查边界和独立方法

审查对象为新 artifact, 指定 commit, frozen config 和 formal evaluation. 复算使用独立 Pandas/NumPy event replay, raw `stock1d` files, frozen predictions 和 formal exit tape. 没有 import 或调用 `astock_overnight.strategy_*` 的计算函数.

关键 accounting identities:

```text
gross NAV_t = cash_t + marked open positions_t
turnover_t = (entry notional_t + non-writeoff exit proceeds_t) / NAV_(t-1)
one-way break-even = terminal gross profit / cumulative traded notional * 10,000
candidate net NAV_t = cash_t + adjusted-close marked remaining base units_t
candidate total cost = broker + stamp duty + transfer + spread/slippage + impact
```

独立 event order 为: 先处理当日 14:00 及以前 exits, 再以当时 available cash 下单, 再处理 14:00 以后 exits, 最后使用 raw daily `close * adj_factor` mark remaining positions. Security code transition `300114 -> 302132` 按 2025-02-17 的 date-effective rule canonicalize.

### 3. Purge fix 验证

### 3.1 Sample-level exclusion

Formal validation predictions 有 1,643 个 `evaluable=false` observations. 其中 2024-08-30 有 675 个 `purged_boundary` rows, 2024-12-31 有 941 个 `purged_boundary` rows. Q10 中两日分别为 67 和 94 个, 合计 161 个. 此外 2024-02-05 有 1 个 Q10 `entry_limit_up_locked` non-evaluable row. 新 `q10_weights.parquet` 因此比旧 artifact 少 162 rows.

逐表 sample-id intersection 结果:

| Outcome table | Rows | Intersection with all validation `evaluable=false` |
| --- | ---: | ---: |
| `q10_weights.parquet` | 34,044 | 0 |
| `gross_positions.parquet` | 187,773 | 0 |
| `alpha_rows.parquet` | 342,275 | 0 |
| `exit_capacity_tape.parquet` | 195,506 | 0 |

`exposure.parquet`, `size_exposure.parquet` 和 `industry_exposure.parquet` 不含 sample ID, 但 validation 均只有 203 个 legal dates, 2024-08-30 和 2024-12-31 的 rows 均为 0. Capacity daily 没有 sample ID, 本审查通过无 overlap 的 exit tape 和独立 capacity event replay 验证其 legal input set.

### 3.2 Ranking coverage 保留

`selection_daily.parquet` 保留 205 个 validation signal dates. 两个 boundary dates 仍分别保留 top20/Q10/top5 coverage rows, 但 `evaluable_count=0`, `mean_return=NaN`. `rank_ic.parquet` 同样报告 205 个 signal dates 和 203 个 finite RankIC dates. 这实现了 ranking coverage 与 outcome eligibility 的明确分离.

### 3.3 Full rerun evidence

相对旧 corrected artifact, 新 heavy tables 的 row deltas 与 exclusion 一致:

```text
q10_weights            -162
gross_positions        -887
alpha_rows            -1615
exit_capacity_tape     -909
exposure                 -6
size_exposure           -24
industry_exposure        -6
selection_daily           0
rank_ic                   0
```

新 artifact 是从 frozen inputs 执行 `python scripts/research_overnight_strategy.py` 的 full rerun. Manifest 没有 `derived_from` 或 summary-only rebuild lineage. 旧 source-heavy artifact 不再是新 formal artifact 的 derivation parent.

### 4. 独立复算

### 4.1 Validation Q10 gross, turnover 和 cost frontier

独立实现从 frozen predictions 取 `split=validation, decile=10, evaluable=true, tradable=true`, 使用 raw adjusted-close marks 重建完整 event ledger. Formal daily NAV 和 turnover 的 maximum absolute difference 均为 0.

| Metric | Independent value | Formal difference |
| --- | ---: | ---: |
| Position count | 12,935 | 0 |
| Observation count | 242 | 0 |
| Gross cumulative return | 0.201321728955825 | 0 |
| Maximum drawdown | -0.047105119213275 | 0 |
| Mean daily turnover | 1.678873105213277 | 0 |
| Cumulative turnover, `sum(turnover_t)` | 406.287291461613 | N/A, formal summary 未单列 |
| Cumulative traded notional, initial capital=1 | 457.744099093321 | `5.68e-14` |
| Terminal one-way break-even | 4.398128328789 bps | 0 |
| Round-trip break-even on entry notional | 8.800127066392 bps | 0 |

对 `0/5/10/15/20/30/50 bps` 全部 7 档 validation cost sweep 逐档重新执行 event ledger. Total return, MDD 和 mean turnover 均与 formal CSV 一致到 `1.25e-14` 以内. 例如 10 bps round-trip cost 下, total return 为 `-0.019284555120200`, MDD 为 `-0.080059019966358`, mean turnover 为 `1.677203905534642`.

### 4.2 Validation alpha realization

独立按 `split, signal_date, checkpoint, decile` 先做 equal-cohort mean, 再计算 daily Q10-Q1 spread 和 checkpoint summary. 所有 summary fields 与 `alpha_summary.parquet` 一致到 `4.44e-16` 以内. Canonical `next_1000` 的 68,455 个 alpha rows 与 frozen `realized_return` 逐 row exact, maximum difference 为 0.

Validation `next_1000`:

```text
signal_date_count       203
Q1 mean return          -0.012674459831550
Q10 mean return          0.000935888796820
Q10-Q1 spread            0.013610348628370
delayed ratio            0.005105958230958
```

两个 purged boundary dates 在 `alpha_rows.parquet` 中均为 0 rows.

### 4.3 CNY 2m reference-cost capacity event replay

Artifact 未持久化 capacity order ledger. 本审查从 raw daily data 独立重建 lagged ADV20 和 volatility20, 独立重建 legal Q10 equal weights, 再以 `exit_capacity_tape.parquet` 重放 lot-rounded buys, partial exits, broker minimum, stamp duty, transfer fee, spread/slippage 和 square-root impact. Replay 没有使用 formal result summary 作为状态输入.

| Metric | Validation independent | Test independent | Maximum formal difference |
| --- | ---: | ---: | ---: |
| Terminal NAV | CNY 1,954,407.868786 | CNY 1,868,384.138185 | `2.33e-10` CNY |
| Net cumulative return | -0.022796065606927 | -0.065807930907453 | `9.71e-17` |
| Maximum drawdown | -0.074416221408119 | -0.120516516050270 | `5.55e-17` |
| Entry fill ratio | 0.831001752589684 | 0.866787714386525 | 0 |
| Total cost | CNY 388,849.641185 | CNY 517,271.233578 | `5.82e-11` CNY |
| Broker cost | CNY 128,706.157059 | CNY 206,530.000000 | 0 |
| Stamp duty | CNY 171,224.620657 | CNY 207,556.197381 | `2.91e-11` CNY |
| Transfer fee | CNY 6,845.552251 | CNY 8,298.391342 | 0 |
| Spread/slippage | CNY 68,455.522512 | CNY 82,983.913415 | 0 |
| Market impact | CNY 13,617.788705 | CNY 11,902.731440 | 0 |

Validation/test 的 entry order count, capped fraction, lot-rounded fraction, rejected count 和 maximum participation 也全部一致到浮点精度. Cost-component sum 与 daily total cost reconcile.

### 4.4 Canonical 2025 baseline invariant

新 artifact 的 test subsets 与旧合法 test evidence row/value exact. 核对范围包括 Q10 weights, gross positions/daily/summary, alpha rows/summary, exit tape, capacity daily/summary, exposure, selection coverage, RankIC 和 3 个 exported CSV.

独立 test gross replay 结果:

| Metric | Independent value | Formal difference |
| --- | ---: | ---: |
| Position count | 21,109 | 0 |
| Observation count | 244 | 0 |
| Gross cumulative return | 0.237165802897637 | 0 |
| Maximum drawdown | -0.069367097116072 | 0 |
| Mean daily turnover | 1.988524655144857 | 0 |
| Cumulative turnover, `sum(turnover_t)` | 485.200015855345 | N/A, formal summary 未单列 |
| Cumulative traded notional, initial capital=1 | 552.923409000342 | 0 |
| Terminal one-way break-even | 4.289306602635 bps | 0 |
| Round-trip break-even on entry notional | 8.582294414479 bps | 0 |

因此 fix 没有改变 2025 canonical baseline 或 CNY 2m reference-cost case.

### 5. Hashes, lineage 和 decision

Repo HEAD 与 manifest 均为 `15a023a20b14ab50e8dd0e5483542f2e575a6791`. Commit diff 在 weights, gross, alpha, capacity 和 exposure input boundaries 加入 `evaluable=true`, 并新增 boundary-row regression test.

Hash audit:

- Manifest 中 24 个 `result_files` SHA-256 全部与实际文件一致, mismatch 为 0.
- Frozen config SHA-256 为 `80531178f11aab544c53c55cd196724f51ec540f4412df08d96f39d49d73dc6c`, 与 manifest 一致.
- Formal predictions SHA-256 为 `a4db9db90ba59b47de6910a8cc09ba9a0f917f8519e6729e8428d79626912b92`, 与 manifest 一致.
- Checkpoint SHA-256 为 `e2695cc29381dd819283e35a87ac484d22138b9649902fed2a4cf44a29a1fd83`, 与 manifest 一致.
- Reports 目录中的 capacity CSV, cost-frontier CSV, daily CSV, manifest JSON 和 results JSON 均与新 artifact byte-identical.

Decision audit:

- `recommended_strategy=q10_equal` 与 validation weighting comparison 一致. Rank-linear 和 risk-liquidity 的 paired block-bootstrap 95% CI 均未证明优于 equal weight.
- Q10 equal reference-cost grid 中, validation 在 CNY 1m/2m 达到 80% fill 但 net return 为负. CNY 5m 以上部分 validation returns 为正, 但 fill 低于 80%.
- Test 在 CNY 2m 达到 80% fill 但 net return 为负. CNY 5m 仍为负, 更高 AUM fill 低于 80%.
- 因此 `reference_cost_feasible_aum_cny=[]` 和 `CONTINUE_RESEARCH` 均由 tables 支持.

Artifact 保持 `analysis_complete_pending_independent_review` 是 review 前的正确状态. 本 review 写入后可运行 finalizer, 但本审查没有修改 artifact manifest 或生成 final HTML.

### 6. Findings

### CRITICAL/HIGH

无.

上一轮 HIGH 已关闭. 所有 outcome-bearing sample IDs 与 validation `evaluable=false` 的交集为 0, 两个 purged dates 只存在于 ranking coverage.

### MEDIUM-1: Selection-breadth stage 缺少 paired liquidity/capacity evidence

Top20%, Q10 和 Top5% 的 formal comparison 提供 gross performance, turnover, break-even 和 holdings, 但 liquidity distribution, concentration 和 aggregate entry-capacity proxy 只对 Q10 finalists 完整计算. `retain_q10` 的方向合理, 但 breadth trade-off 的 audit table 不完整.

建议在 development legal dates 上补充 3 个 breadth rules 的 lagged ADV distribution, effective-name concentration 和 preregistered aggregate entry-capacity proxy. 该 gap 不改变本次 negative promotion decision.

### MEDIUM-2: Capacity central result 未持久化 order ledger

Artifact 保存 exit tape 和 capacity daily/summary, 但未保存 capacity buy/sell orders. 因此 broker minimum, fragmented exits, participation 和 cost components 不能仅依赖 formal result files 逐单复核. 本审查必须从 raw daily inputs 和 exit tape 完整 replay 才能验证.

建议为 finalists 至少持久化一个 reference AUM order ledger, 包含 parent order, child fill, ADV, bar amount, participation, lot rounding, cap/reject reason 和 cost components.

### MEDIUM-3: Industry exposure 未单独披露 unknown coverage

`unknown` 被作为一个 industry bucket 参与 HHI 和 largest-industry. 旧 source-identical exposure audit 显示 q10_equal test 的 unknown mean weight 为 `8.4020%`, maximum 为 `23.7037%`, 且约 `25.1%` dates 的 `largest_industry=unknown`. 这会把 classification coverage 混入 industry concentration.

建议同时报告 classified weight coverage, unknown weight, full-bucket HHI 和 conditional-on-classified HHI.

### LOW-1: Annualized return 是 arithmetic convention

Strategy summary 使用 `mean(daily_return) * annualization_days`, 不是 CAGR. Sharpe 与该 convention 一致, 所有数值可复算. Final report 应称为 arithmetic annualized mean return, 避免与 geometric annualized return 混淆.

### LOW-2: Participation metric 混合正常 cap 和 upper-limit exception

`maximum_participation` 包含 one-price upper-limit full-fill exception, 因而可以超过 10% normal-bar cap. Q10 equal test CNY 2m reference 为 `12.2222%`, validation 为 `30.7692%`. 这符合 frozen exception, 但 aggregate metric 容易被误读为 cap breach.

建议分别报告 normal-bar maximum participation 和 unrestricted upper-limit exit participation.

### 7. 十二项审查结果

| Item | Status | Evidence |
| --- | --- | --- |
| Temporal causality | PASS | Entry 在 D 14:00, lagged ADV/volatility through D-1. Purged boundary outcomes 不进入 strategy paths. |
| Universe/rank semantics | PASS | 独立重排 344,040 rows. `prediction_count`, decile, `rank_from_top` mismatch 均为 0. Legal Q10 membership symmetric difference 为 0. |
| Entry/exit pricing | PASS | 343,972 个 entry VWAP 和 342,391 个 exit VWAP identities error 为 0. Frozen raw checks 覆盖 4 个 `current_price` 和 1,585 个 up-limit exits. |
| Corporate action | PASS | 2,208 个 adjusted-factor-change realized-return identities error 为 0. Date-effective code transition 和 adjusted-close replay 通过. |
| Delayed exit | PASS | 593 个 delayed rows 均记录 10-bar window. Frozen raw window audit 通过. Q10 test 有 9 个 delayed exits, maximum delay 为 2,380 trading minutes. |
| Cash accounting | PASS | Validation/test gross 和 CNY 2m capacity 的 `NAV=cash+invested value` event replay 通过. |
| Turnover | PASS | Validation/test mean turnover, cumulative turnover, traded notional 和 break-even 已独立复算. Writeoff 不计 fictitious exit trade. |
| Cost | PASS | Validation 7 档 cost frontier 和 CNY 2m reference 的 5 个 cost components 均独立复算. 未发现 fee double count. |
| Capacity | PASS with audit gap | Validation/test CNY 2m lot, cap, partial exit 和 cost event replay 与 formal exact. Order-ledger gap 见 MEDIUM-2. |
| Performance metrics | PASS with naming note | Gross/net return, MDD, volatility, Sharpe, hit rate 和 RankIC formulas 均复算通过. Naming note 见 LOW-1. |
| Selection bias | PASS with evidence limitation | Matrix 在新 results 前冻结, 2025 contamination 明确披露, purge fix 生效. Breadth evidence gap 见 MEDIUM-1. |
| Chart/data consistency | PASS at artifact layer | Published CSV/JSON 与 artifact byte-identical. Final HTML 按 workflow 尚未生成, 因此 rendered chart pixel/series comparison 留给 finalizer validation, 不构成当前 artifact finding. |

### 8. Review gate

新 formal artifact 没有 unresolved CRITICAL/HIGH. 可以进入 report finalizer. Final decision 必须保持 `CONTINUE_RESEARCH`, 不得解读为 production approval.

unresolved_critical_high: 0

## 限制与适用边界

这是独立 review 当时的状态快照. 原文 finalizer 尚未运行的描述不覆盖后续 formal HTML 已完成的事实.

2021-2023 为 Train; 2024 Validation 排除 9-10 月. 历史报告中的 2025 one-shot Test 已被查看, 当前仅能作为 historical confirmation, 不支持再次用其选择配置. 本次同步仅整理既有 evidence, 未训练、推理或重跑回测.

## 结论

独立重放验证 purge fix、cost 与 capacity; 仍有三项 MEDIUM evidence gap.

## 附录

来源: `astock-overnight/reports/overnight-strategy-review.md`.

Source SHA-256: `d883b82a7a2d343e0884ada0bc6abb985b1926f077464d8ecb2a4b3f27ce6c7f`.

同步日期: 2026-11-03. 原始归档保留源字节; 本内容包仅移除机器本地路径, 不重新计算研究指标.
