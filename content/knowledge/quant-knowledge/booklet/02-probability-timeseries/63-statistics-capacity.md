# 63. 概率统计：capacity 容量、成交约束、冲击成本与规模敏感性

## 核心概念

capacity 容量指一个策略在不显著恶化收益、风险和执行质量的前提下，最多能承载多少资金规模。

容量不是一个固定常数，而是由多种约束共同决定：

- 标的流动性。
- 持仓集中度。
- 换手率。
- 成交参与率。
- 交易成本和市场冲击。
- alpha 的衰减速度。
- 风控和组合约束。

一个策略在 1,000 万资金下表现很好，不代表在 10 亿资金下也能复制同样 Sharpe。

## capacity 回答的问题

capacity 不是问：

```text
策略当前能不能赚钱？
```

它问的是：

```text
随着资金规模变大，策略还能不能以可接受成本交易，并保留足够净 alpha？
```

实盘里常见的容量瓶颈包括：

- 买不进或卖不出足够数量。
- 交易占日成交额比例过高。
- 冲击成本随交易规模非线性上升。
- 持仓过于集中在低流动性资产。
- 同类资金拥挤导致 alpha 衰减。

因此 capacity 必须和 turnover、交易成本、市场冲击、持仓分布一起分析。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一个 5 只资产的组合：

```python
assets = ["AAA", "BBB", "CCC", "DDD", "EEE"]

weights = pd.Series(
    [0.30, 0.25, 0.20, 0.15, 0.10],
    index=assets,
    name="weight",
)

adv_dollar = pd.Series(
    [80_000_000, 45_000_000, 25_000_000, 12_000_000, 6_000_000],
    index=assets,
    name="adv_dollar",
)

daily_turnover = pd.Series(
    [0.18, 0.22, 0.26, 0.30, 0.35],
    index=assets,
    name="daily_turnover",
)

daily_vol = pd.Series(
    [0.018, 0.022, 0.026, 0.032, 0.040],
    index=assets,
    name="daily_vol",
)
```

这里：

- `weights` 是组合权重。
- `adv_dollar` 是平均日成交额，ADV。
- `daily_turnover` 是每个资产每天需要换掉的持仓比例。
- `daily_vol` 是日波动率，用于简化冲击成本估计。

低流动性资产即使权重不高，也可能成为容量瓶颈。

## 参与率 participation rate

参与率衡量交易金额占 ADV 的比例：

```text
participation_i = trade_dollar_i / ADV_i
```

给定资金规模 AUM：

```python
aum = 25_000_000

position_dollar = aum * weights
one_way_trade_dollar = position_dollar * daily_turnover
participation = one_way_trade_dollar / adv_dollar

participation_table = pd.DataFrame({
    "weight": weights,
    "position_dollar": position_dollar,
    "one_way_trade_dollar": one_way_trade_dollar,
    "adv_dollar": adv_dollar,
    "participation": participation,
})

print(participation_table)
print(participation.idxmax())
print(participation.max())
```

如果某只资产参与率过高，可能意味着：

- 成交时间必须拉长。
- 冲击成本会明显上升。
- 回测成交价假设不现实。
- 策略容量被该资产限制。

实务里常见规则是限制单日交易不超过 ADV 的某个比例，例如 5%、10% 或 20%。具体阈值取决于市场、标的和执行能力。

## 按参与率估算容量上限

假设最大允许参与率是 10%：

```python
max_participation = 0.10

capacity_by_asset = (
    max_participation
    * adv_dollar
    / (weights * daily_turnover)
)

participation_capacity = capacity_by_asset.min()
binding_asset = capacity_by_asset.idxmin()

print(capacity_by_asset)
print(participation_capacity)
print(binding_asset)
```

这个公式来自：

```text
AUM * weight_i * turnover_i / ADV_i <= max_participation
```

整理得：

```text
AUM <= max_participation * ADV_i / (weight_i * turnover_i)
```

所有资产都要满足约束，所以组合容量取最小值。

在这个例子中，低 ADV 且高换手的资产会成为约束资产。

## 简化冲击成本模型

交易成本通常不只是固定手续费。市场冲击常用平方根形式近似：

```text
impact_i = k * volatility_i * sqrt(participation_i)
```

其中：

- `k`：冲击系数。
- `volatility_i`：资产日波动。
- `participation_i`：成交参与率。

这不是精确模型，但能表达一个关键事实：

```text
交易越大，成本越高，而且不是线性可忽略的。
```

代码：

```python
impact_coef = 0.12

impact_cost = impact_coef * daily_vol * np.sqrt(participation.clip(lower=0))
weighted_impact_cost_bps = float((impact_cost * weights).sum() * 10_000)

print(impact_cost)
print(weighted_impact_cost_bps)
```

`weighted_impact_cost_bps` 是组合层面的加权冲击成本，单位是 bps。

真实成本模型还会加入：

- bid-ask spread。
- 手续费和税费。
- 借券费。
- 执行时长。
- 日内成交量曲线。
- 市场状态和波动率 regime。

## 规模扩大后的净 alpha

假设策略毛 alpha 是每天 8 bps。随着 AUM 增加，交易金额变大，冲击成本上升。

```python
base_alpha_bps = 8.0

aums = pd.Series(
    [10_000_000, 25_000_000, 50_000_000, 100_000_000, 200_000_000],
    name="aum",
)

rows = []

for current_aum in aums:
    position_dollar = current_aum * weights
    one_way_trade_dollar = position_dollar * daily_turnover
    participation = one_way_trade_dollar / adv_dollar

    impact_cost = (
        impact_coef
        * daily_vol
        * np.sqrt(participation.clip(lower=0))
    )

    weighted_cost_bps = float((impact_cost * weights).sum() * 10_000)
    net_alpha_bps = base_alpha_bps - weighted_cost_bps

    rows.append({
        "aum": current_aum,
        "max_participation": participation.max(),
        "weighted_cost_bps": weighted_cost_bps,
        "net_alpha_bps": net_alpha_bps,
        "binding_asset": participation.idxmax(),
    })

capacity_curve = pd.DataFrame(rows)

print(capacity_curve)
```

