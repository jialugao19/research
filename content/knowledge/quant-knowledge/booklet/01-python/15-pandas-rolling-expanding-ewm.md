# 15. pandas：rolling / expanding / ewm

## 核心概念

pandas 里常见的时间窗口计算有三类：

- `rolling`：固定长度滚动窗口，例如最近 20 天均值。
- `expanding`：从起点开始不断扩大的累计窗口。
- `ewm`：指数加权窗口，越近的数据权重越大。

这些工具常用于构造时间序列特征，例如动量、波动率、均线、累计收益和指数加权波动率。

最重要的实践原则是：如果特征要用于预测下一期，通常需要先 `shift`，确保特征只使用预测时点之前已经知道的数据。

## rolling：固定窗口

```python
import pandas as pd

s = pd.Series(
    [1.0, 2.0, 3.0, 4.0, 5.0],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
    ]),
    name="return",
)

rolling_mean = s.rolling(window=3).mean()

print(rolling_mean)
```

`window=3` 表示每个位置用最近 3 个观测值计算均值。默认 `min_periods` 等于窗口长度，因此前两个位置结果是缺失值。

如果希望窗口不足时也计算，可以设置 `min_periods`：

```python
rolling_mean_min1 = s.rolling(window=3, min_periods=1).mean()

print(rolling_mean_min1)
```

`min_periods=1` 表示只要窗口里至少有 1 个非缺失值就计算。

## rolling 的窗口是否包含当前值

默认情况下，`rolling` 包含当前行。

```python
s = pd.Series([1.0, 2.0, 3.0, 4.0])

print(s.rolling(3).mean())
```

第 3 个结果是 `(1 + 2 + 3) / 3 = 2`，包含当前值 `3`。

如果你要构造“截至昨天”的特征，应先 `shift(1)`：

```python
feature = s.shift(1).rolling(3).mean()

print(feature)
```

这样第 4 个位置使用的是前 3 个历史值 `1, 2, 3`，不包含当前值 `4`。

## 实战例子：过去 3 日动量

假设有日收盘价：

```python
close = pd.Series(
    [100.0, 102.0, 101.0, 105.0, 110.0],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
    ]),
    name="close",
)

returns = close.pct_change(fill_method=None)
momentum_3d = close / close.shift(3) - 1.0

print(returns)
print(momentum_3d)
```

`momentum_3d` 表示当前价格相对 3 个交易日前价格的涨跌幅。如果用它预测下一天收益，在日期 `t` 收盘后生成并用于预测 `t+1`，这个特征是合理的；如果你在日期 `t` 开盘前使用它，就要确认 `t` 的收盘价当时是否已经可见。

## 实战例子：过去 3 日波动率

如果要用过去收益率估计波动率，并预测下一期，推荐先 `shift`：

```python
returns = close.pct_change(fill_method=None)

vol_3d = returns.shift(1).rolling(window=3).std()

print(vol_3d)
```

这里 `returns.shift(1)` 表示在日期 `t` 的特征只使用到 `t-1` 的收益率。否则，`returns.rolling(3).std()` 会包含日期 `t` 的收益率，而这个收益率通常要等当天收盘后才知道。

## 时间窗口 rolling

如果 index 是 `DatetimeIndex`，rolling 可以使用时间长度作为窗口。

```python
intraday = pd.Series(
    [1.0, 2.0, 3.0, 4.0],
    index=pd.to_datetime([
        "2024-01-02 09:30",
        "2024-01-02 09:31",
        "2024-01-02 09:33",
        "2024-01-02 09:36",
    ]),
)

rolling_3min = intraday.rolling("3min").sum()

print(rolling_3min)
```

`rolling("3min")` 表示使用最近 3 分钟内的观测。时间窗口和固定行数窗口不同：如果数据不均匀，窗口内行数会变化。

## expanding：累计窗口

`expanding` 从开头开始，窗口不断变大。

```python
s = pd.Series([1.0, 2.0, 3.0, 4.0])

print(s.expanding().mean())
print(s.expanding().sum())
```

输出分别是累计均值和累计和。

如果要避免当前值进入特征，也可以先 `shift`：

```python
history_mean = s.shift(1).expanding(min_periods=1).mean()

print(history_mean)
```

这表示每个位置使用此前所有历史值的均值。

## 实战例子：累计最大回撤雏形

累计最高点可以用 `expanding().max()`：

```python
equity = pd.Series([1.00, 1.05, 1.03, 1.10, 1.04])

running_peak = equity.expanding().max()
drawdown = equity / running_peak - 1.0

print(running_peak)
print(drawdown)
```

这只是最大回撤计算的基础组件。完整 drawdown 会在风险指标章节继续展开。

## ewm：指数加权窗口

`ewm` 会给近期数据更高权重，常用于平滑和指数加权波动率。

```python
s = pd.Series([1.0, 2.0, 3.0, 4.0])

ewm_mean = s.ewm(span=3, adjust=False).mean()

print(ewm_mean)
```

