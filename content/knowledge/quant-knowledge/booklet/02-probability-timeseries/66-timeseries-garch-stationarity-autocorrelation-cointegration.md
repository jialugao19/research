# 时间序列：GARCH、平稳性、自相关与协整的核心概念

## 核心概念

本节把四个时间序列高频概念放在一起建立框架：

- stationarity 平稳性：序列的统计性质是否随时间稳定。
- autocorrelation 自相关：当前值是否和过去值相关。
- GARCH：收益本身可能接近不可预测，但波动率会聚集。
- cointegration 协整：两个非平稳序列的某个线性组合可能是平稳的。

它们回答的是不同问题：

```text
平稳性：这个序列能否用稳定模型描述？
自相关：过去值对当前值是否有解释力？
GARCH：波动率是否有持续性？
协整：两个非平稳序列是否存在长期均衡关系？
```

金融时间序列中，价格水平常常非平稳，收益率更接近平稳；收益率自相关可能很弱，但平方收益或绝对收益经常有显著自相关，这就是波动率聚集。

## 准备环境

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, acf, coint
from statsmodels.stats.diagnostic import acorr_ljungbox
```

设置随机种子和日期：

```python
rng = np.random.default_rng(66)

n_obs = 800
dates = pd.bdate_range("2022-01-03", periods=n_obs)
```

本节的例子都用模拟数据，目的是让统计性质更清楚。

## 平稳性 stationarity

粗略地说，平稳序列的均值、方差和自相关结构不随时间系统性变化。

非平稳随机游走：

```text
x_t = x_{t-1} + epsilon_t
```

平稳 AR(1)：

```text
y_t = phi y_{t-1} + epsilon_t,  |phi| < 1
```

构造两个序列：

```python
random_walk = pd.Series(
    np.cumsum(rng.normal(size=n_obs)),
    index=dates,
    name="random_walk",
)

ar_values = np.zeros(n_obs)
ar_noise = rng.normal(size=n_obs)

for t in range(1, n_obs):
    ar_values[t] = 0.65 * ar_values[t - 1] + ar_noise[t]

ar1 = pd.Series(ar_values, index=dates, name="ar1")
```

用 ADF 检验检查单位根：

```python
adf_random_walk = adfuller(random_walk)
adf_diff_random_walk = adfuller(random_walk.diff().dropna())
adf_ar1 = adfuller(ar1)

print(adf_random_walk[1])
print(adf_diff_random_walk[1])
print(adf_ar1[1])
```

ADF 的原假设是“存在单位根”，也就是非平稳。

通常：

- `p-value` 大：不能拒绝非平稳。
- `p-value` 小：有证据认为序列平稳。

随机游走本身通常非平稳；一阶差分后更接近平稳。AR(1) 在 `|phi| < 1` 时是平稳的。

## 自相关 autocorrelation

自相关衡量序列和自身滞后项的相关性。

```text
rho_k = corr(x_t, x_{t-k})
```

计算 AR(1) 的自相关：

```python
ar1_acf = acf(ar1, nlags=5, fft=False)

print(ar1_acf)
```

AR(1) 的自相关通常会逐步衰减：

```text
lag 1 高，lag 2 次之，之后逐步下降
```

在策略研究中，自相关可以用于检查：

- 收益是否有动量或反转。
- 残差是否还是白噪声。
- 因子值是否过度平滑。
- 交易信号是否导致高换手或慢衰减。

但自相关不等于可交易 alpha。即使存在统计自相关，也要考虑成本、延迟和样本外稳定性。

## GARCH 和波动率聚集

很多金融收益序列有一个典型特征：

```text
收益本身自相关不强，但平方收益有明显自相关。
```

这意味着方向难预测，但波动率状态有持续性。

GARCH(1,1) 的基本形式：

```text
r_t = sigma_t z_t
sigma_t^2 = omega + alpha r_{t-1}^2 + beta sigma_{t-1}^2
z_t ~ N(0, 1)
```

其中：

- `omega`：长期方差基准。
- `alpha`：上一期冲击对当前方差的影响。
- `beta`：上一期方差状态的持续性。

如果 `alpha + beta` 接近 1，波动率冲击会持续很久。

## 模拟 GARCH(1,1)

```python
omega = 0.000002
alpha = 0.08
beta = 0.90

z = rng.normal(size=n_obs)
conditional_var = np.empty(n_obs)
garch_return_values = np.empty(n_obs)

conditional_var[0] = omega / (1 - alpha - beta)
garch_return_values[0] = np.sqrt(conditional_var[0]) * z[0]

for t in range(1, n_obs):
    conditional_var[t] = (
        omega
        + alpha * garch_return_values[t - 1] ** 2
        + beta * conditional_var[t - 1]
    )
    garch_return_values[t] = np.sqrt(conditional_var[t]) * z[t]

garch_return = pd.Series(
    garch_return_values,
    index=dates,
    name="garch_return",
)
```

比较收益和平方收益的自相关：

```python
return_acf = acf(garch_return, nlags=5, fft=False)
squared_return_acf = acf(garch_return ** 2, nlags=5, fft=False)

print(return_acf)
print(squared_return_acf)
```

典型结果：

- `return_acf` 除 lag 0 外接近 0。
- `squared_return_acf` 在多个 lag 上明显为正。

这就是波动率聚集：大波动后更容易继续大波动，小波动后更容易继续小波动。

## Ljung-Box 检验

Ljung-Box 检验可以检查一组滞后自相关是否整体显著。

```python
lb_return = acorr_ljungbox(
    garch_return,
    lags=[10],
    return_df=True,
)

lb_squared_return = acorr_ljungbox(
    garch_return ** 2,
    lags=[10],
    return_df=True,
)

