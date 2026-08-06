# 91. 机器学习：robustness 的分布扰动、异常值、噪声和策略稳健性

## 核心概念

robustness 是稳健性。

在机器学习和量化研究里，它问的是：

```text
模型或策略在数据轻微变化、异常值、噪声、分布变化下，表现是否仍然可靠？
```

一个模型在训练集上效果很好，不代表它稳健。

稳健模型应该尽量避免：

- 依赖少数异常样本。
- 依赖不稳定特征。
- 只在某个时间段有效。
- 对轻微噪声极度敏感。
- 在某些市场状态下完全失效。
- 因交易成本或滑点变化而从正变负。

在量化中，robustness 比单次回测收益更重要。

因为未来数据一定和训练数据不同。

## robustness 回答的问题

常见问题：

```text
异常值删掉后结果还成立吗？
换一个训练/测试切分还成立吗？
换一个市场 regime 还成立吗？
加一点噪声后预测还稳定吗？
交易成本提高后策略还盈利吗？
换一组股票池后信号还有效吗？
```

这些问题都在检查：

```text
结果是不是脆弱的偶然现象？
```

## 异常值影响

均值很容易被异常值影响。

```python
returns = [0.01, 0.02, 0.00, -0.01, 0.50]

mean_return = sum(returns) / len(returns)
median_return = sorted(returns)[len(returns) // 2]

print(mean_return)
print(median_return)
```

结果：

```text
0.10400000000000001
0.01
```

`0.50` 这个异常收益把均值拉到 `10.4%`。

但中位数仍是 `1%`。

所以做稳健性检查时，要问：

```text
结论是否主要来自少数极端点？
```

## winsorize

winsorize 是把极端值截到分位数边界。

简化例子：

```python
def winsorize(values, lower, upper):
    return [min(max(x, lower), upper) for x in values]

returns = [0.01, 0.02, 0.00, -0.01, 0.50]
winsorized = winsorize(returns, lower=-0.05, upper=0.05)

print(winsorized)
print(sum(winsorized) / len(winsorized))
```

结果：

```text
[0.01, 0.02, 0.0, -0.01, 0.05]
0.014
```

截尾后均值从 `10.4%` 降到 `1.4%`。

如果结论在 winsorize 后完全消失，说明它可能很依赖异常值。

## 噪声扰动

稳健模型对小噪声不应极度敏感。

例子：一个线性打分函数：

```python
def score(features, weights):
    return sum(x * w for x, w in zip(features, weights))

features = [1.0, 2.0, -1.0]
weights = [0.5, 0.2, -0.1]

base_score = score(features, weights)
noisy_score = score([1.01, 1.98, -1.02], weights)

print(base_score)
print(noisy_score)
print(noisy_score - base_score)
```

结果：

```text
1.0
1.003
0.0029999999999998916
```

轻微特征噪声只让分数变化约 `0.003`。

如果一个模型对很小扰动产生巨大变化，就需要检查：

- 特征尺度。
- 模型复杂度。
- 是否过拟合。
- 是否有不稳定的除法或非线性变换。

## 排名稳健性

量化里经常关心股票排名。

如果加一点噪声，top 组合完全换掉，说明信号可能不稳。

```python
scores = {
    "A": 0.90,
    "B": 0.89,
    "C": 0.30,
    "D": 0.10,
}

noisy_scores = {
    "A": 0.88,
    "B": 0.91,
    "C": 0.31,
    "D": 0.09,
}

def top_k(score_map, k):
    return [name for name, _ in sorted(score_map.items(), key=lambda x: -x[1])[:k]]

print(top_k(scores, 2))
print(top_k(noisy_scores, 2))
```

结果：

```text
['A', 'B']
['B', 'A']
```

top-2 集合没有变，只是顺序变了。

如果投资组合等权持有 top-2，这种扰动影响不大。

如果策略只买 top-1，就会从 `A` 换成 `B`，换手可能很高。

## 分组稳健性

一个信号如果只在某个子样本有效，要谨慎。

例如按市场状态分组：

```python
returns_by_regime = {
    "low_vol": [0.01, 0.02, 0.00, 0.01],
    "high_vol": [-0.03, 0.04, -0.02, 0.01],
}

avg_by_regime = {
    regime: sum(values) / len(values)
    for regime, values in returns_by_regime.items()
}

print(avg_by_regime)
```

结果：

```text
{'low_vol': 0.01, 'high_vol': 0.0}
```

总体可能看起来不错，但高波动环境下没有收益。

稳健性检查应该分维度看：

- 年份。
- 行业。
- 市值。
- 波动率 regime。
- 流动性分组。
- 多空两侧。

## 时间切分稳健性

不要只看一个训练/测试切分。

常见检查：

```text
train: 2015-2018, test: 2019
train: 2016-2019, test: 2020
train: 2017-2020, test: 2021
```

如果模型只在一个窗口好，可能是窗口偶然。

伪代码：

