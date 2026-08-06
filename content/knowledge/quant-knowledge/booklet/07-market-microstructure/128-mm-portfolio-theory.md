# 128. 市场微观结构扩展：均值-方差优化、协方差收缩、风险平价和组合权重约束

## 核心概念

投资组合理论解决的问题是：

```text
给定预期收益、风险和约束，应该如何分配权重？
```

在量化策略里，信号只是第一步。

真正落地还需要把信号转成组合：

```text
买哪些资产
每个资产买多少
总风险是多少
换手是否可接受
行业和风格暴露是否过大
```

这就是投资组合构建。

## 组合预期收益

组合预期收益是资产预期收益的加权和。

```python
weights = [0.6, 0.4]
expected_returns = [0.08, 0.04]

portfolio_return = sum(
    weight * expected_return
    for weight, expected_return in zip(weights, expected_returns)
)

print(round(portfolio_return, 4))
```

结果：

```text
0.064
```

组合预期收益是 `6.4%`。

权重越集中在高预期收益资产上，预期收益越高。

但风险也可能更高。

## 组合方差

组合风险不能只看单个资产波动率。

还要看资产之间的协方差。

两个资产的例子：

```python
weights = [0.6, 0.4]
vols = [0.20, 0.10]
corr = 0.25

cov = [
    [vols[0] ** 2, corr * vols[0] * vols[1]],
    [corr * vols[0] * vols[1], vols[1] ** 2],
]

variance = 0
for i in range(2):
    for j in range(2):
        variance += weights[i] * weights[j] * cov[i][j]

print(round(variance, 6))
print(round(variance ** 0.5, 4))
```

结果：

```text
0.0184
0.1356
```

组合波动率约为 `13.56%`。

如果两个资产相关性更高，分散化效果会变差。

## 均值-方差优化

均值-方差优化的目标通常写成：

```text
maximize expected_return - risk_aversion * variance
```

或者：

```text
在给定风险下最大化收益
在给定收益下最小化风险
```

伪代码：

```text
input:
    expected_returns
    covariance_matrix
    constraints

choose weights to:
    maximize weights · expected_returns - lambda * weights' covariance weights

subject to:
    sum(weights) = 1
    lower_bound <= weights <= upper_bound
    optional industry / factor / turnover constraints
```

均值-方差优化很强，但也很脆弱。

因为它高度依赖：

```text
预期收益估计
协方差估计
约束设置
交易成本假设
```

预期收益一点点变化，最优权重可能大幅变化。

## 样本均值和方差的不稳定

如果样本很少，估计会很不稳定。

```python
returns = [0.01, 0.02, -0.01]

mean = sum(returns) / len(returns)
variance = sum(
    (ret - mean) ** 2
    for ret in returns
) / (len(returns) - 1)

print(round(mean, 4))
print(round(variance, 6))
```

结果：

```text
0.0067
0.000233
```

只有三个观测时，均值和方差都很不可靠。

这就是为什么组合优化里经常要做收缩、约束和稳健处理。

## 协方差收缩

协方差矩阵估计容易噪声很大。

收缩的思想是：

```text
不要完全相信样本协方差
把样本协方差向一个更稳定的目标矩阵靠近
```

例如把样本协方差向对角矩阵收缩：

```python
sample_cov = [
    [0.04, 0.018],
    [0.018, 0.09],
]
target_cov = [
    [0.04, 0.0],
    [0.0, 0.09],
]
lambda_ = 0.5

shrunk = []
for row_sample, row_target in zip(sample_cov, target_cov):
    row = [
        (1 - lambda_) * sample + lambda_ * target
        for sample, target in zip(row_sample, row_target)
    ]
    shrunk.append(row)

print(shrunk)
```

结果：

```text
[[0.04, 0.009], [0.009, 0.09]]
```

非对角协方差从 `0.018` 被收缩到 `0.009`。

这降低了对样本相关性的依赖。

## 风险平价

风险平价的目标不是让金额权重相等。

而是让每个资产贡献的风险更接近。

如果两个资产不相关，粗略的风险平价权重常用 inverse volatility：

```python
vols = [0.20, 0.10]

inverse_vol = [
    1 / vol
    for vol in vols
]
total = sum(inverse_vol)
weights = [
    value / total
    for value in inverse_vol
]

print([round(weight, 4) for weight in weights])
```

