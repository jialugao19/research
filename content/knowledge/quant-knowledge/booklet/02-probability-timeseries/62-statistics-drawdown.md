# 概率统计：drawdown 回撤的定义、最大回撤、持续时间与风险解释

## 核心概念

drawdown 回撤衡量净值从历史高点下跌了多少。

给定净值序列 `NAV_t`，先计算截至 `t` 的历史最高净值：

```text
peak_t = max(NAV_0, NAV_1, ..., NAV_t)
```

回撤定义为：

```text
drawdown_t = NAV_t / peak_t - 1
```

因此：

- 新高位置的 drawdown 是 `0`。
- 亏损回落时 drawdown 是负数。
- 最大回撤 MDD 是 drawdown 序列的最小值。

```text
max_drawdown = min_t drawdown_t
```

回撤关注的是路径风险。两个策略即使最终收益相同，中间亏损路径也可能完全不同。

## drawdown 回答的问题

Sharpe 主要看平均收益和波动，drawdown 关注投资者实际承受的亏损路径。

它回答的问题包括：

- 从历史高点最多亏过多少？
- 最深亏损发生在什么时候？
- 从高点跌到谷底用了多久？
- 从谷底恢复到新高用了多久？
- 策略是否有长时间 underwater 状态？

对实盘资金来说，最大回撤和回撤持续时间往往比单个 Sharpe 更直观。

## 准备环境

```python
import numpy as np
import pandas as pd
```

先构造一个容易手算的净值序列：

```python
dates = pd.bdate_range("2024-01-02", periods=10)

nav = pd.Series(
    [1.00, 1.04, 1.08, 1.02, 0.96, 0.90, 0.95, 1.00, 1.10, 1.06],
    index=dates,
    name="nav",
)

print(nav)
```

这条净值曲线先从 `1.00` 涨到 `1.08`，然后跌到 `0.90`，之后恢复并创新高。

## 计算回撤序列

```python
running_peak = nav.cummax()
drawdown = nav / running_peak - 1

drawdown_table = pd.DataFrame({
    "nav": nav,
    "running_peak": running_peak,
    "drawdown": drawdown,
})

print(drawdown_table)
```

在最高点 `1.08` 之后，净值跌到 `0.90`：

```text
0.90 / 1.08 - 1 = -16.67%
```

这就是该序列的最大回撤。

## 最大回撤、峰值、谷底和修复日期

找到最大回撤：

```python
max_drawdown = drawdown.min()
trough_date = drawdown.idxmin()
peak_date = nav.loc[:trough_date].idxmax()

recovery_candidates = drawdown.loc[trough_date:]
recovery_candidates = recovery_candidates[recovery_candidates >= 0]

if recovery_candidates.empty:
    recovery_date = pd.NaT
else:
    recovery_date = recovery_candidates.index[0]

print(max_drawdown)
print(peak_date)
print(trough_date)
print(recovery_date)
```

这几个日期的含义：

- `peak_date`：最大回撤之前的历史高点日期。
- `trough_date`：最大回撤谷底日期。
- `recovery_date`：净值重新回到历史高点并创新高的日期。

如果 `recovery_date` 是 `NaT`，说明截至样本结束仍未修复。

## 回撤持续时间

可以计算从高点到谷底、从高点到修复的时间：

```python
days_to_trough = (trough_date - peak_date).days

if pd.isna(recovery_date):
    days_to_recovery = np.nan
else:
    days_to_recovery = (recovery_date - peak_date).days

drawdown_event = pd.Series({
    "peak_date": peak_date,
    "trough_date": trough_date,
    "recovery_date": recovery_date,
    "max_drawdown": max_drawdown,
    "days_to_trough": days_to_trough,
    "days_to_recovery": days_to_recovery,
})

print(drawdown_event)
```

回撤深度和持续时间都重要：

- 短而深的回撤考验风控和止损。
- 浅而长的回撤考验资金耐心和策略信心。
- 长期不创新高会带来赎回压力和模型怀疑。

## underwater 区间

drawdown 小于 0 的时期称为 underwater，也就是净值还没回到历史高点。

下面识别每一段 underwater 区间：

```python
def underwater_periods(drawdown_series):
    in_drawdown = drawdown_series < 0
    periods = []
    start = None

    for date, is_underwater in in_drawdown.items():
        if is_underwater and start is None:
            start = date
        elif (not is_underwater) and start is not None:
            periods.append((start, date))
            start = None

    if start is not None:
        periods.append((start, pd.NaT))

    return pd.DataFrame(periods, columns=["start", "end"])


underwater = underwater_periods(drawdown)

print(underwater)
```

如果 `end` 是 `NaT`，说明这段回撤到样本结束还没有修复。

## 从收益序列计算 drawdown

真实回测通常从日收益开始，而不是直接给净值。

构造一个有冲击下跌的日收益序列：

```python
rng = np.random.default_rng(62)

return_dates = pd.bdate_range("2023-01-02", periods=252)

daily_return_values = rng.normal(
    loc=0.0013,
    scale=0.008,
    size=len(return_dates),
)

daily_return_values[70:78] += -0.025
daily_return_values[160:165] += -0.018

daily_return = pd.Series(
    daily_return_values,
    index=return_dates,
    name="daily_return",
)
```

