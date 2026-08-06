# 17. pandas：向量化、apply 与性能

## 核心概念

pandas 代码性能通常取决于你是否让计算留在向量化路径上。

优先级大致是：

1. 直接列运算、布尔表达式、内置方法。
2. `groupby`、`rolling`、`str`、`dt` 等 pandas 专门接口。
3. `map` 或 `replace` 做简单映射。
4. `apply` 处理确实难以向量化的逻辑。
5. 行级 `apply(axis=1)` 和逐行循环通常最慢，应谨慎使用。

核心原则：先写清楚正确的版本，再优化热点；但不要把简单列计算写成行级 `apply`。

## 准备数据

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "asset": ["AAA", "BBB", "CCC", "DDD"],
    "close": [100.0, 49.5, 20.0, 80.0],
    "volume": [1200, 800, 3000, 500],
    "return": [0.01, -0.02, 0.03, -0.01],
    "industry": ["tech", "finance", "tech", "energy"],
})

print(df)
```

下面的例子都基于这个表。

## 向量化列运算

计算成交额：

```python
df["amount"] = df["close"] * df["volume"]

print(df[["asset", "amount"]])
```

这是向量化写法。pandas 会对整列做计算。

不推荐为了这种简单逻辑写行级 `apply`：

```python
# 不推荐
df["amount_slow"] = df.apply(lambda row: row["close"] * row["volume"], axis=1)
```

两者结果相同，但后者每行构造一个 Series，再调用 Python 函数，通常慢很多。

## 条件逻辑：np.where 和布尔赋值

构造收益方向标签：

```python
df["direction"] = np.where(df["return"] > 0, "up", "down_or_flat")

print(df[["asset", "return", "direction"]])
```

多条件可以用 `np.select`：

```python
conditions = [
    df["return"] > 0.02,
    df["return"] < -0.01,
]
choices = ["strong_up", "down"]

df["return_bucket"] = np.select(conditions, choices, default="normal")

print(df[["asset", "return", "return_bucket"]])
```

如果只是给满足条件的行赋值，也可以用 `.loc`：

```python
df["liquid"] = False
df.loc[df["volume"] >= 1000, "liquid"] = True

print(df[["asset", "volume", "liquid"]])
```

## map：简单字典映射

行业映射成大类或编号时，用 `map` 很清楚。

```python
industry_code = {
    "tech": 1,
    "finance": 2,
    "energy": 3,
}

df["industry_code"] = df["industry"].map(industry_code)

print(df[["industry", "industry_code"]])
```

如果有未映射值，会得到缺失值。可以主动检查：

```python
assert df["industry_code"].notna().all()
```

`map` 适合一列到一列的简单映射。多列复杂逻辑不一定适合硬塞进 `map`。

## replace：值替换

如果只是替换取值，`replace` 更直接。

```python
df["industry_name"] = df["industry"].replace({
    "tech": "Technology",
    "finance": "Financials",
    "energy": "Energy",
})

print(df[["industry", "industry_name"]])
```

`map` 更像“映射到新值”，`replace` 更像“把已有值中的某些替换掉”。两者都比手写行循环更适合简单映射。

## str 和 dt 访问器

字符串和日期也有向量化接口。

```python
symbols = pd.Series(["aaa US", "bbb US", "ccc CN"])

upper = symbols.str.upper()
country = symbols.str[-2:]

print(upper)
print(country)
```

日期列：

```python
dates = pd.Series(pd.to_datetime(["2024-01-02", "2024-02-05", "2024-02-06"]))

month = dates.dt.month
weekday = dates.dt.dayofweek

print(month)
print(weekday)
```

不要用 `apply(lambda x: x.month)` 处理日期列，优先使用 `.dt`。

## apply：适合什么场景

`apply` 适合那些难以用内置向量化表达的逻辑。

例如，基于多个字段构造一个解释性字符串：

```python
def describe_row(row):
    sign = "positive" if row["return"] > 0 else "non_positive"
    return f'{row["asset"]}:{sign}:{row["industry"]}'

df["description"] = df.apply(describe_row, axis=1)

print(df[["asset", "description"]])
```

这类逻辑本身偏文本处理或报告生成，性能通常不是主要瓶颈。对于大规模数值计算，不应优先考虑行级 `apply`。

## apply(axis=1) 的替代写法

行级 `apply` 经常可以改写成向量化表达。

```python
# 可以运行，但不推荐
df["signal_apply"] = df.apply(
    lambda row: 1 if (row["return"] > 0 and row["volume"] >= 1000) else 0,
    axis=1,
)
```

向量化写法：

```python
df["signal_vec"] = ((df["return"] > 0) & (df["volume"] >= 1000)).astype(int)

print(df[["asset", "signal_apply", "signal_vec"]])
```

结果相同，但向量化写法更短、更快，也更容易检查条件。

## apply 在列方向上的使用

`DataFrame.apply` 默认按列应用函数。

```python
numeric = df[["close", "volume", "return"]]

summary = numeric.apply(["mean", "std"])

