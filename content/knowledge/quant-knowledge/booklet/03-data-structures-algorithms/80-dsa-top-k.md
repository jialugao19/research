# 80. 数据结构与算法：top-k 的排序、堆、分区选择和流式应用

## 核心概念

top-k 问题是：

```text
从 n 个元素中找出最大的 k 个，或最小的 k 个。
```

例如：

```text
从全市场股票里找因子分最高的前 100 个
从日志里找延迟最高的前 10 条请求
从订单里找金额最大的前 20 笔
从特征里找重要性最高的前 k 个
```

top-k 的关键问题不是“能不能找到”，而是：

```text
是否需要完整排序？
数据是一次性给定，还是持续流入？
top-k 内部是否需要有序？
相同分数时如何 tie-break？
k 相对 n 是大还是小？
```

这些问题会决定你用排序、heap，还是分区选择。

## 三种常见方案

常见 top-k 方案：

```text
完整排序：      O(n log n)
固定大小 heap： O(n log k)
快速选择：      平均 O(n)，之后可选 O(k log k) 排序 top-k
```

简化判断：

```text
数据量小：直接排序
k 很小：固定大小 heap
只要集合不要求有序：快速选择
数据流式到达：固定大小 heap
需要完整排名：排序
```

## 用排序做 top-k

最直接的方法是完整排序后切片。

```python
records = [
    {"symbol": "AAPL", "score": 0.12, "volume": 1000},
    {"symbol": "MSFT", "score": 0.31, "volume": 800},
    {"symbol": "NVDA", "score": 0.31, "volume": 1200},
    {"symbol": "TSLA", "score": 0.05, "volume": 1500},
    {"symbol": "META", "score": 0.22, "volume": 900},
]

top3 = sorted(records, key=lambda r: r["score"], reverse=True)[:3]

print([r["symbol"] for r in top3])
```

结果：

```text
['MSFT', 'NVDA', 'META']
```

这种写法优点明显：

- 简单。
- 可读。
- top-k 内部天然有序。
- 容易加多字段排序规则。

缺点是做了完整排序。

如果 `n` 很大、`k` 很小，完整排序可能浪费。

## 明确 tie-breaker

如果多个元素的 score 相同，只按 score 排序会保留原始输入顺序。

为了让结果可复现，应该明确 tie-breaker。

例如：

```text
score 降序
volume 降序
symbol 升序
```

```python
top3 = sorted(
    records,
    key=lambda r: (-r["score"], -r["volume"], r["symbol"]),
)[:3]

print([r["symbol"] for r in top3])
```

结果：

```text
['NVDA', 'MSFT', 'META']
```

`NVDA` 和 `MSFT` 的 score 相同。

因为 `NVDA` 的 volume 更大，所以排在前面。

在交易系统或研究报告里，top-k 最好总是可复现。

## heapq.nlargest / nsmallest

Python 标准库提供：

```python
heapq.nlargest(k, iterable, key=...)
heapq.nsmallest(k, iterable, key=...)
```

例子：

```python
import heapq

largest3 = heapq.nlargest(3, records, key=lambda r: r["score"])

print([r["symbol"] for r in largest3])
```

结果：

```text
['MSFT', 'NVDA', 'META']
```

`nlargest` 适合一次性取 top-k。

它比手写 heap 更简洁。

但要注意：

```text
如果需要复杂的多字段 tie-breaker，排序的 tuple key 往往更直观。
```

也可以把 key 写成 tuple：

```python
largest3 = heapq.nlargest(
    3,
    records,
    key=lambda r: (r["score"], r["volume"], -ord(r["symbol"][0])),
)
```

这只是演示 tuple key。

实际业务里，不要用这种粗糙的 `ord` 写法处理完整字符串 tie-breaker。

如果需要 `score` 降序、`volume` 降序、`symbol` 升序，完整排序更清楚。

## 固定大小最小堆

如果要维护最大的 k 个元素，可以用大小为 k 的最小堆。

堆顶是当前 top-k 里最小的那个。

新元素进来时：

```text
如果堆没满：直接放入
如果新元素 <= 堆顶：丢弃
如果新元素 > 堆顶：替换堆顶
```

例子：

```python
import heapq

scores = [
    (0.12, "AAPL"),
    (0.31, "MSFT"),
    (0.31, "NVDA"),
    (0.05, "TSLA"),
    (0.22, "META"),
]

k = 3
heap = []

for score, symbol in scores:
    item = (score, symbol)

    if len(heap) < k:
        heapq.heappush(heap, item)
    elif item > heap[0]:
        heapq.heapreplace(heap, item)

top_k = sorted(heap, reverse=True)

print(top_k)
```

一种结果：

```text
[(0.31, 'NVDA'), (0.31, 'MSFT'), (0.22, 'META')]
```

这里 tuple 比较规则是：

```text
先比较 score
score 相同再比较 symbol
```

所以 `NVDA` 排在 `MSFT` 前面。

