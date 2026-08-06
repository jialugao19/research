# 40. statsmodels：回归诊断、异方差、稳健标准误与影响点

## 核心概念

OLS 拟合完成后，不能只看系数和 p 值。还要问：

- 残差是否有明显结构？
- 残差方差是否随解释变量或拟合值变化？
- 标准误是否可能被异方差低估？
- 有没有少数样本强烈影响系数？
- 某个结论是否由一两个极端点驱动？

本节关注 OLS 诊断中最常用的四类工具：

- 残差诊断：`fittedvalues`、`resid`、标准化残差。
- 异方差检验：Breusch-Pagan、White test。
- 稳健标准误：HC0 / HC1 / HC2 / HC3。
- 影响点分析：leverage、studentized residual、Cook's distance。

这些诊断不会自动“修好”模型，但能告诉你当前回归表有多可信。

## 准备环境

```python
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
```

准备一组带异方差和少量影响点的数据：

```python
rng = np.random.default_rng(40)
n = 160

data = pd.DataFrame({
    "momentum": rng.normal(0.0, 1.0, size=n),
    "value": rng.normal(0.0, 1.0, size=n),
    "volatility": rng.lognormal(mean=-2.0, sigma=0.55, size=n),
})

data.loc[0, ["momentum", "value", "volatility"]] = [4.2, -3.5, 0.42]
data.loc[1, ["momentum", "value", "volatility"]] = [-4.0, 3.2, 0.38]

vol_scaled = (
    (data["volatility"] - data["volatility"].min())
    / (data["volatility"].max() - data["volatility"].min())
)
error_scale = 0.010 + 0.050 * vol_scaled
noise = rng.normal(0.0, error_scale)

data["future_return"] = (
    0.008
    + 0.020 * data["momentum"]
    + 0.012 * data["value"]
    - 0.045 * data["volatility"]
    + noise
)

data.loc[0, "future_return"] += 0.12
```

这里故意让噪声规模随 `volatility` 变化，并加入少数极端样本，方便演示诊断工具。

## 拟合 OLS

先拟合一个普通 OLS：

```python
formula = "future_return ~ momentum + value + volatility"

results = smf.ols(formula, data=data).fit()

print(results.params)
print(results.summary())
```

这张回归表给出普通 OLS 标准误。后面会看到，如果存在异方差，普通标准误和 p 值可能不可靠。

## 残差和拟合值

最基础的诊断表：

```python
diagnostics = pd.DataFrame({
    "actual": data["future_return"],
    "fitted": results.fittedvalues,
    "residual": results.resid,
})

print(diagnostics.head())
```

残差定义为：

```text
residual = actual - fitted
```

如果模型设定合理，残差应该围绕 0 随机分布，而不是随拟合值或某个变量呈现明显结构。

## 残差 vs 拟合值

残差图是最常用的第一张诊断图。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.scatter(results.fittedvalues, results.resid, alpha=0.7)
ax.axhline(0.0, color="black", linewidth=1, linestyle="--")

ax.set_title("Residual vs Fitted")
ax.set_xlabel("Fitted value")
ax.set_ylabel("Residual")

fig.tight_layout()
plt.close(fig)
```

如果残差出现漏斗形，说明误差方差可能不是常数。如果残差出现曲线形，说明线性模型可能漏掉了非线性结构。

## 残差分布和 QQ 图

可以同时看残差直方图和 QQ 图。

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)

axes[0].hist(results.resid, bins=30)
axes[0].axvline(0.0, color="black", linewidth=1, linestyle="--")
axes[0].set_title("Residual Distribution")
axes[0].set_xlabel("Residual")

sm.qqplot(results.resid, line="45", fit=True, ax=axes[1])
axes[1].set_title("Residual QQ Plot")

plt.close(fig)
```

QQ 图偏离直线，说明残差分布与正态分布有差异。对 OLS 系数估计来说，正态性不是最核心条件；但对小样本推断和极端值判断会有影响。

## 异方差

同方差假设指：

```text
Var(error | X) = constant
```

异方差指误差方差会随解释变量或拟合值变化。金融数据里，异方差很常见，例如高波动股票的收益噪声通常更大。

OLS 在异方差下仍然可以给出系数估计，但普通标准误可能不可靠。标准误不可靠时，t 值、p 值和置信区间也会受影响。

## Breusch-Pagan 检验

Breusch-Pagan 检验可以检查残差方差是否与解释变量有关。

