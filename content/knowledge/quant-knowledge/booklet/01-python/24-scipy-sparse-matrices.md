# scipy.sparse：稀疏矩阵格式与基本运算

## 核心概念

稀疏矩阵适合存储“大部分元素为 0”的矩阵。它不会保存所有元素，而是只保存非零值和它们的位置。

常见场景包括：

- 文本特征矩阵：样本很多，词表很大，但每篇文档只出现少量词。
- 图的邻接矩阵：节点很多，但边远少于 `n * n`。
- 大规模线性方程：网格、约束、网络结构产生的矩阵通常很稀疏。
- one-hot 编码：每行只有少数几个 1。

本节使用 `scipy.sparse` 的稀疏矩阵接口，例如 `csr_matrix`。SciPy 也有较新的 sparse array API，但为了兼容常见生态，本节例子统一使用 sparse matrix，并用 `@` 表示矩阵乘法。

## 准备环境

```python
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.sparse import linalg as spla
```

稀疏矩阵和 NumPy 数组不是同一种对象。它们有相似的数学含义，但存储方式和部分 API 不同。

## 从 dense 转成 sparse

先看一个普通 NumPy 矩阵：

```python
dense = np.array([
    [0.0, 0.0, 3.0],
    [4.0, 0.0, 0.0],
    [0.0, 5.0, 0.0],
])

A_csr = sparse.csr_matrix(dense)

print(A_csr)
print(A_csr.shape)
print(A_csr.nnz)
print(A_csr.toarray())
```

`nnz` 是 non-zero 的缩写，表示存储的非零元素个数。

```python
density = A_csr.nnz / (A_csr.shape[0] * A_csr.shape[1])

print(density)
```

密度越低，稀疏存储越可能有优势。反过来，如果矩阵大部分元素都非零，稀疏格式可能反而更慢。

## CSR 内部存储

CSR 是 compressed sparse row 的缩写，按行压缩存储。

```python
print(A_csr.data)
print(A_csr.indices)
print(A_csr.indptr)
```

三个数组的含义是：

- `data`：非零值。
- `indices`：每个非零值所在的列号。
- `indptr`：每一行在 `data` 和 `indices` 里的起止位置。

CSR 适合：

- 快速矩阵向量乘法。
- 快速按行切片。
- 快速遍历每一行的非零元素。

```python
row_1 = A_csr[1]

print(row_1)
print(row_1.toarray())
```

按列频繁切片时，CSC 通常更合适。

## 常见格式

SciPy 稀疏矩阵有多种格式。常见选择：

- `coo_matrix`：用 `(row, col, data)` 三元组构造，适合从边表或坐标数据创建。
- `csr_matrix`：按行压缩，适合行切片和矩阵向量乘法。
- `csc_matrix`：按列压缩，适合列切片和某些线性代数分解。
- `lil_matrix`：适合逐步构造和修改，计算前通常转 CSR。
- `dok_matrix`：字典形式，适合零散赋值。
- `dia_matrix`：对角线形式，适合带状矩阵。

实战中最常见的模式是：

```text
构造阶段用 COO / LIL / DOK，计算阶段转 CSR / CSC
```

## COO：用坐标构造

COO 格式用三组数组表示非零元素的位置和值。

```python
row = np.array([0, 0, 1, 2])
col = np.array([1, 1, 2, 0])
data = np.array([1.0, 2.0, 3.0, 4.0])

A_coo = sparse.coo_matrix((data, (row, col)), shape=(3, 3))

print(A_coo)
print(A_coo.toarray())
```

注意 `(0, 1)` 这个位置出现了两次。COO 允许重复坐标，转换成 CSR 时会把重复项相加。

```python
A_from_coo = A_coo.tocsr()

print(A_from_coo.toarray())
print(A_from_coo[0, 1])
```

这个特性在从边表构造图邻接矩阵时很有用，但也可能掩盖重复数据问题。是否应该相加，要由业务语义决定。

## LIL：逐步构造

如果需要逐个位置赋值，可以先用 LIL。

```python
A_lil = sparse.lil_matrix((4, 4), dtype=float)

A_lil[0, 1] = 2.0
A_lil[1, 2] = 3.0
A_lil[2, 3] = 4.0
A_lil[3, 0] = 5.0

print(A_lil)

A_lil_csr = A_lil.tocsr()

print(A_lil_csr.toarray())
```

LIL 适合构造，不适合大量矩阵运算。构造完成后应转成 CSR 或 CSC。

## 对角矩阵和带状矩阵

`sparse.diags` 可以高效构造对角线矩阵。

