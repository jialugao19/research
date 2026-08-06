# 概率统计：regularization 正则化、偏差-方差权衡与岭回归 / Lasso 直觉

## 核心概念

regularization 正则化是在拟合目标里加入惩罚项，限制模型复杂度。

OLS 最小化：

```text
sum((y_i - x_i beta)^2)
```

正则化回归最小化：

```text
loss(data, beta) + penalty(beta)
```

常见线性回归正则化：

- Ridge：L2 正则化，惩罚 `sum(beta_j^2)`。
- Lasso：L1 正则化，惩罚 `sum(abs(beta_j))`。
- Elastic Net：L1 和 L2 混合。

正则化的目标不是让训练误差最小，而是在样本外更稳：

- 降低共线性下的系数爆炸。
- 降低估计方差。
- 防止模型过度追逐训练集噪声。
- 在 Lasso 中产生稀疏系数，做变量选择的近似。

代价是引入偏差：系数会被有意压向 0。

## 准备环境

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
```

准备一组带严重共线性的模拟数据：

```python
rng = np.random.default_rng(52)

n_train = 60
n_test = 300

feature_names = ["x1", "x2_duplicate", "x3_signal", "x4_noise"]
true_beta_raw = np.array([0.8, 0.8, 0.15, 0.0])


def make_data(n):
    x1 = rng.normal(0.0, 1.0, size=n)
    x2 = x1 + rng.normal(0.0, 0.03, size=n)
    x3 = rng.normal(0.0, 1.0, size=n)
    x4 = rng.normal(0.0, 1.0, size=n)

    X = np.column_stack([x1, x2, x3, x4])
    y = X @ true_beta_raw + rng.normal(0.0, 0.7, size=n)

    return X, y


X_train, y_train = make_data(n_train)
X_test, y_test = make_data(n_test)
```

这里：

- `x1` 和 `x2_duplicate` 几乎是同一个变量。
- `x3_signal` 有一点真实信号。
- `x4_noise` 没有真实信号。

```python
corr_x1_x2 = np.corrcoef(X_train[:, 0], X_train[:, 1])[0, 1]

print(corr_x1_x2)
```

严重共线性会让 OLS 的单个系数很不稳定。

## 为什么先标准化

正则化惩罚的是系数大小。如果特征量纲不同，惩罚强度就不可比。

例如一个变量单位是“元”，另一个变量单位是“亿元”，同样的经济含义会对应完全不同的系数数值。

因此正则化前通常要用训练集均值和标准差标准化：

```python
train_mean = X_train.mean(axis=0)
train_scale = X_train.std(axis=0)

Z_train = (X_train - train_mean) / train_scale
Z_test = (X_test - train_mean) / train_scale

print(Z_train.mean(axis=0))
print(Z_train.std(axis=0))
```

注意：标准化参数只能从训练集学到。测试集和未来数据必须复用训练集的 `train_mean` 和 `train_scale`。

## OLS 在共线性下的系数爆炸

先写两个小函数。

```python
def mse(y_true, y_pred):
    return float(np.mean((y_true - y_pred) ** 2))


def fit_ols(Z, y):
    intercept = y.mean()
    beta = np.linalg.lstsq(Z, y - intercept, rcond=None)[0]
    return intercept, beta
```

在标准化后的设计矩阵上拟合 OLS：

```python
ols_intercept, ols_beta = fit_ols(Z_train, y_train)

ols_coef = pd.Series(ols_beta, index=feature_names, name="ols_coef")

