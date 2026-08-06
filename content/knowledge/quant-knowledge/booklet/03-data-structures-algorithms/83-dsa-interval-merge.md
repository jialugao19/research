# 83. 数据结构与算法：interval merge 的区间排序、合并和时间段应用

## 核心概念

interval merge 是区间合并。

给定一组区间：

```text
[1, 3], [2, 6], [8, 10], [9, 12]
```

其中 `[1, 3]` 和 `[2, 6]` 有重叠，可以合并成 `[1, 6]`。

`[8, 10]` 和 `[9, 12]` 有重叠，可以合并成 `[8, 12]`。

结果：

```text
[1, 6], [8, 12]
```

区间合并常用于：

- 合并时间段。
- 合并交易暂停区间。
- 合并任务占用时间。
- 检查会议冲突。
- 计算覆盖长度。
- 合并数据缺失区间。
- 合并风控禁交易窗口。

## 区间边界约定

写区间算法前，必须先明确边界约定。

常见两种：

```text
闭区间 [start, end]      包含 start 和 end
半开区间 [start, end)    包含 start，不包含 end
```

时间序列和工程系统里，半开区间很常见：

```text
[09:30, 10:00)
[10:00, 10:30)
```

这两个区间首尾相接，但不重叠。

如果用闭区间：

```text
[09:30, 10:00]
[10:00, 10:30]
```

它们在 `10:00` 这个点重叠。

本篇默认用半开区间 `[start, end)`，除非特别说明。

## 基础算法

区间合并的标准做法：

```text
先按 start 排序
从左到右扫描
如果当前区间和最后一个结果区间重叠，就扩展 end
否则追加新区间
```

复杂度：

```text
排序：O(n log n)
扫描：O(n)
总复杂度：O(n log n)
```

如果输入已经按 start 排好序，扫描部分就是 `O(n)`。

## 合并半开区间

半开区间 `[start, end)` 中，两个区间重叠的条件是：

```text
next_start < current_end
```

如果：

```text
next_start == current_end
```

它们只是相邻，不算重叠。

```python
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals = sorted(intervals)
    merged = [list(intervals[0])]

    for start, end in intervals[1:]:
        last = merged[-1]

        if start < last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return [tuple(interval) for interval in merged]


intervals = [(1, 3), (2, 6), (8, 10), (9, 12)]
print(merge_intervals(intervals))
```

结果：

```text
[(1, 6), (8, 12)]
```

## 相邻区间是否合并

有时业务上希望把相邻区间也合并。

例如：

```text
[1, 3), [3, 5)
```

如果表示“连续不可交易时间”，可以合并成：

```text
[1, 5)
```

这时条件变成：

```text
next_start <= current_end
```

```python
def merge_intervals_touching(intervals):
    if not intervals:
        return []

    intervals = sorted(intervals)
    merged = [list(intervals[0])]

    for start, end in intervals[1:]:
        last = merged[-1]

        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])

    return [tuple(interval) for interval in merged]


print(merge_intervals_touching([(1, 3), (3, 5), (8, 10)]))
```

结果：

```text
[(1, 5), (8, 10)]
```

关键不是哪种更对，而是业务语义要一致。

## 会议冲突

问题：

```text
给定多个会议时间，判断是否有冲突。
```

半开区间下：

```text
[9, 10), [10, 11)
```

不冲突。

```python
def has_overlap(intervals):
    intervals = sorted(intervals)

    for (prev_start, prev_end), (start, end) in zip(intervals, intervals[1:]):
        if start < prev_end:
            return True

    return False


print(has_overlap([(9, 10), (10, 11), (13, 14)]))
print(has_overlap([(9, 10), (9.5, 11)]))
```

结果：

```text
False
True
```

这类逻辑可用于：

- 任务调度。
- 资源占用检查。
- 交易窗口冲突检查。
- 数据处理 pipeline 的时间段冲突。

## 计算覆盖长度

如果区间有重叠，直接把长度相加会重复计数。

例如：

```text
[1, 3), [2, 5)
```

单独长度是：

```text
2 + 3 = 5
```

实际覆盖是：

```text
[1, 5) -> 4
```

所以要先合并，再求长度。

