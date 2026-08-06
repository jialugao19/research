# Brain Teaser / Green Book：条件概率的基本公式、树状分解和面试题应用

## 核心概念

条件概率回答的问题是：

```text
在已知 B 发生的条件下，A 发生的概率是多少？
```

记作：

```text
P(A | B)
```

读作：

```text
given B, probability of A
```

定义公式：

```text
P(A | B) = P(A and B) / P(B)
```

前提是：

```text
P(B) > 0
```

直觉上，条件概率是在缩小样本空间。

原来样本空间是所有可能结果。

已知 `B` 发生后，样本空间只剩下 `B` 里面的结果。

然后再看其中有多少也属于 `A`。

## 一个最小例子

掷一枚公平骰子。

事件：

```text
A = 点数是偶数 = {2, 4, 6}
B = 点数大于 3 = {4, 5, 6}
```

那么：

```text
A and B = {4, 6}
```

所以：

```text
P(A | B) = P(A and B) / P(B)
         = (2/6) / (3/6)
         = 2/3
```

用 Python 验证：

```python
outcomes = {1, 2, 3, 4, 5, 6}

A = {2, 4, 6}
B = {4, 5, 6}

p_a_given_b = len(A & B) / len(B)

print(p_a_given_b)
```

结果：

```text
0.6666666666666666
```

## 乘法公式

由条件概率定义可得：

```text
P(A and B) = P(A | B) * P(B)
```

也可以写成：

```text
P(A and B) = P(B | A) * P(A)
```

这是很多题目的核心。

例如：

```text
P(先抽到红球，再抽到红球)
= P(第一次红) * P(第二次红 | 第一次红)
```

条件会改变第二步概率。

## 树状分解

条件概率题常用 probability tree。

例如一个信号系统：

```text
市场上涨概率 P(up) = 0.6
市场下跌概率 P(down) = 0.4

上涨时信号为正 P(signal+ | up) = 0.7
下跌时信号为正 P(signal+ | down) = 0.2
```

联合概率：

```text
P(up and signal+) = 0.6 * 0.7 = 0.42
P(down and signal+) = 0.4 * 0.2 = 0.08
```

所以：

```text
P(signal+) = 0.42 + 0.08 = 0.50
```

代码：

```python
p_up = 0.6
p_down = 0.4
p_signal_given_up = 0.7
p_signal_given_down = 0.2

p_up_and_signal = p_up * p_signal_given_up
p_down_and_signal = p_down * p_signal_given_down
p_signal = p_up_and_signal + p_down_and_signal

print(p_up_and_signal)
print(p_down_and_signal)
print(p_signal)
```

结果：

```text
0.42
0.08000000000000002
0.5
```

浮点数显示 `0.08000000000000002` 是二进制浮点表示误差。

数学上就是 `0.08`。

## 全概率公式

如果 `B1, B2, ..., Bn` 构成互斥且完备的分组，那么：

```text
P(A) = sum_i P(A | Bi) * P(Bi)
```

这叫全概率公式。

上面的信号例子就是：

```text
P(signal+) =
P(signal+ | up) * P(up)
+ P(signal+ | down) * P(down)
```

条件概率题里，经常先用全概率公式算分母。

## 反向条件概率

很多题目会给：

```text
P(signal+ | up)
```

但问：

```text
P(up | signal+)
```

这两个不一样。

用前面的数：

```text
P(up | signal+) = P(up and signal+) / P(signal+)
                = 0.42 / 0.50
                = 0.84
```

代码：

```python
p_up_given_signal = p_up_and_signal / p_signal

print(p_up_given_signal)
```

结果：

```text
0.84
```

这就是后面“贝叶斯”章节会系统讲的方向反转。

本篇先记住：

```text
P(A | B) 不等于 P(B | A)
```

## 独立性

如果 `A` 和 `B` 独立，那么：

```text
P(A | B) = P(A)
```

也等价于：

