# 03. NumPy：broadcasting

## 核心概念

`broadcasting` 是 NumPy 在不同 shape 的数组之间做逐元素运算时使用的自动扩展规则。它让你不用手动复制数组，也能写出简洁的向量化代码。

广播的核心规则是：从最后一个维度开始对齐，两个维度可以一起运算，当且仅当它们满足下面任意一个条件：

- 两个维度长度相同。
- 其中一个维度长度是 1。
- 其中一个数组没有这个维度。

如果某一维无法匹配，就会报错。

```python
import numpy as np

a = np.array([1, 2, 3])

print(a + 10)  # [11 12 13]
```

这里标量 `10` 会广播到 `a` 的每个元素上。

## 一维数组与二维数组

考虑一个二维数组：

```python
m = np.array([
    [1, 2, 3],
    [4, 5, 6],
])

v = np.array([10, 20, 30])

print(m.shape)  # (2, 3)
print(v.shape)  # (3,)
print(m + v)
```

输出：

```text
[[11 22 33]
 [14 25 36]]
```

`m.shape == (2, 3)`，`v.shape == (3,)`。从最后一维对齐时，`3` 和 `3` 匹配，缺失的前一维会被看成可以扩展，所以 `v` 被广播到每一行。

等价理解是：

```python
v_broadcasted = np.array([
    [10, 20, 30],
    [10, 20, 30],
])

print(m + v_broadcasted)
```

NumPy 不会真的先复制出完整的 `v_broadcasted`，而是在底层按广播规则计算。

## 行向量与列向量

广播里最容易出错的是 `(n,)`、`(1, n)`、`(n, 1)` 的区别。

```python
x = np.array([1, 2, 3])

row = x.reshape(1, -1)
col = x.reshape(-1, 1)

print(x.shape)    # (3,)
print(row.shape)  # (1, 3)
print(col.shape)  # (3, 1)
```

`row` 和 `col` 的广播结果不同：

```python
print(row + col)
```

输出：

```text
[[2 3 4]
 [3 4 5]
 [4 5 6]]
```

这里 `(1, 3)` 和 `(3, 1)` 广播成 `(3, 3)`。这常用于构造两两组合矩阵，比如两两距离、两两价差、两两相关性前的数据准备。

## 不能广播的例子

```python
a = np.ones((2, 3))
b = np.ones((2,))

# a + b
# ValueError: operands could not be broadcast together with shapes (2,3) (2,)
```

从最后一维开始对齐：

```text
a: (2, 3)
b:    (2,)
```

最后一维是 `3` 和 `2`，既不相等，也没有一个是 `1`，所以不能广播。

如果你想按行加上两个数，应把 `b` 变成列向量：

```python
b_col = b.reshape(-1, 1)

print((a + b_col).shape)  # (2, 3)
```

## 实战例子：横截面去均值

假设 `returns` 是一个 `T x N` 的收益率矩阵，行是日期，列是股票。你想每天做横截面去均值，也就是每一天减去当天所有股票的平均收益。

```python
import numpy as np

returns = np.array([
    [0.01,  0.02, -0.01],
    [0.03,  0.01,  0.02],
    [-0.02, 0.00,  0.01],
])

daily_mean = returns.mean(axis=1, keepdims=True)
demeaned = returns - daily_mean

print(daily_mean)
print(demeaned)
```

输出：

```text
[[0.00666667]
 [0.02      ]
 [-0.00333333]]
[[ 0.00333333  0.01333333 -0.01666667]
 [ 0.01       -0.01        0.        ]
 [-0.01666667  0.00333333  0.01333333]]
```

这里 `daily_mean.shape == (3, 1)`，可以和 `returns.shape == (3, 3)` 广播。每一行减去自己的均值。

`keepdims=True` 很重要。它让聚合结果保留二维形状，减少广播方向写错的风险。

## 实战例子：按股票做时间序列标准化

如果你想对每只股票沿时间维度标准化，可以对每一列减去自己的时间均值，再除以自己的时间标准差。

```python
returns = np.array([
    [0.01,  0.02, -0.01],
    [0.03,  0.01,  0.02],
    [-0.02, 0.00,  0.01],
])

mean_by_asset = returns.mean(axis=0, keepdims=True)
std_by_asset = returns.std(axis=0, keepdims=True)

z = (returns - mean_by_asset) / std_by_asset

print(mean_by_asset.shape)  # (1, 3)
print(std_by_asset.shape)   # (1, 3)
print(z)
```

