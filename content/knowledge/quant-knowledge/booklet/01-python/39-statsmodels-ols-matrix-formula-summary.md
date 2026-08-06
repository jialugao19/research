# 39. statsmodels：OLS 矩阵接口、公式接口与 summary 解读

## 核心概念

OLS 是 Ordinary Least Squares，普通最小二乘回归。它估计的是：

```text
y = beta_0 + beta_1 x_1 + beta_2 x_2 + ... + error
```

OLS 的目标是让残差平方和最小：

```text
sum((y_i - fitted_i)^2)
```

在 statsmodels 中，OLS 最常用两种接口：

- 矩阵接口：`sm.OLS(y, X).fit()`。
- 公式接口：`smf.ols("y ~ x1 + x2", data=df).fit()`。

本节重点讲：

- 如何正确构造 OLS 输入。
- 为什么矩阵接口要手动加截距。
- 公式接口如何处理截距、类别变量和交互项。
- `summary()` 中常见字段怎么读。
- 如何把模型结果整理成 DataFrame。

## 准备环境

```python
import numpy as np
import pandas as pd

import statsmodels.api as sm
import statsmodels.formula.api as smf
```

准备一组可复现的横截面回归数据：

```python
rng = np.random.default_rng(2024)
n = 120

data = pd.DataFrame({
    "momentum": rng.normal(0.0, 1.0, size=n),
    "value": rng.normal(0.0, 1.0, size=n),
    "volatility": rng.lognormal(mean=-2.0, sigma=0.45, size=n),
    "sector": rng.choice(["tech", "finance", "energy"], size=n),
})

sector_effect = data["sector"].map({
    "tech": 0.010,
    "finance": 0.002,
    "energy": -0.006,
})

noise = rng.normal(0.0, 0.025, size=n)

data["future_return"] = (
    0.008
    + 0.018 * data["momentum"]
    + 0.010 * data["value"]
    - 0.045 * data["volatility"]
    + sector_effect
    + noise
)
```

这类数据可以理解为某一期横截面股票样本：

- `future_return`：未来收益。
- `momentum`、`value`、`volatility`：因子暴露。
- `sector`：行业分类。

## 矩阵接口：最基础 OLS

矩阵接口接收 `y` 和 `X`。

```python
y = data["future_return"]
X = data[["momentum", "value", "volatility"]]

X_const = sm.add_constant(X)

model = sm.OLS(y, X_const)
results = model.fit()

print(results.params)
```

`sm.add_constant(X)` 添加截距列 `const`。没有截距时，模型会被强制穿过原点，这通常不是你想要的。

## 截距的重要性

比较有截距和无截距的模型：

```python
results_no_const = sm.OLS(y, X).fit()

print(results.rsquared)
print(results_no_const.rsquared)
print(results.params.index)
print(results_no_const.params.index)
```

有截距模型的参数里有 `const`，无截距模型没有。除非你有明确的理论理由，否则线性回归通常应该包含截距。

注意：不同截距设定下，R-squared 的含义也可能不同，不要简单比较两个模型的 R-squared。

## summary 的整体结构

`summary()` 是 statsmodels 最常用的回归表入口。

```python
summary = results.summary()
summary_text = summary.as_text()

print(summary_text)
```

回归表大致分三块：

- 顶部：模型类型、样本数、R-squared、F-statistic、AIC、BIC 等整体信息。
- 中间：每个系数的估计值、标准误、t 值、p 值、置信区间。
- 底部：残差分布、Durbin-Watson、Jarque-Bera、Condition Number 等诊断信息。

本节先解释最常见字段；更深入的诊断放到下一节。

## summary 顶部字段

常见顶部字段：

- `Dep. Variable`：被解释变量。
- `Model`：模型类型，这里是 OLS。
- `No. Observations`：样本数。
- `Df Residuals`：残差自由度。
- `Df Model`：模型解释变量自由度，不含截距。
- `R-squared`：样本内解释度。
- `Adj. R-squared`：调整后的 R-squared。
- `F-statistic`：整体模型显著性检验统计量。
- `Prob (F-statistic)`：整体模型显著性检验的 p 值。
- `AIC` / `BIC`：信息准则，常用于比较同类模型。

这些字段也可以从结果对象直接读取：

