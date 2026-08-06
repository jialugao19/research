# 60. 概率统计：turnover 换手率的定义、计算、分解与成本含义

## 核心概念

turnover 换手率衡量组合在相邻调仓时点交易了多少。

最常见的权重口径是：

```text
turnover_t = 0.5 * sum_i |w_{t,i} - w_{t-1,i}|
```

其中：

- `w_{t,i}`：调仓后资产 `i` 在日期 `t` 的目标权重。
- `w_{t-1,i}`：上一次调仓后的目标权重。
- 乘以 `0.5` 是因为卖出一边和买入一边在净多头满仓组合中通常同时发生，双边绝对变化会重复计算一次。

如果按交易金额口径：

```text
dollar_turnover_t = traded_value_t / portfolio_value_t
```

这时是否乘以 `0.5` 取决于机构定义。很多交易成本计算会直接使用双边交易金额：

```text
cost_t = sum_i |trade_weight_{t,i}| * cost_rate_i
```

因此使用 turnover 时必须先说明口径。

## turnover 回答的问题

换手率不是收益指标，而是交易强度指标。

它回答的问题包括：

- 因子组合需要多频繁换仓？
- 策略收益是否可能被手续费和滑点吃掉？
- 策略容量是否受交易量限制？
- 实盘成交和回测假设之间是否有差距？

同样的 IC 或 Sharpe 下，低换手策略通常更容易落地；高换手策略需要更强的 alpha、更低成本或更好的执行能力。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一个 4 只资产、8 个交易日的目标权重面板：

```python
rng = np.random.default_rng(60)

dates = pd.bdate_range("2024-01-02", periods=8)
assets = ["AAA", "BBB", "CCC", "DDD"]

raw_signal = pd.DataFrame(
    rng.normal(size=(len(dates), len(assets))),
    index=dates,
    columns=assets,
)

scores = raw_signal.rank(axis=1, pct=True)
target_weights = scores.div(scores.sum(axis=1), axis=0)

print(target_weights.round(4))
```

这里用横截面排名生成一个简单 long-only 组合：

- 每天所有权重为正。
- 每天权重和为 1。
- 排名更高的资产得到更高权重。

## 目标权重差异口径

直接用相邻目标权重差异计算换手：

```python
weight_change = target_weights.diff()
target_turnover = weight_change.abs().sum(axis=1) / 2

target_turnover.iloc[0] = target_weights.iloc[0].abs().sum()

print(target_turnover)
```

第一天没有上一期持仓。常见处理方式有两种：

- 如果从现金建仓，第一天 turnover 等于建仓规模，long-only 满仓就是 `1.0`。
- 如果只评估稳定运行期，可以把第一天设为缺失并排除。

这里采用第一种：从现金买入组合。

## 为什么有时除以 2

假设组合从：

```text
AAA 50%, BBB 50%
```

变成：

```text
AAA 30%, BBB 70%
```

绝对权重变化为：

```text
|30% - 50%| + |70% - 50%| = 40%
```

但真实上只是卖出 20% 的 `AAA`，买入 20% 的 `BBB`。

如果把“一边成交额 / 组合净值”定义为换手，则 turnover 是 `20%`，所以除以 2。

但如果用“双边成交额 / 组合净值”定义交易强度，则是 `40%`。交易成本一般更接近双边成交额口径。

## 漂移后再调仓口径

实盘中，上一期目标权重会随着资产收益自然漂移。真正需要交易的是：

```text
目标权重 - 漂移后的当前权重
```

先模拟每天实现收益：

```python
returns = pd.DataFrame(
    rng.normal(loc=0.0005, scale=0.01, size=(len(dates), len(assets))),
    index=dates,
    columns=assets,
)
```

计算调仓前的漂移权重：

```python
previous_target = target_weights.shift(1)

gross_after_return = previous_target * (1 + returns)
drifted_weights = gross_after_return.div(gross_after_return.sum(axis=1), axis=0)

trade_weights = target_weights - drifted_weights
trade_turnover = trade_weights.abs().sum(axis=1) / 2

print(drifted_weights)
print(trade_turnover)
```

第一天没有上一期组合，`drifted_weights` 为缺失，`trade_turnover` 也没有稳定运行含义。

可以把第一天单独按建仓处理：

```python
trade_turnover.iloc[0] = target_weights.iloc[0].abs().sum()

print(trade_turnover)
```

目标权重差异口径和漂移后口径通常很接近，但不完全一样。

在波动大、调仓间隔长、组合杠杆高的策略中，漂移影响会更明显。

## 双边成交额和成本

如果交易成本按成交额收取，通常使用双边绝对交易权重：

```python
two_sided_trade = trade_weights.abs().sum(axis=1)
two_sided_trade.iloc[0] = target_weights.iloc[0].abs().sum()

fee_rate = 0.0005
estimated_cost = two_sided_trade * fee_rate

cost_table = pd.DataFrame({
    "one_way_turnover": trade_turnover,
    "two_sided_trade": two_sided_trade,
    "estimated_cost": estimated_cost,
})

print(cost_table)
```

这里 `fee_rate = 0.0005` 表示单边成交金额的 5bp 成本。

注意：

