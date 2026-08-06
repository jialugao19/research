# 70. 时间序列：stationarity 平稳性的定义、检验、变换与建模影响

## 核心概念

stationarity 平稳性描述一个时间序列的统计性质是否随时间保持稳定。

常见的弱平稳要求：

```text
E[x_t] 不随 t 变化
Var(x_t) 不随 t 变化
Cov(x_t, x_{t-k}) 只和 lag k 有关，不和具体时间 t 有关
```

直觉上，平稳序列没有持续漂移的均值、不断变化的方差或随时间改变的自相关结构。

很多时间序列模型默认输入是平稳的。例如 ARMA、许多回归残差模型和风险模型。如果非平稳序列被当作平稳序列建模，可能得到虚假的关系和不稳定预测。

## stationarity 回答的问题

平稳性检查回答：

- 序列是否有单位根？
- 均值和方差是否随时间变化？
- 能否直接建 ARMA 或回归模型？
- 是否需要差分、去趋势、取对数或分段建模？
- 样本内关系是否可能只是共同趋势造成的伪相关？

金融中常见经验：

- 价格水平常常非平稳。
- 收益率比价格更接近平稳。
- 波动率可能有聚集和 regime 变化。
- 价差或残差是否平稳，需要单独检验。

## 准备环境

```python
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss
```

为了让 KPSS 的边界插值警告不干扰示例，封装一个 helper：

```python
def kpss_result(series, regression="c"):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        stat, pvalue, lags, critical = kpss(
            series,
            regression=regression,
            nlags="auto",
        )

    return {
        "stat": stat,
        "pvalue": pvalue,
        "lags": lags,
        "critical": critical,
    }
```

KPSS 的 p-value 有时会落在表格边界外，statsmodels 会给出插值警告。这里忽略警告是为了让示例输出干净，不代表真实研究中可以忽略检验限制。

## 构造平稳和非平稳序列

构造三个序列：

1. 平稳 AR(1)。
2. 非平稳随机游走。
3. 趋势平稳序列。

```python
rng = np.random.default_rng(71)

n_obs = 500
dates = pd.bdate_range("2023-01-02", periods=n_obs)

ar_values = np.zeros(n_obs)
ar_noise = rng.normal(loc=0.0, scale=1.0, size=n_obs)

for t in range(1, n_obs):
    ar_values[t] = 0.30 * ar_values[t - 1] + ar_noise[t]

ar1 = pd.Series(ar_values, index=dates, name="stationary_ar1")

random_walk = pd.Series(
    np.cumsum(rng.normal(loc=0.0, scale=1.0, size=n_obs)),
    index=dates,
    name="random_walk",
)

trend_stationary = pd.Series(
    0.03 * np.arange(n_obs) + rng.normal(loc=0.0, scale=1.0, size=n_obs),
    index=dates,
    name="trend_stationary",
)
```

`ar1` 的均值围绕常数波动；`random_walk` 会持续漂移；`trend_stationary` 有确定性趋势，但去掉趋势后是平稳噪声。

## ADF 检验

ADF 检验的原假设：

```text
序列有单位根，即非平稳
```

计算 p-value：

```python
adf_table = pd.DataFrame({
    "series": ["ar1", "random_walk", "trend_stationary"],
    "adf_pvalue": [
        adfuller(ar1)[1],
        adfuller(random_walk)[1],
        adfuller(trend_stationary)[1],
    ],
})

print(adf_table)
```

解释：

- p-value 小：拒绝单位根，有证据支持平稳。
- p-value 大：不能拒绝单位根，序列可能非平稳。

在这个例子中：

- `ar1` 应该显著平稳。
- `random_walk` 通常不能拒绝单位根。
- `trend_stationary` 因为有趋势，直接做 ADF 可能看起来非平稳。

## KPSS 检验

KPSS 检验的原假设和 ADF 相反：

```text
序列是平稳的
```

计算：

```python
kpss_table = pd.DataFrame({
    "series": ["ar1", "random_walk", "trend_stationary"],
    "kpss_pvalue_level": [
        kpss_result(ar1)["pvalue"],
        kpss_result(random_walk)["pvalue"],
        kpss_result(trend_stationary)["pvalue"],
    ],
    "kpss_pvalue_trend": [
        kpss_result(ar1, regression="ct")["pvalue"],
        kpss_result(random_walk, regression="ct")["pvalue"],
        kpss_result(trend_stationary, regression="ct")["pvalue"],
    ],
})

print(kpss_table)
```

`regression="c"` 检查水平平稳；`regression="ct"` 允许确定性趋势，检查趋势平稳。

ADF 和 KPSS 常结合使用：

- ADF 拒绝单位根，KPSS 不拒绝平稳：比较支持平稳。
- ADF 不拒绝单位根，KPSS 拒绝平稳：比较支持非平稳。
- 二者冲突：可能有趋势、结构突变、样本太短或模型设定不合适。

## 差分让随机游走平稳

随机游走：

```text
x_t = x_{t-1} + epsilon_t
```

一阶差分：

```text
delta x_t = x_t - x_{t-1} = epsilon_t
```

代码：

```python
random_walk_diff = random_walk.diff().dropna()

print(adfuller(random_walk)[1])
print(adfuller(random_walk_diff)[1])
print(kpss_result(random_walk_diff)["pvalue"])
```

