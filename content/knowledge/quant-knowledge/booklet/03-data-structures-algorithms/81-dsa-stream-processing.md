# Stream Processing

## 核心概念

stream processing 是流式处理。

它处理的不是一次性完整数据集，而是持续到达的事件：

```text
event_1, event_2, event_3, ...
```

每个事件到达后，系统更新内部状态，并可能输出结果。

典型事件：

```text
行情 tick
成交 trade
订单 order
撤单 cancel
风控告警
日志记录
特征更新
```

流式处理的核心是：

```text
用有限状态处理无限或很长的数据流
```

它和批处理的区别是：

```text
批处理：拿到一整张表，再统一计算
流处理：数据逐条到达，边来边算
```

## 流式处理回答的问题

流式处理常用于：

- 实时行情特征。
- 实时风控。
- 监控指标。
- 在线 top-k。
- 滚动窗口统计。
- 订单和成交事件回放。
- 在线数据清洗和去重。
- 实时 PnL 或敞口计算。

在量化系统里，你经常会看到：

```text
收到 tick -> 更新最近窗口 -> 更新特征 -> 判断信号 -> 更新订单状态
```

每一步都依赖当前状态。

## 事件结构

一个事件通常至少包含：

```text
event_id      事件唯一标识
event_time    事件发生时间
arrival_time  系统收到时间
key           分组键，例如 symbol
payload       业务数据
```

例子：

```python
event = {
    "event_id": "e1",
    "event_time": 93000,
    "arrival_time": 93001,
    "symbol": "AAPL",
    "price": 100.0,
    "size": 200,
}
```

注意区分：

```text
event_time    事件真实发生时间
arrival_time  事件进入系统的时间
```

乱序事件讨论的就是二者不一致时怎么办。

## 最简单的流式处理

假设事件按顺序到达，我们只累计成交量。

```python
events = [
    {"symbol": "AAPL", "size": 100},
    {"symbol": "MSFT", "size": 50},
    {"symbol": "AAPL", "size": 30},
]

total_size = 0

for event in events:
    total_size += event["size"]

print(total_size)
```

结果：

```text
180
```

这就是最小的在线状态：

```text
state = total_size
```

每来一个事件，状态更新一次。

## 按 key 维护状态

流式处理中，通常要按 `symbol`、`account`、`strategy_id` 等 key 维护状态。

```python
from collections import defaultdict

events = [
    {"symbol": "AAPL", "size": 100},
    {"symbol": "MSFT", "size": 50},
    {"symbol": "AAPL", "size": 30},
]

volume_by_symbol = defaultdict(int)

for event in events:
    symbol = event["symbol"]
    volume_by_symbol[symbol] += event["size"]

print(dict(volume_by_symbol))
```

结果：

```text
{'AAPL': 130, 'MSFT': 50}
```

这类状态叫 keyed state。

它的 key 可以是：

- 股票代码。
- 账户。
- 策略。
- 交易所。
- 日期。
- 任意业务分组字段。

## 在线均价 VWAP

流式计算 VWAP 时，不需要保存全部成交。

维护两个状态即可：

```text
sum_notional = sum(price * size)
sum_size     = sum(size)
```

```python
from collections import defaultdict

trades = [
    {"symbol": "AAPL", "price": 100.0, "size": 100},
    {"symbol": "AAPL", "price": 101.0, "size": 50},
    {"symbol": "MSFT", "price": 200.0, "size": 10},
]

notional = defaultdict(float)
volume = defaultdict(int)

for trade in trades:
    symbol = trade["symbol"]
    notional[symbol] += trade["price"] * trade["size"]
    volume[symbol] += trade["size"]

vwap = {
    symbol: notional[symbol] / volume[symbol]
    for symbol in volume
}

print(vwap)
```

结果：

```text
{'AAPL': 100.33333333333333, 'MSFT': 200.0}
```

这是典型的增量计算。

每个事件只处理一次。

## 固定长度最近窗口

如果只关心最近 N 个事件，可以用 `deque(maxlen=N)`。

```python
from collections import deque

prices = [100, 101, 99, 102, 103]
last3 = deque(maxlen=3)
snapshots = []

for price in prices:
    last3.append(price)
    snapshots.append(list(last3))

print(snapshots)
```

结果：

```text
[[100], [100, 101], [100, 101, 99], [101, 99, 102], [99, 102, 103]]
```

这种窗口按“条数”计数，不按时间计数。

适合：

- 最近 100 个 tick。
- 最近 20 笔成交。
- 最近 N 次延迟记录。

## 滑动窗口均值

条数窗口的均值可以用 `deque + running_sum`。

