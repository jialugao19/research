# 38. statsmodels：与 sklearn 的区别、数据接口与结果对象

## 核心概念

`statsmodels` 和 `sklearn` 都能做线性模型，但关注点不同。

`sklearn` 更偏机器学习工程：

- 统一 estimator API：`fit`、`predict`、`transform`。
- 强调预测、交叉验证、pipeline、超参数搜索。
- 常用于机器学习模型训练和部署。

`statsmodels` 更偏统计建模和计量分析：

- 强调参数估计、标准误、t 值、p 值、置信区间。
- 提供 `summary()`、残差、诊断和统计检验。
- 支持公式接口，适合回归、时间序列、计量模型。

一句话：

- 想做预测流水线，优先想到 `sklearn`。
- 想解释系数、检验显著性、看回归表，优先想到 `statsmodels`。

本节先不深入 OLS 推导，只讲 statsmodels 的数据接口和结果对象。

## 准备环境

```python
import numpy as np
import pandas as pd

import statsmodels.api as sm
import statsmodels.formula.api as smf

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
```

准备一组可复现的因子数据：

```python
rng = np.random.default_rng(123)
n = 80

data = pd.DataFrame({
    "momentum": rng.normal(0.0, 1.0, size=n),
    "volatility": rng.lognormal(mean=-2.0, sigma=0.35, size=n),
    "size_score": rng.normal(0.0, 1.0, size=n),
    "sector": rng.choice(["tech", "finance", "energy"], size=n),
})

sector_effect = data["sector"].map({
    "tech": 0.006,
    "finance": 0.001,
    "energy": -0.004,
})

noise = rng.normal(0.0, 0.020, size=n)

data["future_return"] = (
    0.010
    + 0.020 * data["momentum"]
    - 0.030 * data["volatility"]
    + 0.006 * data["size_score"]
    + sector_effect
    + noise
)
```

这份数据里：

- `future_return`：未来收益，是被解释变量。
- `momentum`、`volatility`、`size_score`：数值解释变量。
- `sector`：类别变量。

## sklearn 的同类写法

先用 sklearn 拟合一个线性回归：

```python
feature_cols = ["momentum", "volatility", "size_score"]

X = data[feature_cols]
y = data["future_return"]

sk_model = LinearRegression()
sk_model.fit(X, y)

sk_coef = pd.Series(sk_model.coef_, index=feature_cols)
sk_pred = sk_model.predict(X)

print(sk_model.intercept_)
print(sk_coef)
print(r2_score(y, sk_pred))
```

sklearn 的输出适合继续做预测、评估和 pipeline。但它默认不提供标准误、t 值、p 值和回归表。

## statsmodels 矩阵接口

statsmodels 的矩阵接口接收：

- `endog`：被解释变量，也就是 y。
- `exog`：解释变量，也就是 X。

普通 OLS 写法：

```python
X_const = sm.add_constant(X)

ols_model = sm.OLS(endog=y, exog=X_const)
results = ols_model.fit()

print(results.params)
```

`sm.add_constant(X)` 会添加截距列 `const`。这是 statsmodels 与 sklearn 的一个重要区别：`sm.OLS` 不会自动添加截距。

## params、bse、tvalues 和 pvalues

`fit()` 返回的是结果对象。常用属性包括：

```python
print(results.params)
print(results.bse)
print(results.tvalues)
print(results.pvalues)
```

含义：

- `params`：估计出来的系数。
- `bse`：标准误。
- `tvalues`：t 统计量。
- `pvalues`：p 值。

这些是 statsmodels 的核心价值：它不只是给出预测，还给出参数估计的不确定性。

## conf_int：置信区间

置信区间可以用 `conf_int()` 查看。

```python
conf = results.conf_int(alpha=0.05)
conf.columns = ["lower", "upper"]

print(conf)
```

`alpha=0.05` 表示 95% 置信区间。置信区间很宽，说明系数估计不稳定；置信区间跨过 0，通常意味着该系数在当前模型和样本下不显著。

## fittedvalues 和 resid

结果对象还保存拟合值和残差。

```python
diagnostics = pd.DataFrame({
    "actual": y,
    "fitted": results.fittedvalues,
    "residual": results.resid,
})

print(diagnostics.head())
```

常用属性：

- `results.fittedvalues`：样本内拟合值。
- `results.resid`：残差，等于实际值减拟合值。
- `results.rsquared`：R-squared。
- `results.nobs`：样本数。

这些属性会在回归诊断里反复使用。

## predict：用新数据预测

矩阵接口预测时，新数据必须有与训练时一致的列。

```python
new_X = pd.DataFrame({
    "momentum": [0.5, -0.8],
    "volatility": [0.12, 0.20],
    "size_score": [0.3, -0.4],
})

new_X_const = sm.add_constant(new_X, has_constant="add")
pred = results.predict(new_X_const)

print(pred)
```

`has_constant="add"` 可以确保新数据也添加 `const` 列。预测数据的列名和列顺序要与训练时的 `exog` 保持一致。

## summary：回归表

`summary()` 会生成经典回归表。

```python
summary = results.summary()
summary_text = summary.as_text()

print(summary_text[:800])
```

回归表里通常会看到：

- 模型类型和样本数。
- R-squared 和 Adj. R-squared。
- 每个系数的估计值、标准误、t 值、p 值、置信区间。
- 一些残差分布和诊断统计量。

下一节会专门讲 OLS 的回归表如何阅读。

## 公式接口

statsmodels 支持类似 R 的公式接口。

