# 77. 数据结构与算法：sorting 的稳定性、key 函数、复杂度和排序应用

## 核心概念

sorting 是排序。

它把一组元素按照某个规则排列：

```text
原始数据 -> 按 key 计算排序依据 -> 生成有序结果
```

在 Python 中，最常见的两个接口是：

```python
sorted(iterable, key=None, reverse=False)
list.sort(key=None, reverse=False)
```

区别是：

```text
sorted(...)  返回一个新 list，不修改原对象
list.sort()  原地修改 list，返回 None
```

基础例子：

```python
nums = [3, 1, 2]

copy_sorted = sorted(nums)
print(copy_sorted)
print(nums)

result = nums.sort()
print(nums)
print(result)
```

结果：

```text
[1, 2, 3]
[3, 1, 2]
[1, 2, 3]
None
```

所以不要写：

```python
nums = nums.sort()
```

这样会把 `nums` 变成 `None`。

## Python 排序的复杂度

Python 的 list 排序使用 Timsort。

可以把它理解为：

- 稳定排序。
- 平均和最坏时间复杂度通常是 `O(n log n)`。
- 对已经部分有序的数据很友好。
- 额外空间复杂度通常不是严格 `O(1)`，因为内部会使用临时数组。

常见复杂度对比：

```text
完整排序 n 个元素：O(n log n)
取前 k 个但先完整排序：O(n log n)
用 heap 取前 k 个：O(n log k)
```

当 `k` 很小、`n` 很大时，不一定要完整排序。

## key 函数

`key` 用来定义排序依据。

例子：按绝对值排序。

```python
values = [-10, 3, -2, 8]

ordered = sorted(values, key=abs)
print(ordered)
```

结果：

```text
[-2, 3, 8, -10]
```

对字典列表排序时，`key` 更常用。

```python
records = [
    {"symbol": "AAPL", "score": 0.12, "volume": 1000},
    {"symbol": "MSFT", "score": 0.31, "volume": 800},
    {"symbol": "NVDA", "score": 0.31, "volume": 1200},
    {"symbol": "TSLA", "score": 0.05, "volume": 1500},
]

by_score = sorted(records, key=lambda r: r["score"], reverse=True)

print([r["symbol"] for r in by_score])
```

结果：

```text
['MSFT', 'NVDA', 'AAPL', 'TSLA']
```

这里按 `score` 从高到低排序。

## reverse=True

`reverse=True` 表示反向排序。

```python
scores = [0.12, 0.31, 0.05]

print(sorted(scores))
print(sorted(scores, reverse=True))
```

结果：

```text
[0.05, 0.12, 0.31]
[0.31, 0.12, 0.05]
```

注意：

```python
sorted(records, key=lambda r: r["score"], reverse=True)
```

这会把整个排序方向反过来。

如果你想让某些字段升序、某些字段降序，通常用 tuple key。

## 多字段排序

量化中经常需要：

```text
score 越高越靠前
score 相同时 volume 越高越靠前
再相同时 symbol 字母序越小越靠前
```

可以写成：

```python
records = [
    {"symbol": "AAPL", "score": 0.12, "volume": 1000},
    {"symbol": "MSFT", "score": 0.31, "volume": 800},
    {"symbol": "NVDA", "score": 0.31, "volume": 1200},
    {"symbol": "TSLA", "score": 0.05, "volume": 1500},
]

ordered = sorted(
    records,
    key=lambda r: (-r["score"], -r["volume"], r["symbol"]),
)

print([r["symbol"] for r in ordered])
```

结果：

```text
['NVDA', 'MSFT', 'AAPL', 'TSLA']
```

解释：

```text
-score   score 从高到低
-volume  volume 从高到低
symbol   symbol 从低到高
```

tuple 会从左到右逐项比较。

这比只按 score 排序更可控，因为你明确写出了 tie-breaker。

## 稳定排序

稳定排序的意思是：

```text
如果两个元素的排序 key 相同，它们在结果中的相对顺序保持不变。
```

例子：