print(lb_return)
print(lb_squared_return)
```

常见现象：

- 对收益本身，可能不能拒绝“无自相关”。
- 对平方收益，通常强烈拒绝“无自相关”。

这说明均值模型可能不需要复杂结构，但波动率模型需要处理条件异方差。

## GARCH 的用途

GARCH 主要用于建模条件波动率，而不是直接预测收益方向。

典型用途：

- 波动率预测。
- VaR 和风险预算。
- 动态仓位缩放。
- 期权和波动率策略辅助。
- 检查回归残差是否有条件异方差。

伪代码：

```text
fit mean model on returns
get residuals
fit GARCH on residuals
forecast next-period variance
scale position by target_vol / forecast_vol
```

这类流程在实盘中很常见，但必须注意模型误差、极端跳跃和交易成本。

## 协整 cointegration

两个序列可以各自非平稳，但它们的某个线性组合是平稳的。

例如：

```text
x_t 是随机游走
y_t = 1.5 x_t + stationary_spread_t
spread_t = y_t - 1.5 x_t
```

那么 `x_t` 和 `y_t` 都可能非平稳，但 `spread_t` 是平稳的。

这就是协整。

它常用于：

- pairs trading。
- 价差均值回复。
- ETF 和成分篮子关系。
- 同期限或相邻期限利率关系。
- 商品跨期价差。

## 模拟协整关系

```python
x_values = np.cumsum(rng.normal(scale=1.0, size=n_obs))

spread_values = np.zeros(n_obs)
spread_noise = rng.normal(scale=0.6, size=n_obs)

for t in range(1, n_obs):
    spread_values[t] = 0.75 * spread_values[t - 1] + spread_noise[t]

y_values = 1.5 * x_values + spread_values

x = pd.Series(x_values, index=dates, name="x")
y = pd.Series(y_values, index=dates, name="y")
spread = y - 1.5 * x
```

检查各自平稳性：

```python
print(adfuller(x)[1])
print(adfuller(y)[1])
print(adfuller(spread)[1])
```

通常 `x` 和 `y` 的 ADF p-value 较大，而 `spread` 的 p-value 很小。

用 Engle-Granger 协整检验：

```python
coint_stat, coint_pvalue, coint_crit = coint(y, x)

print(coint_stat)
print(coint_pvalue)
print(coint_crit)
```

如果 `coint_pvalue` 很小，说明有证据认为二者协整。

## 协整不等于相关

相关性看的是两个序列同涨同跌的程度；协整看的是长期均衡误差是否平稳。

两个随机游走可能短期相关很高，但没有稳定价差。

对比一个不协整的随机游走：

```python
z_random_walk = pd.Series(
    np.cumsum(rng.normal(size=n_obs)),
    index=dates,
    name="z_random_walk",
)

not_coint_pvalue = coint(z_random_walk, x)[1]

print(not_coint_pvalue)
```

如果 p-value 较大，就不能认为它和 `x` 有协整关系。

pairs trading 中，只用相关性筛选资产很危险；还需要检查价差平稳性、交易成本、半衰期、结构变化和做空约束。

## 四个概念如何串起来

一个常见研究流程：

1. 先检查价格、收益、价差是否平稳。
2. 如果价格非平稳，考虑差分、收益率或协整价差。
3. 检查收益或残差是否有自相关。
4. 检查平方收益或平方残差是否有自相关。
5. 如果有波动率聚集，考虑 GARCH 或其他波动率模型。
6. 如果两个价格序列有共同趋势，考虑协整和误差修正模型。

这些检查不是为了机械套模型，而是为了避免把非平稳、异方差或伪相关当成 alpha。

## 常见坑

第一，把非平稳价格相关当成有效关系。

两个价格序列都上涨时，相关性可能很高，但价差可能完全不稳定。

第二，只检查收益自相关，不检查平方收益自相关。

收益方向可能不可预测，但风险状态仍然高度可预测。

第三，把 GARCH 当成收益预测模型。

GARCH 主要预测条件方差，不是直接预测正负方向。

第四，看到协整就直接做 pairs trading。

协整关系可能失效，价差均值回复可能太慢，交易成本可能吃掉收益。

第五，忽略结构突变。

平稳性、自相关和协整都可能在 regime 变化后失效。

第六，多重检验。

大量资产两两做协整检验时，总会找到一些看似显著的组合。必须做样本外验证。

## 实战提示

处理时间序列时可以按下面流程：

1. 画出原序列、差分序列和滚动统计量。
2. 用 ADF 辅助判断单位根，但不要只看一个 p-value。
3. 用 ACF / PACF 检查自相关结构。
4. 对收益和平方收益分别做 Ljung-Box 检验。
5. 对波动率聚集明显的序列考虑 GARCH。
6. 对价格对或篮子检查协整，而不是只看相关性。
7. 分样本和滚动窗口检查参数稳定性。
8. 对交易策略加入成本、延迟和风控后再评估。

## 小结

本节的重点：

- 平稳性决定能否用稳定时间序列模型描述数据。
- 自相关衡量序列和自身滞后项的关系。
- 金融收益常见现象是收益自相关弱、平方收益自相关强。
- GARCH 用于刻画条件波动率和波动率聚集。
- 协整描述多个非平稳序列之间的稳定长期关系。
- 相关性不等于协整，协整也不等于可交易收益。
- 这些检验都需要样本外验证和经济解释。

## 自检问题

1. ADF 检验的原假设是什么？
2. 为什么随机游走通常非平稳，而它的一阶差分可能平稳？
3. 收益自相关弱但平方收益自相关强说明什么？
4. GARCH(1,1) 中 `alpha` 和 `beta` 分别代表什么？
5. 协整和相关性有什么区别？
6. 为什么大量资产两两做协整检验会有多重检验风险？
