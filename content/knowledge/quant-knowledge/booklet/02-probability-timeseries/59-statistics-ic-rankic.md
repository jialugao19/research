# 概率统计：IC / RankIC 的定义、计算、解释与稳定性检查

## 核心概念

IC 是 Information Coefficient，通常指某一期因子值和未来收益之间的横截面相关系数。

最常见定义：

```text
IC_t = corr(factor_{t, i}, forward_return_{t, i})
```

其中：

- `factor_{t, i}`：在日期 `t` 可见的资产 `i` 的因子值。
- `forward_return_{t, i}`：从 `t` 之后开始计算的未来收益。
- `corr`：通常是 Pearson 相关。

RankIC 是把因子值和未来收益都转成横截面排名后再算相关。

```text
RankIC_t = corr(rank(factor_{t, i}), rank(forward_return_{t, i}))
```

实际量化研究中，RankIC 往往比普通 IC 更常用，因为它更关注排序能力，对极端值和非线性单调关系更稳健。

## IC 回答的问题

IC / RankIC 不是在问：

```text
这个因子能预测具体收益率是多少？
```

它更像在问：

```text
这个因子在横截面上能不能把未来表现更好的资产排在前面？
```

因此它适合评估选股、择券、截面 alpha 因子。

如果一个因子平均 RankIC 为正，说明高因子值资产未来收益倾向于高于低因子值资产。若平均 RankIC 为负，则可能说明因子方向反了。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一个简单的因子面板：

```python
rng = np.random.default_rng(59)

n_dates = 90
n_assets = 12

dates = pd.bdate_range("2024-01-02", periods=n_dates)
assets = [f"A{i:02d}" for i in range(n_assets)]

signal_values = rng.normal(size=(n_dates, n_assets))

for t in range(1, n_dates):
    signal_values[t] = (
        0.65 * signal_values[t - 1]
        + rng.normal(scale=0.75, size=n_assets)
    )

factor = pd.DataFrame(signal_values, index=dates, columns=assets)
factor.index.name = "date"
factor.columns.name = "asset"

print(factor.head())
```

这里的 `factor` 是宽表：

- 行是日期。
- 列是资产。
- 单元格是当天收盘后或某个固定时点可见的因子值。

## 构造未来收益

为了演示，我们让高因子排名资产在下一期有更高的期望收益。

```python
predictive_component = factor.rank(axis=1, pct=True).sub(0.5) * 0.018

noise = pd.DataFrame(
    rng.normal(scale=0.018, size=(n_dates, n_assets)),
    index=dates,
    columns=assets,
)

next_day_return_from_signal = predictive_component + noise
```

`next_day_return_from_signal.loc[t]` 表示由 `t` 日因子预测出来的下一日收益。

真实数据通常是每天已经实现的收益序列。为了模拟真实对齐方式，先构造 `realized_return`：

```python
realized_return = next_day_return_from_signal.shift(1)
```

这表示：

- `realized_return.loc[t]` 是从 `t-1` 到 `t` 实现的收益。
- `factor.loc[t-1]` 才能预测它。

所以，与 `factor.loc[t]` 对齐的 1 日未来收益应该是：

```python
forward_return_1d = realized_return.shift(-1)
```

这是 IC 计算里最关键的一步：因子日期必须早于收益实现日期。

## 组织成长表

IC 通常按日期做横截面相关，因此长表更方便。

```python
def make_panel(factor_wide, forward_return_wide):
    factor_long = factor_wide.stack().rename("factor")
    forward_long = forward_return_wide.stack().rename("forward_return")

    return pd.concat([factor_long, forward_long], axis=1).dropna()


panel = make_panel(factor, forward_return_1d)

print(panel.head())
```

`panel` 的索引是 `(date, asset)`，列包括：

- `factor`：日期 `date` 可见的因子值。
- `forward_return`：从日期 `date` 之后开始的未来收益。

最后一天没有下一日收益，因此会被 `dropna()` 去掉。

## 计算每日 IC 和 RankIC

写一个通用函数：

