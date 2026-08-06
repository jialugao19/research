# 计算机基础：算法复杂度、大 O 表示法和策略代码效率分析

## 核心概念

算法复杂度描述：

```text
输入规模变大时，程序的运行时间或内存占用如何增长。
```

大 O 表示法关注增长速度，而不是精确运行秒数。

例如：

```text
O(1): 常数复杂度
O(log n): 对数复杂度
O(n): 线性复杂度
O(n log n): 常见高效排序复杂度
O(n^2): 二次复杂度
```

在策略代码里，复杂度直接影响：

```text
回测速度
因子计算速度
内存占用
实时交易延迟
参数搜索成本
```

## O(1)

O(1) 表示常数时间。

输入规模变大，操作次数基本不变。

例如访问列表中的某个位置：

```text
values[0]
```

它不需要扫描整个列表。

O(1) 不代表一定快。

它只表示不随 `n` 增长。

一个很慢的常数操作仍然是 O(1)。

## O(n)

O(n) 表示操作次数随输入规模线性增长。

例如遍历 `n` 个元素：

```python
n = 5
steps = 0

for i in range(n):
    steps += 1

print(steps)
```

结果：

```text
5
```

如果 `n` 从 `5` 变成 `5,000,000`，循环次数也大约变成 `5,000,000`。

很多因子计算、数据清洗和统计聚合都是 O(n)。

## O(n^2)

双重循环经常带来 O(n^2)。

```python
n = 5
steps = 0

for i in range(n):
    for j in range(n):
        steps += 1

print(steps)
```

结果：

```text
25
```

当 `n = 5` 时是 `25` 次。

当 `n = 10,000` 时就是 `100,000,000` 次。

这就是为什么策略代码里要警惕：

```text
按日期循环，再按股票循环，再按窗口循环
两两资产相关性暴力计算
对每个订单扫描所有历史订单
对每个 tick 扫描全日数据
```

这些写法小数据可用，大数据会爆炸。

## O(log n)

O(log n) 表示每一步都能把问题规模大幅缩小。

典型例子是不断除以 `2`：

```python
n = 16
steps = 0

while n > 1:
    n //= 2
    steps += 1

print(steps)
```

结果：

```text
4
```

`16 -> 8 -> 4 -> 2 -> 1`，只需要 `4` 步。

二分查找就是 O(log n)。

## 二分查找

在有序数组中查找目标，可以每次丢掉一半。

```python
values = [1, 3, 5, 7, 9]
target = 7

left = 0
right = len(values) - 1
steps = 0
found = False

while left <= right:
    steps += 1
    mid = (left + right) // 2
    if values[mid] == target:
        found = True
        break
    if values[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

print(found)
print(steps)
```

结果：

```text
True
2
```

二分查找的前提是数据已排序。

如果为了二分先排序，还要加上排序成本。

## O(n log n)

很多高效排序算法平均复杂度是 O(n log n)。

例如 Python 的 `sorted` 使用的排序算法在实际数据上很高效。

在策略代码里，排序很常见：

```text
按因子值排序选 top k
按时间戳排序 tick
按价格排序订单簿
按收益排序分组
```

排序通常比 O(n^2) 好很多。

但如果每个时点都对全市场重新排序，成本仍然可能很高。

## 常数项和大 O

大 O 会忽略常数项。

例如：

```text
3n 和 100n 都是 O(n)
```

但在工程里，常数项仍然重要。

同样是 O(n)，下面两种写法可能差很多：

```text
一次顺序扫描内存
每一步都做复杂对象创建和函数调用
```

所以复杂度是第一层判断。

性能优化还要看实现细节。

## 空间复杂度

时间复杂度描述运行时间增长。

空间复杂度描述额外内存增长。

例如创建一个新列表：

```python
items = [3, 1, 2]
result = []

for item in items:
    result.append(item * 2)

print(result)
print(len(result))
```

结果：

```text
[6, 2, 4]
3
```

`result` 的长度和输入一样。

所以额外空间是 O(n)。

如果数据很大，内存可能比 CPU 更早成为瓶颈。

## 两两组合

两两比较通常是 O(n^2)。

如果只取不重复组合，数量是 `n * (n - 1) / 2`。

```python
n = 4
pairs = [
    (i, j)
    for i in range(n)
    for j in range(i + 1, n)
]

print(pairs)
print(len(pairs))
```

结果：

```text
[(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
6
```

在金融里，两两组合经常出现在：

```text
协整配对
相关性矩阵
组合距离
聚类距离
```

股票数从 `500` 增加到 `5000`，两两计算会增加约 `100` 倍。

## 增长速度对比

同样的输入规模，线性和平方增长差异巨大。

```python
sizes = [10, 100, 1000]

linear = [
    n
    for n in sizes
]
quadratic = [
    n * n
    for n in sizes
]

print(linear)
print(quadratic)
```

结果：

```text
[10, 100, 1000]
[100, 10000, 1000000]
```

当 `n = 1000`，O(n) 是 `1000`。

O(n^2) 已经是 `1,000,000`。

这就是为什么复杂度分析比看小样本运行时间更可靠。

## rolling window 的复杂度

rolling 计算是策略里常见场景。

简单写法：

```python
prices = [100, 101, 102, 103]
window = 2

rolling = []
for i in range(window, len(prices) + 1):
    rolling.append(sum(prices[i - window:i]) / window)

print(rolling)
```

结果：

```text
[100.5, 101.5, 102.5]
```

这个例子很小。

但复杂度是：

```text
每个位置重新 sum window 个元素
总复杂度约 O(n * window)
```

如果 window 很大，这会很慢。

更好的做法是维护滚动和：

```text
新增一个值
减去一个旧值
每一步 O(1)
总复杂度 O(n)
```

这也是很多 pandas rolling 或专门算法的核心思想。

## 策略代码效率分析

分析策略代码时，可以按这几步看：

```text
输入规模是什么？
主循环有几层？
每层循环内部做了什么？
有没有重复排序、重复扫描、重复 groupby？
是否创建了大量中间对象？
是否能用哈希表、堆、二分、滚动更新降低复杂度？
```

例如：

```text
日期数 D
股票数 N
窗口长度 W
因子数 K
```

一个三层循环可能是：

```text
O(D * N * W)
```

如果再在内部排序，可能变成：

```text
O(D * N * W log W)
```

先把量级写出来，优化方向会清楚很多。

## 常见误区

复杂度分析常见误区：

```text
只看一行代码，不看它内部是否循环
认为 pandas 一定快
认为 vectorization 一定省内存
忽略排序和 groupby 成本
忽略中间 DataFrame 的复制成本
只在小样本上计时
把 O(n^2) 问题寄希望于机器更快
```

工程上更稳的做法是：

```text
先估算复杂度
再用代表性数据计时
最后用 profiler 找热点
```

## 小结

大 O 表示法帮助你判断代码随数据规模增长会不会失控。

需要掌握：

```text
O(1)
O(log n)
O(n)
O(n log n)
O(n^2)
时间复杂度
空间复杂度
策略代码中的 D、N、W、K 量级
```

写策略代码时，要特别警惕多层循环、重复排序和重复扫描。

下一篇讨论列表、字典、集合的底层实现与操作代价。
