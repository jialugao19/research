# Cross-Sectional Regression

## 核心概念

cross-sectional regression 横截面回归是在同一个时间点，对多个资产做回归。

典型形式：

```text
r_{i,t+1} = a_t + b_{1,t} x_{1,i,t} + b_{2,t} x_{2,i,t} + ... + e_{i,t+1}
```

其中：

- `i` 是资产。
- `t` 是截面日期。
- `r_{i,t+1}` 是未来一期收益。
- `x_{j,i,t}` 是日期 `t` 已知的因子暴露。
- `b_{j,t}` 是这一期横截面上估出来的因子收益。
- `e_{i,t+1}` 是无法被这些因子解释的个股残差。

和时间序列回归不同：

- 时间序列回归：对一只资产跨时间回归。
- 横截面回归：对同一天的多只资产回归。

量化中常用横截面回归来：

- 估计当期因子收益。
- 对收益做因子归因。
- 对某个信号做行业、市值、风格中性化。
- 检查因子暴露是否解释了截面收益差异。
- 为 Fama-MacBeth 或 Barra 类风险模型打基础。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一个小型资产面板。每一天有 12 只资产，每只资产有两个因子暴露和未来 1 日收益。

```python
rng = np.random.default_rng(57)

dates = pd.bdate_range("2024-01-02", periods=8)
assets = [f"A{i:02d}" for i in range(12)]

industry_map = {
    asset: ["tech", "finance", "health"][i % 3]
    for i, asset in enumerate(assets)
}

true_factor_returns = pd.DataFrame(
    {
        "intercept": [0.0010, -0.0005, 0.0008, 0.0012, -0.0008, 0.0003, 0.0010, -0.0002],
        "momentum": [0.0120, -0.0060, 0.0100, 0.0040, -0.0090, 0.0060, 0.0110, -0.0040],
        "value": [-0.0050, 0.0080, -0.0020, 0.0060, 0.0100, -0.0040, -0.0060, 0.0090],
    },
    index=dates,
)
```

生成暴露和收益：

```python
rows = []

base_momentum = rng.normal(0.0, 1.0, size=len(assets))
base_value = -0.3 * base_momentum + rng.normal(0.0, 1.0, size=len(assets))

industry_effect = {
    "tech": 0.0015,
    "finance": -0.0005,
    "health": 0.0,
}

for date in dates:
    for j, asset in enumerate(assets):
        industry = industry_map[asset]

        momentum = base_momentum[j] + rng.normal(0.0, 0.15)
        value = base_value[j] + rng.normal(0.0, 0.15)

        factor_return = true_factor_returns.loc[date]
        noise = rng.normal(0.0, 0.002)

        return_fwd_1d = (
            factor_return["intercept"]
            + factor_return["momentum"] * momentum
            + factor_return["value"] * value
            + industry_effect[industry]
            + noise
        )

        rows.append({
            "date": date,
            "asset": asset,
            "industry": industry,
            "momentum": momentum,
            "value": value,
            "return_fwd_1d": return_fwd_1d,
        })

panel = pd.DataFrame(rows).sort_values(["date", "asset"]).reset_index(drop=True)

print(panel.head())
```

真实研究中，`true_factor_returns` 不可见。这里保留它只是为了验证横截面回归能否恢复因子收益。

## 每日横截面标准化

很多因子暴露会先在每天横截面上标准化，便于不同因子量纲可比。

```python
def zscore_by_date(frame, columns):
    out = frame.copy()

    for col in columns:
        out[f"{col}_z"] = (
            out
            .groupby("date")[col]
            .transform(lambda s: (s - s.mean()) / s.std(ddof=0))
        )

    return out


panel = zscore_by_date(panel, ["momentum", "value"])

print(panel[["date", "asset", "momentum_z", "value_z"]].head())
```

如果使用 z-score 暴露，回归系数表示“因子暴露增加一个横截面标准差，对未来收益的线性解释变化”。

本节为了和模拟中的真实系数对齐，后面主要用原始 `momentum` 和 `value` 暴露。

## 单日横截面回归

写一个最小 OLS 函数。

