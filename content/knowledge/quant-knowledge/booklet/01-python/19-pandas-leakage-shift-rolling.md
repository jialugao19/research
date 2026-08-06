# pandas：常见泄露：shift、rolling、未来函数

## 核心概念

时间序列和量化研究里，未来信息泄露不是指代码报错，而是指模型或回测在日期 `t` 使用了当时还不知道的信息。

写 pandas 特征时，至少要分清三个时点：

- 预测时点：什么时候做决策。
- 特征时点：特征里的信息最晚来自什么时候。
- 标签时点：要预测的目标发生在什么时候。

如果日期 `t` 的特征用了 `t+1` 才知道的数据，就是泄露。泄露后的回测通常看起来更平滑、更高收益、更高 IC，但上线后会失效。

## 准备数据

下面用一个简单的收盘价矩阵演示。行是日期，列是资产。

```python
import numpy as np
import pandas as pd

close = pd.DataFrame(
    {
        "AAA": [100.0, 102.0, 101.0, 103.0, 104.0, 103.0, 105.0],
        "BBB": [50.0, 49.0, 51.0, 50.0, 52.0, 53.0, 52.0],
    },
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
        "2024-01-09",
        "2024-01-10",
    ]),
)

close.index.name = "date"
close.columns.name = "asset"

ret = close.pct_change(fill_method=None)

print(close)
print(ret)
```

这里 `ret.loc["2024-01-05"]` 是从 `2024-01-04` 收盘到 `2024-01-05` 收盘的收益。它在 `2024-01-05` 收盘后才完整可见。

## shift 的方向

`shift(1)` 把过去值移到当前行，常用于构造滞后特征。

```python
s = pd.Series(
    [10.0, 20.0, 30.0],
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
    name="x",
)

lag1 = s.shift(1)

print(lag1)
```

结果里，`2024-01-03` 这一行拿到的是 `2024-01-02` 的值。

`shift(-1)` 把未来值移到当前行，通常用于构造标签。

```python
lead1 = s.shift(-1)

print(lead1)
```

结果里，`2024-01-03` 这一行拿到的是 `2024-01-04` 的值。如果这列被当成特征，就是明显的未来信息泄露。

## 标签可以用未来，特征不可以

预测下一天收益时，常见标签是从日期 `t` 到 `t+1` 的未来收益。

```python
future_ret_1d = close.shift(-1) / close - 1.0

print(future_ret_1d)
```

这列可以作为训练标签：

```python
label = future_ret_1d.rename_axis(index="date", columns="asset")
```

但它不能作为日期 `t` 的特征。命名上可以直接提醒自己：

- `return_fwd_1d`：未来 1 日收益，标签。
- `return_lag_1d`：滞后 1 日收益，特征。

例如滞后收益特征可以这样写：

```python
return_lag_1d = ret.shift(1)

print(return_lag_1d)
```

如果你的决策发生在日期 `t` 收盘后，并且使用 `t` 收盘价预测 `t+1`，那么 `ret.loc[t]` 已经可见；如果决策发生在日期 `t` 开盘前，则 `ret.loc[t]` 还不可见，应该使用 `ret.shift(1).loc[t]`。

## rolling 默认包含当前行

`rolling` 默认包含当前行。

```python
rolling_mean_bad = ret.rolling(3, min_periods=3).mean()

print(rolling_mean_bad)
```

这不一定总是错。关键取决于预测时点：

- 如果在日期 `t` 收盘后生成特征，用 `t` 的收盘收益可能合理。
- 如果在日期 `t` 收盘前生成特征，`ret.loc[t]` 还不知道，直接 rolling 会泄露。

更保守、也更常见的“截至昨天”写法是先 `shift(1)`：

```python
rolling_mean_safe = ret.shift(1).rolling(3, min_periods=3).mean()

print(rolling_mean_safe)
```

这表示日期 `t` 的 rolling 特征只用到 `t-1` 及以前的收益。

## rolling(center=True) 通常不能做预测特征

`center=True` 会把窗口结果放在窗口中心，因此会使用当前行之后的数据。

```python
centered = ret["AAA"].rolling(3, center=True, min_periods=3).mean()

print(centered)
```

例如 `2024-01-05` 这一行的中心窗口，会用到 `2024-01-08` 的收益。这个值在 `2024-01-05` 做决策时还不可见。

`center=True` 可以用于画图平滑或离线描述，但通常不应进入预测特征。

## 长表里必须按资产 shift 和 rolling

长表数据容易出现另一类泄露：忘记按资产分组，导致一只股票的历史跑到另一只股票的特征里。