```python
n = 5
main = 2.0 * np.ones(n)
off = -1.0 * np.ones(n - 1)

K = sparse.diags(
    diagonals=[off, main, off],
    offsets=[-1, 0, 1],
    format="csr",
)

print(K.toarray())
print(K.nnz)
```

这种三对角矩阵在离散化、平滑惩罚、图拉普拉斯等问题中很常见。

单位矩阵可以用：

```python
I = sparse.eye(n, format="csr")

print(I.toarray())
```

不要为了构造大单位矩阵而先创建 dense 的 `np.eye(n)` 再转 sparse。

## 基本运算

稀疏矩阵可以和 NumPy 向量做矩阵乘法。

```python
x = np.arange(1.0, n + 1.0)

y = K @ x

print(x)
print(y)
```

矩阵和矩阵也可以相乘：

```python
K2 = K @ K

print(type(K2))
print(K2.nnz)
print(K2.toarray())
```

逐元素乘法使用 `.multiply`，不要和矩阵乘法混淆。

```python
elementwise_square = K.multiply(K)

print(elementwise_square.toarray())
```

加法会保留稀疏结构：

```python
shifted = K + 0.1 * I

print(shifted.toarray())
```

但给所有元素加一个非零标量会使零元素也变成非零，通常不适合稀疏表示。

```python
# 不推荐，也通常不被 sparse matrix 支持：
# K + 1.0
```

## 聚合返回值

稀疏矩阵的聚合结果有时不是一维数组，而是矩阵形状的结果。可以显式转成数组。

```python
row_sum = np.asarray(K.sum(axis=1)).ravel()
col_sum = np.asarray(K.sum(axis=0)).ravel()

print(row_sum)
print(col_sum)
```

`.ravel()` 把结果压平成一维，便于放进 pandas。

```python
row_sum_s = pd.Series(row_sum, name="row_sum")

print(row_sum_s)
```

## CSR 和 CSC 的切片

CSR 适合行切片：

```python
first_two_rows = K[:2, :]

print(type(first_two_rows))
print(first_two_rows.toarray())
```

CSC 适合列切片：

```python
K_csc = K.tocsc()
first_two_cols = K_csc[:, :2]

print(type(first_two_cols))
print(first_two_cols.toarray())
```

格式转换本身有成本，不要在循环里反复 `tocsr()`、`tocsc()`。通常应根据主要访问模式提前选好格式。

## vstack 和 hstack

稀疏矩阵可以按行或按列拼接。

```python
top = sparse.csr_matrix([[1.0, 0.0, 2.0]])
bottom = sparse.csr_matrix([[0.0, 3.0, 0.0]])

stacked_rows = sparse.vstack([top, bottom], format="csr")

print(stacked_rows.toarray())
```

按列拼接：

```python
left = sparse.csr_matrix([[1.0], [0.0]])
right = sparse.csr_matrix([[0.0, 2.0], [3.0, 0.0]])

stacked_cols = sparse.hstack([left, right], format="csr")

print(stacked_cols.toarray())
```

这在拼接特征矩阵时很常见，例如把多个 one-hot 块合在一起。

## 稀疏线性方程：spsolve

对于稀疏线性方程：

```text
K x = b
```

可以使用 `scipy.sparse.linalg.spsolve`。

```python
b = np.ones(n)

x_direct = spla.spsolve(K, b)

print(x_direct)
print(K @ x_direct)
```

`spsolve` 适合中等规模稀疏直接求解。它会使用稀疏矩阵结构，而不是先把矩阵转成 dense。

不要这样做：

```python
# 不推荐：可能直接耗尽内存
# x_bad = np.linalg.solve(K.toarray(), b)
```

## 迭代求解：cg

对于对称正定稀疏矩阵，可以使用共轭梯度法 `cg`。

```python
x_cg, info = spla.cg(K, b, rtol=1e-12, atol=0.0)

print(x_cg)
print(info)
print(np.linalg.norm(K @ x_cg - b))
```

`info == 0` 表示成功收敛。非零值表示没有在指定条件内收敛，或输入有问题。

迭代法通常适合更大规模的问题，但要关注收敛容忍度、预条件和矩阵性质。本节先掌握接口和结果检查。

## 图邻接矩阵例子

边表可以自然转成稀疏邻接矩阵。

```python
edges = pd.DataFrame({
    "src": [0, 0, 1, 2, 2],
    "dst": [1, 2, 2, 0, 3],
    "weight": [1.0, 0.5, 2.0, 0.5, 1.5],
})

n_nodes = 4

adj = sparse.coo_matrix(
    (edges["weight"].to_numpy(), (edges["src"].to_numpy(), edges["dst"].to_numpy())),
    shape=(n_nodes, n_nodes),
).tocsr()

print(adj.toarray())
```