- `one_way_turnover` 是除以 2 后的换手。
- `two_sided_trade` 是买入和卖出的绝对权重之和。
- 成本用哪个口径取决于费率定义。

如果费率是对每一笔成交收取，就应用双边成交额。

## 年化 turnover

日频换手常需要年化：

```python
daily_turnover = trade_turnover.iloc[1:]
annualized_turnover = daily_turnover.mean() * 252

print(daily_turnover.mean())
print(annualized_turnover)
```

年化 turnover 的解释：

```text
平均每天换手 20%，大约等价于一年换手 50.4 倍
```

但这个数字不能机械理解为完整卖出 50 次，因为它来自连续的权重调整。

高年化换手意味着策略对交易成本、冲击成本和成交容量更敏感。

## 多空组合的 turnover

多空组合经常是 dollar-neutral：

```text
sum_i w_i = 0
```

示例：

```python
active_weights = pd.DataFrame(
    {
        "AAA": [0.30, 0.10, -0.10],
        "BBB": [-0.10, 0.20, 0.00],
        "CCC": [-0.20, -0.30, 0.10],
        "DDD": [0.00, 0.00, 0.00],
    },
    index=dates[:3],
)

print(active_weights.sum(axis=1))
```

多空组合的换手也可以用绝对权重变化：

```python
active_turnover = active_weights.diff().abs().sum(axis=1) / 2
active_turnover.iloc[0] = active_weights.iloc[0].abs().sum() / 2

print(active_turnover)
```

这里第一天 `sum(abs(weight)) / 2` 表示建立一组多头和空头。若组合 gross exposure 是 100%，第一天 one-way turnover 是 50%；若机构定义为双边成交，则是 100%。

多空策略必须同时说明：

- net exposure：净暴露，例如 `sum(w)`。
- gross exposure：总暴露，例如 `sum(abs(w))`。
- turnover 口径：one-way 还是 two-sided。

## turnover 分解

实际分析中，可以把 turnover 分成几类来源。

第一，信号变化带来的调仓：

```text
新目标组合和旧目标组合不同
```

第二，价格波动导致的漂移再平衡：

```text
资产涨跌后，当前权重偏离目标权重
```

第三，约束变化带来的交易：

```text
停牌、涨跌停、风控约束、行业限制、容量限制
```

第四，资金流入流出：

```text
申购赎回或组合规模变化
```

在回测中，如果只用 `target_weights.diff()`，会低估或误估某些真实交易来源。

## 与 IC、Sharpe、capacity 的关系

turnover 通常和其他指标一起看。

```text
净收益 = 毛收益 - 交易成本 - 冲击成本
```

一个因子可能有不错的 IC，但如果：

- 信号每天大幅变化。
- 持仓集中在低流动性资产。
- spread 和冲击成本很高。
- 组合优化频繁换名。

那么高 turnover 会让净收益显著下降。

turnover 还和 capacity 容量相关：同样的权重变化，在 1 千万资金规模下可成交，不代表在 10 亿资金规模下也可成交。

## 常见坑

第一，不说明口径。

`sum(abs(delta_weight))` 和 `0.5 * sum(abs(delta_weight))` 都有人叫 turnover。报告里必须写清楚。

第二，把目标权重变化当成真实交易。

真实交易应从漂移后权重调到目标权重，还要考虑成交失败、停牌和涨跌停。

第三，第一天建仓处理不一致。

有的研究排除第一天，有的把第一天当作从现金建仓。比较策略时要统一。

第四，只估手续费，不估滑点和冲击。

高换手策略的主要成本常常不是佣金，而是 bid-ask spread、冲击成本和排队成本。

第五，忽略换手集中度。

平均 turnover 不高，但如果交易集中在少数低流动性股票上，实盘仍然困难。

## 实战提示

分析 turnover 时可以按下面流程：

1. 明确权重口径：净权重、gross 权重、主动权重还是实际持仓权重。
2. 明确 turnover 口径：one-way 还是 two-sided。
3. 区分第一天建仓和稳定运行期换手。
4. 用漂移后权重计算真实需要交易的权重。
5. 将交易权重乘以组合规模，得到预估成交金额。
6. 按资产的费率、spread、成交量和冲击模型估算成本。
7. 分资产、行业、市值、流动性桶查看 turnover 分布。
8. 与 IC、持仓周期、Sharpe、capacity 一起判断可交易性。

## 小结

本节的重点：

- turnover 衡量组合交易强度，不是收益指标。
- 常见 one-way turnover 是 `0.5 * sum(abs(delta_weight))`。
- 成本通常更接近双边成交额口径。
- 实盘应从漂移后权重调到目标权重，而不只是看目标权重差异。
- 第一日建仓和稳定运行期换手要分开处理。
- 多空组合要同时说明 net、gross 和 turnover 口径。
- 高 IC 策略如果 turnover 太高，净收益可能仍然很差。

## 自检问题

1. 为什么 long-only 满仓组合计算 one-way turnover 时常除以 2？
2. `target_weights.diff()` 和真实交易权重有什么区别？
3. 为什么第一天建仓要单独处理？
4. 成本计算时应使用 one-way turnover 还是双边成交额？
5. 多空组合为什么必须同时报告 net exposure 和 gross exposure？
6. turnover 为什么会影响 capacity？
