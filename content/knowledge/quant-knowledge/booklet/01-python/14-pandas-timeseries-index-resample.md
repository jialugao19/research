# 14. pandas：时间序列索引与重采样

## 核心概念

pandas 处理时间序列时，最常用的是 `DatetimeIndex`。它让 pandas 理解“这一行发生在什么时间”，从而支持时间切片、频率转换、重采样和按时间窗口聚合。

常见操作包括：

- `pd.to_datetime`：把字符串转换成时间戳。
- `set_index("date")`：把日期列设为 index。
- `sort_index()`：按时间排序。
- `asfreq()`：按新频率重新对齐，不做聚合。
- `resample()`：按新频率分组并聚合。

```python
import pandas as pd

prices = pd.Series(
    [100.0, 102.0, 101.0],
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
    name="close",
)

print(prices.index)
print(prices.loc["2024-01-03"])
```

## 创建 DatetimeIndex

如果原始数据里日期是普通列，先转换再设为 index。

```python
df = pd.DataFrame({
    "date": ["2024-01-02", "2024-01-03", "2024-01-04"],
    "close": [100.0, 102.0, 101.0],
    "volume": [1000, 1200, 900],
})

df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

print(df.index)
print(df)
```

时间序列数据通常还要按时间排序：

```python
df = df.sort_index()
```

很多时间序列操作默认假设 index 有清晰的时间顺序。乱序数据虽然不一定报错，但结果经常不符合预期。

## 时间切片

有 `DatetimeIndex` 后，可以用字符串做时间切片。

```python
prices = pd.Series(
    [100.0, 102.0, 101.0, 105.0, 107.0],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-02-01",
        "2024-02-02",
    ]),
    name="close",
)

print(prices.loc["2024-01"])
print(prices.loc["2024-01-03":"2024-02-01"])
```

`prices.loc["2024-01"]` 会取 2024 年 1 月的数据。区间切片两端通常都包含。

时间切片前，最好确认 index 已排序：

```python
assert prices.index.is_monotonic_increasing
```

## date_range：生成时间索引

`pd.date_range` 可以生成规则时间索引。

```python
daily = pd.date_range("2024-01-02", periods=5, freq="D")
business = pd.date_range("2024-01-02", periods=5, freq="B")

print(daily)
print(business)
```

常见频率：

- `"D"`：自然日。
- `"B"`：工作日。
- `"W-FRI"`：以周五为周期结束点的周频。
- `"ME"`：月末。
- `"h"`：小时。
- `"min"`：分钟。

注意：`"B"` 只表示普通工作日，不等于真实交易日历。真实市场有节假日、临时休市、半日交易等特殊情况，严格回测应使用交易所日历或数据源提供的交易日历。

## asfreq：重新对齐频率

`asfreq` 会把时间序列对齐到新频率，但不做聚合。

```python
prices = pd.Series(
    [100.0, 102.0, 101.0],
    index=pd.to_datetime(["2024-01-02", "2024-01-04", "2024-01-05"]),
    name="close",
)

daily = prices.asfreq("D")

print(daily)
```

输出中 2024-01-03 会出现缺失值，因为原始数据没有这一天。

可以配合前向填充：

```python
daily_ffill = prices.asfreq("D").ffill()

print(daily_ffill)
```

这表示把缺失日期的价格填成上一个已知价格。是否合理取决于业务语义。价格序列可以讨论前向填充，成交量、收益率和因子值通常不能无脑这样填。

## resample：按时间频率聚合

`resample` 会按时间频率把数据分组，然后聚合。

```python
prices = pd.Series(
    [100.0, 102.0, 101.0, 105.0, 107.0],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
    ]),
    name="close",
)

weekly_close = prices.resample("W-FRI").last()

print(weekly_close)
```

`"W-FRI"` 表示每周五作为周频标签。`last()` 表示取每个周期内最后一个观测值。

如果你从日频价格算周收益，常见做法是先得到周收盘价，再算收益：

```python
weekly_return = weekly_close.pct_change(fill_method=None)

print(weekly_return)
```

不要直接把日收益简单相加当作精确周收益。简单收益需要复利合成，或者直接用价格计算。

## 多列 OHLCV 重采样

分钟数据重采样到日频时，OHLCV 常用不同聚合方式：

```python
bars = pd.DataFrame(
    {
        "price": [100.0, 101.0, 99.0, 102.0],
        "volume": [10, 20, 15, 30],
    },
    index=pd.to_datetime([
        "2024-01-02 09:30",
        "2024-01-02 09:31",
        "2024-01-02 09:32",
        "2024-01-02 09:33",
    ]),
)

daily_bar = bars.resample("D").agg(
    open=("price", "first"),
    high=("price", "max"),
    low=("price", "min"),
    close=("price", "last"),
    volume=("volume", "sum"),
)

print(daily_bar)
```

这个例子中：

- `open`：当天第一笔价格。
- `high`：当天最高价。
- `low`：当天最低价。
- `close`：当天最后一笔价格。
- `volume`：当天成交量求和。