```python
bp_lm, bp_lm_pvalue, bp_fvalue, bp_f_pvalue = het_breuschpagan(
    results.resid,
    results.model.exog,
)

bp_test = pd.Series({
    "lm": bp_lm,
    "lm_pvalue": bp_lm_pvalue,
    "fvalue": bp_fvalue,
    "f_pvalue": bp_f_pvalue,
})

print(bp_test)
```

通常关注 p 值。如果 p 值很小，说明有异方差迹象。

注意：检验结果依赖模型设定和样本。p 值不小不等于一定同方差；p 值很小也不代表模型完全不可用。

## White 检验

White test 更一般，会考虑解释变量的平方项和交互项。

```python
white_lm, white_lm_pvalue, white_fvalue, white_f_pvalue = het_white(
    results.resid,
    results.model.exog,
)

white_test = pd.Series({
    "lm": white_lm,
    "lm_pvalue": white_lm_pvalue,
    "fvalue": white_fvalue,
    "f_pvalue": white_f_pvalue,
})

print(white_test)
```

White test 更灵活，但也更消耗自由度。样本很小时，不要机械依赖它。

## 稳健标准误

异方差常见处理方式之一是使用 heteroskedasticity-robust standard errors，也就是稳健标准误。

statsmodels 可以这样得到 HC3 稳健标准误：

```python
hc3_results = results.get_robustcov_results(cov_type="HC3")

param_index = results.params.index

robust_table = pd.DataFrame({
    "coef": results.params,
    "std_err_ols": results.bse,
    "std_err_hc3": pd.Series(hc3_results.bse, index=param_index),
    "pvalue_ols": results.pvalues,
    "pvalue_hc3": pd.Series(hc3_results.pvalues, index=param_index),
})

print(robust_table)
```

`HC3` 常用于中小样本或存在影响点的场景，比 `HC0` 更保守一些。

重要：稳健标准误改变的是标准误、t 值、p 值和置信区间，不改变 OLS 系数本身。

## 直接用 cov_type 拟合

也可以在 `fit` 时直接指定协方差类型。

```python
hc3_direct = smf.ols(formula, data=data).fit(cov_type="HC3")

print(hc3_direct.params)
print(hc3_direct.bse)
print(hc3_direct.pvalues)
```

这适合你已经决定报告稳健标准误的场景。正式报告里要写清楚使用了哪种标准误，例如 `HC3 robust standard errors`。

## 影响点：leverage 和 Cook 距离

一个样本可能因为两种原因影响模型：

- x 值很极端：高 leverage。
- y 值偏离模型很多：大残差。

两者结合起来，就可能成为影响点。

statsmodels 可以通过 `get_influence()` 计算影响诊断：

```python
influence = results.get_influence()
influence_frame = influence.summary_frame()

print(influence_frame.head())
```

常用列：

- `hat_diag`：leverage，也就是帽子矩阵对角线。
- `standard_resid`：标准化残差。
- `student_resid`：学生化残差。
- `cooks_d`：Cook 距离。
- `dffits`：该点对拟合值的影响。

## 整理影响点表

把诊断指标整理成一个更好读的表：

```python
influence_table = pd.DataFrame({
    "fitted": results.fittedvalues,
    "residual": results.resid,
    "student_resid": influence_frame["student_resid"],
    "hat_diag": influence_frame["hat_diag"],
    "cooks_d": influence_frame["cooks_d"],
})

top_cook = influence_table.sort_values("cooks_d", ascending=False).head(5)

print(top_cook)
```

Cook 距离大的样本不一定要删除，但一定值得检查。

## 简单阈值

常用经验阈值：

```python
nobs = int(results.nobs)
n_params = len(results.params)

leverage_threshold = 2 * n_params / nobs
cook_threshold = 4 / nobs

flagged = influence_table[
    (influence_table["hat_diag"] > leverage_threshold)
    | (influence_table["cooks_d"] > cook_threshold)
    | (influence_table["student_resid"].abs() > 3)
]

print(leverage_threshold)
print(cook_threshold)
print(flagged)
```

这些只是经验规则，不是统计法律。它们适合提醒你去检查样本，而不是自动删除样本。

## 影响点可视化

可以画 Cook 距离条形图。

```python
fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(influence_table.index, influence_table["cooks_d"])
ax.axhline(cook_threshold, color="tab:red", linestyle="--", linewidth=1)

ax.set_title("Cook's Distance")
ax.set_xlabel("Observation")
ax.set_ylabel("Cook's D")

fig.tight_layout()
plt.close(fig)
```

