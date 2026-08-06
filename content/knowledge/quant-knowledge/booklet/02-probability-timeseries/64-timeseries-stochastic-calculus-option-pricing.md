# 64. 时间序列：基础随机微积分与期权定价思想

## 核心概念

随机微积分是研究随机过程如何随时间演化的工具。金融里最常见的起点是布朗运动、随机微分方程和伊藤引理。

期权定价思想的核心是：

```text
在无套利市场中，用可交易资产复制衍生品现金流，或在风险中性测度下取贴现期望。
```

本节不追求严格数学证明，而是建立面试和量化研究常用直觉：

- 布朗运动是连续时间随机冲击的基本模型。
- 几何布朗运动 GBM 是 Black-Scholes 股票价格模型的基础。
- 伊藤引理告诉我们非线性函数的随机微分会多出二阶修正项。
- 期权价格可以理解为风险中性世界下未来 payoff 的贴现期望。

## 布朗运动

标准布朗运动 `W_t` 满足：

```text
W_0 = 0
W_t - W_s ~ N(0, t - s)
不同时间区间的增量相互独立
路径连续但几乎处处不可微
```

离散模拟时，用小时间步 `dt` 近似：

```text
dW_t = sqrt(dt) * epsilon_t
epsilon_t ~ N(0, 1)
```

## 准备环境

```python
import math
import numpy as np
import pandas as pd
```

模拟一年内的布朗运动路径：

```python
rng = np.random.default_rng(64)

n_paths = 20_000
n_steps = 252
T = 1.0
dt = T / n_steps

increments = rng.normal(
    loc=0.0,
    scale=math.sqrt(dt),
    size=(n_steps, n_paths),
)

brownian_paths = np.vstack([
    np.zeros(n_paths),
    increments.cumsum(axis=0),
])

time_grid = np.linspace(0.0, T, n_steps + 1)

terminal_w = brownian_paths[-1]

print(terminal_w.mean())
print(terminal_w.var(ddof=1))
```

理论上 `W_1 ~ N(0, 1)`，所以终值均值应接近 `0`，方差应接近 `1`。

## 几何布朗运动 GBM

Black-Scholes 模型中，股票价格常写作：

```text
dS_t = mu S_t dt + sigma S_t dW_t
```

其中：

- `mu`：漂移率。
- `sigma`：波动率。
- `dW_t`：布朗运动冲击。

这个随机微分方程的解是：

```text
S_t = S_0 * exp((mu - 0.5 * sigma^2) * t + sigma * W_t)
```

注意指数里的 `-0.5 * sigma^2`，这就是伊藤修正带来的项。

代码模拟：

```python
S0 = 100.0
mu = 0.08
sigma = 0.20

stock_paths = S0 * np.exp(
    (mu - 0.5 * sigma ** 2) * time_grid[:, None]
    + sigma * brownian_paths
)

terminal_stock = stock_paths[-1]

print(terminal_stock.mean())
print(S0 * math.exp(mu * T))
```

理论上：

```text
E[S_T] = S_0 * exp(mu T)
```

模拟均值应接近这个理论值。

## 为什么 log return 的漂移不是 mu

对 GBM 取对数：

```text
log(S_t) = log(S_0) + (mu - 0.5 sigma^2)t + sigma W_t
```

所以对数收益的漂移是：

```text
mu - 0.5 sigma^2
```

代码验证：

```python
log_stock = np.log(stock_paths)
mean_log_increment = np.diff(log_stock, axis=0).mean()
estimated_log_drift = mean_log_increment / dt

print(estimated_log_drift)
print(mu - 0.5 * sigma ** 2)
```

这是很多人第一次学随机微积分时最容易混淆的地方：

- `S_t` 的期望增长率对应 `mu`。
- `log(S_t)` 的漂移是 `mu - 0.5 sigma^2`。

原因是指数函数是非线性的，波动会改变均值关系。

## 伊藤引理的直觉

普通微积分里，如果 `X = f(W)`，会写：

```text
dX = f'(W) dW
```

但随机微积分里，布朗运动增量满足：

```text
(dW)^2 约等于 dt
```

因此伊藤引理多出二阶项：

```text
df(W_t) = f'(W_t)dW_t + 0.5 f''(W_t)dt
```

例如 `f(W) = W^2`：

```text
d(W_t^2) = 2 W_t dW_t + dt
```

用一条路径离散验证：

```python
one_w = brownian_paths[:, 0]
one_dw = np.diff(one_w)

ito_rhs = np.sum(2 * one_w[:-1] * one_dw + dt)
direct_value = one_w[-1] ** 2

print(direct_value)
print(ito_rhs)
```

离散步长有限时二者不会完全相等，但会比较接近。步长越细，近似越好。

这里的 `+ dt` 就是伊藤修正项；如果漏掉它，长期会系统性偏差。

## 风险中性定价思想

现实世界下股票漂移是 `mu`。但在无套利期权定价中，常在风险中性测度下把股票过程写成：

```text
dS_t = r S_t dt + sigma S_t dW_t^Q
```

其中 `r` 是无风险利率。

欧式看涨期权 payoff：

```text
payoff = max(S_T - K, 0)
```

风险中性定价：

```text
call_price = exp(-rT) * E_Q[max(S_T - K, 0)]
```

这不表示现实中股票期望收益就是 `r`。它表示在用于无套利定价的风险中性世界里，贴现资产价格是鞅。

