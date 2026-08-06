# 数据结构与算法：rolling median 的双堆维护、延迟删除和滑动窗口应用

## 核心概念

rolling median 是滚动中位数。

给定一个序列和窗口长度 `window`，每次只看最近 `window` 个值，计算其中位数。

例如：

```text
values = [5, 1, 9, 3, 8]
window = 3
```

窗口依次是：

```text
[5, 1, 9] -> median = 5
[1, 9, 3] -> median = 3
[9, 3, 8] -> median = 8
```

所以结果是：

```text
[5, 3, 8]
```

rolling median 常用于：

- 鲁棒平滑。
- 去除极端值影响。
- 流式数据监控。
- 微观结构噪声过滤。
- 滚动风险指标。
- 盘口或成交数据的短窗口统计。

和 rolling mean 相比，中位数对异常值更不敏感。

## 为什么 rolling median 更麻烦

rolling mean 可以用 running sum：

```text
新值进来，旧值出去，sum 加减一次
```

所以每步是 `O(1)`。

rolling median 不行。

因为中位数依赖窗口内部的相对顺序。

最直接的方法是：

```text
每个窗口重新排序一次
```

复杂度：

```text
每个窗口排序：O(window log window)
总复杂度：O(n * window log window)
```

窗口很大或数据很多时，这会慢。

## 暴力做法

先看最直观版本。

```python
def median_sorted(items):
    ordered = sorted(items)
    n = len(ordered)
    mid = n // 2

    if n % 2 == 1:
        return ordered[mid]

    return (ordered[mid - 1] + ordered[mid]) / 2


def rolling_median_bruteforce(values, window):
    result = []

    for i in range(window - 1, len(values)):
        chunk = values[i - window + 1 : i + 1]
        result.append(median_sorted(chunk))

    return result


values = [5, 1, 9, 3, 8]
print(rolling_median_bruteforce(values, 3))
```

结果：

```text
[5, 3, 8]
```

这版逻辑清楚，适合：

- 数据量很小。
- 写测试用的基准答案。
- 先验证复杂实现是否正确。

但它不适合高频流式场景。

## 双堆思路

更高效的做法是 two heaps，双堆。

维护两个堆：

```text
small  保存较小的一半，最大堆
large  保存较大的一半，最小堆
```

Python `heapq` 只有最小堆。

所以 `small` 用负数模拟最大堆：

```text
small  里面存 -x，堆顶 -small[0] 是较小一半的最大值
large  里面存 x，堆顶 large[0] 是较大一半的最小值
```

核心不变量：

```text
len(small) == len(large)
或者
len(small) == len(large) + 1
```

也就是让 `small` 的有效元素数量不小于 `large`，最多多一个。

这样中位数就是：

```text
奇数个元素：-small[0]
偶数个元素：(-small[0] + large[0]) / 2
```

## 插入一个数

插入时先和 `small` 的堆顶比较。

```python
import heapq

small = []
large = []

def add_num(x):
    if not small or x <= -small[0]:
        heapq.heappush(small, -x)
    else:
        heapq.heappush(large, x)
```

插入后，两个堆的大小可能失衡。

需要 rebalance。

```python
def rebalance():
    if len(small) > len(large) + 1:
        heapq.heappush(large, -heapq.heappop(small))
    elif len(small) < len(large):
        heapq.heappush(small, -heapq.heappop(large))
```

完整的插入中位数例子：

```python
import heapq

small = []
large = []

def add_num(x):
    if not small or x <= -small[0]:
        heapq.heappush(small, -x)
    else:
        heapq.heappush(large, x)

    if len(small) > len(large) + 1:
        heapq.heappush(large, -heapq.heappop(small))
    elif len(small) < len(large):
        heapq.heappush(small, -heapq.heappop(large))

def current_median():
    if len(small) > len(large):
        return -small[0]
    return (-small[0] + large[0]) / 2

for x in [5, 1, 9, 3]:
    add_num(x)
    print(current_median())
```

输出：

```text
5
3.0
5
4.0
```

这是持续插入场景的 median。

但 rolling window 还需要删除过期元素。

## 删除为什么困难

heap 擅长删除堆顶。

但 rolling window 里，过期元素可能在堆的任意位置。

例如窗口从：

```text
[5, 1, 9]
```

滑到：

```text
[1, 9, 3]
```

需要删除 `5`。

如果 `5` 不在堆顶，直接从 heap 列表里找出来删除，会变成 `O(window)`，再修复堆也麻烦。

常用技巧是 lazy deletion，延迟删除。

