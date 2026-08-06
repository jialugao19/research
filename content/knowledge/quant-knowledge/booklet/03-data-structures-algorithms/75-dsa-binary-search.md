# Binary Search

## 核心概念

binary search 二分查找用于在有序数据中快速定位位置。

最基本问题：

```text
在有序数组中查找 target
```

时间复杂度：

```text
O(log n)
```

二分查找的核心不是“找中间点”这么简单，而是维护一个不变量：

```text
答案一定在当前搜索区间里
```

每一步用 `mid` 排除一半不可能的区间。

## binary search 回答的问题

二分查找适合：

- 在有序数组中查找一个值。
- 找第一个大于等于 target 的位置。
- 找第一个大于 target 的位置。
- 统计 target 出现次数。
- 做有序时间戳查询。
- 在单调函数上找阈值。
- 在答案空间上二分，例如最小可行容量、最小可行时间。

量化数据中很常见：

```text
给定订单时间，找不晚于它的最新 quote
给定日期，找最近一个交易日
给定价格档位，找插入位置
给定阈值，找第一个超过阈值的风险指标
```

## 准备环境

Python 标准库提供 `bisect`：

```python
from bisect import bisect_left, bisect_right
```

准备有重复值的有序数组：

```python
arr = [2, 4, 4, 4, 7, 9, 13]
```

重复值是二分查找最容易写错边界的地方。

## lower_bound 模板

`lower_bound` 找第一个 `>= target` 的位置。

使用半开区间 `[left, right)`：

```python
def lower_bound(a, target):
    left, right = 0, len(a)

    while left < right:
        mid = (left + right) // 2

        if a[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left
```

例子：

```python
print(lower_bound(arr, 4))
print(lower_bound(arr, 5))
print(lower_bound(arr, 20))
```

含义：

- `lower_bound(arr, 4)` 返回第一个 `4` 的位置。
- `lower_bound(arr, 5)` 返回 `7` 的位置，因为 `7` 是第一个大于等于 `5` 的数。
- `lower_bound(arr, 20)` 返回 `len(arr)`，表示没有元素大于等于 `20`。

## upper_bound 模板

`upper_bound` 找第一个 `> target` 的位置。

```python
def upper_bound(a, target):
    left, right = 0, len(a)

    while left < right:
        mid = (left + right) // 2

        if a[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return left
```

例子：

```python
print(upper_bound(arr, 4))
print(upper_bound(arr, 5))
print(upper_bound(arr, 20))
```

`upper_bound(arr, 4)` 返回最后一个 `4` 后面的下标。

所以 target 的出现次数可以写成：

```python
count_4 = upper_bound(arr, 4) - lower_bound(arr, 4)

print(count_4)
```

## 和 bisect 对照

Python 内置：

```python
print(bisect_left(arr, 4))
print(bisect_right(arr, 4))
```

对应关系：

```text
bisect_left  == lower_bound
bisect_right == upper_bound
```

建议：

- 面试时会要求手写二分。
- 工程代码里优先用 `bisect`，更少边界错误。

## 精确查找

如果要找 target 是否存在，可以先找 lower_bound：

```python
def binary_search(a, target):
    idx = lower_bound(a, target)

    if idx < len(a) and a[idx] == target:
        return idx

    return -1


print(binary_search(arr, 7))
print(binary_search(arr, 8))
```

这种写法比同时维护一堆 `left <= right` 条件更稳。

如果数组有重复值，它返回第一个 target 的位置。

## 单调谓词：first true

二分不只用于数组，也可用于单调谓词。

问题：

```text
找最小整数 x，使得 x*x >= 30
```

```python
def first_true(left, right, predicate):
    while left < right:
        mid = (left + right) // 2

        if predicate(mid):
            right = mid
        else:
            left = mid + 1

    return left


answer = first_true(0, 100, lambda x: x * x >= 30)

print(answer)
```

这里搜索空间是 `[0, 100)`。

这个模板适合很多“最小可行值”问题：

```text
最小容量，使得任务能在 D 天内完成
最小阈值，使得风险不超过限制
最小时间，使得订单可以全部成交
```

前提是 predicate 单调：

```text
False False False True True True
```

