# 119. 市场微观结构：bid-ask spread 的报价含义、成本分解和策略影响

## 核心概念

bid-ask spread 是买一价和卖一价之间的差。

```text
best bid: 市场上最高的买入报价
best ask: 市场上最低的卖出报价
spread = best ask - best bid
```

如果你立刻卖出，通常打到 bid。

如果你立刻买入，通常打到 ask。

所以 spread 是即时成交要面对的第一层交易成本。

## bid、ask 和 mid

假设盘口是：

```text
bid = 99.98
ask = 100.02
```

中间价 mid 是：

```python
bid = 99.98
ask = 100.02

mid = (bid + ask) / 2
spread = ask - bid
spread_bps = spread / mid * 10000

print(round(mid, 2))
print(round(spread, 2))
print(round(spread_bps, 2))
```

结果：

```text
100.0
0.04
4.0
```

这里：

```text
mid = 100.00
spread = 0.04
spread = 4 bps
```

`bps` 是 basis points，`1 bps = 0.01%`。

用 bps 表示 spread，便于比较不同价格水平的资产。

## 为什么 mid 不是可成交价格

mid 是报价中点，不一定能成交。

如果你要立刻买入，需要付 ask。

如果你要立刻卖出，只能拿 bid。

小例子：

```python
bid = 99.98
ask = 100.02

buy_price = ask
sell_price = bid
round_trip_loss = buy_price - sell_price

print(round(round_trip_loss, 2))
```

结果：

```text
0.04
```

这表示：

```text
立刻买入再立刻卖出，价格损失约等于一个 spread。
```

如果只做单边成交，相对 mid 的成本通常约是半个 spread。

```text
买入成本：ask - mid
卖出成本：mid - bid
```

## quoted spread

quoted spread 是盘口上看到的报价价差。

```text
quoted spread = best ask - best bid
```

它反映市场即时流动性。

quoted spread 越窄，说明最优买卖报价越接近。

但 quoted spread 不是最终全部交易成本。

因为真实成交还可能受到：

```text
盘口深度不足
价格冲击
排队等待
撤单
隐藏流动性
交易所费用和返佣
```

所以 quoted spread 是成本估算的起点，不是终点。

## effective spread

effective spread 用真实成交价衡量交易成本。

常用定义是：

```text
effective spread = 2 * trade direction * (trade price - mid)
```

其中：

```text
买入 direction = +1
卖出 direction = -1
```

如果 mid 是 `100.00`，一笔主动买单成交在 `100.03`：

```python
mid = 100.00
trade_price = 100.03
side = 1

effective_spread = 2 * side * (trade_price - mid)
effective_spread_bps = effective_spread / mid * 10000

print(round(effective_spread, 2))
print(round(effective_spread_bps, 2))
```

结果：

```text
0.06
6.0
```

这笔成交的 effective spread 是 `6 bps`。

它比 quoted spread 更接近真实成交成本。

原因是成交价可能优于 ask，也可能劣于 ask。

## realized spread 和 price impact

effective spread 还可以拆成两部分：

```text
realized spread: 流动性提供者最终保留下来的价差收益
price impact: 交易后 mid 向成交方向移动的部分
```

对主动买单，可以用未来某个时点的 mid 来估算。

```python
trade_price = 100.03
future_mid = 100.01
side = 1
effective_spread = 0.06

realized_spread = 2 * side * (trade_price - future_mid)
price_impact = effective_spread - realized_spread

print(round(realized_spread, 2))
print(round(price_impact, 2))
```

结果：

```text
0.04
0.02
```

含义是：

```text
成交时成本是 0.06
其中 0.04 更像流动性提供者获得的补偿
其中 0.02 更像交易后的价格冲击
```

这个拆分很粗略，但有助于理解 spread 背后的经济含义。

## spread 的来源

spread 不是凭空出现的。

做市商或流动性提供者挂单时，要承担风险和成本。

