# Python 理解项：lookahead bias 前视偏差的时点语义、识别与修正

## 核心概念

lookahead bias 指模型、特征或回测在某个决策时点使用了当时还不可见的信息。

它的核心不是“有没有未来日期”，而是“信息在决策时点是否已经可得”。

同样是日期 `2024-01-05`，不同字段的可见性可能不同：

- 昨日收盘价：今天开盘前通常可见。
- 今日收盘价：今天开盘前不可见。
- 今日 08:30 发布的宏观数据：今天 09:30 可能可见。
- 今日 16:10 发布的公告：今天 09:30 不可见。
- 财报的 `period_end=2023-12-31`：不代表 2023-12-31 已经知道财报值。
- 未来收益：可以作为标签，不能作为当前特征。

判断前视偏差时，要同时写清楚四个时点：

```text
observation_time：数据对应的经济时期或市场时期
available_time：数据实际可见或发布时间
decision_time：策略或模型做决策的时间
target_time：标签或收益实现的时间
```

只要 `available_time > decision_time`，这个字段就不能作为该行特征。

## 准备环境

```python
import numpy as np
import pandas as pd
```

先准备一个小价格序列：

```python
price_dates = pd.to_datetime([
    "2024-01-02",
    "2024-01-03",
    "2024-01-04",
    "2024-01-05",
    "2024-01-08",
])

close = pd.Series(
    [100.0, 102.0, 101.0, 104.0, 103.0],
    index=price_dates,
    name="close",
)

ret = close.pct_change(fill_method=None)

print(close)
print(ret)
```

## 标签可以向未来看，特征不可以

预测下一期收益时，标签天然来自未来。

```python
feature_lag_1d = ret.shift(1).rename("feature_return_lag_1d")
label_fwd_1d = (close.shift(-1) / close - 1.0).rename("target_return_fwd_1d")

example = pd.concat(
    [
        close,
        ret.rename("return_1d"),
        feature_lag_1d,
        label_fwd_1d,
    ],
    axis=1,
)

print(example)
```

这里：

- `feature_return_lag_1d` 是当前行之前已经发生的收益。
- `target_return_fwd_1d` 是当前行之后才会实现的收益。

下面这列虽然代码能跑，但语义是错的：

```python
feature_bad = label_fwd_1d.rename("feature_return_fwd_1d")

bad_example = pd.concat([example, feature_bad], axis=1)

print(bad_example)
```

`feature_return_fwd_1d` 把未来标签伪装成了特征。这是最直接的 lookahead bias。

## 特征名审计

命名不能完全防止前视偏差，但能帮助快速发现明显风险。

```python
def find_suspicious_feature_names(columns):
    bad_tokens = ("fwd", "future", "lead", "target", "label")
    return [
        col
        for col in columns
        if any(token in col.lower() for token in bad_tokens)
    ]


feature_columns = [
    "feature_return_lag_1d",
    "feature_macro_surprise",
    "feature_return_fwd_1d",
    "target_return_fwd_1d",
]

suspicious = find_suspicious_feature_names(feature_columns)

print(suspicious)
```

输出里的列不一定都错，例如 `target_return_fwd_1d` 可以作为标签。但如果它出现在 `X` 特征矩阵里，就应该立即检查。

## 发布时间比日期更重要

下面构造一组宏观数据。每条数据都有明确的发布时间 `release_at`。

```python
decisions = pd.DataFrame({
    "decision_time": pd.to_datetime([
        "2024-01-02 09:30",
        "2024-01-03 09:30",
        "2024-01-04 09:30",
        "2024-01-05 09:30",
        "2024-01-08 09:30",
    ]),
})

macro = pd.DataFrame({
    "release_at": pd.to_datetime([
        "2024-01-03 08:30",
        "2024-01-05 16:10",
        "2024-01-08 08:30",
    ]),
    "macro_surprise": [0.10, -0.20, 0.05],
})

print(decisions)
print(macro)
```

