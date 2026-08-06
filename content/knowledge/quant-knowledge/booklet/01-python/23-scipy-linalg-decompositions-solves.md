# 23. scipy.linalg：矩阵分解与线性方程

## 核心概念

`scipy.linalg` 是 SciPy 的密集矩阵线性代数模块。它和 `numpy.linalg` 很像，但提供了更多专业接口，例如：

- `solve`：解线性方程组。
- `lu_factor` / `lu_solve`：LU 分解与重复求解。
- `cho_factor` / `cho_solve`：Cholesky 分解与正定矩阵求解。
- `qr`：QR 分解，常用于最小二乘。
- `svd`：奇异值分解，常用于秩、降维、伪逆和数值诊断。
- `eig` / `eigh`：特征值分解，`eigh` 专门处理对称或 Hermitian 矩阵。

核心原则：数值计算中优先“解方程”，不要为了求解而显式求逆。

## 准备环境

```python
import numpy as np
import pandas as pd
from scipy import linalg
```

本节只讨论普通密集矩阵。如果矩阵很大且大部分元素为 0，应使用下一节的 `scipy.sparse`。

## 解线性方程：solve

线性方程组：

```text
A x = b
```

可以用 `linalg.solve` 直接求 `x`。

```python
A = np.array([
    [3.0, 1.0],
    [1.0, 2.0],
])
b = np.array([9.0, 8.0])

x = linalg.solve(A, b)

print(x)
print(A @ x)
```

结果是 `[2, 3]`，因为：

```text
3 * 2 + 1 * 3 = 9
1 * 2 + 2 * 3 = 8
```

求解后应检查残差：

```python
residual = A @ x - b

print(residual)
print(linalg.norm(residual))
```

残差越接近 0，说明数值解越符合原方程。

## 不要为了求解而求逆

数学上可以写：

```text
x = A^{-1} b
```

但代码里通常不要这样写：

```python
x_by_inverse = linalg.inv(A) @ b

print(x_by_inverse)
```

更推荐：

```python
x_by_solve = linalg.solve(A, b)

print(x_by_solve)
```

原因是 `solve` 更直接表达问题，也通常更稳定、更高效。显式求逆会多做工作，还可能放大数值误差。

## 多个右端项

如果要解：

```text
A X = B
```

其中 `B` 有多列，可以一次传入二维数组。

```python
B = np.array([
    [9.0, 1.0],
    [8.0, 0.0],
])

X = linalg.solve(A, B)

print(X)
print(A @ X)
```

`X` 的每一列对应 `B` 的一列右端项。不要手写 Python 循环逐列求解，除非有特殊原因。

## 矩阵条件数

条件数衡量矩阵求解对输入误差的敏感程度。

```python
well_conditioned = np.array([
    [3.0, 1.0],
    [1.0, 2.0],
])

ill_conditioned = np.array([
    [1.0, 1.0],
    [1.0, 1.000001],
])

print(np.linalg.cond(well_conditioned))
print(np.linalg.cond(ill_conditioned))
```

条件数越大，问题越不稳定。协方差矩阵求逆、回归、组合优化里尤其要关注这个指标。

小的输入扰动在病态矩阵上可能被放大：

```python
b1 = np.array([2.0, 2.000001])
b2 = np.array([2.0, 2.000002])

x1 = linalg.solve(ill_conditioned, b1)
x2 = linalg.solve(ill_conditioned, b2)

print(x1)
print(x2)
print(x2 - x1)
```

这不是 SciPy 的问题，而是线性方程本身对误差敏感。

## LU 分解：重复求解

如果同一个矩阵 `A` 要配多个 `b`，可以先做 LU 分解，再重复求解。

```python
lu, piv = linalg.lu_factor(A)

x_lu = linalg.lu_solve((lu, piv), b)
X_lu = linalg.lu_solve((lu, piv), B)

print(x_lu)
print(X_lu)
```

`lu_factor` 把矩阵分解并保存主元信息，`lu_solve` 用这个分解结果解方程。这样避免重复分解同一个 `A`。

当右端项很多时，这种写法比每次都调用 `solve(A, b_i)` 更清楚，也更高效。

## Cholesky 分解：对称正定矩阵

如果矩阵是对称正定的，可以使用 Cholesky 分解。协方差矩阵通常应该是半正定或正定，组合优化中经常会遇到。

