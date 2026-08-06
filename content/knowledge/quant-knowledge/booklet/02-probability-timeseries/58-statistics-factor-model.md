# 概率统计：factor model 因子模型、暴露、因子收益与风险分解

## 核心概念

factor model 因子模型用少数共同因子解释多个资产的收益和风险。

最常见的线性形式：

```text
r_t = B f_t + u_t
```

其中：

- `r_t`：某一天所有资产的收益向量，形状是 `N x 1`。
- `B`：资产对因子的暴露矩阵，形状是 `N x K`。
- `f_t`：当天因子收益向量，形状是 `K x 1`。
- `u_t`：资产特异收益，形状是 `N x 1`。

如果假设因子收益和特异收益不相关，且特异收益之间近似不相关，则资产协方差可以写成：

```text
Sigma = B Sigma_f B' + D
```

其中：

- `Sigma_f`：因子收益协方差矩阵。
- `D`：特异风险方差对角矩阵。

因子模型的价值在于：

- 用少数因子解释很多资产的共同波动。
- 把组合风险拆成因子风险和特异风险。
- 让高维协方差估计更稳定。
- 支持风险归因、行业/风格暴露控制和组合约束。

## 准备环境

```python
import numpy as np
import pandas as pd
```

准备 6 只资产和 3 个因子：

```python
rng = np.random.default_rng(58)

n_days = 600

assets = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"]
factors = ["market", "value", "momentum"]

B_true = pd.DataFrame(
    {
        "market": [1.05, 0.90, 1.20, 0.75, 1.10, 0.85],
        "value": [0.30, -0.20, 0.10, 0.60, -0.40, 0.20],
        "momentum": [0.10, 0.45, -0.30, 0.20, 0.35, -0.25],
    },
    index=assets,
)

factor_cov_true = np.array([
    [0.00016, 0.00003, 0.00001],
    [0.00003, 0.00009, 0.00002],
    [0.00001, 0.00002, 0.00012],
])

specific_var_true = pd.Series(
    [0.00010, 0.00012, 0.00009, 0.00011, 0.00013, 0.00008],
    index=assets,
)
```

这里：

- `B_true` 是真实因子暴露。
- `factor_cov_true` 是真实因子协方差。
- `specific_var_true` 是每只资产的特异风险方差。

真实研究中这些对象通常需要估计；模拟中保留真实值是为了校验。

## 生成因子收益和资产收益

```python
dates = pd.bdate_range("2024-01-02", periods=n_days)

factor_returns = pd.DataFrame(
    rng.multivariate_normal(
        mean=np.zeros(len(factors)),
        cov=factor_cov_true,
        size=n_days,
    ),
    index=dates,
    columns=factors,
)

specific_returns = pd.DataFrame(
    rng.normal(
        loc=0.0,
        scale=np.sqrt(specific_var_true.to_numpy()),
        size=(n_days, len(assets)),
    ),
    index=dates,
    columns=assets,
)

asset_returns = pd.DataFrame(
    factor_returns.to_numpy() @ B_true.T.to_numpy()
    + specific_returns.to_numpy(),
    index=dates,
    columns=assets,
)

print(factor_returns.head())
print(asset_returns.head())
```

每只资产收益由两部分组成：

```text
factor-driven return + specific return
```

例如 `AAA` 的收益近似为：

```text
1.05 * market + 0.30 * value + 0.10 * momentum + specific_AAA
```

## 用时间序列回归估计暴露

如果因子收益已知，可以对每只资产做时间序列回归来估计暴露：

```text
r_{i,t} = alpha_i + beta_{i,1} f_{1,t} + ... + beta_{i,K} f_{K,t} + u_{i,t}
```

```python
X = np.column_stack([
    np.ones(n_days),
    factor_returns.to_numpy(),
])

estimated_rows = []
residual_columns = []

for asset in assets:
    y = asset_returns[asset].to_numpy()
    beta = np.linalg.lstsq(X, y, rcond=None)[0]

    estimated_rows.append(beta)
    residual_columns.append(y - X @ beta)

estimated_exposures = pd.DataFrame(
    estimated_rows,
    index=assets,
    columns=["alpha"] + factors,
)

residuals = pd.DataFrame(
    np.column_stack(residual_columns),
    index=dates,
    columns=assets,
)

print(estimated_exposures)
print(B_true)
```