常见来源包括：

```text
order processing cost: 报价、撮合、系统和交易费用
inventory risk: 持仓不平衡导致价格波动风险
adverse selection: 对手方可能拥有更好信息
tick size constraint: 最小报价单位造成的离散化价差
```

如果资产流动性好、竞争做市商多、信息不对称低，spread 往往更窄。

如果资产流动性差、波动大、信息事件密集，spread 往往更宽。

## spread 和交易成本

对市场单来说，半个 spread 是很常用的单边成本近似。

假设：

```text
价格 = 50
spread = 0.02
交易金额 = 1,000,000
```

```python
price = 50.00
spread = 0.02
notional = 1_000_000

shares = notional / price
one_way_cost = shares * spread / 2
cost_bps = one_way_cost / notional * 10000

print(shares)
print(one_way_cost)
print(cost_bps)
```

结果：

```text
20000.0
200.0
2.0
```

这表示单边半价差成本约是：

```text
200 元
2 bps
```

如果策略频繁换手，这个成本会持续侵蚀收益。

## spread 和信号阈值

交易信号必须覆盖交易成本才有意义。

如果半价差成本是 `2 bps`，那么预测收益只有 `1 bps` 的信号，直接交易通常不划算。

```python
signals = [0.0001, 0.0003, 0.0008]
half_spread_bps = 2.0

tradable = [
    signal * 10000 > half_spread_bps
    for signal in signals
]

print(tradable)
```

结果：

```text
[False, True, True]
```

这里三个信号分别是：

```text
1 bps
3 bps
8 bps
```

只有后两个超过半价差成本。

真实策略还要继续扣除：

```text
手续费
滑点
市场冲击
借券成本
撤单和未成交风险
```

## spread 的时间变化

spread 不是常数。

它会随市场状态变化。

常见规律：

```text
开盘时 spread 通常较宽
收盘附近可能因流动性和调仓需求变化而波动
重大公告前后 spread 可能显著变宽
高波动时 spread 往往变宽
流动性好的主力合约或大盘股 spread 往往更窄
```

因此，回测里不能只用一个固定成本参数。

更好的做法是用当时可见的报价数据估算成本。

## 股票、期货和外汇中的差异

不同市场的 spread 表现不同。

股票市场里，spread 常受 tick size、交易量和做市竞争影响。

期货市场里，主力合约通常 spread 较窄，远月或冷门合约可能更宽。

外汇市场里，报价通常非常连续，但真实成本仍然取决于流动性、交易规模和交易通道。

同一个 spread 数值，在不同资产上含义不同。

所以比较时应尽量使用：

```text
spread / mid
spread bps
相对于预期收益的 spread
相对于波动率的 spread
```

## 回测中的常见错误

使用 spread 时，常见错误包括：

```text
用 mid 价格假设可以无成本成交
只扣手续费，不扣 bid-ask spread
用未来盘口估算当前交易成本
对大额订单只扣半价差，不考虑盘口深度
把 quoted spread 当成所有订单的真实成交成本
忽略开盘、公告、低流动性时段 spread 变宽
```

这些错误都会让策略收益被高估。

尤其是高换手策略，spread 可能比预测信号本身还大。

## 小结

bid-ask spread 是市场微观结构里最基础的成本变量。

它连接了报价、成交、流动性和策略净收益。

实践中要区分：

```text
quoted spread: 盘口报价价差
effective spread: 按真实成交价估算的成交成本
realized spread: 成交后一段时间仍保留的价差部分
price impact: 交易推动价格移动的部分
```

做策略时，至少要问：

```text
信号是否覆盖半价差？
回测成交价是否从 mid 改成 bid/ask 或更保守估计？
spread 是否随时间、资产和市场状态变化？
大额订单是否需要考虑盘口深度？
```

下一篇讨论 order imbalance。

它会从买卖盘数量不平衡的角度，继续解释短期价格压力和盘口信号。