```python
rows = [
    ("tech", "AAPL", 2),
    ("finance", "JPM", 1),
    ("tech", "MSFT", 1),
    ("finance", "BAC", 2),
]

step1 = sorted(rows, key=lambda x: x[2])
step2 = sorted(step1, key=lambda x: x[0])

print(step2)
```

结果：

```text
[('finance', 'JPM', 1), ('finance', 'BAC', 2), ('tech', 'MSFT', 1), ('tech', 'AAPL', 2)]
```

第一步先按第三列排序。

第二步按 sector 排序。

因为排序稳定，所以同一个 sector 内部仍保留第一步留下的第三列顺序。

这是一种常见技巧：

```text
先按次要字段排序
再按主要字段排序
```

不过在 Python 中，如果字段逻辑不复杂，tuple key 通常更直接。

## itemgetter

如果排序对象是 tuple 或 list，可以用 `operator.itemgetter`。

```python
from operator import itemgetter

rows = [
    ("tech", "AAPL", 2),
    ("finance", "JPM", 1),
    ("tech", "MSFT", 1),
    ("finance", "BAC", 2),
]

ordered = sorted(rows, key=itemgetter(0, 2))

print(ordered)
```

这表示按第 0 列、第 2 列依次排序。

在非常频繁调用时，`itemgetter` 往往比简单 lambda 更直接，也更容易表达“按哪几列”。

## 排序行情事件

事件流常见字段：

```text
timestamp
sequence
event_type
payload
```

如果只按 timestamp 排序，遇到同一时间戳的多个事件时，顺序可能不够明确。

更稳妥的方式是同时使用 timestamp 和 sequence。

```python
updates = [
    (93005, 2, "trade"),
    (93000, 1, "open"),
    (93005, 1, "quote"),
]

ordered = sorted(updates, key=lambda x: (x[0], x[1]))

print(ordered)
```

结果：

```text
[(93000, 1, 'open'), (93005, 1, 'quote'), (93005, 2, 'trade')]
```

这类排序在回放行情、构造特征、对齐订单事件时很重要。

如果事件顺序错了，后续计算可能会出现未来信息泄露或不可复现结果。

## top-k 不一定要完整排序

问题：

```text
从很多股票中找 score 最高的前 2 个。
```

可以完整排序：

```python
top2 = sorted(records, key=lambda r: r["score"], reverse=True)[:2]
print([r["symbol"] for r in top2])
```

这会做完整排序，复杂度是 `O(n log n)`。

如果只要前 k 个，可以用 heap：

```python
import heapq

top2 = heapq.nlargest(2, records, key=lambda r: r["score"])

print([r["symbol"] for r in top2])
```

当 `k` 远小于 `n` 时，`heapq.nlargest(k, ...)` 通常更合适。

但如果你还需要完整排名，排序仍然是自然选择。

## 字符串排序

字符串默认按字典序排序。

```python
labels = ["item2", "item10", "item1"]

print(sorted(labels))
```

结果：

```text
['item1', 'item10', 'item2']
```

因为字符串比较不是自然数比较。

如果要按后面的数字排序，需要提取数字：

```python
ordered = sorted(labels, key=lambda s: int(s.replace("item", "")))

print(ordered)
```

结果：

```text
['item1', 'item2', 'item10']
```

## NaN 的排序问题

浮点数据里经常有 `NaN`。

`NaN` 的特殊之处在于：

```text
NaN 不小于任何数
NaN 不大于任何数
NaN 也不等于自己
```

所以排序含 `NaN` 的数据时，不要假设结果一定符合直觉。

更稳妥的做法是显式定义规则。

```python
import math

values = [0.3, math.nan, 0.1, 0.2]

ordered = sorted(values, key=lambda x: (math.isnan(x), x))

print(ordered)
```

结果：

```text
[0.1, 0.2, 0.3, nan]
```

这里的 key 是：

```text
先按是否为 NaN 排序
再按数值排序
```

`False < True`，所以非 NaN 会排在 NaN 前面。

## pandas 中的排序

pandas 里常用：

```python
df.sort_values(...)
df.sort_index(...)
```

