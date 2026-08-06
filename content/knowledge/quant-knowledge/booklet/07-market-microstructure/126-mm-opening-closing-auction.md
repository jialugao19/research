# 126. 市场微观结构：opening/closing auction 的集合竞价撮合价、订单不平衡和开收盘流动性

## 核心概念

opening auction 和 closing auction 是开盘集合竞价和收盘集合竞价。

它们和连续竞价不同。

连续竞价是：

```text
订单到达后，只要价格匹配就连续成交
```

集合竞价是：

```text
在一段时间内收集订单
到指定时点统一撮合
用一个或少数几个价格成交
```

开盘集合竞价用于形成开盘价。

收盘集合竞价用于形成收盘价。

这两个价格对指数、基金估值、业绩归因和回测都很重要。

## 集合竞价撮合价

简化地说，集合竞价会在候选价格中选择一个撮合价。

常见直觉是：

```text
选择能最大化成交量的价格
```

不同交易所还有更细的平局规则。

这里先看一个简化例子。

买单：

```text
限价 100.0 买 300
限价 99.9 买 200
限价 99.8 买 500
```

卖单：

```text
限价 99.8 卖 200
限价 99.9 卖 400
限价 100.0 卖 100
```

```python
buy_orders = [(100.0, 300), (99.9, 200), (99.8, 500)]
sell_orders = [(99.8, 200), (99.9, 400), (100.0, 100)]

prices = sorted({
    price
    for price, _ in buy_orders + sell_orders
})

results = []
for price in prices:
    buy_qty = sum(qty for limit, qty in buy_orders if limit >= price)
    sell_qty = sum(qty for limit, qty in sell_orders if limit <= price)
    executable = min(buy_qty, sell_qty)
    results.append((price, buy_qty, sell_qty, executable))

print(results)
print(max(results, key=lambda row: row[3]))
```

结果：

```text
[(99.8, 1000, 200, 200), (99.9, 500, 600, 500), (100.0, 300, 700, 300)]
(99.9, 500, 600, 500)
```

在这个简化规则下，`99.9` 的可成交量最大。

所以撮合价是 `99.9`。

## 为什么开盘需要 auction

开盘前有大量隔夜信息。

例如：

```text
公司公告
宏观数据
海外市场变化
盘前订单积累
指数成分调整预期
```

如果一开盘就连续撮合，价格可能剧烈跳动。

集合竞价把订单集中起来，用统一价格撮合，可以让开盘价更集中地反映供需。

但这不代表开盘没有风险。

开盘时仍然可能：

```text
spread 宽
成交量集中
价格跳空
盘口深度不稳定
```

## 收盘 auction 的重要性

收盘价经常用于：

```text
基金净值
指数计算
业绩基准
风险模型输入
日频回测价格
```

因此收盘 auction 往往有大量订单。

例如：

```text
指数基金要按收盘价跟踪指数
主动基金要接近收盘价调仓
交易算法要在收盘前完成剩余订单
```

这会让收盘附近的流动性和价格行为与日内普通时段不同。

## MOC 和 LOC

收盘集合竞价里常见两类订单。

MOC 是 market-on-close。

```text
无指定价格，要求按收盘 auction 价格成交
```

LOC 是 limit-on-close。

```text
只在收盘 auction 中参与，并且有价格限制
```

小例子：

```python
market_on_close = 500
limit_on_close = 300

total_close_buy = market_on_close + limit_on_close

print(total_close_buy)
```

结果：

```text
800
```

这表示收盘买入需求合计 `800`。

真实撮合时，LOC 是否成交还取决于最终 auction price 是否满足限价。

## 订单不平衡

auction 期间，交易所可能发布 indicative imbalance。

它表示当前买卖需求不平衡。

例如买量 `1000`，卖量 `700`：

```python
buy_qty = 1000
sell_qty = 700

imbalance = buy_qty - sell_qty
imbalance_ratio = imbalance / (buy_qty + sell_qty)

print(imbalance)
print(round(imbalance_ratio, 4))
```

结果：

```text
300
0.1765
```

正数表示买方需求更强。

负数表示卖方需求更强。

imbalance 可能吸引套利者或流动性提供者参与，帮助平衡供需。

## indicative price

auction 期间还可能发布 indicative price。

它是根据当前订单簿估计的可能撮合价。

如果 indicative price 持续上移，说明当前订单流偏向买方。

