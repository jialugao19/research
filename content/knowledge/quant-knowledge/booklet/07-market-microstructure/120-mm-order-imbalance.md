# 市场微观结构：order imbalance 的盘口数量不平衡和短期价格压力

## 核心概念

order imbalance 是订单不平衡。

在盘口里，它通常指买盘数量和卖盘数量不对称。

最简单的直觉是：

```text
买盘厚、卖盘薄 -> 短期向上压力可能更大
卖盘厚、买盘薄 -> 短期向下压力可能更大
```

但这只是压力信号，不是确定预测。

因为盘口上的数量可能撤掉，也可能被隐藏流动性改变。

## 一档 order imbalance

最常见的一档指标使用 best bid size 和 best ask size。

定义：

```text
imbalance = (bid_size - ask_size) / (bid_size + ask_size)
```

例子：

```python
bid_size = 800
ask_size = 200

imbalance = (bid_size - ask_size) / (bid_size + ask_size)

print(imbalance)
```

结果：

```text
0.6
```

这个值在 `[-1, 1]` 之间。

含义是：

```text
接近 1：买盘明显更厚
接近 -1：卖盘明显更厚
接近 0：两边数量接近
```

## 为什么要归一化

直接用差值：

```text
bid_size - ask_size
```

会受到资产活跃度影响。

例如：

```text
大盘股盘口数量通常更大
冷门股票盘口数量通常更小
期货不同合约深度差异很大
```

归一化后，指标更容易跨时点和跨资产比较。

```text
(bid_size - ask_size) / (bid_size + ask_size)
```

不过归一化不代表完全可比。

还要结合 spread、成交量、tick size 和市场状态。

## 多档 order imbalance

只看一档可能太噪声。

可以把前几档盘口数量加总。

```python
bid_sizes = [500, 300, 200]
ask_sizes = [200, 250, 350]

total_bid = sum(bid_sizes)
total_ask = sum(ask_sizes)
imbalance = (total_bid - total_ask) / (total_bid + total_ask)

print(total_bid)
print(total_ask)
print(round(imbalance, 4))
```

结果：

```text
1000
800
0.1111
```

虽然第一档可能很不平衡，但合并多档后，整体压力可能没那么极端。

多档指标更稳定，但也更慢。

因为离 best bid / ask 更远的挂单，不一定马上影响下一笔成交。

## 加权多档 imbalance

更常见的做法是给近端盘口更高权重。

例如第一档权重 `1.0`，第二档 `0.5`，第三档 `0.25`。

```python
bid_sizes = [500, 300, 200]
ask_sizes = [200, 250, 350]
weights = [1.0, 0.5, 0.25]

weighted_bid = sum(
    size * weight
    for size, weight in zip(bid_sizes, weights)
)
weighted_ask = sum(
    size * weight
    for size, weight in zip(ask_sizes, weights)
)
imbalance = (weighted_bid - weighted_ask) / (weighted_bid + weighted_ask)

print(weighted_bid)
print(weighted_ask)
print(round(imbalance, 4))
```

结果：

```text
700.0
412.5
0.2584
```

加权后，靠近成交价的挂单影响更大。

这通常比简单加总更贴近短期价格形成。

## 时间序列中的 imbalance

order imbalance 通常不是单点使用，而是作为时间序列特征。

例如连续三个盘口快照：

```python
snapshots = [
    {"bid_size": 500, "ask_size": 500},
    {"bid_size": 700, "ask_size": 300},
    {"bid_size": 300, "ask_size": 900},
]

values = []
for row in snapshots:
    bid = row["bid_size"]
    ask = row["ask_size"]
    values.append((bid - ask) / (bid + ask))

print(values)
```

结果：

```text
[0.0, 0.4, -0.5]
```

这个序列表示盘口压力从中性变成偏买方，再变成偏卖方。

策略通常会关心：

```text
imbalance 的水平
imbalance 的变化速度
imbalance 是否持续
imbalance 是否和成交方向一致
```

## order flow imbalance