`mean_by_asset` 和 `std_by_asset` 的 shape 都是 `(1, 3)`，会按列广播到所有日期。

这类操作在因子研究里非常常见：

- 横截面标准化：同一天不同股票之间标准化，通常沿 `axis=1` 聚合。
- 时间序列标准化：同一只股票不同日期之间标准化，通常沿 `axis=0` 聚合。

## 实战例子：手续费和滑点

假设你有一个 `T x N` 的换手矩阵，每个元素表示某天某股票的换手金额比例。每只股票的交易成本不同，可以用一维数组按列广播。

```python
turnover = np.array([
    [0.10, 0.00, 0.05],
    [0.20, 0.10, 0.00],
])

cost_rate = np.array([0.001, 0.002, 0.0015])

cost = turnover * cost_rate

print(cost)
```

输出：

```text
[[1.0e-04 0.0e+00 7.5e-05]
 [2.0e-04 2.0e-04 0.0e+00]]
```

`turnover.shape == (2, 3)`，`cost_rate.shape == (3,)`，所以 `cost_rate` 会按列广播。

## 常见坑

### 1. 忘记 keepdims 导致方向错

```python
returns = np.array([
    [0.01,  0.02, -0.01],
    [0.03,  0.01,  0.02],
    [-0.02, 0.00,  0.01],
])

daily_mean = returns.mean(axis=1)

print(daily_mean.shape)  # (3,)
```

如果 `returns` 刚好是方阵，`returns - daily_mean` 不会报错，但广播方向可能不是你想要的：

```python
wrong = returns - daily_mean
right = returns - returns.mean(axis=1, keepdims=True)

print(wrong)
print(right)
```

`daily_mean.shape == (3,)` 会被当作列方向长度为 3 的行向量，对每一行都减同一个数组，而不是每一行减自己的均值。

为了避免这种静默错误，横截面或时间序列聚合后建议使用 `keepdims=True`。

### 2. `(n,)` 的语义不够明确

```python
x = np.array([1, 2, 3])
m = np.ones((3, 3))

print((m + x).shape)  # (3, 3)
```

`x.shape == (3,)` 默认按最后一维对齐。它更像“按列加到每一行”，而不是“按行加到每一列”。

如果你的意图是按行加，应明确写成列向量：

```python
x_col = x.reshape(-1, 1)
print((m + x_col).shape)  # (3, 3)
```

### 3. 广播不复制输入，但输出仍占内存

广播本身通常不会把小数组复制成大数组，但运算结果仍然会创建完整输出。

```python
a = np.ones((10_000, 1))
b = np.ones((1, 10_000))

# result = a + b  # shape 是 (10000, 10000)，会占用大量内存
```

`a + b` 的输出有一亿个元素。如果是 `float64`，仅结果数组就约 800 MB。广播可以减少输入复制，但不能让巨大输出免费。

### 4. `np.tile` 通常不是必要的

很多广播场景不需要先用 `np.tile` 手动复制。

```python
m = np.ones((2, 3))
v = np.array([10, 20, 30])

print(m + v)
```

没有必要写：

```python
# v2 = np.tile(v, (2, 1))
# print(m + v2)
```

`tile` 会真实复制数据，可能浪费内存。只有在下游 API 明确需要物理展开后的数组时，才考虑使用。

## 实战提示

写广播代码时，建议先把 shape 写出来：

```python
# returns: (T, N)
# daily_mean: (T, 1)
# demeaned: (T, N)
daily_mean = returns.mean(axis=1, keepdims=True)
demeaned = returns - daily_mean
```

对关键路径加断言：

```python
assert returns.ndim == 2
assert daily_mean.shape == (returns.shape[0], 1)
assert demeaned.shape == returns.shape
```

如果你在做因子研究，还应明确每个维度含义：

- `axis=0` 聚合后通常得到每只资产的时间序列统计量。
- `axis=1` 聚合后通常得到每天的横截面统计量。
- 用 `keepdims=True` 保留可广播的二维形状。

## 自检问题

1. NumPy broadcasting 的三个匹配条件是什么？
2. `(2, 3)` 和 `(3,)` 相加时，`(3,)` 是按哪个维度广播？
3. 为什么横截面去均值时推荐 `returns.mean(axis=1, keepdims=True)`？
4. `(3, 1)` 和 `(1, 3)` 相加的结果 shape 是什么？
5. 广播为什么不等于完全没有内存成本？
