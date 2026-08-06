# pandas：缺失值处理

## 核心概念

pandas 里的缺失值通常表现为：

- `np.nan`：浮点缺失值。
- `None`：Python 空值，在很多 pandas 场景中会被视为缺失。
- `pd.NA`：pandas 的 nullable 缺失标记。
- `NaT`：时间戳缺失值。

缺失值处理的基本流程是：

1. 先检测缺失值。
2. 统计缺失比例和分布。
3. 判断缺失原因。
4. 决定删除、填充、保留还是标记。
5. 检查处理后是否引入未来信息或错误含义。

```python
import numpy as np
import pandas as pd

s = pd.Series([1.0, np.nan, None, 4.0])

print(s)
print(s.isna())
```

`isna()` 会把 `np.nan` 和 `None` 都识别为缺失。

## 检测缺失值

`isna()` 和 `notna()` 是最常用的缺失值检测函数。

```python
df = pd.DataFrame({
    "asset": ["AAA", "BBB", "CCC", "DDD"],
    "close": [100.0, np.nan, 20.0, 80.0],
    "volume": [1200, 800, np.nan, 500],
    "return": [0.01, -0.02, np.nan, None],
})

print(df.isna())
print(df.notna())
```

按列统计缺失数量：

```python
print(df.isna().sum())
```

按列统计缺失比例：

```python
missing_ratio = df.isna().mean()

print(missing_ratio)
```

`True` 会被当作 1，`False` 会被当作 0，因此 `mean()` 就是缺失比例。

## 检查哪些行有缺失

如果想找出任意列有缺失的行：

```python
rows_with_missing = df[df.isna().any(axis=1)]

print(rows_with_missing)
```

如果想找出所有关键列都不缺失的行：

```python
clean_rows = df[df[["close", "volume", "return"]].notna().all(axis=1)]

print(clean_rows)
```

这里 `axis=1` 表示按行聚合。`any(axis=1)` 是“这一行是否至少有一个缺失”，`all(axis=1)` 是“这一行是否全部满足条件”。

## dropna：删除缺失值

`dropna()` 可以删除含缺失值的行或列。

删除任意列有缺失的行：

```python
drop_any = df.dropna()

print(drop_any)
```

只检查特定列：

```python
drop_key = df.dropna(subset=["close", "return"])

print(drop_key)
```

删除缺失太多的列，可以用 `axis=1`：

```python
drop_cols = df.dropna(axis=1)

print(drop_cols)
```

删除是最简单的策略，但可能改变样本分布。比如只保留有完整数据的股票，可能偏向流动性好、上市时间长的股票，带来样本选择偏差。

## fillna：填充缺失值

`fillna()` 可以用固定值填充。

```python
filled_zero = df.fillna(0)

print(filled_zero)
```

但固定填 0 要非常谨慎。缺失收益不等于 0，缺失成交量不一定等于 0，缺失因子值也不一定代表中性水平。

更常见的是按列使用不同策略：

```python
filled = df.copy()
filled["volume"] = filled["volume"].fillna(0)
filled["return"] = filled["return"].fillna(filled["return"].mean())

print(filled)
```

这只是演示语法，不代表这两个填充策略一定适合所有业务。

## 前向填充与后向填充

时间序列中常见填充方式：

- `ffill()`：使用前一个有效值填充。
- `bfill()`：使用后一个有效值填充。

```python
prices = pd.Series(
    [100.0, np.nan, 102.0, np.nan, 101.0],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
    ]),
    name="close",
)

print(prices.ffill())
print(prices.bfill())
```

`ffill` 只使用过去已经出现的值，通常比 `bfill` 更符合预测场景。`bfill` 会使用未来值填过去，容易造成未来信息泄露。

可以限制最多填充几步：

```python
print(prices.ffill(limit=1))
```

`limit=1` 表示最多连续填充 1 个缺失值。长时间停牌或长时间缺数据时，不应该无限向前填充。

## 非有限值不是自动缺失

pandas 的 `isna()` 会识别 `NaN`，但不会把 `inf` 当作缺失。

```python
factor = pd.Series([1.0, np.nan, np.inf, -np.inf, 2.0])

print(factor.isna())
```

如果你要把正负无穷也当作坏值，需要显式处理：

```python
finite_mask = np.isfinite(factor)
factor_clean = factor.where(finite_mask)

print(factor_clean)
```

`where` 会保留满足条件的位置，不满足条件的位置变成缺失。

## replace：替换特殊标记

原始数据里经常用特殊值表示缺失，例如 `-999`、空字符串、`"NULL"`。

```python
raw = pd.Series([1.2, -999.0, 0.8, -999.0])

clean = raw.replace(-999.0, np.nan)

print(clean)
```