order imbalance 看的是当前盘口存量。

order flow imbalance 更关注盘口变化。

例如 bid size 增加、ask size 减少，说明买方压力增强。

一个简化例子：

```python
prev_bid = 500
new_bid = 650
prev_ask = 400
new_ask = 300

bid_change = new_bid - prev_bid
ask_change = new_ask - prev_ask
ofi = bid_change - ask_change

print(bid_change)
print(ask_change)
print(ofi)
```

结果：

```text
150
-100
250
```

这里：

```text
bid 增加 150
ask 减少 100
ofi = 250
```

这表示盘口变化方向偏向买方。

真实 order flow imbalance 会更复杂，因为还要处理价格档位变化、撤单和成交。

## 和 spread 的关系

order imbalance 不能脱离 spread 看。

如果 spread 很宽，即使 imbalance 很强，交易成本也可能吃掉信号。

例如：

```python
imbalance = 0.7
spread_bps = 8

can_trade = imbalance > 0.5 and spread_bps < 5

print(can_trade)
```

结果：

```text
False
```

这表示盘口偏买方，但成本太高。

策略上可能选择不交易，或者改用限价单等待。

## 信号方向和滞后

如果用 order imbalance 预测未来收益，必须严格滞后。

正确方式是：

```text
用当前 imbalance 预测未来 return
```

小例子：

```python
imbalances = [0.2, 0.6, -0.4]
future_returns = [0.001, -0.002, 0.0005]

aligned = list(zip(imbalances[:-1], future_returns[1:]))
wrong = list(zip(imbalances, future_returns))

print(aligned)
print(wrong)
```

结果：

```text
[(0.2, -0.002), (0.6, 0.0005)]
[(0.2, 0.001), (0.6, -0.002), (-0.4, 0.0005)]
```

第一行表示用当前 imbalance 配下一期收益。

第二行把同一时点的特征和收益直接配对。

如果收益在该时点结束后才知道，第二种写法会有前视风险。

## 平滑和去噪

盘口变化很快，单个快照的 imbalance 很噪声。

可以用短窗口平均减少噪声。

```python
values = [0.1, 0.3, 0.2, -0.1]
window = 2

rolling = []
for i in range(window, len(values) + 1):
    rolling.append(sum(values[i - window:i]) / window)

print(rolling)
```

结果：

```text
[0.2, 0.25, 0.05]
```

平滑会降低噪声，但也会引入滞后。

窗口越长，信号越稳定，也越慢。

在高频场景里，这个权衡非常关键。

## 常见误区

order imbalance 常见误区包括：

```text
认为买盘厚就一定上涨
忽略盘口撤单和虚假挂单
只看一档，不看多档深度
只看数量，不看 spread 和成交量
用未来盘口构造当前信号
把不同资产的原始盘口数量直接比较
忽略 tick size 和交易规则差异
```

尤其要注意：

```text
盘口数量是可撤销的意愿，不是保证成交的承诺。
```

所以 imbalance 更适合作为短期压力变量，而不是单独的交易决策。

## 实战用法

在策略里，order imbalance 常用于：

```text
短期价格方向预测
限价单挂单方向选择
是否追单或等待
盘口压力过滤器
成交算法里的短期市场状态判断
```

典型使用方式不是单独下单，而是和其他变量一起用：

```text
imbalance + spread
imbalance + recent trades
imbalance + volatility
imbalance + queue position
imbalance + order arrival rate
```

这样可以减少单一盘口快照带来的误判。

## 小结

order imbalance 衡量买卖盘数量不平衡。

它的基本形式是：

```text
(bid_size - ask_size) / (bid_size + ask_size)
```

实践中要关注：

```text
一档还是多档
是否按距离 best price 加权
是否与 spread 和成交量一起解释
是否严格用预测时可见的盘口
是否避免跨资产原始数量直接比较
```

下一篇讨论 queue position。

它会解释为什么即使挂在同一个价格，排队靠前和靠后的成交概率也完全不同。