```python
long = (
    close
    .stack(future_stack=True)
    .rename("close")
    .reset_index()
    .sort_values(["asset", "date"])
    .reset_index(drop=True)
)

long["return"] = (
    long
    .groupby("asset")["close"]
    .transform(lambda x: x.pct_change(fill_method=None))
)

print(long)
```

错误写法是在全表上直接 `shift` 或 `rolling`：

```python
long["return_lag_bad"] = long["return"].shift(1)
```

这会在资产边界处串数据。例如 BBB 的第一行可能拿到 AAA 的最后一行收益。

正确写法是在每只资产内部移动：

```python
long["return_lag_1d"] = long.groupby("asset")["return"].shift(1)

long["rolling_mean_3d"] = (
    long
    .groupby("asset")["return"]
    .transform(lambda x: x.shift(1).rolling(3, min_periods=3).mean())
)

print(long[["date", "asset", "return", "return_lag_bad", "return_lag_1d", "rolling_mean_3d"]])
```

时间序列特征的基本模板是：

```python
long = long.sort_values(["asset", "date"])
feature = long.groupby("asset")["value"].transform(
    lambda x: x.shift(1).rolling(20, min_periods=20).mean()
)
```

先排序，再分组，再在组内 `shift` 和 `rolling`。

## 横截面处理和全样本处理

如果日期 `t` 同一时刻所有股票的因子都已经可见，那么按日期做横截面排名通常不泄露。

```python
factor_long = long.dropna(subset=["return_lag_1d"]).copy()
factor_long["factor"] = factor_long["return_lag_1d"]

factor_long["rank_by_date"] = (
    factor_long
    .groupby("date")["factor"]
    .rank(pct=True)
)

print(factor_long[["date", "asset", "factor", "rank_by_date"]])
```

但对全样本做标准化经常会泄露未来分布。

```python
factor_long["z_full_sample_bad"] = (
    (factor_long["factor"] - factor_long["factor"].mean())
    / factor_long["factor"].std()
)
```

这行代码用了整个数据集的均值和标准差，包括未来日期。用于研究描述未必不行，用于训练或回测特征就有风险。

如果需要时间序列标准化，可以用每只资产过去窗口的均值和标准差：

```python
factor_long = factor_long.sort_values(["asset", "date"]).copy()

past_mean = factor_long.groupby("asset")["factor"].transform(
    lambda x: x.shift(1).rolling(3, min_periods=3).mean()
)
past_std = factor_long.groupby("asset")["factor"].transform(
    lambda x: x.shift(1).rolling(3, min_periods=3).std()
)

factor_long["z_past_3d"] = (factor_long["factor"] - past_mean) / past_std

print(factor_long[["date", "asset", "factor", "z_full_sample_bad", "z_past_3d"]])
```

这里日期 `t` 的标准化参数来自 `t` 之前的窗口。

## merge_asof 的方向

另一类常见泄露来自把财报、公告、宏观数据合并到价格数据时用错方向。

```python
prices = pd.DataFrame({
    "date": pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
    ]),
    "close": [100.0, 101.0, 103.0, 102.0],
})

events = pd.DataFrame({
    "released_at": pd.to_datetime(["2024-01-03", "2024-01-05"]),
    "score": [0.8, 0.3],
})

safe_join = pd.merge_asof(
    prices,
    events,
    left_on="date",
    right_on="released_at",
    direction="backward",
)

print(safe_join)
```

`direction="backward"` 表示每个价格日期只匹配已经发布的最近事件。

危险写法是：

```python
leaky_join = pd.merge_asof(
    prices,
    events,
    left_on="date",
    right_on="released_at",
    direction="forward",
)

print(leaky_join)
```

`direction="forward"` 会把未来才发布的数据贴到过去日期上。除非你的问题定义就是“找下一次事件”，否则这通常不能作为预测特征。

## bfill 也是一种未来函数

`bfill` 会用后面的值填前面的缺失。

```python
macro = pd.Series(
    [np.nan, 3.1, np.nan, np.nan, 3.3],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
    ]),
    name="macro_value",
)

macro_bfill = macro.bfill()
macro_ffill = macro.ffill()

print(macro_bfill)
print(macro_ffill)
```

`bfill` 会让 `2024-01-02` 提前看到 `2024-01-03` 的数据。预测特征里通常应使用 `ffill`，并且要确认原始发布时间本身没有滞后。

## 两种常见收益对齐约定

回测里最容易混乱的是信号和收益的日期含义。

约定一：收益行表示从上一日到当日的收益。

