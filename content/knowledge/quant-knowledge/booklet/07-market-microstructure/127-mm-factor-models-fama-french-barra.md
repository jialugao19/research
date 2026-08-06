# Fama-French & Barra

## 核心概念

因子模型用少数共同变量解释很多资产的收益和风险。

基本思想是：

```text
资产收益 = 因子暴露 * 因子收益 + 个股特有收益
```

因子可以是：

```text
市场因子
规模因子
价值因子
动量因子
行业因子
波动率因子
流动性因子
```

因子模型有两个常见用途。

第一是解释收益来源。

第二是控制组合风险。

## Fama-French 因子

Fama-French 模型是经典资产定价因子模型。

最基本的三因子包括：

```text
MKT: 市场风险溢价
SMB: small minus big，小市值减大市值
HML: high minus low，高账面市值比减低账面市值比
```

直觉是：

```text
股票收益不只来自市场 beta
还可能系统性暴露在规模和价值风格上
```

例如股票收益和市场无风险收益：

```python
market_return = 0.01
stock_return = 0.015
risk_free = 0.002

excess_stock = stock_return - risk_free
excess_market = market_return - risk_free

print(round(excess_stock, 4))
print(round(excess_market, 4))
```

结果：

```text
0.013
0.008
```

Fama-French 模型通常解释的是超额收益。

也就是收益减去无风险收益。

## 多空因子组合

很多因子收益可以用多空组合构造。

例如价值因子：

```text
做多高 book-to-market 股票
做空低 book-to-market 股票
```

小例子：

```python
returns = [0.02, 0.01, -0.01, -0.03]

long = returns[:2]
short = returns[2:]
factor_return = sum(long) / len(long) - sum(short) / len(short)

print(round(factor_return, 4))
```

结果：

```text
0.035
```

多头平均收益是 `1.5%`。

空头平均收益是 `-2.0%`。

多空因子收益是 `3.5%`。

## 因子排序

构造因子组合时，经常先按某个指标排序。

例如 book-to-market 越高，越偏价值。

```python
book_to_market = [0.8, 0.2, 0.6, 0.1]

ranked = sorted(
    range(len(book_to_market)),
    key=lambda i: book_to_market[i]
)
low = ranked[:2]
high = ranked[-2:]

print(low)
print(high)
```

结果：

```text
[3, 1]
[2, 0]
```

索引 `3` 和 `1` 是低 book-to-market。

索引 `2` 和 `0` 是高 book-to-market。

实际研究中，还会处理：

```text
缺失值
极端值
行业差异
市值权重
调仓频率
可交易性
公告滞后
```

## Barra 风险因子

Barra 风险模型更偏风险管理。

它通常把股票收益拆成：

```text
国家/市场因子
行业因子
风格因子
个股特异收益
```

风格因子可能包括：

```text
size
value
momentum
volatility
liquidity
leverage
growth
earnings yield
```

Barra 的重点不是找一个单独 alpha。

而是回答：

```text
组合暴露在哪些系统性风险上？
这些风险贡献了多少波动？
如何控制行业、市值和风格偏离？
```

## 暴露和因子收益

如果一只股票的因子暴露是：

```text
market = 1.1
value = 0.4
size = -0.2
```

当天因子收益是：

```text
market = 1.0%
value = 0.3%
size = -0.2%
```

预测的因子解释收益是：

```python
exposures = {
    "market": 1.1,
    "value": 0.4,
    "size": -0.2,
}
factor_returns = {
    "market": 0.01,
    "value": 0.003,
    "size": -0.002,
}

predicted = sum(
    exposures[name] * factor_returns[name]
    for name in exposures
)

print(round(predicted, 4))
```

结果：

```text
0.0126
```

这表示该股票当天有 `1.26%` 的收益可由这些因子暴露解释。

剩下的是特异收益。

## 特异收益

如果真实收益和因子解释收益不同，差值就是特异收益的简化版本。

```python
returns = [0.02, -0.01, 0.03]
factor_pred = [0.015, -0.005, 0.01]

specific = [
    actual - predicted
    for actual, predicted in zip(returns, factor_pred)
]

print([round(x, 4) for x in specific])
```

结果：

```text
[0.005, -0.005, 0.02]
```

特异收益不一定是 alpha。

它也可能来自噪声、遗漏风险、事件冲击或数据问题。

## 标准化因子

不同因子的量纲不同。

例如：

```text
市值是金额
动量是收益率
波动率是标准差
估值是比率
```