不同字段应该用不同聚合方式。价格不能用 `sum`，成交量通常不能用 `last`。

## 分组后重采样：每只资产分别处理

长表里通常有多只资产。可以先按资产分组，再按时间重采样。

```python
long = pd.DataFrame({
    "date": pd.to_datetime([
        "2024-01-02", "2024-01-03", "2024-01-05",
        "2024-01-02", "2024-01-04", "2024-01-05",
    ]),
    "asset": ["AAA", "AAA", "AAA", "BBB", "BBB", "BBB"],
    "close": [100.0, 102.0, 105.0, 50.0, 51.0, 52.0],
})

weekly = (
    long
    .set_index("date")
    .groupby("asset")["close"]
    .resample("W-FRI")
    .last()
)

print(weekly)
```

结果是带 `asset` 和 `date` 的多层索引。这个模式适合长表数据，但要注意排序和后续 index 处理。

如果想得到普通表：

```python
weekly_table = weekly.rename("weekly_close").reset_index()

print(weekly_table)
```

## label 和 closed

重采样时，`label` 决定聚合后时间标签放在区间左端还是右端，`closed` 决定区间哪一端闭合。

```python
s = pd.Series(
    [1, 2, 3, 4],
    index=pd.to_datetime([
        "2024-01-01",
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
    ]),
)

right_labeled = s.resample("2D", label="right", closed="right").sum()
left_labeled = s.resample("2D", label="left", closed="left").sum()

print(right_labeled)
print(left_labeled)
```

在回测中，时间标签非常重要。如果你把一个区间的聚合结果标在区间开始处，可能让后续代码误以为这个结果在期初就已知。

## timezone：时区要一致

不同数据源可能使用不同时间区。

```python
times = pd.to_datetime(["2024-01-02 09:30", "2024-01-02 09:31"])
local = times.tz_localize("America/New_York")
utc = local.tz_convert("UTC")

print(local)
print(utc)
```

合并不同市场、不同数据源或 tick 数据时，必须明确时区。不要把无时区时间戳和有时区时间戳混在一起后直接合并。

## 实战例子：日频价格到周频收益

```python
daily_close = pd.Series(
    [100.0, 102.0, 101.0, 105.0, 110.0, 108.0],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
        "2024-01-09",
    ]),
    name="close",
)

weekly_close = daily_close.resample("W-FRI").last()
weekly_return = weekly_close.pct_change(fill_method=None)

print(weekly_close)
print(weekly_return)
```

第一周标签是周五，取 2024-01-05 的收盘价。第二周还没到周五，但 `resample("W-FRI").last()` 会把当前已有的 2024-01-09 作为该周截至目前的最后观测。如果你在真实周五之前运行这段代码，要避免使用未完成周期的结果。

## 常见坑

### 1. index 不是 DatetimeIndex

```python
df = pd.DataFrame({"date": ["2024-01-02"], "close": [100.0]})

# df.resample("D").last()
```

`resample` 需要 DatetimeIndex、TimedeltaIndex 或 PeriodIndex。通常应先：

```python
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date").sort_index()
```

### 2. 时间没排序

乱序时间序列可能让切片、前向填充和人工检查都变得混乱。读入数据后应检查：

```python
assert df.index.is_monotonic_increasing
```

### 3. 把自然日当交易日

`asfreq("D")` 会生成自然日，包括周末。`asfreq("B")` 是普通工作日，也不等于真实交易日。严格回测应使用真实交易日历。

### 4. 对所有列使用同一个聚合函数

```python
# 不推荐
# bars.resample("D").last()
```

这会让成交量也取最后一笔，而不是求和。OHLCV 应为不同列指定不同聚合方式。

### 5. 使用未完成周期

周频或月频重采样时，当前周期可能还没结束。如果你在周三使用本周 `W-FRI` 的聚合结果，就可能引入未来窗口定义上的混乱。回测中通常要只使用已经完成的周期。

## 实战提示

时间序列处理前，先做固定检查：

```python
df = df.sort_index()

assert isinstance(df.index, pd.DatetimeIndex)
assert df.index.is_monotonic_increasing
```

重采样时写清楚每列的聚合含义：

```python
daily_bar = bars.resample("D").agg(
    open=("price", "first"),
    high=("price", "max"),
    low=("price", "min"),
    close=("price", "last"),
    volume=("volume", "sum"),
)
```

如果结果要用于预测或回测，额外检查：

1. 重采样标签是在周期开始还是结束？
2. 当前周期是否已经完整？
3. 填充是否用了未来数据？
4. 使用的是自然日、工作日，还是真实交易日？

## 自检问题

1. `asfreq` 和 `resample` 的区别是什么？
2. 为什么时间序列数据通常要先 `sort_index()`？
3. 日频价格重采样到周频收益时，为什么通常先取周收盘价再算收益？
4. OHLCV 重采样时，为什么不能对所有列都用同一个聚合函数？
5. 为什么使用未完成周/月的重采样结果可能有风险？

