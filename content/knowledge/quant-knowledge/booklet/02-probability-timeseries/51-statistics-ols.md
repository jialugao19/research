# 51. 概率统计：OLS 的矩阵形式、估计、解释与诊断入口

## 核心概念

OLS 是 Ordinary Least Squares，普通最小二乘。它估计线性关系：

```text
y = X beta + epsilon
```

其中：

- `y` 是被解释变量，形状是 `n x 1`。
- `X` 是解释变量矩阵，形状是 `n x k`。
- `beta` 是待估系数，形状是 `k x 1`。
- `epsilon` 是误差项。

OLS 选择一组 `beta_hat`，让残差平方和最小：

```text
min_beta sum((y_i - x_i beta)^2)
```

写成矩阵形式就是：

```text
min_beta ||y - X beta||^2
```

如果 `X` 满列秩，OLS 解满足 normal equation：

```text
X'X beta_hat = X'y
```

闭式解是：

```text
beta_hat = (X'X)^(-1) X'y
```

实际写代码时，不建议显式求逆再乘。更稳妥的是用 `np.linalg.solve` 或 `np.linalg.lstsq`。

## 准备环境

```python
import numpy as np
import pandas as pd
from scipy import stats
```

准备一组模拟横截面数据。可以把每行理解为一只股票在某个截面的因子暴露和未来收益。

```python
rng = np.random.default_rng(53)
n = 100

momentum = rng.normal(0.0, 1.0, size=n)
value = 0.25 * momentum + rng.normal(0.0, 1.0, size=n)
noise = rng.normal(0.0, 0.020, size=n)

y = 0.005 + 0.020 * momentum + 0.014 * value + noise

data = pd.DataFrame({
    "future_return": y,
    "momentum": momentum,
    "value": value,
})

print(data.head())
```

这里真实数据生成过程包含：

- 截距：`0.005`
- `momentum` 系数：`0.020`
- `value` 系数：`0.014`

真实项目中我们不知道这些值；模拟数据只是为了验证 OLS 的计算。

## 构造 y 和 X

OLS 的矩阵接口要求显式构造 `y` 和 `X`。

```python
y = data["future_return"].to_numpy()

X = np.column_stack([
    np.ones(n),
    data["momentum"].to_numpy(),
    data["value"].to_numpy(),
])

column_names = ["intercept", "momentum", "value"]

print(X.shape)
print(y.shape)
```

第一列 `np.ones(n)` 是截距项。没有这列，模型会被强制穿过原点。

## normal equation 手算 OLS

根据 normal equation：

```python
xtx = X.T @ X
xty = X.T @ y

beta_hat = np.linalg.solve(xtx, xty)

coef = pd.Series(beta_hat, index=column_names, name="coef")

print(coef)
```

`np.linalg.solve(xtx, xty)` 解的是线性方程组：

```text
(X'X) beta_hat = X'y
```

这比 `np.linalg.inv(xtx) @ xty` 更稳，也更符合数值线性代数的习惯。

用 `lstsq` 可以直接解最小二乘问题：

```python
beta_lstsq, residuals_lstsq, rank, singular_values = np.linalg.lstsq(
    X,
    y,
    rcond=None,
)

print(beta_lstsq)
print(rank)
print(singular_values)
```

在满秩情形下，`solve` 和 `lstsq` 的结果应一致。

```python
print(np.allclose(beta_hat, beta_lstsq))
```

## 拟合值和残差

拟合值：

```text
y_hat = X beta_hat
```

残差：

```text
e_hat = y - y_hat
```

```python
fitted = X @ beta_hat
resid = y - fitted

fit_table = pd.DataFrame({
    "actual": y,
    "fitted": fitted,
    "residual": resid,
})

print(fit_table.head())
```

OLS 的一阶条件意味着残差和每一列解释变量正交：

```text
X' e_hat = 0
```

可以数值验证：

```python
orthogonality = X.T @ resid

print(orthogonality)
print(resid.mean())
```

如果模型包含截距，残差均值会接近 0，因为截距列就是一列 1。

## R-squared

残差平方和：

```text
RSS = sum((y_i - y_hat_i)^2)
```

总平方和：

```text
TSS = sum((y_i - mean(y))^2)
```

R-squared：

```text
R^2 = 1 - RSS / TSS
```

```python
rss = float(resid @ resid)
tss = float((y - y.mean()) @ (y - y.mean()))
r_squared = 1.0 - rss / tss

print(rss)
print(tss)
print(r_squared)
```

`R^2` 表示样本内方差解释比例。它不是样本外预测能力，也不是因果证明。