出度或出边权重和可以用按行求和：

```python
out_weight = np.asarray(adj.sum(axis=1)).ravel()

out_weight_s = pd.Series(out_weight, name="out_weight")

print(out_weight_s)
```

如果图是无向图，通常要把邻接矩阵对称化：

```python
undirected_adj = adj + adj.T

print(undirected_adj.toarray())
```

如果双向边可能重复，要确认权重相加是否符合业务语义。

## 显式零和 eliminate_zeros

稀疏矩阵可能存储显式的 0。

```python
Z = sparse.csr_matrix(
    (
        np.array([1.0, 0.0, 2.0]),
        np.array([0, 1, 2]),
        np.array([0, 3]),
    ),
    shape=(1, 3),
)

print(Z.nnz)
print(Z.toarray())

Z.eliminate_zeros()

print(Z.nnz)
print(Z.toarray())
```

`nnz` 统计的是存储的元素个数，不一定等于数学上非零的个数。清理显式零可以节省空间，并减少后续计算负担。

## 内存直觉

稀疏矩阵省不省内存，取决于非零比例和索引开销。

```python
dense_bytes = dense.nbytes
sparse_bytes = (
    A_csr.data.nbytes
    + A_csr.indices.nbytes
    + A_csr.indptr.nbytes
)

print(dense_bytes)
print(sparse_bytes)
```

对很小的矩阵，稀疏格式未必省内存，因为索引数组也要占空间。稀疏格式的价值通常出现在大矩阵、低密度、可利用结构的场景。

## 常见坑

第一，随手 `.toarray()`。

```python
# 小矩阵调试可以
print(K.toarray())

# 大矩阵生产计算中要谨慎
```

如果矩阵形状是 `1_000_000 x 1_000_000`，即使只有很少非零元素，转 dense 也会试图创建巨大的数组。

第二，把逐元素乘法和矩阵乘法混淆。

```python
matmul_result = K @ x
elementwise_result = K.multiply(K)
```

本节统一用 `@` 做矩阵乘法，用 `.multiply` 做逐元素乘法。

第三，构造阶段选错格式。

如果要逐个元素赋值，用 LIL 或 DOK 更合适；如果已经有坐标数组，用 COO 更直接；计算阶段再转 CSR 或 CSC。

第四，忽略重复坐标。

COO 转 CSR 时会把重复坐标相加。这个行为可能正是你想要的，也可能掩盖重复数据。

第五，认为所有 NumPy 函数都能无缝处理稀疏矩阵。

很多 NumPy 函数会把输入转 dense，或返回意外类型。稀疏矩阵运算优先使用 `scipy.sparse` 和 `scipy.sparse.linalg` 的接口。

## 实战提示

稀疏矩阵进入计算前，可以做这些检查：

```python
assert sparse.issparse(K)
assert K.ndim == 2
assert K.shape[0] == K.shape[1]
assert np.isfinite(K.data).all()

density = K.nnz / (K.shape[0] * K.shape[1])
print(density)
```

线性求解后检查残差：

```python
x = spla.spsolve(K, b)
residual_norm = np.linalg.norm(K @ x - b)

print(residual_norm)
```

如果要和 pandas 配合，仍然保存标签：

```python
index = pd.Index([f"node_{i}" for i in range(n_nodes)], name="node")

out_weight = np.asarray(adj.sum(axis=1)).ravel()
out_weight = pd.Series(out_weight, index=index, name="out_weight")

print(out_weight)
```

SciPy 稀疏矩阵负责存储和计算，pandas 负责标签语义。

## 小结

`scipy.sparse` 的核心是用合适格式表达稀疏结构：

- COO 适合从坐标或边表构造。
- LIL/DOK 适合逐步赋值。
- CSR 适合行切片和矩阵向量乘法。
- CSC 适合列切片和某些列导向算法。
- `diags` 和 `eye` 适合构造结构化稀疏矩阵。
- `spsolve` 和 `cg` 可以直接在稀疏矩阵上解线性方程。

稀疏矩阵的关键不是“看起来有很多 0”，而是避免把大矩阵不必要地 densify，并利用正确格式做计算。

## 自检问题

1. CSR、CSC、COO 分别适合什么场景？
2. 为什么不要在大稀疏矩阵上随手 `.toarray()`？
3. COO 中重复坐标转换成 CSR 时会发生什么？
4. 稀疏矩阵里矩阵乘法和逐元素乘法分别应怎么写？
5. `spsolve` 和 `cg` 的使用场景有什么不同？
