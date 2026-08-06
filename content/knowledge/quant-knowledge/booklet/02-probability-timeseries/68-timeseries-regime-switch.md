# 68. 时间序列：regime switch 的状态切换思想、简单识别与策略风险

## 核心概念

regime switch 指时间序列在不同市场状态之间切换。

例如市场可能处于：

- 低波动牛市。
- 高波动熊市。
- 横盘震荡。
- 危机流动性收缩。
- 政策驱动行情。

不同 regime 下，同一个策略的收益、波动、相关性、成交成本和容量都可能不同。

最简单的两状态模型可以写成：

```text
state_t in {0, 1}
return_t | state_t ~ Normal(mu_state, sigma_state^2)
P(state_t | state_{t-1}) 由转移矩阵决定
```

这里 `state_t` 是隐藏状态，不能直接观测，只能通过收益、波动、成交量、宏观变量等间接推断。

## regime switch 回答的问题

它不是问：

```text
未来收益一定涨还是跌？
```

它更常回答：

```text
当前市场更像哪种状态？
这个状态下策略风险和预期收益是否不同？
应该扩大、缩小还是暂停策略暴露？
```

regime switch 的价值在于提醒我们：很多模型参数不是永久稳定的。

例如：

- 低波动期有效的 carry 策略，危机期可能快速亏损。
- 均值回复策略在趋势行情中可能失效。
- 股票和债券相关性在不同通胀 regime 下可能改变。
- 流动性正常时的交易成本模型，压力期可能严重低估冲击。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一个两状态马尔可夫链：

```python
rng = np.random.default_rng(68)

n_obs = 600
dates = pd.bdate_range("2023-01-02", periods=n_obs)

transition = np.array([
    [0.96, 0.04],
    [0.12, 0.88],
])

states = np.empty(n_obs, dtype=int)
states[0] = 0

for t in range(1, n_obs):
    states[t] = rng.choice([0, 1], p=transition[states[t - 1]])
```

转移矩阵含义：

```text
P(明天低波动 | 今天低波动) = 0.96
P(明天高波动 | 今天低波动) = 0.04
P(明天低波动 | 今天高波动) = 0.12
P(明天高波动 | 今天高波动) = 0.88
```

状态有持续性，所以不会每天随机乱跳。

## 生成不同 regime 的收益

设状态 0 是低波动，状态 1 是高波动。

```python
mu = np.array([0.0005, -0.0004])
sigma = np.array([0.006, 0.018])

returns = pd.Series(
    rng.normal(loc=mu[states], scale=sigma[states]),
    index=dates,
    name="return",
)

state = pd.Series(states, index=dates, name="state")

print(state.value_counts(normalize=True).sort_index())
print(returns.groupby(state).agg(["mean", "std", "count"]))
```

教学模拟里我们知道真实状态；真实市场里通常不知道。

我们希望从可见数据推断：

- 当前更像低波动还是高波动？
- 状态是否刚刚切换？
- 策略是否应该降风险？

## 状态持续性

统计状态切换次数：

```python
state_switch_count = int(state.ne(state.shift()).sum() - 1)

print(state_switch_count)
```

如果状态切换太频繁，regime 概念可能没有实用意义；如果状态过于持久，样本中可观察到的切换次数太少，估计也不可靠。

regime 模型最难的地方之一，就是既要足够快地识别变化，又不能把普通噪声误判为状态切换。

## 用滚动波动率做简单识别

一个非常简单的规则：滚动波动率高于阈值，就认为进入高波动状态。

```python
rolling_vol = returns.rolling(window=20).std()
vol_threshold = rolling_vol.quantile(0.65)

estimated_state = (rolling_vol > vol_threshold).astype(float)
estimated_state = estimated_state.where(rolling_vol.notna()).dropna().astype(int)

aligned_true_state = state.loc[estimated_state.index]

accuracy = (estimated_state == aligned_true_state).mean()

print(vol_threshold)
print(accuracy)
```

这不是完整的 regime switching model，只是一个可解释的规则。

它展示了一个现实问题：状态识别通常有延迟。

20 日滚动波动率只有在高波动发生一段时间后才会升高，因此它不可能完美识别状态切换当日。

## 混淆矩阵

查看识别结果：

```python
confusion = pd.crosstab(
    aligned_true_state,
    estimated_state,
    normalize="index",
)

print(confusion)
```

行是真实状态，列是估计状态。

关注两类错误：

- 高波动状态被误判为低波动：风险暴露可能过高。
- 低波动状态被误判为高波动：可能错过收益。

实盘中第一类错误往往更危险，因为它发生在市场压力期。

## regime-aware 风险缩放

假设在估计为高波动状态时，把策略暴露降到 40%。

重要：今天估计出的状态，只能用于明天或之后的仓位，不能用于同一天已经发生的收益。