调整后的 R-squared 会惩罚解释变量数量：

```python
k = X.shape[1]
df_resid = n - k

adj_r_squared = 1.0 - (rss / df_resid) / (tss / (n - 1))

print(adj_r_squared)
```

## 标准误、t 值和置信区间

在经典同方差假设下：

```text
Var(beta_hat | X) = sigma^2 (X'X)^(-1)
```

其中 `sigma^2` 可以用残差平方和估计：

```text
sigma_hat^2 = RSS / (n - k)
```

```python
sigma2_hat = rss / df_resid
xtx_inv = np.linalg.inv(xtx)
cov_beta = sigma2_hat * xtx_inv

std_err = np.sqrt(np.diag(cov_beta))
t_values = beta_hat / std_err
p_values = 2.0 * stats.t.sf(np.abs(t_values), df=df_resid)

t_crit = stats.t.ppf(0.975, df=df_resid)
ci_low = beta_hat - t_crit * std_err
ci_high = beta_hat + t_crit * std_err

coef_table = pd.DataFrame({
    "coef": beta_hat,
    "std_err": std_err,
    "t": t_values,
    "pvalue": p_values,
    "ci_low": ci_low,
    "ci_high": ci_high,
}, index=column_names)

print(coef_table)
```

解释：

- `coef` 是系数估计。
- `std_err` 是估计不确定性。
- `t` 是 `coef / std_err`。
- `pvalue` 是在经典假设下检验系数为 0 的 p 值。
- `ci_low` 和 `ci_high` 是 95% 置信区间。

在金融数据中，同方差和独立误差经常不成立。真实研究里常需要稳健标准误、聚类标准误或时间序列修正，这些属于后续诊断和计量细节。

## 系数解释

本例中 `momentum` 系数表示：

```text
在 value 不变的条件下，momentum 增加 1 个单位，future_return 的线性预测平均增加 beta_momentum。
```

```python
momentum_effect = coef.loc["momentum"]

print(momentum_effect)
```

“控制其他变量”是多元回归解释的关键。`momentum` 的系数不是简单相关系数，而是在 `value` 已经进入模型后，`momentum` 的边际线性关系。

## 遗漏变量偏差

如果真实模型里有 `value`，但你只回归 `momentum`，`momentum` 的系数可能被污染。

```python
X_momentum_only = np.column_stack([
    np.ones(n),
    data["momentum"].to_numpy(),
])

beta_momentum_only = np.linalg.lstsq(
    X_momentum_only,
    y,
    rcond=None,
)[0]

omitted_compare = pd.Series({
    "full_model_momentum": beta_hat[column_names.index("momentum")],
    "momentum_only": beta_momentum_only[1],
    "corr_momentum_value": np.corrcoef(momentum, value)[0, 1],
})

print(omitted_compare)
```

因为本例中 `momentum` 和 `value` 有相关性，遗漏 `value` 后，`momentum` 的系数吸收了一部分 `value` 的影响。

遗漏变量偏差需要同时满足两个条件：

1. 被遗漏变量影响 `y`。
2. 被遗漏变量和已包含解释变量相关。

## 截距项不能随便省略

如果不加截距，模型被迫穿过原点。

```python
X_no_intercept = X[:, 1:]

beta_no_intercept = np.linalg.lstsq(
    X_no_intercept,
    y,
    rcond=None,
)[0]

resid_no_intercept = y - X_no_intercept @ beta_no_intercept

no_intercept_compare = pd.Series({
    "rss_with_intercept": rss,
    "rss_no_intercept": float(resid_no_intercept @ resid_no_intercept),
    "mean_resid_with_intercept": resid.mean(),
    "mean_resid_no_intercept": resid_no_intercept.mean(),
})

print(no_intercept_compare)
```

除非理论上明确要求过原点，否则 OLS 通常应包含截距。没有截距时，残差均值不再保证为 0，R-squared 的解释也会变得更容易误读。

## 多重共线性和条件数

如果解释变量之间几乎线性相关，`X'X` 会接近奇异，系数估计会非常不稳定。

构造一个几乎等于 `2 * momentum` 的变量：

```python
almost_duplicate = 2.0 * momentum + rng.normal(0.0, 1e-4, size=n)

X_bad = np.column_stack([
    np.ones(n),
    momentum,
    almost_duplicate,
])

condition_good = np.linalg.cond(X.T @ X)
condition_bad = np.linalg.cond(X_bad.T @ X_bad)

print(condition_good)
print(condition_bad)
```

