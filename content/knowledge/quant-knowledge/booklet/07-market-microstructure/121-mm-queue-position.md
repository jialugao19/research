# Queue Position

## 核心概念

queue position 是队列位置。

在限价订单簿里，同一个价格上可能有很多订单排队。

如果交易所采用价格优先、时间优先规则，那么：

```text
价格更优的订单先成交
同一价格上，先提交的订单先成交
```

所以，即使你和别人挂在同一个 bid 或 ask，你的成交概率也取决于你前面还有多少订单。

这就是 queue position 的核心。

## 为什么同价不同命

假设 best bid 是 `100.00`。

你也挂买单在 `100.00`。

如果你前面已经有 `700` 股排队，而接下来只有 `500` 股主动卖单打进来，那么成交只会消耗你前面的人。

```python
queue_ahead = 700
my_order = 100
incoming_sell = 500

filled_before_me = min(queue_ahead, incoming_sell)
remaining_ahead = queue_ahead - filled_before_me
my_fill = max(0, incoming_sell - queue_ahead)
my_fill = min(my_order, my_fill)

print(remaining_ahead)
print(my_fill)
```

结果：

```text
200
0
```

含义是：

```text
前方队列还剩 200
我的订单成交 0
```

你虽然挂在 best bid，但没有成交。

## 前方队列被打穿

如果主动卖单足够大，先消耗前方队列，然后才轮到你。

```python
queue_ahead = 300
my_order = 100
incoming_sell = 450

my_fill = min(
    my_order,
    max(0, incoming_sell - queue_ahead)
)

print(my_fill)
```

结果：

```text
100
```

这里主动卖单先消耗前方 `300` 股，然后还有 `150` 股继续成交。

你的 `100` 股订单可以全部成交。

## FIFO 队列

很多市场在同一价格层采用 FIFO。

FIFO 是 first in, first out。

假设同一价格上有三个订单：

```python
orders = [
    {"id": "A", "size": 200},
    {"id": "B", "size": 300},
    {"id": "me", "size": 100},
]

queue_ahead = 0
for order in orders:
    if order["id"] == "me":
        break
    queue_ahead += order["size"]

print(queue_ahead)
```

结果：

```text
500
```

你的前方队列是 `500`。

只有前方 `500` 被成交或撤掉后，才轮到你。

## 撤单对队列位置的影响

queue position 不只会被成交消耗，也会被撤单改善。

如果你前方有 `500` 股，其中 `200` 股撤单：

```python
queue_ahead = 500
cancellations_ahead = 200

new_queue_ahead = max(0, queue_ahead - cancellations_ahead)

print(new_queue_ahead)
```

结果：

```text
300
```

你的位置变好了。

这也是为什么高频交易会关心：

```text
前方成交
前方撤单
同价新增订单
价格档位变化
```

只看盘口总量，不知道自己在队列里的位置，成交概率会估错。

## 用成交量估算填单

一个很粗的 fill estimate 可以这样做：

```text
expected_fill = max(0, expected_aggressive_volume - queue_ahead)
```

再截断到自己的订单大小。

```python
queue_ahead = 400
expected_sell_volume = 600
my_order = 100

expected_fill = min(
    my_order,
    max(0, expected_sell_volume - queue_ahead)
)
fill_rate = expected_fill / my_order

print(expected_fill)
print(fill_rate)
```

结果：

```text
100
1.0
```

这表示在这个简化估计下，订单可以完全成交。

真实填单模型还要考虑：

```text
撤单率
新增挂单
隐藏订单
部分成交
价格跳动
交易所撮合规则
自己的订单是否会改变市场行为
```

## 队列消耗过程

队列位置可以随着每笔成交逐步更新。

例如前方有 `500` 股，后续同价成交量依次为 `100`、`150`、`200`：

```python
queue_ahead = 500
trade_sizes = [100, 150, 200]

for trade in trade_sizes:
    queue_ahead = max(0, queue_ahead - trade)

print(queue_ahead)
```

结果：

```text
50
```

前方队列还剩 `50`。

这时你仍然没有成交，但已经接近队首。

## 改价会失去优先级

如果你撤单再重新挂单，通常会失去原来的时间优先级。

例如从 `100.00` 改到 `99.99`，这已经不是同一个价格队列。

```python
initial_bid = 100.00
new_bid = 99.99

kept_priority = initial_bid == new_bid

print(kept_priority)
```

结果：

```text
False
```

改价可能降低被不利成交的风险，也可能让你重新排到队尾。

所以限价单执行不是简单地“挂单就省半个 spread”。

你还要付出等待和未成交风险。

## maker 和 taker 的权衡

主动单 taker 的优点是：

```text
马上成交
执行不确定性小
不会错过当前机会
```

缺点是：

```text
支付 spread
可能产生更大 market impact
```

限价单 maker 的优点是：

```text
可能赚取 spread
费用结构可能更好
可以控制成交价格
```

缺点是：

```text
不一定成交
成交时可能代表市场正向不利方向移动
队列位置靠后时等待成本高
```

queue position 正是 maker 策略的核心风险变量之一。

## 未成交风险

如果你选择挂限价单，可能发生：

```text
价格直接向有利方向走，但你没成交
价格向不利方向走，你成交了
价格在原地震荡，你排队很久
```

这会造成选择偏差。

回测中如果假设所有触碰到限价的订单都成交，就会高估 maker 策略。

更合理的回测至少要问：

```text
触价时我前方有多少队列？
后续成交量是否足够消耗前方队列？
前方撤单是否可观测？
我的订单是否会改变盘口？
未成交时是否追单？
```

## adverse selection 风险

queue position 还和 adverse selection 有关。

有时你排队很久没成交。

一旦成交，可能是因为有人急着卖给你。

这可能意味着价格即将下跌。

因此 maker 成交并不总是好事。

它可能代表：

```text
你赚到了 spread
也可能接住了有信息的卖单
```

这就是下一篇 adverse selection 要重点讨论的问题。

## 简单执行决策

一个很粗的执行判断可以写成：

```text
if expected_alpha > spread_cost + adverse_selection_cost:
    take liquidity
elif fill_probability is high and adverse_selection_cost is low:
    provide liquidity
else:
    wait
```

小例子：

```python
spread_cost_bps = 2
missed_alpha_bps = 5
adverse_move_bps = 3

net_value = missed_alpha_bps - spread_cost_bps - adverse_move_bps

print(net_value)
```

结果：

```text
0
```

这里主动成交节省了错过机会的损失，但 spread 和不利价格变动刚好抵消收益。

真实执行模型会更复杂，但核心仍然是：

```text
成交概率
等待成本
spread 成本
不利选择成本
```

## 和 order imbalance 的关系

上一篇的 order imbalance 衡量盘口两边数量不平衡。

queue position 更进一步问：

```text
在这边盘口里，我排在哪里？
```

例如买盘很厚，可能说明下方支撑强。

但如果你作为买单排在很后面，短时间内未必能成交。

所以：

```text
imbalance 描述盘口整体压力
queue position 描述我的订单执行机会
```

两者经常一起使用。

## 小结

queue position 解释了限价单成交的排队机制。

实践中要区分：

```text
best price 上有多少总量
我前方有多少量
前方量是被成交消耗还是撤单消失
改价是否会丢失时间优先级
未成交时策略如何处理
```

对 maker 策略和高频执行来说，queue position 是比静态 bid/ask 更接近真实成交结果的变量。

下一篇讨论 adverse selection。

它会解释为什么“被成交”有时反而是坏消息。