```python
exposure = (1.0 - 0.6 * estimated_state).shift(1)
exposure = exposure.reindex(returns.index).fillna(1.0)

strategy_return = exposure * returns

base_vol = returns.std(ddof=1)
strategy_vol = strategy_return.std(ddof=1)

base_sharpe = returns.mean() / returns.std(ddof=1) * np.sqrt(252)
strategy_sharpe = (
    strategy_return.mean()
    / strategy_return.std(ddof=1)
    * np.sqrt(252)
)

print(base_vol)
print(strategy_vol)
print(base_sharpe)
print(strategy_sharpe)
```

这个例子只说明机制：在高波动状态降暴露，可以降低组合波动。

但它不保证一定提高 Sharpe，因为：

- 状态识别会出错。
- 降暴露可能错过反弹。
- 频繁切换会增加交易成本。
- 高波动不一定代表低收益。

## Markov switching model 的思想

更正式的 regime switch 模型通常把状态设为隐藏马尔可夫链。

两状态收益模型：

```text
state_t ~ Markov transition matrix
return_t | state_t = k ~ Normal(mu_k, sigma_k^2)
```

估计目标：

- 每个状态的 `mu_k` 和 `sigma_k`。
- 状态转移概率。
- 每个日期属于某个状态的概率。

伪代码：

```text
initialize transition probabilities, regime means, regime variances

repeat until convergence:
    E-step:
        use forward-backward algorithm
        estimate P(state_t = k | all observations)

    M-step:
        update transition probabilities
        update regime means and variances
```

这类似 HMM 的 EM 估计。

在 Python 中可以用 `statsmodels` 的 Markov regression、HMM 库或自定义 EM 实现。

## filtered probability 和 smoothed probability

regime 模型里要区分：

```text
filtered probability = P(state_t | observations up to t)
smoothed probability = P(state_t | all observations, including future)
```

实盘信号只能使用 filtered probability。

如果回测中用 smoothed probability 判断历史状态，就会引入未来信息。

这是 regime switch 回测里非常常见的前视偏差。

## regime switch 的策略用途

常见用法包括：

1. 风险缩放：高波动 regime 降杠杆。
2. 策略开关：某些状态暂停均值回复或 carry 策略。
3. 参数切换：不同状态用不同半衰期、止损和仓位。
4. 组合配置：风险资产、债券、商品在不同 regime 下权重不同。
5. 压力测试：检查策略在危机状态中的表现。

一个实用框架：

```text
estimate state probability using data available today
if high_risk_probability > threshold:
    reduce exposure tomorrow
else:
    keep normal exposure tomorrow
```

这里最关键的是时间对齐：状态估计必须发生在交易决策之前。

## regime switch 的风险

第一，状态不可观测。

模型给出的状态只是推断，不是真实标签。不同模型可能给出不同状态划分。

第二，状态切换有延迟。

等模型确认高波动时，市场可能已经跌了一段。

第三，状态数量不稳定。

两状态、三状态、四状态模型可能给出完全不同解释。状态越多，越容易过拟合。

第四，结构变化会破坏历史转移概率。

过去危机的持续时间和未来危机不一定相同。

第五，策略响应会改变市场。

如果很多资金都在类似高波动信号下同时降仓，会放大流动性冲击。

## 常见坑

第一，用未来信息标注 regime。

例如事后看完整行情，把某段定义为危机期，然后用这个标签回测策略开关。这不是可交易信号。

第二，把 regime 解释得过于确定。

状态概率是概率，不是事实。`P(high vol)=60%` 不等于“已经确定高波动”。

第三，只看分类准确率。

在风险控制中，把高风险误判为低风险比相反错误更危险，损失函数不对称。

第四，忽略交易成本。

状态频繁切换会导致频繁调仓。即使风险下降，也可能被成本抵消。

第五，状态定义和策略目标不一致。

如果策略亏损来自流动性冲击，而 regime 只用收益波动定义，可能识别不到真正风险。

## 实战提示

使用 regime switch 时可以按下面流程：

1. 先明确状态要服务的目标：降风险、择时、调参数还是压力测试。
2. 选择可实时获得的观测变量：收益、波动、成交量、利差、宏观指标等。
3. 从简单规则开始，例如滚动波动率或趋势过滤。
4. 再考虑 Markov switching、HMM 或状态空间模型。
5. 区分 filtered 和 smoothed probability。
6. 所有信号至少滞后一日用于交易，避免同日收益泄露。
7. 分 regime 汇总收益、波动、回撤、turnover 和成本。
8. 做样本外和压力期检验。

## 小结

本节的重点：

- regime switch 描述市场在不同状态之间切换。
- 状态通常不可观测，只能从数据中推断。
- 简单滚动波动率规则可以作为高低波动状态识别基准。
- Markov switching model 把状态建模为隐藏马尔可夫链。
- filtered probability 可用于实时，smoothed probability 会使用未来信息。
- regime-aware 策略必须注意识别延迟、误判成本和交易成本。

## 自检问题

1. regime switch 和普通固定参数模型有什么区别？
2. 为什么状态识别通常有延迟？
3. filtered probability 和 smoothed probability 有什么区别？
4. 为什么用事后危机标签回测策略开关会有前视偏差？
5. 高波动状态识别准确率高是否一定能提升策略收益？
6. regime switch 模型为什么容易过拟合？