多个特殊标记可以一起替换：

```python
raw = pd.Series(["1.2", "", "NULL", "0.8"])

clean = raw.replace({"": np.nan, "NULL": np.nan})
clean = pd.to_numeric(clean)

print(clean)
```

先把特殊标记替换成真正缺失值，再转换为数值，是常见数据清洗流程。

## 实战例子：清洗横截面因子

假设某一天的因子值包含缺失和无穷：

```python
factor = pd.Series(
    [1.2, np.nan, np.inf, -0.5, 0.3],
    index=["AAA", "BBB", "CCC", "DDD", "EEE"],
    name="value_factor",
)

factor = factor.where(np.isfinite(factor))
valid_factor = factor.dropna()

print(factor)
print(valid_factor)
print(valid_factor.mean())
```

处理含义：

1. `np.inf` 被视为无效，变成缺失。
2. 原来的 `np.nan` 保持缺失。
3. `dropna()` 得到可用于横截面统计的样本。

是否删除缺失股票，取决于后续任务。如果是横截面打分，缺失因子通常应从这一因子的排序样本中剔除；如果是组合构建，还要确认剔除是否影响股票池约束。

## 实战例子：价格缺失与收益率

价格数据缺失时，直接算收益会产生缺失：

```python
prices = pd.Series(
    [100.0, np.nan, 102.0, 101.0],
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]),
)

returns = prices.pct_change(fill_method=None)

print(returns)
```

如果先 `ffill` 再算收益：

```python
returns_ffill = prices.ffill(limit=1).pct_change(fill_method=None)

print(returns_ffill)
```

这会把缺失日价格视为延续前值，因此缺失日收益为 0，下一天收益基于前值计算。这个假设可能适合某些停牌价格处理，也可能不适合真实可交易回测。关键是把假设写清楚。

## 实战例子：按列设置缺失阈值

假设你有一个因子矩阵，行是日期，列是股票：

```python
factor_panel = pd.DataFrame(
    {
        "AAA": [1.0, 1.1, np.nan, 1.3],
        "BBB": [np.nan, np.nan, np.nan, 0.5],
        "CCC": [2.0, 2.1, 2.2, 2.3],
    },
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]),
)

missing_by_asset = factor_panel.isna().mean()
keep_assets = missing_by_asset[missing_by_asset <= 0.5].index

filtered_panel = factor_panel[keep_assets]

print(missing_by_asset)
print(filtered_panel)
```

这里删除缺失比例超过 50% 的资产列。真实研究里，阈值应该来自数据质量要求，而不是随手设定。

## 常见坑

### 1. 直接填 0

```python
filled = df.fillna(0)
```

这很方便，但也很危险。缺失不等于 0。尤其是因子值、收益率、价格、财务指标，填 0 可能改变信号含义。

### 2. 用 bfill 造成未来信息泄露

```python
prices_filled = prices.bfill()
```

`bfill` 会用未来数据填过去。在预测和回测中，这通常是未来信息泄露。除非你有非常明确的离线数据修复理由，否则时间序列特征构造里应避免使用。

### 3. 忘记处理 inf

```python
factor = pd.Series([1.0, np.inf, 2.0])

print(factor.isna().sum())  # 0
```

`inf` 不会被 `isna()` 当作缺失。清洗数值因子时，通常要先用 `np.isfinite` 检查。

### 4. 删除缺失值造成样本选择偏差

只保留完整样本可能让股票池偏向大市值、高流动性、数据覆盖更好的公司。删除前应统计被删除样本的特征。

### 5. 混淆原始缺失和人工填充

填充后最好保留一个标记列或记录：

```python
df["close_was_missing"] = df["close"].isna()
df["close"] = df["close"].ffill()
```

这样后续模型或报告可以知道哪些值是原始观测，哪些值是填充得到的。

## 实战提示

处理缺失值时，建议固定写出数据质量摘要：

```python
summary = pd.DataFrame({
    "missing_count": df.isna().sum(),
    "missing_ratio": df.isna().mean(),
    "dtype": df.dtypes,
})

print(summary)
```

对于时间序列特征，优先问：

1. 这个缺失值在真实交易时点是否已经知道？
2. 填充是否用了未来信息？
3. 填充后的值是否改变了业务含义？
4. 是否需要保留“原本缺失”的标记？

## 自检问题

1. `isna()` 和 `notna()` 分别做什么？
2. 为什么不能无脑把缺失值填成 0？
3. `ffill` 和 `bfill` 在时间序列预测中的风险有什么不同？
4. 为什么 `np.inf` 需要单独处理？
5. 删除缺失样本可能带来什么偏差？