高于阈值的点需要结合原始数据查看：是否是录入错误、极端市场状态，还是确实存在的重要样本。

## 敏感性分析

影响点分析的一个实用做法是：去掉 Cook 距离最大的样本，比较系数变化。

```python
top_index = influence_table["cooks_d"].idxmax()

drop_top_results = smf.ols(
    formula,
    data=data.drop(index=top_index),
).fit()

sensitivity = pd.DataFrame({
    "full_sample": results.params,
    "drop_top_cook": drop_top_results.params,
})

sensitivity["abs_change"] = (
    sensitivity["drop_top_cook"] - sensitivity["full_sample"]
).abs()

print(top_index)
print(sensitivity)
```

如果删除一个样本后系数方向或数量级大幅变化，说明结论对该样本很敏感。此时不应该直接报告“稳定显著”。

## outlier_test

statsmodels 还提供 `outlier_test()`，用于查看学生化残差和多重检验调整后的 p 值。

```python
outlier_table = results.outlier_test(method="bonf")

print(outlier_table.head())
```

它适合辅助查找异常残差点。仍然要回到原始数据判断这些点代表错误、特殊状态，还是模型遗漏结构。

## 常见坑

第一，只看 p 值，不看残差。

p 值依赖标准误，而标准误依赖模型假设。残差图明显有结构时，回归表需要谨慎解读。

第二，把稳健标准误当成万能修复。

稳健标准误能让异方差下的推断更稳健，但它不会修复遗漏变量、非线性、样本选择偏差或未来函数。

第三，机械删除 Cook 距离大的样本。

影响点可能是错误数据，也可能是最重要的风险事件。删除前必须有业务或数据质量理由。

第四，把异方差检验当成唯一证据。

异方差检验有功效问题，也依赖设定。残差图、业务逻辑和稳健标准误应一起看。

第五，忘记报告标准误类型。

如果用了 HC3，就在报告中写明。不同标准误会影响 t 值和 p 值。

## 实战提示

一个 OLS 诊断流程：

1. 拟合普通 OLS，保存 `results`。
2. 画残差 vs 拟合值。
3. 看残差分布和 QQ 图。
4. 做 Breusch-Pagan 或 White 检验。
5. 对比普通标准误和 HC3 稳健标准误。
6. 查看 leverage、studentized residual 和 Cook 距离。
7. 对关键影响点做敏感性分析。
8. 报告中明确说明样本筛选、异常点处理和标准误类型。

一个整理诊断结果的模板：

```python
def regression_diagnostics(result):
    influence = result.get_influence()
    influence_frame = influence.summary_frame()

    bp = het_breuschpagan(result.resid, result.model.exog)
    white = het_white(result.resid, result.model.exog)

    hc3 = result.get_robustcov_results(cov_type="HC3")
    param_index = result.params.index

    coef = pd.DataFrame({
        "coef": result.params,
        "std_err_ols": result.bse,
        "std_err_hc3": pd.Series(hc3.bse, index=param_index),
        "pvalue_ols": result.pvalues,
        "pvalue_hc3": pd.Series(hc3.pvalues, index=param_index),
    })

    influence_table = pd.DataFrame({
        "student_resid": influence_frame["student_resid"],
        "hat_diag": influence_frame["hat_diag"],
        "cooks_d": influence_frame["cooks_d"],
    })

    tests = pd.DataFrame(
        {
            "breusch_pagan": bp,
            "white": white,
        },
        index=["lm", "lm_pvalue", "fvalue", "f_pvalue"],
    )

    return coef, tests, influence_table


coef, tests, influence_table = regression_diagnostics(results)

print(coef)
print(tests)
print(influence_table.sort_values("cooks_d", ascending=False).head())
```

## 小结

本节的重点：

- 残差图能快速暴露非线性、异方差和异常点。
- Breusch-Pagan 和 White test 用于检查异方差迹象。
- 异方差会影响普通 OLS 标准误，从而影响 t 值和 p 值。
- HC3 稳健标准误常用于中小样本和存在影响点的场景。
- `get_influence()` 可以计算 leverage、studentized residual 和 Cook 距离。
- Cook 距离大的点要检查和做敏感性分析，不能机械删除。

## 自检问题

1. 残差 vs 拟合值图出现漏斗形通常意味着什么？
2. Breusch-Pagan 检验和 White test 分别用于什么？
3. 稳健标准误会不会改变 OLS 系数？它改变什么？
4. leverage、studentized residual 和 Cook 距离分别关注什么？
5. 为什么不能自动删除 Cook 距离最大的样本？
