# pandas：因子数据面板的长表/宽表组织

## 核心概念

量化研究里经常会遇到“时间 × 标的”的数据面板。例如：

- 每个交易日、每只股票有一个因子值。
- 每个交易日、每只股票有一个未来 1 日收益。
- 每个交易日、每只股票还有行业、市值、是否停牌等属性。

这种数据通常有两种常用组织方式：

1. 长表：一行代表一个观测点，例如 `(date, asset)`。
2. 宽表：行是 `date`，列是 `asset`，单元格是某一个变量的值。

长表适合存储、合并、分组统计、保留多个字段；宽表适合矩阵计算、横截面排名、与收益矩阵逐元素对齐。

核心原则：先明确每一行的粒度，再决定用长表还是宽表。

## 准备数据

```python
import numpy as np
import pandas as pd

long = pd.DataFrame({
    "date": [
        "2024-01-02", "2024-01-02", "2024-01-02",
        "2024-01-03", "2024-01-03", "2024-01-03",
        "2024-01-04", "2024-01-04",
    ],
    "asset": ["AAA", "BBB", "CCC", "AAA", "BBB", "CCC", "AAA", "BBB"],
    "value_factor": [1.20, -0.40, 0.60, 1.40, -0.10, 0.20, 0.90, -0.60],
    "quality_factor": [0.80, 0.50, 0.70, 0.90, 0.40, 0.65, 0.70, 0.55],
    "return_fwd_1d": [0.012, -0.004, 0.005, 0.006, -0.010, 0.002, -0.003, 0.008],
    "industry": ["tech", "finance", "health", "tech", "finance", "health", "tech", "finance"],
    "market_cap": [120, 80, 60, 125, 78, 62, 123, 81],
})

long["date"] = pd.to_datetime(long["date"])
long = long.sort_values(["date", "asset"]).reset_index(drop=True)

print(long)
```

这个表的行粒度是 `(date, asset)`：某一天、某个标的的一条观测。

正式计算前，应该先检查主键是否唯一：

```python
key_cols = ["date", "asset"]

duplicate_count = long.duplicated(key_cols).sum()
print(duplicate_count)

assert duplicate_count == 0
```

这一步很重要。后面的 `pivot`、对齐、回测统计都默认一个 `(date, asset)` 只有一条记录。

## 长表适合什么

长表的优点是字段可以自然扩展。

```python
print(long[["date", "asset", "value_factor", "return_fwd_1d", "industry"]])
```

例如，按行业计算每天的平均因子值：

```python
industry_mean = (
    long
    .groupby(["date", "industry"])["value_factor"]
    .mean()
)

print(industry_mean)
```

再例如，把因子表和收益表合并：

```python
factor_long = long[["date", "asset", "value_factor"]]
return_long = long[["date", "asset", "return_fwd_1d"]]

panel = factor_long.merge(
    return_long,
    on=["date", "asset"],
    how="inner",
    validate="one_to_one",
)

print(panel)
```

`validate="one_to_one"` 能帮你防止无意中把重复键 merge 成笛卡尔积。

长表通常适合：

- 从数据库或 parquet 文件读取和保存。
- 合并行业、市值、收益、风险暴露等多个字段。
- 用 `groupby` 做按日期、行业、分组的统计。
- 保留不规则面板，例如某些日期缺少某些标的。

## 宽表适合什么

宽表把一个变量变成矩阵：

```python
factor_wide = long.pivot(
    index="date",
    columns="asset",
    values="value_factor",
)

return_wide = long.pivot(
    index="date",
    columns="asset",
    values="return_fwd_1d",
)

print(factor_wide)
print(return_wide)
```

`factor_wide` 的行是日期，列是标的，值是 `value_factor`。

宽表适合做横截面计算，例如每天对因子做百分位排名：

```python
rank_pct = factor_wide.rank(axis=1, pct=True)

print(rank_pct)
```

也适合做逐元素运算。下面构造一个简单多空信号：

```python
signal = pd.DataFrame(0, index=factor_wide.index, columns=factor_wide.columns)
signal[rank_pct >= 0.67] = 1
signal[rank_pct <= 0.33] = -1

print(signal)
```

如果这个信号是在当日收盘后才能得到，不能直接乘同一天的收益；通常要按交易逻辑做滞后处理。这里先展示矩阵形态的逐元素计算：

```python
pnl_by_asset = signal.shift(1) * return_wide
daily_pnl = pnl_by_asset.mean(axis=1)

print(daily_pnl)
```

`shift` 是否正确、收益是否是未来收益、是否发生信息泄露，是下一小节单独讨论的内容。

