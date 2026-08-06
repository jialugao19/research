# 数据结构与算法：heap 的优先队列语义、top-k 与事件调度应用

## 核心概念

heap 堆是一种支持快速取出最小值或最大值的数据结构。

Python 标准库提供：

```python
import heapq
```

`heapq` 实现的是最小堆：

```text
heap[0] 永远是当前最小元素
```

常见操作复杂度：

```text
heapify: O(n)
heappush: O(log n)
heappop: O(log n)
peek heap[0]: O(1)
```

heap 的核心用途是优先队列：每次都处理当前优先级最高的任务。

## heap 回答的问题

heap 适合处理：

- 动态 top-k。
- 按优先级处理任务。
- 事件驱动模拟。
- 多路有序流合并。
- Dijkstra 最短路。
- 滚动窗口中位数的一部分。
- 订单簿或撮合系统中的价格优先队列。

如果你需要“不断插入元素，同时频繁取当前最小或最大”，heap 往往比反复排序更合适。

## 最小堆基础

```python
import heapq

latencies = [23, 5, 17, 9, 31, 12]

heap = latencies[:]
heapq.heapify(heap)

print(heap[0])
```

`heap[0]` 是最小元素，但整个列表不一定完全有序。

依次弹出：

```python
ordered = []

while heap:
    ordered.append(heapq.heappop(heap))

print(ordered)
```

结果会是升序。

注意：如果只想排序一次，直接 `sorted()` 更清楚。heap 的优势在于动态插入和动态取最小。

## heappush 和 heappop

```python
heap = []

for x in [10, 4, 7, 1]:
    heapq.heappush(heap, x)

print(heapq.heappop(heap))
print(heapq.heappop(heap))
```

每次 `heappop` 都返回当前最小元素。

堆内部只维护局部有序关系，不保证列表整体排序。

不要写：

```python
heap.sort()
```

这会破坏你使用 heap 的意义。需要有序输出时，用反复 `heappop` 或 `sorted(heap)`。

## 最大堆模拟

`heapq` 是最小堆。如果需要最大堆，可以把优先级取负：

```python
scores = [
    (0.12, "AAPL"),
    (0.08, "MSFT"),
    (0.31, "NVDA"),
    (0.05, "TSLA"),
    (0.22, "META"),
]

max_heap = []

for score, symbol in scores:
    heapq.heappush(max_heap, (-score, symbol))

best_score_neg, best_symbol = heapq.heappop(max_heap)

print(best_symbol)
print(-best_score_neg)
```

这种写法常用于：

- 最高分优先。
- 最大收益优先。
- 最大价格优先。
- 最大优先级任务先处理。

## top-k：保留最大的 k 个元素

如果数据流很长，只想保留最大的 `k` 个元素，可以维护大小为 `k` 的最小堆。

```python
k = 3
top_k = []

for score, symbol in scores:
    heapq.heappush(top_k, (score, symbol))

    if len(top_k) > k:
        heapq.heappop(top_k)

top_k_sorted = sorted(top_k, reverse=True)

print(top_k_sorted)
```

逻辑：

- 堆里保留当前最大的 `k` 个元素。
- 堆顶是这 `k` 个元素里最小的。
- 新元素进来后，如果堆超过 `k`，弹掉最小的。

复杂度：

```text
O(n log k)
```

如果 `k` 远小于 `n`，比全量排序 `O(n log n)` 更合适。

量化例子：

```text
从每天几千只股票中保留因子分数最高的 100 只
从海量 tick 中保留最大成交额的 k 笔
从日志中保留延迟最高的 k 次请求
```

## nlargest 和 nsmallest

Python 也提供便捷函数：

```python
largest_three = heapq.nlargest(3, scores)
smallest_three = heapq.nsmallest(3, scores)

print(largest_three)
print(smallest_three)
```

对于一次性 top-k，这两个函数很方便。

如果是流式数据，需要边来边维护，手写固定大小 heap 更灵活。

