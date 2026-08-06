# Python 理解项：vectorization 向量化的含义、收益与边界

## 核心概念

向量化不是“没有循环”。向量化的真正含义是：

```text
把 Python 层逐元素循环，交给底层数组库、矢量化内核或批量接口执行。
```

典型例子：

```python
out = x * x + 1.0
```

这行代码看不到 `for`，但底层仍然在遍历数组。区别是遍历发生在 NumPy 的 C 层或底层数值库中，而不是 Python 解释器中。

向量化的收益通常来自：

- 减少 Python 函数调用和循环解释开销。
- 使用连续、同类型的数组内存。
- 调用 C / Fortran / BLAS 等底层优化实现。
- 用批量表达式让代码更短、更接近数学公式。

但向量化也有边界：

- 可能创建很大的临时数组。
- 对复杂状态逻辑不一定自然。
- 对 `object` dtype、字符串或 Python 对象不一定快。
- 硬写成向量化可能降低可读性。

## 准备环境

```python
import timeit

import numpy as np
import pandas as pd
```

准备数据：

```python
rng = np.random.default_rng(42)

returns = rng.normal(0.0005, 0.015, size=10_000)
prices = 100.0 * np.cumprod(1.0 + returns)

factor_data = pd.DataFrame({
    "momentum": rng.normal(0.0, 1.0, size=1_000),
    "volatility": rng.lognormal(mean=-2.0, sigma=0.4, size=1_000),
    "liquidity": rng.integers(1_000, 20_000, size=1_000),
})
```

## Python 循环和向量化表达

假设要计算一个简单打分：

```text
score = return^2 + 2 * return + 1
```

Python 循环写法：

```python
scores_loop = []

for value in returns:
    scores_loop.append(value * value + 2.0 * value + 1.0)

scores_loop = np.array(scores_loop)
```

向量化写法：

```python
scores_vec = returns * returns + 2.0 * returns + 1.0
```

验证两者相同：

```python
print(np.allclose(scores_loop, scores_vec))
```

向量化写法通常更快，因为 Python 不再逐个元素执行循环体。

## 向量化为什么通常更快

Python 的 `for` 循环每处理一个元素，都要执行解释器层面的操作：

- 取出对象。
- 做类型分派。
- 执行 Python 字节码。
- 调用运算方法。
- 把结果放回容器。

NumPy 数组通常是同类型、连续或规则步长的数据。`returns * returns` 可以把“逐元素乘法”交给底层循环完成。

简单计时可以这样写：

```python
def loop_score(x):
    out = []
    for value in x:
        out.append(value * value + 2.0 * value + 1.0)
    return np.array(out)


def vectorized_score(x):
    return x * x + 2.0 * x + 1.0


loop_seconds = min(timeit.repeat(lambda: loop_score(returns), number=10, repeat=3))
vec_seconds = min(timeit.repeat(lambda: vectorized_score(returns), number=10, repeat=3))

print(loop_seconds)
print(vec_seconds)
```

不要把一次计时当成绝对结论。性能和机器、数据规模、内存状态有关。更可靠的做法是用 `timeit` 或 profiler 找热点。

## ufunc：通用函数

NumPy 的很多函数是 ufunc，也就是 universal function。它们能对数组逐元素计算。

```python
log_return = np.log(prices[1:] / prices[:-1])

abs_return = np.abs(returns)
clipped_return = np.clip(returns, -0.05, 0.05)
```

这些操作都是批量处理：

- `np.log`：逐元素取对数。
- `np.abs`：逐元素取绝对值。
- `np.clip`：逐元素截断。

ufunc 通常支持广播、类型处理和 `out=` 参数，是 NumPy 向量化的核心。

## 布尔掩码和条件逻辑

很多 `if` 可以改写成布尔数组。

循环写法：

```python
buckets_loop = []

for value in returns[:10]:
    if value > 0.02:
        buckets_loop.append("strong_up")
    elif value < -0.02:
        buckets_loop.append("strong_down")
    else:
        buckets_loop.append("normal")
```

向量化写法：