`alpha` 是因子无法解释的平均收益。`market`、`value`、`momentum` 列是估计出的因子暴露。

模拟数据足够长时，估计暴露会接近真实暴露。

## 收益分解

选择某一天，拆解每只资产收益。

```python
one_date = dates[0]

B_hat = estimated_exposures[factors]

factor_part = B_hat.to_numpy() @ factor_returns.loc[one_date].to_numpy()
specific_part = residuals.loc[one_date].to_numpy()
reconstructed_return = factor_part + specific_part + estimated_exposures["alpha"].to_numpy()

decomposition = pd.DataFrame(
    {
        "actual_return": asset_returns.loc[one_date],
        "factor_part": factor_part,
        "specific_part": specific_part,
        "alpha": estimated_exposures["alpha"],
        "reconstructed": reconstructed_return,
    },
    index=assets,
)

print(decomposition)
```

线性回归保证：

```text
actual_return = alpha + factor_part + residual
```

这就是收益归因的最基本形式。

## 因子协方差和特异方差

估计因子协方差：

```python
factor_cov = factor_returns.cov()

print(factor_cov)
```

估计特异方差。这里按回归自由度修正：

```python
n_params = len(factors) + 1

specific_var_hat = (residuals ** 2).sum(axis=0) / (n_days - n_params)

print(specific_var_hat)
```

在简单风险模型里，常假设特异协方差矩阵是对角矩阵：

```python
D_hat = np.diag(specific_var_hat.to_numpy())
```

这意味着不同资产的特异收益近似不相关。

真实风险模型有时会进一步处理行业内残差相关、国家效应、异方差和极端值。

## 协方差分解

用因子模型构造资产协方差：

```python
model_cov = (
    B_hat.to_numpy()
    @ factor_cov.to_numpy()
    @ B_hat.to_numpy().T
    + D_hat
)

sample_cov = asset_returns.cov().to_numpy()

cov_compare = pd.DataFrame({
    "sample_diag": np.diag(sample_cov),
    "model_diag": np.diag(model_cov),
}, index=assets)

print(cov_compare)
```

因子模型协方差不需要直接估计所有 `N x N` 的资产协方差元素。它只需要：

- `N x K` 个暴露。
- `K x K` 个因子协方差。
- `N` 个特异方差。

当 `N` 很大、`K` 较小时，这比样本协方差更稳定。

## 组合风险分解

给定一个组合权重：

```python
weights = pd.Series(
    [0.20, 0.15, 0.25, 0.10, 0.20, 0.10],
    index=assets,
)

print(weights.sum())
```

组合的因子暴露是：

```text
b_p = w' B
```

```python
portfolio_factor_exposure = weights.to_numpy() @ B_hat.to_numpy()

portfolio_factor_exposure = pd.Series(
    portfolio_factor_exposure,
    index=factors,
    name="portfolio_factor_exposure",
)

print(portfolio_factor_exposure)
```

组合方差可以拆成：

```text
portfolio_var = b_p Sigma_f b_p' + sum(w_i^2 specific_var_i)
```

```python
factor_var = float(
    portfolio_factor_exposure.to_numpy()
    @ factor_cov.to_numpy()
    @ portfolio_factor_exposure.to_numpy()
)

specific_var = float(
    np.sum((weights.to_numpy() ** 2) * specific_var_hat.to_numpy())
)

total_var = factor_var + specific_var
model_portfolio_var = float(weights.to_numpy() @ model_cov @ weights.to_numpy())

risk_decomposition = pd.Series({
    "factor_var": factor_var,
    "specific_var": specific_var,
    "total_var": total_var,
    "model_portfolio_var": model_portfolio_var,
    "factor_share": factor_var / total_var,
    "specific_share": specific_var / total_var,
})

print(risk_decomposition)
```

`total_var` 和 `model_portfolio_var` 应该相等，只是计算路径不同。

