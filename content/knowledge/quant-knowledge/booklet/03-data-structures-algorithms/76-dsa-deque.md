# 76. 数据结构与算法：deque 的双端队列语义、滑动窗口和流式处理应用

## 核心概念

deque 是 double-ended queue，双端队列。

Python 标准库提供：

```python
from collections import deque
```

它支持在两端高效插入和删除：

```text
append      右端插入
appendleft  左端插入
pop         右端弹出
popleft     左端弹出
```

这些操作的时间复杂度通常是：

```text
O(1)
```

相比之下，Python list 在左端插入或弹出通常是 `O(n)`，因为后面的元素要整体移动。

## deque 回答的问题

deque 适合处理：

- FIFO 队列。
- 双端队列。
- 固定长度最近窗口。
- 滑动窗口统计。
- 单调队列。
- BFS 图遍历。
- 流式数据缓冲。
- 事件队列的简单先进先出处理。

在量化和数据处理中，deque 常用于：

```text
保存最近 N 个 tick
维护滑动窗口最大值
保存待处理事件
做 order book 或行情流的短窗口缓存
```

## 基础操作

```python
from collections import deque

q = deque()

q.append("trade_1")
q.append("trade_2")
q.appendleft("open")

print(list(q))
print(q.popleft())
print(q.pop())
print(list(q))
```

执行顺序：

```text
append      -> 右端加入
appendleft  -> 左端加入
popleft     -> 左端取出
pop         -> 右端取出
```

如果你只需要 FIFO 队列，常用：

```python
queue = deque()
queue.append(item)
item = queue.popleft()
```

## 为什么不用 list 做队列

list 的右端操作很快：

```python
items.append(x)
items.pop()
```

但左端弹出：

```python
items.pop(0)
```

通常是 `O(n)`，因为所有剩余元素都要向前移动。

deque 的 `popleft()` 是 `O(1)`。

所以：

```text
栈：list 可以
队列：deque 更合适
```

## 固定长度缓冲 maxlen

`deque(maxlen=N)` 可以保存最近 N 个元素。

```python
last3 = deque(maxlen=3)

for x in [10, 20, 30, 40, 50]:
    last3.append(x)

print(list(last3))
```

结果：

```text
[30, 40, 50]
```

当超过 `maxlen` 时，最旧元素会自动被丢弃。

这适合流式场景：

- 最近 100 个 tick。
- 最近 20 个收益。
- 最近 N 个订单事件。
- 最近 N 次延迟观测。

## 滑动窗口均值

用 deque 维护最近 `window` 个值，并维护 running sum。

```python
values = [2, 4, 6, 8, 10]
window = 3

buffer = deque()
running_sum = 0
means = []

for x in values:
    buffer.append(x)
    running_sum += x

    if len(buffer) > window:
        running_sum -= buffer.popleft()

    if len(buffer) == window:
        means.append(running_sum / window)

print(means)
```

结果：

```text
[4.0, 6.0, 8.0]
```

这种写法每个元素进队一次、出队一次，整体是 `O(n)`。

如果每个窗口都重新求和，复杂度会是 `O(n * window)`。

## 单调队列：滑动窗口最大值

问题：

```text
给定 prices 和窗口长度 window，求每个窗口的最大值。
```

暴力做法每个窗口扫描一次，复杂度 `O(n * window)`。

单调队列可以做到 `O(n)`。

```python
prices = [101, 99, 103, 102, 105, 98, 104]
window = 3

mono = deque()
rolling_max = []

for i, price in enumerate(prices):
    while mono and mono[0][0] <= i - window:
        mono.popleft()

    while mono and mono[-1][1] <= price:
        mono.pop()

    mono.append((i, price))

    if i >= window - 1:
        rolling_max.append(mono[0][1])

print(rolling_max)
```

核心不变量：

```text
队列中价格从左到右单调递减
队首永远是当前窗口最大值
```

每个元素最多进队一次、出队一次，所以整体 `O(n)`。

## FIFO 事件队列

简单事件处理可以用 deque：

```python
event_queue = deque(["open", "quote", "trade"])

processed = []

while event_queue:
    event = event_queue.popleft()
    processed.append(event)

print(processed)
```

如果事件只需要先进先出，deque 足够。

如果事件需要按时间戳或优先级排序，应使用 heap。

区别：

```text
deque: 谁先来先处理
heap: 谁优先级最高先处理
```

## BFS 中的 deque

BFS 广度优先搜索也常用 deque。

伪代码：

```text
queue = deque([start])
visited = set([start])

while queue:
    node = queue.popleft()

    for next_node in graph[node]:
        if next_node not in visited:
            visited.add(next_node)
            queue.append(next_node)
```

原因：

- BFS 需要 FIFO。
- `popleft()` 必须高效。
- list 的 `pop(0)` 会拖慢大图遍历。

## deque 和 heap 的区别

deque 维护的是顺序：

```text
先进入的先出去，或者从两端操作
```

heap 维护的是优先级：

```text
最小或最大优先级先出去
```

例子：

- 订单按到达顺序处理：deque。
- 订单按价格优先处理：heap 或更专门的 order book 结构。
- 最近 N 个价格缓存：deque。
- 当前 top-k 分数：heap。

## 常见坑

第一，用 list 的 `pop(0)` 做队列。

小数据没问题，大数据会慢。用 deque 的 `popleft()`。

第二，在 deque 中间频繁随机访问。

deque 适合两端操作，不适合大量中间随机访问。需要随机访问时用 list。

第三，误以为 `maxlen` 会报错。

超过 `maxlen` 时旧元素会自动丢弃，不会报错。

第四，单调队列忘记删除过期元素。

窗口滑动时，队首元素可能已经不在窗口内，必须先清理。

第五，单调队列比较方向写反。

求最大值时，队列保持递减；求最小值时，队列保持递增。

## 实战提示

使用 deque 时可以按下面判断：

1. 是否需要从左端高效弹出？
2. 是否需要保存最近 N 个元素？
3. 是否是 FIFO 队列？
4. 是否是滑动窗口问题？
5. 是否能用单调队列把窗口最值降到 `O(n)`？
6. 是否需要按优先级处理？如果是，用 heap。

在量化流式处理中，deque 特别适合处理“最近窗口”：

```text
最近 60 秒成交量
最近 100 个 tick 的最大价差
最近 N 个延迟样本的均值
```

## 小结

本节的重点：

- deque 是双端队列。
- `append`、`appendleft`、`pop`、`popleft` 通常是 `O(1)`。
- FIFO 队列应优先用 deque，而不是 list 的 `pop(0)`。
- `maxlen` 可以实现固定长度最近窗口。
- 滑动窗口均值可以用 deque + running sum。
- 单调队列可以用 `O(n)` 求滑动窗口最大值或最小值。
- deque 管顺序，heap 管优先级。

## 自检问题

1. deque 和 list 在左端弹出上的复杂度有什么区别？
2. `deque(maxlen=3)` 超过长度后会发生什么？
3. 如何用 deque 和 running sum 计算滑动窗口均值？
4. 单调队列求滑动窗口最大值时，队列应保持什么顺序？
5. FIFO 事件队列和优先级事件队列分别适合用什么结构？
6. 为什么 BFS 常用 deque？