```python
conditions = [
    returns[:10] > 0.02,
    returns[:10] < -0.02,
]
choices = ["strong_up", "strong_down"]

buckets_vec = np.select(conditions, choices, default="normal")

print(buckets_vec)
```

布尔掩码也可以用于过滤：

```python
large_move = np.abs(returns) > 0.03
large_move_returns = returns[large_move]

print(large_move_returns.shape)
```

这种写法清楚表达了“选出满足条件的元素”。

## 矩阵运算也是向量化

组合收益可以写成矩阵乘法。

```python
asset_returns = rng.normal(0.0005, 0.015, size=(252, 4))
weights = np.array([0.4, 0.3, 0.2, 0.1])

portfolio_return = asset_returns @ weights

print(portfolio_return.shape)
```

`@` 背后调用的是矩阵运算。它比手写双层循环更清楚，也更容易调用底层优化。

等价的循环：

```python
portfolio_loop = []

for t in range(asset_returns.shape[0]):
    total = 0.0
    for j in range(asset_returns.shape[1]):
        total += asset_returns[t, j] * weights[j]
    portfolio_loop.append(total)

portfolio_loop = np.array(portfolio_loop)

print(np.allclose(portfolio_loop, portfolio_return))
```

如果你能把问题表达成矩阵乘法、聚合、广播或 ufunc，通常优先使用这些成熟接口。

## pandas 中的向量化

pandas 的列运算通常会调用底层数组逻辑。

```python
factor_data["score"] = (
    factor_data["momentum"]
    - 0.5 * factor_data["volatility"]
    + np.log1p(factor_data["liquidity"]) / 10.0
)

factor_data["signal"] = np.where(
    factor_data["score"] > factor_data["score"].median(),
    1,
    -1,
)

print(factor_data[["score", "signal"]].head())
```

不要把这种列计算写成行级 `apply(axis=1)`，除非逻辑确实很难用列表达。

## apply 不是自动向量化

`apply` 是一个批量接口，但不一定是真正的底层向量化。

```python
def row_signal(row):
    score = row["momentum"] - 0.5 * row["volatility"] + np.log1p(row["liquidity"]) / 10.0
    return 1 if score > factor_data["score"].median() else -1


signal_apply = factor_data.apply(row_signal, axis=1)

print((signal_apply == factor_data["signal"]).all())
```

`apply(axis=1)` 通常会逐行构造对象并调用 Python 函数。它可能让代码看起来“批量”，但性能路径仍然接近 Python 循环。

## np.vectorize 的误区

`np.vectorize` 也容易被误解。它主要是为了让 Python 函数能用数组语法调用，不是性能优化工具。

```python
def classify_return(value):
    if value > 0.02:
        return "strong_up"
    if value < -0.02:
        return "strong_down"
    return "normal"


classify_vec = np.vectorize(classify_return)

labels = classify_vec(returns[:10])

print(labels)
```

这段代码可读，但底层仍然会反复调用 Python 函数。对性能敏感的数值逻辑，优先考虑 `np.where`、`np.select`、ufunc 或专门算法。

## 向量化可能增加内存占用

表达式越长，中间临时数组越多。

```python
x = np.arange(1_000, dtype=float)

y = (x * x + 2.0 * x + 1.0) / (x + 1.0)
```

这段代码清楚，但中间可能产生多个临时数组。对于小数组无所谓；对于几千万行数据，临时数组可能成为瓶颈。

可以使用分步写法提高可读性：

```python
numerator = x * x + 2.0 * x + 1.0
denominator = x + 1.0
y_step = numerator / denominator

print(np.allclose(y, y_step))
```

如果内存真的紧，可以考虑原地操作、`out=`、分块处理，或使用更合适的数据引擎。

## out= 和分块处理

`out=` 可以把结果写入已有数组，减少一次结果分配。

```python
x = np.arange(5, dtype=float)
out = np.empty_like(x)

np.multiply(x, x, out=out)
np.add(out, 1.0, out=out)

print(out)
```

对特别大的数组，也可以分块处理：