```python
from collections import deque

prices = [100, 101, 99, 102, 103]
window = 3

buffer = deque()
running_sum = 0
means = []

for price in prices:
    buffer.append(price)
    running_sum += price

    if len(buffer) > window:
        running_sum -= buffer.popleft()

    if len(buffer) == window:
        means.append(running_sum / window)

print(means)
```

结果：

```text
[100.0, 100.66666666666667, 101.33333333333333]
```

每个元素进队一次、出队一次。

总复杂度是：

```text
O(n)
```

## 按 key 的滑动窗口均值

多股票流里，每个 symbol 都有自己的窗口。

```python
from collections import defaultdict, deque

events = [
    {"symbol": "AAPL", "price": 100},
    {"symbol": "MSFT", "price": 200},
    {"symbol": "AAPL", "price": 101},
    {"symbol": "AAPL", "price": 102},
    {"symbol": "MSFT", "price": 202},
]

window = 2
buffers = defaultdict(deque)
sums = defaultdict(float)
features = []

for event in events:
    symbol = event["symbol"]
    price = event["price"]
    buffer = buffers[symbol]

    buffer.append(price)
    sums[symbol] += price

    if len(buffer) > window:
        sums[symbol] -= buffer.popleft()

    if len(buffer) == window:
        features.append((symbol, sums[symbol] / window))

print(features)
```

结果：

```text
[('AAPL', 100.5), ('AAPL', 101.5), ('MSFT', 201.0)]
```

这就是 keyed window state。

状态数量大约是：

```text
key 数量 * window 大小
```

所以 key 很多时，要注意内存。

## 时间窗口

另一种常见窗口按时间长度定义。

例如：

```text
最近 3 秒内的事件
```

可以用 deque 保存 `(timestamp, value)`。

```python
from collections import deque

events = [
    (1, 100),
    (2, 101),
    (4, 103),
    (6, 107),
]

window_seconds = 3
buffer = deque()
running_sum = 0
means = []

for timestamp, price in events:
    buffer.append((timestamp, price))
    running_sum += price

    while buffer and buffer[0][0] < timestamp - window_seconds:
        _, old_price = buffer.popleft()
        running_sum -= old_price

    means.append(running_sum / len(buffer))

print(means)
```

结果：

```text
[100.0, 100.5, 101.33333333333333, 105.0]
```

在 `timestamp = 6` 时，窗口保留时间戳 `3` 到 `6` 的事件。

所以 `(1, 100)` 和 `(2, 101)` 都被移除，只剩 `(4, 103)` 和 `(6, 107)`。

## tumbling window 和 sliding window

tumbling window 是不重叠窗口。

例如每 5 秒一个窗口：

```text
[0,5), [5,10), [10,15)
```

sliding window 是滑动窗口。

例如长度 5 秒，每 1 秒滑动一次：

```text
[0,5), [1,6), [2,7)
```

简单 tumbling count：

```python
from collections import defaultdict

events = [
    {"event_time": 1, "symbol": "AAPL"},
    {"event_time": 2, "symbol": "MSFT"},
    {"event_time": 6, "symbol": "AAPL"},
    {"event_time": 7, "symbol": "AAPL"},
]

window_size = 5
counts = defaultdict(int)

for event in events:
    window_start = (event["event_time"] // window_size) * window_size
    key = (window_start, event["symbol"])
    counts[key] += 1

print(dict(counts))
```

结果：

```text
{(0, 'AAPL'): 1, (0, 'MSFT'): 1, (5, 'AAPL'): 2}
```

## 乱序事件

流里事件不一定按 `event_time` 到达。

例如：

```python
events = [
    {"event_id": "e1", "event_time": 10, "arrival_time": 10},
    {"event_id": "e2", "event_time": 12, "arrival_time": 12},
    {"event_id": "e3", "event_time": 11, "arrival_time": 13},
]
```

`e3` 的事件时间是 11，但到达时间是 13。

如果直接按到达顺序处理，时间序列计算可能错。

解决思路：

```text
允许一定延迟
先缓存事件
等 watermark 推进后，再输出确定不会被更早事件改变的结果
```

## watermark

watermark 是流式系统里判断“可以关闭某些时间窗口”的机制。

简单理解：

```text
watermark = 当前见过的最大 event_time - 允许迟到时间
```

如果一个窗口的结束时间小于等于 watermark，就认为这个窗口可以输出。

## 简单 watermark 聚合

下面例子计算 5 秒 tumbling window 的事件数。

允许迟到 4 秒。