```python
def fit_cross_section(frame, y_col, x_cols):
    X = np.column_stack([
        np.ones(len(frame)),
        frame[x_cols].to_numpy(),
    ])
    y = frame[y_col].to_numpy()

    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    fitted = X @ beta
    residual = y - fitted

    rss = float(residual @ residual)
    tss = float((y - y.mean()) @ (y - y.mean()))
    r2 = 1.0 - rss / tss

    return pd.Series(
        np.r_[beta, np.mean(residual ** 2), r2],
        index=["intercept"] + x_cols + ["mse", "r2"],
    )
```

取第一天的截面：

```python
one_day = panel[panel["date"].eq(dates[0])].copy()

single_result = fit_cross_section(
    one_day,
    y_col="return_fwd_1d",
    x_cols=["momentum", "value"],
)

print(single_result)
print(true_factor_returns.loc[dates[0]])
```

`momentum` 和 `value` 的回归系数就是这一天估计出的因子收益。它们回答的问题是：

```text
在这一天的股票截面上，暴露更高的股票是否获得了更高的未来收益？
```

## 回归残差的含义

残差是因子解释不了的那部分收益。

```python
X_one_day = np.column_stack([
    np.ones(len(one_day)),
    one_day[["momentum", "value"]].to_numpy(),
])

beta_one_day = single_result[["intercept", "momentum", "value"]].to_numpy()

one_day["fitted_return"] = X_one_day @ beta_one_day
one_day["specific_return"] = one_day["return_fwd_1d"] - one_day["fitted_return"]

print(one_day[[
    "asset",
    "return_fwd_1d",
    "fitted_return",
    "specific_return",
]].head())
```

在 OLS 中，残差和解释变量正交：

```python
orthogonality = X_one_day.T @ one_day["specific_return"].to_numpy()

print(orthogonality)
```

因此，残差可以理解为在当前线性因子模型下的特异收益。

## 多日期逐日回归

实际研究通常每天做一次横截面回归，得到一条因子收益时间序列。

```python
factor_return_rows = []

for date, group in panel.groupby("date"):
    result = fit_cross_section(
        group,
        y_col="return_fwd_1d",
        x_cols=["momentum", "value"],
    )
    result["date"] = date
    factor_return_rows.append(result)

estimated_factor_returns = (
    pd.DataFrame(factor_return_rows)
    .set_index("date")
    .sort_index()
)

print(estimated_factor_returns)
```

把估计因子收益和真实模拟值对比：

```python
compare_factor_returns = estimated_factor_returns[
    ["intercept", "momentum", "value"]
].join(
    true_factor_returns,
    lsuffix="_estimated",
    rsuffix="_true",
)

print(compare_factor_returns)
```

真实项目没有 `*_true` 列。这里的对比只是说明逐日横截面回归能从截面收益中估计因子收益。

## 因子收益的时间序列总结

逐日估计得到的 `momentum` 系数序列，可以当作动量因子的每日收益序列。

```python
def summarize_factor_return(series):
    mean = series.mean()
    std = series.std(ddof=1)
    t_stat = mean / (std / np.sqrt(len(series)))

    return pd.Series({
        "mean": mean,
        "std": std,
        "t_stat_naive": t_stat,
    })


factor_return_summary = pd.DataFrame({
    factor: summarize_factor_return(estimated_factor_returns[factor])
    for factor in ["momentum", "value"]
}).T

print(factor_return_summary)
```

这里的 `t_stat_naive` 只是普通时间序列均值 t 值，没有处理自相关、异方差、交易成本或多重检验。正式研究中要更谨慎。

## 加入行业哑变量

横截面回归常用行业、市值等控制变量。行业是类别变量，可以转成 dummy。

```python
def fit_cross_section_with_industry(frame):
    dummies = pd.get_dummies(
        frame["industry"],
        prefix="industry",
        drop_first=True,
        dtype=float,
    )

    X_df = pd.concat(
        [
            frame[["momentum", "value"]].reset_index(drop=True),
            dummies.reset_index(drop=True),
        ],
        axis=1,
    )

    X = np.column_stack([np.ones(len(X_df)), X_df.to_numpy()])
    y = frame["return_fwd_1d"].to_numpy()

    beta = np.linalg.lstsq(X, y, rcond=None)[0]

    return pd.Series(
        beta,
        index=["intercept"] + X_df.columns.tolist(),
    )


industry_result = fit_cross_section_with_industry(one_day)

print(industry_result)
```

