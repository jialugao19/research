# 22. scipy.optimize：最小化、约束优化与根查找

## 核心概念

`scipy.optimize` 用来解决数值优化和方程求根问题。常见任务包括：

- 最小化一个标量目标函数。
- 在边界和约束下最小化目标函数。
- 寻找一元方程 `f(x) = 0` 的根。
- 寻找多元方程组 `F(x) = 0` 的根。

优化问题通常写成：

```text
minimize f(x)
```

其中 `x` 是待求参数，`f(x)` 必须返回一个标量。求根问题通常写成：

```text
find x such that f(x) = 0
```

优化器给出的结果是数值解，不是代数证明。使用时要检查是否收敛、约束是否满足、结果是否符合业务含义。

## 准备环境

```python
import numpy as np
import pandas as pd
from scipy import optimize
```

本节例子都使用小规模问题，便于观察输入、输出和约束语义。

## 一维最小化：minimize_scalar

先看一个一维函数：

```python
def objective_1d(x):
    return (x - 2.0) ** 2 + 1.0

result = optimize.minimize_scalar(objective_1d)

print(result.x)
print(result.fun)
print(result.success)
```

这个函数在 `x = 2` 处最小，最小值是 `1`。

`minimize_scalar` 返回的是 `OptimizeResult` 对象，常用字段包括：

- `x`：找到的最优点。
- `fun`：最优点处的目标函数值。
- `success`：是否成功收敛。
- `message`：优化器给出的说明。
- `nfev`：目标函数调用次数。

不要只看 `result.x`，至少要检查 `result.success`。

## 有边界的一维最小化

如果只允许在某个区间内搜索，可以使用 `method="bounded"`。

```python
bounded_result = optimize.minimize_scalar(
    objective_1d,
    bounds=(0.0, 1.0),
    method="bounded",
)

print(bounded_result.x)
print(bounded_result.fun)
```

原函数的全局最小点是 `x = 2`，但边界限制为 `[0, 1]`，所以最优点会落在右边界附近。

## 多维最小化：minimize

多维优化使用 `optimize.minimize`。目标函数接收一维数组，返回一个标量。

```python
def objective_2d(x):
    return (x[0] - 1.0) ** 2 + (x[1] + 2.0) ** 2

x0 = np.array([0.0, 0.0])

result = optimize.minimize(objective_2d, x0=x0, method="BFGS")

print(result.x)
print(result.fun)
print(result.success)
```

这里理论最优点是 `[1, -2]`。

`x0` 是初始点。很多优化算法对初始点敏感，尤其是非凸问题。不同初始点可能收敛到不同局部最优。

## 提供梯度

如果能写出梯度，可以传给 `jac`，通常能提高速度和稳定性。

```python
def objective_with_grad(x):
    value = (x[0] - 1.0) ** 2 + (x[1] + 2.0) ** 2
    grad = np.array([
        2.0 * (x[0] - 1.0),
        2.0 * (x[1] + 2.0),
    ])
    return value, grad

grad_result = optimize.minimize(
    objective_with_grad,
    x0=np.array([0.0, 0.0]),
    method="BFGS",
    jac=True,
)

print(grad_result.x)
print(grad_result.jac)
```

`jac=True` 表示目标函数同时返回 `(value, gradient)`。

如果梯度写错，优化器可能比不用梯度更糟。实战中可以用有限差分检查梯度，或者先跑无梯度版本做对照。

## bounds：变量边界

边界约束表示每个变量的取值范围。

```python
bounds = [
    (0.0, None),   # x[0] >= 0
    (-1.0, 1.0),  # -1 <= x[1] <= 1
]

bounded_2d = optimize.minimize(
    objective_2d,
    x0=np.array([0.0, 0.0]),
    method="L-BFGS-B",
    bounds=bounds,
)

print(bounded_2d.x)
print(bounded_2d.fun)
```

无约束最优点是 `[1, -2]`，但第二个变量最低只能到 `-1`，所以带边界的最优点会变成 `[1, -1]`。

## args：给目标函数传额外参数

目标函数通常依赖数据或参数。可以通过 `args` 传入。

