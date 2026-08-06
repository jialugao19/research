# Covariance Shrinkage

## 核心概念

协方差矩阵描述多个资产收益如何一起变化。

在投资组合里，它直接进入组合方差：

```text
portfolio_variance = w' Sigma w
```

也进入最小方差组合：

```text
w ∝ Sigma^(-1) 1
```

问题是：样本协方差矩阵 `S` 在样本少、资产多、资产高度相关时很不稳定。

常见现象：

- 最小特征值被估得过小。
- 条件数很大，求逆放大噪声。
- 最小方差组合权重极端。
- 样本内预测风险很低，样本外实际风险很高。
- 当样本数小于资产数时，样本协方差矩阵直接奇异。

covariance shrinkage 协方差收缩的基本思想是：

```text
shrunk_cov = (1 - alpha) * sample_cov + alpha * target_cov
```

其中：

- `sample_cov`：数据估出来的样本协方差，信息丰富但噪声大。
- `target_cov`：更简单、更稳定的目标矩阵，偏差大但方差小。
- `alpha`：收缩强度，越大越接近目标矩阵。

这和正则化的思想类似：主动引入一点偏差，换取更低估计方差和更稳定的求逆。

## 准备环境

```python
import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf
```

准备一组由共同因子驱动的资产收益。真实协方差矩阵在模拟中已知，但在真实研究里未知。

```python
rng = np.random.default_rng(2024)

n_assets = 25
n_train = 40
n_test = 1000
n_factors = 3

loadings = rng.normal(0.0, 1.0, size=(n_assets, n_factors))
factor_vol = np.array([0.020, 0.014, 0.010])
idio_vol = rng.uniform(0.008, 0.020, size=n_assets)

true_cov = (
    loadings @ np.diag(factor_vol ** 2) @ loadings.T
    + np.diag(idio_vol ** 2)
)

train_returns = rng.multivariate_normal(
    mean=np.zeros(n_assets),
    cov=true_cov,
    size=n_train,
)

test_returns = rng.multivariate_normal(
    mean=np.zeros(n_assets),
    cov=true_cov,
    size=n_test,
)

asset_names = [f"asset_{i:02d}" for i in range(n_assets)]
```

这里训练样本只有 40 天，资产有 25 个。这个比例已经足以让样本协方差很嘈杂。

## 样本协方差

样本协方差：

```python
sample_cov = np.cov(train_returns, rowvar=False)

sample_cov_df = pd.DataFrame(
    sample_cov,
    index=asset_names,
    columns=asset_names,
)

print(sample_cov_df.iloc[:5, :5])
```

检查特征值和条件数：

```python
sample_eigvals = np.linalg.eigvalsh(sample_cov)
sample_condition = np.linalg.cond(sample_cov)

print(sample_eigvals[:5])
print(sample_eigvals[-5:])
print(sample_condition)
```

条件数越大，矩阵求逆越不稳定。协方差矩阵要被用于组合优化时，这个问题尤其严重。

## 小样本下的奇异问题

如果样本数小于资产数，样本协方差矩阵最多只有 `n_obs - 1` 的秩，通常不可逆。

```python
small_sample = train_returns[:15]
small_cov = np.cov(small_sample, rowvar=False)

small_rank = np.linalg.matrix_rank(small_cov)

print(small_cov.shape)
print(small_rank)
```

这里 `small_cov` 是 `25 x 25`，但秩最多是 14。最小方差组合需要求逆，这种矩阵不能直接稳定使用。

## 简单目标矩阵

最常见的收缩目标包括：

- 对角矩阵：保留每个资产方差，去掉相关性。
- 等方差单位矩阵：所有资产方差相同，互不相关。
- 常数相关矩阵：保留平均相关结构。
- 因子模型协方差：用少数因子解释共同波动。

先构造两个简单目标：

```python
diag_target = np.diag(np.diag(sample_cov))

avg_variance = np.trace(sample_cov) / n_assets
identity_target = avg_variance * np.eye(n_assets)
```

对角目标承认每个资产波动不同，但不相信样本相关性。

单位目标更强，认为所有资产都有相同方差且互不相关。

## 手写 shrinkage

手写一个收缩函数：

```python
def shrink_cov(sample_cov, target_cov, alpha):
    return (1.0 - alpha) * sample_cov + alpha * target_cov
```

用 `alpha=0.4` 分别向两个目标收缩：

```python
alpha = 0.4

diag_shrunk_cov = shrink_cov(sample_cov, diag_target, alpha)
identity_shrunk_cov = shrink_cov(sample_cov, identity_target, alpha)

condition_table = pd.Series({
    "sample": np.linalg.cond(sample_cov),
    "diag_shrunk": np.linalg.cond(diag_shrunk_cov),
    "identity_shrunk": np.linalg.cond(identity_shrunk_cov),
})

print(condition_table)
```

收缩后条件数通常会明显下降。直觉上，向稳定目标靠近会抬高过小特征值，减少求逆时的噪声放大。

## Ledoit-Wolf 直觉

Ledoit-Wolf 是常用的自动协方差收缩方法。它的目标是自动估计一个收缩强度，在样本协方差的噪声和目标矩阵的偏差之间折中。

sklearn 提供了实现：

```python
lw = LedoitWolf().fit(train_returns)

lw_cov = lw.covariance_
lw_alpha = lw.shrinkage_

print(lw_alpha)
print(np.linalg.cond(lw_cov))
```

这里的 `lw_alpha` 是估计出的收缩强度。它不是越大越好，而是试图平衡：

- 样本协方差的高方差。
- 收缩目标的高偏差。

