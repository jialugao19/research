# 21. scipy.stats：分布、概率密度、分位数与随机变量

## 核心概念

`scipy.stats` 提供大量概率分布和统计函数。它最常用的一组接口是：

- `pdf`：连续分布的概率密度函数。
- `pmf`：离散分布的概率质量函数。
- `cdf`：累积分布函数，计算 `P(X <= x)`。
- `ppf`：分位数函数，计算满足 `P(X <= x) = q` 的 `x`。
- `sf`：生存函数，计算 `P(X > x)`，也就是 `1 - cdf(x)`。
- `rvs`：随机抽样。
- `mean`、`var`、`std`：理论均值、方差、标准差。

`scipy.stats` 的分布函数通常支持 NumPy 数组输入，并返回 NumPy 数组。它适合做理论分布计算、概率阈值、模拟抽样和简单参数估计。

## 准备环境

```python
import numpy as np
import pandas as pd
from scipy import stats

rng = np.random.default_rng(42)
```

后续随机抽样都使用显式随机数生成器，便于复现。

## 连续分布：正态分布

标准正态分布可以通过 `stats.norm` 使用。

```python
x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])

pdf = stats.norm.pdf(x)
cdf = stats.norm.cdf(x)

print(pdf)
print(cdf)
```

`pdf` 是密度，不是概率。对于连续变量，单点概率 `P(X = x)` 是 0；区间概率要通过 `cdf` 的差来算。

```python
prob_between = stats.norm.cdf(1.0) - stats.norm.cdf(-1.0)

print(prob_between)
```

这表示标准正态落在 `[-1, 1]` 之间的概率。

## ppf：从概率到分位数

`cdf` 是从取值到概率；`ppf` 是从概率到取值。

```python
q = np.array([0.025, 0.5, 0.975])
z = stats.norm.ppf(q)

print(z)
print(stats.norm.cdf(z))
```

输出的 `z` 约等于 `[-1.96, 0, 1.96]`。这就是标准正态 95% 区间常见临界值的来源。

## loc 和 scale

很多连续分布都有 `loc` 和 `scale` 参数。对正态分布：

- `loc` 是均值。
- `scale` 是标准差，必须为正。

```python
mu = 0.001
sigma = 0.02

daily_return_dist = stats.norm(loc=mu, scale=sigma)

print(daily_return_dist.mean())
print(daily_return_dist.std())
print(daily_return_dist.ppf(0.05))
```

`daily_return_dist.ppf(0.05)` 是左侧 5% 分位数。如果把收益视作正态分布，这是一个简单的 5% 分位收益。

注意：不同领域对 VaR 的符号约定不同。有的写成负收益分位数，有的写成正的损失金额。写代码时应明确列名和符号。

## frozen distribution：冻结随机变量

上面的 `daily_return_dist` 是一个“冻结分布对象”。它把参数固定住，之后可以直接调用方法。

```python
loss_threshold = -0.03
gain_threshold = 0.03

prob_large_loss = daily_return_dist.cdf(loss_threshold)
prob_large_gain = daily_return_dist.sf(gain_threshold)

print(prob_large_loss)
print(prob_large_gain)
```

这里：

- `cdf(-0.03)` 表示 `P(return <= -3%)`。
- `sf(0.03)` 表示 `P(return > 3%)`。

对尾部概率，优先使用 `sf(x)`，而不是 `1 - cdf(x)`。在极端尾部，`sf` 通常有更好的数值稳定性。

## logpdf：避免极小数下溢

密度很小时，直接连乘可能下溢。更常见的做法是使用 log 密度并求和。

```python
sample_returns = np.array([0.010, -0.005, 0.002, 0.018])

log_density = daily_return_dist.logpdf(sample_returns)
total_log_likelihood = log_density.sum()

print(log_density)
print(total_log_likelihood)
```

这在最大似然估计和模型比较里很常见。不要把很多很小的 `pdf` 值直接相乘。

## 随机抽样：rvs

`rvs` 用来从理论分布里抽样。

```python
draws = daily_return_dist.rvs(size=5, random_state=rng)

print(draws)
```

