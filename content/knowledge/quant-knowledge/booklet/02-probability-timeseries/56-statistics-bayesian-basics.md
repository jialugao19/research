# 概率统计：Bayesian basics 先验、似然、后验与贝叶斯更新直觉

## 核心概念

贝叶斯统计的核心是用数据更新信念。

最基本公式是 Bayes rule：

```text
posterior ∝ likelihood × prior
```

完整写法：

```text
P(theta | data) = P(data | theta) P(theta) / P(data)
```

其中：

- `theta`：未知参数，例如胜率、均值、波动率。
- `prior`：看到当前数据前，对 `theta` 的信念。
- `likelihood`：给定 `theta` 时，当前数据出现的概率。
- `posterior`：看到数据后，对 `theta` 的更新信念。
- `P(data)`：归一化常数，让后验分布积分为 1。

频率学派通常把参数看作固定未知量，把数据看作随机样本。

贝叶斯方法把参数也当成不确定量，用概率分布表达这种不确定性。

## 准备环境

```python
import numpy as np
import pandas as pd
import math

from scipy.special import betaln
from scipy.stats import beta as beta_dist
from scipy.stats import norm
```

本节用两个共轭例子：

- Beta-Binomial：估计胜率。
- Normal-Normal：估计均值。

共轭的意思是：先验和后验属于同一类分布，更新公式有闭式解。

## Beta-Binomial：估计胜率

假设一个策略每天只有两种结果：

- win：当天收益为正。
- loss：当天收益不为正。

想估计真实胜率 `p`。

如果 `p` 未知，可以给它一个 Beta 先验：

```text
p ~ Beta(a, b)
```

Beta 分布常用于表示 0 到 1 之间的概率。

```python
prior_a = 2.0
prior_b = 2.0

prior_mean = prior_a / (prior_a + prior_b)

print(prior_mean)
```

`Beta(2, 2)` 是一个温和的中性先验，均值是 0.5。它可以理解成“先验上像是见过 2 次 win 和 2 次 loss”，但这只是直觉，不是必须严格当作真实样本。

## 观察数据后更新

假设观察到：

```python
wins = 58
losses = 42
```

Binomial likelihood 是：

```text
P(data | p) ∝ p^wins (1 - p)^losses
```

Beta 先验和 Binomial likelihood 共轭，因此后验仍然是 Beta：

```text
p | data ~ Beta(a + wins, b + losses)
```

```python
post_a = prior_a + wins
post_b = prior_b + losses

posterior_mean = post_a / (post_a + post_b)
posterior_ci = beta_dist.ppf([0.025, 0.975], post_a, post_b)
prob_gt_half = 1.0 - beta_dist.cdf(0.5, post_a, post_b)

posterior_summary = pd.Series({
    "prior_mean": prior_mean,
    "posterior_mean": posterior_mean,
    "ci_low": posterior_ci[0],
    "ci_high": posterior_ci[1],
    "prob_p_gt_0_5": prob_gt_half,
})

print(posterior_summary)
```

解释：

- 后验均值是更新后的胜率估计。
- `ci_low` 和 `ci_high` 是 95% credible interval，可信区间。
- `prob_p_gt_0_5` 是后验下胜率大于 50% 的概率。

可信区间可以直接说：

```text
在当前模型、先验和数据下，p 落在该区间的后验概率约为 95%。
```

这和频率学派置信区间的解释不同。

## 似然、先验和后验

可以在网格上看三者关系。

```python
p_grid = np.linspace(0.01, 0.99, 99)

log_likelihood = wins * np.log(p_grid) + losses * np.log1p(-p_grid)

log_prior = (
    (prior_a - 1.0) * np.log(p_grid)
    + (prior_b - 1.0) * np.log1p(-p_grid)
    - betaln(prior_a, prior_b)
)

log_posterior_unnormalized = log_likelihood + log_prior

grid_map = p_grid[np.argmax(log_posterior_unnormalized)]
closed_form_map = (post_a - 1.0) / (post_a + post_b - 2.0)

print(grid_map)
print(closed_form_map)
```

