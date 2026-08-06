# Bayes' Theorem

## 核心概念

贝叶斯公式用于把条件概率反过来。

如果你知道：

```text
P(B | A)
```

但想求：

```text
P(A | B)
```

就需要贝叶斯公式：

```text
P(A | B) = P(B | A) * P(A) / P(B)
```

其中：

```text
P(A)      prior，先验概率
P(B | A)  likelihood，似然
P(B)      evidence，证据概率
P(A | B)  posterior，后验概率
```

直觉：

```text
先有一个基础判断 prior
看到新证据 B
用证据更新判断，得到 posterior
```

在面试题中，贝叶斯最常见的陷阱是：

```text
忽略基础率 base rate
把 P(B | A) 错当成 P(A | B)
```

## 从条件概率推导

由乘法公式：

```text
P(A and B) = P(A | B)P(B)
P(A and B) = P(B | A)P(A)
```

两边相等：

```text
P(A | B)P(B) = P(B | A)P(A)
```

所以：

```text
P(A | B) = P(B | A)P(A) / P(B)
```

这里的分母 `P(B)` 常常用全概率公式算：

```text
P(B) = P(B | A)P(A) + P(B | not A)P(not A)
```

二分类场景里，最常用的形式是：

```text
P(A | B) =
P(B | A)P(A)
/
[P(B | A)P(A) + P(B | not A)P(not A)]
```

## 疾病检测题

经典题：

```text
某疾病在人群中的患病率是 1%。
检测灵敏度 99%：患病者检测阳性的概率是 99%。
检测假阳性率 5%：未患病者检测阳性的概率是 5%。
一个人检测阳性，问他真的患病的概率是多少？
```

定义：

```text
D = 患病
T = 检测阳性
```

已知：

```text
P(D) = 0.01
P(T | D) = 0.99
P(T | not D) = 0.05
```

要求：

```text
P(D | T)
```

计算：

```text
P(T) = P(T|D)P(D) + P(T|not D)P(not D)
     = 0.99 * 0.01 + 0.05 * 0.99
     = 0.0594

P(D|T) = 0.99 * 0.01 / 0.0594
       = 0.166666...
```

检测阳性后，真的患病概率只有约 `16.7%`。

这不是因为检测差，而是因为疾病本身很少见，假阳性人数会很多。

代码：

```python
p_disease = 0.01
p_positive_given_disease = 0.99
p_positive_given_no_disease = 0.05

p_positive = (
    p_positive_given_disease * p_disease
    + p_positive_given_no_disease * (1 - p_disease)
)
p_disease_given_positive = (
    p_positive_given_disease * p_disease / p_positive
)

print(p_positive)
print(p_disease_given_positive)
```

结果：

```text
0.0594
0.16666666666666669
```

## 频率表解法

面试中，频率表通常比公式更稳。

假设有 10000 人。

```text
患病 1% -> 100 人
未患病 -> 9900 人

患病者阳性 99% -> 99 人
未患病者假阳性 5% -> 495 人

阳性总数 = 99 + 495 = 594
真患病且阳性 = 99
```

所以：

```text
P(D | T) = 99 / 594 = 16.67%
```

代码：

```python
total = 10000
disease = total * 0.01
no_disease = total - disease

true_positive = disease * 0.99
false_positive = no_disease * 0.05

posterior = true_positive / (true_positive + false_positive)

print(posterior)
```

结果：

```text
0.16666666666666666
```

频率表的优点：

- 不容易把方向写反。
- 更容易心算。
- 能直观看到基础率影响。

## 基础率 base rate

基础率是事件本来发生的概率。

在上面的例子中：

```text
P(D) = 1%
```

就是基础率。

很多人看到：

```text
检测灵敏度 99%
```

就误以为阳性后患病概率接近 99%。

这是忽略了基础率。

如果疾病基础率变成 50%，同样检测参数下：

```python
def posterior_positive(prior, sensitivity, false_positive_rate):
    p_positive = (
        sensitivity * prior
        + false_positive_rate * (1 - prior)
    )
    return sensitivity * prior / p_positive

print(posterior_positive(0.01, 0.99, 0.05))
print(posterior_positive(0.50, 0.99, 0.05))
```

