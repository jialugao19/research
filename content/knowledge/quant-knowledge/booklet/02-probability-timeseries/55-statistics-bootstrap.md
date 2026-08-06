# bootstrap

## 核心概念

bootstrap 是一种用重采样估计统计量不确定性的方法。

核心思想：

```text
真实总体未知
手上只有一个样本
把这个样本当作总体的近似
从样本中有放回地抽样，构造许多 bootstrap 样本
每个 bootstrap 样本计算一次统计量
这些统计量的分布近似原统计量的抽样分布
```

bootstrap 常用于估计：

- 均值、 中位数、分位数的标准误。
- 回归系数的不确定性。
- Sharpe、IC、RankIC、最大回撤等复杂统计量的置信区间。
- 小样本下难以手写标准误的统计量。

最基础的 iid bootstrap 假设观测之间可以交换，近似独立同分布。时间序列、面板数据和分组数据通常不能直接用 iid bootstrap。

## 准备环境

```python
import numpy as np
import pandas as pd
```

准备一组带厚尾和少量负向冲击的收益样本：

```python
rng = np.random.default_rng(55)
n = 120

returns = 0.0007 + 0.012 * rng.standard_t(df=5, size=n)
returns[::37] -= 0.035

sample_mean = returns.mean()
sample_median = np.median(returns)
sample_std = returns.std(ddof=1)
analytic_mean_se = sample_std / np.sqrt(n)

print(sample_mean)
print(sample_median)
print(analytic_mean_se)
```

这里的 `analytic_mean_se` 是均值标准误的常规公式：

```text
sample_std / sqrt(n)
```

但对于中位数、分位数、Sharpe、最大回撤等统计量，手写标准误就没这么直接。

## iid bootstrap 函数

写一个通用 bootstrap 函数：

```python
def bootstrap_statistic(values, statistic, n_boot=4000, seed=0):
    values = np.asarray(values)
    rng = np.random.default_rng(seed)

    n = len(values)
    out = np.empty(n_boot)

    for b in range(n_boot):
        sample = values[rng.integers(0, n, size=n)]
        out[b] = statistic(sample)

    return out
```

每次 `rng.integers(0, n, size=n)` 都会抽出一组长度为 `n` 的索引。因为是有放回抽样，同一条观测可能出现多次，也可能完全没出现。

再写一个 percentile 区间函数：

```python
def percentile_interval(samples, level=0.95):
    alpha = 1.0 - level
    return np.quantile(samples, [alpha / 2.0, 1.0 - alpha / 2.0])
```

## 均值的 bootstrap 标准误

对均值做 bootstrap：

```python
boot_mean = bootstrap_statistic(
    returns,
    statistic=np.mean,
    n_boot=4000,
    seed=100,
)

boot_mean_se = boot_mean.std(ddof=1)
boot_mean_ci = percentile_interval(boot_mean, level=0.95)

print(boot_mean_se)
print(boot_mean_ci)
print(analytic_mean_se)
```

对 iid 样本均值，bootstrap 标准误通常会接近常规公式。差异来自有限样本和随机重采样误差。

可以整理成表：

```python
mean_summary = pd.Series({
    "sample_mean": sample_mean,
    "analytic_se": analytic_mean_se,
    "bootstrap_se": boot_mean_se,
    "ci_low": boot_mean_ci[0],
    "ci_high": boot_mean_ci[1],
})

print(mean_summary)
```

percentile 区间是最直观的 bootstrap 置信区间：直接取 bootstrap 统计量分布的 2.5% 和 97.5% 分位数。

## 中位数的 bootstrap

对中位数也可以用同一套函数：

```python
boot_median = bootstrap_statistic(
    returns,
    statistic=np.median,
    n_boot=4000,
    seed=101,
)

median_summary = pd.Series({
    "sample_median": sample_median,
    "bootstrap_se": boot_median.std(ddof=1),
    "ci_low": percentile_interval(boot_median)[0],
    "ci_high": percentile_interval(boot_median)[1],
})

print(median_summary)
```

