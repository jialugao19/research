# Combinatorics

## 核心概念

combinatorics 是组合计数。

它回答的问题是：

```text
有多少种可能？
```

常见场景：

- 排队。
- 抽牌。
- 分组。
- 选子集。
- 安排座位。
- 密码组合。
- 路径数量。
- 至少一个、恰好几个、没有相邻等限制条件。

计数题最常见的错误不是公式不会，而是：

```text
有没有顺序？
能不能重复？
限制条件怎么处理？
有没有重复计数？
```

## 乘法原则

如果一个过程分成两步：

```text
第一步有 a 种选择
第二步有 b 种选择
```

并且每个第一步选择后都有 `b` 种第二步选择，那么总数是：

```text
a * b
```

例子：

```text
3 件上衣，4 条裤子
搭配数 = 3 * 4 = 12
```

代码：

```python
tops = 3
pants = 4

outfits = tops * pants

print(outfits)
```

结果：

```text
12
```

多步时继续相乘。

## 加法原则

如果两类情况互斥：

```text
情况 A 有 a 种
情况 B 有 b 种
```

那么总数是：

```text
a + b
```

互斥的意思是：

```text
一个结果不能同时属于 A 和 B
```

例子：

```text
从菜单中选一个主菜。
肉类 5 种，素类 3 种。
如果一个菜不能同时属于肉类和素类，总数 = 5 + 3 = 8。
```

如果类别有重叠，就不能简单相加，需要容斥。

## 排列 permutation

排列关注顺序。

从 `n` 个不同元素中选 `k` 个并排序：

```text
P(n, k) = n * (n-1) * ... * (n-k+1)
```

也可以写成：

```text
P(n, k) = n! / (n-k)!
```

例子：

```text
5 个人里选 3 个人站成一排
```

第一位 5 种，第二位 4 种，第三位 3 种：

```text
5 * 4 * 3 = 60
```

代码：

```python
import math

print(math.perm(5, 3))
```

结果：

```text
60
```

## 组合 combination

组合不关注顺序。

从 `n` 个不同元素中选 `k` 个：

```text
C(n, k) = n! / (k!(n-k)!)
```

例子：

```text
5 个人里选 3 个人组成小组
```

小组 `{A, B, C}` 和 `{C, B, A}` 是同一个结果。

所以是组合：

```python
import math

print(math.comb(5, 3))
```

结果：

```text
10
```

排列和组合的关系：

```text
P(n, k) = C(n, k) * k!
```

先选出 k 个，再给这 k 个排序。

## 顺序判断

遇到计数题，先问：

```text
顺序是否重要？
```

例子：

```text
从 10 只股票中选 3 只进入组合。
```

如果只是候选池：

```text
C(10, 3)
```

如果要排出第一、第二、第三优先级：

```text
P(10, 3)
```

代码：

```python
import math

portfolio_choices = math.comb(10, 3)
ranked_choices = math.perm(10, 3)

print(portfolio_choices)
print(ranked_choices)
```

结果：

```text
120
720
```

同样是“选 3 个”，是否有顺序会差很多。

## 可重复选择

如果每次选择后可以重复使用，情况不同。

例子：

```text
4 位数字密码，每位可以是 0-9，可重复。
```

每位 10 种：

```text
10^4 = 10000
```

```python
passwords = 10 ** 4

print(passwords)
```

结果：

```text
10000
```

如果不能重复，第一位 10 种，第二位 9 种，第三位 8 种，第四位 7 种：

```python
import math

print(math.perm(10, 4))
```

结果：

```text
5040
```

## 补集法

“至少一个”问题常用补集法。

例子：

```text
抛 5 次硬币，至少一次正面的概率是多少？
```

直接算：

```text
1 次正面 + 2 次正面 + ... + 5 次正面
```

很麻烦。

补集是：

```text
一次正面都没有
```

所以：

```text
P(至少一次正面) = 1 - P(全是反面)
              = 1 - (1/2)^5
              = 31/32
```

代码：

```python
p_at_least_one_head = 1 - (1 / 2) ** 5

print(p_at_least_one_head)
```