这张表展示了容量分析的核心：

- AUM 越大，参与率越高。
- 冲击成本越高。
- 净 alpha 越低。
- 约束资产通常是低流动性和高换手资产。

当 `net_alpha_bps` 接近 0 时，即使毛 alpha 仍然存在，策略也可能已经没有经济意义。

## 净 alpha 容量阈值

可以用网格搜索近似找到净 alpha 仍为正的最大 AUM：

```python
aum_grid = np.linspace(5_000_000, 100_000_000, 200)

net_alpha_by_aum = []

for current_aum in aum_grid:
    participation = (
        current_aum
        * weights
        * daily_turnover
        / adv_dollar
    )

    impact_cost = (
        impact_coef
        * daily_vol
        * np.sqrt(participation.clip(lower=0))
    )

    weighted_cost_bps = float((impact_cost * weights).sum() * 10_000)
    net_alpha_by_aum.append(base_alpha_bps - weighted_cost_bps)

net_alpha_by_aum = pd.Series(net_alpha_by_aum, index=aum_grid)

positive_capacity = net_alpha_by_aum[net_alpha_by_aum > 0].index.max()

print(positive_capacity)
```

这个容量阈值和参与率容量阈值可能不同：

- 参与率阈值关注能不能交易。
- 净 alpha 阈值关注交易后还值不值得做。

一个策略可能满足参与率约束，但净 alpha 已经被成本吃掉。

## 分资产容量诊断

为了知道瓶颈在哪里，可以把指标按资产展开。

```python
diagnostic = pd.DataFrame({
    "weight": weights,
    "adv_dollar": adv_dollar,
    "daily_turnover": daily_turnover,
    "daily_vol": daily_vol,
    "capacity_by_participation": capacity_by_asset,
})

diagnostic["capacity_rank"] = (
    diagnostic["capacity_by_participation"].rank(method="first")
)

print(diagnostic.sort_values("capacity_by_participation"))
```

容量低的资产通常有以下特征：

- ADV 小。
- 权重大。
- 换手高。
- 波动大。
- spread 宽。

如果容量瓶颈集中在少数资产，可以考虑：

- 降低这些资产权重。
- 设置最小流动性过滤。
- 延长调仓周期。
- 使用更平滑的目标权重。
- 增加行业或资产数量分散交易。

## capacity 和回测的关系

回测里常见的错误是只用收益序列评估策略，而不检查成交规模。

一个回测可能显示：

```text
年化收益 20%，Sharpe 2.0，最大回撤 8%
```

但如果每天需要交易某些股票 50% ADV，实盘很可能无法按回测价格成交。

容量检查至少应该回答：

1. 每天每只资产的交易金额是多少？
2. 交易金额占 ADV 的比例是多少？
3. 成本模型是否随参与率上升？
4. 组合规模扩大后净收益如何变化？
5. 哪些资产、行业或流动性桶限制容量？

## 常见坑

第一，只看组合总 turnover，不看单名参与率。

组合 turnover 不高，但交易集中在低流动性资产上，容量仍然很小。

第二，假设成本线性。

手续费近似线性，但市场冲击通常随交易规模非线性上升。

第三，忽略 alpha 衰减。

资金越大，交易越慢、价格影响越大，也越容易暴露意图，alpha 可能衰减。

第四，只用当前 ADV。

流动性会随市场环境变化。压力期 ADV、spread 和深度都可能恶化。

第五，不考虑拥挤交易。

如果很多资金用相似信号，名义 ADV 看起来足够，实际可用流动性可能不足。

第六，把理论容量当成硬上限。

容量是模型估计，不是保证。实盘要留安全边际。

## 实战提示

分析 capacity 时可以按下面流程：

1. 从目标权重和 AUM 计算持仓金额。
2. 从 turnover 计算每期交易金额。
3. 将交易金额除以 ADV 得到参与率。
4. 设置单名、行业和组合层面的参与率上限。
5. 用成本模型估计手续费、spread 和冲击成本。
6. 画出 AUM、成本、净 alpha、净 Sharpe 的容量曲线。
7. 找出最先触发约束的资产和流动性桶。
8. 对压力期 ADV 和更高波动率做敏感性分析。
9. 给策略规模设置安全边际，而不是用理论最大值满打满算。

## 小结

本节的重点：

- capacity 衡量策略能承载的资金规模。
- 容量主要受流动性、换手、持仓集中度和冲击成本限制。
- 参与率是交易金额占 ADV 的比例。
- 单名容量上限可由 `max_participation * ADV / (weight * turnover)` 估算。
- 冲击成本会随交易规模上升，净 alpha 会随 AUM 下降。
- 容量分析要定位瓶颈资产，而不只看组合总指标。
- 回测报告必须把 capacity 与 IC、turnover、Sharpe、drawdown 一起看。

## 自检问题

1. capacity 为什么不是策略收益本身，而是规模敏感性问题？
2. 参与率 participation rate 如何计算？
3. 为什么低权重资产也可能成为容量瓶颈？
4. 参与率容量阈值和净 alpha 容量阈值有什么区别？
5. 为什么冲击成本通常不能简单当作固定线性费用？
6. 回测中如果忽略 capacity，可能产生什么实盘偏差？
