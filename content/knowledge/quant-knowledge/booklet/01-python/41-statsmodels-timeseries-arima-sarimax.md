# statsmodels：时间序列模型接口：ARIMA / SARIMAX 基础与预测结果

## 核心概念

statsmodels 里的时间序列模型常用于：

- 根据历史序列预测未来值。
- 建模自相关结构。
- 在预测中加入外生变量。
- 输出预测均值、标准误和预测区间。

本节聚焦两个常用接口：

- `ARIMA`：自回归、差分、移动平均模型。
- `SARIMAX`：更通用的状态空间模型，可包含季节项和外生变量。

先记住一个实用区分：

- 只根据序列自身历史预测：先考虑 `ARIMA`。
- 还要加入市场收益、宏观变量、节假日、事件变量等外生变量：考虑 `SARIMAX(exog=...)`。

时间序列建模最重要的工程原则是：按时间顺序训练和预测，不能随机打乱。

## 准备环境

```python
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
```

构造一组可复现的日频收益数据：

```python
rng = np.random.default_rng(41)

dates = pd.bdate_range("2024-01-02", periods=180)

market = pd.Series(
    rng.normal(0.0005, 0.010, size=len(dates)),
    index=dates,
    name="market_return",
)

strategy_values = np.empty(len(dates))
strategy_values[0] = 0.0

noise = rng.normal(0.0, 0.012, size=len(dates))

for t in range(1, len(dates)):
    strategy_values[t] = (
        0.0008
        + 0.35 * strategy_values[t - 1]
        + 0.45 * market.iloc[t]
        + noise[t]
    )

returns = pd.Series(
    strategy_values,
    index=dates,
    name="strategy_return",
)

nav = (1.0 + returns).cumprod()
```

这里的 `returns` 是平稳性更强的收益序列。价格、净值这类累计序列通常更容易有趋势，直接建 ARIMA 前要更谨慎。

## 保留时间索引和频率

时间序列模型最好使用带频率的 `DatetimeIndex`。

```python
print(returns.index)
print(returns.index.freq)
```

`pd.bdate_range(...)` 生成的是工作日频率，`freq='B'`。如果索引没有频率，statsmodels 仍然可能拟合，但预测索引可能退化成整数位置，或者产生频率相关警告。

## 按时间切分训练集和测试集

时间序列不能随机切分。应该用过去训练，用未来测试。

```python
horizon = 20

train = returns.iloc[:-horizon]
test = returns.iloc[-horizon:]

print(train.index.min(), train.index.max())
print(test.index.min(), test.index.max())
```

`horizon` 是预测步数。这里用前 160 个工作日训练，最后 20 个工作日测试。

## ARIMA 的 order=(p, d, q)

ARIMA 的三个参数：

- `p`：AR 项，使用多少阶历史值。
- `d`：差分阶数，用来处理非平稳趋势。
- `q`：MA 项，使用多少阶历史冲击。

常见例子：

- `ARIMA(order=(1, 0, 0))`：AR(1)，适合有一阶自相关的平稳序列。
- `ARIMA(order=(0, 1, 0))`：随机游走形式，对序列做一阶差分。
- `ARIMA(order=(1, 1, 1))`：对一阶差分后的序列建 ARMA(1,1)。

本节用收益序列演示，所以先使用 `order=(1, 0, 0)`。

## 拟合 ARIMA

```python
arima_model = ARIMA(
    train,
    order=(1, 0, 0),
    trend="c",
)

arima_results = arima_model.fit()

print(arima_results.params)
print(arima_results.aic)
print(arima_results.bic)
```

`trend="c"` 表示包含常数项。结果对象和回归模型类似，也有 `params`、`aic`、`bic`、`summary()` 等属性。

## 查看 summary

```python
summary_text = arima_results.summary().as_text()

print(summary_text[:1000])
```

ARIMA 的 summary 会包含：

- 参数估计，例如常数项、AR 系数和误差方差。
- 标准误、z 值、p 值和置信区间。
- AIC、BIC 等信息准则。
- 残差诊断统计量。

时间序列模型的 summary 仍然只是样本内信息，不能替代样本外预测检验。

## 样本内预测

`get_prediction` 可以取某段样本内拟合预测。