## 最小方差组合

最小方差组合在只要求权重和为 1 时为：

```text
w = Sigma^(-1) 1 / (1' Sigma^(-1) 1)
```

写成函数：

```python
def min_variance_weights(cov):
    ones = np.ones(cov.shape[0])
    raw = np.linalg.solve(cov, ones)
    return raw / (ones @ raw)
```

再写评估函数：

```python
def portfolio_report(weights, cov_used, test_returns):
    portfolio_returns = test_returns @ weights

    return pd.Series({
        "gross_leverage": np.sum(np.abs(weights)),
        "max_abs_weight": np.max(np.abs(weights)),
        "ex_ante_vol": np.sqrt(weights @ cov_used @ weights),
        "realized_test_vol": portfolio_returns.std(ddof=1),
    })
```

分别用样本协方差、手写收缩协方差、Ledoit-Wolf 协方差和真实协方差计算组合：

```python
covariances = {
    "sample": sample_cov,
    "diag_shrunk": diag_shrunk_cov,
    "identity_shrunk": identity_shrunk_cov,
    "ledoit_wolf": lw_cov,
    "true_cov": true_cov,
}

weights = {
    name: min_variance_weights(cov)
    for name, cov in covariances.items()
}

portfolio_reports = pd.DataFrame({
    name: portfolio_report(w, covariances[name], test_returns)
    for name, w in weights.items()
}).T

print(portfolio_reports)
```

通常会看到：

- `sample` 的样本内预测波动 `ex_ante_vol` 很低，但样本外 `realized_test_vol` 明显更高。
- 收缩协方差的权重更温和。
- 收缩组合的样本外波动更接近真实最小方差组合。
- `true_cov` 是模拟里才知道的上限参照，真实研究中不可得。

## 为什么样本内风险会被低估

最小方差优化会主动寻找样本协方差里“看起来风险最低”的方向。

如果某些方向的风险只是被噪声低估，优化器会放大这些方向，导致：

```text
样本内风险很低
样本外风险并不低
权重很极端
```

这不是优化器坏了，而是输入的协方差估计太嘈杂。

协方差收缩不是保证收益更高，而是让风险估计和优化输入更稳。

## 特征值视角

比较几个矩阵的特征值：

```python
eig_table = pd.DataFrame({
    "sample": np.linalg.eigvalsh(sample_cov),
    "diag_shrunk": np.linalg.eigvalsh(diag_shrunk_cov),
    "identity_shrunk": np.linalg.eigvalsh(identity_shrunk_cov),
    "ledoit_wolf": np.linalg.eigvalsh(lw_cov),
})

print(eig_table.head())
print(eig_table.tail())
```

收缩常见效果：

- 抬高过小特征值。
- 压低过大特征值。
- 降低条件数。
- 让逆矩阵更稳定。

这和 Ridge 回归给 `X'X` 加 `alpha I` 的稳定化作用很相似。

## 选择 target 的含义

不同 target 代表不同先验信念：

- 对角 target：相信个体波动估计，不相信相关性估计。
- 单位 target：只相信平均方差，不相信个体差异和相关性。
- 常数相关 target：相信平均相关结构，不相信每一对资产的样本相关。
- 因子 target：相信低维因子结构。

target 越简单，估计方差越低，但偏差可能越大。

target 越复杂，偏差可能更小，但估计方差更高。

## 常见坑

第一，样本协方差可逆就直接用。

可逆不代表稳定。条件数很大时，求逆仍然会放大估计噪声。

第二，只看样本内组合风险。

样本协方差优化得到的 `ex_ante_vol` 可能过低。更重要的是样本外风险、滚动表现和权重稳定性。

第三，把收缩当作收益预测工具。

协方差收缩主要改善风险估计和优化稳定性，不会自动提高预期收益估计。

第四，忽略约束。

真实组合通常有 long-only、行业、杠杆、换手和容量约束。收缩协方差只是优化输入的一部分。

第五，混用不同频率和不同清洗规则的收益。

协方差估计对异常值、缺失值、不同交易日历和复权方式很敏感。矩阵方法不能替代数据清洗。

## 实战提示

使用协方差矩阵做组合优化时，可以按下面流程：

1. 检查收益矩阵形状：行是时间，列是资产。
2. 检查缺失值、异常值和资产上市/退市处理。
3. 计算样本协方差的秩、特征值和条件数。
4. 如果资产数接近或超过样本数，不要直接求逆样本协方差。
5. 尝试 Ledoit-Wolf、对角收缩、常数相关收缩或因子模型协方差。
6. 比较权重集中度、gross leverage、样本内风险和样本外风险。
7. 在滚动窗口中检查权重稳定性和换手。
8. 最终组合还要加入交易成本、约束和风险归因。

## 小结

本节的重点：

- 样本协方差在高维小样本下噪声很大。
- 协方差矩阵求逆会放大小特征值方向的估计误差。
- 收缩估计把样本协方差拉向稳定目标矩阵。
- 收缩引入偏差，但能降低估计方差和条件数。
- Ledoit-Wolf 自动估计收缩强度。
- 对组合优化，收缩通常能让权重和样本外风险更稳定。

## 自检问题

1. 为什么样本协方差矩阵在资产数接近样本数时不稳定？
2. covariance shrinkage 的一般公式是什么？
3. 对角 target 和单位 target 分别代表什么假设？
4. Ledoit-Wolf 想自动平衡什么？
5. 为什么最小方差组合特别容易放大协方差估计噪声？
6. 为什么样本内 `ex_ante_vol` 很低不一定是好事？