```python
def ridge_objective(beta, x, y, alpha):
    prediction = x @ beta
    residual = prediction - y
    return np.mean(residual ** 2) + alpha * np.sum(beta ** 2)

x_data = np.array([
    [1.0, 0.0],
    [1.0, 1.0],
    [1.0, 2.0],
    [1.0, 3.0],
])
y_data = np.array([1.0, 2.0, 2.9, 4.1])
alpha = 0.1

ridge_result = optimize.minimize(
    ridge_objective,
    x0=np.zeros(2),
    args=(x_data, y_data, alpha),
    method="BFGS",
)

print(ridge_result.x)
print(ridge_result.fun)
```

这里 `beta` 是优化变量，`x_data`、`y_data`、`alpha` 是固定输入。

如果目标函数闭包里引用很多外部变量，调试会变难。显式使用 `args` 更容易看清楚谁是变量，谁是数据。

## 约束优化：SLSQP

约束优化常用于组合权重、风险预算、参数限制等问题。

下面做一个最小方差组合：

```python
cov = np.array([
    [0.0400, 0.0060, 0.0040],
    [0.0060, 0.0225, 0.0030],
    [0.0040, 0.0030, 0.0100],
])

assets = pd.Index(["AAA", "BBB", "CCC"], name="asset")

def portfolio_variance(w, cov):
    return float(w @ cov @ w)

constraints = [
    {
        "type": "eq",
        "fun": lambda w: np.sum(w) - 1.0,
    },
]

bounds = [(0.0, 1.0)] * len(assets)
x0 = np.repeat(1.0 / len(assets), len(assets))

portfolio_result = optimize.minimize(
    portfolio_variance,
    x0=x0,
    args=(cov,),
    method="SLSQP",
    bounds=bounds,
    constraints=constraints,
)

weights = pd.Series(portfolio_result.x, index=assets, name="weight")

print(portfolio_result.success)
print(weights)
print(weights.sum())
print(portfolio_result.fun)
```

这里的约束含义是：

- `sum(w) - 1 = 0`：权重之和必须等于 1。
- `0 <= w_i <= 1`：不允许做空，也不允许单个权重超过 100%。

SLSQP 支持等式约束和不等式约束。SciPy 约定：

- `type="eq"`：约束函数结果必须等于 0。
- `type="ineq"`：约束函数结果必须大于等于 0。

## 加入不等式约束

假设还希望组合预期收益至少达到某个目标，可以添加不等式约束。

```python
expected_return = np.array([0.06, 0.05, 0.03])
target_return = 0.045

constraints_with_return = [
    {
        "type": "eq",
        "fun": lambda w: np.sum(w) - 1.0,
    },
    {
        "type": "ineq",
        "fun": lambda w: w @ expected_return - target_return,
    },
]

target_result = optimize.minimize(
    portfolio_variance,
    x0=x0,
    args=(cov,),
    method="SLSQP",
    bounds=bounds,
    constraints=constraints_with_return,
)

target_weights = pd.Series(target_result.x, index=assets, name="weight")

print(target_result.success)
print(target_weights)
print(target_weights @ expected_return)
```

不等式函数写成 `组合收益 - 目标收益`，是因为 SLSQP 要求它大于等于 0。

如果你写反成 `target_return - w @ expected_return`，含义就变成“组合收益不超过目标收益”。

## 局部最优和初始点

很多目标函数不是凸函数，优化器可能只找到局部最优。

```python
def nonconvex_1d(x):
    z = x[0]
    return np.sin(5.0 * z) + 0.1 * z ** 2

starts = [-2.0, 0.0, 2.0]
solutions = []

for start in starts:
    res = optimize.minimize(nonconvex_1d, x0=np.array([start]), method="BFGS")
    solutions.append((start, res.x[0], res.fun, res.success))

solutions_df = pd.DataFrame(
    solutions,
    columns=["start", "x_opt", "objective", "success"],
)

print(solutions_df)
```

不同初始点可能得到不同解。遇到非凸问题，可以多试几个初始点，或者使用更适合全局搜索的工具。本节先掌握局部优化的基本接口。

## 一元方程求根：root_scalar

如果目标是解方程 `f(x) = 0`，不一定要把它改写成最小化问题。

例如求 `sqrt(2)`：

```python
def equation_1d(x):
    return x ** 2 - 2.0

root_result = optimize.root_scalar(
    equation_1d,
    bracket=[0.0, 2.0],
    method="brentq",
)

print(root_result.root)
print(root_result.converged)
print(equation_1d(root_result.root))
```

`brentq` 需要给出一个 bracket，且函数在区间两端符号相反。

