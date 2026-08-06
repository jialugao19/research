# 124. 市场微观结构：market impact 的临时/永久冲击、订单规模和执行成本

## 核心概念

market impact 是市场冲击。

它指自己的交易行为对价格造成的影响。

直观地说：

```text
小订单可能按当前报价成交
大订单会吃掉盘口深度
更大的订单还会让市场参与者调整报价
```

因此，真实成交价格可能比下单前看到的价格更差。

对买单来说，market impact 通常表现为成交价更高。

对卖单来说，market impact 通常表现为成交价更低。

## 和 bid-ask spread 的区别

bid-ask spread 是立刻成交时面对的报价差。

market impact 是你的订单改变市场价格带来的额外成本。

例如：

```text
买入 100 股：可能只付 ask
买入 100 万股：可能连续吃掉多档 ask，并推动后续报价上移
```

所以总执行成本通常包括：

```text
spread cost
market impact
fees
delay cost
opportunity cost
```

不要只扣手续费或半价差。

大额订单里，market impact 往往是更主要的成本。

## 参与率

衡量订单大小时，常用 participation rate。

```text
participation rate = order size / market volume
```

例如要买 `100,000` 股，当日成交量是 `2,000,000` 股：

```python
order_size = 100_000
daily_volume = 2_000_000

participation_rate = order_size / daily_volume

print(participation_rate)
```

结果：

```text
0.05
```

这表示订单占当日成交量的 `5%`。

参与率越高，越容易产生冲击。

## 用 bps 表示冲击

如果 mid 是 `100.00`，买入冲击是 `5 bps`，执行价约为：

```python
mid = 100.00
impact_bps = 5

execution_price = mid * (1 + impact_bps / 10000)

print(execution_price)
```

结果：

```text
100.05
```

`5 bps` 看起来很小。

但对大额订单，金额成本很可观。

例如买入 `100,000` 股，mid 是 `50.00`，平均成交价是 `50.03`：

```python
shares = 100_000
mid = 50.00
execution_price = 50.03

impact_cost = (execution_price - mid) * shares
cost_bps = (execution_price - mid) / mid * 10000

print(round(impact_cost, 2))
print(round(cost_bps, 2))
```

结果：

```text
3000.0
6.0
```

平均成交价只高了 `0.03`。

但总成本是 `3000`。

## 线性冲击模型

最简单的冲击模型是假设冲击和订单规模成正比。

```text
impact = coefficient * order_size
```

小例子：

```python
order_sizes = [10_000, 20_000, 50_000]
coef = 0.000001

impacts = [
    coef * size
    for size in order_sizes
]

print(impacts)
```

结果：

```text
[0.01, 0.02, 0.049999999999999996]
```

订单越大，估计冲击越大。

线性模型容易解释，但经常过于粗糙。

真实冲击可能随流动性、波动率、成交节奏和市场状态变化。

## 平方根冲击直觉

很多执行模型会使用类似平方根的形式。

一个简化表达是：

```text
impact ≈ volatility * sqrt(order_size / volume)
```

例子：

```python
import math

sigma = 0.02
participation = 0.10

impact = sigma * math.sqrt(participation)

print(round(impact, 6))
print(round(impact * 10000, 2))
```

结果：

```text
0.006325
63.25
```

这里的冲击约为 `63.25 bps`。

这不是通用定律，只是说明两个直觉：

```text
波动率越高，冲击越大
订单相对成交量越大，冲击越大
```

## 临时冲击和永久冲击

market impact 常分成两类。

第一类是 temporary impact。

```text
交易时把价格推开
交易结束后价格部分回落
```

第二类是 permanent impact。

```text
交易传递了信息
市场重新定价
价格不完全回落
```

假设成交时冲击是 `6 bps`，其中 `2 bps` 是永久冲击：

```python
temporary_bps = 6
permanent_bps = 2

realized_bps = temporary_bps - permanent_bps

print(realized_bps)
```