结果：

```text
0.96875
```

## 至少一个重复生日

经典生日问题：

```text
n 个人中，至少两个人生日相同的概率是多少？
```

用补集：

```text
1 - 所有人生日都不同的概率
```

假设一年 365 天，每天等概率，不考虑闰年。

所有生日不同：

```text
365/365 * 364/365 * ... * (365-n+1)/365
```

```python
def birthday_collision_prob(n, days=365):
    p_all_distinct = 1.0

    for i in range(n):
        p_all_distinct *= (days - i) / days

    return 1 - p_all_distinct

print(birthday_collision_prob(23))
```

结果约为：

```text
0.5072972343239854
```

23 个人时，重复生日概率已经超过 50%。

这类题的关键是：

```text
至少一个重复 = 1 - 全都不重复
```

## 二项计数

如果有 `n` 次独立试验，每次成功概率为 `p`。

恰好成功 `k` 次的概率：

```text
C(n, k) * p^k * (1-p)^(n-k)
```

例子：

```text
抛 10 次公平硬币，恰好 3 次正面。
```

```python
import math

p_exact_3_heads = math.comb(10, 3) * (0.5 ** 3) * (0.5 ** 7)

print(p_exact_3_heads)
```

结果：

```text
0.1171875
```

这里：

```text
C(10, 3)
```

表示选择哪 3 次是正面。

## 容斥原理

如果两个集合有重叠：

```text
|A union B| = |A| + |B| - |A intersection B|
```

三集合：

```text
|A union B union C|
= |A| + |B| + |C|
- |A∩B| - |A∩C| - |B∩C|
+ |A∩B∩C|
```

例子：

```text
1 到 100 中，能被 2 或 3 整除的数有多少个？
```

能被 2 整除：

```text
floor(100/2) = 50
```

能被 3 整除：

```text
floor(100/3) = 33
```

同时能被 2 和 3 整除，也就是能被 6 整除：

```text
floor(100/6) = 16
```

所以：

```text
50 + 33 - 16 = 67
```

代码：

```python
count = 100 // 2 + 100 // 3 - 100 // 6

print(count)
```

结果：

```text
67
```

## 分组计数

例子：

```text
8 个人分成 A、B 两组，每组 4 人，有多少种分法？
```

如果 A、B 组有标签：

```text
C(8, 4) = 70
```

选出 A 组，剩下自动是 B 组。

如果两组没有标签，只是分成两堆：

```text
C(8, 4) / 2 = 35
```

因为每种无标签分组被数了两次。

代码：

```python
import math

labeled_groups = math.comb(8, 4)
unlabeled_groups = labeled_groups // 2

print(labeled_groups)
print(unlabeled_groups)
```

结果：

```text
70
35
```

是否有标签是分组题的核心。

## 多重集合排列

如果有重复元素，排列数要除以重复阶乘。

例子：

```text
BANANA 有 6 个字母：
A 出现 3 次
N 出现 2 次
B 出现 1 次
```

不同排列数：

```text
6! / (3! * 2! * 1!) = 60
```

代码：

```python
import math

arrangements = math.factorial(6) // (
    math.factorial(3) * math.factorial(2) * math.factorial(1)
)

print(arrangements)
```

结果：

```text
60
```

如果把重复的 A 当成不同对象，会重复计数。

## 路径计数

从网格左下角走到右上角。

只能向右 `R` 或向上 `U`。

如果需要：

```text
3 次 R
2 次 U
```

总共 5 步。

只要选择哪 2 步是 `U`，或哪 3 步是 `R`：

```text
C(5, 2) = C(5, 3) = 10
```

代码：

```python
import math

paths = math.comb(5, 2)

print(paths)
```

结果：

```text
10
```

## 没有相邻的选择

经典题：

```text
从 10 个位置中选 3 个，要求没有两个相邻。
```

公式：

```text
C(n-k+1, k)
```

这里：

```text
n = 10, k = 3
C(8, 3) = 56
```

直觉：

先把 3 个选中位置放下，它们之间至少要有 2 个间隔。