从日收益得到净值：

```python
strategy_nav = (1 + daily_return).cumprod()

strategy_peak = strategy_nav.cummax()
strategy_drawdown = strategy_nav / strategy_peak - 1

print(strategy_nav.tail())
print(strategy_drawdown.min())
```

这里虽然最终净值可能高于初始值，但中间仍可能经历很深的回撤。

这说明正收益策略也可能有难以承受的路径风险。

## 回撤摘要函数

把常用指标封装成函数：

```python
def drawdown_summary(nav_series):
    running_peak = nav_series.cummax()
    drawdown_series = nav_series / running_peak - 1

    max_drawdown = drawdown_series.min()
    trough_date = drawdown_series.idxmin()
    peak_date = nav_series.loc[:trough_date].idxmax()

    recovery_candidates = drawdown_series.loc[trough_date:]
    recovery_candidates = recovery_candidates[recovery_candidates >= 0]

    if recovery_candidates.empty:
        recovery_date = pd.NaT
        days_to_recovery = np.nan
    else:
        recovery_date = recovery_candidates.index[0]
        days_to_recovery = (recovery_date - peak_date).days

    return pd.Series({
        "start_nav": nav_series.iloc[0],
        "end_nav": nav_series.iloc[-1],
        "max_drawdown": max_drawdown,
        "peak_date": peak_date,
        "trough_date": trough_date,
        "recovery_date": recovery_date,
        "days_to_trough": (trough_date - peak_date).days,
        "days_to_recovery": days_to_recovery,
    })


summary = drawdown_summary(strategy_nav)

print(summary)
```

这个函数适合放在回测报告里，与 Sharpe、年化收益、年化波动一起输出。

## Calmar ratio

Calmar ratio 用年化收益除以最大回撤绝对值：

```text
Calmar = annualized_return / abs(max_drawdown)
```

代码：

```python
n_periods = strategy_nav.count()
annualized_return = strategy_nav.iloc[-1] ** (252 / n_periods) - 1

calmar_ratio = annualized_return / abs(summary["max_drawdown"])

print(annualized_return)
print(calmar_ratio)
```

Calmar 更强调下行路径风险。两个 Sharpe 类似的策略，如果一个最大回撤更浅，它的 Calmar 往往更好。

但 Calmar 也有缺点：

- 只使用样本内最糟糕的一次回撤。
- 对样本起止点敏感。
- 如果样本没有经历压力期，可能过于乐观。

## drawdown 和 volatility 的区别

波动率衡量收益围绕均值的离散程度，drawdown 衡量从高点到低点的路径损失。

例如：

- 策略 A 每天小幅震荡，但长期不创新高，drawdown 可能很长。
- 策略 B 波动较高，但经常创新高，drawdown 可能较短。
- 卖期权策略平时波动低，但危机中可能出现深回撤。

因此不能用 Sharpe 或 volatility 替代 drawdown。

回测报告至少应同时包含：

- 年化收益。
- 年化波动。
- Sharpe。
- 最大回撤。
- 回撤持续时间。
- 最差单日或单周收益。

## 常见坑

第一，用收益率直接算回撤。

回撤应该基于净值或累计收益曲线，而不是直接对单期收益做 `cummin`。

第二，忘记用历史高点。

drawdown 是相对历史峰值的下跌，不是相对初始净值的下跌。

第三，只看最大回撤，不看持续时间。

最大回撤浅但持续很久，也可能难以实盘坚持。

第四，只看样本内最大回撤。

历史最大回撤不是未来最大回撤的上限。样本太短会低估极端风险。

第五，忽略未修复回撤。

如果策略当前还在 underwater，`recovery_date` 应该是缺失，而不是样本结束日。

第六，复权、分红和现金流处理错误。

净值序列必须可比。外部申购赎回、分红、拆股、费用计提都会影响回撤计算。

## 实战提示

分析 drawdown 时可以按下面流程：

1. 从可复现的收益序列构造净值。
2. 用 `cummax()` 得到历史峰值。
3. 计算完整 drawdown 序列。
4. 输出最大回撤、峰值日期、谷底日期和修复日期。
5. 统计回撤持续时间和 underwater 区间。
6. 分年份、分策略、分资产查看回撤来源。
7. 将回撤与市场指数、风险因子和持仓暴露对齐分析。
8. 与 Sharpe、turnover、capacity 和压力测试一起判断策略能否实盘承受。

## 小结

本节的重点：

- drawdown 是净值相对历史高点的跌幅。
- 最大回撤是 drawdown 序列的最小值。
- 回撤事件包含 peak、trough、recovery 三个关键日期。
- 回撤深度和持续时间都重要。
- 未修复回撤应明确标记为 `NaT`。
- Calmar ratio 用年化收益除以最大回撤绝对值。
- Sharpe 不能替代 drawdown，二者刻画不同风险。

## 自检问题

1. drawdown 为什么必须基于净值曲线计算？
2. 最大回撤的 peak、trough、recovery 分别是什么意思？
3. 为什么未修复回撤不能把样本结束日当作 recovery date？
4. 最大回撤和波动率有什么区别？
5. Calmar ratio 如何计算，它和 Sharpe 关注点有什么不同？
6. 为什么样本内最大回撤不是未来最大亏损上限？
