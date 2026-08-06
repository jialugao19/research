# 08. NumPy：线性代数基础

## 核心概念

量化研究里经常把数据写成向量和矩阵：

- 向量：一组数，例如资产权重、某一天的横截面收益。
- 矩阵：二维数组，例如 `T x N` 的收益率矩阵。
- 线性代数运算：点积、矩阵乘法、转置、解线性方程、特征值分解等。

NumPy 的线性代数主要用两个入口：

- `@`：矩阵乘法或向量点积。
- `np.linalg`：线性代数函数模块。

```python
import numpy as np

x = np.array([1.0, 2.0, 3.0])
y = np.array([0.5, 0.3, 0.2])

print(x @ y)  # 1.7000000000000002
```

这里 `x @ y` 是点积：

```text
1.0 * 0.5 + 2.0 * 0.3 + 3.0 * 0.2 = 1.7
```

## 向量点积：组合收益

如果 `returns` 是某一天所有资产的收益率，`weights` 是组合权重，那么组合收益就是点积。

```python
returns = np.array([0.01, -0.02, 0.03])
weights = np.array([0.5, 0.3, 0.2])

portfolio_return = returns @ weights

print(portfolio_return)  # 0.005
```

计算过程是：

```text
0.01 * 0.5 + (-0.02) * 0.3 + 0.03 * 0.2 = 0.005
```

点积要求两个一维数组长度一致。

```python
bad_weights = np.array([0.5, 0.5])

# returns @ bad_weights
# ValueError: matmul: Input operand 1 has a mismatch in its core dimension
```

## 矩阵乘法：批量组合收益

如果 `returns.shape == (T, N)`，行是日期，列是资产；`weights.shape == (N,)`，那么：

```python
returns = np.array([
    [0.01,  0.02, -0.01],
    [0.03,  0.01,  0.02],
    [-0.02, 0.00,  0.01],
])

weights = np.array([0.5, 0.3, 0.2])

portfolio_returns = returns @ weights

print(portfolio_returns)  # [ 0.009  0.022 -0.008]
print(portfolio_returns.shape)  # (3,)
```

这相当于对每一天做一次组合收益计算。

矩阵乘法的 shape 规则是：

```text
(T, N) @ (N,) -> (T,)
(T, N) @ (N, K) -> (T, K)
```

例如同时计算两个组合：

```python
weights_matrix = np.array([
    [0.5, 0.2],
    [0.3, 0.5],
    [0.2, 0.3],
])

two_portfolios = returns @ weights_matrix

print(two_portfolios)
print(two_portfolios.shape)  # (3, 2)
```

`weights_matrix.shape == (N, K)`，每一列是一组组合权重，结果 `two_portfolios.shape == (T, K)`。

## 转置

转置会交换二维数组的行和列。

```python
x = np.array([
    [1, 2, 3],
    [4, 5, 6],
])

print(x.shape)    # (2, 3)
print(x.T.shape)  # (3, 2)
print(x.T)
```

输出：

```text
[[1 4]
 [2 5]
 [3 6]]
```

转置在计算协方差、Gram 矩阵、线性回归正规方程时很常见。

## 一维数组转置没有效果

```python
x = np.array([1, 2, 3])

print(x.shape)    # (3,)
print(x.T.shape)  # (3,)
```

一维数组既不是行向量，也不是列向量。要明确二维形状，需要 reshape：

```python
row = x.reshape(1, -1)
col = x.reshape(-1, 1)

print(row.shape)  # (1, 3)
print(col.shape)  # (3, 1)
print((row @ col).shape)  # (1, 1)
print((col @ row).shape)  # (3, 3)
```

这也是 NumPy 线性代数里最常见的 shape 坑之一。

## 范数：向量长度和误差大小

`np.linalg.norm` 可以计算向量或矩阵的范数。最常见的是二范数，也就是欧氏长度。

```python
x = np.array([3.0, 4.0])

print(np.linalg.norm(x))  # 5.0
```

在模型评估里，范数常用于描述误差大小：

```python
prediction = np.array([0.10, 0.20, 0.15])
target = np.array([0.12, 0.18, 0.11])

error = prediction - target
rmse_like = np.linalg.norm(error) / np.sqrt(error.size)

print(error)
print(rmse_like)
```

这里 `np.linalg.norm(error)` 是误差向量的整体大小，除以 `sqrt(n)` 后等价于均方根误差。

## 解线性方程：solve

如果有线性方程：

```text
A x = b
```

可以用 `np.linalg.solve(A, b)` 求解 `x`。

```python
A = np.array([
    [3.0, 1.0],
    [1.0, 2.0],
])

b = np.array([9.0, 8.0])

x = np.linalg.solve(A, b)

print(x)  # [2. 3.]
print(A @ x)  # [9. 8.]
```

`solve` 比显式求逆再相乘更稳、更推荐。

不推荐：

```python
# x = np.linalg.inv(A) @ b
```

推荐：

```python
x = np.linalg.solve(A, b)
```

## 逆矩阵：inv

矩阵逆满足：

```text
A @ inv(A) = I
```

其中 `I` 是单位矩阵。

```python
A = np.array([
    [3.0, 1.0],
    [1.0, 2.0],
])

A_inv = np.linalg.inv(A)
I = np.eye(2)

print(A @ A_inv)
print(np.allclose(A @ A_inv, I))  # True
```

逆矩阵在数学推导里常出现，但数值计算中不要随手求逆。实际求解线性方程时，优先使用 `solve`。

