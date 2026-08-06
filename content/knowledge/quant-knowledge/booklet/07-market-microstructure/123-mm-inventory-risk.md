# Inventory Risk

## 核心概念

inventory risk 是库存风险。

在交易和做市里，inventory 指当前持仓。

inventory risk 指：

```text
持仓暴露在价格波动中，导致损益不稳定。
```

做市商不断买入和卖出。

理想状态是双边成交大致平衡，库存接近零。

但真实市场里，经常出现：

```text
连续被买走 -> 做市商变成空头
连续被卖给你 -> 做市商变成多头
价格波动扩大 -> 库存价值波动变大
```

这就是 inventory risk。

## 持仓带来的 PnL

如果你持有 `1000` 股，价格下跌 `0.05`，损益是：

```python
position = 1000
price_change = -0.05

pnl = position * price_change

print(pnl)
```

结果：

```text
-50.0
```

正库存遇到价格下跌会亏损。

负库存遇到价格上涨会亏损。

所以库存本身就是方向性风险。

## inventory risk 和 adverse selection 的区别

adverse selection 关心：

```text
为什么这笔订单打到我？
成交后价格是否马上朝不利方向走？
```

inventory risk 关心：

```text
我成交后持有什么仓位？
如果价格波动，我的库存会亏多少？
我是否需要调报价或对冲？
```

两者经常同时出现。

但概念上不同。

adverse selection 是成交选择偏差。

inventory risk 是持仓暴露风险。

## 库存比例

为了控制风险，通常会设置最大库存。

例如最大允许持仓是 `1000` 股，当前持仓是 `800` 股：

```python
inventory = 800
max_inventory = 1000

inventory_ratio = inventory / max_inventory

print(inventory_ratio)
```

结果：

```text
0.8
```

这表示库存已经达到上限的 `80%`。

此时继续增加多头库存会很危险。

策略应开始偏向减少库存。

## 报价偏移

做市商可以通过调报价来控制库存。

如果库存过多，说明已经持有太多多头。

可以：

```text
降低 bid，减少继续买入的概率
降低 ask，鼓励别人买走库存
```

小例子：

```python
mid = 100.00
base_half_spread = 0.02
inventory = 800
max_inventory = 1000

skew = 0.01 * inventory / max_inventory
bid = mid - base_half_spread - skew
ask = mid + base_half_spread - skew

print(round(bid, 4))
print(round(ask, 4))
```

结果：

```text
99.972
100.012
```

没有库存时，报价可能是：

```text
bid = 99.98
ask = 100.02
```

多头库存过高时，双边报价整体下移。

这样更容易卖出库存，也更不容易继续买入。

## 空头库存的偏移方向

如果库存是负数，说明空头过多。

这时希望买回库存。

可以把报价整体上移：

```text
提高 bid，增加买回概率
提高 ask，减少继续卖空概率
```

一个简单方向信号：

```python
inventory = -600
max_inventory = 1000

bias = -inventory / max_inventory

print(bias)
```

结果：

```text
0.6
```

这里 `bias` 为正，表示报价应向上偏移，帮助减少空头。

## 仓位约束

库存控制通常需要硬约束。

例如持仓上限是 `1000` 股，当前已经有 `1200` 股：

```python
position = 1200
limit = 1000

can_buy_more = position < limit
can_sell_more = position > -limit

print(can_buy_more)
print(can_sell_more)
```

结果：

```text
False
True
```

这表示不能继续买入，只能卖出或减仓。

真实系统里，超过上限时可能要：

```text
停止一侧报价
扩大风险方向报价
主动对冲
降低订单量
触发风控告警
```

## 多时点库存监控

库存风险要连续监控。

例如一段时间内仓位变化：

```python
positions = [200, 500, 900, 1200]
limit = 1000

breaches = [
    abs(position) > limit
    for position in positions
]

print(breaches)
```

结果：

```text
[False, False, False, True]
```

最后一个时点突破了仓位限制。

如果回测没有记录库存路径，只看最终收益，很容易漏掉中间风险。

## 用波动率衡量库存风险

同样的库存，在高波动资产上风险更大。

一个简单风险分数：

```python
position = 500
volatility = 0.02

risk_score = abs(position) * volatility

print(risk_score)
```

结果：

```text
10.0
```

这不是完整风险模型，只是说明：

```text
库存越大，风险越高；
波动率越高，风险越高。
```

实际可使用 dollar exposure、VaR、预期短缺或压力测试。

## 对冲库存

如果库存太大，可以用相关资产对冲。

例如持有 `1000` 股股票，用期货或 ETF 对冲 `80%`：

```python
position = 1000
hedge_ratio = 0.8

hedge_position = -position * hedge_ratio
net_exposure = position + hedge_position

print(hedge_position)
print(net_exposure)
```

结果：

```text
-800.0
200.0
```

对冲后净暴露从 `1000` 降到 `200`。

但对冲不是免费午餐。

它会引入：

```text
基差风险
相关性变化
交易成本
对冲滞后
合约流动性风险
```

## 做市中的库存目标

做市策略通常不是无脑双边报价。

它会围绕一个目标库存调节行为。

伪代码：

```text
target_inventory = 0
inventory_error = current_inventory - target_inventory

if inventory_error > 0:
    lower_bid()
    lower_ask()
elif inventory_error < 0:
    raise_bid()
    raise_ask()
else:
    quote_symmetrically()
```

这段逻辑表示：

```text
多头太多 -> 报价下移，鼓励卖出库存
空头太多 -> 报价上移，鼓励买回库存
库存接近目标 -> 正常双边报价
```

## spread、adverse selection 和 inventory

做市报价至少要补偿三类风险：

```text
交易处理成本
adverse selection 风险
inventory risk
```

如果库存已经很偏，做市商不一定愿意继续提供同样价格的流动性。

例如多头库存过高时：

```text
继续买入会增加风险
所以 bid 应该更保守
```

如果市场波动率突然升高：

```text
同样库存带来的损益波动更大
所以 spread 可能需要变宽
```

这解释了为什么压力市场中流动性会变差。

## 回测中的常见错误

inventory risk 常被回测低估。

常见错误包括：

```text
只看成交收益，不记录仓位路径
假设可以无限持仓
没有设置单资产和组合仓位上限
忽略高波动时库存风险上升
忽略对冲成本和基差风险
只看平均收益，不看库存导致的回撤
用收盘净仓位替代日内最大仓位
```

对做市和高换手策略来说，库存路径和收益同样重要。

一个策略平均赚钱，但需要承受巨大库存波动，可能并不可交易。

## 小结

inventory risk 是持仓暴露造成的风险。

核心问题是：

```text
我现在持有什么仓位？
如果价格波动，我会亏多少？
库存是否超过目标或上限？
报价是否应该向减少库存的方向偏移？
是否需要对冲？
```

它和 adverse selection 一起决定了提供流动性的真实风险。

下一篇讨论 market impact。

它会解释自己的交易如何反过来推动价格，尤其是在大额订单和低流动性市场中。