`random_state=rng` 让结果可复现。需要二维样本时可以传入 shape：

```python
panel_draws = daily_return_dist.rvs(size=(3, 2), random_state=rng)

draws_df = pd.DataFrame(
    panel_draws,
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
    columns=["AAA", "BBB"],
)

print(draws_df)
```

SciPy 返回的是数组；如果需要日期和资产标签，要自己包回 pandas。

## 离散分布：二项分布

离散分布使用 `pmf`，不是 `pdf`。

假设一次交易有 55% 概率盈利，10 次交易里盈利次数 `K` 可以用二项分布描述：

```python
n = 10
p = 0.55
k = np.arange(0, n + 1)

win_count_dist = stats.binom(n=n, p=p)
pmf = win_count_dist.pmf(k)
cdf = win_count_dist.cdf(k)

print(pmf)
print(cdf)
print(pmf.sum())
```

`pmf[k]` 表示刚好盈利 `k` 次的概率。

计算至少盈利 7 次：

```python
prob_at_least_7 = win_count_dist.sf(6)

print(prob_at_least_7)
```

`sf(6)` 表示 `P(K > 6)`，也就是 `P(K >= 7)`。

离散分布也有 `ppf`：

```python
median_win_count = win_count_dist.ppf(0.5)

print(median_win_count)
```

离散分布的 `ppf` 返回的是使 `cdf(k) >= q` 的最小取值。

## 离散分布：泊松分布

泊松分布常用于计数数据，例如某段时间内订单到达次数、交易笔数、事件次数。

```python
lam = 3.0
order_count_dist = stats.poisson(mu=lam)

counts = np.arange(0, 10)
count_probs = order_count_dist.pmf(counts)

print(count_probs)
print(order_count_dist.mean())
print(order_count_dist.var())
```

泊松分布的均值和方差都等于 `lambda`。

```python
prob_more_than_5 = order_count_dist.sf(5)

print(prob_more_than_5)
```

这表示一个时间窗口里订单数大于 5 的概率。

## t 分布：厚尾直觉

金融收益经常有厚尾。t 分布比正态分布有更厚的尾部，`df` 是自由度。

```python
x = np.linspace(-4.0, 4.0, 9)

normal_pdf = stats.norm.pdf(x)
t_pdf = stats.t.pdf(x, df=3)

comparison = pd.DataFrame({
    "x": x,
    "normal_pdf": normal_pdf,
    "t_df3_pdf": t_pdf,
})

print(comparison)
```

在远离 0 的位置，低自由度 t 分布通常给尾部更高密度。它是理解厚尾风险的基础工具之一。

比较左右 2.5% 分位数：

```python
normal_975 = stats.norm.ppf(0.975)
t_975 = stats.t.ppf(0.975, df=3)

print(normal_975)
print(t_975)
```

同样是 97.5% 分位数，t 分布的临界值更大，反映尾部更厚。

## 理论分布 vs 经验分布

`stats.norm.ppf(0.05, loc=mu, scale=sigma)` 是理论分布分位数；`np.quantile(sample, 0.05)` 是样本经验分位数。

```python
sample = daily_return_dist.rvs(size=1000, random_state=rng)

theoretical_q05 = daily_return_dist.ppf(0.05)
empirical_q05 = np.quantile(sample, 0.05)

print(theoretical_q05)
print(empirical_q05)
```

样本分位数会随抽样变化。样本越小，经验分位数越不稳定。

```python
small_sample = daily_return_dist.rvs(size=20, random_state=rng)
small_empirical_q05 = np.quantile(small_sample, 0.05)

print(small_empirical_q05)
```

实务中要区分“假设收益服从某个分布后得到的理论分位数”和“直接从历史样本估出来的经验分位数”。

## 参数估计：fit

`fit` 可以用样本估计分布参数。

```python
observed = np.array([0.010, -0.004, 0.006, 0.002, -0.008, 0.014])

fit_mu, fit_sigma = stats.norm.fit(observed)

print(fit_mu)
print(fit_sigma)
```

对正态分布，`fit` 返回估计的 `loc` 和 `scale`。这不代表“数据真的服从正态分布”，只是把正态分布参数拟合到这组样本上。