## 奇异矩阵和条件数

有些矩阵不可逆，称为奇异矩阵。

```python
A = np.array([
    [1.0, 2.0],
    [2.0, 4.0],
])

# np.linalg.inv(A)
# LinAlgError: Singular matrix
```

第二行正好是第一行的 2 倍，矩阵没有足够独立的信息。

即使矩阵可逆，也可能非常接近奇异。可以用条件数 `np.linalg.cond` 粗略判断数值稳定性：

```python
A = np.array([
    [1.0, 1.0],
    [1.0, 1.000001],
])

print(np.linalg.cond(A))
```

条件数越大，线性方程求解对输入误差越敏感。回归、协方差矩阵求逆、组合优化里都要警惕这个问题。

## 协方差矩阵

协方差矩阵描述多个变量之间如何一起变化。假设 `returns.shape == (T, N)`，行是日期，列是资产，可以用：

```python
returns = np.array([
    [0.01,  0.02, -0.01],
    [0.03,  0.01,  0.02],
    [-0.02, 0.00,  0.01],
    [0.00, -0.01,  0.03],
])

cov = np.cov(returns, rowvar=False)

print(cov)
print(cov.shape)  # (3, 3)
```

`rowvar=False` 表示每一列是一个变量，也就是每只资产一个收益序列。这和常见的 `returns.shape == (T, N)` 约定一致。

组合方差可以写成：

```python
weights = np.array([0.5, 0.3, 0.2])

portfolio_var = weights @ cov @ weights
portfolio_vol = np.sqrt(portfolio_var)

print(portfolio_var)
print(portfolio_vol)
```

这个公式是投资组合理论的基础。后面概率统计和投资组合理论章节会展开风险、协方差收缩和均值-方差优化。

## 特征值和特征向量

特征值分解用于理解矩阵的主要方向。对称矩阵，例如协方差矩阵，常用 `np.linalg.eigh`：

```python
eigvals, eigvecs = np.linalg.eigh(cov)

print(eigvals)
print(eigvecs.shape)  # (3, 3)
```

`eigh` 适合对称矩阵或 Hermitian 矩阵。协方差矩阵是对称矩阵，因此优先使用 `eigh`，而不是更通用的 `eig`。

特征值越大，表示对应方向上的方差越大。PCA 会在后续概率统计章节更系统地展开。

## 最小二乘：lstsq

如果方程数量多于未知数，通常没有精确解，可以用最小二乘找近似解。

```python
X = np.array([
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 3.0],
])

y = np.array([2.0, 2.9, 4.1])

beta, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)

print(beta)
print(residuals)
print(rank)
```

这里 `X` 第一列是截距项，第二列是自变量。`lstsq` 返回的 `beta` 是最小二乘估计。OLS 会在概率统计章节单独讲推导和统计含义。

## 常见坑

### 1. 把 `*` 当成矩阵乘法

```python
A = np.array([
    [1, 2],
    [3, 4],
])
B = np.array([
    [10, 20],
    [30, 40],
])

print(A * B)
print(A @ B)
```

`*` 是逐元素乘法，`@` 才是矩阵乘法。两者含义完全不同。

### 2. 一维数组转置不改变 shape

```python
x = np.array([1, 2, 3])
print(x.T.shape)  # (3,)
```

如果需要列向量，写：

```python
x_col = x.reshape(-1, 1)
```

### 3. 不必要地显式求逆

```python
# 不推荐
x = np.linalg.inv(A) @ b

# 推荐
x = np.linalg.solve(A, b)
```

`solve` 通常更稳定，也更直接表达“解线性方程”。

### 4. 忘记 `rowvar=False`

```python
cov_wrong = np.cov(returns)
cov_right = np.cov(returns, rowvar=False)
```

如果 `returns.shape == (T, N)`，默认 `np.cov(returns)` 会把每一行当作变量，这通常不是你想要的资产协方差矩阵。应使用 `rowvar=False`。

### 5. 忽略病态矩阵

矩阵可逆不代表数值稳定。条件数很大的矩阵会放大输入误差。协方差矩阵求逆、回归和组合优化里，病态矩阵经常导致结果极端不稳定。

## 实战提示

写线性代数代码时，先检查 shape：

```python
# returns: (T, N)
# weights: (N,)
# portfolio_returns: (T,)
assert returns.ndim == 2
assert weights.ndim == 1
assert returns.shape[1] == weights.shape[0]

portfolio_returns = returns @ weights
```

对于协方差矩阵：

```python
cov = np.cov(returns, rowvar=False)

assert cov.shape == (returns.shape[1], returns.shape[1])
assert np.allclose(cov, cov.T)
```

对于线性方程：

```python
assert A.ndim == 2
assert A.shape[0] == A.shape[1]
assert b.shape[0] == A.shape[0]

x = np.linalg.solve(A, b)
```

这些断言能在早期暴露 shape 错误，比等到模型结果异常再排查更省时间。

## 自检问题

1. `*` 和 `@` 在 NumPy 里分别表示什么？
2. 如果 `returns.shape == (T, N)`，`weights.shape == (N,)`，`returns @ weights` 的结果 shape 是什么？
3. 为什么一维数组 `x.T` 不会变成列向量？
4. 解 `A x = b` 时，为什么通常推荐 `np.linalg.solve(A, b)`，而不是 `np.linalg.inv(A) @ b`？
5. 计算资产协方差矩阵时，为什么常写 `np.cov(returns, rowvar=False)`？