条件数越大，矩阵越接近病态。病态矩阵会让系数对微小噪声非常敏感。

```python
beta_bad = np.linalg.lstsq(X_bad, y, rcond=None)[0]

print(beta_bad)
```

这不一定导致预测值完全崩溃，但会让单个系数解释变得不可靠。正则化会在下一节处理这类问题。

## 杠杆值和诊断入口

OLS 的 fitted value 可以写成：

```text
y_hat = H y
```

其中：

```text
H = X (X'X)^(-1) X'
```

`H` 叫 hat matrix。对角线元素是 leverage，表示某个样本的解释变量位置有多极端。

```python
hat_matrix = X @ xtx_inv @ X.T
leverage = np.diag(hat_matrix)

leverage_summary = pd.Series({
    "sum_leverage": leverage.sum(),
    "num_parameters": k,
    "mean_leverage": leverage.mean(),
    "max_leverage": leverage.max(),
    "high_leverage_rule": 2.0 * k / n,
    "max_leverage_row": int(np.argmax(leverage)),
})

print(leverage_summary)
```

leverage 的和等于参数个数 `k`。高杠杆点不一定是坏点，但它有能力强烈影响拟合结果。完整诊断还需要结合残差、Cook's distance、异方差检验和稳健标准误。

## OLS 假设的层次

OLS 结果要分清三层：

第一，系数作为最小二乘投影。

只要 `X` 满秩，就能计算出让样本残差平方和最小的 `beta_hat`。

第二，系数作为条件均值的估计。

需要假设线性条件均值或至少把 OLS 看成最佳线性近似。

第三，p 值和置信区间作为统计推断。

需要更强的误差假设，例如外生性、独立性、同方差或合适的稳健标准误。

常见经典假设包括：

- 线性：`E[y | X]` 可以用 `X beta` 表示，或至少线性近似有意义。
- 满秩：解释变量没有完全线性相关。
- 外生性：`E[epsilon | X] = 0`。
- 同方差：`Var(epsilon | X)` 为常数。
- 独立性：样本误差之间没有相关。
- 正态性：小样本精确 t/F 推断常用；大样本下可由渐近理论替代。

这些假设不是为了让 OLS 能运行，而是为了让解释和推断可信。

## 常见坑

第一，忘记截距。

矩阵接口里截距要手动添加。没有截距时，模型过原点，残差均值也不再保证为 0。

第二，把 p 值当成交易信号。

p 值小只说明在当前模型和假设下系数不太像 0，不代表样本外一定有效，更不代表扣费后能赚钱。

第三，忽略共线性。

高度相关的解释变量会让单个系数非常不稳定。看系数前先看变量相关性、条件数和经济含义。

第四，把相关解释成因果。

OLS 系数是条件相关或线性投影。要做因果解释，还需要识别假设、实验设计、工具变量、断点、双重差分等更强框架。

第五，在时间序列或面板数据里直接使用普通标准误。

金融数据常有异方差、序列相关和横截面相关。普通 OLS 标准误可能过于乐观。

## 实战提示

做 OLS 时可以按这个顺序检查：

1. 明确 `y` 是什么，`X` 里有哪些变量。
2. 确认是否需要截距，通常需要。
3. 用 `np.linalg.lstsq` 或成熟库拟合，不要手写显式逆作为生产代码。
4. 检查 `X` 的秩和条件数。
5. 看残差、R-squared、系数符号和经济量级。
6. 区分样本内拟合、样本外预测和因果解释。
7. 根据数据结构选择普通标准误、稳健标准误、聚类标准误或时间序列修正。
8. 对金融预测任务，最后仍要用严格的样本外验证和回测。

## 小结

本节的重点：

- OLS 最小化残差平方和。
- 满秩时，OLS 解满足 `X'X beta_hat = X'y`。
- 有截距时，残差均值为 0，残差与解释变量正交。
- `R^2` 是样本内解释度，不等于预测能力。
- 标准误和 p 值依赖误差假设。
- 遗漏变量、无截距、共线性和高杠杆点都会影响解释。
- OLS 可以是预测工具、描述工具，也可以在额外假设下用于因果分析，但三者不能混为一谈。

## 自检问题

1. OLS 的目标函数是什么？
2. 为什么矩阵接口通常要手动加入截距列？
3. normal equation `X'X beta_hat = X'y` 来自什么一阶条件？
4. 为什么有截距时残差均值接近 0？
5. `R^2` 高为什么不等于样本外预测能力强？
6. 遗漏变量偏差需要哪两个条件？
7. 条件数很大时，系数解释为什么危险？