```python
top_metrics = pd.Series({
    "nobs": results.nobs,
    "df_model": results.df_model,
    "df_resid": results.df_resid,
    "rsquared": results.rsquared,
    "rsquared_adj": results.rsquared_adj,
    "fvalue": results.fvalue,
    "f_pvalue": results.f_pvalue,
    "aic": results.aic,
    "bic": results.bic,
})

print(top_metrics)
```

`R-squared` 高不代表模型可用于交易或预测。它只是样本内拟合程度，仍然需要样本外验证。

## 系数表字段

中间的系数表是最常读的一部分。

```python
coef_table = pd.DataFrame({
    "coef": results.params,
    "std_err": results.bse,
    "t": results.tvalues,
    "pvalue": results.pvalues,
})

conf = results.conf_int(alpha=0.05)
conf.columns = ["ci_lower", "ci_upper"]

coef_table = coef_table.join(conf)

print(coef_table)
```

字段含义：

- `coef`：系数估计值。
- `std_err`：标准误。
- `t`：t 统计量，约等于 `coef / std_err`。
- `pvalue`：在模型假设下，检验该系数为 0 的 p 值。
- `ci_lower` / `ci_upper`：置信区间上下界。

如果 `momentum` 的系数是正的，表示在控制其他变量后，`momentum` 越高，`future_return` 的线性预测越高。

## p 值的正确语境

p 值经常被误读。

可以说：

- 在当前模型设定、样本和误差假设下，某个系数与 0 的差异是否明显。

不应该说：

- p 值小就一定能赚钱。
- p 值小就一定有样本外预测能力。
- p 值大就一定没有经济意义。

统计显著性、经济显著性和样本外稳定性是三件不同的事。

## 公式接口：更可读的模型规格

同一个模型可以用公式接口写：

```python
formula_results = smf.ols(
    "future_return ~ momentum + value + volatility",
    data=data,
).fit()

print(formula_results.params)
```

公式接口默认包含截距。这个公式等价于：

```text
future_return = Intercept + beta1 * momentum + beta2 * value + beta3 * volatility + error
```

如果明确不要截距，可以写：

```python
formula_no_intercept = smf.ols(
    "future_return ~ 0 + momentum + value + volatility",
    data=data,
).fit()

print(formula_no_intercept.params.index)
```

`0 +` 或 `- 1` 都可以移除截距。普通回归里不要随手去掉截距。

## 类别变量：C()

公式接口可以直接处理类别变量。

```python
sector_results = smf.ols(
    "future_return ~ momentum + value + volatility + C(sector)",
    data=data,
).fit()

print(sector_results.params)
```

`C(sector)` 会把行业变量展开成虚拟变量，并自动选择一个基准组。

例如参数里可能出现：

```text
C(sector)[T.finance]
C(sector)[T.tech]
```

这些系数表示相对基准行业的差异。基准组不会单独出现在参数表中。

## 指定类别基准组

如果想明确指定基准组，可以先把列转成有序类别。

```python
sector_ordered = data.copy()
sector_ordered["sector"] = pd.Categorical(
    sector_ordered["sector"],
    categories=["energy", "finance", "tech"],
)

ordered_results = smf.ols(
    "future_return ~ momentum + value + volatility + C(sector)",
    data=sector_ordered,
).fit()

print(ordered_results.params.index)
```

这里 `energy` 是第一个类别，通常会成为基准组。明确基准组能让回归表更容易解释。

## 交互项

公式接口也适合写交互项。

```python
interaction_results = smf.ols(
    "future_return ~ momentum + value + volatility + momentum:volatility",
    data=data,
).fit()

print(interaction_results.params)
```

`momentum:volatility` 表示只加入交互项，不自动加入主效应。

如果写：

```python
expanded_interaction = smf.ols(
    "future_return ~ momentum * volatility + value",
    data=data,
).fit()

print(expanded_interaction.params)
```

`momentum * volatility` 等价于：

```text
momentum + volatility + momentum:volatility
```

交互项表示一个变量的影响会随另一个变量变化而变化。

## AIC / BIC 比较模型

AIC 和 BIC 常用于比较同一数据、同一响应变量下的模型。

```python
simple_results = smf.ols(
    "future_return ~ momentum + value",
    data=data,
).fit()

full_results = smf.ols(
    "future_return ~ momentum + value + volatility + C(sector)",
    data=data,
).fit()

comparison = pd.DataFrame({
    "model": ["simple", "full"],
    "aic": [simple_results.aic, full_results.aic],
    "bic": [simple_results.bic, full_results.bic],
    "adj_r2": [simple_results.rsquared_adj, full_results.rsquared_adj],
})

print(comparison)
```