如果决策发生在 09:30，那么 08:30 发布的数据可见，16:10 发布的数据不可见。

正确对齐方式是向后找最近一次已经发布的数据：

```python
safe_macro = pd.merge_asof(
    decisions.sort_values("decision_time"),
    macro.sort_values("release_at"),
    left_on="decision_time",
    right_on="release_at",
    direction="backward",
)

print(safe_macro)
```

错误对齐方式是向前找下一次发布的数据：

```python
leaky_macro = pd.merge_asof(
    decisions.sort_values("decision_time"),
    macro.sort_values("release_at"),
    left_on="decision_time",
    right_on="release_at",
    direction="forward",
)

print(leaky_macro)
```

`direction="forward"` 会把未来才发布的数据贴到过去的决策行上。除非你的任务本来就是寻找下一次事件，否则它不能作为预测特征。

## 可见性断言

可以写一个小函数检查 `available_time <= decision_time`。

```python
def assert_no_lookahead(frame, decision_col, available_col):
    visible = frame[available_col].isna() | (frame[available_col] <= frame[decision_col])

    if not visible.all():
        bad_rows = frame.loc[~visible, [decision_col, available_col]].head()
        raise ValueError(f"lookahead rows found:\n{bad_rows}")


assert_no_lookahead(safe_macro, "decision_time", "release_at")
```

对错误合并结果运行同一个检查：

```python
try:
    assert_no_lookahead(leaky_macro, "decision_time", "release_at")
except ValueError as exc:
    print(type(exc).__name__)
    print(exc)
```

真实项目里，只要特征来自事件、公告、财报、新闻、宏观数据、评级调整或另类数据，都应该保留一个 `available_time` 字段，并在构造训练集后做类似检查。

## 财报期末日不是可见日

财报数据常有两个时间：

- `period_end`：财报覆盖的会计期间结束日。
- `released_at`：财报真正发布的时间。

如果用 `period_end` 对齐，就容易把尚未发布的财报贴到过去。

```python
fundamental = pd.DataFrame({
    "asset": ["AAA", "AAA"],
    "period_end": pd.to_datetime(["2023-12-31", "2024-03-31"]),
    "released_at": pd.to_datetime(["2024-01-05 16:05", "2024-04-05 16:05"]),
    "eps": [1.20, 1.35],
})

fund_decisions = pd.DataFrame({
    "asset": ["AAA", "AAA", "AAA"],
    "decision_time": pd.to_datetime([
        "2024-01-03 09:30",
        "2024-01-08 09:30",
        "2024-04-04 09:30",
    ]),
})
```

错误做法：按 `period_end` 向后合并。

```python
wrong_fundamental = pd.merge_asof(
    fund_decisions.sort_values("decision_time"),
    fundamental.sort_values("period_end"),
    left_on="decision_time",
    right_on="period_end",
    by="asset",
    direction="backward",
)

print(wrong_fundamental)
```

`2024-01-03 09:30` 这行已经拿到了 `2023-12-31` 期末的 EPS，但它实际要到 `2024-01-05 16:05` 才发布。

正确做法：按 `released_at` 向后合并。

```python
right_fundamental = pd.merge_asof(
    fund_decisions.sort_values("decision_time"),
    fundamental.sort_values("released_at"),
    left_on="decision_time",
    right_on="released_at",
    by="asset",
    direction="backward",
)

print(right_fundamental)

assert_no_lookahead(right_fundamental, "decision_time", "released_at")
```

财务数据、分析师预期、指数成分、评级调整都要按当时可见版本对齐，而不是按事件所属期间对齐。

## bfill 会把未来填到过去

`ffill` 和 `bfill` 都能填缺失值，但时间语义完全不同。

```python
sparse_signal = pd.Series(
    [np.nan, 0.10, np.nan, -0.20, np.nan],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
    ]),
    name="event_value",
)

filled = pd.DataFrame({
    "raw": sparse_signal,
    "ffill": sparse_signal.ffill(),
    "bfill": sparse_signal.bfill(),
})

print(filled)
```

