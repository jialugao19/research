# pandas：groupby / agg / transform

## 核心概念

`groupby` 用来做“分组计算”。它遵循 split-apply-combine 思路：

1. split：按某些列把数据拆成多个组。
2. apply：在每个组内做计算。
3. combine：把每个组的结果合并起来。

最常见的两类结果是：

- `agg`：每组返回较少行，通常是一组一行。
- `transform`：每组返回和原组一样长的结果，最终结果和原表行数一致。

```python
import pandas as pd

df = pd.DataFrame({
    "date": ["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"],
    "asset": ["AAA", "BBB", "AAA", "BBB"],
    "return": [0.01, -0.02, 0.03, 0.00],
})

print(df.groupby("date")["return"].mean())
```

这会计算每天的平均收益。

## 准备数据

下面使用一个长表，表示每天每只股票的行业、收益率、因子值和成交额。

```python
import pandas as pd

df = pd.DataFrame({
    "date": pd.to_datetime([
        "2024-01-02", "2024-01-02", "2024-01-02",
        "2024-01-03", "2024-01-03", "2024-01-03",
    ]),
    "asset": ["AAA", "BBB", "CCC", "AAA", "BBB", "CCC"],
    "industry": ["tech", "finance", "tech", "tech", "finance", "tech"],
    "return": [0.01, -0.02, 0.03, 0.02, 0.00, -0.01],
    "factor": [1.2, 0.5, 1.8, 1.0, 0.7, 1.5],
    "amount": [1000, 800, 1500, 1200, 900, 1300],
})

print(df)
```

这个表是长表结构：

- 每行是一条 `date-asset` 观测。
- `date` 和 `industry` 可以作为分组键。
- `return`、`factor`、`amount` 是要统计的数值列。

## groupby 后做简单聚合

按日期计算平均收益：

```python
daily_return = df.groupby("date")["return"].mean()

print(daily_return)
```

输出是一个 Series，index 是 `date`，value 是每天的平均收益。

按行业计算平均收益：

```python
industry_return = df.groupby("industry")["return"].mean()

print(industry_return)
```

如果要保留普通列，而不是把分组键放到 index，可以使用 `as_index=False`：

```python
daily_return_table = df.groupby("date", as_index=False)["return"].mean()

print(daily_return_table)
```

`as_index=False` 常用于后续还要 merge 回别的表的场景。

## 多个分组键

可以按多个列分组。例如每天、每个行业的平均收益：

```python
daily_industry_return = df.groupby(["date", "industry"])["return"].mean()

print(daily_industry_return)
```

默认结果的 index 是 `MultiIndex`。如果希望普通 DataFrame：

```python
daily_industry_return = (
    df.groupby(["date", "industry"], as_index=False)["return"]
    .mean()
)

print(daily_industry_return)
```

多键分组在因子研究里很常见，例如：

- 按日期分组：每天做横截面统计。
- 按日期和行业分组：每天在行业内部做标准化或排名。
- 按资产分组：每只股票沿时间序列做统计。

## agg：一次计算多个统计量

`agg` 可以一次计算多个统计量。

```python
summary = df.groupby("date")["return"].agg(["mean", "std", "count"])

print(summary)
```

输出里每一行是一个日期，每一列是一个统计量。

也可以对多列使用不同聚合：

```python
summary = df.groupby("date").agg({
    "return": ["mean", "std"],
    "amount": "sum",
})

print(summary)
```

这会产生多层列名。为了得到更清晰的一层列名，推荐使用 named aggregation。

## named aggregation

named aggregation 可以显式指定输出列名。

```python
summary = df.groupby("date", as_index=False).agg(
    mean_return=("return", "mean"),
    return_std=("return", "std"),
    total_amount=("amount", "sum"),
    n_assets=("asset", "nunique"),
)

print(summary)
```

这种写法可读性强，适合研究报告和生产代码。

输出列含义：

- `mean_return`：当天横截面平均收益。
- `return_std`：当天横截面收益标准差。
- `total_amount`：当天总成交额。
- `n_assets`：当天股票数量。

## transform：把组级结果广播回原行

`transform` 的结果长度和原表一致。它适合做“组内标准化、组内排名、组内去均值”。

例如，把每天的平均收益写回每一行：

```python
df["daily_mean_return"] = df.groupby("date")["return"].transform("mean")

print(df[["date", "asset", "return", "daily_mean_return"]])
```

这里 `daily_mean_return` 每一行都有值，同一天的股票共享同一个日均收益。

再做每天横截面去均值：

```python
df["return_demeaned"] = df["return"] - df["daily_mean_return"]

print(df[["date", "asset", "return_demeaned"]])
```

如果用 `agg` 得到每天均值，结果只有每天一行，不能直接作为新列赋给原表。`transform` 的价值就在于自动把组级结果对齐回原行。

## transform 做横截面 z-score

每天对因子值做横截面标准化：

```python
mean = df.groupby("date")["factor"].transform("mean")
std = df.groupby("date")["factor"].transform("std")

df["factor_z"] = (df["factor"] - mean) / std

print(df[["date", "asset", "factor", "factor_z"]])
```

这表示每一天内部，因子值减去当天均值，再除以当天标准差。

