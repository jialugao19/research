# 概率统计：PCA 主成分分析的方差分解、特征向量与降维解释

## 核心概念

PCA 是 Principal Component Analysis，主成分分析。

它把一组相关变量转换成一组新的正交变量：

```text
PC1, PC2, PC3, ...
```

这些新变量按解释方差从大到小排列：

- PC1 是方差最大的线性组合。
- PC2 是在与 PC1 正交的条件下，方差第二大的线性组合。
- 后续主成分依次类推。

在统计上，PCA 是对协方差矩阵或相关矩阵做特征值分解。

在数据矩阵 `X` 已经中心化后：

```text
cov = X'X / (n - 1)
cov v_j = lambda_j v_j
```

其中：

- `v_j` 是第 `j` 个主成分方向。
- `lambda_j` 是该方向上的方差。
- `lambda_j / sum(lambda)` 是解释方差比例。

PCA 常用于：

- 降维。
- 去噪。
- 可视化高维数据。
- 理解共同因子。
- 处理共线变量。
- 压缩协方差结构。

## 准备环境

```python
import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
```

准备一组由两个潜在因子驱动的 4 变量数据。可以把它理解为 4 个资产的收益暴露在共同市场因子和风格因子上。

```python
rng = np.random.default_rng(53)
n = 180

market = rng.normal(0.0, 1.0, size=n)
style = rng.normal(0.0, 1.0, size=n)
noise = rng.normal(0.0, 0.25, size=(n, 4))

X = np.column_stack([
    0.90 * market + 0.30 * style,
    0.85 * market + 0.10 * style,
    0.45 * market - 0.85 * style,
    0.35 * market - 0.90 * style,
]) + noise

columns = ["asset_a", "asset_b", "asset_c", "asset_d"]

frame = pd.DataFrame(X, columns=columns)

print(frame.head())
```

这里真实世界中看不到 `market` 和 `style`，PCA 会尝试从观测变量的协方差结构里找出主要方向。

## 中心化

PCA 首先要中心化数据。中心化是减去每列均值。

```python
X_centered = frame - frame.mean()

print(X_centered.mean())
```

如果不中心化，第一主成分可能去解释均值水平，而不是变量的共同波动。

注意：中心化不等于标准化。中心化只减均值；标准化还会除以标准差。

## 协方差矩阵

PCA 的核心对象是协方差矩阵。

```python
cov = np.cov(X_centered, rowvar=False)

cov_df = pd.DataFrame(cov, index=columns, columns=columns)

print(cov_df)
```

`rowvar=False` 表示每一列是一个变量。对常见形状 `(n_samples, n_features)`，通常应使用 `rowvar=False`。

协方差矩阵是对称矩阵，因此可以使用 `np.linalg.eigh`。

## 特征值分解

对协方差矩阵做特征值分解：

```python
eigvals, eigvecs = np.linalg.eigh(cov)

print(eigvals)
print(eigvecs)
```

`eigh` 返回的特征值默认从小到大排列。PCA 需要按解释方差从大到小排列。

```python
order = eigvals.argsort()[::-1]

eigvals = eigvals[order]
components = eigvecs[:, order]
```

为了让展示结果更稳定，可以把每个主成分方向的最大绝对载荷调整为正。注意这只是符号约定，不改变 PCA 本身。

```python
for j in range(components.shape[1]):
    largest_loading = np.argmax(np.abs(components[:, j]))
    if components[largest_loading, j] < 0:
        components[:, j] *= -1

component_table = pd.DataFrame(
    components,
    index=columns,
    columns=[f"pc{i + 1}" for i in range(components.shape[1])],
)

print(eigvals)
print(component_table)
```

PCA 的符号不唯一。`v` 是特征向量，`-v` 也是同一个方向。解释主成分时不要过度纠结正负号本身，要看相对载荷。

## 解释方差比例

每个特征值就是对应主成分得分的方差。

```python
explained_ratio = eigvals / eigvals.sum()

explained_table = pd.DataFrame({
    "eigenvalue": eigvals,
    "explained_ratio": explained_ratio,
    "cumulative_ratio": np.cumsum(explained_ratio),
}, index=[f"pc{i + 1}" for i in range(len(eigvals))])

print(explained_table)
```

本例由两个潜在因子生成，所以前两个主成分会解释绝大部分方差。

如果前几个主成分累计解释比例很高，说明原始变量中存在较强的低维共同结构。

## 主成分得分

主成分方向是 `components`。每一行样本投影到这些方向上，得到主成分得分。

```python
scores = X_centered.to_numpy() @ components

scores_df = pd.DataFrame(
    scores,
    columns=[f"pc{i + 1}_score" for i in range(scores.shape[1])],
    index=frame.index,
)

print(scores_df.head())
```

主成分得分之间应该近似不相关。它们的协方差矩阵应该接近对角矩阵，对角线就是特征值。

```python
score_cov = np.cov(scores, rowvar=False)

print(score_cov)
```

这就是 PCA 把相关变量转换成正交变量的含义。

## 降维和重构

如果只保留前 `k` 个主成分：

```text
X_hat_k = scores_k components_k'
```

再加回均值，就得到原始数据的低维重构。

```python
def reconstruct(scores, components, mean, k):
    return scores[:, :k] @ components[:, :k].T + mean


mean = frame.mean().to_numpy()

reconstruction_rows = []

for k in [1, 2, 4]:
    X_hat = reconstruct(scores, components, mean, k)
    recon_mse = np.mean((frame.to_numpy() - X_hat) ** 2)
    reconstruction_rows.append({
        "n_components": k,
        "reconstruction_mse": recon_mse,
    })

reconstruction_table = pd.DataFrame(reconstruction_rows)

print(reconstruction_table)
```