## 时间戳查找：最近不晚于

行情数据常按时间排序。

给定一个交易时间，找不晚于它的最新 quote。

```python
quotes = [
    (93000, 100.1),
    (93005, 100.2),
    (93010, 100.4),
    (93020, 100.0),
]

times = [timestamp for timestamp, price in quotes]

query_time = 93012

idx = bisect_right(times, query_time) - 1

if idx >= 0:
    latest_quote = quotes[idx]
else:
    latest_quote = None

print(latest_quote)
```

`bisect_right(times, query_time)` 给出第一个 `> query_time` 的位置。

减 1 后就是最后一个 `<= query_time` 的位置。

这是处理 tick 数据、订单事件和特征对齐时非常常见的模式。

## 范围查询

找 `[start, end]` 时间区间内的 quotes：

```python
start_time = 93005
end_time = 93015

left = bisect_left(times, start_time)
right = bisect_right(times, end_time)

quotes_in_range = quotes[left:right]

print(quotes_in_range)
```

半开切片 `[left:right]` 和二分边界天然配合。

注意：

- `bisect_left` 包含左边界。
- `bisect_right` 包含右边界。

如果你需要 `[start, end)`，右边界应使用 `bisect_left(times, end_time)`。

## 边界为什么容易错

常见错误：

- `while left <= right` 和 `while left < right` 混用。
- 更新 `left = mid` 导致死循环。
- 忘记 target 不存在时返回插入位置。
- 重复值时不知道要左边界还是右边界。
- 查询“不晚于”时忘记 `-1`。

半开区间模板的优点：

```text
left, right = 0, len(a)
while left < right
最终返回 left
```

这个模板天然能返回 `0` 到 `len(a)` 之间的插入位置。

## 复杂度和适用条件

二分查找复杂度：

```text
时间 O(log n)
空间 O(1)
```

前提：

- 数据按 key 有序。
- 可以通过下标快速访问中间元素。
- 或者 predicate 在答案空间上单调。

如果数据无序，二分无效。

如果每次插入都要保持列表有序，插入本身可能是 `O(n)`。这时要根据场景考虑 heap、平衡树、数据库索引或批量排序。

## 常见坑

第一，在无序数组上二分。

二分依赖有序性或单调性。没有这个前提，结果没有意义。

第二，重复值边界混乱。

找第一个等于 target，用 `bisect_left`；找最后一个等于 target，通常用 `bisect_right(target) - 1`。

第三，时间戳对齐方向错。

实盘特征一般要找“不晚于当前时点”的最近数据，不能找未来最近数据。

第四，边界外没有处理。

`bisect_right(times, query) - 1` 可能是 `-1`，表示 query 早于所有数据。

第五，把二分用于链表。

链表不能 O(1) 访问中间元素，二分优势消失。

## 实战提示

使用 binary search 时可以按下面判断：

1. 数据是否有序？
2. 你要找的是精确值、左边界、右边界还是插入点？
3. 重复值时想要第一个还是最后一个？
4. 时间戳查询是找不晚于、早于、不早于，还是严格晚于？
5. predicate 是否单调？
6. 是否要处理没有结果的边界情况？

工程代码里，能用 `bisect_left` / `bisect_right` 时优先使用标准库。

手写时，优先使用 `[left, right)` 模板，减少边界错误。

## 小结

本节的重点：

- binary search 用于有序数据或单调 predicate。
- `lower_bound` 找第一个 `>= target` 的位置。
- `upper_bound` 找第一个 `> target` 的位置。
- `bisect_left` 对应 lower_bound，`bisect_right` 对应 upper_bound。
- 重复值计数可以用 `upper_bound - lower_bound`。
- 时间序列里常用二分找“不晚于当前时点”的最新记录。
- 二分的关键是边界不变量，而不是记住某个魔法模板。

## 自检问题

1. `bisect_left` 和 `bisect_right` 的区别是什么？
2. 为什么二分查找要求数据有序或 predicate 单调？
3. 如何统计有序数组中 target 出现次数？
4. 给定交易时间，如何找不晚于它的最新 quote？
5. `[left, right)` 模板为什么常返回插入位置？
6. 为什么链表不适合做普通二分查找？