例如：

```python
df.sort_values(["date", "score"], ascending=[True, False])
```

这表示：

```text
date 升序
同一天内部 score 降序
```

如果在因子研究中做每日选股，常见模式是：

```text
按 date 分组
每一天内部按 score 排名
取每一天 top-k
```

不要把所有日期混在一起直接排序再取前 k。

否则你得到的是全样本最高分，而不是每个交易日的截面组合。

## 排序的常见错误

### 错误 1：忘记 tie-breaker

只写：

```python
sorted(records, key=lambda r: r["score"], reverse=True)
```

如果很多股票 score 一样，排序结果会依赖原始输入顺序。

这不一定错，但你要确认原始输入顺序本身有意义。

更可复现的做法：

```python
sorted(records, key=lambda r: (-r["score"], r["symbol"]))
```

### 错误 2：误用 list.sort 的返回值

错误：

```python
nums = [3, 1, 2]
nums = nums.sort()
```

正确：

```python
nums = [3, 1, 2]
nums.sort()
```

或者：

```python
nums = [3, 1, 2]
ordered = sorted(nums)
```

### 错误 3：每个 tick 都完整排序

如果实时系统里每来一个 tick 都把全市场股票完整排序，成本可能很高。

如果只关心 top-k，可以考虑：

- heap。
- 局部更新。
- 分桶。
- 延迟排序。
- 批量刷新。

排序本身不难，难的是在正确频率上排序。

### 错误 4：对象不可比较

Python 不能随意比较两个 dict：

```python
records = [{"x": 1}, {"x": 2}]
```

直接写：

```python
sorted(records)
```

会报错。

应该指定 key：

```python
sorted(records, key=lambda r: r["x"])
```

### 错误 5：跨语言误判稳定性

Python 排序是稳定的。

但其他语言或库里的默认排序不一定稳定。

如果算法依赖稳定性，要检查对应环境的排序实现，或者显式使用稳定排序接口。

## 小例子：每日截面排名的思路

假设一天内有几只股票的因子分：

```python
scores = [
    ("2026-01-02", "AAPL", 0.12),
    ("2026-01-02", "MSFT", 0.31),
    ("2026-01-02", "NVDA", 0.31),
    ("2026-01-02", "TSLA", 0.05),
]

ordered = sorted(scores, key=lambda x: (x[0], -x[2], x[1]))

print(ordered[:2])
```

结果：

```text
[('2026-01-02', 'MSFT', 0.31), ('2026-01-02', 'NVDA', 0.31)]
```

排序规则是：

```text
date 升序
score 降序
symbol 升序作为 tie-breaker
```

如果有多天数据，真实项目里更常用 pandas `groupby("date")` 后在每个截面内部排序或排名。

## 什么时候用排序

适合排序的场景：

- 需要完整排名。
- 需要按时间回放事件。
- 需要确定性输出。
- 数据量不大，简单排序足够快。
- 需要按多个字段做清晰的优先级排序。

不一定适合完整排序的场景：

- 只需要 top-k 且 k 很小。
- 数据持续流入，只维护一个窗口。
- 每个事件都触发全量重排。
- 可以用堆、二分插入、分桶或增量结构解决。

## 记忆要点

- `sorted()` 返回新 list。
- `list.sort()` 原地排序，返回 `None`。
- Python 排序稳定。
- `key` 定义排序依据。
- tuple key 可以表达多字段排序。
- `reverse=True` 会反转整体顺序。
- top-k 不一定要完整排序。
- 对行情事件排序时，要明确 timestamp 之外的 tie-breaker。
- 对 `NaN`、字符串数字、不可比较对象，要显式定义排序规则。

## 自测题

1. `sorted()` 和 `list.sort()` 的区别是什么？
2. 什么是稳定排序？为什么它对多阶段排序有用？
3. 如何按 `score` 降序、`symbol` 升序排序一组股票记录？
4. 为什么只取 top-k 时不一定要完整排序？
5. 对行情事件排序时，为什么通常不能只依赖 timestamp？