```python
def ic_by_date(panel, method="pearson"):
    rows = []

    for date, group in panel.groupby(level="date", sort=True):
        x = group["factor"]
        y = group["forward_return"]

        if method == "spearman":
            x = x.rank(method="average")
            y = y.rank(method="average")

        rows.append((date, x.corr(y)))

    return pd.Series(dict(rows), name=f"{method}_ic")
```

普通 IC：

```python
ic = ic_by_date(panel, method="pearson")

print(ic.head())
print(ic.mean())
```

RankIC：

```python
rank_ic = ic_by_date(panel, method="spearman")

print(rank_ic.head())
print(rank_ic.mean())
```

这里的 `method="spearman"` 不是调用黑箱函数，而是先做横截面排名，再计算 Pearson 相关。

## 汇总指标

单日 IC 很 noisy，不能只看某一天。常见汇总方式：

```python
ic_summary = pd.Series({
    "ic_mean": ic.mean(),
    "ic_std": ic.std(ddof=1),
    "ic_ir": ic.mean() / ic.std(ddof=1),
    "rank_ic_mean": rank_ic.mean(),
    "rank_ic_std": rank_ic.std(ddof=1),
    "rank_ic_ir": rank_ic.mean() / rank_ic.std(ddof=1),
    "rank_ic_positive_ratio": (rank_ic > 0).mean(),
})

print(ic_summary)
```

含义：

- `ic_mean`：平均预测方向。
- `ic_std`：IC 的波动。
- `ic_ir`：IC 均值除以 IC 标准差，类似因子稳定性的信噪比。
- `rank_ic_positive_ratio`：RankIC 大于 0 的日期比例。

经验上，一个非常小但稳定为正的 RankIC 就可能有价值。IC 的经济意义还要结合换手、容量、成本和组合构建方式一起看。

## 分组收益检查

RankIC 看的是排序相关。更直观的检查是按因子分组，看高分组未来收益是否高于低分组。

```python
pieces = []

for date, group in panel.groupby(level="date", sort=True):
    tmp = group.copy()
    ranks = tmp["factor"].rank(method="first")
    tmp["quantile"] = (pd.qcut(ranks, q=5, labels=False) + 1).astype(int)
    pieces.append(tmp)

panel_with_quantile = pd.concat(pieces).sort_index()

quantile_return = (
    panel_with_quantile
    .groupby("quantile")["forward_return"]
    .mean()
)

spread_5_minus_1 = quantile_return.loc[5] - quantile_return.loc[1]

print(quantile_return)
print(spread_5_minus_1)
```

如果因子方向正确，通常希望看到：

```text
第 5 组平均未来收益 > 第 1 组平均未来收益
```

分组收益和 RankIC 是互补检查：

- RankIC 给出整体排序相关。
- 分组收益展示从低分组到高分组的经济单调性。

## 不同预测期限的 RankIC

因子可能只预测 1 日，也可能预测 5 日或 20 日。需要分别检查不同 horizon。

下面用简单收益相加近似多日未来收益：

```python
horizon_rows = []

for horizon in [1, 5, 10]:
    forward_return_h = sum(
        realized_return.shift(-step)
        for step in range(1, horizon + 1)
    )

    panel_h = make_panel(factor, forward_return_h)
    rank_ic_h = ic_by_date(panel_h, method="spearman")

    horizon_rows.append({
        "horizon": horizon,
        "rank_ic_mean": rank_ic_h.mean(),
        "rank_ic_std": rank_ic_h.std(ddof=1),
        "positive_ratio": (rank_ic_h > 0).mean(),
    })

horizon_summary = pd.DataFrame(horizon_rows).set_index("horizon")

print(horizon_summary)
```

常见现象：

- 高频短周期因子可能 1 日 RankIC 最强，随后快速衰减。
- 慢变量基本面因子可能在更长 horizon 上更有效。
- 如果长 horizon 计算使用重叠收益，IC 序列会有自相关，显著性不能按独立样本粗暴解释。

## 中性化后的 IC

有些因子的 RankIC 来自行业、市值或 beta 暴露，而不是真正的个股选择能力。

下面做一个简单的行业内去均值：

