# 05. NumPy：向量化计算与性能

## 核心概念

向量化是指把“逐个元素的 Python 循环”改写成“对整个数组的一次 NumPy 运算”。NumPy 的很多运算在底层用 C 实现，能一次处理连续内存中的大量元素，通常比 Python 层的 `for` 循环快很多。

典型区别是：

```python
import numpy as np

x = np.array([1.0, 2.0, 3.0])

print(x * x + 1.0)  # [ 2.  5. 10.]
```

这行代码表达的是“对所有元素做同一个公式”，而不是显式写循环。

## 循环写法与向量化写法

假设要计算每个元素的平方：

```python
import numpy as np

x = np.array([1.0, 2.0, 3.0, 4.0])

out = []
for value in x:
    out.append(value * value)

out = np.array(out)
print(out)  # [ 1.  4.  9. 16.]
```

向量化写法更短：

```python
out = x * x

print(out)  # [ 1.  4.  9. 16.]
```

这两段逻辑等价，但第二段通常更快、更清楚，也更不容易写错边界条件。

## 实战例子：价格转收益率

给定一段价格序列，简单收益率定义为：

```text
return[t] = price[t] / price[t-1] - 1
```

循环写法：

```python
prices = np.array([100.0, 102.0, 101.0, 105.0])

returns = []
for i in range(1, len(prices)):
    returns.append(prices[i] / prices[i - 1] - 1.0)

returns = np.array(returns)
print(returns)
```

向量化写法：

```python
returns_vec = prices[1:] / prices[:-1] - 1.0

print(returns_vec)
```

输出：

```text
[ 0.02       -0.00980392  0.03960396]
```

`prices[1:]` 是当前价格，`prices[:-1]` 是前一期价格。两个切片 shape 相同，所以可以逐元素相除。

## 实战例子：批量计算组合收益

假设 `returns.shape == (T, N)`，行是日期，列是资产；`weights.shape == (N,)`，表示每只资产的组合权重。

```python
returns = np.array([
    [0.01,  0.02, -0.01],
    [0.03,  0.01,  0.02],
    [-0.02, 0.00,  0.01],
])

weights = np.array([0.5, 0.3, 0.2])

portfolio_returns = returns @ weights

print(portfolio_returns)  # [ 0.009  0.022 -0.008]
```

`@` 是矩阵乘法。这里它一次性完成每一天的加权求和：

```text
portfolio_return[t] = sum(returns[t, i] * weights[i])
```

如果用循环写，也能得到同样结果：

```python
out = []
for t in range(returns.shape[0]):
    out.append((returns[t] * weights).sum())

out = np.array(out)
print(out)  # [ 0.009  0.022 -0.008]
```

但矩阵乘法更直接，也通常更高效。

## 条件逻辑的向量化

很多 `if` 也可以改成布尔数组或 `np.where`。

假设要把收益率截断到 `[-0.05, 0.05]`：

```python
r = np.array([0.02, -0.10, 0.08, 0.01])

clipped = np.where(r > 0.05, 0.05, r)
clipped = np.where(clipped < -0.05, -0.05, clipped)

print(clipped)  # [ 0.02 -0.05  0.05  0.01]
```

更直接的写法是 `np.clip`：

```python
clipped = np.clip(r, -0.05, 0.05)

print(clipped)  # [ 0.02 -0.05  0.05  0.01]
```

如果要按条件赋值，也可以用布尔索引：

```python
r2 = r.copy()
r2[r2 > 0.05] = 0.05
r2[r2 < -0.05] = -0.05

print(r2)  # [ 0.02 -0.05  0.05  0.01]
```

## 简单性能计时

在脚本里可以用 `time.perf_counter()` 做粗略计时。

```python
import time
import numpy as np

n = 1_000_000
x = np.arange(n, dtype=float)

start = time.perf_counter()
out_loop = np.empty_like(x)
for i in range(n):
    out_loop[i] = x[i] * x[i] + 1.0
loop_seconds = time.perf_counter() - start

start = time.perf_counter()
out_vec = x * x + 1.0
vec_seconds = time.perf_counter() - start

print(np.allclose(out_loop, out_vec))  # True
print(loop_seconds > vec_seconds)      # 通常是 True
```

实际耗时会受机器、负载、数组大小影响。不要把一次计时当作严格结论。对于研究代码，先用简单计时找到数量级差异；如果要严肃优化，再使用 `timeit`、`cProfile` 或专门 profiler。

## 向量化不等于永远更省内存

向量化可能创建临时数组。比如：

```python
x = np.arange(5, dtype=float)

y = (x * x + 2 * x + 1) / (x + 1)

print(y)  # [1. 2. 3. 4. 5.]
```

这个表达式可读性很好，但中间可能产生多个临时数组，例如 `x * x`、`2 * x`、`x + 1`。对小数组无所谓，对非常大的数组可能占用明显内存。