结果：

```text
0.16666666666666669
0.9519230769230769
```

同样的检测，基础率不同，后验概率差很多。

## 交易信号例子

定义：

```text
U = 明天上涨
S = 因子发出正信号
```

假设：

```text
P(U) = 0.52
P(S | U) = 0.60
P(S | not U) = 0.45
```

求：

```text
P(U | S)
```

计算：

```python
p_up = 0.52
p_signal_given_up = 0.60
p_signal_given_down = 0.45

p_signal = (
    p_signal_given_up * p_up
    + p_signal_given_down * (1 - p_up)
)
p_up_given_signal = p_signal_given_up * p_up / p_signal

print(p_signal)
print(p_up_given_signal)
```

结果：

```text
0.528
0.5909090909090908
```

解释：

```text
信号在上涨日出现概率是 60%
但看到信号后，上涨概率是 59.09%
```

这两个方向不同。

后验概率还取决于：

- 上涨基础率。
- 下跌时误报率。
- 信号整体出现频率。

## 多种状态的贝叶斯

如果市场有多个状态：

```text
bull
flat
bear
```

且观察到一个信号 `S`，可以对每个状态计算后验概率：

```text
P(state | S) = P(S | state)P(state) / P(S)
```

其中：

```text
P(S) = sum_state P(S | state)P(state)
```

例子：

```python
priors = {
    "bull": 0.30,
    "flat": 0.50,
    "bear": 0.20,
}

likelihood = {
    "bull": 0.70,
    "flat": 0.40,
    "bear": 0.20,
}

evidence = sum(likelihood[state] * priors[state] for state in priors)
posterior = {
    state: likelihood[state] * priors[state] / evidence
    for state in priors
}

print(evidence)
print(posterior)
print(sum(posterior.values()))
```

结果：

```text
0.45
{'bull': 0.4666666666666666, 'flat': 0.4444444444444445, 'bear': 0.08888888888888889}
1.0
```

观察到信号后，`bull` 的概率从 `30%` 上升到约 `46.7%`。

`bear` 的概率从 `20%` 下降到约 `8.9%`。

## 连续更新

贝叶斯可以连续更新。

```text
prior -> 看到证据 1 -> posterior 1
posterior 1 作为新的 prior
看到证据 2 -> posterior 2
```

简单例子：

```python
def bayes_update(prior, likelihood_true, likelihood_false):
    evidence = (
        likelihood_true * prior
        + likelihood_false * (1 - prior)
    )
    return likelihood_true * prior / evidence

prior = 0.10

after_signal_1 = bayes_update(prior, 0.80, 0.20)
after_signal_2 = bayes_update(after_signal_1, 0.70, 0.30)

print(after_signal_1)
print(after_signal_2)
```

结果：

```text
0.30769230769230776
0.5090909090909091
```

第一个证据把概率从 `10%` 提高到约 `30.8%`。

第二个证据继续提高到约 `50.9%`。

前提是你接受这两个证据在给定真假状态后可以这样独立更新。

如果证据高度相关，连续更新会重复计算信息。

## odds 形式

贝叶斯也可以用 odds 表示。

概率 `p` 对应 odds：

```text
odds = p / (1 - p)
```

贝叶斯更新：

```text
posterior odds = prior odds * likelihood ratio
```

其中：

```text
likelihood ratio = P(E | H) / P(E | not H)
```

例子：

```python
prior = 0.10
likelihood_true = 0.80
likelihood_false = 0.20

prior_odds = prior / (1 - prior)
likelihood_ratio = likelihood_true / likelihood_false
posterior_odds = prior_odds * likelihood_ratio
posterior = posterior_odds / (1 + posterior_odds)

print(prior_odds)
print(likelihood_ratio)
print(posterior)
```

结果：

```text
0.11111111111111112
4.0
0.3076923076923077
```

这和前面 `bayes_update(0.10, 0.80, 0.20)` 的结果一致。

odds 形式适合快速理解：

```text
证据让 odds 乘上多少倍
```

## 垃圾邮件过滤例子

假设：