```python
industries = pd.Series(
    [
        "tech", "tech", "tech", "tech",
        "finance", "finance", "finance", "finance",
        "health", "health", "health", "health",
    ],
    index=assets,
    name="industry",
)

neutralized_factor = factor.copy()

for industry, industry_assets in industries.groupby(industries).groups.items():
    cols = list(industry_assets)
    neutralized_factor.loc[:, cols] = factor.loc[:, cols].sub(
        factor.loc[:, cols].mean(axis=1),
        axis=0,
    )

neutralized_panel = make_panel(neutralized_factor, forward_return_1d)
neutralized_rank_ic = ic_by_date(neutralized_panel, method="spearman")

print(neutralized_rank_ic.mean())
```

这不是完整的风险中性化，只是最简单的行业内中心化。

实际研究中常用横截面回归做中性化：

```text
factor_i = a + b1 * size_i + b2 * beta_i + industry_dummies_i + residual_i
```

然后用残差因子计算 IC。

## 显著性和稳定性

平均 IC 为正不等于因子可靠。至少要检查：

```python
rank_ic_t_stat = (
    rank_ic.mean()
    / (rank_ic.std(ddof=1) / np.sqrt(rank_ic.count()))
)

rolling_rank_ic = rank_ic.rolling(window=20).mean()

print(rank_ic_t_stat)
print(rolling_rank_ic.tail())
```

需要注意：

- IC 序列可能自相关，简单 t 统计可能过于乐观。
- 市场 regime 变化会让 IC 衰减或反转。
- 极端市场环境下的少数日期可能主导平均值。
- 分层样本太少时，单日 IC 非常不稳定。

更严谨的做法包括分年份、分行业、分市值桶、分波动率环境检查，并使用 Newey-West 等方法修正自相关标准误。

## 常见坑

第一，收益对齐错误。

`factor.loc[t]` 必须对应 `t` 之后的收益。把 `factor.loc[t]` 和 `return.loc[t]` 直接相关，很可能混入已经发生的收益。

第二，把时间序列相关当成 IC。

IC 是每个日期做一次横截面相关，然后再看时间序列均值。不是把所有日期和资产摊平成一个大向量后算一次相关。

第三，只看平均 IC，不看稳定性。

平均 IC 可能被少数极端日期拉高。需要看胜率、滚动均值、分样本和分市场环境。

第四，不做中性化。

一个看似有效的因子可能只是行业暴露、市值暴露或 beta 暴露。

第五，只看 RankIC，不看成本。

IC 高但换手极高、容量很小或交易成本很大，可能无法变成真实收益。

## 实战提示

计算 IC / RankIC 时可以按下面流程：

1. 固定因子可见时点，例如每日收盘后。
2. 明确交易假设，例如下一日开盘成交或下一日收盘成交。
3. 根据交易假设构造 forward return。
4. 每个日期单独做横截面 IC / RankIC。
5. 汇总均值、标准差、ICIR、正 IC 比例。
6. 做分组收益和多空 spread 检查。
7. 分 horizon 检查预测衰减。
8. 做行业、市值、beta 等中性化后复查。
9. 分年份、分市场状态、分样本外区间复查。
10. 结合 turnover、成本、容量再判断是否可交易。

## 小结

本节的重点：

- IC 是因子值和未来收益的横截面相关。
- RankIC 是排名后的 IC，更关注排序能力。
- 因子必须和未来收益正确对齐。
- IC 要按日期计算，再汇总时间序列表现。
- 平均 IC、ICIR、正 IC 比例和滚动 IC 都要看。
- 分组收益能帮助确认经济单调性。
- 中性化后 IC 更能反映纯粹选股能力。
- IC 只是研究入口，最终还要结合换手、成本、容量和组合构建。

## 自检问题

1. IC 和 RankIC 分别如何计算？
2. 为什么 `factor.loc[t]` 不能直接和 `return.loc[t]` 随便做相关？
3. 为什么 IC 应该逐日横截面计算，而不是全样本摊平计算？
4. RankIC 比普通 IC 对哪些问题更稳健？
5. 平均 RankIC 为正但策略亏钱，可能有哪些原因？
6. 为什么要做行业、市值或 beta 中性化后的 IC？