加入行业 dummy 后，`momentum` 和 `value` 系数表示在控制行业差异后的截面线性关系。

实际因子研究中，常见控制项包括：

- 行业 dummy。
- 国家或交易所 dummy。
- size / beta / volatility 等风险暴露。
- 是否可交易、流动性、价格水平等过滤变量。

## 样本数和秩检查

横截面回归每一天都需要足够样本。

如果某天可用股票太少，或者解释变量完全共线，回归结果会不稳定。

```python
def check_cross_section_design(frame, x_cols):
    X = np.column_stack([
        np.ones(len(frame)),
        frame[x_cols].to_numpy(),
    ])

    rank = np.linalg.matrix_rank(X)

    return pd.Series({
        "n_obs": len(frame),
        "n_params": X.shape[1],
        "rank": rank,
        "full_rank": rank == X.shape[1],
    })


design_check_rows = []

for date, group in panel.groupby("date"):
    check = check_cross_section_design(group, ["momentum", "value"])
    check["date"] = date
    design_check_rows.append(check)

design_checks = (
    pd.DataFrame(design_check_rows)
    .set_index("date")
    .sort_index()
)

print(design_checks)
```

经验上，截面样本数应明显大于参数个数。行业 dummy 很多、股票池很小或缺失很多时，这个问题会特别突出。

## 横截面回归和因子排序的区别

因子排序常问：

```text
高因子组是否比低因子组收益高？
```

横截面回归问：

```text
在控制其他暴露后，每单位因子暴露对应多少截面收益差异？
```

排序更直观、非参数；回归更适合多因子控制和归因。

两者通常应一起看：一个因子如果排序有效，但回归中被行业或市值控制后消失，说明它可能只是行业或市值暴露的代理。

## 常见坑

第一，把时间序列回归和横截面回归混为一谈。

横截面回归是一日多资产；时间序列回归是一资产多日期。二者估计对象不同。

第二，特征和标签时点错位。

日期 `t` 的暴露只能使用当时可见信息，标签可以是 `t` 到 `t+1` 的未来收益。

第三，样本数太少仍然加入很多 dummy。

每加一个控制变量都会消耗自由度。小股票池上加入大量行业 dummy 会让回归不稳定。

第四，忽略截面异方差。

不同股票的收益噪声不同，市值、流动性、波动率也不同。正式估计可以考虑 WLS 或稳健标准误。

第五，把因子收益均值 t 值当作最终结论。

还要看样本外、交易成本、换手、容量、行业暴露和多重检验。

## 实战提示

做横截面回归时，可以按下面流程：

1. 明确每行粒度是 `(date, asset)`。
2. 检查主键唯一、缺失值和可交易样本。
3. 确认特征在 `date` 时点可见，标签是未来收益。
4. 每天单独回归，不要把所有日期直接混成一个截面。
5. 对因子暴露做横截面标准化或 winsorize。
6. 根据需要加入行业、市值、beta、volatility 等控制项。
7. 每天检查样本数、参数个数和矩阵秩。
8. 汇总因子收益时间序列时，处理自相关、异方差和多重检验。

## 小结

本节的重点：

- 横截面回归是在同一天的资产截面上做回归。
- 回归系数可以解释为当期因子收益。
- 逐日横截面回归会得到因子收益时间序列。
- 残差是当前因子模型解释不了的特异收益。
- 行业、市值等控制变量可以帮助做中性化和归因。
- 截面回归必须严格检查时点、样本数、秩和控制变量含义。

## 自检问题

1. 横截面回归和时间序列回归有什么区别？
2. 为什么横截面回归的系数可以叫因子收益？
3. 回归残差在因子归因里代表什么？
4. 为什么要每天单独做横截面回归？
5. 加入行业 dummy 后，因子系数的解释发生了什么变化？
6. 为什么小截面样本不能随便加入很多控制变量？