bootstrap 的优势是：只要能在一个样本上计算统计量，就能通过重采样估计它的不确定性。

当然，这不代表 bootstrap 永远准确。样本太小、极端尾部事件没被观测到、数据强相关时，bootstrap 也会给出过于乐观的结论。

## bootstrap bias

bootstrap 还可以估计统计量偏差：

```text
bias_hat = mean(bootstrap_statistic) - statistic(original_sample)
```

```python
mean_bias = boot_mean.mean() - sample_mean
median_bias = boot_median.mean() - sample_median

bias_summary = pd.Series({
    "mean_bias": mean_bias,
    "median_bias": median_bias,
})

print(bias_summary)
```

小偏差不一定需要修正。实际报告中，更常用的是 bootstrap 标准误和置信区间。

## 成对 bootstrap：回归斜率

回归数据里，`x` 和 `y` 是成对观测。bootstrap 时要整行重采样，而不是分别重采样 `x` 和 `y`。

构造一组线性数据：

```python
rng = np.random.default_rng(56)
n_reg = 80

x = rng.normal(size=n_reg)
y = 0.4 + 0.75 * x + rng.normal(0.0, 0.8, size=n_reg)
```

拟合斜率：

```python
def fit_slope(x, y):
    X = np.column_stack([np.ones(len(x)), x])
    return np.linalg.lstsq(X, y, rcond=None)[0][1]


slope_hat = fit_slope(x, y)

print(slope_hat)
```

成对 bootstrap：

```python
def paired_bootstrap_slope(x, y, n_boot=4000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(x)
    out = np.empty(n_boot)

    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        out[b] = fit_slope(x[idx], y[idx])

    return out


boot_slopes = paired_bootstrap_slope(x, y, n_boot=4000, seed=200)

slope_ci = percentile_interval(boot_slopes)

slope_summary = pd.Series({
    "slope_hat": slope_hat,
    "bootstrap_se": boot_slopes.std(ddof=1),
    "ci_low": slope_ci[0],
    "ci_high": slope_ci[1],
})

print(slope_summary)
```

这里重采样的是 `(x_i, y_i)` 这一整行。这样能保留解释变量和被解释变量之间的对应关系。

## 时间序列不能随便 iid bootstrap

如果收益有自相关，iid bootstrap 会打散时间顺序，低估均值的不确定性。

构造一个 AR(1) 序列：

```python
rng = np.random.default_rng(57)
n_ts = 250
phi = 0.65

innov = rng.normal(0.0, 0.01, size=n_ts)
ts_returns = np.empty(n_ts)
ts_returns[0] = innov[0]

for t in range(1, n_ts):
    ts_returns[t] = phi * ts_returns[t - 1] + innov[t]

acf1 = np.corrcoef(ts_returns[:-1], ts_returns[1:])[0, 1]

print(acf1)
```

对这个序列直接 iid bootstrap 均值：

```python
iid_boot_mean = bootstrap_statistic(
    ts_returns,
    statistic=np.mean,
    n_boot=3000,
    seed=300,
)

print(iid_boot_mean.std(ddof=1))
```

因为 iid bootstrap 打散了连续性，它会忽略正自相关带来的有效样本数下降。

## block bootstrap

一种简单修正是 block bootstrap：每次抽连续区块，而不是抽单个观测。

```python
def block_bootstrap_mean(values, block_size, n_boot=3000, seed=0):
    values = np.asarray(values)
    rng = np.random.default_rng(seed)

    n = len(values)
    starts = np.arange(0, n - block_size + 1)
    n_blocks = int(np.ceil(n / block_size))

    out = np.empty(n_boot)

    for b in range(n_boot):
        chosen_starts = rng.choice(starts, size=n_blocks, replace=True)
        sample = np.concatenate([
            values[start:start + block_size]
            for start in chosen_starts
        ])[:n]
        out[b] = sample.mean()

    return out
```