```text
P(A and B) = P(A) * P(B)
```

例子：

```text
A = 第一枚硬币正面
B = 第二枚硬币正面
```

两次抛硬币独立。

```text
P(A | B) = P(A) = 1/2
P(A and B) = 1/2 * 1/2 = 1/4
```

但是注意：

```text
互斥不等于独立
```

如果 `A` 和 `B` 互斥，且二者概率都大于 0：

```text
P(A and B) = 0
P(A) * P(B) > 0
```

所以它们不是独立。

## 面试常见误区：条件改变样本空间

题目：

```text
从一副普通扑克牌中抽一张。
A = 抽到 A
B = 抽到黑桃
问 P(A | B)
```

普通 52 张牌。

已知是黑桃后，样本空间只剩 13 张黑桃。

其中只有 1 张黑桃 A。

所以：

```text
P(A | B) = 1/13
```

不是：

```text
4/52
```

虽然 `4/52` 也等于 `1/13`，但推理方式要正确。

换一个条件就不一定碰巧一样。

## 不放回抽样

袋子里有：

```text
3 个红球
2 个蓝球
```

不放回抽两次。

问：

```text
两次都是红球的概率是多少？
```

计算：

```text
P(第一次红) = 3/5
P(第二次红 | 第一次红) = 2/4

P(两次红) = 3/5 * 2/4 = 3/10
```

代码：

```python
p_two_red = (3 / 5) * (2 / 4)

print(p_two_red)
```

结果：

```text
0.3
```

如果是放回抽样，第二次概率仍是 `3/5`。

所以放回和不放回一定要分清。

## 至少一个问题

经典题型：

```text
一个家庭有两个孩子。
已知至少一个是女孩。
问两个都是女孩的概率是多少？
```

假设：

```text
每个孩子男/女概率相同
出生顺序可区分
```

样本空间：

```text
BB, BG, GB, GG
```

已知至少一个是女孩，排除 `BB`。

剩下：

```text
BG, GB, GG
```

其中两个都是女孩只有：

```text
GG
```

所以答案：

```text
1/3
```

代码：

```python
families = {"BB", "BG", "GB", "GG"}

at_least_one_girl = {x for x in families if "G" in x}
two_girls = {"GG"}

answer = len(at_least_one_girl & two_girls) / len(at_least_one_girl)

print(answer)
```

结果：

```text
0.3333333333333333
```

## “随机遇到一个女孩”不是同一道题

如果题目改成：

```text
随机从所有有两个孩子的家庭中，随机遇到其中一个孩子，发现她是女孩。
问这个家庭两个都是女孩的概率？
```

这时抽样机制变了。

家庭 `GG` 有两个女孩，更容易被“随机遇到一个女孩”观察到。

用加权计数：

```python
families = ["BB", "BG", "GB", "GG"]

observations = []

for family in families:
    for child in family:
        if child == "G":
            observations.append(family)

prob = observations.count("GG") / len(observations)

print(observations)
print(prob)
```

结果：

```text
['BG', 'GB', 'GG', 'GG']
0.5
```

这个答案是 `1/2`。

所以条件概率题里最重要的是：

```text
条件是怎么被观察到的？
样本空间到底是什么？
```

## 混淆矩阵例子

假设一个模型预测上涨。

定义：

```text
U = 实际上涨
S = 模型发出上涨信号
```

给定：

```text
P(U) = 0.55
P(S | U) = 0.60
P(S | not U) = 0.40
```

求：

```text
P(U | S)
```

先算：

```text
P(S) = P(S|U)P(U) + P(S|not U)P(not U)
     = 0.60 * 0.55 + 0.40 * 0.45
     = 0.51
```

再算：

```text
P(U | S) = P(S|U)P(U) / P(S)
         = 0.33 / 0.51
         = 0.6470588235
```

代码：