```python
in_sample_pred = arima_results.get_prediction(
    start=train.index[20],
    end=train.index[-1],
)

in_sample_mean = in_sample_pred.predicted_mean

print(in_sample_mean.head())
```

`predicted_mean` 是点预测。样本内预测常用于查看模型是否大致跟随数据，但真正评估要看样本外。

## 样本外预测：get_forecast

预测未来 20 个工作日：

```python
forecast = arima_results.get_forecast(steps=len(test))
forecast_frame = forecast.summary_frame(alpha=0.05)

print(forecast_frame.head())
```

`summary_frame` 常见列：

- `mean`：点预测。
- `mean_se`：预测均值的标准误。
- `mean_ci_lower` / `mean_ci_upper`：预测均值的置信区间。

预测结果的索引会延续训练序列的时间索引。

```python
print(forecast_frame.index.equals(test.index))
```

如果这里是 `False`，通常要检查输入序列是否有明确频率。

## 简单预测评估

把预测均值和测试集对齐：

```python
forecast_mean = forecast_frame["mean"]

error = test - forecast_mean

mae = error.abs().mean()
rmse = np.sqrt((error ** 2).mean())

print(mae)
print(rmse)
```

MAE 和 RMSE 都是误差指标。RMSE 对大误差更敏感。

## 画预测和区间

```python
fig, ax = plt.subplots(figsize=(9, 4))

ax.plot(train.index[-60:], train.iloc[-60:], label="train")
ax.plot(test.index, test, label="test", color="tab:orange")
ax.plot(forecast_frame.index, forecast_frame["mean"], label="forecast", color="tab:green")

ax.fill_between(
    forecast_frame.index,
    forecast_frame["mean_ci_lower"],
    forecast_frame["mean_ci_upper"],
    color="tab:green",
    alpha=0.20,
)

ax.axhline(0.0, color="black", linewidth=1)
ax.set_title("ARIMA Forecast")
ax.set_ylabel("Return")
ax.legend()

fig.tight_layout()
plt.close(fig)
```

预测区间通常会随着预测步数增加而变宽。点预测只是一个中心值，不应该忽略不确定性。

## 残差诊断

ARIMA 结果对象也可以画诊断图。

```python
fig = arima_results.plot_diagnostics(figsize=(10, 8))

plt.close(fig)
```

诊断图通常包括标准化残差、残差分布、QQ 图和残差自相关。理想情况下，残差应接近白噪声，不再有明显自相关结构。

## SARIMAX：加入外生变量

如果策略收益受到市场收益影响，可以把市场收益作为外生变量。

```python
exog = market.to_frame()

train_exog = exog.iloc[:-horizon]
test_exog = exog.iloc[-horizon:]

sarimax_model = SARIMAX(
    train,
    exog=train_exog,
    order=(1, 0, 0),
    trend="c",
    enforce_stationarity=True,
    enforce_invertibility=True,
)

sarimax_results = sarimax_model.fit(disp=False)

print(sarimax_results.params)
```

`exog` 必须与被建模序列按时间严格对齐。训练时的 `train_exog` 和 `train` 行数要一致。

## SARIMAX 预测时必须提供未来 exog

如果模型训练时用了外生变量，预测未来时也必须提供未来对应的外生变量。

```python
sarimax_forecast = sarimax_results.get_forecast(
    steps=len(test),
    exog=test_exog,
)

sarimax_frame = sarimax_forecast.summary_frame(alpha=0.05)

print(sarimax_frame.head())
print(sarimax_frame.index.equals(test.index))
```

这一步在真实预测中很关键：如果你不知道未来外生变量，就不能直接用真实未来外生变量预测。比如未来市场收益在预测时通常是未知的，除非你是在做情景分析或已经有外生变量预测。

## 比较 ARIMA 和 SARIMAX 预测

```python
comparison = pd.DataFrame({
    "actual": test,
    "arima": forecast_frame["mean"],
    "sarimax": sarimax_frame["mean"],
})

comparison["arima_error"] = comparison["actual"] - comparison["arima"]
comparison["sarimax_error"] = comparison["actual"] - comparison["sarimax"]

metrics = pd.Series({
    "arima_mae": comparison["arima_error"].abs().mean(),
    "sarimax_mae": comparison["sarimax_error"].abs().mean(),
    "arima_rmse": np.sqrt((comparison["arima_error"] ** 2).mean()),
    "sarimax_rmse": np.sqrt((comparison["sarimax_error"] ** 2).mean()),
})

print(metrics)
```