一般来说，AIC / BIC 越低越好，调整 R-squared 越高越好。但它们不是自动选模型的理由，还要结合业务解释、稳定性和样本外表现。

## 从 summary 提取表格

`summary()` 是给人看的文本表。写程序时更推荐从结果对象提取结构化数据。

```python
def make_ols_report(result):
    conf = result.conf_int()
    conf.columns = ["ci_lower", "ci_upper"]

    coef = pd.DataFrame({
        "coef": result.params,
        "std_err": result.bse,
        "t": result.tvalues,
        "pvalue": result.pvalues,
    }).join(conf)

    metrics = pd.Series({
        "nobs": result.nobs,
        "rsquared": result.rsquared,
        "rsquared_adj": result.rsquared_adj,
        "aic": result.aic,
        "bic": result.bic,
    })

    return coef, metrics


coef, metrics = make_ols_report(full_results)

print(coef)
print(metrics)
```

这样做比解析 `summary().as_text()` 更稳定。

## 常见坑

第一，矩阵接口忘记加截距。

`sm.OLS(y, X)` 不会自动加截距。大多数情况下应该先 `sm.add_constant(X)`。

第二，公式接口和矩阵接口的列不一致。

公式接口默认有截距，还会自动展开类别变量。矩阵接口需要你自己准备好所有列。

第三，把 R-squared 当成样本外收益。

R-squared 是样本内拟合指标，不能替代回测、交叉验证或未来样本检验。

第四，机械筛选 p 值。

反复尝试变量直到 p 值显著，会带来多重检验和数据挖掘偏差。模型规格应该尽量由理论、业务逻辑和预先假设驱动。

第五，直接比较不同样本上的 AIC / BIC。

AIC / BIC 适合比较同一响应变量、同一数据样本上的模型。样本不同，比较意义会弱很多。

## 实战提示

OLS 分析可以按这个流程做：

1. 明确被解释变量和解释变量。
2. 检查样本筛选、缺失值处理和变量单位。
3. 先用公式接口写出可读模型规格。
4. 查看系数方向和数量级是否符合预期。
5. 查看标准误、p 值和置信区间，但不把它们当成唯一结论。
6. 对比简单模型和完整模型。
7. 把系数表和整体指标整理成结构化 DataFrame。
8. 下一步做残差、异方差、影响点等诊断。

一个简洁模板：

```python
def fit_and_summarize_ols(formula, df):
    result = smf.ols(formula, data=df).fit()

    conf = result.conf_int()
    conf.columns = ["ci_lower", "ci_upper"]

    coef_table = pd.DataFrame({
        "coef": result.params,
        "std_err": result.bse,
        "t": result.tvalues,
        "pvalue": result.pvalues,
    }).join(conf)

    model_metrics = pd.Series({
        "nobs": result.nobs,
        "rsquared": result.rsquared,
        "rsquared_adj": result.rsquared_adj,
        "aic": result.aic,
        "bic": result.bic,
    })

    return result, coef_table, model_metrics


result, coef_table, model_metrics = fit_and_summarize_ols(
    "future_return ~ momentum + value + volatility + C(sector)",
    data,
)

print(coef_table)
print(model_metrics)
```

这个模板把 OLS 拟合、系数表和模型指标打包在一起，适合后续接报告生成。

## 小结

本节的重点：

- OLS 估计线性模型，使残差平方和最小。
- 矩阵接口 `sm.OLS(y, X)` 不自动添加截距。
- 公式接口 `smf.ols("y ~ x1 + x2", data=df)` 默认包含截距。
- `summary()` 的顶部是整体模型信息，中间是系数表，底部是诊断统计。
- `coef`、`std err`、`t`、`P>|t|`、置信区间是系数表核心字段。
- `C(variable)` 用于类别变量，`:` 和 `*` 用于交互项。
- 写程序时优先从结果对象提取结构化表格，而不是解析 summary 文本。

## 自检问题

1. 为什么矩阵接口通常需要 `sm.add_constant(X)`？
2. `summary()` 的顶部、中间和底部大致分别展示什么？
3. `coef`、`std err`、`t`、`P>|t|` 分别表示什么？
4. 公式接口里的 `momentum:volatility` 和 `momentum * volatility` 有什么区别？
5. AIC / BIC 适合在什么前提下比较模型？
