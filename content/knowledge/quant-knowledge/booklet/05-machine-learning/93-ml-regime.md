# 93. 机器学习：regime 的市场状态划分、分布变化和分状态建模

## 核心概念

regime 是状态、环境、阶段。

在量化和机器学习中，regime 常指：

```text
市场处于某种可识别的状态，数据分布和模型关系在这个状态下比较相似。
```

常见 market regime：

- 高波动 / 低波动。
- 趋势 / 震荡。
- 高流动性 / 低流动性。
- 牛市 / 熊市。
- 风险偏好 / 风险厌恶。
- 宽信用 / 紧信用。
- 高相关性 / 低相关性。

regime 的核心问题是：

```text
同一个模型在所有市场状态下都适用吗？
```

很多策略不是永远有效，而是在某些 regime 下有效，在另一些 regime 下失效。

## regime 为什么重要

机器学习通常假设：

```text
训练集和测试集来自相似分布
```

但金融市场里，分布会变。

例如：

```text
低波动环境下，均值回复因子有效
高波动环境下，趋势和流动性风险更重要
```

如果把所有状态混在一起训练，模型可能学到一个“平均关系”。

这个平均关系在任何一个状态下都不够好。

regime 分析可以帮助你：

- 解释模型失效。
- 做分状态评估。
- 决定是否训练分状态模型。
- 控制风险暴露。
- 调整交易成本和仓位。

## 一个简单 regime 划分

用 rolling volatility 划分高低波动状态。

简化数据：

```python
returns = [0.01, -0.02, 0.015, 0.005, -0.04, 0.03]
vols = [0.10, 0.12, 0.11, 0.25, 0.30, 0.28]

regimes = [
    "high_vol" if vol >= 0.20 else "low_vol"
    for vol in vols
]

print(regimes)
```

结果：

```text
['low_vol', 'low_vol', 'low_vol', 'high_vol', 'high_vol', 'high_vol']
```

这里用 `0.20` 作为阈值。

真实项目里，阈值可以来自：

- 历史分位数。
- 业务经验。
- 聚类。
- 隐马尔可夫模型。
- 宏观或微观结构指标。

## 分 regime 统计收益

有了状态标签后，可以分组看收益。

```python
from collections import defaultdict

returns = [0.01, -0.02, 0.015, 0.005, -0.04, 0.03]
regimes = ["low_vol", "low_vol", "low_vol", "high_vol", "high_vol", "high_vol"]

by_regime = defaultdict(list)

for regime, ret in zip(regimes, returns):
    by_regime[regime].append(ret)

avg_by_regime = {
    regime: sum(values) / len(values)
    for regime, values in by_regime.items()
}

print(avg_by_regime)
```

结果：

```text
{'low_vol': 0.0016666666666666663, 'high_vol': -0.0016666666666666663}
```

同一组收益，低波动状态平均为正，高波动状态平均为负。

这说明：

```text
总体平均可能掩盖状态差异
```

## 分状态命中率

除了平均收益，也可以看 hit rate。

```python
hit_rate_by_regime = {
    regime: sum(x > 0 for x in values) / len(values)
    for regime, values in by_regime.items()
}

print(hit_rate_by_regime)
```

结果：

```text
{'low_vol': 0.6666666666666666, 'high_vol': 0.6666666666666666}
```

这里两个状态的 hit rate 一样。

但平均收益不同。

说明高波动状态下亏损样本可能更大。

所以 regime 分析不要只看一个指标。

## regime 特征

常用 regime 特征包括：

```text
realized volatility
market drawdown
index trend
cross-sectional dispersion
average correlation
liquidity / volume
bid-ask spread
macro variables
credit spread
rates level / slope
```

选择 regime 特征时，要问：

```text
这个状态在决策时是否已经可见？
它是否使用了未来信息？
它和策略收益是否有合理机制关系？
```

例如：

```text
用未来 20 天波动率给今天打标签
```

会引入未来信息。

应该使用截至当前可见的数据，例如：

```text
过去 20 天 realized volatility
```

## 防止 regime 泄露

错误做法：

```python
future_returns = [0.03, -0.02, 0.01]
regime = "bull" if sum(future_returns) > 0 else "bear"
```

这个 regime 使用了未来收益。

如果你用它训练或评估模型，会产生严重泄露。

安全原则：

```text
用于 t 时刻决策的 regime 标签，只能依赖 t 时刻之前或当时可见的信息。
```

伪代码：

```python
regime_t = compute_regime(data_up_to_time_t)
signal_t = model.predict(features_at_time_t, regime_t)
```

不要写成：

```python
regime_t = compute_regime(data_from_t_to_t_plus_20)
```

## 分状态模型

有三种常见做法。

第一种：一个全局模型，加 regime 作为特征。

```text
y ~ features + regime
```

第二种：每个 regime 单独训练一个模型。

```text
low_vol_model
high_vol_model
```

第三种：全局模型 + 分状态校准。

```text
global score -> regime-specific threshold / position sizing
```

选择时要考虑：

- 每个 regime 样本是否足够。
- 状态切换是否稳定。
- 分状态模型是否过拟合。
- regime 标签是否实时可得。