用长度为 10 的 block：

```python
block_boot_mean = block_bootstrap_mean(
    ts_returns,
    block_size=10,
    n_boot=3000,
    seed=301,
)

time_series_summary = pd.Series({
    "acf1": acf1,
    "iid_bootstrap_se": iid_boot_mean.std(ddof=1),
    "block_bootstrap_se": block_boot_mean.std(ddof=1),
    "block_ci_low": percentile_interval(block_boot_mean)[0],
    "block_ci_high": percentile_interval(block_boot_mean)[1],
})

print(time_series_summary)
```

在正自相关序列里，block bootstrap 的均值标准误通常比 iid bootstrap 更大，因为它保留了部分连续依赖结构。

block 长度没有万能答案。太短会破坏依赖，太长会减少可组合的区块数量。实践里常结合业务周期、样本长度和敏感性分析选择。

## bootstrap 置信区间的解释

percentile bootstrap 区间可以理解为：

```text
如果原始样本能代表总体，重采样统计量中间 95% 的范围大致反映统计量不确定性。
```

注意它不是说“真实参数有 95% 概率在这个具体区间内”。频率学派置信区间的概率解释针对重复抽样过程，而不是已经固定的参数。

常见 bootstrap 区间：

- percentile interval：直接取 bootstrap 分布分位数。
- basic interval：围绕原统计量做镜像修正。
- studentized interval：对每次统计量再标准化。
- BCa interval：修正偏差和加速度。

本节只讲最基础的 percentile interval。复杂区间更稳，但实现和解释也更复杂。

## 常见坑

第一，样本太小。

bootstrap 只能重用已有观测。如果样本没有覆盖尾部风险，bootstrap 也很难凭空创造真实尾部。

第二，对时间序列使用 iid bootstrap。

收益、成交量、波动率通常有自相关和波动聚集。直接抽单点会低估不确定性。

第三，回归里分别重采样 `x` 和 `y`。

这样会破坏样本对关系。成对数据应整行重采样。

第四，把 bootstrap 当成模型正确性的证明。

bootstrap 估计的是统计量在当前数据生成近似下的不确定性。模型遗漏变量、前视偏差、样本选择偏差不会被 bootstrap 自动修复。

第五，用同一个测试集反复看 bootstrap 结果后调策略。

bootstrap 不能解决数据挖掘和测试集污染问题。

## 实战提示

使用 bootstrap 时可以按下面流程：

1. 明确要估计哪个统计量的不确定性。
2. 判断观测是否可以近似 iid。
3. iid 数据用有放回行抽样。
4. 回归和分类任务保留整行样本关系。
5. 时间序列考虑 block bootstrap、stationary bootstrap 或其他依赖结构方法。
6. 固定随机种子，记录 `n_boot`、block 长度和统计量定义。
7. 报告 bootstrap 标准误和区间，不只报告点估计。
8. 对结果做敏感性分析，例如改变 block 长度或重采样次数。

## 小结

本节的重点：

- bootstrap 用有放回重采样近似统计量的抽样分布。
- iid bootstrap 适合近似独立同分布的观测。
- percentile interval 是最直接的 bootstrap 置信区间。
- 成对数据要整行重采样。
- 时间序列不能随便打散顺序，常用 block bootstrap 保留局部依赖。
- bootstrap 估计不确定性，但不能修复数据偏差、模型错设或泄露。

## 自检问题

1. bootstrap 为什么要有放回抽样？
2. bootstrap 标准误是怎么从重采样统计量中得到的？
3. percentile bootstrap 置信区间怎么计算？
4. 回归里为什么要做成对 bootstrap？
5. 为什么自相关时间序列不适合直接 iid bootstrap？
6. block bootstrap 的 block 长度太短或太长分别有什么问题？
