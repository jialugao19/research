# 概率统计：Sharpe ratio 的定义、年化、假设限制与实战解释

## 核心概念

Sharpe ratio 衡量单位波动率对应的超额收益。

最常见定义：

```text
Sharpe = mean(R_p - R_f) / std(R_p - R_f)
```

其中：

- `R_p`：组合收益。
- `R_f`：无风险收益。
- `R_p - R_f`：超额收益。
- `std`：超额收益的标准差。

如果用日收益计算年化 Sharpe：

```text
annualized_sharpe = daily_sharpe * sqrt(252)
```

更一般地：

```text
annualized_sharpe = mean(excess_return) / std(excess_return) * sqrt(periods_per_year)
```

Sharpe 的核心思想是：同样的平均收益，波动越低越好；同样的波动，平均收益越高越好。

## Sharpe 回答的问题

Sharpe 不是问：

```text
策略赚了多少钱？
```

它问的是：

```text
承担一单位波动风险，策略获得了多少超额收益？
```

因此两个策略可能有相同年化收益，但 Sharpe 不同：

- 策略 A 年化收益 10%，年化波动 10%，Sharpe 约为 1。
- 策略 B 年化收益 10%，年化波动 25%，Sharpe 约为 0.4。

如果只看收益，不看波动，很容易高估高杠杆、高回撤或尾部风险策略。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造两年日频策略收益：

```python
rng = np.random.default_rng(61)

dates = pd.bdate_range("2023-01-02", periods=504)

market_return = rng.normal(
    loc=0.00025,
    scale=0.010,
    size=len(dates),
)

alpha_return = rng.normal(
    loc=0.00045,
    scale=0.004,
    size=len(dates),
)

strategy_return = pd.Series(
    0.35 * market_return + alpha_return,
    index=dates,
    name="strategy_return",
)

print(strategy_return.head())
```

这个模拟策略有两部分：

- 一部分来自市场暴露。
- 一部分来自独立 alpha。

真实研究中，`strategy_return` 通常来自回测净值的日收益。

## 计算日频 Sharpe

设年化无风险收益为 2%。

```python
risk_free_annual = 0.02
risk_free_daily = (1 + risk_free_annual) ** (1 / 252) - 1

excess_return = strategy_return - risk_free_daily

daily_mean = excess_return.mean()
daily_vol = excess_return.std(ddof=1)
daily_sharpe = daily_mean / daily_vol
annualized_sharpe = daily_sharpe * np.sqrt(252)

print(daily_mean)
print(daily_vol)
print(annualized_sharpe)
```

这里用 `ddof=1` 计算样本标准差。

如果无风险收益很小，也常看到近似写法：

```python
simple_sharpe = (
    strategy_return.mean()
    / strategy_return.std(ddof=1)
    * np.sqrt(252)
)

print(simple_sharpe)
```

但正式报告里应尽量使用超额收益，尤其是在利率较高或持有现金较多的策略中。

## 年化收益、年化波动和 Sharpe

可以把 Sharpe 拆成年化收益除以年化波动。

```python
annualized_excess_return = excess_return.mean() * 252
annualized_volatility = excess_return.std(ddof=1) * np.sqrt(252)

sharpe_from_annualized_values = (
    annualized_excess_return
    / annualized_volatility
)

print(annualized_excess_return)
print(annualized_volatility)
print(sharpe_from_annualized_values)
```

这和前面 `daily_sharpe * sqrt(252)` 等价。

注意这里的年化收益是简单年化均值，不是复利 CAGR。Sharpe 通常使用收益均值和标准差，不直接使用 CAGR。

## 和 t 统计的关系

如果收益近似独立同分布，样本均值的 t 统计为：

```text
t_stat = mean(excess_return) / (std(excess_return) / sqrt(n))
```

它和年化 Sharpe 的关系是：

```text
t_stat = annualized_sharpe * sqrt(n / periods_per_year)
```

代码验证：

```python
n_obs = excess_return.count()

t_stat = (
    excess_return.mean()
    / (excess_return.std(ddof=1) / np.sqrt(n_obs))
)

t_stat_from_sharpe = annualized_sharpe * np.sqrt(n_obs / 252)

print(t_stat)
print(t_stat_from_sharpe)
```

这个关系常用于把 Sharpe 和统计显著性联系起来。

但它依赖较强假设：收益独立、波动稳定、尾部不过厚。实际策略收益往往存在自相关、波动聚集和尾部风险，因此简单 t 统计可能过于乐观。

## 月频 Sharpe

如果数据是月频，不应该再乘 `sqrt(252)`。应使用每年 12 期。

先把日收益聚合成月收益：

```python
monthly_return = (1 + strategy_return).resample("ME").prod() - 1
monthly_risk_free = (1 + risk_free_annual) ** (1 / 12) - 1

monthly_excess_return = monthly_return - monthly_risk_free

monthly_sharpe = (
    monthly_excess_return.mean()
    / monthly_excess_return.std(ddof=1)
    * np.sqrt(12)
)

print(monthly_return.head())
print(monthly_sharpe)
```

年化因子必须和收益频率匹配：