结果：

```text
[0.3333, 0.6667]
```

低波动资产获得更高权重。

这不是因为它预期收益更高，而是为了让风险贡献更均衡。

## 风险贡献

简化地看，权重乘波动率可以作为风险贡献的直觉近似。

```python
weights = [1 / 3, 2 / 3]
vols = [0.20, 0.10]

risk_contrib = [
    weight * vol
    for weight, vol in zip(weights, vols)
]

print([round(value, 4) for value in risk_contrib])
```

结果：

```text
[0.0667, 0.0667]
```

两个资产风险贡献相同。

真实风险平价要考虑完整协方差矩阵，而不只是单资产波动率。

## 权重约束

没有约束的优化可能给出不可交易权重。

例如：

```text
单个资产权重过大
大量空头
行业集中
换手过高
杠杆过大
```

一个简单权重裁剪例子：

```python
raw_weights = [0.8, 0.5, -0.1]

clipped = [
    min(max(weight, 0), 0.6)
    for weight in raw_weights
]
total = sum(clipped)
normalized = [
    weight / total
    for weight in clipped
]

print(clipped)
print([round(weight, 4) for weight in normalized])
```

结果：

```text
[0.6, 0.5, 0]
[0.5455, 0.4545, 0.0]
```

先把权重限制在 `[0, 0.6]`。

再重新归一化到总权重为 `1`。

## 换手约束

调仓会产生交易成本。

换手可以用新旧权重差的一半来估算。

```python
old_weights = [0.5, 0.5]
new_weights = [0.7, 0.3]

turnover = sum(
    abs(new - old)
    for new, old in zip(new_weights, old_weights)
) / 2

print(round(turnover, 4))
```

结果：

```text
0.2
```

这表示组合有 `20%` 的单边换手。

如果策略信号很弱，但每次调仓换手很高，交易成本可能吃掉收益。

## 从信号到权重

实际策略不会只最大化信号。

常见做法是把信号和风险放在一起。

```python
signal = [0.03, 0.01]
risk_penalty = [0.02, 0.005]

scores = [
    alpha - risk
    for alpha, risk in zip(signal, risk_penalty)
]

print(scores)
```

结果：

```text
[0.009999999999999998, 0.005]
```

第一个资产 alpha 更高，但风险惩罚也更大。

组合构建的目标是：

```text
在风险、成本和约束下使用 alpha
```

而不是机械地买入信号最高的资产。

## 约束的实际类型

真实组合通常有很多约束：

```text
总权重 = 1
单资产权重上下限
行业权重上下限
国家或市场权重限制
beta 暴露限制
风格因子暴露限制
杠杆限制
换手限制
成交量参与率限制
```

这些约束会让优化结果更可交易。

但约束太多也可能让组合无法表达信号。

所以组合构建是收益、风险、成本和可执行性的折中。

## 回测中的常见错误

投资组合回测常见错误包括：

```text
用未来收益估计当前预期收益
用全样本协方差矩阵
没有滚动估计风险
忽略交易成本和 market impact
没有单资产和行业约束
允许现实中不可用的杠杆或空头
只看平均收益，不看回撤和风险贡献
把优化器输出当成一定可成交的订单
```

尤其要注意协方差矩阵。

如果用全样本协方差优化历史组合，未来信息会泄露进过去权重。

## 与因子模型的关系

上一篇因子模型回答：

```text
组合暴露在哪些风险因子上？
```

投资组合理论回答：

```text
在这些风险和约束下，权重应该是多少？
```

两者通常一起使用。

例如：

```text
用 alpha 模型产生预期收益
用风险模型估计协方差和因子暴露
用优化器生成权重
用交易成本模型调整换手
```

这才是完整的组合构建流程。

## 小结

投资组合理论把信号转成可交易权重。

需要掌握：

```text
组合预期收益
组合方差
均值-方差优化
协方差收缩
风险平价
权重约束
换手和交易成本
回测防泄露
```

下一篇讨论 bid-ask bounce、VWAP 和 tick 数据特性。

它会回到更细粒度的市场微观结构数据，说明高频价格和成交数据为什么不能直接当成干净时间序列。