```python
formula_results = smf.ols(
    "future_return ~ momentum + volatility + size_score + C(sector)",
    data=data,
).fit()

print(formula_results.params)
```

公式接口的特点：

- 左边是被解释变量。
- 右边是解释变量。
- 默认包含截距。
- `C(sector)` 表示把 `sector` 当作类别变量处理。

公式接口适合回归分析，因为它保留变量名，能自动处理类别变量，也让模型规格更容易读。

## 公式接口的预测

公式接口预测时，可以直接传入包含原始变量名的新 DataFrame。

```python
new_data = pd.DataFrame({
    "momentum": [0.5, -0.8],
    "volatility": [0.12, 0.20],
    "size_score": [0.3, -0.4],
    "sector": ["tech", "energy"],
})

formula_pred = formula_results.predict(new_data)

print(formula_pred)
```

这里不需要手动添加 `const`，也不需要手动 one-hot 编码 `sector`。公式接口会根据训练时的公式处理。

## get_prediction：预测区间

`predict()` 只返回点预测。`get_prediction()` 可以返回更完整的预测结果。

```python
pred_results = formula_results.get_prediction(new_data)
pred_frame = pred_results.summary_frame(alpha=0.05)

print(pred_frame)
```

常见列包括：

- `mean`：点预测。
- `mean_se`：均值预测的标准误。
- `mean_ci_lower` / `mean_ci_upper`：均值预测置信区间。
- `obs_ci_lower` / `obs_ci_upper`：单个观测值的预测区间。

预测区间通常比均值置信区间更宽，因为它还包含新观测自身的噪声。

## pandas index 和列名

使用 pandas 输入时，statsmodels 会尽量保留 index 和列名。

```python
print(results.params.index)
print(results.fittedvalues.index.equals(data.index))
print(results.resid.index.equals(data.index))
```

这对分析很重要：你可以把残差、拟合值、预测结果重新合并回原始 DataFrame。

```python
data_with_resid = data.assign(
    fitted=results.fittedvalues,
    residual=results.resid,
)

print(data_with_resid.head())
```

## 缺失值处理

回归前最好显式处理缺失值。公式接口可以用 `missing="drop"` 丢弃含缺失值的样本。

```python
data_missing = data.copy()
data_missing.loc[0, "momentum"] = np.nan

missing_results = smf.ols(
    "future_return ~ momentum + volatility + size_score",
    data=data_missing,
    missing="drop",
).fit()

print(missing_results.nobs)
```

缺失值不是纯技术细节。丢弃样本可能改变样本分布，也可能引入选择偏差。正式分析前要记录缺失处理方式。

## 常见坑

第一，忘记添加截距。

矩阵接口 `sm.OLS(y, X)` 不会自动添加截距。通常需要 `sm.add_constant(X)`。公式接口默认包含截距。

第二，把 p 值当成预测能力。

p 值描述的是在模型假设下，系数估计与 0 的关系。它不能替代样本外预测评估。

第三，预测数据列不一致。

矩阵接口预测时，新数据必须有与训练时一致的列，包括 `const`。公式接口预测时，新数据必须有公式里用到的原始变量。

第四，类别变量没有正确处理。

矩阵接口里，字符串类别变量不能直接进 OLS，需要 one-hot 编码。公式接口可以用 `C(variable)`。

第五，忽略结果对象。

statsmodels 的重点不只是 `predict`。`params`、`bse`、`pvalues`、`resid`、`summary()` 才是统计分析的主要入口。

## 实战提示

选择工具时可以这样判断：

1. 需要 pipeline、交叉验证、超参数搜索：优先 `sklearn`。
2. 需要回归表、标准误、p 值、置信区间：优先 `statsmodels`。
3. 需要处理类别变量和交互项并保持模型规格可读：考虑公式接口。
4. 需要正式预测评估：无论用哪个库，都要做样本外验证。
5. 需要解释模型：保存公式、样本筛选规则、缺失值处理方式和结果表。

一个常用分析模板：

```python
def fit_factor_regression(df):
    required = ["future_return", "momentum", "volatility", "size_score", "sector"]
    clean = df[required].dropna()

    result = smf.ols(
        "future_return ~ momentum + volatility + size_score + C(sector)",
        data=clean,
    ).fit()

    table = pd.DataFrame({
        "coef": result.params,
        "std_err": result.bse,
        "t": result.tvalues,
        "pvalue": result.pvalues,
    })

    return result, table


result, coef_table = fit_factor_regression(data)
print(coef_table)
```

这个模板把样本清洗、模型规格和系数表整理放在一起，适合作为回归分析的起点。

## 小结

本节的重点：

- `sklearn` 更偏预测工程，`statsmodels` 更偏统计推断。
- statsmodels 矩阵接口使用 `endog` 和 `exog`。
- 矩阵接口通常需要手动 `sm.add_constant(X)`。
- `fit()` 返回结果对象，核心属性包括 `params`、`bse`、`tvalues`、`pvalues`、`fittedvalues`、`resid`。
- `summary()` 生成经典回归表。
- 公式接口 `smf.ols("y ~ x1 + x2", data=df)` 更适合可读的统计模型规格。
- `get_prediction().summary_frame()` 可以查看预测区间。

## 自检问题

1. statsmodels 和 sklearn 的主要使用场景有什么区别？
2. 为什么 `sm.OLS` 矩阵接口通常要配合 `sm.add_constant`？
3. `params`、`bse`、`pvalues` 分别表示什么？
4. 公式接口里的 `C(sector)` 有什么作用？
5. `predict()` 和 `get_prediction().summary_frame()` 有什么区别？