注意：pandas 的 `std` 默认 `ddof=1`，也就是样本标准差。这和 NumPy 的 `np.std` 默认 `ddof=0` 不同。做研究时要保持定义一致。

## transform 做组内排名

每天对股票按因子值排名：

```python
df["factor_rank"] = df.groupby("date")["factor"].rank(ascending=False)

print(df[["date", "asset", "factor", "factor_rank"]])
```

`ascending=False` 表示因子值越大排名越靠前，最大值 rank 为 1。

如果要归一化成百分位：

```python
df["factor_pct_rank"] = df.groupby("date")["factor"].rank(pct=True)

print(df[["date", "asset", "factor_pct_rank"]])
```

rank 在截面因子评估里很常见，例如构造分组组合、计算 RankIC、做极值处理前后比较。

## 按资产做时间序列统计

按资产分组可以沿时间方向计算统计量。

```python
asset_summary = df.groupby("asset").agg(
    mean_return=("return", "mean"),
    return_std=("return", "std"),
    mean_factor=("factor", "mean"),
)

print(asset_summary)
```

如果要把每只股票的时间序列均值写回原表：

```python
df["asset_mean_return"] = df.groupby("asset")["return"].transform("mean")

print(df[["date", "asset", "return", "asset_mean_return"]])
```

按日期分组和按资产分组含义完全不同：

- `groupby("date")`：横截面统计。
- `groupby("asset")`：时间序列统计。

## filter：按组筛选

`filter` 可以按组级条件保留或删除整组。

例如只保留至少有 2 条记录的行业：

```python
kept = df.groupby("industry").filter(lambda g: len(g) >= 2)

print(kept)
```

在真实数据里，可以用它删除样本太少的行业、股票或日期。但过度使用 `filter` 可能比较慢，简单条件优先考虑先用 `agg` 计算组统计，再 merge 或 map 回原表。

## 缺失分组键

默认情况下，分组键为缺失值的行会被排除。

```python
tmp = df.copy()
tmp.loc[0, "industry"] = None

print(tmp.groupby("industry")["return"].mean())
```

如果希望保留缺失组，可以使用 `dropna=False`：

```python
print(tmp.groupby("industry", dropna=False)["return"].mean())
```

缺失组是否应保留，取决于业务含义。行业缺失可能是数据问题，也可能代表“未分类”。

## groupby 排序

`groupby` 默认会对分组键排序。可以使用 `sort=False` 保留出现顺序：

```python
print(df.groupby("industry", sort=False)["return"].mean())
```

在多数统计结果里排序不是问题。但如果你依赖结果顺序，应该显式指定 `sort`，不要靠默认行为。

## 常见坑

### 1. 把 agg 结果当作原表长度

```python
daily_mean = df.groupby("date")["return"].mean()

# df["daily_mean"] = daily_mean  # 通常不是你想要的
```

`daily_mean` 的 index 是日期，长度是日期数量。原表 index 是行号，直接赋值可能按 index 对齐后产生大量缺失。要写回原表，用 `transform`：

```python
df["daily_mean"] = df.groupby("date")["return"].transform("mean")
```

### 2. 忘记 groupby 的方向

```python
df.groupby("date")["factor"].transform("mean")
df.groupby("asset")["factor"].transform("mean")
```

前者是每天横截面均值，后者是每只股票的时间序列均值。两者都能运行，但含义完全不同。

### 3. groupby.apply 滥用

`apply` 很灵活，但也更容易慢、更难读。能用内置聚合、`agg`、`transform`、`rank` 解决时，优先用这些明确接口。

```python
# 优先
df["factor_rank"] = df.groupby("date")["factor"].rank()
```

而不是一上来写复杂的 `groupby.apply`。

### 4. 多层列名后续难处理

```python
summary = df.groupby("date").agg({"return": ["mean", "std"]})
```

这会产生多层 columns。为了减少后续清理，优先使用 named aggregation。

### 5. std 的 ddof 不一致

pandas 的 `Series.std()` 默认 `ddof=1`。如果你在 NumPy 里用 `np.std()` 默认 `ddof=0`，结果会不同。标准化和风险统计里要明确这一点。

## 实战提示

选择 `agg` 还是 `transform`，可以用这个判断：

1. 结果是一组一行，用 `agg`。
2. 结果要写回原表、每行一个值，用 `transform`。
3. 只是组内排序，用 `groupby(...).rank()`。
4. 分组键有缺失时，显式决定是否使用 `dropna=False`。
5. 输出要给人读或后续 merge，优先 named aggregation。

量化研究里最常见的模式：

```python
# 每天横截面标准化
mean = df.groupby("date")["factor"].transform("mean")
std = df.groupby("date")["factor"].transform("std")
df["factor_z"] = (df["factor"] - mean) / std

# 每天汇总统计
daily_summary = df.groupby("date", as_index=False).agg(
    mean_return=("return", "mean"),
    n_assets=("asset", "nunique"),
)
```

## 自检问题

1. `agg` 和 `transform` 的输出长度有什么区别？
2. 为什么把每日均值写回原表时应该用 `transform("mean")`？
3. `groupby("date")` 和 `groupby("asset")` 在量化数据里分别代表什么方向？
4. named aggregation 相比普通多函数 `agg` 有什么好处？
5. pandas 的 `std` 默认 `ddof` 是多少？为什么要注意它？