```python
cov = np.array([
    [0.0400, 0.0060, 0.0040],
    [0.0060, 0.0225, 0.0030],
    [0.0040, 0.0030, 0.0100],
])

print(np.allclose(cov, cov.T))
print(np.linalg.eigvalsh(cov))
```

如果特征值都大于 0，矩阵是正定的，可以做 Cholesky：

```python
c_factor, lower = linalg.cho_factor(cov, lower=True)

ones = np.ones(cov.shape[0])
inv_cov_ones = linalg.cho_solve((c_factor, lower), ones)

weights = inv_cov_ones / (ones @ inv_cov_ones)

print(weights)
print(weights.sum())
```

这里没有显式计算 `inv(cov)`，而是通过解：

```text
cov * y = 1
```

得到 `y = cov^{-1} 1`。最小方差组合权重与这个向量成比例。

把结果包回 pandas 会更清楚：

```python
assets = pd.Index(["AAA", "BBB", "CCC"], name="asset")
weights_s = pd.Series(weights, index=assets, name="min_var_weight")

print(weights_s)
```

## 正定假设不满足时

Cholesky 要求矩阵正定。如果矩阵不是正定，会报错。

```python
not_positive_definite = np.array([
    [1.0, 2.0],
    [2.0, 1.0],
])

print(np.linalg.eigvalsh(not_positive_definite))

# 这行会报错：矩阵不是正定
# linalg.cho_factor(not_positive_definite)
```

不要在 Cholesky 报错后盲目加很大的对角线修正。应先理解矩阵为什么不正定：样本太少、特征共线、估计噪声，还是数据错误。

小的对角线 jitter 有时用于数值稳定：

```python
jitter = 1e-6
regularized_cov = cov + jitter * np.eye(cov.shape[0])

print(np.linalg.eigvalsh(regularized_cov))
```

但 jitter 是建模选择，不是无成本修复。

## QR 分解：最小二乘

线性回归可以写成最小二乘问题：

```text
minimize ||X beta - y||^2
```

如果 `X` 是满列秩，可以用 QR 分解求解。

```python
X_data = np.array([
    [1.0, 0.0],
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 3.0],
])
y = np.array([1.0, 2.0, 2.9, 4.1])

Q, R = linalg.qr(X_data, mode="economic")

beta_qr = linalg.solve_triangular(R, Q.T @ y)

print(beta_qr)
print(X_data @ beta_qr)
```

`mode="economic"` 返回较小的 `Q` 和 `R`，适合样本数大于特征数的场景。

也可以直接用 `linalg.lstsq`：

```python
beta_lstsq, residuals, rank, singular_values = linalg.lstsq(X_data, y)

print(beta_lstsq)
print(residuals)
print(rank)
print(singular_values)
```

`lstsq` 更直接，QR 分解帮助你理解它背后的线性代数结构。

## SVD：奇异值分解

SVD 把矩阵分解为：

```text
A = U S V^T
```

在 SciPy 中：

```python
M = np.array([
    [3.0, 1.0],
    [1.0, 3.0],
    [1.0, 1.0],
])

U, s, Vt = linalg.svd(M, full_matrices=False)

reconstructed = U @ np.diag(s) @ Vt

print(s)
print(np.allclose(M, reconstructed))
```

奇异值可以用来判断矩阵秩和数值稳定性。

```python
rank = np.sum(s > 1e-12)
condition_from_svd = s.max() / s.min()

print(rank)
print(condition_from_svd)
```

如果最小奇异值接近 0，矩阵接近低秩，求逆或求解会更不稳定。

## 低秩近似

SVD 还可以做低秩近似。只保留最大的一个奇异值：

```python
k = 1
M_rank1 = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]

print(M_rank1)
print(linalg.norm(M - M_rank1))
```

这类思想会出现在 PCA、矩阵压缩和因子模型中。本节只关注接口和矩阵形状。

## 特征值分解：eig 和 eigh

一般矩阵可以用 `eig`：

```python
G = np.array([
    [0.9, 0.2],
    [0.1, 0.8],
])

eigvals, eigvecs = linalg.eig(G)

print(eigvals)
print(eigvecs)
```

如果矩阵是对称矩阵，应优先使用 `eigh`：

