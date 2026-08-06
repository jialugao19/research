# 时间序列：ARIMA 的平稳化、AR / I / MA 含义、拟合与预测

## 核心概念

ARIMA 是 AutoRegressive Integrated Moving Average。

常写作：

```text
ARIMA(p, d, q)
```

其中：

- `p`：AR 阶数，使用过去的序列值解释当前值。
- `d`：差分阶数，用来把非平稳序列变得更接近平稳。
- `q`：MA 阶数，使用过去的误差项解释当前值。

直觉上：

```text
ARIMA = 先差分平稳化 + 对差分后的序列建 ARMA 模型
```

如果 `d = 0`，ARIMA 就退化成 ARMA。

## ARIMA 回答的问题

ARIMA 主要用于刻画和预测单变量时间序列。

它适合回答：

- 序列是否需要差分？
- 当前值是否和过去值有关？
- 当前冲击是否会在未来几期继续影响序列？
- 短期预测区间如何变化？

它不适合单独解决：

- 非线性 regime 切换。
- 波动率聚集。
- 多变量长期均衡关系。
- 高频市场微观结构噪声。

这些问题通常需要 GARCH、状态空间模型、协整模型或更复杂的机器学习模型。

## 准备环境

```python
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf
```

构造一个非平稳价格序列。它的日变化量带有 ARMA 结构：

```python
rng = np.random.default_rng(65)

n_obs = 260
dates = pd.bdate_range("2024-01-02", periods=n_obs)

eps = rng.normal(loc=0.0, scale=0.8, size=n_obs)
diff_values = np.zeros(n_obs)

for t in range(2, n_obs):
    diff_values[t] = (
        0.45 * diff_values[t - 1]
        - 0.25 * diff_values[t - 2]
        + eps[t]
        + 0.35 * eps[t - 1]
    )

price = pd.Series(
    100 + np.cumsum(0.03 + diff_values),
    index=dates,
    name="price",
)

print(price.head())
```

这里 `price` 是价格水平，通常不是平稳序列。

`diff_values` 是价格变化，带有 AR 和 MA 结构。

## 平稳性和差分

时间序列建模常先检查平稳性。

平稳的粗略含义是：

- 均值不随时间系统性漂移。
- 方差相对稳定。
- 自相关结构不随时间改变。

ARMA 要求序列平稳。ARIMA 通过差分处理非平稳。

先做 ADF 检验：

```python
adf_price = adfuller(price)

print(adf_price[0])
print(adf_price[1])
```

ADF 的原假设是存在单位根，即序列非平稳。`p-value` 较大时，通常不能拒绝非平稳。

对价格做一阶差分：

```python
price_diff = price.diff().dropna()

adf_diff = adfuller(price_diff)

print(adf_diff[0])
print(adf_diff[1])
```

如果差分后 `p-value` 变小，说明一阶差分后更接近平稳。

这对应 ARIMA 中的 `d = 1`。

## AR、I、MA 分别是什么

AR 部分：

```text
y_t = phi_1 y_{t-1} + ... + phi_p y_{t-p} + error_t
```

它表示当前值和过去值有关。

MA 部分：

```text
y_t = error_t + theta_1 error_{t-1} + ... + theta_q error_{t-q}
```

它表示过去的冲击会继续影响当前值。

I 部分：

```text
差分 d 次后再建 ARMA
```

例如 `ARIMA(2, 1, 1)` 表示：

```text
对原序列做一阶差分，然后对差分序列拟合 ARMA(2, 1)
```

## 拟合 ARIMA(2, 1, 1)

因为模拟数据的差分项包含 2 阶 AR 和 1 阶 MA，所以拟合 `ARIMA(2, 1, 1)`：

```python
model = ARIMA(price, order=(2, 1, 1), trend="t")
result = model.fit()

print(result.params)
print(result.aic)
```

这里 `trend="t"` 表示在差分方程中允许线性时间趋势，对应差分后的常数漂移。

在真实研究中，不应该因为知道数据生成过程就直接选阶。这里是教学例子。

## 预测未来几期

做 5 个交易日预测：

```python
forecast_result = result.get_forecast(steps=5)
forecast_mean = forecast_result.predicted_mean
forecast_interval = forecast_result.conf_int()

forecast_table = pd.DataFrame({
    "forecast": forecast_mean,
    "lower": forecast_interval.iloc[:, 0],
    "upper": forecast_interval.iloc[:, 1],
})

print(forecast_table)
```

ARIMA 预测通常会给出：

- 点预测。
- 预测区间。
- 预测误差方差。

预测 horizon 越长，不确定性通常越大。

## 残差诊断

拟合后不能只看参数，还要看残差。

如果模型抓住了主要时间结构，残差应该接近白噪声。