MAP 是 maximum a posteriori，后验密度最高的位置。

对 `Beta(a, b)` 且 `a, b > 1`，众数是：

```text
(a - 1) / (a + b - 2)
```

## 序贯更新

贝叶斯更新可以分批进行。先看第一批数据，再看第二批数据，结果和一次性看完相同。

```python
batch1_wins, batch1_losses = 30, 20
batch2_wins, batch2_losses = 28, 22

a_after_batch1 = prior_a + batch1_wins
b_after_batch1 = prior_b + batch1_losses

a_after_batch2 = a_after_batch1 + batch2_wins
b_after_batch2 = b_after_batch1 + batch2_losses

one_shot_a = prior_a + wins
one_shot_b = prior_b + losses

print(a_after_batch2, b_after_batch2)
print(one_shot_a, one_shot_b)
```

这就是贝叶斯更新的自然性：昨天的后验可以作为今天的先验。

## 先验敏感性

同一份数据，不同先验会得到不同后验。样本越小，先验影响越大；样本越大，似然影响越大。

```python
priors = [
    ("uniform", 1.0, 1.0),
    ("neutral_weak", 2.0, 2.0),
    ("skeptical_strong", 20.0, 20.0),
    ("optimistic", 8.0, 2.0),
]

rows = []

for name, a, b in priors:
    pa = a + wins
    pb = b + losses
    ci = beta_dist.ppf([0.025, 0.975], pa, pb)

    rows.append({
        "prior": name,
        "prior_mean": a / (a + b),
        "posterior_mean": pa / (pa + pb),
        "ci_low": ci[0],
        "ci_high": ci[1],
        "prob_p_gt_0_5": 1.0 - beta_dist.cdf(0.5, pa, pb),
    })

prior_sensitivity = pd.DataFrame(rows)

print(prior_sensitivity)
```

实战中，如果结论只在某个非常特定的先验下成立，就要谨慎。报告里最好说明先验选择，并做敏感性分析。

## 后验预测

贝叶斯方法不仅给参数后验，也能给未来观测的预测分布。

在 Beta-Binomial 模型里，下一次 win 的后验预测概率是：

```text
E[p | data]
```

也就是后验均值。

如果未来做 10 次交易，成功次数的后验预测分布是 Beta-Binomial。

```python
def beta_binomial_pmf(k, m, a, b):
    log_prob = (
        np.log(math.comb(m, k))
        + betaln(a + k, b + m - k)
        - betaln(a, b)
    )
    return np.exp(log_prob)


m_future = 10
predictive_probs = np.array([
    beta_binomial_pmf(k, m_future, post_a, post_b)
    for k in range(m_future + 1)
])

predictive_mean = m_future * posterior_mean
prob_at_least_6 = predictive_probs[6:].sum()

print(predictive_probs)
print(predictive_mean)
print(prob_at_least_6)
```

后验预测同时考虑：

- 参数 `p` 的不确定性。
- 未来交易结果自身的随机性。

## Normal-Normal：估计均值

再看一个连续变量例子。假设日收益 `x_i` 来自：

```text
x_i | mu ~ Normal(mu, sigma^2)
```

这里为了演示，先把 `sigma` 当作已知。

给均值 `mu` 一个正态先验：

```text
mu ~ Normal(mu0, tau0^2)
```

准备一组小样本收益：

```python
returns_small = np.array([
    0.010,
    -0.004,
    0.006,
    0.012,
    -0.008,
    0.003,
    0.015,
    -0.002,
    0.007,
    0.001,
])

sigma = 0.010
mu0 = 0.0
tau0 = 0.005

n_small = len(returns_small)
xbar = returns_small.mean()

print(xbar)
```

已知 `sigma` 时，后验精度等于先验精度加数据精度：

```text
1 / tau_post^2 = 1 / tau0^2 + n / sigma^2
```

后验均值是按精度加权的平均：

```text
mu_post = tau_post^2 * (mu0 / tau0^2 + n * xbar / sigma^2)
```

