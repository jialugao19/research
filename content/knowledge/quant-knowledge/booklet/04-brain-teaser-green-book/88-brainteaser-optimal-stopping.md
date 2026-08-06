# 88. Brain Teaser / Green Book：optimal stopping 的阈值策略、秘书问题和停止规则应用

## 核心概念

optimal stopping 是最优停止问题。

它回答的问题是：

```text
现在停，还是继续等？
```

典型场景：

- 现在接受 offer，还是等下一个。
- 现在卖出资产，还是继续持有。
- 看到当前候选人，是否录用。
- 当前价格是否触发止盈或止损。
- 当前信号是否足够强，还是继续观察。

最优停止的核心权衡：

```text
停止：锁定当前收益，放弃未来机会
继续：保留未来机会，但承担错过当前机会或额外成本
```

## 停止问题的基本结构

一个最优停止问题通常包含：

```text
state        当前状态
reward_stop 现在停止的收益
value_continue 继续的期望价值
```

决策规则：

```text
如果 reward_stop >= value_continue，就停止
否则继续
```

这和动态规划是一回事：

```text
V(state) = max(stop_value, continue_value)
```

最优策略往往可以写成阈值：

```text
当前值 >= threshold -> 停止
当前值 < threshold  -> 继续
```

但不是所有问题都有简单阈值。

## 一个最小例子

你有一次机会看到一个报价 `x`。

可以：

```text
现在接受 x
或者付出成本 c 再抽一次新报价 y，然后必须接受 y
```

假设 `y` 在 `{1, 2, 3, 4, 5, 6}` 中均匀分布。

继续的期望价值：

```text
E[y] - c = 3.5 - c
```

所以：

```text
如果 x >= 3.5 - c，接受 x
否则继续
```

代码：

```python
def accept_now(x, cost):
    continue_value = 3.5 - cost
    return x >= continue_value

print(accept_now(3, cost=0.2))
print(accept_now(4, cost=0.2))
```

结果：

```text
False
True
```

当成本是 `0.2` 时，继续价值是 `3.3`。

所以 `x = 3` 时继续，`x = 4` 时接受。

## 有限期动态规划

如果还可以继续多轮，阈值会随剩余轮数变化。

例子：

```text
最多看 n 次报价
每次报价是 1 到 6 的均匀整数
看到报价后可以接受并结束
也可以拒绝并看下一次
最后一次必须接受
```

设：

```text
V[t] = 还剩 t 次机会时的最优期望价值
```

最后一次：

```text
V[1] = E[roll] = 3.5
```

还剩 `t` 次时，当前报价为 `x`：

```text
接受价值 = x
拒绝价值 = V[t-1]
```

所以：

```text
V[t] = E[max(X, V[t-1])]
```

代码：

```python
def dice_offer_values(rounds):
    values = {1: 3.5}
    thresholds = {}

    for t in range(2, rounds + 1):
        continue_value = values[t - 1]
        thresholds[t] = continue_value
        values[t] = sum(max(x, continue_value) for x in range(1, 7)) / 6

    return values, thresholds

values, thresholds = dice_offer_values(3)

print(values)
print(thresholds)
```

结果：

```text
{1: 3.5, 2: 4.25, 3: 4.666666666666667}
{2: 3.5, 3: 4.25}
```

解释：

- 还剩 2 次时，如果当前报价至少 `3.5`，就接受。
- 还剩 3 次时，如果当前报价至少 `4.25`，就接受。
- 机会越多，越挑剔。

## 阈值策略

上面的骰子报价问题有阈值策略。

如果还剩 `t` 次机会：

```text
threshold = V[t-1]
```

当前报价 `x`：

```text
x >= threshold -> 接受
x < threshold  -> 拒绝
```

可以写成策略函数：

```python
def should_stop_offer(x, remaining_rounds, values):
    if remaining_rounds == 1:
        return True

    threshold = values[remaining_rounds - 1]
    return x >= threshold

values, _ = dice_offer_values(3)

print(should_stop_offer(4, 3, values))
print(should_stop_offer(5, 3, values))
```