```python
residual = pd.Series(result.resid, index=price.index).iloc[5:]

residual_acf = acf(residual, nlags=5, fft=False)

print(residual.mean())
print(residual.std(ddof=1))
print(residual_acf)
```

`residual_acf` 中除 lag 0 以外的自相关应接近 0。

如果残差仍有明显自相关，说明模型阶数可能不足，或者序列存在结构变化、季节性或非线性。

## 简单选阶

真实建模常会尝试多个 `(p, d, q)`，用 AIC / BIC 和残差诊断共同判断。

下面用很小的网格搜索示例：

```python
candidate_rows = []

for p in [0, 1, 2, 3]:
    for q in [0, 1, 2]:
        fitted = ARIMA(price, order=(p, 1, q), trend="t").fit()

        candidate_rows.append({
            "p": p,
            "d": 1,
            "q": q,
            "aic": fitted.aic,
            "bic": fitted.bic,
        })

candidate_table = (
    pd.DataFrame(candidate_rows)
    .sort_values("aic")
    .reset_index(drop=True)
)

print(candidate_table.head())
```

注意：

- AIC 越低不一定实盘预测越好。
- 高阶模型更容易过拟合。
- 必须保留样本外验证。
- 时间序列不能随机打乱做 train / test split。

## train / test 切分

时间序列验证要按时间顺序切分。

```python
train = price.iloc[:220]
test = price.iloc[220:]

train_model = ARIMA(train, order=(2, 1, 1), trend="t").fit()
test_forecast = train_model.get_forecast(steps=len(test)).predicted_mean

forecast_error = test - test_forecast
mae = forecast_error.abs().mean()
rmse = np.sqrt((forecast_error ** 2).mean())

print(mae)
print(rmse)
```

这里是一次性预测后面所有点。实际预测系统更常见的是 walk-forward：

```text
每到一个新日期，只使用当时之前的数据重新拟合或更新模型，再预测下一期。
```

这样更接近真实交易环境。

## ARIMA 在金融里的位置

ARIMA 更适合建模：

- 宏观经济序列。
- 利率、库存、销量等低频序列。
- 平稳化后的价差或指标。
- 短期均值回复过程。

对股票价格本身，ARIMA 往往很难给出稳定 alpha，因为价格接近随机游走，收益噪声很大。

在量化研究中，ARIMA 更常作为：

- 时间序列建模基础。
- 预测基准模型。
- 残差自相关诊断工具。
- 更复杂模型前的 sanity check。

## 常见坑

第一，对非平稳价格直接拟合 ARMA。

如果序列有单位根，直接拟合 ARMA 会产生伪回归和不稳定预测。通常要先差分或做其他平稳化处理。

第二，过度差分。

差分太多会丢失有用结构，并引入额外噪声。`d` 不是越大越好。

第三，只看 AIC，不看残差和样本外。

低 AIC 可能来自样本内过拟合。残差诊断和时间顺序样本外验证同样重要。

第四，把预测区间当成风险上限。

ARIMA 预测区间依赖模型假设。结构突变、极端事件和波动率变化会让真实误差远大于区间。

第五，随机打乱时间序列做交叉验证。

时间序列有时间顺序，随机切分会泄露未来信息。

第六，忽略季节性。

有日内、周内、月度或季度季节性的序列，可能需要 SARIMA 或额外季节项。

## 实战提示

使用 ARIMA 时可以按下面流程：

1. 画出序列和差分序列。
2. 检查平稳性，包括 ADF、滚动均值、滚动方差。
3. 决定差分阶数 `d`。
4. 用 ACF / PACF 或小网格选择 `p` 和 `q`。
5. 拟合模型并检查参数稳定性。
6. 检查残差是否接近白噪声。
7. 用时间顺序 train / test 或 walk-forward 验证预测。
8. 与 naive forecast、移动平均等简单基准比较。
9. 在交易策略中加入成本、延迟和风险控制后再评估。

## 小结

本节的重点：

- ARIMA(p, d, q) 是差分后的 ARMA 模型。
- `d` 用于平稳化，`p` 描述过去值影响，`q` 描述过去冲击影响。
- ADF 检验常用于检查单位根，但不能替代业务判断。
- 拟合后要做残差诊断。
- AIC / BIC 可以辅助选阶，但不能替代样本外验证。
- 时间序列验证必须保持时间顺序，避免未来信息泄露。

## 自检问题

1. ARIMA(p, d, q) 中 `p`、`d`、`q` 分别代表什么？
2. 为什么非平稳价格序列通常不能直接拟合 ARMA？
3. ADF 检验的原假设是什么？
4. 为什么过度差分可能有害？
5. 拟合 ARIMA 后为什么要看残差自相关？
6. 为什么时间序列 train / test 不能随机打乱？