```python
from collections import defaultdict

events = [
    {"event_id": "e1", "event_time": 1, "symbol": "AAPL"},
    {"event_id": "e2", "event_time": 6, "symbol": "AAPL"},
    {"event_id": "e3", "event_time": 2, "symbol": "AAPL"},
    {"event_id": "e4", "event_time": 9, "symbol": "MSFT"},
]

window_size = 5
allowed_lateness = 4
max_event_time = float("-inf")
counts = defaultdict(int)
emitted = []

for event in events:
    event_time = event["event_time"]
    max_event_time = max(max_event_time, event_time)
    watermark = max_event_time - allowed_lateness

    window_start = (event_time // window_size) * window_size
    window_end = window_start + window_size
    counts[(window_start, window_end, event["symbol"])] += 1

    ready = [
        key for key in counts
        if key[1] <= watermark
    ]

    for key in sorted(ready):
        emitted.append((key, counts.pop(key)))

print(emitted)
print(dict(counts))
```

结果：

```text
[((0, 5, 'AAPL'), 2)]
{(5, 10, 'AAPL'): 1, (5, 10, 'MSFT'): 1}
```

解释：

- 见到 `event_time = 6` 后，watermark 变成 2。
- `event_time = 2` 的迟到事件仍然可以进入窗口 `[0,5)`。
- 见到 `event_time = 9` 后，watermark 变成 5，窗口 `[0,5)` 可以输出。

真实系统要明确 late event 策略。

## late event 策略

late event 是迟到事件。

如果某个事件到达时，它所属窗口已经输出，常见处理方式有：

- 丢弃。
- 发送修正结果。
- 写入旁路日志。
- 触发重算。
- 允许窗口在 grace period 内更新。

没有统一正确答案。

关键是：

```text
策略必须明确，并且研究、回测、生产保持一致
```

## 去重

流式数据可能重复到达。

如果重复事件被累计两次，成交量、金额、风险指标都会错。

简单去重可以维护 seen id。

```python
events = [
    {"event_id": "e1", "size": 100},
    {"event_id": "e2", "size": 50},
    {"event_id": "e1", "size": 100},
]

seen = set()
total_size = 0

for event in events:
    if event["event_id"] in seen:
        continue

    seen.add(event["event_id"])
    total_size += event["size"]

print(total_size)
```

结果：

```text
150
```

如果数据流很长，`seen` 不能无限增长。

常见办法：

- 按时间清理 seen。
- 用 TTL。
- 用布隆过滤器。
- 只在最近窗口内去重。

## 幂等性

idempotent 是幂等。

意思是：

```text
同一个事件处理一次和处理多次，最终状态一样
```

例如，用 event_id 覆盖状态通常比直接累加更容易幂等。

非幂等：

```python
position = 0
fill = {"event_id": "f1", "qty": 100}

position += fill["qty"]
position += fill["qty"]

print(position)
```

结果：

```text
200
```

幂等版本：

```python
fills = {}

for fill in [
    {"event_id": "f1", "qty": 100},
    {"event_id": "f1", "qty": 100},
]:
    fills[fill["event_id"]] = fill["qty"]

position = sum(fills.values())
print(position)
```

结果：

```text
100
```

流式系统常常需要重放事件。

幂等设计可以降低重复处理带来的风险。

## checkpoint

checkpoint 是状态快照。

流式处理可能运行很久，如果进程崩溃，需要从某个位置恢复。

最小 checkpoint 通常包含：

```text
已处理到的 offset / sequence
当前状态
去重状态或必要的 seen 范围
窗口状态
```

简单示例：

```python
events = [
    {"seq": 1, "size": 100},
    {"seq": 2, "size": 50},
    {"seq": 3, "size": 20},
]

state = {"last_seq": 0, "total_size": 0}

for event in events:
    if event["seq"] <= state["last_seq"]:
        continue

    state["total_size"] += event["size"]
    state["last_seq"] = event["seq"]

checkpoint = state.copy()

print(checkpoint)
```

结果：

```text
{'last_seq': 3, 'total_size': 170}
```

恢复时，从 `last_seq` 后面的事件继续处理。

## 背压 backpressure

backpressure 是背压。

如果事件到达速度大于处理速度，队列会越积越长。

表现可能是：

- 延迟升高。
- 内存增长。
- 丢包。
- 下游超时。
- 状态落后于真实市场。

处理方式包括：

- 降低输入频率。
- 批量处理。
- 丢弃低价值事件。
- 扩容消费者。
- 优化状态更新。
- 对 key 做分区并行。

这是系统设计问题，但和数据结构选择有关。

例如，`list.pop(0)` 会让队列处理变慢，`deque.popleft()` 更合适。