拟合后可以生成一个冻结分布：

```python
fitted_dist = stats.norm(loc=fit_mu, scale=fit_sigma)

print(fitted_dist.ppf(0.05))
print(fitted_dist.cdf(0.0))
```

样本很少时，拟合参数会非常不稳定。不要把 `fit` 当作分布假设检验。

## 向量化参数

SciPy 分布函数支持广播。可以一次计算多个均值、多个阈值下的概率。

```python
means = np.array([0.000, 0.001, 0.002])
sigmas = np.array([0.010, 0.020, 0.030])
threshold = -0.02

tail_probs = stats.norm.cdf(threshold, loc=means, scale=sigmas)

print(tail_probs)
```

这等价于分别计算三组正态分布下 `P(X <= -2%)`。

如果要保留标签，可以手动包回 Series：

```python
assets = pd.Index(["AAA", "BBB", "CCC"], name="asset")
tail_prob_series = pd.Series(tail_probs, index=assets, name="prob_return_le_minus_2pct")

print(tail_prob_series)
```

## 常见坑

第一，把 `pdf` 当成概率。

连续分布的 `pdf(x)` 是密度，不是 `P(X = x)`。区间概率应使用 `cdf(b) - cdf(a)`。

第二，混淆 `cdf` 和 `sf`。

```python
right_tail = stats.norm.sf(2.0)
left_tail = stats.norm.cdf(-2.0)

print(right_tail)
print(left_tail)
```

`cdf(x)` 是左尾概率，`sf(x)` 是右尾概率。

第三，忘记 `scale` 是标准差，不是方差。

```python
# 正确：标准差为 0.02
dist = stats.norm(loc=0.0, scale=0.02)
```

如果把方差传给 `scale`，分布会被错误地压得非常窄。

第四，用理论分布掩盖样本事实。

拟合出正态参数后，还应检查样本分布、极端值和业务机制。分布函数是工具，不是保证。

第五，随机抽样不设置随机数来源。

```python
rng = np.random.default_rng(42)
draws = stats.norm.rvs(size=3, random_state=rng)
```

研究代码里显式传入随机数生成器，结果更容易复现。

## 实战提示

使用 `scipy.stats` 时，可以按这个顺序思考：

1. 变量是连续还是离散？
2. 你需要密度、累计概率、分位数，还是随机抽样？
3. 参数的含义是什么，尤其是 `loc`、`scale`、`df`、`n`、`p`、`mu`？
4. 返回值是否需要恢复 pandas 标签？
5. 结果是理论分布下的计算，还是样本经验统计？

一段常见的风险阈值计算可以这样写：

```python
returns = pd.Series([0.010, -0.004, 0.006, 0.002, -0.008, 0.014])

mu, sigma = stats.norm.fit(returns.to_numpy(dtype=float))
dist = stats.norm(loc=mu, scale=sigma)

left_5pct_return = dist.ppf(0.05)
prob_loss_more_than_1pct = dist.cdf(-0.01)

print(left_5pct_return)
print(prob_loss_more_than_1pct)
```

这段代码的解释应是：“在正态分布假设下，用样本估计参数后得到的理论左尾概率”。它不是历史回测，也不是分布假设的证明。

## 小结

`scipy.stats` 的核心是分布对象和统一接口：

- 连续分布用 `pdf`，离散分布用 `pmf`。
- `cdf` 计算左尾累计概率，`sf` 计算右尾概率。
- `ppf` 把概率转换成分位数。
- `rvs` 用于模拟抽样，建议传入 `random_state`。
- `fit` 可以估计参数，但不证明分布假设正确。

掌握这些接口后，很多概率阈值、风险分位数和模拟问题都可以用统一方式表达。

## 自检问题

1. 连续分布里的 `pdf(x)` 为什么不是 `P(X = x)`？
2. `cdf`、`sf`、`ppf` 分别回答什么问题？
3. 正态分布的 `loc` 和 `scale` 分别是什么含义？
4. 二项分布为什么用 `pmf` 而不是 `pdf`？
5. 理论分位数和样本经验分位数有什么区别？