## 长表转宽表：pivot

当 `(date, asset)` 唯一时，用 `pivot` 最清楚。

```python
quality_wide = long.pivot(
    index="date",
    columns="asset",
    values="quality_factor",
)

print(quality_wide)
```

`pivot` 不做聚合。如果同一个 `(date, asset)` 出现多行，它会报错，这通常是好事，因为重复记录应该先查清楚。

```python
dupe = pd.concat(
    [
        long,
        long.iloc[[0]].assign(value_factor=2.00),
    ],
    ignore_index=True,
)

print(dupe.duplicated(["date", "asset"], keep=False).sum())

# 这行会报错：Index contains duplicate entries, cannot reshape
# dupe.pivot(index="date", columns="asset", values="value_factor")
```

不要在没检查原因的情况下直接改用 `pivot_table`。

## pivot_table：能聚合，但可能掩盖问题

`pivot_table` 可以处理重复键，因为它会聚合。

```python
mean_factor = dupe.pivot_table(
    index="date",
    columns="asset",
    values="value_factor",
    aggfunc="mean",
)

print(mean_factor)
```

这在确实需要聚合时很有用。例如一个 `(date, asset)` 下有多笔交易，需要汇总成日频值。

但在因子面板里，如果理论上每个 `(date, asset)` 只应该有一个因子值，`pivot_table(..., aggfunc="mean")` 可能把上游数据错误悄悄平均掉。

更稳妥的流程是：

```python
bad_keys = dupe.loc[
    dupe.duplicated(["date", "asset"], keep=False),
    ["date", "asset"],
]

print(bad_keys.drop_duplicates())
```

先定位重复键，再决定应该去重、聚合、还是修复上游逻辑。

## 宽表转长表：stack

宽表可以用 `stack` 变回长表。

```python
factor_long_again = (
    factor_wide
    .stack(future_stack=True)
    .rename("value_factor")
    .reset_index()
)

print(factor_long_again)
```

这里使用 `future_stack=True`，采用 pandas 新版 `stack` 行为，会保留宽表中缺失的 `(date, asset)` 组合。

例如 `CCC` 在 `2024-01-04` 没有记录，宽表里会出现缺失值。是否保留这类缺失组合，取决于后续计算：

- 如果要检查面板覆盖率，保留缺失组合更方便。
- 如果要恢复原始观测记录，可以在转回长表后过滤缺失值。

```python
observed_factor_long = factor_long_again.dropna(subset=["value_factor"])

print(observed_factor_long)
```

## 宽表转长表：melt

如果宽表是普通列，也可以用 `melt`。

```python
factor_wide_reset = factor_wide.reset_index()

factor_long_melt = factor_wide_reset.melt(
    id_vars="date",
    var_name="asset",
    value_name="value_factor",
)

print(factor_long_melt)
```

`stack` 更适合从带有 `index` 和 `columns` 名称的矩阵恢复长表；`melt` 更适合处理普通列结构的数据。

## 多个因子的组织方式

如果长表里有多个因子列，可以保留为多列：

```python
factor_columns = ["value_factor", "quality_factor"]

print(long[["date", "asset"] + factor_columns])
```

这种方式适合常规研究流水线，因为每个 `(date, asset)` 的所有字段都在同一行。

如果要做矩阵计算，通常为每个因子生成一个宽表：

```python
value_matrix = long.pivot(index="date", columns="asset", values="value_factor")
quality_matrix = long.pivot(index="date", columns="asset", values="quality_factor")

combined_score = value_matrix.rank(axis=1, pct=True) + quality_matrix.rank(axis=1, pct=True)

print(combined_score)
```

也可以使用带多层列索引的宽表：

```python
wide_multi = long.pivot(
    index="date",
    columns="asset",
    values=["value_factor", "quality_factor", "return_fwd_1d"],
)

print(wide_multi)
print(wide_multi["value_factor"])
```

多层列索引可以同时保存多个变量，但代码复杂度更高。研究早期通常先用长表，等需要矩阵计算时再拆成单变量宽表。

## MultiIndex 长表

长表也可以把 `(date, asset)` 放进索引。

```python
mi_panel = long.set_index(["date", "asset"]).sort_index()

print(mi_panel)
print(mi_panel.index.is_unique)
```

取某一天的横截面：

```python
one_day = mi_panel.loc[pd.Timestamp("2024-01-03")]

print(one_day)
```

取某只股票的时间序列：

```python
aaa_path = mi_panel.xs("AAA", level="asset")

print(aaa_path)
```