```python
for train_start, train_end, test_start, test_end in splits:
    model = fit(data[train_start:train_end])
    metric = evaluate(model, data[test_start:test_end])
    print(metric)
```

你关心的不只是平均结果，还包括：

```text
最差窗口是否可接受？
窗口之间差异是否过大？
差的窗口是否集中在某类 regime？
```

## 特征扰动检查

如果某个特征稍微改口径，模型就失效，说明模型可能过度依赖该特征。

例子：

```text
feature = 20 日动量
替代检查：
feature = 19 日动量
feature = 21 日动量
feature = 20 日动量但 winsorize 不同
feature = 20 日动量但去掉最低流动性股票
```

如果只有一个精确口径有效，要警惕数据挖掘。

稳健信号通常对合理邻近参数不应完全崩掉。

## 交易成本稳健性

量化策略必须检查交易成本。

```python
gross_daily_return = 0.0008
turnover = 0.5
cost_per_turnover = 0.001

net_daily_return = gross_daily_return - turnover * cost_per_turnover

print(net_daily_return)
```

结果：

```text
0.00030000000000000003
```

如果成本翻倍：

```python
net_daily_return_stressed = gross_daily_return - turnover * (2 * cost_per_turnover)

print(net_daily_return_stressed)
```

结果：

```text
-0.00019999999999999998
```

成本一翻倍就变负，说明策略对成本很敏感。

这不一定不能做，但需要明确容量和执行假设。

## robust metric

单一平均指标容易掩盖问题。

可以同时看：

```text
mean performance
median performance
worst period
hit rate
drawdown
turnover
cost sensitivity
subgroup performance
```

例如多个窗口收益：

```python
window_returns = [0.12, 0.08, -0.03, 0.10, 0.06]

mean_return = sum(window_returns) / len(window_returns)
worst_return = min(window_returns)
hit_rate = sum(x > 0 for x in window_returns) / len(window_returns)

print(mean_return)
print(worst_return)
print(hit_rate)
```

结果：

```text
0.066
-0.03
0.8
```

平均收益是正的，但有一个窗口亏损。

面试或研究报告中，要说明这个亏损窗口是否可接受。

## 训练稳健性

模型训练也有稳健性问题。

例如：

- 换 random seed 后结果是否变化很大？
- 换训练样本子集后结果是否变化很大？
- 换超参数附近值是否变化很大？
- 换 early stopping 轮数是否变化很大？

树模型、神经网络和复杂 ensemble 都可能对训练细节敏感。

如果表现只在某个 seed 下特别好，要警惕。

## robustness 和 stability 的区别

这两个词接近，但可以这样区分：

```text
robustness: 面对外部扰动或环境变化，表现是否还能接受
stability: 模型本身或估计结果对样本、参数、随机性的波动是否小
```

例子：

```text
异常值冲击后模型是否还能工作 -> robustness
换一个 bootstrap 样本特征重要性是否差不多 -> stability
```

下一篇会更集中讨论 stability。

本篇重点是外部扰动、异常值、噪声和策略假设变化。

## 常见错误

### 错误 1：只看平均表现

平均收益好，不代表每个年份、行业、regime 都可接受。

要看分组和最差场景。

### 错误 2：忽略异常值来源

异常值可能是真实机会，也可能是坏数据。

不能机械删除，要先判断来源。

### 错误 3：参数只测一个点

如果只在 `lookback=20` 有效，`19` 和 `21` 都失效，要警惕过拟合。

### 错误 4：不做成本压力测试

交易成本、滑点、冲击成本稍微变动就可能改变结论。

### 错误 5：把样本内稳健当成样本外稳健

样本内多切几组仍然是历史数据。

真正可靠性还要看样本外、实时跟踪和经济逻辑。

## 实战检查清单

做 robustness 检查时可以问：

1. 删除或截尾极端值后结果如何？
2. 增加小噪声后预测或排名是否稳定？
3. 不同年份、行业、市值、流动性分组是否都可接受？
4. 交易成本提高 1 倍或 2 倍后是否仍可接受？
5. 参数在合理邻域内变化时结果是否平滑？
6. 最差窗口有多差？能否解释？
7. 结果是否有经济逻辑，而不仅是统计显著？

## 记忆要点

- robustness 是模型或策略面对扰动时是否仍可靠。
- 异常值可能显著改变均值和模型拟合。
- winsorize 可以检查结论是否依赖极端值。
- 小噪声扰动可以检查预测或排名是否脆弱。
- 分时间、行业、regime、流动性看表现很重要。
- 成本压力测试是量化 robustness 的核心部分。
- 稳健性不等于表现永远不变，而是变化后仍可解释、可接受。
- 样本内稳健不能替代样本外验证。

## 自测题

1. robustness 在机器学习和量化中指什么？
2. 为什么只看平均收益不够？
3. winsorize 能帮助检查什么问题？
4. 为什么要做交易成本压力测试？
5. robustness 和 stability 可以如何区分？
