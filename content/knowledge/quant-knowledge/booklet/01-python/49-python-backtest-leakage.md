# 49. Python 理解项：backtest leakage 回测泄露的来源、检测与修正

## 核心概念

backtest leakage 指回测过程使用了在真实交易时不可获得、或不应参与评估决策的信息。

它比 lookahead bias 更宽。lookahead bias 主要是“看到了未来”；backtest leakage 还包括：

- 用未来收益、未来成分、未来财报修订值构造特征。
- 用全样本拟合标准化、缺失值填充、行业分类或特征选择。
- 用测试期表现挑策略、挑参数、挑样本池。
- 用幸存者样本替代真实历史样本池。
- 信号生成时点和成交时点不一致。
- 忽略手续费、滑点、停牌、涨跌停、可交易性限制。

回测泄露的危险在于它通常不会报错。代码能跑，曲线也很好看，但结果不能代表真实可交易表现。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一个小型价格矩阵。行是日期，列是资产。

```python
dates = pd.to_datetime([
    "2024-01-02",
    "2024-01-03",
    "2024-01-04",
    "2024-01-05",
    "2024-01-08",
    "2024-01-09",
    "2024-01-10",
    "2024-01-11",
    "2024-01-12",
    "2024-01-16",
])

close = pd.DataFrame(
    {
        "AAA": [100.0, 102.0, 101.0, 104.0, 103.0, 105.0, 107.0, 106.0, 108.0, 109.0],
        "BBB": [50.0, 49.0, 50.0, 51.0, 50.0, 52.0, 51.0, 53.0, 54.0, 53.0],
        "CCC": [80.0, 81.0, 83.0, 82.0, 84.0, 83.0, 85.0, 86.0, 84.0, 87.0],
    },
    index=dates,
)

close.index.name = "date"
close.columns.name = "asset"

ret = close.pct_change(fill_method=None)
future_ret_1d = close.shift(-1) / close - 1.0

print(close)
print(ret)
print(future_ret_1d)
```

`ret.loc[t]` 是从上一个交易日到 `t` 的收益。`future_ret_1d.loc[t]` 是从 `t` 到下一个交易日的收益，通常只能作为标签或回测实现收益，不能作为日期 `t` 的特征。

## 一个最小回测函数

下面的函数做一个很简单的横截面多空回测：

- 每天选 signal 最高的资产做多。
- 每天选 signal 最低的资产做空。
- 用同一天索引上的 `forward_return` 计算下一期多空收益。

```python
def long_short_backtest(signal, forward_return):
    rows = []
    long_assets = []
    short_assets = []

    for date in signal.index:
        score = signal.loc[date].dropna()
        realized = forward_return.loc[date].dropna()
        assets = score.index.intersection(realized.index)

        if len(assets) < 2:
            rows.append(np.nan)
            long_assets.append(None)
            short_assets.append(None)
            continue

        score = score.loc[assets]
        long_asset = score.idxmax()
        short_asset = score.idxmin()

        rows.append(realized.loc[long_asset] - realized.loc[short_asset])
        long_assets.append(long_asset)
        short_assets.append(short_asset)

    return pd.DataFrame(
        {
            "strategy_return": rows,
            "long": long_assets,
            "short": short_assets,
        },
        index=signal.index,
    )
```

再写一个简单汇总函数：

```python
def summarize_strategy(result):
    r = result["strategy_return"].dropna()
    return pd.Series({
        "n": len(r),
        "mean": r.mean(),
        "sum": r.sum(),
        "compound": (1.0 + r).prod() - 1.0,
        "hit_rate": (r > 0).mean(),
    })
```

真实回测还要考虑仓位、杠杆、交易成本、换手、约束和成交规则。这里先用最小版本讲清楚泄露问题。

## 泄露 1：直接用未来收益做信号

最明显的泄露是把未来收益当成信号。

```python
signal_bad = future_ret_1d

bad_result = long_short_backtest(signal_bad, future_ret_1d)
bad_summary = summarize_strategy(bad_result)

print(bad_result)
print(bad_summary)
```

这相当于每天提前知道下一期哪只资产涨得最多、哪只资产跌得最多。多空收益自然几乎完美。

一个不看未来的简单信号可以用滞后收益：

```python
signal_safe = ret.shift(1)

safe_result = long_short_backtest(signal_safe, future_ret_1d)
safe_summary = summarize_strategy(safe_result)

print(safe_result)
print(safe_summary)
```

对比结果：