## 固定大小堆的复杂度

固定大小堆每个元素最多做一次 `O(log k)` 操作。

总复杂度：

```text
O(n log k)
```

空间复杂度：

```text
O(k)
```

当 `k` 远小于 `n` 时，这比完整排序更省。

例如：

```text
n = 1,000,000
k = 100
```

完整排序会比较和移动全体元素。

固定大小堆只维护 100 个候选。

## 流式 top-k

固定大小堆最适合流式数据。

例如，订单一笔笔到达，要随时维护金额最大的 3 笔。

```python
import heapq

orders = [
    {"order_id": "o1", "notional": 1200},
    {"order_id": "o2", "notional": 5000},
    {"order_id": "o3", "notional": 800},
    {"order_id": "o4", "notional": 7000},
    {"order_id": "o5", "notional": 3000},
]

heap = []
k = 3

for order in orders:
    item = (order["notional"], order["order_id"])

    if len(heap) < k:
        heapq.heappush(heap, item)
    elif item > heap[0]:
        heapq.heapreplace(heap, item)

current_top = sorted(heap, reverse=True)

print(current_top)
```

结果：

```text
[(7000, 'o4'), (5000, 'o2'), (3000, 'o5')]
```

这个结构可以持续更新。

如果每来一笔订单都完整排序全部历史订单，成本会越来越高。

## 最小的 k 个

如果要找最小的 k 个，可以：

- 用 `heapq.nsmallest`。
- 用大小为 k 的最大堆。

Python 没有内置最大堆接口，所以常用负数模拟。

```python
import heapq

latencies = [23, 5, 17, 9, 31, 12]
k = 3
heap = []

for latency in latencies:
    item = -latency

    if len(heap) < k:
        heapq.heappush(heap, item)
    elif item > heap[0]:
        heapq.heapreplace(heap, item)

smallest = sorted([-x for x in heap])

print(smallest)
```

结果：

```text
[5, 9, 12]
```

逻辑是：

```text
heap 存负数
堆顶对应当前保留集合里最大的原始 latency
新 latency 更小，才替换掉当前最大者
```

日常代码中，一次性数据直接用 `heapq.nsmallest(k, latencies)` 更清楚。

## 快速选择 quickselect

quickselect 是快速排序思想的选择算法。

它通过 partition 找第 k 大或第 k 小的位置。

平均复杂度：

```text
O(n)
```

最坏复杂度：

```text
O(n^2)
```

但随机选 pivot 时，平均表现通常很好。

如果只需要 top-k 集合，不要求内部有序，quickselect 很合适。

## 一个简单 quickselect 例子

下面用 quickselect 找最大的 k 个数。

为了让示例可复现，pivot 直接取中间位置。

```python
def top_k_quickselect(nums, k):
    if k <= 0:
        return []
    if k >= len(nums):
        return nums[:]

    target = k - 1
    arr = nums[:]
    left = 0
    right = len(arr) - 1

    while left <= right:
        pivot = arr[(left + right) // 2]
        i = left
        j = right

        while i <= j:
            while arr[i] > pivot:
                i += 1
            while arr[j] < pivot:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1

        if target <= j:
            right = j
        elif target >= i:
            left = i
        else:
            break

    return arr[:k]


nums = [7, 1, 9, 3, 8, 2]
print(sorted(top_k_quickselect(nums, 3), reverse=True))
```

结果：

```text
[9, 8, 7]
```

注意：

```text
quickselect 返回的前 k 个不一定内部有序
```

如果需要有序 top-k，要对结果再排序：

```python
top_k_sorted = sorted(top_k_quickselect(nums, 3), reverse=True)
```

## 分组 top-k

量化里经常不是“全样本 top-k”，而是“每个交易日截面 top-k”。

示例数据：

```python
rows = [
    ("2026-01-02", "AAPL", 0.12),
    ("2026-01-02", "MSFT", 0.31),
    ("2026-01-02", "NVDA", 0.28),
    ("2026-01-03", "AAPL", 0.18),
    ("2026-01-03", "MSFT", 0.10),
    ("2026-01-03", "NVDA", 0.35),
]
```

目标：

```text
每一天选 score 最高的前 2 只股票
```

可以按日期分桶，然后每组排序。

```python
from collections import defaultdict

groups = defaultdict(list)

for date, symbol, score in rows:
    groups[date].append((symbol, score))

selected = {}

for date, items in groups.items():
    selected[date] = sorted(items, key=lambda x: (-x[1], x[0]))[:2]

print(selected)
```

结果：

```text
{'2026-01-02': [('MSFT', 0.31), ('NVDA', 0.28)], '2026-01-03': [('NVDA', 0.35), ('AAPL', 0.18)]}
```

不要把所有日期混在一起取 top-k。

那会得到全样本最高分，而不是每日截面组合。

## 用 heap 做每组 top-k

如果每组很大，也可以给每个组维护一个固定大小堆。