print(summary)
```

不过，对常见统计量，直接用内置方法更清楚：

```python
print(numeric.mean())
print(numeric.std())
```

`apply` 不是不能用，而是不要用它替代已有的清晰接口。

## eval 和 query

`eval` 和 `query` 可以让表达式更简洁，在大表上有时也能减少临时对象。

```python
df["amount_eval"] = df.eval("close * volume")

liquid_positive = df.query("volume >= 1000 and `return` > 0")

print(df[["asset", "amount", "amount_eval"]])
print(liquid_positive[["asset", "return", "volume"]])
```

`query` 适合简单筛选表达式。复杂逻辑、外部变量很多或需要调试时，普通布尔表达式更直观。

## 简单计时

可以用 `time.perf_counter()` 做粗略计时。

```python
import time

n = 100_000
big = pd.DataFrame({
    "close": np.linspace(10.0, 100.0, n),
    "volume": np.arange(n),
})

start = time.perf_counter()
amount_vec = big["close"] * big["volume"]
vec_seconds = time.perf_counter() - start

start = time.perf_counter()
amount_apply = big.apply(lambda row: row["close"] * row["volume"], axis=1)
apply_seconds = time.perf_counter() - start

print(np.allclose(amount_vec, amount_apply))  # True
print(apply_seconds > vec_seconds)            # 通常是 True
```

一次计时不是严格 benchmark，但能帮助你识别数量级差异。真实优化时，应在真实数据规模和真实运行环境中测量。

## 实战例子：因子 winsorize

对因子值做截尾，优先使用向量化方法。

```python
factor = pd.Series([0.2, 10.0, -8.0, 0.5, 1.1], name="factor")

clipped = factor.clip(lower=-3.0, upper=3.0)

print(clipped)
```

不要写成：

```python
# 不推荐
clipped_apply = factor.apply(lambda x: min(max(x, -3.0), 3.0))
```

`clip` 是专门为这个场景设计的接口。

## 实战例子：按日期做向量化横截面处理

长表中，很多横截面处理可以用 `groupby.transform`，不需要 `apply`。

```python
panel = pd.DataFrame({
    "date": pd.to_datetime([
        "2024-01-02", "2024-01-02", "2024-01-02",
        "2024-01-03", "2024-01-03", "2024-01-03",
    ]),
    "asset": ["AAA", "BBB", "CCC", "AAA", "BBB", "CCC"],
    "factor": [1.2, 0.5, 1.8, 1.0, 0.7, 1.5],
})

mean = panel.groupby("date")["factor"].transform("mean")
std = panel.groupby("date")["factor"].transform("std")

panel["factor_z"] = (panel["factor"] - mean) / std

print(panel)
```

这是典型的向量化 pandas 写法：分组统计用 `transform`，逐行计算用列表达式。

## 常见坑

### 1. 一上来就 apply(axis=1)

行级 `apply` 很直观，但通常慢。先问自己：能不能用列运算、`np.where`、`np.select`、`map`、`groupby.transform` 或内置方法？

### 2. apply 隐藏类型问题

`apply` 调用 Python 函数，返回值类型可能不稳定，最后得到 `object` dtype，影响性能和后续计算。

```python
mixed = pd.Series([1, 2, 3]).apply(lambda x: x if x > 1 else "small")

print(mixed.dtype)  # object
```

数值列应尽量保持数值 dtype。

### 3. 向量化表达式过长

一行塞太多逻辑会难以检查：

```python
# 难读
signal = (((df["return"] > 0) & (df["volume"] >= 1000)) | (df["industry"] == "tech")).astype(int)
```

可以拆开：

```python
positive_liquid = (df["return"] > 0) & (df["volume"] >= 1000)
is_tech = df["industry"] == "tech"
signal = (positive_liquid | is_tech).astype(int)
```

### 4. eval/query 不适合所有情况

`eval` 和 `query` 对简单表达式很好，但复杂表达式、字符串处理、调试断点、外部变量多时，普通 pandas 代码更可靠。

### 5. 忽略真正瓶颈

性能问题不一定来自 pandas 表达式。I/O、merge 粒度错误、重复计算、数据过宽、内存压力，都可能是更大的瓶颈。先测量，再优化。

## 实战提示

写 pandas 特征工程时，可以按这个顺序尝试：

1. 能用内置列运算就用列运算。
2. 条件分支用 `np.where`、`np.select` 或 `.loc`。
3. 简单映射用 `map` 或 `replace`。
4. 字符串和日期用 `.str`、`.dt`。
5. 分组结果写回原表用 `groupby.transform`。
6. 只有确实难以表达时才使用 `apply`。

验证优化没有改变结果：

```python
assert (df["signal_apply"] == df["signal_vec"]).all()
```

优化前后都要保留小样本测试，尤其是缺失值、边界值和异常类型。

## 自检问题

1. 为什么行级 `apply(axis=1)` 通常比列运算慢？
2. `map` 和 `replace` 分别适合什么场景？
3. 日期列为什么优先使用 `.dt` 而不是 `apply(lambda x: ...)`？
4. `groupby.transform` 在横截面标准化中解决了什么问题？
5. 为什么性能优化前要先确认真正瓶颈？