```python
comparison = pd.DataFrame({
    "bad_future_signal": bad_summary,
    "safe_lag_signal": safe_summary,
})

print(comparison)
```

如果一个新因子回测胜率接近 100%、每天都抓住最大涨幅和最大跌幅，第一反应应该是检查泄露，而不是庆祝。

## 泄露 2：同日信号和同日收益混用

执行时点也会造成泄露。

假设 `ret.loc[t]` 要等到 `t` 收盘后才能知道。如果你用它生成信号，却又把它用于同一段收益，就等于先知道当天赢家再买入。

错误写法：

```python
same_day_execution = long_short_backtest(ret, ret)

print(same_day_execution)
print(summarize_strategy(same_day_execution))
```

更合理的写法是：用 `t` 收盘后才能得到的信号，去交易下一期收益。

```python
next_period_execution = long_short_backtest(ret, future_ret_1d)

print(next_period_execution)
print(summarize_strategy(next_period_execution))
```

同一个信号，错误执行时点和正确执行时点的表现可能完全相反。

写回测前必须明确：

- 信号在什么时候生成？
- 价格在什么时候可见？
- 订单在什么时候提交？
- 成交价是什么？
- 收益区间从什么时候到什么时候？

## 泄露 3：全样本标准化

另一个常见泄露是用全样本统计量处理特征。

下面的因子本身是安全的滞后收益：

```python
factor = ret.shift(1)
```

但如果用完整样本的均值和标准差标准化，就把未来分布信息带进了早期日期。

```python
def finite_values(frame):
    values = frame.to_numpy(dtype=float).ravel()
    return values[np.isfinite(values)]


def full_sample_zscore(frame):
    values = finite_values(frame)
    return (frame - values.mean()) / values.std(ddof=0)


full_z = full_sample_zscore(factor)

print(full_z)
```

更接近真实在线流程的是只用当前日期之前的历史估计标准化参数：

```python
def causal_global_zscore(frame):
    out = pd.DataFrame(index=frame.index, columns=frame.columns, dtype=float)

    for i, date in enumerate(frame.index):
        history = frame.iloc[:i]
        values = finite_values(history)

        if len(values) < 2:
            continue

        scale = values.std(ddof=0)
        if np.isclose(scale, 0.0):
            scale = 1.0

        out.loc[date] = (frame.loc[date] - values.mean()) / scale

    return out


causal_z = causal_global_zscore(factor)

print(causal_z)
```

比较某一天的差异：

```python
z_compare = pd.DataFrame({
    "full_sample": full_z.loc["2024-01-05"],
    "causal": causal_z.loc["2024-01-05"],
})

print(z_compare)
```

全样本标准化未必每天都让收益变好，但它破坏了评估口径。训练、验证、测试和线上都应该使用只在训练期或历史窗口中学到的状态。

## 泄露 4：用测试期挑策略

测试集只能用于最后评估一次。如果看过测试集表现后再挑策略、改参数、删特征，测试集就变成了训练过程的一部分。

构造两个候选信号：

```python
candidate_signals = {
    "lag_return": ret.shift(1),
    "mean_reversion": -ret.shift(1),
}
```

写一个候选策略评估函数：

```python
def evaluate_candidates(candidate_signals, forward_return, split_date):
    split_date = pd.Timestamp(split_date)
    rows = []

    for name, signal in candidate_signals.items():
        result = long_short_backtest(signal, forward_return)
        r = result["strategy_return"]

        train_sum = r.loc[r.index <= split_date].dropna().sum()
        test_sum = r.loc[r.index > split_date].dropna().sum()

        rows.append({
            "signal": name,
            "train_sum": train_sum,
            "test_sum": test_sum,
        })

    return pd.DataFrame(rows)


candidate_report = evaluate_candidates(
    candidate_signals,
    future_ret_1d,
    split_date="2024-01-10",
)

print(candidate_report)
```

正确选择：只看训练期或验证期。

```python
best_by_train = candidate_report.sort_values("train_sum", ascending=False).iloc[0]

print(best_by_train)
```

泄露选择：看测试期以后挑表现最好的。

```python
best_by_test = candidate_report.sort_values("test_sum", ascending=False).iloc[0]

print(best_by_test)
```

在这个小例子里，训练期更好的信号和测试期更好的信号相反。如果你先看测试期再选 `mean_reversion`，后续报告的测试表现就是被污染的。

## 泄露 5：用最终赢家定义样本池

样本池也可能泄露。

如果先看完整区间，挑最终涨得最好的资产，再回头做组合，这就用了未来信息。