## 事件调度优先队列

事件驱动回测或仿真中，事件通常按时间戳处理。

用 heap 做事件队列：

```python
events = []
seq = 0

for timestamp, event_type in [
    (3, "quote"),
    (1, "open"),
    (3, "trade"),
    (2, "signal"),
]:
    heapq.heappush(events, (timestamp, seq, event_type))
    seq += 1

popped = []

while events:
    popped.append(heapq.heappop(events))

print(popped)
```

这里 key 是：

```text
(timestamp, seq, event)
```

含义：

- 先按 `timestamp` 排序。
- 时间相同，用 `seq` 保持插入顺序。
- `event` 是实际内容。

为什么需要 `seq`？

如果两个事件时间相同，而事件对象本身不能比较，heap 会尝试比较事件对象并报错。加一个递增序号可以避免这个问题，也能让处理顺序稳定。

## 多路有序流合并

多个数据源各自有序，可以用 `heapq.merge` 合并。

```python
stream_a = [(1, "A"), (4, "A"), (7, "A")]
stream_b = [(2, "B"), (3, "B"), (8, "B")]

merged = list(heapq.merge(stream_a, stream_b))

print(merged)
```

它适合：

- 合并多个交易所行情流。
- 合并多个 symbol 的时间序列事件。
- 合并分片排序后的日志。

`heapq.merge` 是惰性的，可以边读取边输出，不必一次把所有数据放进内存。

## heap 和排序的区别

排序适合：

```text
一次性拿到所有数据，然后需要完整有序结果
```

heap 适合：

```text
数据动态到达，只需要当前最小、最大或 top-k
```

对比：

```text
全排序 top-k: O(n log n)
heap top-k: O(n log k)
```

如果 `k` 很小，heap 更高效。

如果最终需要完整排序，直接排序通常更简单。

## 常见坑

第一，以为 heap 列表整体有序。

`heap[0]` 是最小值，但 `heap[1:]` 不保证有序。

第二，忘记 Python `heapq` 是最小堆。

最大堆通常用负数优先级模拟。

第三，优先级相同且对象不可比较。

用 `(priority, seq, item)`，不要只用 `(priority, item)`。

第四，修改 heap 中元素后不重建。

如果你直接改了堆中某个元素的优先级，堆结构不会自动修复。需要重新 `heapify`，或采用 lazy deletion。

第五，top-k 时堆大小没有限制。

如果把所有元素都 push 进去，内存和复杂度就接近全排序了。

## 实战提示

使用 heap 时可以按下面判断：

1. 是否需要频繁取最小或最大？
2. 数据是否动态到达？
3. 是否只需要 top-k，而不是完整排序？
4. 优先级是否可能相同？
5. 是否需要稳定顺序？
6. 是否存在更新或删除已有任务的需求？

如果需要更新已有任务优先级，可以考虑：

```text
新增一条新优先级记录
旧记录标记为无效
弹出时跳过无效记录
```

这叫 lazy deletion，很多调度器都会用这种方式。

## 小结

本节的重点：

- heap 是优先队列的常用实现。
- Python `heapq` 是最小堆。
- `heappush` 和 `heappop` 是 `O(log n)`。
- `heap[0]` 是当前最小元素，但堆列表整体不保证有序。
- 最大堆可以用负优先级模拟。
- 固定大小 heap 可以用 `O(n log k)` 维护 top-k。
- 事件调度中常用 `(timestamp, seq, event)` 保证稳定处理顺序。

## 自检问题

1. Python `heapq` 默认是最小堆还是最大堆？
2. 为什么 `heap[0]` 是最小值，但整个 heap 列表不一定有序？
3. 如何用最小堆维护最大的 k 个元素？
4. 为什么事件队列常用 `(timestamp, seq, event)`？
5. heap top-k 和全排序 top-k 的复杂度有什么区别？
6. 如果 heap 中任务优先级需要更新，为什么不能直接改列表里的元素？