结果：

```text
4
```

这里 `4 bps` 可以理解为交易后回落的部分。

永久冲击越大，说明订单包含的信息越强，或者市场把交易解释成方向性信号。

## 分拆订单

为了降低冲击，大订单通常会拆成多个 child orders。

例如父订单是 `100,000` 股，拆成五笔：

```python
parent_order = 100_000
child_orders = [20_000] * 5

print(sum(child_orders) == parent_order)
print(max(child_orders))
```

结果：

```text
True
20000
```

分拆可以降低单次吃掉盘口的冲击。

但也有代价：

```text
执行时间变长
价格可能在等待中变差
市场可能识别出你的订单
未完成风险上升
```

所以执行算法要平衡冲击成本和时间风险。

## VWAP/TWAP 的执行直觉

TWAP 按时间平均执行。

```text
每隔固定时间执行一部分
```

VWAP 按成交量分布执行。

```text
市场成交量高时多执行
市场成交量低时少执行
```

如果每个时间段都固定买 `10,000` 股，而市场成交量不同：

```python
volumes = [100_000, 150_000, 50_000]
child_order = 10_000

rates = [
    child_order / volume
    for volume in volumes
]

print([round(rate, 4) for rate in rates])
```

结果：

```text
[0.1, 0.0667, 0.2]
```

第三个时段成交量低，同样 `10,000` 股会变成更高参与率。

这可能带来更大冲击。

VWAP 的思想就是让参与率更贴近市场成交量节奏。

## 净 alpha 要扣 impact

策略信号必须覆盖完整执行成本。

假设预测收益是 `8 bps`，spread 成本 `2 bps`，impact 成本 `5 bps`，手续费 `1 bps`：

```python
alpha_bps = 8
spread_bps = 2
impact_bps = 5
fee_bps = 1

net_alpha = alpha_bps - spread_bps - impact_bps - fee_bps

print(net_alpha)
```

结果：

```text
0
```

账面 alpha 是正的。

扣完执行成本后，净 alpha 为零。

如果回测忽略 market impact，这类策略会显得可赚钱，但真实交易可能没有边际。

## 冲击的主要驱动因素

market impact 受很多变量影响：

```text
订单规模
订单占成交量比例
盘口深度
bid-ask spread
波动率
交易速度
是否在公告或开收盘时段
是否容易被其他参与者识别
资产本身流动性
```

同样的订单规模，在不同市场状态下冲击完全不同。

例如：

```text
正常时段买 10 万股可能影响很小
公告后流动性撤退时买 10 万股可能冲击很大
```

## 回测中的常见错误

market impact 很容易被回测低估。

常见错误包括：

```text
用 mid 价成交
只扣固定手续费
只扣固定半价差，不考虑订单规模
不限制参与率
不考虑盘口深度
把大订单一次性按最优价成交
忽略高波动和低流动性时段冲击上升
用未来成交量决定当前订单大小
```

特别是容量测试中，market impact 是核心约束。

策略在小资金下盈利，不代表资金放大后仍然盈利。

## 实战检查清单

建模 market impact 时，至少检查：

```text
订单规模占成交量比例是多少
是否按资产和时段估计流动性
是否区分 spread cost 和 market impact
是否限制最大参与率
是否模拟分拆执行
是否把未完成订单纳入结果
是否在高波动时放大冲击假设
是否做容量敏感性分析
```

一个实际可用的回测，宁愿对 impact 保守，也不要假设大额订单可以无成本通过市场。

## 小结

market impact 是自己的交易推动价格造成的成本。

它和 spread、adverse selection、inventory risk 一起决定真实执行质量。

核心直觉是：

```text
订单越大，冲击越大
流动性越差，冲击越大
执行越急，冲击越大
波动越高，冲击越大
```

下一篇讨论 VPIN。

它会从成交量分桶和买卖压力不平衡的角度，解释一种衡量毒性订单流的指标。