## 延迟删除

延迟删除的思路：

```text
过期元素先记录到 delayed 计数表
真正出现在堆顶时再弹掉
```

例如：

```python
from collections import Counter

delayed = Counter()
delayed[5] += 1
```

清理堆顶：

```python
def prune(heap, sign):
    while heap:
        x = sign * heap[0]
        if delayed[x] == 0:
            break

        delayed[x] -= 1
        if delayed[x] == 0:
            del delayed[x]
        heapq.heappop(heap)
```

其中：

```text
sign = -1  表示 small，因为 small 存的是 -x
sign = 1   表示 large
```

## 完整实现：双堆 rolling median

下面是一版可运行实现。

它维护：

```text
small       较小一半，最大堆，用负数实现
large       较大一半，最小堆
delayed     延迟删除计数
small_size  small 中有效元素数量
large_size  large 中有效元素数量
```

注意：`len(small)` 包含尚未清理的过期元素，所以需要单独维护有效大小。

```python
from collections import Counter
import heapq


class RollingMedian:
    def __init__(self, window):
        self.window = window
        self.small = []
        self.large = []
        self.delayed = Counter()
        self.small_size = 0
        self.large_size = 0

    def add(self, x):
        if not self.small or x <= -self.small[0]:
            heapq.heappush(self.small, -x)
            self.small_size += 1
        else:
            heapq.heappush(self.large, x)
            self.large_size += 1

        self._rebalance()

    def remove(self, x):
        self.delayed[x] += 1

        if x <= -self.small[0]:
            self.small_size -= 1
            if x == -self.small[0]:
                self._prune(self.small, -1)
        else:
            self.large_size -= 1
            if self.large and x == self.large[0]:
                self._prune(self.large, 1)

        self._rebalance()

    def median(self):
        if self.window % 2 == 1:
            return -self.small[0]

        return (-self.small[0] + self.large[0]) / 2

    def _rebalance(self):
        if self.small_size > self.large_size + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
            self.small_size -= 1
            self.large_size += 1
            self._prune(self.small, -1)
        elif self.small_size < self.large_size:
            heapq.heappush(self.small, -heapq.heappop(self.large))
            self.large_size -= 1
            self.small_size += 1
            self._prune(self.large, 1)

    def _prune(self, heap, sign):
        while heap:
            x = sign * heap[0]
            if self.delayed[x] == 0:
                break

            self.delayed[x] -= 1
            if self.delayed[x] == 0:
                del self.delayed[x]
            heapq.heappop(heap)
```

使用它计算滚动中位数：

```python
def rolling_median(values, window):
    if window <= 0:
        raise ValueError("window must be positive")
    if window > len(values):
        return []

    state = RollingMedian(window)
    result = []

    for i, x in enumerate(values):
        state.add(x)

        if i >= window:
            state.remove(values[i - window])

        if i >= window - 1:
            result.append(state.median())

    return result


values = [5, 1, 9, 3, 8]
print(rolling_median(values, 3))
```

结果：

```text
[5, 3, 8]
```

## 偶数窗口

偶数窗口的中位数通常定义为中间两个值的平均。

```python
values = [5, 1, 9, 3, 8]

print(rolling_median(values, 4))
```

窗口：

```text
[5, 1, 9, 3] -> sorted = [1, 3, 5, 9] -> median = 4.0
[1, 9, 3, 8] -> sorted = [1, 3, 8, 9] -> median = 5.5
```

结果：

```text
[4.0, 5.5]
```

在金融数据中，要提前定义好偶数窗口中位数规则。

有些系统会取低中位数或高中位数，而不是平均值。

## 和暴力版本做校验

复杂数据结构容易写错。

一个实用习惯是：

```text
用简单暴力实现当 oracle
随机生成小数据
比较两个实现的输出
```

例子：

```python
import random

random.seed(7)

for _ in range(100):
    n = random.randint(1, 20)
    values = [random.randint(-5, 5) for _ in range(n)]
    window = random.randint(1, n)

    expected = rolling_median_bruteforce(values, window)
    actual = rolling_median(values, window)

    assert actual == expected
```

这种测试能覆盖：

- 重复值。
- 负数。
- 奇数窗口。
- 偶数窗口。
- 窗口为 1。
- 窗口等于全长度。

## 时间复杂度

双堆方案的复杂度：

```text
插入：O(log window)
删除：摊还 O(log window)
取中位数：O(1)
总复杂度：O(n log window)
空间复杂度：O(window)
```

这里删除是摊还复杂度。