```python
def covered_length(intervals):
    merged = merge_intervals(intervals)
    return sum(end - start for start, end in merged)


print(covered_length([(1, 3), (2, 5), (10, 12)]))
```

结果：

```text
6
```

覆盖区间是：

```text
[1, 5), [10, 12)
```

长度：

```text
4 + 2 = 6
```

## 交易时段合并

假设某策略有多个允许交易窗口：

```python
windows = [
    (93000, 100000),
    (94500, 103000),
    (130000, 140000),
    (140000, 145000),
]
```

如果相邻窗口要合并，使用 `merge_intervals_touching`。

```python
print(merge_intervals_touching(windows))
```

结果：

```text
[(93000, 103000), (130000, 145000)]
```

注意这里的时间只是整数编码，真实系统中最好使用标准时间类型或统一的纳秒/毫秒时间戳。

## 插入新区间

问题：

```text
已有不重叠且按 start 排序的区间，插入一个新区间，然后合并。
```

直接做法：

```python
def insert_interval(intervals, new_interval):
    return merge_intervals(intervals + [new_interval])


print(insert_interval([(1, 3), (6, 9)], (2, 7)))
```

结果：

```text
[(1, 9)]
```

这个做法简单可靠，复杂度是：

```text
O(n log n)
```

如果输入已排序且区间互不重叠，可以用一次扫描做到 `O(n)`。

```python
def insert_interval_sorted(intervals, new_interval):
    result = []
    new_start, new_end = new_interval
    i = 0

    while i < len(intervals) and intervals[i][1] <= new_start:
        result.append(intervals[i])
        i += 1

    while i < len(intervals) and intervals[i][0] < new_end:
        new_start = min(new_start, intervals[i][0])
        new_end = max(new_end, intervals[i][1])
        i += 1

    result.append((new_start, new_end))
    result.extend(intervals[i:])

    return result


print(insert_interval_sorted([(1, 3), (6, 9)], (2, 7)))
```

结果：

```text
[(1, 9)]
```

这里仍然按半开区间处理，相邻不自动合并。

## 找空闲时间

给定忙碌时间段，找某个范围内的空闲时间。

```python
def free_intervals(busy, start, end):
    busy = merge_intervals(busy)
    free = []
    cursor = start

    for busy_start, busy_end in busy:
        if busy_start > cursor:
            free.append((cursor, busy_start))
        cursor = max(cursor, busy_end)

    if cursor < end:
        free.append((cursor, end))

    return free


busy = [(9, 10), (9.5, 11), (13, 14)]
print(free_intervals(busy, 9, 15))
```

结果：

```text
[(11, 13), (14, 15)]
```

这可用于：

- 找可交易窗口。
- 找任务可调度时间。
- 找机器空闲时间。
- 找数据缺失以外的可用时间段。

## 合并缺失数据区间

假设你记录了多个缺失数据时间段：

```python
missing = [
    (1000, 1010),
    (1005, 1020),
    (1100, 1110),
]

merged_missing = merge_intervals(missing)

print(merged_missing)
```

结果：

```text
[(1000, 1020), (1100, 1110)]
```

后续可以计算总缺失长度：

```python
print(covered_length(missing))
```

结果：

```text
30
```

这比简单相加更准确，因为重叠缺失时间不会被重复计数。

## 多个来源的禁交易窗口

禁交易窗口可能来自多个来源：

```text
市场休市
风控暂停
数据异常
策略冷却时间
手动禁用
```

把它们统一成区间列表后合并：

```python
halt_windows = [(93000, 93500), (93400, 94000)]
risk_windows = [(100000, 101000)]
data_windows = [(100500, 101500)]

blocked = merge_intervals_touching(
    halt_windows + risk_windows + data_windows
)

print(blocked)
```

结果：

```text
[(93000, 94000), (100000, 101500)]
```

这样可以得到最终不可交易时间段。

再用 `free_intervals` 可以得到可交易时间段。

## 判断某个点是否在区间内

如果区间已经合并且排序，可以用二分查找判断某个时间点是否被覆盖。

