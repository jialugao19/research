# 130. 市场微观结构扩展：事件驱动回测、向量化回测、偏差和交易成本

## 核心概念

回测框架用来回答：

```text
如果过去按这个策略交易，结果会怎样？
```

但一个回测是否可信，关键不在代码跑得多快。

关键在于它是否正确模拟了：

```text
信息到达时间
信号生成时间
下单时间
成交价格
交易成本
可交易资产池
组合约束
```

回测最常见的问题不是少赚一点。

而是把现实中不可能获得的信息或成交价格放进了历史结果。

## 向量化回测

向量化回测通常用数组或表格一次性计算。

例如：

```text
收益序列 * 持仓序列 = 策略收益
```

小例子：

```python
prices = [100, 102, 101, 105]
returns = [
    prices[i] / prices[i - 1] - 1
    for i in range(1, len(prices))
]
signals = [1, 0, 1]

strategy_returns = [
    signal * ret
    for signal, ret in zip(signals, returns)
]

print([round(x, 4) for x in returns])
print([round(x, 4) for x in strategy_returns])
print(round(sum(strategy_returns), 4))
```

结果：

```text
[0.02, -0.0098, 0.0396]
[0.02, -0.0, 0.0396]
0.0596
```

这种写法很快。

但它默认 `signals[0]` 能吃到第一个收益。

如果信号是在第一个收益结束后才知道，这就是前视偏差。

## 信号必须滞后

更合理的处理是：

```text
今天收盘后得到信号
明天才能持仓获得收益
```

```python
prices = [100, 102, 101, 105]
signals = [1, 0, 1]

positions = [0] + signals[:-1]
returns = [
    prices[i] / prices[i - 1] - 1
    for i in range(1, len(prices))
]
strategy_returns = [
    position * ret if position else 0
    for position, ret in zip(positions, returns)
]

print(positions)
print([round(x, 4) for x in strategy_returns])
```

结果：

```text
[0, 1, 0]
[0, -0.0098, 0]
```

同样的价格和信号，滞后后结果完全不同。

这说明回测里 `shift` 的方向非常重要。

## 事件驱动回测

事件驱动回测按时间顺序处理事件。

常见事件包括：

```text
行情更新
信号更新
下单
成交
撤单
资金和持仓更新
风控检查
```

简化事件流：

```python
orders = [
    {"time": 1, "type": "signal", "action": "buy"},
    {"time": 2, "type": "fill", "price": 100.1},
]

print([event["type"] for event in orders])
```

结果：

```text
['signal', 'fill']
```

事件驱动回测更接近真实交易。

它可以自然处理：

```text
订单延迟
部分成交
成交队列
盘中风控
不同数据源时间戳
```

缺点是实现复杂、运行较慢。

## 成交和持仓更新

事件驱动回测会显式更新现金和持仓。

例如买入 `5` 股，价格 `100`：

```python
cash = 1000
shares = 0
price = 100
order_qty = 5

cost = order_qty * price
cash -= cost
shares += order_qty

print(cash)
print(shares)
```

结果：

```text
500
5
```

真实系统还要扣：

```text
手续费
印花税或交易税
滑点
spread
market impact
借券成本
融资成本
```

## 向量化和事件驱动的取舍

向量化回测适合：

```text
日频或低频策略
初步研究
快速参数扫描
信号探索
成交假设简单的组合策略
```

事件驱动回测适合：

```text
高频策略
订单簿策略
复杂执行逻辑
盘中风控
需要模拟成交和撤单的策略
```

一个实用流程是：

```text
先用向量化回测快速验证信号
再用事件驱动回测验证执行可行性
最后用真实交易日志做归因和校准
```

## 幸存者偏差

幸存者偏差是指只使用最后仍然存在的资产。

例如历史上有三只股票：