因为延迟删除的元素不会立刻从堆内部移除，但每个元素最终最多被 `heappop` 一次。

和每个窗口重新排序相比：

```text
暴力排序：O(n * window log window)
双堆：O(n log window)
```

窗口越大，差距越明显。

## 小例子：鲁棒价格平滑

假设成交价里有一个异常跳点：

```python
prices = [100, 101, 102, 150, 103, 104, 105]

print(rolling_median(prices, 3))
```

结果：

```text
[101, 102, 103, 104, 104]
```

窗口 `[102, 150, 103]` 的中位数是 `103`。

如果用均值，这个异常值会明显抬高窗口统计。

rolling median 因此适合做：

- tick 噪声过滤。
- 异常报价平滑。
- 特征预处理。
- 稳健趋势估计。

## 小例子：盘口价差中位数

假设每个 tick 有一个 bid-ask spread：

```python
spreads = [1, 1, 2, 20, 2, 1, 2]

median_spread = rolling_median(spreads, 3)

print(median_spread)
```

结果：

```text
[1, 2, 2, 2, 2]
```

极端 spread `20` 没有像均值那样强烈影响结果。

这类统计可以用于：

- 判断近期交易成本。
- 平滑盘口噪声。
- 过滤异常流动性状态。

## pandas rolling median

在 pandas 里，最常用的是：

```python
df["price_median_20"] = df["price"].rolling(20).median()
```

pandas 已经实现了滚动窗口逻辑。

你不需要在日常分析里手写双堆。

但理解双堆有价值：

- 面试常考。
- 能判断复杂度。
- 能写流式系统。
- 能处理 pandas 不适合的在线场景。

在回测里要注意：

```text
rolling(...).median() 默认包含当前行
```

如果当前信号只能使用上一时刻以前的信息，通常要加：

```python
feature = df["price"].rolling(20).median().shift(1)
```

这和之前讲过的未来信息泄露是同一类问题。

## 常见错误

### 错误 1：窗口删除时直接 heap.remove

`heap.remove(x)` 会线性搜索，复杂度是 `O(window)`。

删除后还需要重新维护堆性质。

在频繁滑动窗口里，这会抵消 heap 的优势。

### 错误 2：用 len(heap) 当有效大小

延迟删除后，heap 中可能有过期元素。

所以：

```python
len(small)
```

不等于 `small` 的有效元素数量。

需要单独维护 `small_size` 和 `large_size`。

### 错误 3：没有处理重复值

rolling median 中重复值很常见。

延迟删除不能只用 set。

应该用 `Counter` 记录每个值要删除几次。

### 错误 4：偶数窗口定义不清

偶数窗口中位数可以有不同定义：

- 中间两个值的平均。
- 低中位数。
- 高中位数。

不同定义会影响策略特征。

在研究和生产之间要保持一致。

### 错误 5：回测特征忘记 shift

如果你用当前 bar 的收盘价计算 rolling median，然后立刻在同一 bar 交易，就可能引入未来信息。

常见安全写法：

```python
feature = price.rolling(window).median().shift(1)
```

信号时间和可用数据时间必须对齐。

## 什么时候手写 rolling median

适合手写或理解双堆的场景：

- 在线流式数据。
- 面试算法题。
- 不方便使用 pandas 的低延迟系统。
- 需要明确控制窗口删除和中位数定义。
- 需要和其他堆结构一起维护复杂状态。

日常离线研究中，优先使用成熟库：

```text
pandas rolling median
numpy / bottleneck / polars 的滚动统计
```

除非性能、语义或部署环境要求你自己实现。

## 记忆要点

- rolling median 比 rolling mean 难，因为它依赖窗口内部排序。
- 暴力做法简单，但每个窗口重新排序会慢。
- 双堆维护较小一半和较大一半。
- `small` 用负数模拟最大堆。
- 中位数可以从两个堆顶 `O(1)` 得到。
- 滑动窗口删除需要延迟删除。
- 延迟删除时要用 `Counter` 处理重复值。
- 有过期元素时，不能用 `len(heap)` 当有效大小。
- pandas 研究中常用 `.rolling(...).median()`，但回测特征要注意 `shift(1)`。

## 自测题

1. 为什么 rolling mean 可以用 running sum，而 rolling median 不行？
2. 双堆方案中 `small` 和 `large` 分别保存什么？
3. 为什么 Python 的 `small` 要存负数？
4. 什么是延迟删除？为什么 rolling window 中需要它？
5. 在回测中使用 rolling median 特征时，为什么经常需要 `shift(1)`？