print(ols_coef)
print(np.linalg.norm(ols_beta))
```

由于 `x1` 和 `x2_duplicate` 几乎重复，OLS 可能给出一个很大的负系数和一个很大的正系数。二者合起来预测还可以，但单个系数解释已经不可靠。

## Ridge 的目标函数

Ridge 在平方误差后加入 L2 惩罚：

```text
min_beta ||y - X beta||^2 + alpha ||beta||^2
```

标准化并把截距单独处理后，Ridge 解为：

```text
beta_ridge = (Z'Z + alpha I)^(-1) Z'y_centered
```

其中 `alpha >= 0` 控制正则强度：

- `alpha = 0` 时退化为 OLS。
- `alpha` 越大，系数越靠近 0。
- 太大的 `alpha` 会欠拟合。

截距通常不惩罚。下面的实现只惩罚特征系数：

```python
def fit_ridge(Z, y, alpha):
    intercept = y.mean()
    centered_y = y - intercept

    penalty = alpha * np.eye(Z.shape[1])
    beta = np.linalg.solve(Z.T @ Z + penalty, Z.T @ centered_y)

    return intercept, beta
```

拟合一个 `alpha=1.0` 的 Ridge：

```python
ridge_intercept, ridge_beta = fit_ridge(Z_train, y_train, alpha=1.0)

ridge_coef = pd.Series(ridge_beta, index=feature_names, name="ridge_coef")

print(ridge_coef)
print(np.linalg.norm(ridge_beta))
```

和 OLS 相比，Ridge 把共线变量的极端正负系数压回更稳定的范围。

## alpha 路径

观察不同 `alpha` 下的系数、条件数和测试误差：

```python
alphas = [0.0, 0.1, 1.0, 10.0, 100.0]
rows = []

for alpha in alphas:
    if alpha == 0.0:
        intercept, beta = fit_ols(Z_train, y_train)
        effective_condition = np.linalg.cond(Z_train.T @ Z_train)
    else:
        intercept, beta = fit_ridge(Z_train, y_train, alpha=alpha)
        effective_condition = np.linalg.cond(
            Z_train.T @ Z_train + alpha * np.eye(Z_train.shape[1])
        )

    train_pred = intercept + Z_train @ beta
    test_pred = intercept + Z_test @ beta

    rows.append({
        "alpha": alpha,
        "condition": effective_condition,
        "beta_norm": np.linalg.norm(beta),
        "train_mse": mse(y_train, train_pred),
        "test_mse": mse(y_test, test_pred),
        "x1": beta[0],
        "x2_duplicate": beta[1],
        "x3_signal": beta[2],
        "x4_noise": beta[3],
    })

ridge_path = pd.DataFrame(rows)

print(ridge_path)
```

通常会看到：

- `alpha` 增大后，`condition` 下降，数值问题变稳定。
- `beta_norm` 下降，系数被压小。
- 训练误差通常上升。
- 测试误差可能先下降后上升。

这就是偏差-方差权衡的直观版本：适度正则化降低方差，过度正则化带来过大偏差。

## Ridge 的偏差

Ridge 不是无偏估计。固定设计矩阵时，如果真实标准化系数是 `beta_true`，Ridge 的期望大致被下面这个矩阵压缩：

```text
E[beta_ridge | Z] = (Z'Z + alpha I)^(-1) Z'Z beta_true
```

```python
true_beta_standardized = true_beta_raw * train_scale

alpha = 1.0
expected_ridge = np.linalg.solve(
    Z_train.T @ Z_train + alpha * np.eye(Z_train.shape[1]),
    Z_train.T @ Z_train @ true_beta_standardized,
)

ridge_bias = expected_ridge - true_beta_standardized

bias_table = pd.DataFrame({
    "true_beta_standardized": true_beta_standardized,
    "expected_ridge": expected_ridge,
    "bias": ridge_bias,
}, index=feature_names)

print(bias_table)
```

Ridge 主动引入偏差，换取更低的估计方差和更稳的样本外表现。

## Ridge 的方差降低

用固定的 `X_train` 重复模拟不同噪声，比较 OLS 和 Ridge 系数的波动。

```python
sim_rng = np.random.default_rng(999)

ols_samples = []
ridge_samples = []

for _ in range(500):
    y_sim = X_train @ true_beta_raw + sim_rng.normal(0.0, 0.7, size=n_train)

    _, beta_ols_sim = fit_ols(Z_train, y_sim)
    _, beta_ridge_sim = fit_ridge(Z_train, y_sim, alpha=1.0)

    ols_samples.append(beta_ols_sim)
    ridge_samples.append(beta_ridge_sim)

ols_samples = np.asarray(ols_samples)
ridge_samples = np.asarray(ridge_samples)

variance_table = pd.DataFrame({
    "ols_std": ols_samples.std(axis=0),
    "ridge_std": ridge_samples.std(axis=0),
}, index=feature_names)

print(variance_table)
```

在 `x1` 和 `x2_duplicate` 这两个高度共线变量上，OLS 系数会大幅摆动。Ridge 把这两个方向的波动压得很小。

注意：两个共线变量的“合计预测效果”可能稳定，但单个 OLS 系数不稳定。正则化主要稳定的是估计问题。

## Lasso 的目标函数

Lasso 使用 L1 惩罚：

```text
min_beta loss(data, beta) + alpha sum(abs(beta_j))
```

L1 惩罚的特点是会把一些系数压成精确的 0，因此常被用作稀疏建模或变量筛选。

为了理解 Lasso，可以先看 soft-thresholding：

```python
def soft_threshold(z, penalty):
    return np.sign(z) * np.maximum(np.abs(z) - penalty, 0.0)


z = np.array([1.2, 0.4, -0.1, -1.5])
soft = soft_threshold(z, penalty=0.5)

print(soft)
```

小于惩罚强度的值会被压到 0，大于惩罚强度的值会向 0 收缩。

多变量 Lasso 通常没有像 Ridge 那样简单的闭式解。实践中使用坐标下降等数值算法。

## 用 sklearn 拟合 Lasso

这里直接在标准化后的 `Z_train` 上拟合 Lasso。

```python
lasso = Lasso(
    alpha=0.20,
    fit_intercept=True,
    max_iter=100_000,
    tol=1e-10,
)

lasso.fit(Z_train, y_train)

lasso_coef = pd.Series(
    lasso.coef_,
    index=feature_names,
    name="lasso_coef",
)

lasso_pred = lasso.predict(Z_test)

print(lasso_coef)
print(mse(y_test, lasso_pred))
```

在这个例子里，`x1` 和 `x2_duplicate` 几乎重复。Lasso 可能只保留其中一个，把另一个压到 0。

这很有用，但也有风险：在高度相关的特征组里，Lasso 选哪个变量可能不稳定。不要把“被 Lasso 选中”直接解释成因果重要性。

注意：sklearn 的 `Lasso(alpha=...)` 使用的是带 `1 / (2n)` 缩放的目标函数。不同教材和软件里的 `alpha` 数值不可直接比较，但正则强弱的方向一致。

## Ridge 和 Lasso 的区别

Ridge：

- L2 惩罚。
- 系数连续收缩，很少精确为 0。
- 对共线变量通常会分摊权重。
- 适合希望保留所有变量、提升稳定性的场景。

Lasso：

- L1 惩罚。
- 可以产生精确 0 系数。
- 可以做变量筛选。
- 在相关特征组中可能随机保留其中一个，选择不一定稳定。

Elastic Net：

- 混合 L1 和 L2。
- 既能稀疏，又比纯 Lasso 更能处理相关特征组。

## alpha 不能用测试集挑

`alpha` 是超参数，不能看测试集结果后手动挑。

正确流程：

1. 训练集内做交叉验证或留出验证集。
2. 在验证集上选择 `alpha`。
3. 用固定的 `alpha` 重新训练。
4. 最后只在测试集上评估一次。

时间序列任务还要使用时间顺序切分，不能随机打乱后交叉验证。

## 常见坑

第一，不标准化就做正则化。

不同量纲会导致惩罚不公平。正则化通常应先用训练集参数标准化特征。

第二，惩罚截距。

截距只是均值水平，通常不应被 L1/L2 惩罚。常见库默认会单独处理截距，但手写公式时要注意。

第三，把 `alpha` 越大越好。

正则化过强会欠拟合。训练误差上升是正常的，但测试误差也可能在过强惩罚下变差。

第四，把 Lasso 选择解释成真因果。

Lasso 做的是预测意义上的稀疏化。相关变量之间谁被选中，可能对样本扰动很敏感。

第五，用测试集挑 `alpha`。

这会污染最终评估。超参数选择属于训练过程，只能使用训练期内部验证。

## 实战提示

使用正则化线性模型时，可以按下面流程：

1. 明确预测目标和特征列。
2. 按时间或任务要求切分训练、验证、测试。
3. 只用训练集拟合标准化参数。
4. 在训练集内部选择 `alpha`。
5. 共线变量多、想稳定预测时优先试 Ridge。
6. 想做稀疏特征筛选时试 Lasso 或 Elastic Net。
7. 对相关特征组，不要过度解读单个 Lasso 系数。
8. 报告训练误差、验证误差、测试误差和系数路径。

## 小结

本节的重点：

- 正则化在损失函数中加入系数惩罚。
- Ridge 使用 L2 惩罚，能稳定共线性下的系数估计。
- Lasso 使用 L1 惩罚，可以把部分系数压成 0。
- 正则化引入偏差，换取更低方差和更稳的样本外表现。
- 特征标准化和不惩罚截距是实践中的关键细节。
- `alpha` 必须通过训练期内部验证选择，不能用测试集调。

## 自检问题

1. Ridge 和 OLS 的目标函数有什么区别？
2. 为什么正则化前通常要标准化特征？
3. Ridge 为什么能缓解共线性？
4. 正则化为什么会引入偏差？
5. Lasso 为什么能产生精确 0 系数？
6. 在高度相关特征组中，为什么不能过度解读 Lasso 选中的单个变量？
7. 为什么不能用测试集选择 `alpha`？