```python
prior_precision = 1.0 / (tau0 ** 2)
likelihood_precision = n_small / (sigma ** 2)

posterior_var = 1.0 / (prior_precision + likelihood_precision)
posterior_sd = np.sqrt(posterior_var)

posterior_mean_normal = posterior_var * (
    prior_precision * mu0
    + likelihood_precision * xbar
)

normal_ci = norm.ppf(
    [0.025, 0.975],
    loc=posterior_mean_normal,
    scale=posterior_sd,
)

prob_mu_gt_0 = 1.0 - norm.cdf(
    0.0,
    loc=posterior_mean_normal,
    scale=posterior_sd,
)

normal_summary = pd.Series({
    "sample_mean": xbar,
    "posterior_mean": posterior_mean_normal,
    "posterior_sd": posterior_sd,
    "ci_low": normal_ci[0],
    "ci_high": normal_ci[1],
    "prob_mu_gt_0": prob_mu_gt_0,
})

print(normal_summary)
```

因为先验均值是 0，且先验比较保守，后验均值会被从样本均值拉向 0。这就是贝叶斯收缩。

如果使用非常宽的先验，后验会更接近样本均值：

```python
tau_big = 1.0

posterior_var_big = 1.0 / (1.0 / tau_big ** 2 + n_small / sigma ** 2)
posterior_mean_big = posterior_var_big * (
    mu0 / tau_big ** 2
    + n_small * xbar / sigma ** 2
)

print(posterior_mean_big)
```

宽先验信息弱，数据主导后验。

## 贝叶斯和正则化

很多正则化方法可以从贝叶斯角度理解：

- Ridge 对应正态先验：系数更可能接近 0。
- Lasso 对应 Laplace 先验：更鼓励稀疏。
- 协方差收缩也可以理解成把估计拉向一个先验目标。

贝叶斯方法不是“主观拍脑袋”，而是把先验假设显式写出来，再用数据更新。

关键是：先验要能解释，后验要做敏感性分析。

## 常见坑

第一，把 prior 当成随便调结论的旋钮。

先验应该来自历史数据、业务知识、约束或保守假设。不能为了得到想要的后验随意调。

第二，只报告后验均值。

贝叶斯方法的优势是完整不确定性表达。应该报告可信区间、后验概率或预测分布。

第三，混淆置信区间和可信区间。

可信区间可以在给定模型和先验下直接谈参数概率；频率学派置信区间不能这样解释。

第四，忽略模型错设。

如果 likelihood 错了，后验也会被带偏。贝叶斯更新不能自动修复错误模型。

第五，样本很大时仍让强先验支配结论。

强先验需要强理由。否则要做先验敏感性分析。

## 实战提示

使用贝叶斯方法时可以按下面流程：

1. 明确未知参数 `theta` 是什么。
2. 写出 likelihood：数据在参数给定时如何生成。
3. 选择可解释的 prior。
4. 计算 posterior，能共轭就用闭式解，复杂模型用 MCMC 或变分近似。
5. 报告 posterior mean / median、credible interval 和关键概率。
6. 做 prior sensitivity。
7. 如果用于预测，报告 posterior predictive distribution。
8. 对交易或风控问题，关注后验尾部概率，而不只看均值。

## 小结

本节的重点：

- 贝叶斯更新是 `posterior ∝ likelihood × prior`。
- prior 表示看到当前数据前的信念。
- likelihood 表示参数给定时数据出现的概率。
- posterior 表示看到数据后的更新信念。
- Beta-Binomial 可以自然更新胜率。
- Normal-Normal 可以展示后验均值向先验收缩。
- credible interval 和 frequentist confidence interval 的解释不同。
- 后验预测同时包含参数不确定性和未来观测随机性。

## 自检问题

1. Bayes rule 中 prior、likelihood、posterior 分别是什么？
2. `Beta(a, b)` 在胜率问题里可以怎样直观理解？
3. 为什么贝叶斯更新可以分批进行？
4. credible interval 和 confidence interval 的解释有什么区别？
5. Normal-Normal 例子里，为什么后验均值会被拉向先验均值？
6. 为什么要做 prior sensitivity？