```python
signal_at_close = (ret.shift(1) > 0).astype(int)
pnl_convention_1 = signal_at_close.shift(1) * ret

print(pnl_convention_1)
```

这里 `signal_at_close.loc[t-1]` 在 `t-1` 收盘后生成，乘以 `ret.loc[t]`，也就是从 `t-1` 到 `t` 的收益。

约定二：标签行表示从当日到下一日的未来收益。

```python
future_ret_1d = close.shift(-1) / close - 1.0
signal_for_next_day = (ret > 0).astype(int)
pnl_convention_2 = signal_for_next_day * future_ret_1d

print(pnl_convention_2)
```

这里 `future_ret_1d.loc[t]` 是标签，不是特征。只要 `signal_for_next_day.loc[t]` 不使用 `t+1` 的信息，这个乘法可以表达“日期 `t` 的信号赚取 `t` 到 `t+1` 的收益”。

两种约定都可以，不能混着用。项目里应把列名写清楚，例如：

- `ret_close_to_close`：行 `t` 表示 `t-1` 到 `t` 的收益。
- `return_fwd_1d`：行 `t` 表示 `t` 到 `t+1` 的收益。
- `signal_at_close`：行 `t` 表示 `t` 收盘后可得到的信号。

## 可以写成代码的检查

一些泄露问题不能靠断言完全发现，但可以用检查降低风险。

```python
feature_cols = ["return_lag_1d", "rolling_mean_3d"]
label_cols = ["return_fwd_1d"]

assert not set(feature_cols) & set(label_cols)
assert all("fwd" not in col for col in feature_cols)
```

检查索引对齐：

```python
features = return_lag_1d
labels = future_ret_1d

assert features.index.equals(labels.index)
assert features.columns.equals(labels.columns)
```

检查训练测试按时间切分：

```python
split_date = pd.Timestamp("2024-01-08")

train_features = features.loc[features.index < split_date]
test_features = features.loc[features.index >= split_date]

assert train_features.index.max() < test_features.index.min()
```

这类检查不能证明完全无泄露，但能防止常见的列混用、标签错位和随机时间切分。

## 常见坑

第一，把 `shift(-1)` 生成的未来收益误放进特征列。

```python
# 标签可以这样写
return_fwd_1d = close.shift(-1) / close - 1.0

# 但 return_fwd_1d 不能进入 feature_cols
```

第二，在预测特征里直接用 `rolling`，忘记它包含当前行。

```python
# 常见安全写法
vol_past_20d = ret.shift(1).rolling(20, min_periods=20).std()
```

第三，长表上忘记按资产分组。

```python
# 不推荐
# df["lag"] = df["return"].shift(1)

# 推荐
# df["lag"] = df.groupby("asset")["return"].shift(1)
```

第四，用全样本均值、标准差、分位数做训练前的标准化。

训练集和测试集应按时间分开，标准化参数只能来自训练期或预测时点之前。

第五，用 `bfill`、`merge_asof(direction="forward")`、`rolling(center=True)` 给历史样本补未来信息。

这些操作本身不总是错，但进入预测特征前必须能解释“这个值在预测时点已经可见”。

## 实战提示

构造每个特征时，都写清楚一句话：

```text
在 date=t 的这一行，这个特征最晚使用到 date=?
```

如果答案晚于预测时点，就是泄露。

列名也要带方向：

- 滞后特征：`lag`、`past`、`hist`。
- 未来标签：`fwd`、`future`、`target`、`label`。
- 信号时点：`signal_at_close`、`signal_next_open`。

不要只看代码有没有 `shift`，要看 `shift` 的方向、收益列的定义、预测时点和交易时点是否一致。

## 小结

防止未来信息泄露的核心不是记住某个固定公式，而是建立时间语义：

- `shift(1)` 常用于滞后特征。
- `shift(-1)` 常用于未来标签。
- `rolling` 默认包含当前行。
- 长表特征要在资产内部 `shift` 和 `rolling`。
- `bfill`、`center=True`、全样本标准化、向前合并事件数据都可能成为未来函数。

只要特征、标签、信号、收益的日期含义清楚，绝大多数泄露都能在写代码时被发现。

## 自检问题

1. 为什么 `shift(-1)` 适合构造标签，但通常不能构造特征？
2. `rolling(20).std()` 和 `shift(1).rolling(20).std()` 在预测语义上有什么区别？
3. 长表数据为什么不能直接对整列 `shift(1)`？
4. `merge_asof(direction="forward")` 在什么情况下会造成未来信息泄露？
5. 如果信号行是日期 `t`，收益行也是日期 `t`，你如何判断是否需要对信号或收益再 `shift`？
