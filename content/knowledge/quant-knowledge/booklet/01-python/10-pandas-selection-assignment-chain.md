# 10. pandas：选择、过滤、赋值与链式赋值

## 核心概念

pandas 选择数据时，最重要的是区分两套语义：

- `.loc`：按标签选择，也就是 index 和 column label。
- `.iloc`：按位置选择，也就是第几行、第几列。

常见规则：

- 取列：`df["col"]`
- 按标签取行列：`df.loc[row_label, col_label]`
- 按位置取行列：`df.iloc[row_pos, col_pos]`
- 按条件过滤：`df[mask]`
- 安全赋值：`df.loc[mask, "col"] = value`

链式赋值，例如 `df[mask]["col"] = value`，容易产生不确定行为，应避免。

## 准备数据

下面用一个简单行情表：

```python
import pandas as pd

df = pd.DataFrame(
    {
        "asset": ["AAA", "BBB", "CCC", "DDD"],
        "close": [100.0, 49.5, 20.0, 80.0],
        "volume": [1200, 800, 3000, 500],
        "return": [0.01, -0.02, 0.03, -0.01],
    },
    index=pd.to_datetime(["2024-01-02", "2024-01-02", "2024-01-02", "2024-01-02"]),
)

print(df)
```

这个例子里 index 是日期，但同一天有多只股票，所以 index 不唯一。为了演示更清楚，很多选择会直接使用列条件。

## 选择列

取单列会得到 `Series`：

```python
close = df["close"]

print(type(close))
print(close)
```

取多列会得到 `DataFrame`：

```python
sub = df[["asset", "close"]]

print(type(sub))
print(sub)
```

注意双层方括号：`df[["asset", "close"]]` 表示选择多列，返回二维表。

## 用 loc 按标签选择

`.loc` 的基本格式是：

```python
df.loc[row_selector, col_selector]
```

例如取所有行的两列：

```python
print(df.loc[:, ["asset", "return"]])
```

如果 index 唯一，可以按标签取某一行。当前例子 index 不唯一，因此同一个日期会返回多行：

```python
print(df.loc["2024-01-02"])
```

在时间序列数据中，日期 index 不唯一并不一定错，但你必须知道选择一个日期可能得到多条记录。

## 用 iloc 按位置选择

`.iloc` 按整数位置选择，不看 index 标签。

```python
print(df.iloc[0])       # 第 0 行
print(df.iloc[:2])      # 前 2 行
print(df.iloc[:2, :3])  # 前 2 行、前 3 列
```

`.iloc` 的切片和 Python 一样，左闭右开：`df.iloc[:2]` 取第 0、1 行，不包含第 2 行。

如果你只是想要“第几行”，用 `.iloc`。如果你想要“某个日期、某个股票代码”，用 `.loc` 或明确的条件过滤。

## 布尔过滤

布尔过滤用一个 True/False 的 Series 选择行。

```python
mask = df["volume"] > 1000

print(mask)
print(df[mask])
```

可以直接写：

```python
liquid = df[df["volume"] > 1000]

print(liquid)
```

这个例子筛选出成交量大于 1000 的股票。

## 多条件过滤

多个条件要用 `&`、`|`、`~`，并且每个条件用括号包起来。

```python
mask = (df["volume"] > 1000) & (df["return"] > 0)

print(df[mask])
```

不要写成：

```python
# mask = df["volume"] > 1000 and df["return"] > 0
```

`and` 是 Python 标量逻辑，不能用于 pandas Series 的逐元素判断。

常见写法：

```python
positive = df[df["return"] > 0]
not_positive = df[~(df["return"] > 0)]
large_or_positive = df[(df["volume"] > 1000) | (df["return"] > 0)]
```

## isin：集合过滤

筛选某些股票代码时，用 `.isin`：

```python
universe = ["AAA", "CCC"]

selected = df[df["asset"].isin(universe)]

print(selected)
```

这比写多个 `==` 条件更清楚，也更容易扩展。

## between：区间过滤

筛选数值区间可以用 `.between`：

```python
mid_price = df[df["close"].between(40, 100)]

print(mid_price)
```

默认包含两端，因此 `40 <= close <= 100`。

## 新增和修改列

新增一列很直接：

```python
df["dollar_volume"] = df["close"] * df["volume"]

print(df[["asset", "dollar_volume"]])
```

也可以基于条件赋值：

```python
df["liquid"] = False
df.loc[df["volume"] > 1000, "liquid"] = True

print(df[["asset", "volume", "liquid"]])
```

这里推荐使用：

```python
df.loc[mask, "col"] = value
```

这能明确表示“在原 DataFrame 的某些行、某一列上写入”。

## assign：函数式新增列

如果你不想原地修改原 DataFrame，可以用 `.assign` 返回新 DataFrame。