外生变量是否有用，要看样本外误差和业务合理性，而不是只看样本内 p 值。

## 更新结果对象：append

当新观测到来后，可以把测试集追加到已有结果对象。

```python
extended_results = sarimax_results.append(
    test,
    exog=test_exog,
    refit=False,
)

print(len(extended_results.fittedvalues))
```

`refit=False` 表示不重新估计参数，只用新数据更新状态。这适合在线更新预测状态。定期重新估计参数仍然很重要，因为市场结构可能变化。

## 常见坑

第一，随机切分时间序列。

时间序列必须用过去预测未来。随机切分会把未来信息泄露到训练中。

第二，对非平稳价格序列直接套 ARIMA。

价格、净值、成交量等序列可能有趋势或单位根。通常先看收益、差分、对数差分，或设置合适的 `d`。

第三，忽略索引频率。

没有频率的日期索引会影响预测索引。尽量使用 `pd.date_range`、`pd.bdate_range` 或显式设置频率。

第四，SARIMAX 预测时使用真实未来 exog。

如果未来外生变量在预测时不可知，直接使用真实未来值就是未来信息泄露。只能使用当时可得的预测值、场景假设或已知日历变量。

第五，只看 AIC / BIC 不看样本外误差。

AIC / BIC 是样本内模型比较指标。预测任务必须看样本外表现。

## 实战提示

一个基础流程：

1. 确认序列索引是按时间排序的 `DatetimeIndex`。
2. 确认是否有明确频率。
3. 按时间切分训练集和测试集。
4. 对收益或差分序列建模，不要盲目对价格建模。
5. 从简单模型开始，例如 `ARIMA(1, 0, 0)`。
6. 使用 `get_forecast().summary_frame()` 查看预测和区间。
7. 用测试集计算 MAE / RMSE。
8. 使用外生变量时，严格检查 exog 时间对齐和未来可得性。

一个预测模板：

```python
def fit_arima_forecast(series, order=(1, 0, 0), horizon=20):
    series = series.sort_index()
    train = series.iloc[:-horizon]
    test = series.iloc[-horizon:]

    result = ARIMA(train, order=order, trend="c").fit()
    forecast = result.get_forecast(steps=horizon).summary_frame()

    comparison = pd.DataFrame({
        "actual": test,
        "forecast": forecast["mean"],
        "lower": forecast["mean_ci_lower"],
        "upper": forecast["mean_ci_upper"],
    })

    error = comparison["actual"] - comparison["forecast"]
    metrics = pd.Series({
        "mae": error.abs().mean(),
        "rmse": np.sqrt((error ** 2).mean()),
        "aic": result.aic,
        "bic": result.bic,
    })

    return result, comparison, metrics


result, comparison, metrics = fit_arima_forecast(
    returns,
    order=(1, 0, 0),
    horizon=20,
)

print(comparison.head())
print(metrics)
```

这个模板只适合基础起点。正式时间序列建模还要检查平稳性、自相关、残差、结构变化和样本外稳定性。

## 小结

本节的重点：

- `ARIMA(order=(p, d, q))` 用于建模序列自身的自相关和差分结构。
- `SARIMAX` 可以加入外生变量 `exog`，也能扩展到季节结构。
- 时间序列必须按时间切分，不能随机打乱。
- `get_forecast(steps)` 返回预测结果对象。
- `summary_frame()` 提供点预测、标准误和预测区间。
- 使用外生变量预测时，未来 `exog` 必须在预测时真实可得或来自独立预测。
- AIC / BIC 不能替代样本外预测误差。

## 自检问题

1. ARIMA 的 `order=(p, d, q)` 中，`p`、`d`、`q` 分别表示什么？
2. 为什么时间序列不能随机 train/test split？
3. `get_forecast().summary_frame()` 里常见的 `mean` 和 `mean_ci_lower` 是什么？
4. SARIMAX 使用 `exog` 时，预测未来为什么也需要未来 exog？
5. 为什么 AIC / BIC 不能替代样本外 MAE / RMSE？