```python
p_up = 0.55
p_signal_given_up = 0.60
p_signal_given_not_up = 0.40

p_signal = (
    p_signal_given_up * p_up
    + p_signal_given_not_up * (1 - p_up)
)
p_up_given_signal = p_signal_given_up * p_up / p_signal

print(p_signal)
print(p_up_given_signal)
```

结果：

```text
0.51
0.6470588235294118
```

这说明：

```text
模型在上涨时 60% 发信号
不代表发信号后上涨概率就是 60%
```

后者还取决于基础上涨概率和下跌时误报率。

## 频率表做法

面试中，如果概率公式容易混乱，可以先构造 1000 个样本的频率表。

继续上面的例子：

```text
1000 天
上涨 550 天
不上涨 450 天

上涨时发信号 60% -> 330 天
不上涨时发信号 40% -> 180 天
发信号共 510 天
```

所以：

```text
P(up | signal) = 330 / 510 = 0.6471
```

代码：

```python
total_days = 1000
up_days = 550
not_up_days = 450

signal_and_up = up_days * 0.60
signal_and_not_up = not_up_days * 0.40
signal_days = signal_and_up + signal_and_not_up

print(signal_and_up / signal_days)
```

结果：

```text
0.6470588235294118
```

频率表的好处是：

- 不容易把方向写反。
- 更适合心算。
- 面试解释更清楚。

## 条件概率和相关性

条件概率也能帮助理解“条件下的分布变化”。

例如：

```text
P(大跌 | 高波动)
P(大跌 | 低波动)
```

如果两者明显不同，说明高波动环境改变了大跌概率。

但要小心：

- 条件样本可能很少。
- 条件可能和未来信息有关。
- 条件定义可能是事后才知道的。
- 相关不代表因果。

在回测中，如果条件使用了未来信息，就会产生泄露。

## 常见错误

### 错误 1：把 P(A | B) 当成 P(B | A)

这是最常见错误。

例如：

```text
P(发信号 | 上涨) 不等于 P(上涨 | 发信号)
```

要反过来，通常需要全概率公式或贝叶斯公式。

### 错误 2：条件样本空间没改

已知 `B` 发生后，样本空间变成 `B`。

不要还在原始样本空间里数。

### 错误 3：忽略抽样机制

“至少一个是女孩”和“随机遇到一个女孩”不是同一道题。

观察条件是怎么产生的，会改变概率。

### 错误 4：把互斥当独立

如果两个正概率事件互斥，它们通常不是独立。

因为一个发生会让另一个发生概率变成 0。

### 错误 5：忘记基础概率

模型准确率、信号命中率、疾病检测题里，基础概率很关键。

低基础概率事件即使有较好的检测信号，反向条件概率也可能不高。

## 解题步骤

条件概率题可以按下面流程：

1. 定义事件 `A`、`B`。
2. 明确题目问的是 `P(A | B)` 还是 `P(B | A)`。
3. 写出条件后的样本空间。
4. 如果有多条路径，用树状图列联合概率。
5. 用全概率公式算分母。
6. 必要时用频率表做 sanity check。

## 记忆要点

- `P(A | B) = P(A and B) / P(B)`。
- 条件概率本质是缩小样本空间。
- `P(A | B)` 通常不等于 `P(B | A)`。
- 乘法公式：`P(A and B) = P(A | B)P(B)`。
- 全概率公式用于把多个路径加总。
- 独立表示 `P(A | B) = P(A)`。
- 互斥不等于独立。
- 条件概率题要特别注意抽样机制。
- 频率表是面试中非常稳的解题工具。

## 自测题

1. 条件概率 `P(A | B)` 的定义是什么？
2. 为什么 `P(A | B)` 一般不等于 `P(B | A)`？
3. “至少一个孩子是女孩”和“随机遇到一个女孩”为什么答案不同？
4. 独立和互斥有什么区别？
5. 模型给出上涨信号后，为什么上涨概率不只取决于 `P(signal | up)`？