结果：

```text
False
True
```

还剩 3 次时阈值是 `4.25`。

所以 4 不停，5 停。

## 秘书问题

secretary problem 是经典最优停止问题。

设有 `n` 个候选人，随机顺序面试。

规则：

```text
面试后必须立即决定是否录用
拒绝后不能回头
目标是选到全体最好的候选人
只能比较相对排名，不能知道绝对分数
```

经典策略：

```text
先观察前 r 个，不录用
记录其中最好者
之后遇到第一个超过前 r 个最好者的人，就录用
如果一直没有，最后录用最后一个
```

当 `n` 很大时，最优 `r` 约为：

```text
n / e
```

成功概率约为：

```text
1 / e
```

也就是大约 `36.8%`。

## 秘书问题小规模模拟

下面用枚举而不是随机模拟，计算给定 `n` 和 `r` 的成功概率。

把候选人质量表示为 `1..n`，数字越大越好。

```python
from itertools import permutations

def secretary_success_probability(n, r):
    success = 0
    total = 0

    for order in permutations(range(1, n + 1)):
        total += 1
        best_seen = max(order[:r]) if r > 0 else 0
        chosen = order[-1]

        for candidate in order[r:]:
            if candidate > best_seen:
                chosen = candidate
                break

        if chosen == n:
            success += 1

    return success / total

for r in range(5):
    print(r, secretary_success_probability(5, r))
```

一种输出：

```text
0 0.2
1 0.4166666666666667
2 0.43333333333333335
3 0.35
4 0.2
```

`n=5` 时，`r=2` 是最优。

大规模时不能枚举所有排列，使用公式或随机模拟更合适。

## 秘书问题公式直觉

策略成功需要：

```text
全局最好的人出现在观察期之后
观察期中包含全局最好之前的最佳参照
```

当观察比例是 `x = r/n` 时，成功概率近似：

```text
-x * ln(x)
```

这个函数在：

```text
x = 1/e
```

处达到最大值：

```text
1/e
```

所以经典口径是：

```text
先看约 37%，然后选择第一个超过此前所有人的候选人
```

这不是保证成功，而是最大化选到最佳候选人的概率。

## 房屋 offer 问题

题目：

```text
你最多看 3 套房。
每套房价值是 1 到 6 的随机数。
看完一套必须决定是否买。
目标最大化买到房子的期望价值。
```

这和骰子报价问题一样。

还剩 3 套房时，阈值是 `4.25`。

策略：

```text
第 1 套如果 >= 4.25，买
否则看第 2 套
第 2 套如果 >= 3.5，买
否则买第 3 套
```

代码验证：

```python
values, thresholds = dice_offer_values(3)

print(thresholds[3])
print(thresholds[2])
```

结果：

```text
4.25
3.5
```

## 交易中的停止规则

交易里也经常有停止问题：

```text
现在平仓，还是继续持有？
```

简化模型：

```text
当前未实现收益是 x
继续一天后，收益增加 +1 的概率是 p
收益减少 -1 的概率是 1-p
继续持有成本是 c
明天必须平仓
```

继续的期望增量：

```text
p * 1 + (1-p) * (-1) - c
= 2p - 1 - c
```

继续价值：

```text
x + 2p - 1 - c
```

现在平仓价值：

```text
x
```

所以如果：

```text
2p - 1 - c > 0
```

继续更好。

代码：

```python
def should_hold_one_more_day(p_up, cost):
    expected_increment = 2 * p_up - 1 - cost
    return expected_increment > 0

print(should_hold_one_more_day(0.55, cost=0.02))
print(should_hold_one_more_day(0.50, cost=0.02))
```

结果：

```text
True
False
```

真实交易问题复杂得多，因为：

