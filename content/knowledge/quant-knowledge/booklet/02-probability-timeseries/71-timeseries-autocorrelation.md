# Autocorrelation

## 核心概念

autocorrelation 自相关衡量一个时间序列和自身滞后项之间的相关性。

lag `k` 的自相关定义为：

```text
rho_k = corr(x_t, x_{t-k})
```

如果 `rho_1 > 0`，说明当前值和上一期同向关系更强；如果 `rho_1 < 0`，说明当前值和上一期反向关系更强。

自相关常用于回答：

- 序列是否有动量或反转？
- ARMA 模型阶数可能是多少？
- 回归残差是否接近白噪声？
- 收益方向是否有可预测性？
- 波动率是否有聚集？

但自相关不等于可交易 alpha。交易成本、延迟、容量和样本外稳定性同样重要。

## ACF 和 PACF

ACF 是 autocorrelation function，直接计算每个 lag 的自相关。

PACF 是 partial autocorrelation function，衡量在控制中间 lag 后，`x_t` 和 `x_{t-k}` 的直接关系。

直觉：

- AR(p) 模型：PACF 常在 p 阶后截尾，ACF 通常拖尾衰减。
- MA(q) 模型：ACF 常在 q 阶后截尾，PACF 通常拖尾衰减。

这只是经验规则，不是机械定律。

## 准备环境

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
```

设置随机种子和日期：

```python
rng = np.random.default_rng(71)

n_obs = 800
dates = pd.bdate_range("2022-01-03", periods=n_obs)
```

## AR(1) 的自相关

构造 AR(1)：

```text
x_t = 0.65 x_{t-1} + epsilon_t
```

```python
ar_values = np.zeros(n_obs)
ar_noise = rng.normal(size=n_obs)

for t in range(1, n_obs):
    ar_values[t] = 0.65 * ar_values[t - 1] + ar_noise[t]

ar1 = pd.Series(ar_values, index=dates, name="ar1")
```

计算 ACF 和 PACF：

```python
ar1_acf = acf(ar1, nlags=5, fft=False)
ar1_pacf = pacf(ar1, nlags=5, method="yw")

print(ar1_acf)
print(ar1_pacf)
```

典型结果：

- ACF 从 lag 1 开始逐步衰减。
- PACF 在 lag 1 很高，之后明显变小。

这符合 AR(1) 的特征：一阶滞后直接解释当前值。

## MA(1) 的自相关

构造 MA(1)：

```text
x_t = epsilon_t + 0.7 epsilon_{t-1}
```

```python
ma_noise = rng.normal(size=n_obs)
ma_values = np.zeros(n_obs)

for t in range(1, n_obs):
    ma_values[t] = ma_noise[t] + 0.7 * ma_noise[t - 1]

ma1 = pd.Series(ma_values, index=dates, name="ma1")
```

计算 ACF 和 PACF：

```python
ma1_acf = acf(ma1, nlags=5, fft=False)
ma1_pacf = pacf(ma1, nlags=5, method="yw")

print(ma1_acf)
print(ma1_pacf)
```

MA(1) 的 ACF 通常在 lag 1 后快速变小，而 PACF 会逐步衰减。

这也是为什么 ACF / PACF 常用于 ARMA 初步选阶。

## 白噪声检验

白噪声序列没有系统性自相关。

```python
white_noise = pd.Series(
    rng.normal(size=n_obs),
    index=dates,
    name="white_noise",
)
```

Ljung-Box 检验可以检查多个 lag 的自相关是否整体显著。

```python
lb_white = acorr_ljungbox(
    white_noise,
    lags=[10],
    return_df=True,
)

lb_ar1 = acorr_ljungbox(
    ar1,
    lags=[10],
    return_df=True,
)

print(lb_white)
print(lb_ar1)
```

Ljung-Box 的原假设是：

```text
到指定 lag 为止没有自相关
```

通常：

- 白噪声 p-value 较大。
- AR(1) p-value 很小。

拟合时间序列模型后，也常用 Ljung-Box 检查残差是否仍有自相关。

## 负自相关和 bid-ask bounce

在高频数据中，负一阶自相关可能来自 bid-ask bounce。

一个简化例子：

```python
true_return = rng.normal(loc=0.0, scale=0.01, size=n_obs)
bounce = np.array([0.003 * ((-1) ** t) for t in range(n_obs)])

observed_return = pd.Series(
    true_return + bounce,
    index=dates,
    name="observed_return",
)

observed_acf = acf(observed_return, nlags=3, fft=False)

print(observed_acf)
```

如果成交价在 bid 和 ask 之间来回跳，即使真实价格没有可预测性，观测收益也可能出现短期负自相关。

这类自相关未必能直接交易，因为：

- 买卖价差本身就是成本。
- 信号可能只是成交价格噪声。
- 延迟和排队会吃掉理论利润。

## 平方收益自相关

收益方向可能没有自相关，但平方收益可能有自相关。

这说明波动率有聚集。

构造一个 GARCH-like 过程：

```python
omega = 0.000002
alpha = 0.08
beta = 0.90