```python
eigvals_sym, eigvecs_sym = linalg.eigh(cov)

print(eigvals_sym)
print(eigvecs_sym)
print(eigvecs_sym.T @ eigvecs_sym)
```

`eigh` 利用对称结构，结果通常是实数，数值性质也更适合协方差矩阵、相关矩阵这类对象。

重构对称矩阵：

```python
cov_reconstructed = eigvecs_sym @ np.diag(eigvals_sym) @ eigvecs_sym.T

print(np.allclose(cov, cov_reconstructed))
```

## 白化和协方差矩阵直觉

特征值分解可以帮助理解协方差矩阵。对称正定矩阵可以写成：

```text
cov = Q Lambda Q^T
```

其中 `Lambda` 是特征值对角矩阵。协方差矩阵的逆平方根可以写成：

```python
eps = 1e-12
inv_sqrt_cov = eigvecs_sym @ np.diag(1.0 / np.sqrt(eigvals_sym + eps)) @ eigvecs_sym.T

identity_like = inv_sqrt_cov @ cov @ inv_sqrt_cov

print(identity_like)
```

如果数值稳定，结果会接近单位矩阵。这是白化、风险模型和 PCA 里常见的线性代数思想。

## 常见坑

第一，为了解方程而显式求逆。

```python
# 不推荐
# x = linalg.inv(A) @ b

# 推荐
x = linalg.solve(A, b)
```

第二，不检查残差。

```python
residual_norm = linalg.norm(A @ x - b)

print(residual_norm)
```

求解成功不代表误差可以忽略，尤其是病态矩阵。

第三，对非正定矩阵使用 Cholesky。

Cholesky 是给对称正定矩阵用的。协方差矩阵如果有负特征值，应先查估计过程和数据质量。

第四，把 `eig` 用在本该使用 `eigh` 的对称矩阵上。

对称矩阵优先用 `eigh`，这能更好地利用数学结构。

第五，忽略矩阵形状和 dtype。

```python
assert A.ndim == 2
assert b.ndim == 1
assert A.shape[0] == A.shape[1]
assert A.shape[0] == b.shape[0]
assert np.issubdtype(A.dtype, np.floating)
```

线性代数错误很多时候来自形状、标签或 dtype，而不是算法本身。

## 实战提示

使用 `scipy.linalg` 前，先做这组检查：

```python
assert np.isfinite(A).all()
assert np.isfinite(b).all()
assert A.shape[0] == A.shape[1]
assert A.shape[0] == b.shape[0]

cond_A = np.linalg.cond(A)
print(cond_A)
```

求解后检查：

```python
x = linalg.solve(A, b)
residual = A @ x - b

assert linalg.norm(residual) < 1e-10
```

对协方差矩阵，额外检查：

```python
assert np.allclose(cov, cov.T)
eigvals = np.linalg.eigvalsh(cov)
print(eigvals)
```

如果要在 pandas 表格和 SciPy 矩阵之间转换，仍然要保存标签：

```python
cov_df = pd.DataFrame(cov, index=assets, columns=assets)

cov_arr = cov_df.to_numpy(dtype=float)
weights_arr = linalg.solve(cov_arr, np.ones(len(assets)))
weights_arr = weights_arr / weights_arr.sum()

weights = pd.Series(weights_arr, index=cov_df.index, name="weight")

print(weights)
```

SciPy 负责数值计算，pandas 负责标签语义。

## 小结

`scipy.linalg` 是密集矩阵线性代数的常用工具箱：

- 用 `solve` 解线性方程，不要为了求解而显式求逆。
- 同一个矩阵重复求解时，用 LU 或 Cholesky 分解复用计算。
- 对称正定矩阵优先考虑 Cholesky。
- 最小二乘可用 QR 分解或 `lstsq`。
- SVD 用于秩、条件数、低秩近似和数值诊断。
- 对称矩阵特征分解优先用 `eigh`。

线性代数代码的可信度来自三件事：形状正确、分解假设正确、残差和条件数检查通过。

## 自检问题

1. 为什么数值计算中不推荐为了求解 `Ax=b` 而显式计算 `A^{-1}`？
2. LU 分解和 Cholesky 分解分别适合什么场景？
3. 为什么协方差矩阵通常应使用 `eigh` 而不是普通 `eig`？
4. 条件数大说明什么问题？
5. SVD 的奇异值可以用来诊断哪些线性代数问题？