价格和收益的关系也是类似的：

- 价格水平常像随机游走。
- 收益或价格变化更接近平稳。

这就是 ARIMA 中 `I` 的含义：通过差分处理单位根。

## 去趋势处理 trend stationarity

趋势平稳不是随机游走。它是：

```text
x_t = a + b t + stationary_noise_t
```

如果直接差分，可能把可解释的趋势也去掉，并引入额外噪声。

更合适的方式可能是先估计确定性趋势：

```python
time_index = np.arange(n_obs)
trend_X = sm.add_constant(time_index)

trend_model = sm.OLS(trend_stationary.to_numpy(), trend_X).fit()
detrended = pd.Series(
    trend_model.resid,
    index=dates,
    name="detrended",
)

print(adfuller(detrended)[1])
print(kpss_result(detrended)["pvalue"])
```

如果去趋势后的残差平稳，说明原序列更像趋势平稳，而不是差分平稳。

两者区别很重要：

- 差分平稳：冲击有永久影响。
- 趋势平稳：冲击是暂时偏离，长期回到确定性趋势附近。

## 滚动统计量

平稳性也可以用滚动均值和滚动标准差做直观检查。

```python
rolling_window = 60

rolling_stats = pd.DataFrame({
    "ar1_mean": ar1.rolling(rolling_window).mean(),
    "ar1_std": ar1.rolling(rolling_window).std(),
    "rw_mean": random_walk.rolling(rolling_window).mean(),
    "rw_std": random_walk.rolling(rolling_window).std(),
}).dropna()

summary = rolling_stats.agg(["mean", "std", "min", "max"])

print(summary)
```

平稳序列的滚动均值和滚动方差不应长期系统性漂移。

随机游走的滚动均值常会随样本段落大幅变化。

滚动统计不是正式检验，但非常适合作为建模前的 sanity check。

## 结构突变不是普通非平稳

构造一个均值突然变化的序列：

```python
structural_break = pd.Series(
    np.r_[
        rng.normal(loc=0.0, scale=1.0, size=n_obs // 2),
        rng.normal(loc=2.0, scale=1.0, size=n_obs - n_obs // 2),
    ],
    index=dates,
    name="structural_break",
)

print(adfuller(structural_break)[1])
print(kpss_result(structural_break)["pvalue"])
```

结构突变可能让检验结论混乱：

- 全样本看起来不平稳。
- 每个子样本内部可能平稳。
- 模型参数在突变前后不同。

这类问题不能只靠差分解决，常需要：

- 分段建模。
- regime switch。
- 加入事件哑变量。
- 做滚动窗口估计。

## 平稳性和建模选择

不同情况对应不同处理：

```text
价格有单位根 -> 用收益、差分、ARIMA 或协整
确定性趋势 -> 去趋势或加入趋势项
方差变化 -> 变换、GARCH、分 regime
结构突变 -> 分段、滚动窗口、状态切换
季节性 -> 季节差分或季节项
```

平稳性不是为了“通过检验”而处理，而是为了让模型假设和数据生成机制更一致。

## 常见坑

第一，只看 ADF。

ADF 不拒绝单位根不等于一定非平稳；可能是样本短、趋势项没设对或检验力不足。

第二，把趋势平稳和差分平稳混淆。

趋势平稳适合去趋势；差分平稳适合差分。处理错了会损失信息。

第三，对所有序列机械差分。

过度差分会引入额外噪声，并破坏长期关系。

第四，忽略结构突变。

结构突变会让全样本检验失真。应检查分段、滚动参数和重大事件。

第五，把平稳性当永久属性。

金融市场会变。一个序列在历史样本中平稳，不代表未来仍然平稳。

第六，先看完整样本再决定变换用于回测。

如果变换选择依赖未来数据，也可能引入研究偏差。严谨做法是在训练窗口内决定处理方式。

## 实战提示

检查 stationarity 时可以按下面流程：

1. 画原序列、差分序列和滚动统计量。
2. 判断序列是否有明显趋势、季节性或结构突变。
3. 同时看 ADF 和 KPSS，不只依赖一个 p-value。
4. 区分差分平稳和趋势平稳。
5. 对价格、收益、价差、残差分别检查。
6. 在滚动窗口中复查平稳性和参数稳定性。
7. 对回测，所有变换选择必须只使用当时可见数据。
8. 把统计检验和经济逻辑结合起来。

## 小结

本节的重点：

- 弱平稳要求均值、方差和自协方差结构稳定。
- ADF 原假设是单位根；KPSS 原假设是平稳。
- 随机游走通常需要差分后才更接近平稳。
- 趋势平稳序列更适合去趋势，而不是机械差分。
- 结构突变会干扰平稳性检验。
- 平稳性决定 ARMA、回归、协整、GARCH 等模型能否合理使用。

## 自检问题

1. 弱平稳要求哪些统计性质不随时间变化？
2. ADF 和 KPSS 的原假设分别是什么？
3. 差分平稳和趋势平稳有什么区别？
4. 为什么不能对所有时间序列机械差分？
5. 结构突变会如何影响平稳性检验？
6. 为什么回测中选择变换方式也可能产生前视偏差？