如果 `0.10` 是 `2024-01-03` 才知道的值，那么 `bfill` 把它填到 `2024-01-02` 就是前视偏差。

在时间序列预测里，默认优先使用 `ffill`，并且要确认被前向填充的值在填充时点已经可见。

## center=True 的窗口也会前视

中心窗口会用到当前行之后的数据。

```python
centered = close.rolling(3, center=True).mean()

print(centered)
```

`2024-01-03` 的中心窗口使用：

```text
2024-01-02, 2024-01-03, 2024-01-04
```

如果决策发生在 `2024-01-03`，那么 `2024-01-04` 还不可见。`center=True` 可以用于离线平滑和画图，但通常不能作为预测特征。

## 时点审计表

做复杂特征时，建议为每一类特征维护一张时点审计表：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| feature_name | 特征名 | `macro_surprise` |
| observation_time | 数据对应时期 | `2024-01` |
| available_time | 实际可见时间 | `2024-01-05 16:10` |
| decision_time | 使用该特征做决策的时间 | `2024-01-08 09:30` |
| source | 数据来源 | macro release |
| transformation | 变换方式 | backward asof + ffill |

只要能系统性地回答“这行特征在这个决策时点为什么已经可见”，前视偏差就会少很多。

## 常见坑

第一，把 `shift(-1)` 结果放进特征。

`shift(-1)` 经常用于构造未来标签，但如果进入特征矩阵，就是直接前视。

第二，用发布日期以外的日期对齐事件数据。

财报的期末日、新闻的事件日、评级对应的覆盖日期，都不一定是数据可见日。预测中应使用发布时间或可见时间。

第三，`merge_asof(direction="forward")`。

它会找未来最近事件。很多事件研究可以用它找下一次事件，但预测特征通常不应使用。

第四，`bfill` 修补历史缺失。

`bfill` 会把未来值填回过去。除非是离线数据清洗并且不会进入预测特征，否则要非常谨慎。

第五，日频数据忽略日内发布时间。

同一天发布的数据不一定同一时刻可见。开盘前、盘中、收盘后发布，对交易决策含义完全不同。

## 实战提示

防止 lookahead bias，可以按下面的习惯写代码：

1. 特征表里保留 `decision_time` 和每类外部数据的 `available_time`。
2. 事件数据用 `merge_asof(..., direction="backward")`，并检查 `available_time <= decision_time`。
3. 财报、公告、新闻、宏观数据按发布时间对齐，不按覆盖期末日对齐。
4. 特征列名避免 `future`、`fwd`、`lead`、`target`、`label`。
5. 标签列可以用 `fwd`，但必须和特征列清单分开。
6. 时间序列填充优先 `ffill`，避免无审计地使用 `bfill`。
7. rolling 特征避免 `center=True`，预测特征通常显式 `shift(1)`。
8. 对关键数据源写小样本单元测试，专门断言没有 `available_time > decision_time`。

## 小结

本节的重点：

- lookahead bias 是决策时点使用了尚不可见的信息。
- 是否前视取决于 `available_time` 和 `decision_time`，不只取决于日期大小。
- 未来收益可以作为标签，不能作为当前特征。
- `merge_asof(direction="forward")`、`bfill`、`center=True` 都可能把未来信息贴到过去。
- 财报、公告、宏观数据要按发布时间对齐。
- 保留 `available_time` 并写可见性断言，是防止前视偏差的工程基础。

## 自检问题

1. lookahead bias 和 backtest leakage 的区别是什么？
2. 为什么财报的 `period_end` 不能直接当作可见时间？
3. `merge_asof(direction="backward")` 和 `direction="forward"` 在预测特征里有什么区别？
4. 为什么 `bfill` 在时间序列预测中危险？
5. 一个特征表至少应该保留哪些时点字段来审计前视偏差？