```text
P(spam) = 0.20
P(word="free" | spam) = 0.60
P(word="free" | not spam) = 0.05
```

收到一封邮件，里面有 `free`。

求：

```text
P(spam | free)
```

```python
p_spam = 0.20
p_free_given_spam = 0.60
p_free_given_not_spam = 0.05

p_free = (
    p_free_given_spam * p_spam
    + p_free_given_not_spam * (1 - p_spam)
)
p_spam_given_free = p_free_given_spam * p_spam / p_free

print(p_spam_given_free)
```

结果：

```text
0.7499999999999999
```

一个词就把 spam 概率从 `20%` 提高到了 `75%`。

真实朴素贝叶斯会使用多个特征，并做平滑处理。

这里主要看公式方向。

## Green Book 风格心算

贝叶斯题如果数字复杂，可以换成频率表。

例子：

```text
基础率 2%
命中率 90%
误报率 10%
检测阳性后概率？
```

用 1000 人：

```text
患病 20 人 -> 阳性 18 人
未患病 980 人 -> 假阳性 98 人
阳性总数 116 人
真阳性 18 人
概率 18 / 116 = 15.5%
```

代码：

```python
posterior = (20 * 0.90) / (20 * 0.90 + 980 * 0.10)

print(posterior)
```

结果：

```text
0.15517241379310345
```

这比直接套公式更适合口算。

## 贝叶斯和校准

模型输出一个概率时，你关心的是：

```text
模型说 70% 的样本里，实际发生频率是否接近 70%
```

这叫 calibration，校准。

贝叶斯思维提醒你：

- 后验概率不是单看信号强度。
- 它还依赖基础率。
- 不同 regime 下基础率可能不同。
- 信号在不同条件下的误报率也可能不同。

例如同一个交易信号：

```text
高波动 regime 下 P(up) 可能不同
低波动 regime 下 P(up) 可能不同
```

如果你把所有状态混在一起，后验概率可能不稳定。

## 常见错误

### 错误 1：忽略基础率

检测很准，不代表阳性后目标事件概率很高。

如果目标事件极少见，假阳性可能占阳性样本的大多数。

### 错误 2：把灵敏度当后验概率

```text
P(positive | disease) 不等于 P(disease | positive)
```

模型信号里也是：

```text
P(signal | up) 不等于 P(up | signal)
```

### 错误 3：分母漏掉反例路径

分母是证据发生的总概率。

二分类时：

```text
P(B) = P(B|A)P(A) + P(B|not A)P(not A)
```

漏掉假阳性路径会严重高估后验。

### 错误 4：连续更新时重复计算相关证据

两个信号如果高度相关，把它们当独立证据连续更新，会让后验过度自信。

### 错误 5：把先验当固定真理

先验是当前信息下的基础判断。

不同样本、不同 regime、不同时间段，先验可能变化。

## 解题步骤

贝叶斯题可以按这个流程：

1. 定义假设 `H` 和证据 `E`。
2. 写出要求的是 `P(H | E)`。
3. 找到先验 `P(H)`。
4. 找到似然 `P(E | H)` 和误报路径 `P(E | not H)`。
5. 用全概率公式算 `P(E)`。
6. 代入贝叶斯公式。
7. 用频率表做 sanity check。

## 记忆要点

- 贝叶斯公式：`P(H|E)=P(E|H)P(H)/P(E)`。
- 分母 `P(E)` 是证据发生的总概率。
- 二分类分母通常包含真阳性路径和假阳性路径。
- 基础率会强烈影响后验概率。
- `P(E|H)` 不是 `P(H|E)`。
- 频率表是贝叶斯题的稳健解法。
- odds 形式是 `posterior odds = prior odds * likelihood ratio`。
- 连续更新要小心证据相关性。
- 交易信号的后验概率取决于基础上涨概率和误报率。

## 自测题

1. 贝叶斯公式是什么？每一项分别代表什么？
2. 为什么检测灵敏度 99% 不代表阳性后患病概率 99%？
3. 二分类贝叶斯题的分母通常由哪两条路径组成？
4. odds 形式下，证据如何更新先验？
5. 为什么多个相关信号不能简单当成独立证据连续更新？