等价于在压缩后的 `n-k+1` 个位置中选 `k` 个。

代码：

```python
import math

no_adjacent = math.comb(10 - 3 + 1, 3)

print(no_adjacent)
```

结果：

```text
56
```

小规模可以用枚举验证：

```python
from itertools import combinations

valid = []

for combo in combinations(range(10), 3):
    if all(combo[i + 1] - combo[i] > 1 for i in range(2)):
        valid.append(combo)

print(len(valid))
```

结果：

```text
56
```

## 抽牌例子

问题：

```text
5 张牌手牌中，恰好 2 张 A 的数量是多少？
```

一副牌：

```text
4 张 A
48 张非 A
```

恰好 2 张 A：

```text
C(4, 2) * C(48, 3)
```

```python
import math

hands = math.comb(4, 2) * math.comb(48, 3)

print(hands)
```

结果：

```text
103776
```

如果问概率，再除以所有 5 张手牌数：

```python
prob = hands / math.comb(52, 5)

print(prob)
```

结果约为：

```text
0.03992981808107859
```

## 分情况讨论

计数题有时需要拆情况。

例子：

```text
3 位数中，至少有一位是 7 的数字有多少个？
```

用补集更快。

所有 3 位数：

```text
900
```

没有 7 的 3 位数：

```text
百位不能是 0 或 7 -> 8 种
十位不能是 7 -> 9 种
个位不能是 7 -> 9 种
```

所以：

```text
900 - 8 * 9 * 9 = 252
```

代码：

```python
count = 900 - 8 * 9 * 9

print(count)
```

结果：

```text
252
```

直接分“一个 7、两个 7、三个 7”也可以，但更容易漏情况。

## 量化例子：组合数量

从 500 只股票里选 20 只等权组成组合，可能组合数量是：

```python
import math

num_portfolios = math.comb(500, 20)

print(num_portfolios)
```

这是一个非常大的数。

这说明：

```text
穷举所有组合通常不可行
```

实际投资组合构建需要优化方法、启发式搜索或约束规划，而不是枚举所有组合。

## 常见错误

### 错误 1：排列和组合混用

如果顺序不重要，用组合。

如果顺序重要，用排列。

把 `{A, B, C}` 和 `{C, B, A}` 算成不同结果，会多算。

### 错误 2：忘记是否允许重复

密码每位数字是否可重复，会直接改变答案。

```text
可重复：10^4
不可重复：P(10,4)
```

### 错误 3：类别重叠却直接相加

如果集合有交集，要用容斥。

否则交集会被重复计数。

### 错误 4：无标签分组多算

把 8 人分成两组，如果两组无标签，`C(8,4)` 会把每种分法数两次。

要除以 `2!`。

### 错误 5：至少一个问题不用补集

“至少一个”直接分情况往往容易漏。

先考虑：

```text
1 - 一个都没有
```

## 解题步骤

计数题可以按这个流程：

1. 明确对象是否不同。
2. 判断顺序是否重要。
3. 判断是否允许重复。
4. 如果有“至少一个”，先想补集。
5. 如果有重叠类别，用容斥。
6. 如果有分组，判断组是否有标签。
7. 如果有限制条件，考虑先排基本结构，再插空或压缩。
8. 小规模时用枚举做 sanity check。

## 记忆要点

- 乘法原则用于连续步骤。
- 加法原则要求情况互斥。
- 排列关注顺序，组合不关注顺序。
- 可重复和不可重复是两类问题。
- “至少一个”常用补集法。
- 重叠集合要用容斥。
- 无标签分组要除掉组之间的重复计数。
- 有重复元素的排列要除以重复元素的阶乘。
- 没有相邻选择常用 `C(n-k+1, k)`。
- 复杂计数题先定义样本空间，再分解限制。

## 自测题

1. `P(n,k)` 和 `C(n,k)` 的区别是什么？
2. 什么时候应该用补集法？
3. 为什么两个集合计数相加时要减去交集？
4. 8 人分成两个无标签 4 人组，为什么要除以 2？
5. 从 10 个位置选 3 个且不相邻，为什么答案是 `C(8,3)`？