常见做法是转成 z-score。

```python
scores = [1.5, 0.5, -0.5, -1.5]

mean = sum(scores) / len(scores)
std = (
    sum((x - mean) ** 2 for x in scores) / len(scores)
) ** 0.5
z_scores = [
    (x - mean) / std
    for x in scores
]

print([round(x, 4) for x in z_scores])
```

结果：

```text
[1.3416, 0.4472, -0.4472, -1.3416]
```

标准化后，不同因子更容易比较和合成。

但标准化必须只使用当时可见的横截面数据，不能用未来样本。

## 行业中性化

很多因子会天然带有行业偏差。

例如银行股和科技股的估值指标分布可能完全不同。

如果不控制行业，所谓价值因子可能只是行业 bet。

简化的行业中性化做法是：每个行业内减去行业均值。

```python
factor = [0.8, 0.4, -0.2, -0.6]
industries = ["Tech", "Tech", "Bank", "Bank"]

neutralized = []
for value, industry in zip(factor, industries):
    group_values = [
        x
        for x, group in zip(factor, industries)
        if group == industry
    ]
    group_mean = sum(group_values) / len(group_values)
    neutralized.append(value - group_mean)

print(neutralized)
```

结果：

```text
[0.19999999999999996, -0.20000000000000007, 0.2, -0.19999999999999996]
```

行业均值被去掉后，因子主要表达行业内部差异。

## 市值中性化

很多因子也会和市值相关。

例如流动性、估值、波动率都可能带有 size 暴露。

可以用横截面回归去掉 size 影响。

这里用一个非常小的线性回归例子：

```python
size = [10, 20, 30]
factor = [1.0, 1.8, 3.2]

mean_size = sum(size) / len(size)
mean_factor = sum(factor) / len(factor)

beta = sum(
    (s - mean_size) * (f - mean_factor)
    for s, f in zip(size, factor)
) / sum(
    (s - mean_size) ** 2
    for s in size
)
alpha = mean_factor - beta * mean_size

residual = [
    f - (alpha + beta * s)
    for s, f in zip(size, factor)
]

print(round(alpha, 4))
print(round(beta, 4))
print([round(x, 4) for x in residual])
```

结果：

```text
-0.2
0.11
[0.1, -0.2, 0.1]
```

残差就是去掉线性 size 暴露后的因子。

实际 Barra 风格模型会用更完整的横截面回归和约束。

## 组合暴露控制

因子模型可以检查组合是否真的中性。

例如一个多空组合：

```python
weights = [0.5, -0.5]
market_betas = [1.2, 0.8]

portfolio_beta = sum(
    weight * beta
    for weight, beta in zip(weights, market_betas)
)

print(round(portfolio_beta, 4))
```

结果：

```text
0.2
```

虽然权重一多一空，看起来 dollar neutral。

但市场 beta 暴露仍然是 `0.2`。

所以：

```text
dollar neutral 不等于 beta neutral
industry neutral 不等于 style neutral
factor neutral 不等于没有风险
```

## 因子构造中的泄露

因子构造很容易产生前视偏差。

常见风险包括：

```text
使用未来财报数据
用复权后未来已知的成分股列表
用全样本分位数分组
用未来行业分类或市值
用调仓日之后才发布的数据做调仓日信号
没有处理公告滞后
```

例如财务因子必须考虑公告日期。

不是年报期末是 `2025-12-31`，就能在这一天使用全部年报数据。

应按真实可获得时间进入信号。

## Fama-French 和 Barra 的区别

可以粗略理解为：

```text
Fama-French: 更偏资产定价和解释长期收益溢价
Barra: 更偏组合风险分解、风险预测和约束管理
```

Fama-French 常问：

```text
价值、规模、市场这些因子是否解释了收益？
```

Barra 常问：

```text
我的组合暴露在哪些行业和风格风险上？
风险来自 common factor 还是 specific risk？
如何让组合满足约束？
```

两者都重要，但使用场景不同。

## 小结

因子模型把资产收益拆成共同因子和特异部分。

实践中要掌握：

```text
因子如何构造
因子暴露和因子收益的区别
Fama-French 的多空因子思想
Barra 的风险暴露管理思想
行业中性化
市值中性化
组合因子暴露检查
数据可得性和前视偏差
```

下一篇讨论投资组合理论。

它会从均值-方差优化、协方差收缩和风险平价开始，说明如何把信号和风险转成组合权重。
