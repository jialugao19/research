# 129. 市场微观结构：bid-ask bounce、VWAP、tick 数据特性和高频数据清洗

## 核心概念

tick 数据是最细粒度的市场数据之一。

它通常包含：

```text
逐笔成交
逐笔报价
盘口更新
成交量
买卖方向估计
时间戳
```

tick 数据看起来信息丰富，但不能直接当成干净时间序列使用。

原因是：

```text
成交价会在 bid 和 ask 之间跳动
成交时间不等间隔
数据可能重复、乱序、缺失
报价可能异常
大单和拆单会改变成交序列
```

这一篇重点讲三个概念：

```text
bid-ask bounce
VWAP
tick 数据特性与清洗
```

## bid-ask bounce

bid-ask bounce 是成交价在买一价和卖一价之间来回跳动造成的噪声。

假设真实 mid 一直是 `100.00`。

bid 是 `99.98`，ask 是 `100.02`。

如果成交价交替发生在 ask 和 bid：

```python
prices = [100.02, 99.98, 100.02, 99.98]

returns = [
    prices[i] / prices[i - 1] - 1
    for i in range(1, len(prices))
]

print([round(ret, 6) for ret in returns])
```

结果：

```text
[-0.0004, 0.0004, -0.0004]
```

看起来价格在上下震荡。

但 mid 其实没有动。

这就是 bid-ask bounce。

如果直接用逐笔成交价算超短期收益，可能会把成交方向变化误认为真实价格变化。

## 用 mid price 降低 bounce

mid price 是 bid 和 ask 的中点。

```python
bid = 99.98
ask = 100.02

mid = (bid + ask) / 2

print(mid)
```

结果：

```text
100.0
```

用 mid price 计算收益，可以减少 bid-ask bounce。

但 mid price 也不是完美价格。

因为：

```text
mid 不一定可成交
盘口可能很薄
bid/ask 可能快速撤单
宽 spread 下 mid 的经济意义更弱
```

所以研究时要明确：

```text
用 trade price 研究成交
用 mid price 研究报价中点变化
用 bid/ask 研究真实可执行价格
```

## mid return

如果使用 mid price 序列：

```python
mid_prices = [100.0, 100.1, 100.3]

mid_returns = [
    mid_prices[i] / mid_prices[i - 1] - 1
    for i in range(1, len(mid_prices))
]

print([round(ret, 6) for ret in mid_returns])
```

结果：

```text
[0.001, 0.001998]
```

这更接近报价中点的变化。

但如果策略要真实成交，仍然要回到 bid/ask 和订单簿深度。

## VWAP

VWAP 是 volume-weighted average price。

中文常叫成交量加权平均价。

公式是：

```text
VWAP = sum(price * volume) / sum(volume)
```

小例子：

```python
prices = [100.0, 100.2, 99.9]
volumes = [200, 300, 500]

vwap = sum(
    price * volume
    for price, volume in zip(prices, volumes)
) / sum(volumes)

print(round(vwap, 4))
```

结果：

```text
100.01
```

成交量大的价格对 VWAP 影响更大。

这里 `99.9` 的成交量最大，所以 VWAP 被往下拉。

## VWAP 的用途

VWAP 常用于：

```text
衡量执行质量
构造日内基准价
分析成交集中在哪些价格
做 VWAP 执行算法
```

例如一笔买单平均成交价低于市场 VWAP，通常说明执行相对较好。

但 VWAP 也有局限。

它是成交结果，不是可交易承诺。

如果一个策略用全天 VWAP 生成信号，又假设能在同一天 VWAP 成交，就可能有前视偏差。

## tick 数据不等间隔

tick 数据不是每秒固定一条。

活跃时段可能一秒有很多笔。

冷清时段可能几分钟没有成交。

这会带来问题：

```text
不能直接把 tick 当作均匀时间序列
rolling window 的含义可能变成笔数窗口而不是时间窗口
高成交频率时段权重更高
缺失成交不等于价格不变
```

常见处理方式包括：

```text
按时间重采样
按成交量分桶
按事件数分桶
只使用 quote mid 的固定时间快照
```

## tick 乱序

