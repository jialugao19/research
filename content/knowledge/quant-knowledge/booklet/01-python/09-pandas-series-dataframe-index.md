# 09. pandas：Series、DataFrame 与 Index

## 核心概念

pandas 的核心数据结构有三个：

- `Series`：带索引的一维数据。
- `DataFrame`：带行索引和列索引的二维表格。
- `Index`：行标签或列标签，用来对齐、选择和标识数据。

可以把 `Series` 理解成“带名字的一列”，把 `DataFrame` 理解成“由多列 Series 组成的表”。

```python
import pandas as pd

s = pd.Series([0.01, -0.02, 0.03], index=["A", "B", "C"], name="return")

print(s)
```

输出：

```text
A    0.01
B   -0.02
C    0.03
Name: return, dtype: float64
```

左边的 `A/B/C` 是 index，右边是 value，`return` 是这列数据的名字。

## Series：一维带标签数组

`Series` 很适合表示某一天的横截面数据，例如 3 只股票的收益率：

```python
returns = pd.Series(
    [0.01, -0.02, 0.03],
    index=["AAA", "BBB", "CCC"],
    name="return",
)

print(returns.index)
print(returns.values)
print(returns.name)
```

输出中：

- `returns.index` 是股票代码标签。
- `returns.values` 是底层数值数组。
- `returns.name` 是这个 Series 的名称。

Series 的一个关键能力是按 index 对齐：

```python
returns = pd.Series([0.01, -0.02, 0.03], index=["AAA", "BBB", "CCC"])
weights = pd.Series([0.5, 0.3, 0.2], index=["AAA", "CCC", "BBB"])

weighted = returns * weights

print(weighted)
print(weighted.sum())
```

虽然 `weights` 的顺序是 `AAA, CCC, BBB`，但 pandas 会按标签对齐，而不是按位置相乘。结果等价于：

```text
AAA: 0.01 * 0.5
BBB: -0.02 * 0.2
CCC: 0.03 * 0.3
```

这对金融数据很重要，因为资产列表经常排序不同。

## DataFrame：二维表格

`DataFrame` 可以从字典创建。字典的 key 会变成列名。

```python
df = pd.DataFrame({
    "close": [100.0, 102.0, 101.0],
    "volume": [1000, 1200, 900],
})

print(df)
```

输出：

```text
   close  volume
0  100.0    1000
1  102.0    1200
2  101.0     900
```

默认行索引是 `RangeIndex(start=0, stop=3, step=1)`。在时间序列数据里，通常会显式使用日期作为 index：

```python
dates = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"])

prices = pd.DataFrame(
    {
        "AAA": [100.0, 102.0, 101.0],
        "BBB": [50.0, 49.5, 51.0],
    },
    index=dates,
)

print(prices)
print(prices.index)
print(prices.columns)
```

这里：

- `prices.index` 是日期索引。
- `prices.columns` 是资产代码。
- `prices.loc["2024-01-03", "AAA"]` 表示 2024-01-03 这天 AAA 的价格。

## Index 是数据语义的一部分

在 pandas 里，index 不只是行号，而是数据标签。很多运算会按 index 对齐。

```python
a = pd.Series([1.0, 2.0, 3.0], index=["x", "y", "z"])
b = pd.Series([10.0, 20.0, 30.0], index=["z", "x", "y"])

print(a + b)
```

输出：

```text
x    21.0
y    32.0
z    13.0
dtype: float64
```

计算过程按标签对齐：

- `x`: `1.0 + 20.0`
- `y`: `2.0 + 30.0`
- `z`: `3.0 + 10.0`

这和 NumPy 的按位置运算不同：

```python
print(a.to_numpy() + b.to_numpy())  # [11. 22. 33.]
```

因此，pandas 的 index 是保护，也是风险：它能防止错位相乘，但如果 index 本身错了，结果也会跟着错。

## DataFrame 的行索引和列索引

DataFrame 同时有行索引和列索引：

```python
print(prices.index)
print(prices.columns)
print(prices.shape)
```

如果 `prices.shape == (3, 2)`，表示 3 行、2 列。在这个例子中：

- 行：日期。
- 列：股票代码。

可以把每一列取出来，它会变成一个 Series：

```python
aaa = prices["AAA"]

print(type(aaa))
print(aaa)
```

这个 Series 的 index 仍然是日期。这意味着列数据不会丢掉时间标签。

## 从长表和宽表理解 DataFrame

金融数据经常有两种组织方式。

宽表：行是日期，列是资产。

```python
wide = pd.DataFrame(
    {
        "AAA": [0.01, 0.02],
        "BBB": [-0.01, 0.00],
    },
    index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
)

print(wide)
```

长表：每行是一条观测，列里显式放日期、资产和数值。

```python
long = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"]),
    "asset": ["AAA", "BBB", "AAA", "BBB"],
    "return": [0.01, -0.01, 0.02, 0.00],
})

print(long)
```