```python
final_total_return = close.iloc[-1] / close.iloc[0] - 1.0
leaky_survivors = final_total_return.nlargest(2).index.tolist()

print(final_total_return)
print(leaky_survivors)
```

比较全样本资产池和“最终赢家资产池”的等权组合：

```python
all_asset_portfolio = future_ret_1d.mean(axis=1).dropna()
survivor_portfolio = future_ret_1d[leaky_survivors].mean(axis=1).dropna()

sample_pool_compare = pd.DataFrame({
    "all_assets": all_asset_portfolio,
    "chosen_by_final_return": survivor_portfolio,
})

print(sample_pool_compare)
print(sample_pool_compare.sum())
```

真实研究里，样本池应来自 point-in-time 数据：

- 当天实际上市并可交易的证券。
- 当天实际属于某指数或行业的证券。
- 当天未停牌、未涨跌停、满足流动性约束的证券。
- 包含后来退市、合并、长期停牌或表现很差的资产。

只保留今天仍存在的资产，会产生幸存者偏差。

## 泄露 6：忽略交易成本和可交易性

有些回测没有直接看未来，但仍然过于乐观。

例如：

- 用收盘价产生信号，也假设按同一个收盘价成交。
- 忽略调仓换手导致的手续费和滑点。
- 假设涨停可以买入、跌停可以卖出。
- 假设停牌资产可以随时交易。
- 假设大资金可以按小成交量资产的中间价成交。

这些不一定是严格的信息泄露，但会让回测收益不可实现。实战中应把交易成本和可交易性约束显式纳入回测。

## 泄露检查清单

检查一个回测时，可以按下面的顺序问：

1. 特征列有没有 `future`、`fwd`、`lead`、`shift(-1)` 这类未来含义？
2. rolling、expanding、标准化、填充、winsorize 是否只用训练期或历史窗口？
3. 样本池、行业分类、指数成分、财务数据是否是 point-in-time？
4. 调参、选特征、选策略是否只用训练期或验证期？
5. 测试集是否只在最终报告时评估一次？
6. 信号时点、下单时点、成交时点和收益区间是否一致？
7. 回测是否包含手续费、滑点、停牌、涨跌停和容量限制？
8. 如果把信号整体滞后一日，表现是否大幅变化？
9. 如果打乱标签或使用随机信号，回测是否仍然异常好？
10. 每个结果是否能追溯到对应的数据版本和代码版本？

## 常见坑

第一，用未来收益做排序、分组或筛选。

这种错误通常会带来极高胜率，是最直接的泄露。

第二，全样本预处理。

全样本均值、全样本标准差、全样本缺失值填充、全样本 winsorize 都会把未来分布信息带到过去。

第三，测试集反复使用。

只要根据测试集表现继续改策略，测试集就不再是独立检验。

第四，样本池不是历史真实样本池。

只用当前还存在的股票、当前指数成分、当前行业分类，都会污染历史评估。

第五，执行时点没写清楚。

信号、成交和收益区间错一格，回测可能从普通策略变成完美策略。

## 实战提示

降低 backtest leakage 的做法：

1. 在代码里明确命名 `feature_*`、`target_*`、`return_fwd_*`。
2. 先生成时间安全的特征，再按时间切训练、验证、测试。
3. 有状态预处理只在训练集上 `fit`。
4. 每次调参只使用训练期内部交叉验证或验证集。
5. 测试集只评估一次，并记录测试前已经确定的配置。
6. 样本池、财务数据、指数成分使用 point-in-time 版本。
7. 回测函数要求显式传入 `signal_time`、`trade_time` 或至少明确 shift 规则。
8. 对关键假设写小样本单元测试。

## 小结

本节的重点：

- backtest leakage 是任何污染回测评估的信息或流程错误。
- 直接用未来收益是最明显的泄露。
- 同日信号和同日收益混用会造成执行时点泄露。
- 全样本标准化和全样本样本池也会污染结果。
- 用测试期挑策略会让测试集失去独立性。
- 样本池必须 point-in-time，不能用最终赢家或幸存者倒推历史。
- 回测要显式处理信号时点、成交时点、交易成本和可交易性。

## 自检问题

1. backtest leakage 和 lookahead bias 有什么区别？
2. 为什么 `future_ret_1d` 可以作为标签，但不能作为特征？
3. 全样本标准化为什么会污染早期日期？
4. 为什么看测试期表现后再选策略会让测试集失效？
5. 样本池为什么必须使用 point-in-time 数据？