```python
df2 = df.assign(
    abs_return=df["return"].abs(),
    signed_volume=df["volume"] * df["return"].apply(lambda x: 1 if x > 0 else -1),
)

print(df2[["asset", "abs_return", "signed_volume"]])
```

`.assign` 适合流水线风格代码。需要注意的是，复杂逻辑不一定非要塞进一行；可读性更重要。

## 链式赋值问题

不要写：

```python
# df[df["volume"] > 1000]["liquid"] = True
```

这叫链式赋值。第一步 `df[df["volume"] > 1000]` 可能返回临时对象，第二步 `["liquid"] = True` 可能只改了临时对象，而没有改原始 `df`。

正确写法是：

```python
df.loc[df["volume"] > 1000, "liquid"] = True
```

链式赋值的问题不是“永远不生效”，而是你不应该依赖它是否生效。不同 pandas 版本、不同数据路径、不同 copy/view 行为，都可能让结果变得难以判断。

## 过滤后要修改：显式 copy

如果你要先筛选一部分数据，再独立修改它，建议显式 `.copy()`：

```python
liquid = df[df["volume"] > 1000].copy()
liquid["rank"] = liquid["return"].rank(ascending=False)

print(liquid[["asset", "return", "rank"]])
```

这表示 `liquid` 是独立表。你修改 `liquid`，不是在修改原始 `df`。

如果你的目标是修改原始 `df`，不要创建中间过滤表，直接用 `.loc`：

```python
df.loc[df["volume"] > 1000, "rank_flag"] = 1
```

## 实战例子：构造可交易股票池

假设你要筛选一个简单股票池：

- 成交量大于 1000。
- 收益率不是极端负数，大于 -5%。
- 股票代码在候选池中。

```python
candidate_assets = ["AAA", "BBB", "CCC"]

mask = (
    (df["volume"] > 1000)
    & (df["return"] > -0.05)
    & (df["asset"].isin(candidate_assets))
)

tradable = df.loc[mask, ["asset", "close", "volume", "return"]].copy()

print(tradable)
```

这里 `.copy()` 的含义是：筛选出的 `tradable` 将作为后续独立研究对象，不再依赖原始表的视图关系。

## 实战例子：安全地写入信号

假设你想在原表中写入一个简单信号：收益率为正且成交量大于 1000 的股票标记为 1，否则为 0。

```python
df["signal"] = 0
signal_mask = (df["return"] > 0) & (df["volume"] > 1000)
df.loc[signal_mask, "signal"] = 1

print(df[["asset", "return", "volume", "signal"]])
```

这段代码有两个优点：

1. 默认值和条件覆盖很明确。
2. 写入发生在原始 `df` 上，不存在链式赋值歧义。

## 常见坑

### 1. loc 和 iloc 混用

```python
s = pd.Series([10, 20, 30], index=[100, 101, 102])

print(s.loc[100])   # 标签 100
print(s.iloc[0])    # 第 0 个位置
```

如果 index 是整数，`.loc[100]` 和 `.iloc[100]` 完全不是一回事。

### 2. 多条件过滤忘记括号

```python
# 错误或容易出错
# df[df["volume"] > 1000 & df["return"] > 0]
```

正确写法：

```python
df[(df["volume"] > 1000) & (df["return"] > 0)]
```

括号不是装饰，而是确保运算优先级正确。

### 3. 过滤后直接赋值

```python
# 不推荐
# df[df["volume"] > 1000]["signal"] = 1
```

推荐：

```python
df.loc[df["volume"] > 1000, "signal"] = 1
```

### 4. 以为 df[mask] 一定是视图

pandas 不应该按 NumPy 的视图/拷贝规则去猜。过滤结果是否共享底层数据不是你应该依赖的接口。需要独立对象就 `.copy()`；需要改原表就 `.loc`。

### 5. 用 apply 做简单条件

```python
# 可以运行，但没必要
df["is_positive"] = df["return"].apply(lambda x: x > 0)
```

更直接：

```python
df["is_positive"] = df["return"] > 0
```

简单逐元素条件优先用向量化表达式。

## 实战提示

写 pandas 选择和赋值代码时，可以按这个规则：

1. 取列：`df["col"]` 或 `df[["col1", "col2"]]`。
2. 按标签选：`.loc`。
3. 按位置选：`.iloc`。
4. 过滤后独立使用：`df[mask].copy()`。
5. 修改原表：`df.loc[mask, "col"] = value`。
6. 多条件过滤：每个条件加括号，用 `&`、`|`、`~`。

在研究代码里，宁可多写几行，也要把“筛选的是哪些行、写入的是哪个表”表达清楚。

## 自检问题

1. `.loc` 和 `.iloc` 的区别是什么？
2. 为什么多个 pandas 条件要用 `&`，而不是 `and`？
3. 为什么不推荐 `df[mask]["col"] = value`？
4. 什么时候应该在过滤后使用 `.copy()`？
5. 如果要修改原始 DataFrame 中满足条件的行，推荐写法是什么？