## Black-Scholes 公式

欧式看涨期权价格：

```text
C = S N(d1) - K exp(-rT) N(d2)

d1 = [log(S/K) + (r + 0.5 sigma^2)T] / [sigma sqrt(T)]
d2 = d1 - sigma sqrt(T)
```

用 Python 实现标准正态分布函数：

```python
def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def black_scholes_call(spot, strike, rate, vol, maturity):
    d1 = (
        math.log(spot / strike)
        + (rate + 0.5 * vol ** 2) * maturity
    ) / (vol * math.sqrt(maturity))

    d2 = d1 - vol * math.sqrt(maturity)

    return (
        spot * norm_cdf(d1)
        - strike * math.exp(-rate * maturity) * norm_cdf(d2)
    )


spot = 100.0
strike = 100.0
rate = 0.03
vol = 0.20
maturity = 1.0

bs_call = black_scholes_call(spot, strike, rate, vol, maturity)

print(bs_call)
```

这给出 Black-Scholes 假设下的欧式看涨期权理论价格。

## Monte Carlo 定价

同一个看涨期权也可以用风险中性模拟定价：

```python
n_mc = 200_000

z = rng.normal(size=n_mc)
risk_neutral_terminal = spot * np.exp(
    (rate - 0.5 * vol ** 2) * maturity
    + vol * math.sqrt(maturity) * z
)

payoff = np.maximum(risk_neutral_terminal - strike, 0.0)
mc_call = math.exp(-rate * maturity) * payoff.mean()

print(mc_call)
print(bs_call)
```

Monte Carlo 价格应接近 Black-Scholes 公式价格。路径数越多，误差通常越小。

Monte Carlo 的优势是灵活：

- 可以处理路径依赖期权。
- 可以加入复杂 payoff。
- 可以模拟多个风险因子。

缺点是有抽样误差，且 Greeks 计算更复杂。

## Delta hedge 的思想

Black-Scholes 推导的一个核心直觉是动态复制。

期权价格 `V(S, t)` 对股票价格的敏感度是：

```text
Delta = partial V / partial S
```

如果持有一个期权，同时卖出 `Delta` 份股票，就能在一个很短时间内抵消股票价格的一阶随机冲击。

剩下的无风险组合应该赚无风险利率，否则存在套利。

这就是 Black-Scholes PDE 的直觉来源：

```text
V_t + 0.5 sigma^2 S^2 V_SS + r S V_S - r V = 0
```

面试中不一定要求完整推导，但要理解：

- `V_S` 是 Delta。
- `V_SS` 是 Gamma。
- 伊藤引理产生 `0.5 sigma^2 S^2 V_SS` 这一项。
- 无套利复制把期权定价问题变成 PDE 或风险中性期望。

## 常见坑

第一，把现实漂移 `mu` 用进无套利期权定价。

Black-Scholes 定价公式使用风险中性漂移 `r`，不是现实世界预期收益 `mu`。

第二，忘记伊藤修正项。

GBM 的显式解里是 `(mu - 0.5 sigma^2)t`，不是 `mu t`。

第三，把 `dW` 当普通微小量。

布朗运动中 `(dW)^2` 是 `dt` 量级，这正是伊藤微积分和普通微积分不同的地方。

第四，认为 Black-Scholes 是真实市场完整模型。

真实市场有波动率微笑、跳跃、交易成本、离散对冲、随机波动率和流动性约束。

第五，忽略 payoff 类型。

欧式期权可以直接用终值 payoff；美式、障碍、亚式等期权可能需要动态规划、树模型、PDE 或路径模拟。

## 实战提示

学习随机微积分和期权定价时可以按下面路线：

1. 先掌握布朗运动增量 `dW ~ N(0, dt)`。
2. 理解 GBM：`dS = mu S dt + sigma S dW`。
3. 记住 `log(S)` 漂移是 `mu - 0.5 sigma^2`。
4. 用 `f(W)=W^2` 理解伊藤引理的二阶项。
5. 区分现实测度和风险中性测度。
6. 用风险中性贴现期望理解欧式期权定价。
7. 用 Delta hedge 理解无套利复制。
8. 再扩展到波动率微笑、局部波动率、随机波动率和跳跃模型。

## 小结

本节的重点：

- 布朗运动增量服从 `N(0, dt)`，且独立增量。
- GBM 是 Black-Scholes 股票价格模型的基础。
- `S_t` 的期望增长率是 `mu`，`log(S_t)` 的漂移是 `mu - 0.5 sigma^2`。
- 伊藤引理多出 `0.5 f'' dt` 二阶修正项。
- 风险中性定价使用漂移 `r`，不是现实漂移 `mu`。
- 欧式期权价格可以看成贴现后的风险中性 payoff 期望。
- Black-Scholes 公式和 Monte Carlo 定价应给出相近结果。

## 自检问题

1. 标准布朗运动的增量有什么分布性质？
2. GBM 的显式解为什么有 `-0.5 sigma^2`？
3. 为什么 `d(W_t^2)` 不是简单的 `2W_t dW_t`？
4. 风险中性定价为什么使用 `r` 而不是现实漂移 `mu`？
5. Black-Scholes 公式中的 `d1` 和 `d2` 分别如何进入看涨期权价格？
6. Delta hedge 和伊藤引理在 Black-Scholes 推导中分别起什么作用？
