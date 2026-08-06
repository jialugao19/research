# 市场微观结构：adverse selection 的信息不对称、被动成交风险和价差补偿

## 核心概念

adverse selection 是逆向选择。

在交易里，它指你成交时，对手方可能拥有更好的信息。

尤其对提供流动性的限价单来说，最危险的情况是：

```text
没人和你成交时，价格正常；
一旦有人打你，价格马上朝不利方向走。
```

这时你看似赚到了 spread，实际可能接住了信息更强的一方。

## 一个被动买单的例子

假设 mid 是 `100.00`。

你挂买单在 bid `99.99`，看起来比 mid 便宜 `0.01`。

但成交后，未来 mid 跌到 `99.95`。

```python
mid_at_fill = 100.00
fill_price = 99.99
future_mid = 99.95

spread_gain = mid_at_fill - fill_price
adverse_move = mid_at_fill - future_mid
net = spread_gain - adverse_move

print(round(spread_gain, 4))
print(round(adverse_move, 4))
print(round(net, 4))
```

结果：

```text
0.01
0.05
-0.04
```

你从半价差里赚了 `0.01`。

但成交后价格下跌 `0.05`。

净结果是亏 `0.04`。

这就是 adverse selection 的直觉。

## 为什么被成交可能是坏消息

限价单成交有两种可能。

第一种是无信息交易：

```text
对手方只是需要立刻成交
价格之后没有明显不利变化
```

第二种是有信息交易：

```text
对手方知道或更快反应到坏消息
他主动卖给你
之后价格继续下跌
```

对做市或 maker 策略来说，问题不是单笔是否成交。

而是成交样本本身有选择偏差：

```text
好的时候不一定成交；
坏的时候更容易成交。
```

## 成交后 mid 的漂移

可以用成交后一段时间的 mid 变化估计 adverse selection。

例如你都是被动买入，成交价都是 `99.99`：

```python
fills = [
    {"fill_price": 99.99, "future_mid": 100.01},
    {"fill_price": 99.99, "future_mid": 99.95},
    {"fill_price": 99.99, "future_mid": 99.97},
]

pnls = [
    row["future_mid"] - row["fill_price"]
    for row in fills
]
avg_pnl = sum(pnls) / len(pnls)

print([round(x, 4) for x in pnls])
print(round(avg_pnl, 4))
```

结果：

```text
[0.02, -0.04, -0.02]
-0.0133
```

平均来看，被动买入后未来 mid 相对成交价更低。

这说明成交可能带有不利选择。

## expected value 分解

可以把 maker 成交看成两种状态的混合。

```text
无信息成交：赚半价差
有信息成交：亏未来价格漂移
```

一个简化期望值：

```python
prob_informed = 0.3
loss_if_informed = 0.08
gain_if_uninformed = 0.02

expected_value = (
    (1 - prob_informed) * gain_if_uninformed
    - prob_informed * loss_if_informed
)

print(round(expected_value, 4))
```

结果：

```text
-0.01
```

即使只有 `30%` 的有信息交易，期望值也可能为负。

这解释了为什么做市商需要 spread 补偿。

## spread 是风险补偿

spread 不只是交易所费用或系统成本。

它还补偿流动性提供者承担的风险。

其中一部分就是 adverse selection。

如果半价差是 `0.01`，但预期不利价格漂移是 `0.015`：

```python
spread_half = 0.01
expected_adverse_move = 0.015

quote_value = spread_half - expected_adverse_move

print(round(quote_value, 4))
```

结果：

```text
-0.005
```

这笔被动报价的期望值为负。

合理做法可能是：

```text
撤单
报价更宽
降低挂单量
改成主动成交
等待信息风险下降
```

## 主动单方向和未来价格

adverse selection 也可以从主动单角度观察。

如果主动买单之后价格继续上涨，说明买方可能更有信息。

如果主动卖单之后价格继续下跌，说明卖方可能更有信息。

```python
trades = [
    {"side": "buy", "future_mid_change": 0.03},
    {"side": "buy", "future_mid_change": 0.02},
    {"side": "sell", "future_mid_change": -0.01},
]

adverse = []
for trade in trades:
    direction = 1 if trade["side"] == "buy" else -1
    adverse.append(direction * trade["future_mid_change"] > 0)

print(adverse)
```

结果：

```text
[True, True, True]
```

这里每笔主动单之后，价格都朝主动方方向移动。

对被动成交的一方来说，这都是不利选择。

## 和 realized spread 的关系

前面 bid-ask spread 一节提到 realized spread。

如果成交后 mid 朝主动单方向移动，流动性提供者保留下来的 realized spread 会变小。

直觉上：

```text
effective spread 高，不代表 maker 真赚钱
未来 mid 如果快速不利移动，realized spread 会被吃掉
```

所以评估流动性提供策略时，要看：

```text
成交时 spread
成交后 mid 漂移
realized spread
库存风险
撤单和未成交样本
```

只看成交价优于 mid，容易误判。

## adverse selection 信号

实务中会用一些变量估计不利选择风险：

```text
强方向性 order imbalance
大单连续主动买入或卖出
成交后价格持续同向移动
公告或数据发布前后
短期波动率突然升高
盘口快速撤单
跨市场价格已经先动
```

一个简单过滤器：

```python
signals = [0.2, 0.8, 0.6]
threshold = 0.7

provide_liquidity = [
    score < threshold
    for score in signals
]

print(provide_liquidity)
```

结果：

```text
[True, False, True]
```

这里把高于阈值的 adverse selection score 过滤掉。

实际模型可以更复杂，但原则是一样的：

```text
信息风险高时，少提供流动性或提高报价补偿。
```

## 费用和返佣不能掩盖风险

有些市场 maker 有返佣。

但返佣不一定能覆盖不利选择。

例如：

```python
spread_bps = 4
adverse_bps = 6
rebate_bps = 1

net_cost_bps = adverse_bps - spread_bps / 2 - rebate_bps

print(net_cost_bps)
```

结果：

```text
3.0
```

半价差收益是 `2 bps`，返佣是 `1 bps`。

但 adverse selection 成本是 `6 bps`。

净成本仍然是 `3 bps`。

所以 maker 策略不能只看返佣和 spread。

## 回测中的常见错误

adverse selection 在回测里很容易被低估。

常见错误包括：

```text
假设所有限价单触价都成交
只统计成交样本，不统计未成交机会
用成交价相对当时 mid 的优势当作收益
忽略成交后价格漂移
用未来盘口信息决定是否撤单
没有建模公告、高波动和跨市场领先价格
```

尤其是 maker 策略，如果不模拟 queue position 和成交选择偏差，结果通常会过于乐观。

## 和 inventory risk 的区别

adverse selection 和 inventory risk 有联系，但不是同一件事。

adverse selection 关注：

```text
为什么这笔成交发生？
对手方是否更有信息？
成交后价格是否立即不利漂移？
```

inventory risk 关注：

```text
成交后我持有什么仓位？
价格波动会如何影响库存价值？
仓位偏离目标时如何调整报价？
```

下一篇会专门讨论 inventory risk。

它会从持仓风险和报价调节角度解释做市策略的另一个核心约束。

## 小结

adverse selection 是流动性提供者面对的信息不对称风险。

核心判断不是：

```text
我有没有赚到半个 spread？
```

而是：

```text
成交后价格是否系统性地朝对我不利的方向移动？
```

实践中要同时看：

```text
成交时 spread
成交后 mid 漂移
主动单方向
order imbalance
queue position
公告和波动状态
realized spread
```

如果这些变量显示信息风险很高，单纯提供流动性可能不是低风险套利，而是在接信息更强的订单。