本例中 2 个主成分已经抓住大部分共同结构，重构误差会比只用 1 个主成分小很多。

如果保留所有主成分，重构误差应接近 0。

## PCA 和 SVD 的关系

PCA 也可以通过 SVD 计算。

对中心化矩阵：

```text
X = U S V'
```

右奇异向量 `V` 就是主成分方向，特征值为：

```text
lambda_j = S_j^2 / (n - 1)
```

```python
U, singular_values, Vt = np.linalg.svd(
    X_centered.to_numpy(),
    full_matrices=False,
)

eigvals_from_svd = singular_values ** 2 / (n - 1)
components_from_svd = Vt.T

print(eigvals_from_svd)
print(np.allclose(eigvals, eigvals_from_svd))
print(np.allclose(np.abs(components), np.abs(components_from_svd)))
```

实际大型数据常通过 SVD 算 PCA，比显式构造协方差矩阵更稳定。

## 和 sklearn PCA 对齐

用 sklearn 验证手算结果：

```python
pca = PCA(n_components=4)
pca.fit(X_centered)

print(pca.explained_variance_)
print(pca.explained_variance_ratio_)
print(np.allclose(eigvals, pca.explained_variance_))
print(np.allclose(explained_ratio, pca.explained_variance_ratio_))
```

组件方向仍然有符号不唯一的问题，因此比较时通常看绝对值：

```python
print(np.allclose(np.abs(components), np.abs(pca.components_.T)))
```

## 协方差 PCA 和相关矩阵 PCA

如果变量量纲不同，协方差 PCA 会被高方差变量主导。

把 `asset_d` 放大 10 倍：

```python
scaled_frame = frame.copy()
scaled_frame["asset_d_scaled_x10"] = scaled_frame.pop("asset_d") * 10.0

scaled_centered = scaled_frame - scaled_frame.mean()
scaled_cov = np.cov(scaled_centered, rowvar=False)

scaled_eigvals, scaled_eigvecs = np.linalg.eigh(scaled_cov)
scaled_order = scaled_eigvals.argsort()[::-1]

scaled_eigvals = scaled_eigvals[scaled_order]
scaled_eigvecs = scaled_eigvecs[:, scaled_order]

first_scaled_loading = pd.Series(
    scaled_eigvecs[:, 0],
    index=scaled_frame.columns,
)

print(scaled_eigvals[0] / scaled_eigvals.sum())
print(first_scaled_loading)
```

第一主成分会几乎完全由放大后的变量支配。这不一定错，但你必须确认这是否符合研究目的。

如果希望每个变量先变成同等尺度，可以标准化后做 PCA。这等价于对相关矩阵做 PCA。

```python
Z = StandardScaler().fit_transform(scaled_frame)

corr_cov = np.cov(Z, rowvar=False)
corr_eigvals, _ = np.linalg.eigh(corr_cov)
corr_eigvals = np.sort(corr_eigvals)[::-1]

corr_explained_ratio = corr_eigvals / corr_eigvals.sum()

print(corr_explained_ratio)
```

协方差 PCA 和相关矩阵 PCA 都合理，关键看问题：

- 如果变量单位相同，方差大小本身有意义，可以用协方差 PCA。
- 如果变量单位不同，或只关心相关结构，通常先标准化。

## 主成分如何解释

解释 PCA 时看载荷，也就是 `component_table`。

如果一个主成分对所有资产载荷同号，通常像“共同市场方向”。

如果一个主成分对前两列为正、后两列为负，可能像“风格差异方向”。

但 PCA 只看方差，不看标签，不保证有经济含义。解释主成分需要结合业务背景、变量定义和稳定性检验。

## 常见坑

第一，忘记中心化。

PCA 分析的是围绕均值的波动结构。没有中心化时，主成分可能解释均值水平。

第二，量纲不同却直接做协方差 PCA。

高方差变量会主导结果。是否标准化要由研究问题决定。

第三，把主成分符号当成固定含义。

主成分方向正负号可以整体翻转。解释时看相对载荷，不要依赖某次运行的符号。

第四，用 PCA 后解释单个原始变量的重要性。

PCA 是无监督方法，只最大化 `X` 的方差，不关心预测目标 `y`。高方差方向不一定是对预测最有用的方向。

第五，把 PCA 当成因子模型的完整替代。

PCA 可以提取统计因子，但金融因子模型还涉及经济解释、风险暴露、约束、中性化和样本外稳定性。

## 实战提示

做 PCA 时可以按下面流程：

1. 明确样本是行、变量是列。
2. 检查缺失值和异常值。
3. 决定中心化还是标准化后再 PCA。
4. 计算解释方差比例和累计比例。
5. 看主成分载荷，判断是否有可解释结构。
6. 用重构误差检查保留维度是否足够。
7. 在滚动窗口或样本外检查主成分是否稳定。
8. 如果用于预测，必须在训练集上 fit PCA，再 transform 测试集。

## 小结

本节的重点：

- PCA 是协方差矩阵的特征值分解。
- 主成分方向是特征向量，解释方差是特征值。
- 主成分得分互相正交，协方差矩阵为对角矩阵。
- 降维重构只保留前几个高方差方向。
- SVD 是计算 PCA 的常用稳定方法。
- 协方差 PCA 会受量纲影响，标准化后 PCA 等价于相关矩阵 PCA。
- PCA 是无监督降维，不保证对预测目标最有用。

## 自检问题

1. PCA 为什么要先中心化？
2. 协方差矩阵的特征值和解释方差有什么关系？
3. 主成分得分为什么互相不相关？
4. 为什么主成分方向的符号不唯一？
5. 协方差 PCA 和相关矩阵 PCA 有什么区别？
6. 为什么 PCA 不等于监督学习里的特征选择？