## 简化分状态预测

假设低波动和高波动下，同一个信号的收益映射不同。

```python
signal = [0.2, 0.4, 0.1, 0.3]
regime = ["low", "low", "high", "high"]

coef_by_regime = {
    "low": 0.5,
    "high": -0.2,
}

pred = [
    coef_by_regime[r] * x
    for x, r in zip(signal, regime)
]

print(pred)
```

结果：

```text
[0.1, 0.2, -0.020000000000000004, -0.06]
```

同样是正信号：

```text
low regime 下预测收益为正
high regime 下预测收益为负
```

这就是分状态建模的直觉。

## regime 切换成本

regime 标签如果频繁跳变，会导致模型或仓位频繁切换。

例如：

```python
regimes = ["low", "high", "low", "high", "low"]

switches = sum(
    regimes[i] != regimes[i - 1]
    for i in range(1, len(regimes))
)

print(switches)
```

结果：

```text
4
```

5 天里切换 4 次，太频繁。

常见处理：

- 平滑 regime 指标。
- 设置 hysteresis 上下阈值。
- 要求状态持续若干天才切换。
- 仓位调整时做缓慢过渡。

## hysteresis 阈值

hysteresis 是滞后阈值。

例如：

```text
vol > 0.25 才进入 high
vol < 0.18 才退出 high
中间保持原状态
```

```python
vols = [0.16, 0.20, 0.26, 0.23, 0.19, 0.17]
state = "low"
states = []

for vol in vols:
    if state == "low" and vol > 0.25:
        state = "high"
    elif state == "high" and vol < 0.18:
        state = "low"

    states.append(state)

print(states)
```

结果：

```text
['low', 'low', 'high', 'high', 'high', 'low']
```

这样可以减少状态在阈值附近来回跳动。

## regime 失衡

有些状态样本很少。

```python
labels = ["low"] * 90 + ["high"] * 10

high_ratio = labels.count("high") / len(labels)

print(high_ratio)
```

结果：

```text
0.1
```

如果高波动样本只有 10%，单独训练 high regime 模型可能样本不足。

这时可以考虑：

- 更粗的状态划分。
- 使用全局模型 + regime 特征。
- 分状态只调整阈值或仓位。
- 增加正则化。
- 用更长历史，但注意结构变化。

## regime 和 robustness

regime 分析本身是 robustness 检查的一部分。

你要问：

```text
模型是否只在一种状态下有效？
状态变化时是否有保护机制？
最差状态下亏损是否可接受？
```

例如：

```python
performance = {
    "low_vol": 0.12,
    "high_vol": -0.08,
    "crisis": -0.25,
}

worst_regime = min(performance, key=performance.get)

print(worst_regime)
print(performance[worst_regime])
```

结果：

```text
crisis
-0.25
```

如果 crisis 下亏损不可接受，就需要风控或降仓规则。

## regime 和模型评估

评估报告中，最好同时给出：

```text
overall metric
metric by regime
sample count by regime
turnover by regime
drawdown by regime
cost by regime
```

否则可能出现：

```text
overall Sharpe = 1.2
low_vol Sharpe = 2.0
high_vol Sharpe = -0.5
```

这比单个 overall 数字更有信息量。

## 常见错误

### 错误 1：用未来数据定义 regime

这是最严重错误。

例如用未来收益、未来波动率、未来最大回撤给当前打标签。

这会让模型看到未来。

### 错误 2：状态切得太细

状态越多，每个状态样本越少。

分状态模型容易过拟合。

### 错误 3：只看状态内平均值

要同时看样本数、波动、最差窗口、成本和换手。

### 错误 4：状态频繁跳变

频繁跳变会带来高换手和不稳定决策。

需要平滑或滞后机制。

### 错误 5：把 regime 当成因果解释

regime 标签通常只是分组或状态描述。

它不自动证明因果关系。

## 实战检查清单

做 regime 分析时可以问：

1. regime 标签在决策时是否可见？
2. 每个 regime 样本量是否足够？
3. 各 regime 下收益、风险、成本、换手如何？
4. regime 是否频繁切换？
5. 分状态模型是否比全局模型稳定提升？
6. 最差 regime 下是否有风控保护？
7. regime 定义是否有清晰经济含义？

## 记忆要点

- regime 是市场状态或环境。
- 金融数据关系常随 regime 改变。
- regime 可以作为特征、分组评估维度或分状态模型开关。
- regime 标签必须只使用当时可见信息。
- 分状态模型需要足够样本，否则容易过拟合。
- hysteresis 可以减少状态频繁跳变。
- 评估模型时要看 overall，也要看 by regime。
- regime 分析能帮助解释 robustness，但不能自动证明因果。

## 自测题

1. regime 在量化机器学习中是什么意思？
2. 为什么不能用未来 20 天收益给今天定义 regime？
3. 全局模型加 regime 特征和每个 regime 单独训练模型有什么区别？
4. hysteresis 阈值为什么能减少状态来回跳动？
5. 做分 regime 评估时，除了平均收益还应该看什么？