在分散组合中，特异风险通常会被分散掉，因子风险往往占主要部分。

## 资产风险贡献

总组合方差还可以按资产贡献拆分。

```python
marginal_contribution = model_cov @ weights.to_numpy()
component_contribution = (
    weights.to_numpy()
    * marginal_contribution
    / model_portfolio_var
)

risk_contribution = pd.Series(
    component_contribution,
    index=assets,
    name="risk_contribution_share",
)

print(risk_contribution)
print(risk_contribution.sum())
```

这里的贡献是对组合方差的贡献比例。它可能和权重很不一样，因为资产风险和相关性不同。

## 主动组合的因子暴露

很多策略需要控制主动暴露。例如一个多空组合可能希望市场暴露接近 0。

```python
active_weights = pd.Series(
    [0.25, -0.20, 0.15, -0.10, -0.05, -0.05],
    index=assets,
)

active_factor_exposure = active_weights.to_numpy() @ B_hat.to_numpy()

active_exposure = pd.Series(
    active_factor_exposure,
    index=factors,
    name="active_factor_exposure",
)

print(active_weights.sum())
print(active_exposure)
```

主动权重和为 0 不代表因子暴露为 0。一个 dollar-neutral 组合仍然可能有明显的 market、value 或 momentum 暴露。

这就是为什么实际组合优化经常加入：

```text
w' B = target_exposure
```

这样的因子约束。

## Fama-French 和 Barra 的区别

Fama-French 类模型常见形式是时间序列回归：

```text
r_i - r_f = alpha_i + beta_mkt MKT + beta_smb SMB + beta_hml HML + epsilon_i
```

它常用于解释基金或资产的收益来源。

Barra 类风险模型更偏风险管理：

- 暴露可能来自基本面、行业、风格、国家等。
- 因子收益可以用横截面回归估计。
- 风险模型重点是 `B Sigma_f B' + D`。
- 组合层面关注风险预测、风险贡献和约束。

二者都叫因子模型，但用途和数据构造不同。

## 常见坑

第一，把因子暴露和因子收益混淆。

暴露是资产对因子的敏感度；因子收益是某一期因子本身的回报。

第二，只看收益解释，不看风险分解。

因子模型不仅解释收益，还用于预测组合风险、风险贡献和压力测试。

第三，假设特异收益完全独立。

对角 `D` 是简化。真实市场里同一行业、同一事件或同一流动性冲击可能让残差相关。

第四，忽略暴露时点。

基本面暴露、行业分类、市值、beta 都必须是当时可见版本。否则风险模型也会前视。

第五，认为 dollar-neutral 就是 factor-neutral。

权重和为 0 只控制资金暴露，不控制 market、行业、风格等因子暴露。

## 实战提示

构建和使用因子模型时，可以按下面流程：

1. 明确因子集合：市场、行业、风格、国家或宏观变量。
2. 明确暴露矩阵 `B` 的来源和时点。
3. 估计因子收益时间序列或用已知因子收益。
4. 估计因子协方差 `Sigma_f`。
5. 估计特异方差 `D`。
6. 检查残差相关性、残差波动和异常点。
7. 用 `B Sigma_f B' + D` 预测组合风险。
8. 对组合做因子暴露、风险贡献和压力情景分析。

## 小结

本节的重点：

- 因子模型写作 `r = Bf + u`。
- `B` 是暴露，`f` 是因子收益，`u` 是特异收益。
- 协方差可以分解为 `B Sigma_f B' + D`。
- 组合因子暴露是 `w'B`。
- 组合风险可以拆成因子风险和特异风险。
- dollar-neutral 不等于 factor-neutral。
- Fama-French 更常用于收益解释，Barra 类模型更常用于风险管理和组合约束。

## 自检问题

1. 因子暴露和因子收益有什么区别？
2. `Sigma = B Sigma_f B' + D` 中每一项代表什么？
3. 为什么因子模型能让高维协方差估计更稳定？
4. 组合因子暴露如何计算？
5. 为什么权重和为 0 不代表市场暴露为 0？
6. Fama-French 类模型和 Barra 类风险模型的侧重点有什么不同？
