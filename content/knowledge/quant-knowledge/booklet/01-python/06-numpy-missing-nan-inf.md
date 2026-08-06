# NumPy：缺失值、nan 与 inf

## 核心概念

NumPy 里常见的异常数值有两类：

- `np.nan`：Not a Number，通常表示缺失值、无效计算结果或无法定义的数。
- `np.inf` / `-np.inf`：正无穷和负无穷，通常来自除以 0、溢出或人为标记。

它们都是浮点数体系的一部分，因此通常只能自然存在于 float dtype 数组里。

```python
import numpy as np

x = np.array([1.0, np.nan, np.inf, -np.inf])

print(x)        # [  1.  nan  inf -inf]
print(x.dtype)  # float64
```

在量化数据里，`nan` 和 `inf` 很常见：停牌、未上市、缺失行情、复权价格异常、除以 0、收益率计算中的坏数据，都可能产生它们。

## nan 的基本性质

`nan` 有一个非常重要的性质：它不等于任何值，包括它自己。

```python
x = np.nan

print(x == x)  # False
print(x != x)  # True
```

因此不要用 `== np.nan` 判断缺失值：

```python
arr = np.array([1.0, np.nan, 3.0])

print(arr == np.nan)  # [False False False]
```

正确做法是用 `np.isnan`：

```python
print(np.isnan(arr))  # [False  True False]
```

## inf 的基本性质

`inf` 表示无穷大，可以参与比较：

```python
x = np.array([1.0, np.inf, -np.inf])

print(x > 0)       # [ True  True False]
print(np.isinf(x)) # [False  True  True]
```

但 `inf` 参与算术运算时可能继续产生 `inf` 或 `nan`：

```python
print(np.inf + 1)       # inf
print(np.inf * 2)       # inf
print(np.inf - np.inf)  # nan
```

`inf - inf` 无法定义，因此结果是 `nan`。

## 检测异常值

常用检测函数：

- `np.isnan(x)`：是否为 `nan`。
- `np.isinf(x)`：是否为正负无穷。
- `np.isfinite(x)`：是否为有限数，也就是既不是 `nan`，也不是正负无穷。

```python
x = np.array([1.0, np.nan, np.inf, -np.inf, 5.0])

print(np.isnan(x))    # [False  True False False False]
print(np.isinf(x))    # [False False  True  True False]
print(np.isfinite(x)) # [ True False False False  True]
```

在清洗数值数据时，`np.isfinite` 往往是最实用的第一道检查。

```python
valid = np.isfinite(x)

print(x[valid])  # [1. 5.]
```

## nan 会传播

普通算术运算遇到 `nan`，结果通常也会变成 `nan`。

```python
x = np.array([1.0, np.nan, 3.0])

print(x + 1.0)  # [ 2. nan  4.]
print(x * 2.0)  # [ 2. nan  6.]
print(x.mean()) # nan
```

如果你希望聚合时忽略 `nan`，需要使用 `nan` 版本函数：

```python
print(np.nanmean(x))  # 2.0
print(np.nansum(x))   # 4.0
```

注意：忽略 `nan` 不代表数据问题消失。你仍然需要知道缺失值为什么出现，以及忽略它是否符合业务含义。

## 除以 0 与 inf

除以 0 经常产生 `inf` 或 `nan`：

```python
num = np.array([1.0, 0.0, -1.0])
den = np.array([0.0, 0.0, 0.0])

out = num / den

print(out)  # [ inf  nan -inf]
```

这段代码通常会触发运行时警告：

```text
RuntimeWarning: divide by zero encountered in divide
RuntimeWarning: invalid value encountered in divide
```

警告不是异常，程序会继续执行，但结果里已经出现了 `inf` 和 `nan`。研究代码里不能忽略这类警告。

## 用 where 安全除法

对于可能除以 0 的计算，可以显式指定合法位置。

```python
num = np.array([1.0, 0.0, -1.0])
den = np.array([0.0, 2.0, 0.5])

out = np.full_like(num, np.nan)
valid = den != 0
out[valid] = num[valid] / den[valid]

print(out)  # [nan  0. -2.]
```

这种写法比先算出 `inf` 再替换更清楚，因为它直接表达了“分母为 0 时结果无效”。

也可以用 `np.divide` 的 `where` 和 `out` 参数：

```python
out = np.full_like(num, np.nan)
np.divide(num, den, out=out, where=den != 0)

print(out)  # [nan  0. -2.]
```

## 替换异常值

可以用 `np.nan_to_num` 把异常值替换成指定数值。

```python
x = np.array([1.0, np.nan, np.inf, -np.inf])

clean = np.nan_to_num(x, nan=0.0, posinf=999.0, neginf=-999.0)

print(clean)  # [   1.    0.  999. -999.]
```

但替换要谨慎。把缺失值全部替换成 0 可能引入错误含义。比如某只股票停牌，并不等于它的因子值是 0，也不等于它的收益率是 0。

更稳妥的做法通常是：

1. 先检测异常值比例。
2. 明确异常值来源。
3. 根据业务含义选择剔除、填充、截断或保留缺失。