可以用分步写法提高可读性并便于检查：

```python
numerator = x * x + 2 * x + 1
denominator = x + 1
y = numerator / denominator
```

如果内存很紧，可以考虑原地操作或 `out=` 参数。

## 原地操作与 out 参数

原地操作会修改已有数组，减少额外分配：

```python
x = np.array([1.0, 2.0, 3.0])

x *= 2.0
x += 1.0

print(x)  # [3. 5. 7.]
```

一些 NumPy 函数支持 `out=`，把结果写入已有数组：

```python
x = np.array([1.0, 2.0, 3.0])
out = np.empty_like(x)

np.multiply(x, x, out=out)

print(out)  # [1. 4. 9.]
```

`out=` 常用于内存敏感的批处理任务。但它会让代码更啰嗦，不应为了微小优化过早使用。

## 实战例子：向量化回测中的交易成本

假设 `position.shape == (T, N)`，表示每天收盘后的目标仓位；相邻两天仓位变化产生换手。交易成本可以近似写成：

```text
cost[t, i] = abs(position[t, i] - position[t-1, i]) * cost_rate[i]
```

向量化实现：

```python
position = np.array([
    [0.2, 0.3, 0.5],
    [0.1, 0.4, 0.5],
    [0.0, 0.6, 0.4],
])

cost_rate = np.array([0.001, 0.002, 0.0015])

turnover = np.abs(position[1:] - position[:-1])
cost = turnover * cost_rate
daily_cost = cost.sum(axis=1)

print(turnover)
print(daily_cost)
```

输出：

```text
[[0.1 0.1 0. ]
 [0.1 0.2 0.1]]
[0.0003  0.00065]
```

这个例子里：

- `position[1:] - position[:-1]` 一次性计算所有相邻日期的仓位变化。
- `cost_rate.shape == (N,)` 会按列广播。
- `sum(axis=1)` 得到每天的总交易成本。

## 常见坑

### 1. 向量化表达式隐藏未来信息

向量化很容易写出“看起来正确，但时间方向错了”的代码。

```python
prices = np.array([100.0, 102.0, 101.0, 105.0])

future_return = prices[1:] / prices[:-1] - 1.0
```

这行计算的是从今天到明天的收益。如果它被当作今天可用的特征，就会产生未来信息泄露。用于预测时，要明确它是标签还是特征，并在数据对齐时使用正确的 `shift` 逻辑。

### 2. 过度向量化让代码不可读

一行很长的向量化表达式不一定更好：

```python
# 难读
score = ((x - np.nanmean(x, axis=1, keepdims=True)) / np.nanstd(x, axis=1, keepdims=True)).clip(-3, 3)
```

更建议拆成几步：

```python
mean = np.nanmean(x, axis=1, keepdims=True)
std = np.nanstd(x, axis=1, keepdims=True)
score = (x - mean) / std
score = np.clip(score, -3, 3)
```

拆开以后更容易检查 shape，也更容易处理 `std == 0` 等异常情况。

### 3. Python 函数包一层不一定真正向量化

`np.vectorize` 主要是便利工具，不会把普通 Python 函数变成高速底层循环。

```python
def sign_label(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

label_func = np.vectorize(sign_label)
print(label_func(np.array([0.1, -0.2, 0.0])))  # [ 1 -1  0]
```

这段写法方便，但通常不是真正的性能优化。更好的写法是使用数组表达式：

```python
r = np.array([0.1, -0.2, 0.0])
label = np.where(r > 0, 1, np.where(r < 0, -1, 0))

print(label)  # [ 1 -1  0]
```

### 4. 小数据上优化意义有限

如果数组只有几十个元素，循环和向量化的性能差异通常不重要。优先写清楚、可验证的代码。性能优化应该从真实瓶颈出发，而不是从风格偏好出发。

## 实战提示

写 NumPy 性能相关代码时，可以按这个顺序做：

1. 先写清楚、正确的版本。
2. 用小样本和断言验证结果。
3. 用向量化替换热点循环。
4. 用简单计时确认是否真的改善。
5. 如果内存变成瓶颈，再考虑分块、原地操作、`out=` 或更合适的数据结构。

对量化研究尤其重要的是：性能优化不能改变时间对齐。快但泄露未来信息的回测没有价值。

## 自检问题

1. 为什么 NumPy 向量化通常比 Python `for` 循环快？
2. `prices[1:] / prices[:-1] - 1` 计算的是哪个方向的收益？作为特征使用时有什么风险？
3. `np.where`、布尔索引和 `np.clip` 分别适合什么条件处理场景？
4. 为什么向量化表达式可能增加内存占用？
5. `np.vectorize` 为什么通常不应该被当作性能优化工具？