## 小例子：在线价格特征处理器

下面做一个简化版处理器：

```text
按 symbol 维护最近 window 个价格
输出滚动均值
按 event_id 去重
```

```python
from collections import defaultdict, deque

class PriceFeatureProcessor:
    def __init__(self, window):
        self.window = window
        self.buffers = defaultdict(deque)
        self.sums = defaultdict(float)
        self.seen = set()

    def process(self, event):
        event_id = event["event_id"]
        if event_id in self.seen:
            return None

        self.seen.add(event_id)

        symbol = event["symbol"]
        price = event["price"]
        buffer = self.buffers[symbol]

        buffer.append(price)
        self.sums[symbol] += price

        if len(buffer) > self.window:
            self.sums[symbol] -= buffer.popleft()

        if len(buffer) < self.window:
            return None

        return {
            "symbol": symbol,
            "event_time": event["event_time"],
            "mean_price": self.sums[symbol] / self.window,
        }


processor = PriceFeatureProcessor(window=2)

events = [
    {"event_id": "e1", "event_time": 1, "symbol": "AAPL", "price": 100},
    {"event_id": "e2", "event_time": 2, "symbol": "AAPL", "price": 102},
    {"event_id": "e2", "event_time": 2, "symbol": "AAPL", "price": 102},
    {"event_id": "e3", "event_time": 3, "symbol": "AAPL", "price": 104},
]

outputs = []

for event in events:
    output = processor.process(event)
    if output is not None:
        outputs.append(output)

print(outputs)
```

结果：

```text
[{'symbol': 'AAPL', 'event_time': 2, 'mean_price': 101.0}, {'symbol': 'AAPL', 'event_time': 3, 'mean_price': 103.0}]
```

重复的 `e2` 没有被处理第二次。

## 增量计算和重算

流式处理倾向于增量计算：

```text
旧状态 + 新事件 -> 新状态
```

例如 running sum：

```text
sum_new = sum_old + x_new - x_expired
```

而不是每次重扫整个窗口。

但增量计算有代价：

- 状态更复杂。
- 错误更难排查。
- 乱序事件可能破坏假设。
- 需要 checkpoint 和恢复逻辑。

因此在研究阶段，可以先用批处理或简单重算确认逻辑。

生产阶段再优化成增量流式实现。

## 流处理中的常见错误

### 错误 1：把 arrival_time 当 event_time

行情或日志可能延迟到达。

如果应该按事件发生时间计算，却用到达时间排序，窗口统计可能错。

### 错误 2：状态无限增长

常见无限增长状态：

- `seen` 集合。
- 按 key 的 buffer。
- 尚未关闭的窗口。
- 每个账户或股票的中间状态。

需要 TTL、窗口清理或状态压缩。

### 错误 3：重复事件导致重复累计

累加类指标最怕重复事件。

如果没有 event_id 去重，成交量和 notional 会被放大。

### 错误 4：乱序事件没有策略

如果事件可能乱序，就要明确：

- 等多久。
- 何时输出。
- late event 如何处理。
- 输出是否允许修正。

### 错误 5：回测和实盘语义不一致

回测中如果假设数据完美有序、没有延迟、没有重复，而实盘有这些问题，策略表现会偏离。

至少要在关键特征上明确：

```text
信号在什么时候可用？
使用的是 event_time 还是 arrival_time？
当前事件是否能用于当前决策？
```

## 什么时候用流式处理

适合流式处理的场景：

- 数据持续到达。
- 需要低延迟输出。
- 不能等全量数据到齐。
- 状态可以增量维护。
- 需要在线监控、风控或信号。

不一定要流式处理的场景：

- 离线研究。
- 报表统计。
- 小数据量分析。
- 需要全局排序或全局优化。
- 迟到数据很多且修正成本很高。

## 记忆要点

- 流式处理是逐事件更新状态。
- keyed state 按 symbol、账户等 key 维护状态。
- 窗口可以按条数，也可以按时间。
- `deque` 适合维护最近窗口。
- running sum 是典型增量计算。
- event_time 和 arrival_time 要区分。
- watermark 用来决定窗口何时可以输出。
- late event 策略必须明确。
- 去重和幂等性对可靠流处理很重要。
- 状态需要 checkpoint，也需要清理策略。

## 自测题

1. stream processing 和 batch processing 的区别是什么？
2. 什么是 keyed state？为什么多股票流里需要它？
3. event_time 和 arrival_time 有什么区别？
4. watermark 的作用是什么？
5. 为什么流式系统要考虑去重、幂等性和 checkpoint？