## 实战例子：价格转收益率时处理坏数据

收益率计算中，如果前一期价格为 0 或缺失，结果应该标记为无效。

```python
prices = np.array([100.0, 102.0, 0.0, 105.0, np.nan])

prev = prices[:-1]
curr = prices[1:]

returns = np.full(prev.shape, np.nan)
valid = np.isfinite(prev) & np.isfinite(curr) & (prev != 0)
returns[valid] = curr[valid] / prev[valid] - 1.0

print(returns)
```

输出：

```text
[0.02 -1.    nan  nan]
```

解释：

- `102 / 100 - 1 = 0.02`。
- `0 / 102 - 1 = -1`，价格跌到 0 在真实行情中通常也应进一步排查。
- `105 / 0 - 1` 分母为 0，因此记为 `nan`。
- `nan` 参与计算，结果也记为 `nan`。

## 实战例子：因子矩阵清洗

假设 `factor.shape == (T, N)`，行是日期，列是股票。你希望把所有非有限值标记为缺失，然后做横截面均值。

```python
factor = np.array([
    [1.2, np.nan, 2.0, np.inf],
    [0.7, 1.1, -np.inf, 1.5],
    [2.2, 2.0, 1.8, 2.1],
])

factor_clean = factor.copy()
factor_clean[~np.isfinite(factor_clean)] = np.nan

daily_mean = np.nanmean(factor_clean, axis=1)

print(factor_clean)
print(daily_mean)  # [1.6 1.1 2.025]
```

这里的处理含义是：`inf`、`-inf` 和已有 `nan` 都被当作缺失值，在横截面均值里忽略。

## 统计缺失比例

数据清洗不能只做替换，还要报告异常值比例。

```python
x = np.array([1.0, np.nan, 2.0, np.inf, 3.0])

missing_or_bad = ~np.isfinite(x)
bad_ratio = missing_or_bad.mean()

print(bad_ratio)  # 0.4
```

二维因子矩阵中，可以按日期统计坏值比例：

```python
bad_by_day = (~np.isfinite(factor)).mean(axis=1)

print(bad_by_day)  # [0.5  0.25 0.  ]
```

这类指标很适合放进数据质量检查。如果某天坏值比例突然升高，往往说明数据源、复权、合并或对齐出了问题。

## 控制浮点警告

有时你明确知道某段计算可能产生警告，并且已经准备好处理结果，可以用 `np.errstate` 限定警告范围。

```python
num = np.array([1.0, 0.0, -1.0])
den = np.array([0.0, 0.0, 0.0])

with np.errstate(divide="ignore", invalid="ignore"):
    out = num / den

print(out)  # [ inf  nan -inf]
```

不要在全局关闭警告。局部使用 `np.errstate` 更安全，因为它能把“我知道这里可能出问题，并且会处理”的意图写清楚。

## 常见坑

### 1. 用 `== np.nan` 判断缺失值

```python
x = np.array([1.0, np.nan, 3.0])

print(x == np.nan)  # [False False False]
```

应使用：

```python
print(np.isnan(x))  # [False  True False]
```

### 2. 把缺失值直接填 0

```python
factor = np.array([1.2, np.nan, 0.8])
filled = np.nan_to_num(factor, nan=0.0)

print(filled)  # [1.2 0.  0.8]
```

这可能把“未知”变成“真实的 0”。在因子研究中，0 往往有明确含义，比如因子位于中性水平。缺失值是否能填 0，必须由业务语义决定。

### 3. 忽略 inf

很多人只检查 `np.isnan`，但忘记检查 `inf`：

```python
x = np.array([1.0, np.inf, 3.0])

print(np.isnan(x).any())     # False
print(np.isfinite(x).all())  # False
```

清洗数值矩阵时，通常应该先用 `np.isfinite`。

### 4. 空切片的 nan 聚合

```python
x = np.array([np.nan, np.nan])

print(np.nanmean(x))  # nan
```

这会触发 `RuntimeWarning: Mean of empty slice`。如果某个横截面全是缺失值，`nanmean` 也无法产生有效统计量。

## 实战提示

处理异常数值时，建议使用固定流程：

1. 用 `np.isfinite` 检测非有限值。
2. 统计异常值比例，而不是直接覆盖。
3. 根据业务含义决定填充、剔除、截断或保留为 `nan`。
4. 聚合时明确使用普通函数还是 `nan` 版本函数。
5. 对除法、标准化、收益率计算这类高风险操作加断言或数据质量检查。

一个常用检查函数可以写成：

```python
def finite_ratio(x):
    x = np.asarray(x, dtype=float)
    return np.isfinite(x).mean()

print(finite_ratio([1.0, np.nan, np.inf, 2.0]))  # 0.5
```

## 自检问题

1. 为什么不能用 `x == np.nan` 判断缺失值？
2. `np.isnan`、`np.isinf`、`np.isfinite` 分别检查什么？
3. 除以 0 时可能产生哪些结果？
4. 为什么把所有缺失值填成 0 可能有风险？
5. 在因子矩阵中按日期统计异常值比例，可以怎么写？

