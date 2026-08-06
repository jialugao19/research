# 时间序列：cointegration 协整、检验、价差建模与配对交易风险

## 核心概念

cointegration 协整描述多个非平稳序列之间的长期均衡关系。

两个价格序列 `x_t` 和 `y_t` 可能各自是非平稳的随机游走，但存在某个线性组合是平稳的：

```text
spread_t = y_t - alpha - beta x_t
```

如果 `spread_t` 是平稳的，就说 `y_t` 和 `x_t` 存在协整关系。

直觉上：

```text
价格可以一起漂移，但它们之间的价差不会无限发散。
```

这和相关性不同。相关性只衡量同涨同跌；协整强调长期均衡误差是否会回归。

## 协整回答的问题

协整常用于回答：

- 两个价格序列是否有稳定长期关系？
- 它们的价差是否可能均值回复？
- hedge ratio 应该如何估计？
- pairs trading 的价差信号是否有统计基础？

但协整不保证策略赚钱。

即使价差平稳，也还要考虑：

- 均值回复速度。
- 交易成本。
- 做空约束。
- borrow fee。
- 结构变化。
- 拥挤交易。
- 极端行情下价差断裂。

## 准备环境

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
```

构造一组协整价格：

```python
rng = np.random.default_rng(69)

n_obs = 700
dates = pd.bdate_range("2022-01-03", periods=n_obs)

x = pd.Series(
    100 + np.cumsum(rng.normal(loc=0.03, scale=1.0, size=n_obs)),
    index=dates,
    name="x",
)

spread_values = np.zeros(n_obs)
spread_noise = rng.normal(loc=0.0, scale=0.8, size=n_obs)

for t in range(1, n_obs):
    spread_values[t] = 0.82 * spread_values[t - 1] + spread_noise[t]

y = pd.Series(
    12 + 1.35 * x.to_numpy() + spread_values,
    index=dates,
    name="y",
)
```

这里：

- `x` 是非平稳价格。
- `y` 跟随 `x` 的共同趋势。
- `spread_values` 是平稳价差。

真实市场里我们不知道真实 `beta=1.35`，需要估计。

## 先检查单序列平稳性

用 ADF 检验：

```python
adf_x = adfuller(x)
adf_y = adfuller(y)

print(adf_x[1])
print(adf_y[1])
```

ADF 原假设是存在单位根，即非平稳。

如果 `x` 和 `y` 的 p-value 都较大，说明不能拒绝它们各自非平稳。

协整检验的典型前提就是：

```text
单个价格序列非平稳，但某个线性组合平稳。
```

如果序列本来就平稳，问题就不是协整，而是普通价差或均值回复建模。

## 估计 hedge ratio

用 OLS 估计：

```text
y_t = alpha + beta x_t + error_t
```

```python
X = sm.add_constant(x)
ols_result = sm.OLS(y, X).fit()

alpha_hat = ols_result.params["const"]
beta_hat = ols_result.params["x"]

estimated_spread = y - (alpha_hat + beta_hat * x)

print(alpha_hat)
print(beta_hat)
print(estimated_spread.head())
```

`beta_hat` 可以解释为 hedge ratio。

如果做多一单位 `y`，为了构造价差组合，可能需要做空 `beta_hat` 单位 `x`。

实际交易还要按合约乘数、价格单位、融资成本和做空约束调整。

## 检查价差平稳性

```python
adf_spread = adfuller(estimated_spread)

print(adf_spread[1])
```

如果价差的 ADF p-value 很小，说明有证据认为价差是平稳的。

这支持“二者有长期均衡关系”的说法。

但注意：

- 这是样本内检验。
- hedge ratio 估计误差会影响结果。
- 价差平稳不代表每次偏离都能盈利。

## Engle-Granger 协整检验

statsmodels 提供 `coint`：

```python
coint_stat, coint_pvalue, coint_crit = coint(y, x)

print(coint_stat)
print(coint_pvalue)
print(coint_crit)
```

如果 `coint_pvalue` 很小，说明有证据认为 `y` 和 `x` 协整。

Engle-Granger 两步法：

1. 用 OLS 估计长期关系。
2. 检查残差是否平稳。

它简单直观，但对变量顺序、结构变化和多变量系统有局限。多变量协整常用 Johansen test。

## 对比非协整随机游走

构造另一个独立随机游走：

```python
z = pd.Series(
    50 + np.cumsum(rng.normal(loc=0.02, scale=1.2, size=n_obs)),
    index=dates,
    name="z",
)

not_coint_pvalue = coint(z, x)[1]

print(not_coint_pvalue)
```

`z` 和 `x` 都可能有趋势，也可能在某段时间看起来相关，但如果没有稳定价差，协整检验不会显著。

这就是为什么 pairs trading 不能只看价格相关性。

## 半衰期 half-life

价差平稳还不够，还要看均值回复速度。

常用近似：

```text
delta_spread_t = a + b * spread_{t-1} + error_t
half_life = -log(2) / b
```

如果 `b < 0`，价差有均值回复倾向。

代码：

```python
lagged_spread = estimated_spread.shift(1).dropna()
delta_spread = estimated_spread.diff().dropna()
lagged_spread = lagged_spread.loc[delta_spread.index]

