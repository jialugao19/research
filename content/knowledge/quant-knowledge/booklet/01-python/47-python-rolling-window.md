# 47. Python 理解项：rolling window 窗口语义、边界与性能

## 核心概念

rolling window 的核心问题不是“怎么调用 `.rolling()`”，而是：

```text
某一行的窗口结果，到底使用了哪些观测？
这些观测在预测时点是否已经可见？
窗口边界、缺失值和分组是否符合业务语义？
```

rolling window 常用于：

- 过去 N 期均值、标准差、最大值、最小值。
- 动量、波动率、换手率、成交额均值。
- 时间序列特征。
- 风险指标和滚动监控。

但 rolling 也常带来隐性 bug：

- 默认窗口包含当前行。
- 固定行数窗口和时间长度窗口语义不同。
- `min_periods` 会改变样本有效范围。
- `center=True` 会使用未来数据。
- 长表里忘记按资产分组会串数据。
- 自定义 `rolling.apply` 可能非常慢。

## 准备环境

```python
from collections import deque
import timeit

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
```

准备一个价格序列：

```python
dates = pd.to_datetime([
    "2024-01-02",
    "2024-01-03",
    "2024-01-04",
    "2024-01-05",
    "2024-01-08",
    "2024-01-09",
])

close = pd.Series(
    [100.0, 102.0, 101.0, 105.0, 104.0, 106.0],
    index=dates,
    name="close",
)

returns = close.pct_change(fill_method=None)
```

## 固定行数窗口

`rolling(window=3)` 表示每一行使用最近 3 个观测。

```python
rolling_mean_3 = close.rolling(window=3).mean()

print(rolling_mean_3)
```

默认 `min_periods` 等于 `window`，所以前两个位置是缺失值。

第 3 个结果使用：

```text
2024-01-02, 2024-01-03, 2024-01-04
```

可以手动验证：

```python
manual_third = close.iloc[0:3].mean()

print(manual_third)
print(rolling_mean_3.iloc[2])
```

固定行数窗口不关心日期间隔，只关心有多少行。

## 窗口默认包含当前行

rolling 默认包含当前行。

```python
current_included = close.rolling(3).mean()

print(current_included.loc["2024-01-04"])
```

`2024-01-04` 的结果使用 `2024-01-02`、`2024-01-03`、`2024-01-04` 三个价格。

如果要构造“截至昨天”的特征，通常先 `shift(1)`：

```python
past_only = close.shift(1).rolling(3).mean()

print(past_only.loc["2024-01-05"])
```

`2024-01-05` 的 `past_only` 使用的是 `2024-01-02`、`2024-01-03`、`2024-01-04`，不包含 `2024-01-05`。

## min_periods 的含义

`min_periods` 控制窗口内至少有多少个非缺失值才输出结果。

```python
mean_min1 = close.rolling(window=3, min_periods=1).mean()
mean_min3 = close.rolling(window=3, min_periods=3).mean()

print(mean_min1)
print(mean_min3)
```

`min_periods=1` 会让序列开头更早产生结果，但这些结果基于较少观测，统计含义和完整窗口不同。

可以配合 `count()` 检查每个窗口有效样本数：

```python
window_count = close.rolling(window=3, min_periods=1).count()

print(window_count)
```

研究报告里如果混用不完整窗口和完整窗口，最好明确说明。

## 时间长度窗口

如果 index 是 `DatetimeIndex`，rolling 可以使用时间长度。

```python
irregular = pd.Series(
    [1.0, 2.0, 3.0, 4.0],
    index=pd.to_datetime([
        "2024-01-01",
        "2024-01-02",
        "2024-01-04",
        "2024-01-05",
    ]),
)

rolling_3d = irregular.rolling("3D").sum()

print(rolling_3d)
```

`rolling("3D")` 表示最近 3 个日历日内的观测。因为日期不均匀，每个窗口里的行数可能不同。

默认时间窗口通常是左开右闭，也就是包含当前时间点，不包含左边界端点。

## closed 参数

时间窗口可以用 `closed` 控制边界。

```python
sum_default = irregular.rolling("3D").sum()
sum_left = irregular.rolling("3D", closed="left").sum()
sum_both = irregular.rolling("3D", closed="both").sum()

print(sum_default)
print(sum_left)
print(sum_both)
```