```python
all_assets = {
    "A": 0.10,
    "B": -0.30,
    "C": 0.05,
}
survivors = {
    "A": 0.10,
    "C": 0.05,
}

all_mean = sum(all_assets.values()) / len(all_assets)
survivor_mean = sum(survivors.values()) / len(survivors)

print(round(all_mean, 4))
print(round(survivor_mean, 4))
```

结果：

```text
-0.05
0.075
```

包含退市或失败资产时，平均收益是 `-5%`。

只看幸存者时，平均收益变成 `7.5%`。

这会严重高估策略。

## 前视偏差

前视偏差是指使用预测时点还不知道的信息。

最明显的错误是直接用未来收益做信号：

```python
prices = [100, 102, 101]

future_return_signal = [
    prices[i + 1] / prices[i] - 1
    for i in range(len(prices) - 1)
]

print([round(x, 4) for x in future_return_signal])
```

结果：

```text
[0.02, -0.0098]
```

这个信号当然很准。

因为它就是未来收益。

真实回测必须根据数据发布时间和策略决策时间，明确每个字段什么时候可用。

## 交易成本

交易成本必须进回测。

一个简单换手成本模型：

```python
old_weights = [0.5, 0.5]
new_weights = [0.8, 0.2]
cost_bps = 10

turnover = sum(
    abs(new - old)
    for new, old in zip(new_weights, old_weights)
) / 2
cost = turnover * cost_bps / 10000

print(round(turnover, 4))
print(round(cost, 6))
```

结果：

```text
0.3
0.0003
```

`30%` 单边换手，在 `10 bps` 成本下，组合损失是 `0.03%`。

高换手策略必须特别关注这部分。

## bid/ask 成交价格

如果按 mid 成交，通常会低估成本。

```python
mid = 100.00
spread = 0.04

buy_price = mid + spread / 2
sell_price = mid - spread / 2

print(buy_price)
print(sell_price)
```

结果：

```text
100.02
99.98
```

买入应接近 ask。

卖出应接近 bid。

如果回测用 `100.00` 同时买卖，就免费消除了 spread。

## 净值曲线

策略收益要复利累积成净值。

```python
returns = [0.01, -0.02, 0.03]

equity = 1.0
curve = []
for ret in returns:
    equity *= (1 + ret)
    curve.append(equity)

print([round(x, 6) for x in curve])
```

结果：

```text
[1.01, 0.9898, 1.019494]
```

净值曲线比简单收益和更真实。

它能反映复利、回撤和路径依赖。

## 成本不只是手续费

完整交易成本至少包括：

```text
佣金和交易所费用
bid-ask spread
滑点
market impact
借券成本
融资成本
税费
未成交和部分成交
```

低频策略可能手续费更显眼。

高频或大资金策略里，spread 和 market impact 经常更重要。

## 事件时间线

可信回测要有清晰时间线。

例如：

```text
t0: 数据发布
t1: 信号生成
t2: 下单
t3: 成交
t4: 组合更新
```

不能把 `t3` 或 `t4` 才知道的信息放回 `t1`。

这条规则适用于：

```text
财报数据
指数成分
行业分类
成交量
VWAP
收盘价
tick 数据修正
```

## 常见回测检查清单

回测完成后至少检查：

```text
信号是否滞后到可交易时点
资产池是否包含历史退市和历史成分
财务和基本面数据是否按公告日可用
成交价格是否使用可执行价格
交易成本是否包括 spread 和 impact
是否限制成交量参与率
是否模拟停牌、涨跌停和不可交易日
是否避免用全样本参数
是否记录换手、回撤和容量
```

这些检查比调参更重要。

有偏差的回测再漂亮也不能说明策略可交易。

## 小结

回测框架的核心是还原历史中的可获得信息和可执行交易。

要区分：

```text
向量化回测：快，适合信号研究
事件驱动回测：慢，但更接近真实交易
```

同时要系统控制：

```text
幸存者偏差
前视偏差
交易成本
滑点和 market impact
成交约束
数据发布时间
```

到这里，Market Microstructure 部分完成。

下一篇进入计算机基础，从算法复杂度和大 O 表示法开始。