half_life_model = sm.OLS(
    delta_spread,
    sm.add_constant(lagged_spread),
).fit()

speed = half_life_model.params.iloc[1]
half_life = -np.log(2) / speed

print(speed)
print(half_life)
```

半衰期太短，可能难以覆盖交易成本；半衰期太长，资金占用和回撤压力会变大。

## z-score 信号

配对交易常把价差标准化：

```text
z_t = (spread_t - rolling_mean_t) / rolling_std_t
```

示例：

```python
window = 60

spread_mean = estimated_spread.rolling(window).mean()
spread_std = estimated_spread.rolling(window).std()
zscore = (estimated_spread - spread_mean) / spread_std

position = pd.Series(0.0, index=dates, name="position")
position[zscore > 1.5] = -1.0
position[zscore < -1.5] = 1.0
position[zscore.abs() < 0.2] = 0.0

print(zscore.dropna().head())
print(position.value_counts())
```

解释：

- `zscore > 1.5`：价差偏高，做空价差。
- `zscore < -1.5`：价差偏低，做多价差。
- `abs(zscore) < 0.2`：价差接近均值，平仓。

这只是教学信号，不是完整交易系统。

## 简化价差 PnL

如果 `position=1` 表示做多价差，那么价差上升时盈利。

必须用上一期仓位乘以本期价差变化，避免前视：

```python
spread_change = estimated_spread.diff().fillna(0.0)
spread_pnl = position.shift(1).fillna(0.0) * spread_change

print(spread_pnl.mean())
print(spread_pnl.std(ddof=1))
```

完整回测还需要：

- 交易成本。
- 两腿成交价格。
- 做空成本。
- 保证金和融资。
- beta / dollar 中性约束。
- 停牌、涨跌停和流动性限制。

## 滚动估计和前视问题

上面的 OLS 使用了全样本估计 `beta_hat`，这适合教学，但不能直接用于真实回测。

真实策略中，hedge ratio 必须只用当时之前的数据估计。

伪代码：

```text
for each date t:
    use data from t-lookback to t-1
    estimate alpha_hat and beta_hat
    compute spread_t using current x_t and y_t
    compute zscore_t from historical spread up to t
    generate position for t+1
```

如果用完整样本估计 hedge ratio，再回测历史信号，会有前视偏差。

## 协整失效

协整关系不是永恒的。

常见失效原因：

- 公司基本面变化。
- 指数成分变化。
- 监管、税收或合约规则变化。
- 商品供需结构变化。
- 资金拥挤导致价差持续偏离。
- 一只资产出现停牌、退市或流动性枯竭。

因此要做滚动窗口检验：

```text
rolling coint p-value
rolling hedge ratio
rolling spread volatility
rolling half-life
```

如果这些指标明显漂移，策略应该降权或停止。

## 常见坑

第一，把相关性当协整。

高相关不代表价差平稳。两个随机游走可能长期同向，但价差不断漂移。

第二，用全样本估计 hedge ratio 回测。

这会使用未来信息。交易时只能用当时可见窗口估计。

第三，只看 p-value，不看经济关系。

统计显著的组合如果没有基本面联系，样本外更容易失效。

第四，忽略半衰期和交易成本。

价差会回归，但回归太慢或成本太高，也没有交易价值。

第五，大规模批量检验不做校正。

从几千个资产对里筛协整，总会找到一些假阳性。必须样本外验证。

第六，忽略做空和融资限制。

pairs trading 常需要两腿交易。做空约束和借券成本会显著改变收益。

## 实战提示

做协整研究时可以按下面流程：

1. 先确认资产之间有经济联系。
2. 检查单序列是否是同阶单整，通常是 I(1)。
3. 用 OLS 或 Johansen 方法估计长期关系。
4. 检查残差价差是否平稳。
5. 估计半衰期、价差波动和极端偏离。
6. 用滚动窗口估计 hedge ratio，避免前视。
7. 用上一期信号交易下一期收益。
8. 加入交易成本、做空成本、融资和容量约束。
9. 做样本外、分市场环境和压力期检验。

## 小结

本节的重点：

- 协整表示非平稳序列之间存在平稳线性组合。
- 协整不同于相关性。
- Engle-Granger 方法先估计长期关系，再检验残差平稳。
- hedge ratio 可以用 OLS 估计，但回测中必须滚动估计。
- 半衰期衡量价差均值回复速度。
- z-score 可以构造价差偏离信号，但必须避免前视。
- 协整关系会失效，必须做滚动检验和样本外验证。

## 自检问题

1. 协整和相关性的区别是什么？
2. 为什么两个价格各自非平稳，价差却可能平稳？
3. Engle-Granger 两步法做了哪两件事？
4. hedge ratio 在配对交易中起什么作用？
5. 为什么全样本估计 hedge ratio 会导致前视偏差？
6. 半衰期太长或太短分别有什么交易问题？