真实 tick 数据可能乱序。

例如：

```python
ticks = [
    {"time": 3, "price": 100.2},
    {"time": 1, "price": 100.0},
    {"time": 2, "price": 100.1},
]

ordered = sorted(
    ticks,
    key=lambda row: row["time"]
)

print([row["price"] for row in ordered])
```

结果：

```text
[100.0, 100.1, 100.2]
```

如果不排序，收益、成交方向和盘口状态都会错。

高频数据处理的第一步通常就是按时间戳和序列号重建顺序。

## 重复 tick

数据源可能出现重复记录。

```python
trades = [
    {"time": "09:30:01", "price": 100.0, "volume": 100},
    {"time": "09:30:01", "price": 100.0, "volume": 100},
    {"time": "09:30:02", "price": 100.1, "volume": 50},
]

unique = []
seen = set()
for trade in trades:
    key = (
        trade["time"],
        trade["price"],
        trade["volume"],
    )
    if key not in seen:
        unique.append(trade)
        seen.add(key)

print(unique)
```

结果：

```text
[{'time': '09:30:01', 'price': 100.0, 'volume': 100}, {'time': '09:30:02', 'price': 100.1, 'volume': 50}]
```

去重规则要谨慎。

因为同一时间、同一价格、同一数量也可能是真实的两笔不同成交。

如果数据有交易编号，应优先使用交易编号去重。

## 异常价格过滤

tick 数据里可能有错误价格或特殊成交。

例如：

```python
prices = [100.0, 100.1, 150.0, 100.2]

filtered = [
    price
    for price in prices
    if 90 <= price <= 110
]

print(filtered)
```

结果：

```text
[100.0, 100.1, 100.2]
```

这里 `150.0` 被过滤掉。

真实清洗不能只靠固定阈值。

还要结合：

```text
涨跌停规则
成交条件代码
quote mid
前后价格
成交量
交易所修正记录
```

## 报价有效性

quote 数据也可能异常。

例如 bid 高于 ask：

```python
quotes = [
    {"bid": 99.9, "ask": 100.1},
    {"bid": 100.2, "ask": 100.1},
]

valid = [
    quote
    for quote in quotes
    if quote["bid"] <= quote["ask"]
]

print(valid)
```

结果：

```text
[{'bid': 99.9, 'ask': 100.1}]
```

`bid > ask` 通常说明数据错位、延迟或市场状态特殊。

不能直接拿来算 spread。

## 成交方向估计

很多微观结构指标需要知道成交是主动买还是主动卖。

如果没有交易方向，可以用成交价相对 mid 粗略估计。

```python
trade_price = 100.08
bid = 99.98
ask = 100.10

side = "buy" if trade_price >= (bid + ask) / 2 else "sell"

print(side)
```

结果：

```text
buy
```

这个规则很粗。

在成交价等于 mid、报价延迟或暗池成交时，方向估计可能错。

方向错误会影响：

```text
order imbalance
VPIN
adverse selection
买卖压力分析
```

## 高频回测中的前视问题

tick 数据回测很容易泄露未来。

常见错误包括：

```text
用成交后才更新的 quote 判断成交前信号
用当前 bar 的完整 VWAP 做当前 bar 决策
用未来 tick 修正当前成交方向
用日内最终成交量决定早盘参与率
忽略数据发布时间和交易所延迟
```

正确做法是：

```text
每个时点只能使用当时已经到达的数据
quote 和 trade 要按真实时间线合并
bar 特征只能在 bar 完成后使用
执行价格要用信号之后可成交的 bid/ask 或订单簿
```

## 小结

tick 数据比日频数据更细，但也更脏。

需要重点理解：

```text
bid-ask bounce 会制造虚假短期反转
mid price 可以降低 bounce，但不是可成交价
VWAP 是成交量加权平均价，不能随意当作可交易价格
tick 数据可能乱序、重复、缺失和异常
quote 数据也需要检查 bid <= ask
成交方向估计会影响许多微观结构指标
```

下一篇讨论回测框架。

它会比较事件驱动回测和向量化回测，并系统总结幸存者偏差、前视偏差和交易成本如何纳入。
