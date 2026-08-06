# 86. Brain Teaser / Green Book：期望的线性性、条件期望和常见面试题应用

## 核心概念

期望 expectation 是随机变量的平均值。

如果随机变量 `X` 可能取值：

```text
x1, x2, ..., xn
```

对应概率：

```text
p1, p2, ..., pn
```

那么：

```text
E[X] = x1*p1 + x2*p2 + ... + xn*pn
```

也就是：

```text
每个结果 * 它发生的概率，然后加总
```

期望不是“最可能的值”。

它是长期平均值。

## 骰子期望

公平六面骰子的点数 `X`：

```text
1, 2, 3, 4, 5, 6
```

每个概率都是 `1/6`。

所以：

```text
E[X] = (1 + 2 + 3 + 4 + 5 + 6) / 6 = 3.5
```

代码：

```python
outcomes = [1, 2, 3, 4, 5, 6]
expected = sum(outcomes) / len(outcomes)

print(expected)
```

结果：

```text
3.5
```

注意骰子永远不会掷出 `3.5`。

但长期平均点数会接近 `3.5`。

## 一般离散期望

假设一笔交易的收益 `X` 有三种可能：

```text
+10，概率 0.2
  0，概率 0.5
 -5，概率 0.3
```

期望收益：

```text
E[X] = 10 * 0.2 + 0 * 0.5 + (-5) * 0.3
     = 2 - 1.5
     = 0.5
```

代码：

```python
outcomes = [10, 0, -5]
probs = [0.2, 0.5, 0.3]

expected_pnl = sum(x * p for x, p in zip(outcomes, probs))

print(expected_pnl)
```

结果：

```text
0.5
```

如果交易成本是 `0.8`，净期望就是：

```text
0.5 - 0.8 = -0.3
```

所以正的毛期望不一定代表策略可交易。

## 期望的线性性

期望最重要的性质：

```text
E[X + Y] = E[X] + E[Y]
```

不要求 `X` 和 `Y` 独立。

也有：

```text
E[aX + b] = aE[X] + b
```

这是 Green Book / brain teaser 里非常常用的技巧。

例如两个骰子点数之和：

```text
E[dice1 + dice2] = E[dice1] + E[dice2] = 3.5 + 3.5 = 7
```

代码：

```python
expected_two_dice = 3.5 + 3.5

print(expected_two_dice)
```

结果：

```text
7.0
```

## 线性性不需要独立

假设：

```text
Y = 2X
```

显然 `X` 和 `Y` 不独立。

但仍然：

```text
E[X + Y] = E[X] + E[Y]
```

例子：

```python
xs = [1, 2, 3]
probs = [1/3, 1/3, 1/3]

expected_x = sum(x * p for x, p in zip(xs, probs))
expected_y = sum((2 * x) * p for x, p in zip(xs, probs))
expected_x_plus_y = sum((x + 2 * x) * p for x, p in zip(xs, probs))

print(expected_x)
print(expected_y)
print(expected_x_plus_y)
```

结果：

```text
2.0
4.0
6.0
```

`6.0 = 2.0 + 4.0`。

## 指示变量

指示变量 indicator 是只取 0 或 1 的随机变量。

例如：

```text
I = 1 表示事件 A 发生
I = 0 表示事件 A 不发生
```

那么：

```text
E[I] = P(A)
```

因为：

```text
E[I] = 1 * P(A) + 0 * P(not A) = P(A)
```

这让很多计数问题变简单。

## 例子：硬币正面个数

抛 10 次公平硬币，问正面个数的期望。

令：

```text
Ii = 第 i 次是否正面
```

正面总数：

```text
X = I1 + I2 + ... + I10
```

每个：

```text
E[Ii] = 1/2
```

所以：

```text
E[X] = 10 * 1/2 = 5
```

代码：

```python
n = 10
p_head = 0.5

expected_heads = n * p_head

print(expected_heads)
```

结果：

```text
5.0
```

## 例子：抽牌中 A 的数量

从 52 张牌中不放回抽 5 张，问抽到 A 的数量期望。

直接算分布比较麻烦。

用指示变量：

```text
Ii = 第 i 张 A 是否被抽中
```

一副牌有 4 张 A。

每张 A 被包含在 5 张手牌中的概率：

```text
5 / 52
```

所以 A 的数量期望：

```text
4 * 5/52 = 20/52 = 5/13
```

代码：

```python
expected_aces = 4 * 5 / 52

print(expected_aces)
```

结果：

```text
0.38461538461538464
```

这里不需要计算抽到 0、1、2、3、4 张 A 的概率。

## 条件期望

条件期望是：

```text
E[X | A]
```

意思是：

```text
在 A 发生的条件下，X 的平均值
```

例子：骰子已知点数大于 3，问点数期望。

条件样本空间：

```text
{4, 5, 6}
```

所以：

```text
E[X | X > 3] = (4 + 5 + 6) / 3 = 5
```

代码：

```python
outcomes = [1, 2, 3, 4, 5, 6]
conditioned = [x for x in outcomes if x > 3]

expected_given_gt3 = sum(conditioned) / len(conditioned)

print(expected_given_gt3)
```

结果：

```text
5.0
```

条件期望和条件概率一样，关键是先改变样本空间。

## 全期望公式

如果事件 `A` 和 `not A` 把样本空间分成两块：

```text
E[X] = E[X | A]P(A) + E[X | not A]P(not A)
```

更一般地：

```text
E[X] = sum_i E[X | Bi]P(Bi)
```

例子：

```text
市场上涨概率 0.6，平均收益 +2
市场下跌概率 0.4，平均收益 -3
```

总期望：

```text
E[R] = 2 * 0.6 + (-3) * 0.4 = 0
```

代码：