z = rng.normal(size=n_obs)
conditional_var = np.empty(n_obs)
return_values = np.empty(n_obs)

conditional_var[0] = omega / (1 - alpha - beta)
return_values[0] = np.sqrt(conditional_var[0]) * z[0]

for t in range(1, n_obs):
    conditional_var[t] = (
        omega
        + alpha * return_values[t - 1] ** 2
        + beta * conditional_var[t - 1]
    )
    return_values[t] = np.sqrt(conditional_var[t]) * z[t]

garch_like_return = pd.Series(
    return_values,
    index=dates,
    name="garch_like_return",
)
```

比较收益和平方收益：

```python
return_acf = acf(garch_like_return, nlags=5, fft=False)
squared_return_acf = acf(garch_like_return ** 2, nlags=5, fft=False)

lb_return = acorr_ljungbox(
    garch_like_return,
    lags=[10],
    return_df=True,
)

lb_squared_return = acorr_ljungbox(
    garch_like_return ** 2,
    lags=[10],
    return_df=True,
)

print(return_acf)
print(squared_return_acf)
print(lb_return)
print(lb_squared_return)
```

典型现象：

- 收益本身没有明显自相关。
- 平方收益有显著自相关。

这说明方向可能难预测，但风险状态有持续性。

## 自相关和简单策略

用 AR(1) 序列演示一个简单的滞后信号。

如果上一期为正，就做多；上一期为负，就做空：

```python
lag_signal = np.sign(ar1.shift(1)).fillna(0.0)
toy_pnl = lag_signal * ar1

toy_summary = pd.Series({
    "mean": toy_pnl.mean(),
    "std": toy_pnl.std(ddof=1),
    "positive_ratio": (toy_pnl > 0).mean(),
})

print(toy_summary)
```

这个例子只说明：正自相关序列中，过去方向可能对当前方向有信息。

真实交易中还需要：

- 用真实可成交价格。
- 扣除手续费和滑点。
- 考虑信号延迟。
- 样本外验证。
- 检查自相关是否稳定。

## 重叠收益造成的自相关

如果用重叠窗口计算 5 日收益：

```text
r_{t,t+5} = r_{t+1} + ... + r_{t+5}
r_{t+1,t+6} = r_{t+2} + ... + r_{t+6}
```

相邻两个 5 日收益共享 4 天数据，因此会机械地产生自相关。

这类自相关不是 alpha，而是构造方式造成的。

处理方式：

- 用非重叠样本。
- 使用 Newey-West 标准误。
- 明确 horizon 和重叠方式。
- 不把重叠收益自相关当作交易信号。

## 常见坑

第一，把统计自相关当成可交易收益。

自相关可能太弱、太短、成本太高，无法交易。

第二，忽略微观结构噪声。

高频负自相关可能来自 bid-ask bounce，而不是真实反转机会。

第三，忘记检查平方收益。

收益方向无自相关不代表风险不可预测。平方收益自相关常用于波动率建模。

第四，混淆 ACF 和 PACF。

ACF 是总相关，PACF 是控制中间 lag 后的直接相关。

第五，使用非平稳序列直接看 ACF。

随机游走的 ACF 会很高，但这通常是非平稳造成的，不是稳定预测关系。

第六，忽略多重检验。

检查很多资产、很多 lag，总会出现一些显著结果。必须做样本外验证。

## 实战提示

分析 autocorrelation 时可以按下面流程：

1. 先确认序列是否平稳。
2. 画 ACF / PACF 或打印主要 lag。
3. 用 Ljung-Box 检查多个 lag 的整体显著性。
4. 对收益、残差、平方收益分别检查。
5. 区分真实信号、构造自相关和微观结构噪声。
6. 用滞后信号交易下一期收益，避免同期期收益泄露。
7. 加入成本、延迟和容量后再判断可交易性。
8. 在滚动窗口和样本外检查稳定性。

## 小结

本节的重点：

- 自相关衡量 `x_t` 和 `x_{t-k}` 的相关性。
- ACF 是总相关，PACF 是控制中间 lag 后的直接相关。
- AR 模型常表现为 ACF 衰减、PACF 截尾。
- MA 模型常表现为 ACF 截尾、PACF 衰减。
- Ljung-Box 可以检验多个 lag 的整体自相关。
- 收益方向和平方收益的自相关含义不同。
- 自相关必须结合平稳性、成本、延迟和样本外稳定性解释。

## 自检问题

1. 自相关 `rho_k` 如何定义？
2. ACF 和 PACF 有什么区别？
3. AR(1) 和 MA(1) 的 ACF/PACF 典型形态有什么不同？
4. Ljung-Box 检验的原假设是什么？
5. 为什么平方收益自相关强不等于收益方向可预测？
6. 为什么重叠收益会机械地产生自相关？