```python
from collections import defaultdict
import heapq

k = 2
group_heaps = defaultdict(list)

for date, symbol, score in rows:
    heap = group_heaps[date]
    item = (score, symbol)

    if len(heap) < k:
        heapq.heappush(heap, item)
    elif item > heap[0]:
        heapq.heapreplace(heap, item)

selected = {
    date: sorted(heap, reverse=True)
    for date, heap in group_heaps.items()
}

print(selected)
```

结果：

```text
{'2026-01-02': [(0.31, 'MSFT'), (0.28, 'NVDA')], '2026-01-03': [(0.35, 'NVDA'), (0.18, 'AAPL')]}
```

这种写法适合：

- 数据流按行到达。
- 不能一次把所有组完整放入内存。
- 每组只保留少量候选。

## top-k 与排序方向

top-k 经常因为方向写错出问题。

常见约定：

```text
score 越高越好 -> largest k
cost 越低越好  -> smallest k
rank 越小越好  -> smallest k
latency 越高越异常 -> largest k
```

写代码前先明确指标方向。

例如因子分选股：

```python
long_candidates = heapq.nlargest(2, records, key=lambda r: r["score"])
short_candidates = heapq.nsmallest(2, records, key=lambda r: r["score"])

print([r["symbol"] for r in long_candidates])
print([r["symbol"] for r in short_candidates])
```

结果：

```text
['MSFT', 'NVDA']
['TSLA', 'AAPL']
```

这里 long 选高分，short 选低分。

真实策略中要确认因子方向和收益预期一致。

## top-k 内部是否需要排序

有些任务只需要知道集合：

```text
哪些股票进入候选池
```

这时内部顺序不重要。

有些任务需要完整顺序：

```text
按分数分配权重
按排名输出报告
展示 top 10 列表
```

这时 top-k 内部必须有序。

heap 维护出来的内部列表不是完整有序的。

如果要输出有序结果，最后加：

```python
result = sorted(heap, reverse=True)
```

## pandas 中的 top-k

pandas 常用：

```python
df.nlargest(k, "score")
df.nsmallest(k, "score")
```

分组 top-k 常见写法：

```python
selected = (
    df.sort_values(["date", "score"], ascending=[True, False])
      .groupby("date")
      .head(k)
)
```

或者在每组内用 rank：

```python
rank = df.groupby("date")["score"].rank(ascending=False, method="first")
selected = df[rank <= k]
```

需要注意：

```text
method="first" 会让相同分数按原始顺序打破平局
```

如果原始顺序没有业务含义，应该先定义清楚 tie-breaker。

## 常见错误

### 错误 1：为 top-k 做完整排序但 n 很大

完整排序简单，但不总是合适。

如果只要前 100 个，而数据有几千万条，固定大小 heap 或分区选择可能更合适。

### 错误 2：忘记 top-k 内部是否有序

heap 的内部数组不是排序结果。

错误理解：

```python
heap[0:k]
```

不是有序 top-k。

要输出排名，必须排序 heap 里的候选。

### 错误 3：tie-breaker 不稳定

同分股票很多时，如果没有 tie-breaker，结果可能依赖输入顺序。

研究中这会影响复现。

生产中这会影响日志、报告和下单列表一致性。

### 错误 4：把全样本 top-k 当成每日 top-k

因子选股通常是截面问题。

应该每个日期内部选 top-k。

如果直接对所有日期排序取 top-k，就混入了跨日期比较。

### 错误 5：指标方向反了

高分不一定更好。

例如：

```text
spread 越小越好
rank 越小越好
drawdown 越小越好
```

使用 `nlargest` 还是 `nsmallest` 前，要确认指标含义。

## 什么时候用哪种方法

可以用这个规则：

```text
需要完整排名：排序
数据量小：排序
k 很小且 n 很大：heap
数据流式到达：heap
只要无序 top-k 集合：quickselect
每组 top-k：groupby 后每组排序或每组 heap
```

实际工程里，可读性也重要。

如果数据量不大，排序往往是最清楚、最少出错的方案。

性能瓶颈明确后，再换 heap 或 quickselect。

## 记忆要点

- top-k 不一定需要完整排序。
- 排序方案简单，复杂度 `O(n log n)`。
- 固定大小 heap 复杂度 `O(n log k)`，适合 k 小和流式数据。
- quickselect 平均 `O(n)`，但结果内部不一定有序。
- heap 内部数组不是排序结果。
- top-k 要明确最大还是最小。
- 相同分数时要定义 tie-breaker。
- 因子研究里常见的是每日截面 top-k，而不是全样本 top-k。

## 自测题

1. 完整排序 top-k 和 heap top-k 的复杂度分别是什么？
2. 为什么 heap 的内部数组不能直接当成有序排名？
3. 什么情况下 quickselect 比排序更合适？
4. 因子研究中为什么常常要做每日分组 top-k？
5. 对 score 相同的股票，为什么需要 tie-breaker？