```python
from bisect import bisect_right

def contains_point(merged_intervals, point):
    starts = [start for start, _ in merged_intervals]
    idx = bisect_right(starts, point) - 1

    if idx < 0:
        return False

    start, end = merged_intervals[idx]
    return start <= point < end


blocked = [(93000, 94000), (100000, 101500)]

print(contains_point(blocked, 93500))
print(contains_point(blocked, 94000))
```

结果：

```text
True
False
```

因为本篇使用半开区间，所以 `94000` 不属于 `(93000, 94000)`。

严格写法应说：

```text
94000 不属于 [93000, 94000)
```

## 扫描线思想

有些区间问题不是只合并，而是要统计同时覆盖数量。

例如：

```text
最多同时有多少个任务在运行？
```

可以用 sweep line，扫描线。

半开区间 `[start, end)` 下：

```python
def max_overlap_count(intervals):
    events = []

    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))

    events.sort(key=lambda x: (x[0], x[1]))

    current = 0
    best = 0

    for _, delta in events:
        current += delta
        best = max(best, current)

    return best


print(max_overlap_count([(1, 3), (2, 5), (5, 8)]))
```

结果：

```text
2
```

排序 key 里 `(time, delta)` 会让同一时间的 `-1` 在 `+1` 前面。

这符合半开区间：

```text
[2, 5) 和 [5, 8) 在 5 不重叠
```

## pandas 中的时间区间

pandas 里经常会遇到：

```text
start_time
end_time
```

可以先把每行转成 tuple，然后用 Python 函数合并。

伪代码：

```python
intervals = list(zip(df["start_time"], df["end_time"]))
merged = merge_intervals(intervals)
```

如果要按股票分别合并缺失区间：

```python
result = {}

for symbol, group in df.groupby("symbol"):
    intervals = list(zip(group["start_time"], group["end_time"]))
    result[symbol] = merge_intervals(intervals)
```

真实项目中要注意：

- 时区。
- 日期跨越。
- 开闭边界。
- 时间戳精度。
- 是否允许相邻区间合并。

## 常见错误

### 错误 1：没有先排序

区间合并必须先按 start 排序。

如果直接按输入顺序扫描，结果依赖输入顺序，可能漏合并。

### 错误 2：边界条件不清楚

`start < end` 还是 `start <= end`？

相邻区间是否合并？

`[1,3)` 和 `[3,5)` 是否重叠？

这些都要在写代码前确定。

### 错误 3：用闭区间思维写半开区间

半开区间中：

```text
[1, 3) 和 [3, 5) 不重叠
```

如果用 `start <= last_end` 合并，就会把它们合并。

这可能正确，也可能错误，取决于业务。

### 错误 4：覆盖长度重复计数

不要直接求：

```python
sum(end - start for start, end in intervals)
```

除非你确定区间没有重叠。

否则要先合并。

### 错误 5：时间编码不统一

例如：

```text
93000
09:30:00
datetime
Unix timestamp
```

这些不能混用。

先统一时间表示，再合并区间。

## 什么时候用 interval merge

适合使用 interval merge 的场景：

- 需要合并重叠时间段。
- 需要计算总覆盖长度。
- 需要找空闲时间。
- 需要判断时间点是否落入禁用窗口。
- 需要合并多个来源的交易暂停区间。
- 需要处理缺失数据、异常数据、任务占用时间。

不一定需要 interval merge 的场景：

- 区间本来就互不重叠且已排序。
- 只处理单个时间点。
- 更关心并发数量而不是合并后的区间。
- 需要复杂区间查询，应考虑 interval tree 等结构。

## 记忆要点

- interval merge 的核心是先排序再扫描。
- 半开区间 `[start, end)` 在工程里很常见。
- 半开区间中，相邻不等于重叠。
- 是否合并相邻区间是业务语义。
- 合并后再求覆盖长度，避免重复计数。
- 插入区间可以先追加再合并，也可以在线性扫描中合并。
- 已排序合并区间可以配合二分判断点是否被覆盖。
- 扫描线可以统计最大重叠数量。

## 自测题

1. 区间合并为什么要先按 start 排序？
2. 半开区间 `[1, 3)` 和 `[3, 5)` 是否重叠？
3. 什么时候应该把相邻区间也合并？
4. 为什么计算覆盖长度前要先合并区间？
5. 如何用扫描线计算最大同时重叠区间数？