```python
print(equation_1d(0.0))
print(equation_1d(2.0))
```

如果区间两端没有夹住根，`brentq` 会失败。

## 多元方程组求根：root

多元方程组可以用 `optimize.root`。

下面求解：

```text
x + y = 3
x^2 + y^2 = 5
```

```python
def system_equations(v):
    x, y = v
    return np.array([
        x + y - 3.0,
        x ** 2 + y ** 2 - 5.0,
    ])

system_result = optimize.root(
    system_equations,
    x0=np.array([0.5, 2.5]),
)

print(system_result.x)
print(system_result.success)
print(system_equations(system_result.x))
```

这个方程组有两个解：`[1, 2]` 和 `[2, 1]`。初始点会影响收敛到哪个解。

```python
system_result_2 = optimize.root(
    system_equations,
    x0=np.array([2.5, 0.5]),
)

print(system_result_2.x)
```

求根同样要检查残差是否足够接近 0，而不是只看 `success`。

## 选择 minimize 还是 root

如果问题本质是“让某个标量目标尽量小”，用 `minimize`。

```text
minimize portfolio_variance(w)
```

如果问题本质是“让方程等于 0”，用 `root` 或 `root_scalar`。

```text
find x such that x^2 - 2 = 0
```

当然也可以最小化平方残差：

```python
def squared_residual(x):
    return equation_1d(x[0]) ** 2

minimize_root = optimize.minimize(
    squared_residual,
    x0=np.array([1.0]),
    method="BFGS",
)

print(minimize_root.x)
print(equation_1d(minimize_root.x[0]))
```

但如果有稳定的求根接口，直接使用 `root_scalar` 或 `root` 通常更清楚。

## 常见坑

第一，目标函数返回了数组而不是标量。

```python
# 不推荐：返回 residual 向量，不是标量
# def bad_objective(beta):
#     return x_data @ beta - y_data
```

`minimize` 的目标函数应返回一个标量。如果要拟合残差，可以返回平方误差和，或者使用专门的最小二乘接口。

第二，不检查 `success` 和 `message`。

```python
res = optimize.minimize(objective_2d, x0=np.array([0.0, 0.0]))

print(res.success)
print(res.message)
```

失败的优化结果也会有 `x`，不能直接当作可用解。

第三，变量尺度差太大。

如果一个变量量级是 `1e-6`，另一个是 `1e6`，优化器可能很难搜索。可以考虑标准化变量或重参数化。

第四，约束函数符号写反。

SLSQP 的不等式约束要求 `fun(x) >= 0`。目标收益约束应写成：

```python
# w @ expected_return - target_return >= 0
```

第五，把局部优化当成全局最优保证。

`minimize` 常用算法多数是局部优化方法。非凸问题需要多初始点、全局优化方法或额外问题结构分析。

## 实战提示

每次使用 `scipy.optimize`，建议按这个清单检查：

1. 优化变量 `x` 的 shape 是什么？
2. 目标函数是否返回标量？
3. 初始点是否可行？
4. bounds 和 constraints 是否表达了真实业务限制？
5. 是否检查了 `success`、`message`、目标函数值和约束残差？

例如组合优化完成后，不只看权重，还要检查：

```python
assert portfolio_result.success
assert np.isclose(weights.sum(), 1.0)
assert (weights >= -1e-10).all()
assert (weights <= 1.0 + 1e-10).all()
```

求根完成后，应检查：

```python
assert root_result.converged
assert abs(equation_1d(root_result.root)) < 1e-10
```

数值优化的结果要靠这些检查建立可信度。

## 小结

`scipy.optimize` 的核心接口可以先掌握这几个：

- `minimize_scalar`：一维标量最小化。
- `minimize`：多维目标函数最小化。
- `bounds`：变量边界。
- `constraints`：等式和不等式约束。
- `root_scalar`：一元方程求根。
- `root`：多元方程组求根。

优化代码最重要的不是把函数调用跑通，而是明确目标函数、变量、约束、初始点和结果检查。

## 自检问题

1. `minimize` 的目标函数为什么必须返回标量？
2. `OptimizeResult` 里至少应该检查哪些字段？
3. SLSQP 中 `type="ineq"` 的约束函数符号规则是什么？
4. 为什么非凸问题可能需要多个初始点？
5. 什么情况下应该用 `root_scalar` 或 `root`，而不是把问题改写成平方残差最小化？