- 波动不是固定 1。
- 收益分布有尾部。
- 成本和冲击不是常数。
- 继续持有会改变风险暴露。
- 风控约束可能强制停止。

但“停还是继续”的结构相同。

## 止盈止损不是自动最优

很多人以为：

```text
到止盈价就卖
到止损价就卖
```

一定合理。

但最优停止规则依赖：

- 后续收益分布。
- 持有成本。
- 风险约束。
- 机会成本。
- 信号衰减。
- 资金占用。

如果继续持有的期望价值高于现在卖出，机械止盈可能过早。

如果继续持有的风险太大，即使期望略高也可能不该继续。

因此停止规则要区分：

```text
期望最优
风险约束下最优
心理 comfort rule
```

## 动态规划模板

有限期最优停止常用模板：

```python
def backward_induction(states, final_value, transition, stop_value):
    value = final_value

    for t in reversed(range(len(states))):
        continue_value = transition(t, value)
        value = max(stop_value(t), continue_value)

    return value
```

这是伪代码。

真实问题里：

- `state` 可能是价格、收益、剩余时间、库存。
- `transition` 需要对下一期状态求期望。
- `stop_value` 是立即停止收益。

核心仍然是：

```text
value = max(stop, continue)
```

## 有成本时阈值下降

回到骰子报价问题。

如果继续要付成本 `c`，还剩 2 次机会时：

```text
拒绝当前报价的价值 = E[next roll] - c = 3.5 - c
```

成本越高，继续价值越低，接受阈值越低。

```python
def one_step_threshold(cost):
    return 3.5 - cost

print(one_step_threshold(0.0))
print(one_step_threshold(0.5))
print(one_step_threshold(1.0))
```

结果：

```text
3.5
3.0
2.5
```

这和交易直觉一致：

```text
持有成本越高，越倾向于早点停止
```

## 常见错误

### 错误 1：只比较当前值，不比较继续价值

最优停止不是看当前值高不高，而是看：

```text
当前停止收益 vs 继续的期望价值
```

### 错误 2：忘记机会成本

继续等待可能错过当前机会。

也可能占用资金、时间或风险预算。

这些都应进入继续价值。

### 错误 3：把秘书问题的 37% 当成万能规则

`1/e` 规则依赖严格假设：

- 随机顺序。
- 只能选一次。
- 目标是选到全局最佳。
- 只能比较相对排名。
- 拒绝后不能回头。

换了目标或信息结构，规则会变。

### 错误 4：忽略有限期边界

最后一期没有未来机会，通常必须停止。

倒推时边界条件很重要。

### 错误 5：只看期望不看风险约束

交易停止问题不能只看期望。

如果继续持有带来爆仓或超限风险，即使期望更高也可能不允许。

## 解题步骤

最优停止题可以按下面流程：

1. 明确目标：最大化期望收益、成功概率，还是风险调整收益。
2. 定义状态：当前值、剩余次数、历史最好值、成本等。
3. 写出停止收益。
4. 写出继续价值。
5. 从最后一期倒推。
6. 看策略是否能简化成阈值。
7. 检查题目假设是否满足经典规则。

## 记忆要点

- 最优停止问题是“现在停还是继续”。
- 基本决策是比较 `stop value` 和 `continue value`。
- 有限期问题常用向后归纳。
- 很多最优停止问题会出现阈值策略。
- 秘书问题经典规则是先观察约 `n/e`，再选第一个超过观察期最佳的人。
- `1/e` 规则不是万能，依赖强假设。
- 成本越高，继续价值越低，停止阈值通常越低。
- 交易停止规则要同时考虑期望、成本和风险约束。

## 自测题

1. 最优停止问题的基本决策比较是什么？
2. 为什么有限期停止问题通常从最后一期倒推？
3. 骰子报价问题中，还剩 2 次机会时为什么阈值是 3.5？
4. 秘书问题的经典 `1/e` 规则依赖哪些假设？
5. 为什么交易中的止盈止损不一定是期望意义下最优？