直觉上：

- 默认窗口包含当前点。
- `closed="left"` 排除当前点，常用于“只看当前点之前”的时间窗口。
- `closed="both"` 两端都包含。

不过预测特征里，`shift(1)` 往往比依赖 `closed` 更清楚，尤其是固定行数窗口和分组窗口。

## center=True 的风险

`center=True` 会把结果标签放到窗口中心。

```python
centered = close.rolling(3, center=True).mean()

print(centered)
```

`2024-01-03` 的 centered 结果会使用：

```text
2024-01-02, 2024-01-03, 2024-01-04
```

如果在 `2024-01-03` 做预测，这就用了未来的 `2024-01-04`。因此 `center=True` 通常只适合离线平滑和画图，不适合作为预测特征。

## 预测特征和标签对齐

预测下一期收益时，可以这样构造数据集：

```python
feature_vol = returns.shift(1).rolling(3, min_periods=3).std()
label_fwd = (close.shift(-1) / close - 1.0).rename("return_fwd_1d")

dataset = pd.concat(
    [
        feature_vol.rename("vol_past_3d"),
        label_fwd,
    ],
    axis=1,
).dropna()

print(dataset)
```

这里每一行：

- `vol_past_3d` 只使用当前日期之前的收益。
- `return_fwd_1d` 是未来 1 日收益，用作标签。

特征可以向过去看，标签可以向未来看；不能反过来。

## 长表必须按实体分组

长表数据里，rolling 必须在每个资产内部进行。

```python
long = pd.DataFrame({
    "date": pd.to_datetime([
        "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
        "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
    ]),
    "asset": ["AAA", "AAA", "AAA", "AAA", "BBB", "BBB", "BBB", "BBB"],
    "return": [0.01, -0.02, 0.03, 0.00, -0.01, 0.02, 0.01, -0.02],
})

long = long.sort_values(["asset", "date"]).reset_index(drop=True)
```

错误写法：

```python
long["roll_bad"] = long["return"].shift(1).rolling(2).mean()
```

这会在资产边界处把 AAA 的最后一行带到 BBB 的第一行。

正确写法：

```python
long["roll_good"] = (
    long
    .groupby("asset")["return"]
    .transform(lambda s: s.shift(1).rolling(2, min_periods=2).mean())
)

print(long[["date", "asset", "return", "roll_bad", "roll_good"]])
```

核心模板：

```python
grouped_feature = (
    long
    .sort_values(["asset", "date"])
    .groupby("asset")["return"]
    .transform(lambda s: s.shift(1).rolling(20, min_periods=20).mean())
)
```

先排序，再分组，再在组内 shift 和 rolling。

## rolling.apply

内置聚合通常最快，例如 `.mean()`、`.std()`、`.sum()`。

自定义逻辑可以用 `rolling.apply`。

```python
def downside_mean(values):
    values = np.asarray(values)
    downside = values[values < 0]
    if len(downside) == 0:
        return 0.0
    return float(downside.mean())


downside = returns.rolling(3, min_periods=3).apply(
    downside_mean,
    raw=True,
)

print(downside)
```

`raw=True` 会把窗口作为 NumPy 数组传入，通常比传 Series 更快。

但 `rolling.apply` 仍然会对每个窗口调用一次 Python 函数。窗口很多时，它可能比内置方法慢很多。

## rolling apply 的性能对比

可以用 `timeit` 粗略比较内置均值和自定义均值。

```python
big = pd.Series(np.random.default_rng(0).normal(size=10_000))

builtin_seconds = min(
    timeit.repeat(lambda: big.rolling(20).mean(), number=3, repeat=3)
)

apply_seconds = min(
    timeit.repeat(
        lambda: big.rolling(20).apply(np.mean, raw=True),
        number=3,
        repeat=3,
    )
)

print(builtin_seconds)
print(apply_seconds)
```

不要依赖一次计时做结论，但通常内置 rolling 聚合会更高效。

## NumPy sliding_window_view

NumPy 可以用 `sliding_window_view` 生成滑动窗口视图。

```python
values = close.to_numpy()
windows = sliding_window_view(values, window_shape=3)

window_mean = windows.mean(axis=1)

window_mean_series = pd.Series(
    window_mean,
    index=close.index[2:],
    name="mean_3",
)

print(windows.shape)
print(window_mean_series)
```