宽表适合矩阵计算和横截面运算，长表适合存储、合并、分组和数据库风格处理。后面会单独讲长表/宽表组织和因子面板。

## DatetimeIndex：时间序列的常见索引

行情和因子数据通常用日期或时间戳作为索引。

```python
dates = pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"])
close = pd.Series([100.0, 102.0, 101.0], index=dates, name="close")

print(close.index)
print(close.index.dtype)
```

`DatetimeIndex` 的好处是 pandas 能理解时间顺序，后续可以做重采样、滚动窗口、时间切片等操作。

不过，只把字符串看起来写成日期还不够。应该显式转换：

```python
df = pd.DataFrame({
    "date": ["2024-01-02", "2024-01-03"],
    "close": [100.0, 102.0],
})

df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

print(df.index)
```

## Index 唯一性

很多操作默认假设 index 能唯一标识一行。可以检查 index 是否唯一：

```python
df = pd.DataFrame(
    {"close": [100.0, 101.0, 102.0]},
    index=pd.to_datetime(["2024-01-02", "2024-01-02", "2024-01-03"]),
)

print(df.index.is_unique)  # False
```

重复 index 不一定错误。例如 tick 数据里，同一时间戳可能有多笔成交。但你必须知道它存在，因为选择、合并、对齐时的结果可能和唯一 index 不同。

如果你的数据应该是一只股票每天一行，那么重复日期通常是数据质量问题。

## MultiIndex 的最小概念

长表数据有时会用多个键组成索引，例如日期和资产。

```python
panel = long.set_index(["date", "asset"])

print(panel)
print(panel.index.names)
```

这种索引叫 `MultiIndex`。它可以表达“同一天、同一只股票”的二维键。

本篇只需要知道 MultiIndex 是复合索引。更复杂的选择、重排、宽表长表转换会在后续 pandas 小节里展开。

## to_numpy：什么时候脱离 pandas

如果你只需要纯数值矩阵，可以用 `.to_numpy()`：

```python
matrix = prices.to_numpy()

print(matrix)
print(type(matrix))
```

这会得到 NumPy 数组。注意：NumPy 数组不再保留 index 和 columns。

```python
print(prices.index)
print(prices.columns)
print(matrix.shape)
```

脱离 pandas 后，所有计算都按位置进行。进入模型或矩阵运算前，应确认行列顺序已经固定，并保存必要的标签映射。

## 常见坑

### 1. 把 index 当作普通行号

```python
s = pd.Series([10, 20, 30], index=[100, 101, 102])

print(s.index)  # Index([100, 101, 102], dtype='int64')
```

这里的 index 是标签 `100/101/102`，不是第 100、101、102 行。位置选择和标签选择是两套语义，下一篇会详细讲 `loc` 和 `iloc`。

### 2. 忘记 index 对齐

```python
returns = pd.Series([0.01, -0.02, 0.03], index=["AAA", "BBB", "CCC"])
weights = pd.Series([0.5, 0.3, 0.2], index=["AAA", "CCC", "DDD"])

print(returns * weights)
```

输出会包含 `BBB` 和 `DDD` 的 `NaN`，因为它们只出现在其中一个 Series 里。对齐能暴露缺失匹配，但你需要决定是否填充、剔除或报错。

### 3. 日期还是字符串

```python
df = pd.DataFrame({"date": ["2024-1-2", "2024-1-10"]})

print(df["date"].dtype)  # object
```

字符串日期不是时间索引。时间序列处理前应使用 `pd.to_datetime`，否则排序、切片、重采样可能不符合预期。

### 4. 默认 RangeIndex 丢失业务含义

```python
df = pd.DataFrame({"close": [100.0, 102.0, 101.0]})

print(df.index)  # RangeIndex(start=0, stop=3, step=1)
```

如果这些价格对应具体日期，默认 index 无法表达时间。研究代码里应尽早把日期、资产代码等关键标识放到 index 或列中。

### 5. 转成 NumPy 后丢掉标签

```python
matrix = prices.to_numpy()
```

`matrix` 只有位置，没有日期和股票代码。后续如果要把模型输出映射回日期和资产，必须保留 `prices.index` 和 `prices.columns`。

## 实战提示

读入任何 pandas 数据后，先检查这些信息：

```python
print(df.shape)
print(df.index)
print(df.columns)
print(df.dtypes)
print(df.index.is_unique)
```

对于行情或因子数据，还建议明确写下注释：

```python
# prices: DataFrame, index=date, columns=asset, values=close price
# returns: DataFrame, index=date, columns=asset, values=daily return
```

这样后续做对齐、rolling、merge、回测时，不容易混淆行列含义。

## 自检问题

1. `Series` 和 `DataFrame` 的区别是什么？
2. pandas 的 index 为什么不只是行号？
3. 两个 Series 相乘时，pandas 默认按位置对齐还是按 index 对齐？
4. 为什么时间序列数据通常要用 `DatetimeIndex`？
5. `to_numpy()` 之后会丢失哪些 pandas 信息？

