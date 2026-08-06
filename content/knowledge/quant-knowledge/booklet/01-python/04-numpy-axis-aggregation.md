# NumPy：axis 语义与聚合

## 核心概念

NumPy 里的 `axis` 表示“沿着哪个维度做操作”。对数组做 `sum`、`mean`、`std`、`max` 这类聚合时，`axis` 决定哪个维度会被压缩掉。

对二维数组来说：

- `axis=0`：沿着行方向聚合，压缩行，结果按列保留。
- `axis=1`：沿着列方向聚合，压缩列，结果按行保留。

如果一个收益率矩阵 `returns.shape == (T, N)`，并约定：

- 行是时间，例如交易日。
- 列是资产，例如股票。

那么：

- `returns.mean(axis=0)`：每只股票跨时间的平均收益，结果 shape 是 `(N,)`。
- `returns.mean(axis=1)`：每天所有股票的横截面平均收益，结果 shape 是 `(T,)`。

## 最小例子

```python
import numpy as np

x = np.array([
    [1, 2, 3],
    [4, 5, 6],
])

print(x.shape)       # (2, 3)
print(x.sum())       # 21
print(x.sum(axis=0)) # [5 7 9]
print(x.sum(axis=1)) # [ 6 15]
```

理解 `axis` 的一个实用方法是：指定的那个维度会消失。

```python
print(x.shape)              # (2, 3)
print(x.sum(axis=0).shape)  # (3,)
print(x.sum(axis=1).shape)  # (2,)
```

`axis=0` 让第 0 维，也就是长度为 2 的行维度消失，所以结果剩下列维度 `(3,)`。`axis=1` 让第 1 维，也就是长度为 3 的列维度消失，所以结果剩下行维度 `(2,)`。

## 量化例子：时间序列均值与横截面均值

假设有 4 天、3 只股票的收益率：

```python
returns = np.array([
    [0.01,  0.02, -0.01],
    [0.03,  0.01,  0.02],
    [-0.02, 0.00,  0.01],
    [0.00, -0.01,  0.03],
])

mean_by_asset = returns.mean(axis=0)
mean_by_day = returns.mean(axis=1)

print(mean_by_asset)  # [0.005 0.005 0.0125]
print(mean_by_day)    # [0.00666667 0.02       -0.00333333 0.00666667]
```

`mean_by_asset` 是每只股票 4 天的平均收益。`mean_by_day` 是每天 3 只股票的平均收益。

这两个统计量回答的是不同问题：

- `axis=0`：某只股票在时间维度上表现如何？
- `axis=1`：某一天市场横截面整体表现如何？

## keepdims：保留可广播形状

默认情况下，聚合会删除对应维度：

```python
daily_mean = returns.mean(axis=1)

print(daily_mean.shape)  # (4,)
```

如果后续要和原矩阵做广播运算，推荐使用 `keepdims=True`：

```python
daily_mean_2d = returns.mean(axis=1, keepdims=True)

print(daily_mean_2d.shape)  # (4, 1)

demeaned = returns - daily_mean_2d
print(demeaned.shape)      # (4, 3)
```

横截面去均值时，`daily_mean_2d.shape == (T, 1)`，可以明确表示“每一天一个均值，广播到当天所有资产”。

同理，按资产做时间序列去均值时：

```python
asset_mean_2d = returns.mean(axis=0, keepdims=True)
demeaned_by_asset = returns - asset_mean_2d

print(asset_mean_2d.shape)     # (1, 3)
print(demeaned_by_asset.shape) # (4, 3)
```

`asset_mean_2d.shape == (1, N)`，可以明确表示“每只资产一个均值，广播到所有日期”。

## 多轴聚合

高维数组可以同时沿多个轴聚合。

假设一个数组 `panel.shape == (T, N, F)`，分别表示：

- `T`：日期。
- `N`：资产。
- `F`：特征。

```python
panel = np.arange(2 * 3 * 4).reshape(2, 3, 4)

print(panel.shape)                 # (2, 3, 4)
print(panel.mean(axis=0).shape)    # (3, 4)
print(panel.mean(axis=1).shape)    # (2, 4)
print(panel.mean(axis=2).shape)    # (2, 3)
print(panel.mean(axis=(0, 1)).shape)  # (4,)
```

`axis=(0, 1)` 表示同时压缩日期和资产维度，最后保留特征维度。因此结果是每个特征在所有日期、所有资产上的平均值。

如果保留维度：

```python
feature_mean = panel.mean(axis=(0, 1), keepdims=True)

print(feature_mean.shape)  # (1, 1, 4)
```

这个 shape 可以广播回原来的 `(T, N, F)`。

## 常用聚合函数

NumPy 中常见聚合函数包括：

- `sum`：求和。
- `mean`：均值。
- `std`：标准差。
- `var`：方差。
- `min` / `max`：最小值和最大值。
- `argmin` / `argmax`：最小值或最大值的位置。
- `median`：中位数。
- `quantile`：分位数。
- `all` / `any`：布尔数组聚合。

例子：

```python
x = np.array([
    [1.0, 5.0, 3.0],
    [4.0, 2.0, 6.0],
])

print(x.max(axis=0))     # [4. 5. 6.]
print(x.argmax(axis=1))  # [1 2]
print(np.median(x, axis=0))  # [2.5 3.5 4.5]
print(np.quantile(x, 0.5, axis=1))  # [3. 4.]
```