```python
indicative_prices = [99.8, 100.1, 100.0, 100.2]

returns = [
    price / indicative_prices[0] - 1
    for price in indicative_prices
]

print([round(value, 4) for value in returns])
```

结果：

```text
[0.0, 0.003, 0.002, 0.004]
```

这里 indicative price 相对初始值最高上移约 `0.4%`。

但 indicative price 会随订单新增和撤单变化。

它不是最终成交价的保证。

## auction volume 占比

收盘 auction 的成交量可能占全天很大比例。

例如 auction 成交量 `2,000,000`，全天成交量 `20,000,000`：

```python
auction_volume = 2_000_000
daily_volume = 20_000_000

share = auction_volume / daily_volume

print(share)
```

结果：

```text
0.1
```

这表示 `10%` 的成交量集中在 auction。

如果策略大量依赖收盘价成交，必须考虑收盘 auction 的容量和冲击。

## auction return

可以用 auction price 相对连续交易最后价格的变化衡量 auction impact。

例如连续交易结束价是 `100.00`，auction price 是 `100.15`：

```python
close_price = 100.00
auction_price = 100.15

auction_return_bps = (auction_price / close_price - 1) * 10000

print(round(auction_return_bps, 2))
```

结果：

```text
15.0
```

auction 价格比连续交易结束价高 `15 bps`。

这可能来自真实信息，也可能来自收盘需求不平衡。

## imbalance 相对 ADV

订单不平衡的绝对数量要和资产流动性一起看。

例如 imbalance 是 `300,000` 股，平均日成交量是 `10,000,000` 股：

```python
imbalance_qty = 300_000
avg_daily_volume = 10_000_000

imbalance_adv_ratio = imbalance_qty / avg_daily_volume

print(imbalance_adv_ratio)
```

结果：

```text
0.03
```

这表示不平衡约为 ADV 的 `3%`。

对高流动性资产可能可吸收。

对低流动性资产可能已经很大。

## auction 订单统计

可以把不同类型的 auction 订单合并统计。

```python
orders = [
    {"type": "MOC", "side": "buy", "qty": 500},
    {"type": "LOC", "side": "buy", "qty": 300},
    {"type": "LOC", "side": "sell", "qty": 600},
]

buy = sum(
    order["qty"]
    for order in orders
    if order["side"] == "buy"
)
sell = sum(
    order["qty"]
    for order in orders
    if order["side"] == "sell"
)

print(buy)
print(sell)
```

结果：

```text
800
600
```

买方需求比卖方多 `200`。

但最终成交还取决于限价、优先级、交易所规则和新增订单。

## 开收盘流动性特征

开收盘 auction 的流动性有几个特点：

```text
成交集中在一个时点
订单不平衡可能突然变化
价格对大单更敏感
指数和基金相关需求较强
撤单和修改规则可能不同
最终价格有时难以提前精确预测
```

因此，使用开盘价或收盘价回测时，不能简单假设：

```text
任何规模都能无冲击按 open/close 成交
```

尤其是大资金策略。

## 回测中的常见错误

opening/closing auction 常见回测错误包括：

```text
用收盘价成交但不考虑收盘 auction 容量
用当日收盘价生成信号又按同一收盘价成交
忽略 auction imbalance 对成交价的影响
假设 MOC 一定完全成交且无冲击
使用最终 auction 信息做盘中决策
忽略不同市场的 auction 规则差异
```

如果信号用到了收盘后才能确认的数据，就不能再假设按同一日收盘价成交。

这是典型前视偏差。

## 和 market impact 的关系

auction 可以降低连续交易中的拆单冲击。

因为大量订单集中撮合。

但 auction 自身也有冲击：

```text
大额 MOC 可能推动 indicative price
不平衡订单可能造成 auction return
低流动性股票 auction 容量有限
```

所以执行选择不是简单地：

```text
auction 一定比连续交易便宜
```

而是要比较：

```text
连续交易的 spread 和 impact
auction 的容量和不平衡风险
未完成风险
信号时效
```

## 小结

opening/closing auction 是集中撮合机制。

它们对开盘价、收盘价、指数跟踪和日频回测非常重要。

关键概念包括：

```text
撮合价
最大可成交量
MOC / LOC
indicative price
imbalance
auction volume
auction return
```

实践中要特别注意：

```text
auction 信息在什么时候可见
订单是否真的能按 auction price 成交
容量是否足够
是否存在前视偏差
```

下一篇进入因子模型。

它会从 Fama-French 和 Barra 风险因子的角度，讨论因子构造、中性化、行业与市值控制。