`windows.shape == (len(values) - 3 + 1, 3)`。它很适合理解窗口，也适合某些 NumPy 批量计算。

注意：窗口视图可能让逻辑数组形状变得很大。即使底层是视图，后续聚合或复制也可能消耗大量内存。

## 流式 rolling sum

有些场景不需要 pandas，可以用队列维护窗口。

```python
def rolling_sum_stream(values, window):
    q = deque()
    total = 0.0
    out = []

    for value in values:
        q.append(value)
        total += value

        if len(q) > window:
            total -= q.popleft()

        if len(q) == window:
            out.append(total)
        else:
            out.append(np.nan)

    return np.array(out)


stream_sum = rolling_sum_stream(close.to_numpy(), window=3)

print(stream_sum)
```

这种写法每来一个新值只更新一次总和，适合在线计算或很长的数据流。缺点是需要自己管理边界和缺失值。

## 缺失值和 rolling

rolling 聚合通常会跳过缺失值，但受 `min_periods` 控制。

```python
with_nan = pd.Series([1.0, np.nan, 3.0, 4.0])

mean_nan = with_nan.rolling(3, min_periods=2).mean()
count_nan = with_nan.rolling(3, min_periods=1).count()

print(mean_nan)
print(count_nan)
```

这里窗口内有效值数量不足 `min_periods` 时，结果是 NaN。

对金融数据，缺失值可能代表停牌、未上市、数据缺失或不在资产池中。rolling 前应先定义业务含义，而不是盲目填充。

## 常见坑

第一，忘记 rolling 默认包含当前行。

预测特征通常要先 `shift(1)`，确保只用过去数据。

第二，把固定行数窗口当成时间窗口。

`rolling(20)` 是 20 个观测，不一定是 20 个自然日。数据缺日期或不规则时，两者差异很大。

第三，长表没有按实体分组。

不分组 rolling 会让一个资产的历史流入另一个资产。

第四，过度使用 `rolling.apply`。

自定义函数灵活，但可能慢。优先使用内置聚合、向量化或专门算法。

第五，忽略 `min_periods`。

不完整窗口和完整窗口统计含义不同。样本开始阶段要特别小心。

## 实战提示

写 rolling 特征前，先回答：

1. 窗口是最近 N 行，还是最近 N 天 / 分钟？
2. 当前行是否允许进入窗口？
3. 最少需要多少有效观测？
4. 数据是否需要按资产、用户、合约分组？
5. 结果 index 是否和标签对齐？
6. 是否存在缺失值？缺失值代表什么？
7. 内置 rolling 聚合是否已经足够？

一个安全模板：

```python
def past_rolling_feature(frame, group_col, time_col, value_col, window, min_periods=None):
    if min_periods is None:
        min_periods = window

    frame = frame.sort_values([group_col, time_col]).copy()

    feature = (
        frame
        .groupby(group_col)[value_col]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=min_periods).mean())
    )

    return feature


long["past_mean_2"] = past_rolling_feature(
    long,
    group_col="asset",
    time_col="date",
    value_col="return",
    window=2,
)

print(long[["date", "asset", "return", "past_mean_2"]])
```

这个模板强制排序、分组、先 shift 再 rolling，适合作为预测特征的基础形式。

## 小结

本节的重点：

- rolling window 的核心是窗口成员和边界语义。
- 固定行数窗口和时间长度窗口不同。
- pandas rolling 默认包含当前行。
- 预测特征常用 `shift(1).rolling(...)`。
- `min_periods` 决定不完整窗口是否输出。
- 长表数据必须按实体分组 rolling。
- 内置 rolling 聚合通常比 `rolling.apply` 更快。
- `sliding_window_view` 适合理解窗口和部分 NumPy 批量计算，但要注意内存形状。

## 自检问题

1. `rolling(3)` 的第 3 个结果默认使用哪些观测？
2. 为什么预测特征里常写 `shift(1).rolling(...)`？
3. `rolling(20)` 和 `rolling("20D")` 有什么区别？
4. 长表数据为什么必须先按资产分组再 rolling？
5. `rolling.apply` 灵活但有什么性能风险？