`span` 越小，越强调近期数据。`adjust=False` 常用于递推形式，直觉上更像：

```text
new_value = alpha * current + (1 - alpha) * old_value
```

其中 `alpha = 2 / (span + 1)`。

## 实战例子：指数加权波动率

收益率的指数加权波动率可以写成：

```python
returns = pd.Series([0.01, -0.02, 0.03, 0.00, -0.01])

ewm_vol = returns.shift(1).ewm(span=3, adjust=False).std()

print(ewm_vol)
```

同样，先 `shift(1)` 是为了让日期 `t` 的波动率特征只依赖 `t` 之前的收益率。

## DataFrame rolling

DataFrame 上也可以做 rolling。

```python
returns = pd.DataFrame(
    {
        "AAA": [0.01, -0.02, 0.03, 0.00, 0.02],
        "BBB": [-0.01, 0.01, 0.00, 0.02, -0.02],
    },
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
    ]),
)

rolling_vol = returns.shift(1).rolling(3).std()

print(rolling_vol)
```

这里每一列独立做滚动标准差。列是资产，index 是日期。

## 长表中按资产 rolling

长表数据需要先按资产分组，再做 rolling。

```python
long = pd.DataFrame({
    "date": pd.to_datetime([
        "2024-01-02", "2024-01-03", "2024-01-04",
        "2024-01-02", "2024-01-03", "2024-01-04",
    ]),
    "asset": ["AAA", "AAA", "AAA", "BBB", "BBB", "BBB"],
    "return": [0.01, -0.02, 0.03, -0.01, 0.01, 0.00],
})

long = long.sort_values(["asset", "date"])
long["roll_mean_2"] = (
    long.groupby("asset")["return"]
    .transform(lambda x: x.shift(1).rolling(2).mean())
)

print(long)
```

这里每只资产独立计算过去 2 期均值。`shift(1)` 在每只资产内部发生，不会把 AAA 的值泄露到 BBB。

## min_periods 的业务含义

`min_periods` 控制窗口里至少有多少有效观测才输出结果。

```python
s = pd.Series([1.0, 2.0, 3.0])

print(s.rolling(3).mean())
print(s.rolling(3, min_periods=1).mean())
```

`min_periods=1` 能让早期样本产生值，但这些值基于更少历史数据，统计稳定性较弱。研究代码里应明确早期样本是保留、删除，还是单独标记。

## center 参数

`rolling(..., center=True)` 会把窗口结果放在窗口中心。

```python
s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])

print(s.rolling(3, center=True).mean())
```

这在平滑画图时可能有用，但预测和回测里通常危险，因为中心窗口会使用未来值。构造特征时一般不要使用 `center=True`。

## 常见坑

### 1. rolling 默认包含当前值

```python
feature = returns.rolling(20).std()
```

如果这个特征在当天收盘前使用，就可能包含当天尚不可知的收益率。预测下一期时更常见的写法是：

```python
feature = returns.shift(1).rolling(20).std()
```

### 2. 在全表 rolling，忘记按资产分组

长表里如果直接：

```python
# 不推荐
# long["roll"] = long["return"].shift(1).rolling(2).mean()
```

窗口会跨资产滚动，导致不同资产之间互相污染。应先 `groupby("asset")`。

### 3. center=True 泄露未来

中心窗口会使用当前点前后的数据。它适合某些离线平滑分析，不适合可交易特征。

### 4. min_periods 太小导致早期样本不稳定

`min_periods=1` 会让窗口不足时也输出统计量。早期值可用，但统计含义和完整窗口不同。

### 5. 不规则时间序列误用固定行数窗口

`rolling(5)` 是最近 5 条记录，不一定是最近 5 分钟或 5 天。如果数据时间间隔不均匀，应考虑时间窗口，例如 `rolling("5min")`。

## 实战提示

构造滚动特征时，建议固定写出时间可见性：

```python
# 用于预测 t 的收益，只使用 t 之前的数据
feature = returns.shift(1).rolling(window=20, min_periods=20).std()
```

长表中按资产构造：

```python
long = long.sort_values(["asset", "date"])
long["vol_20"] = (
    long.groupby("asset")["return"]
    .transform(lambda x: x.shift(1).rolling(20, min_periods=20).std())
)
```

每次写 rolling 特征，都问：

1. 窗口是否包含当前值？
2. 是否需要 `shift(1)`？
3. 窗口是在每个资产内部计算，还是跨资产计算了？
4. `min_periods` 是否符合样本要求？
5. 时间间隔不规则时，应该用行数窗口还是时间窗口？

## 自检问题

1. `rolling`、`expanding`、`ewm` 分别适合什么窗口逻辑？
2. 为什么预测特征里经常要写 `shift(1).rolling(...)`？
3. 长表中按股票计算滚动均值时，为什么要先 `groupby("asset")`？
4. `min_periods` 会影响什么？
5. 为什么 `center=True` 通常不适合回测特征？