`argmax(axis=1)` 返回每一行最大值的位置。对于第一行 `[1.0, 5.0, 3.0]`，最大值在下标 1；对于第二行 `[4.0, 2.0, 6.0]`，最大值在下标 2。

## 缺失值场景：nan 聚合

普通聚合遇到 `np.nan` 通常会得到 `nan`：

```python
x = np.array([
    [1.0, np.nan, 3.0],
    [4.0, 5.0, np.nan],
])

print(x.mean(axis=0))  # [2.5 nan nan]
```

如果希望忽略缺失值，可以使用 `nanmean`、`nanstd`、`nanmedian`、`nanmax` 等函数：

```python
print(np.nanmean(x, axis=0))  # [2.5 5.  3. ]
print(np.nanmean(x, axis=1))  # [2.  4.5]
```

金融数据里，停牌、未上市、数据缺失都可能产生 `nan`。在做横截面统计时，要明确你的策略是“忽略缺失值”还是“把缺失值视为不可交易样本并剔除”。

## ddof：样本标准差与总体标准差

`np.std` 默认使用 `ddof=0`，也就是总体标准差。样本标准差通常使用 `ddof=1`。

```python
x = np.array([1.0, 2.0, 3.0])

print(np.std(x, ddof=0))  # 0.816496580927726
print(np.std(x, ddof=1))  # 1.0
```

在统计估计中，如果你把数据看作从总体中抽出的样本，常见做法是使用 `ddof=1`。在特征标准化或机器学习预处理里，也经常使用 `ddof=0`。关键是保持一致，并知道自己用的是哪一种定义。

## 实战例子：横截面标准化

横截面标准化常用于因子处理。假设 `factor.shape == (T, N)`，行是日期，列是股票。每天对所有股票的因子值做 z-score：

```python
factor = np.array([
    [1.2, 0.5, 2.0, np.nan],
    [0.7, 1.1, 0.9, 1.5],
    [2.2, np.nan, 1.8, 2.0],
])

mean = np.nanmean(factor, axis=1, keepdims=True)
std = np.nanstd(factor, axis=1, keepdims=True)

z = (factor - mean) / std

print(mean.shape)  # (3, 1)
print(std.shape)   # (3, 1)
print(z)
```

这个写法有几个关键点：

1. `axis=1` 表示每天在股票横截面上聚合。
2. `nanmean` 和 `nanstd` 忽略缺失值。
3. `keepdims=True` 保证结果是 `(T, 1)`，能正确广播回 `(T, N)`。

## 常见坑

### 1. 把 axis 方向记反

```python
# returns: (T, N)
mean_by_asset = returns.mean(axis=0)
mean_by_day = returns.mean(axis=1)
```

不要只背“0 是行、1 是列”。更稳的理解是：`axis` 指定哪个维度被压缩。`axis=0` 压缩时间维度，剩下资产维度；`axis=1` 压缩资产维度，剩下时间维度。

### 2. 方阵掩盖广播错误

如果 `returns.shape == (3, 3)`，下面的代码不会报错：

```python
daily_mean = returns.mean(axis=1)
wrong = returns - daily_mean
```

但 `daily_mean.shape == (3,)` 会按最后一维广播，容易变成错误方向。应写：

```python
daily_mean = returns.mean(axis=1, keepdims=True)
right = returns - daily_mean
```

### 3. 全是 nan 的切片会产生 nan

```python
x = np.array([
    [np.nan, np.nan],
    [1.0, 2.0],
])

print(np.nanmean(x, axis=1))  # [nan 1.5]
```

忽略缺失值不等于一定能得到有效数值。如果某一天所有资产都缺失，横截面均值仍然是 `nan`，并且 NumPy 会给出 `RuntimeWarning: Mean of empty slice`。策略代码需要决定是跳过这天、填充默认值，还是触发数据质量检查。

### 4. 标准差为 0 会导致除零

```python
factor = np.array([
    [1.0, 1.0, 1.0],
    [0.5, 1.0, 1.5],
])

std = factor.std(axis=1, keepdims=True)
z = (factor - factor.mean(axis=1, keepdims=True)) / std

print(z)
```

第一天所有因子值相同，标准差为 0，会产生 `nan`，并且 NumPy 会给出除零相关的 `RuntimeWarning`。实际代码里常见处理是先检查标准差：

```python
std_safe = np.where(std == 0, np.nan, std)
z = (factor - factor.mean(axis=1, keepdims=True)) / std_safe
```

## 实战提示

写聚合代码时，建议在注释里标明 shape：

```python
# factor: (T, N)
# mean: (T, 1), 每天一个横截面均值
# z: (T, N)
mean = np.nanmean(factor, axis=1, keepdims=True)
std = np.nanstd(factor, axis=1, keepdims=True)
z = (factor - mean) / std
```

关键中间结果要加断言：

```python
assert factor.ndim == 2
assert mean.shape == (factor.shape[0], 1)
assert std.shape == (factor.shape[0], 1)
assert z.shape == factor.shape
```

如果你一时不确定 `axis`，用一个小矩阵手算一次。手算比猜测更快，也更可靠。

## 自检问题

1. 对 shape 为 `(T, N)` 的收益矩阵，`mean(axis=0)` 和 `mean(axis=1)` 分别代表什么？
2. 为什么说 `axis` 指定的是“被压缩掉的维度”？
3. `keepdims=True` 对后续广播有什么帮助？
4. `np.mean` 和 `np.nanmean` 在遇到缺失值时有什么不同？
5. 标准化时如果标准差为 0，会发生什么？应该如何处理？