```python
def chunked_score(x, chunk_size=1_000):
    out = np.empty_like(x)

    for start in range(0, len(x), chunk_size):
        stop = min(start + chunk_size, len(x))
        chunk = x[start:stop]
        out[start:stop] = chunk * chunk + 2.0 * chunk + 1.0

    return out


scores_chunked = chunked_score(returns)

print(np.allclose(scores_chunked, scores_vec))
```

分块处理重新引入了 Python 循环，但每次处理的是一块数组，而不是一个元素。它常用于内存受限的批处理。

## 不适合硬向量化的逻辑

有些逻辑天然有状态依赖，例如止损规则：

```python
def stop_loss_position(returns, threshold=-0.05):
    position = np.ones_like(returns)
    cumulative = 0.0
    active = True

    for i, value in enumerate(returns):
        if active:
            cumulative += value
            if cumulative <= threshold:
                active = False
        else:
            position[i] = 0.0

    return position


position = stop_loss_position(returns[:50])

print(position)
```

这里当前状态依赖历史路径和是否已经触发止损。可以硬做复杂向量化，但未必更清楚。对于这类逻辑，可以先写正确清晰的循环，再用 numba、Cython、专门算法或分块方案优化。

## object dtype 的问题

向量化依赖同类型数组。`object` dtype 会让很多操作退回 Python 对象层。

```python
numeric = np.array([1.0, 2.0, 3.0])
objects = np.array([1.0, 2.0, 3.0], dtype=object)

print(numeric.dtype)
print(objects.dtype)

print(numeric * 2.0)
print(objects * 2.0)
```

两者结果看起来相同，但性能路径不同。数值计算中应尽量保持 `float64`、`int64`、`bool` 等明确 dtype。

## 常见坑

第一，把“看不到 for”误以为一定快。

`apply(axis=1)`、`np.vectorize` 可能看不到显式循环，但底层仍然在调用 Python 函数。

第二，为了向量化牺牲可读性。

一行极复杂的表达式很难审查。可以拆成几个有名字的中间变量。

第三，忽略临时数组内存。

长表达式会创建临时结果。数据很大时，内存可能比 CPU 更先成为瓶颈。

第四，忽略 dtype。

`object` dtype、混合类型列、字符串处理会显著改变性能路径。

第五，用向量化掩盖时间顺序。

时间序列特征中，向量化计算也必须遵守时间方向。比如 rolling、shift、未来收益标签不能混入未来信息。

## 实战提示

优化数值代码时可以按这个顺序：

1. 先写清楚正确的版本。
2. 用小样本断言循环版和向量化版结果一致。
3. 用 `timeit` 或 profiler 确认热点。
4. 优先使用 NumPy / pandas / scipy / sklearn 的内置批量接口。
5. 检查 dtype 和 shape。
6. 数据很大时，关注临时数组和内存峰值。
7. 对状态依赖强的逻辑，不要为了“没有 for”牺牲正确性。

一个重构模板：

```python
def score_loop(x):
    out = []
    for value in x:
        out.append(value * value + 2.0 * value + 1.0)
    return np.array(out)


def score_vectorized(x):
    return x * x + 2.0 * x + 1.0


sample = returns[:100]

assert np.allclose(score_loop(sample), score_vectorized(sample))
```

先用小样本证明等价，再扩大到全量数据。

## 小结

本节的重点：

- 向量化是把逐元素 Python 循环交给底层批量接口。
- 快的主要原因是减少解释器开销、使用同类型数组和底层优化循环。
- ufunc、广播、布尔掩码、矩阵乘法、pandas 列运算都是常见向量化形式。
- `apply(axis=1)` 和 `np.vectorize` 不等于性能向量化。
- 向量化可能增加临时数组和内存峰值。
- 有状态、路径依赖、早停逻辑不一定适合硬向量化。
- 正确性、可读性和可验证性优先于表面上的“没有 for”。

## 自检问题

1. 向量化为什么通常比 Python 层逐元素循环快？
2. `np.vectorize` 为什么不等于真正的性能优化？
3. 布尔掩码适合替代哪类 `if` 逻辑？
4. 为什么很长的向量化表达式可能导致内存问题？
5. 哪些场景不适合为了消除 `for` 而硬写向量化？