- 日频常用 `252`。
- 周频常用 `52`。
- 月频常用 `12`。
- 分钟频不能机械乘很大的平方根因子，微观结构噪声和自相关会很明显。

## 扣成本后的 Sharpe

Sharpe 应该优先看净收益口径。下面用 turnover 估算交易成本。

```python
turnover = pd.Series(
    rng.uniform(0.05, 0.25, size=len(dates)),
    index=dates,
    name="turnover",
)

fee_rate = 0.0005
trading_cost = turnover * fee_rate * 2

net_return = strategy_return - trading_cost
net_excess_return = net_return - risk_free_daily

gross_sharpe = annualized_sharpe
net_sharpe = (
    net_excess_return.mean()
    / net_excess_return.std(ddof=1)
    * np.sqrt(252)
)

print(gross_sharpe)
print(net_sharpe)
```

在这个例子里，扣成本后 Sharpe 会下降。

这也是为什么评价因子时不能只看 IC 或毛收益。高 turnover 策略如果成本过高，净 Sharpe 可能很低。

## 滚动 Sharpe

单个全样本 Sharpe 可能掩盖稳定性问题。可以看滚动 Sharpe。

```python
rolling_window = 63

rolling_sharpe = (
    excess_return.rolling(rolling_window).mean()
    / excess_return.rolling(rolling_window).std(ddof=1)
    * np.sqrt(252)
)

print(rolling_sharpe.dropna().head())
print(rolling_sharpe.dropna().tail())
```

滚动 Sharpe 可以帮助发现：

- 策略是否只在某个阶段有效。
- 是否存在 regime 切换。
- 最近表现是否明显低于历史平均。
- 是否有单一时期贡献了大部分收益。

但滚动窗口越短，估计越 noisy；窗口越长，反应越慢。

## Sharpe 的限制

Sharpe 使用标准差衡量风险，这隐含了一个重要假设：上行波动和下行波动都被视为风险。

如果策略收益分布明显偏态，例如：

- 卖期权策略：平时小赚，偶尔大亏。
- 高杠杆套利：长期平稳，危机时跳跌。
- 止损策略：收益分布被截断。

Sharpe 可能低估尾部风险或误导比较。

可以辅助查看：

```python
downside_return = excess_return.copy()
downside_return[downside_return > 0] = 0

sortino_ratio = (
    excess_return.mean()
    / np.sqrt((downside_return ** 2).mean())
    * np.sqrt(252)
)

skewness = excess_return.skew()
excess_kurtosis = excess_return.kurtosis()

print(sortino_ratio)
print(skewness)
print(excess_kurtosis)
```

Sortino ratio 只惩罚下行波动；偏度和峰度帮助观察尾部形态。

它们不能替代 Sharpe，但能补充风险画像。

## 常见坑

第一，忘记使用超额收益。

利率很低时差异可能不大，但在高利率环境中，直接用总收益会高估策略风险调整后表现。

第二，年化因子用错。

日频、月频、周频必须使用不同的 `periods_per_year`。不要把月收益乘 `sqrt(252)`。

第三，把高 Sharpe 当成稳定盈利保证。

历史 Sharpe 是样本估计，有统计误差。样本越短，估计越不可靠。

第四，忽略自相关。

平滑收益、低频估值、持有期重叠都会产生自相关，使年化 Sharpe 和 t 统计偏乐观。

第五，只看毛 Sharpe。

交易成本、滑点、冲击成本、借券费、融资成本都会降低净 Sharpe。

第六，用 Sharpe 比较尾部风险完全不同的策略。

卖尾部风险的策略可能 Sharpe 很高，但隐藏巨大回撤风险。

## 实战提示

报告 Sharpe 时可以按下面流程：

1. 明确收益口径：毛收益、净收益、超额收益还是主动收益。
2. 明确频率：日频、周频、月频。
3. 使用匹配频率的无风险收益。
4. 使用匹配频率的年化因子。
5. 同时报告年化收益、年化波动、Sharpe。
6. 对比扣成本前后 Sharpe。
7. 检查滚动 Sharpe、分年份 Sharpe 和样本外 Sharpe。
8. 同时查看 drawdown、偏度、峰度和极端损失。
9. 对自相关明显的策略使用更保守的显著性评估。

## 小结

本节的重点：

- Sharpe 衡量单位波动率上的超额收益。
- 日频 Sharpe 年化常乘 `sqrt(252)`，月频常乘 `sqrt(12)`。
- Sharpe 和 t 统计有简单关系，但依赖独立同分布等假设。
- 净 Sharpe 比毛 Sharpe 更接近实盘。
- 滚动 Sharpe 能观察稳定性。
- Sharpe 不充分刻画尾部风险，必须结合回撤、偏度、峰度和交易成本。

## 自检问题

1. 为什么 Sharpe 应该使用超额收益？
2. 日频收益和月频收益的 Sharpe 年化因子有什么不同？
3. Sharpe 和样本均值 t 统计有什么关系？
4. 为什么自相关会让年化 Sharpe 过于乐观？
5. 毛 Sharpe 和净 Sharpe 的区别是什么？
6. 为什么高 Sharpe 策略仍然可能有严重尾部风险？