MultiIndex 适合表达“主键就是 `(date, asset)`”的面板数据。它仍然是长表，不等于宽矩阵。

## 因子矩阵和收益矩阵的对齐

实际项目中，因子矩阵和收益矩阵很可能来自不同文件。计算前必须对齐日期和标的。

```python
factor_aligned, return_aligned = factor_wide.align(
    return_wide,
    join="inner",
    axis=None,
)

print(factor_aligned.index.equals(return_aligned.index))
print(factor_aligned.columns.equals(return_aligned.columns))
```

`join="inner"` 只保留两边共同存在的日期和标的。

如果想检查共同非缺失样本，可以构造掩码：

```python
valid = factor_aligned.notna() & return_aligned.notna()

print(valid)
```

例如，计算每天的横截面相关性：

```python
ic_by_date = (
    factor_aligned.where(valid)
    .corrwith(return_aligned.where(valid), axis=1)
)

print(ic_by_date)
```

这里的相关性只是演示面板对齐方法，不代表这个小样本有统计意义。

## 选择长表还是宽表

一般经验：

- 数据入口、清洗、合并、保存：优先长表。
- 横截面排名、矩阵乘法、逐元素收益计算：转成宽表。
- 多个字段一起管理：长表更清楚。
- 单个变量做矩阵计算：宽表更直接。
- 数据稀疏、标的不固定：长表通常更节省空间，也更容易定位缺失。

不要在整个项目中频繁来回转换。常见做法是：清洗阶段维护长表，进入具体计算函数时转成宽表，计算完再把结果转回长表保存。

## 常见坑

第一，没检查重复键就 `pivot_table`。

```python
assert not long.duplicated(["date", "asset"]).any()
```

如果这句不通过，应先查重复来源，而不是直接平均。

第二，行粒度定义不完整。

如果同一只股票同一天有多个预测期限，就不能只用 `(date, asset)` 做主键，而要加入 `horizon`：

```python
# 例：更完整的主键可能是 ["date", "asset", "horizon"]
```

第三，把缺失资产填成 0。

```python
# 谨慎：这会把“没有观测”变成“因子值为 0”
# factor_wide = factor_wide.fillna(0)
```

缺失通常代表未上市、停牌、无数据或不在股票池里，不能随便当作真实的 0。

第四，转成 NumPy 后丢掉标签。

```python
factor_array = factor_wide.to_numpy()

print(factor_wide.index)
print(factor_wide.columns)
```

`factor_array` 本身不再知道哪一行是哪天、哪一列是哪只股票。只要后面还要回到 pandas 或和别的矩阵对齐，就必须保留 `index` 和 `columns`。

第五，把多个变量混在一张宽表的普通列名里。

例如列名写成 `AAA_value`、`AAA_return`、`BBB_value`、`BBB_return`，后续对齐会很麻烦。更好的选择是：

- 长表多列保存。
- 每个变量一张宽表。
- 或使用 MultiIndex columns。

## 实战提示

每次把因子表交给下游计算前，可以做一组轻量检查：

```python
assert long["date"].notna().all()
assert long["asset"].notna().all()
assert not long.duplicated(["date", "asset"]).any()

factor_wide = long.pivot(index="date", columns="asset", values="value_factor")
return_wide = long.pivot(index="date", columns="asset", values="return_fwd_1d")

assert factor_wide.index.is_monotonic_increasing
assert factor_wide.index.equals(return_wide.index)
assert factor_wide.columns.equals(return_wide.columns)
```

如果因子和收益来自不同源，不要假设它们自动对齐：

```python
factor_wide, return_wide = factor_wide.align(return_wide, join="inner", axis=None)
```

在回测和建模里，标签比数值更重要。只要日期或标的错位，计算出来的数字越精确，误导性越强。

## 小结

长表和宽表不是谁替代谁，而是服务于不同环节：

- 长表回答“每条观测是什么”。
- 宽表回答“这个变量的时间 × 标的矩阵是什么”。
- `pivot`、`stack`、`melt`、`align` 是两者之间最常用的转换与对齐工具。

因子研究里，先守住 `(date, asset)` 粒度和标签对齐，再谈排名、IC、回测收益。

## 自检问题

1. 为什么因子长表在 `pivot` 前要检查 `(date, asset)` 是否唯一？
2. `pivot` 和 `pivot_table` 的关键区别是什么？
3. 什么时候应该使用长表，什么时候应该转成宽表？
4. 为什么不能随意把宽表里的缺失值填成 0？
5. 因子矩阵和收益矩阵做逐元素计算前，应该检查哪些标签是否一致？