```python
expected_return = 2 * 0.6 + (-3) * 0.4

print(round(expected_return, 10))
```

结果：

```text
0.0
```

## 几何分布等待时间

经典题：

```text
不断抛公平硬币，直到第一次出现正面。
问期望抛几次？
```

每次成功概率：

```text
p = 1/2
```

几何分布等待时间期望：

```text
E[T] = 1 / p = 2
```

更一般地，如果每次独立尝试成功概率为 `p`：

```text
期望等待次数 = 1 / p
```

代码：

```python
p = 0.5
expected_wait = 1 / p

print(expected_wait)
```

结果：

```text
2.0
```

如果某信号每天触发概率是 `5%`，独立近似下期望等待：

```text
1 / 0.05 = 20 天
```

## 用递推解等待时间

同一个硬币题也可以用递推。

设期望等待次数为 `E`。

第一次抛：

- 正面，概率 `1/2`，总次数 1。
- 反面，概率 `1/2`，已经用 1 次，还要重新等 `E` 次。

所以：

```text
E = 1/2 * 1 + 1/2 * (1 + E)
```

化简：

```text
E = 1 + E/2
E = 2
```

递推法适合处理更复杂的等待题。

## 公平价格

如果一个游戏的随机收益是 `X`，公平价格是：

```text
E[X]
```

例子：

```text
掷一个骰子。
掷到 6 赢 12 元，否则赢 0 元。
这个游戏公平价格是多少？
```

期望收益：

```text
12 * 1/6 + 0 * 5/6 = 2
```

所以公平价格是 2 元。

如果入场费低于 2，期望正。

如果入场费高于 2，期望负。

代码：

```python
fair_price = 12 * (1 / 6)

print(fair_price)
```

结果：

```text
2.0
```

## 期望不等于风险

两个游戏：

```text
A: 稳定获得 1
B: 50% 获得 3，50% 亏 1
```

B 的期望：

```text
3 * 0.5 + (-1) * 0.5 = 1
```

A 和 B 期望相同。

但风险不同。

代码：

```python
expected_a = 1
expected_b = 3 * 0.5 + (-1) * 0.5

print(expected_a)
print(expected_b)
```

结果：

```text
1
1.0
```

在投资里，不能只看期望，还要看波动、回撤、容量、交易成本和尾部风险。

## 线性性面试题：帽子问题

题目：

```text
n 个人随机拿 n 顶帽子。
问拿到自己帽子的人数期望。
```

令：

```text
Ii = 第 i 个人是否拿到自己的帽子
```

那么：

```text
P(Ii = 1) = 1/n
E[Ii] = 1/n
```

总人数：

```text
X = I1 + I2 + ... + In
```

所以：

```text
E[X] = n * 1/n = 1
```

不管 `n` 多大，期望都是 1。

代码：

```python
def expected_matching_hats(n):
    return n * (1 / n)

print(expected_matching_hats(10))
print(expected_matching_hats(100))
```

结果：

```text
1.0
1.0
```

这题的关键是线性性，不需要算复杂排列分布。

## 量化例子：信号条件收益

假设你估计：

```text
P(signal) = 0.3
E[return | signal] = 0.002
E[return | no signal] = -0.0002
```

总体期望收益：

```text
E[return] =
0.002 * 0.3 + (-0.0002) * 0.7
= 0.00046
```

代码：

```python
p_signal = 0.3
expected_given_signal = 0.002
expected_given_no_signal = -0.0002

overall_expected_return = (
    expected_given_signal * p_signal
    + expected_given_no_signal * (1 - p_signal)
)

print(overall_expected_return)
```

结果：

```text
0.00046
```

如果每次交易成本是 `0.0006`，净期望为负。

所以条件收益看起来不错，也要乘上触发概率并扣成本。

## 常见错误

### 错误 1：把期望当最可能结果

骰子期望是 `3.5`，但不会出现 `3.5`。

期望是长期平均，不是最可能结果。

### 错误 2：以为线性性需要独立

`E[X + Y] = E[X] + E[Y]` 总是成立，只要期望存在。

独立性是方差、乘积期望等问题里更常出现的条件。

### 错误 3：忘记交易成本

策略毛期望为正，不代表净期望为正。

交易成本、滑点、冲击成本会改变期望。

### 错误 4：条件期望样本空间没变

算 `E[X | A]` 时，要只在条件 `A` 的样本空间里平均。

### 错误 5：只看期望不看分布

同样期望的两个策略，风险可能完全不同。

面试中回答公平价格可以只用期望。

投资中不能只用期望做决策。

## 解题步骤

期望题可以按下面流程：

1. 明确随机变量是什么。
2. 列出可能取值和概率。
3. 能直接算就用 `sum(value * prob)`。
4. 看到“总数”问题，优先考虑指示变量。
5. 看到分情形，考虑全期望公式。
6. 看到“直到第一次成功”，考虑几何分布或递推。
7. 最后检查期望是否需要扣成本或考虑风险。

## 记忆要点

- 期望是长期平均值，不一定是可能出现的值。
- 离散期望是 `sum(value * probability)`。
- 期望线性性：`E[X+Y]=E[X]+E[Y]`。
- 线性性不要求独立。
- 指示变量的期望等于事件概率。
- 条件期望要改变样本空间。
- 全期望公式按条件分组加权平均。
- 几何分布等待时间是 `1/p`。
- 公平价格等于期望收益。
- 期望不等于风险，投资场景要看分布和成本。

## 自测题

1. 骰子点数的期望为什么是 3.5？
2. 期望线性性是否要求随机变量独立？
3. 为什么指示变量的期望等于事件概率？
4. 抛公平硬币直到第一次正面，期望等待次数是多少？
5. 为什么两个策略期望相同但风险可能不同？
