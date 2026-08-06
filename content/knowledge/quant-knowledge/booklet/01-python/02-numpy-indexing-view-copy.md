# NumPy：索引、切片、视图与拷贝

## 核心概念

NumPy 的索引决定你取出哪些元素，也决定返回结果是否和原数组共享内存。

最重要的规则是：

- 标量索引会取出单个元素。
- 普通切片通常返回视图，也就是和原数组共享底层数据。
- 布尔索引和整数数组索引通常返回拷贝。
- 对视图赋值会修改原数组；对拷贝赋值不会修改原数组。

这几个规则很关键。很多研究代码的隐性 bug 都来自“我以为自己改的是临时结果，实际改了原数组”，或者“我以为自己改了原数组，实际只改了拷贝”。

## 一维数组索引

```python
import numpy as np

x = np.array([10, 20, 30, 40, 50])

print(x[0])     # 10
print(x[-1])    # 50
print(x[1:4])   # [20 30 40]
print(x[:3])    # [10 20 30]
print(x[::2])   # [10 30 50]
```

切片语法是 `start:stop:step`，其中 `stop` 不包含在结果里。

```python
print(x[1:4])  # 取下标 1, 2, 3
```

## 二维数组索引

二维数组常见写法是 `arr[row_index, col_index]`。

```python
m = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

print(m[0, 0])    # 1
print(m[1, 2])    # 6
print(m[0])       # [1 2 3]，第 0 行
print(m[:, 0])    # [1 4 7]，第 0 列
print(m[:2, 1:])  # 前两行，后两列
```

输出：

```text
[[2 3]
 [5 6]]
```

在量化数据里，如果 `returns.shape == (T, N)`，通常可以约定：

- `returns[t, i]`：第 `t` 个时间点、第 `i` 个资产的收益率。
- `returns[t, :]`：某个时间点的所有资产横截面。
- `returns[:, i]`：某个资产的完整时间序列。
- `returns[-20:, :]`：最近 20 个时间点的所有资产。

## 切片通常是视图

普通切片通常不复制数据，而是返回原数组的一个视图。

```python
x = np.array([10, 20, 30, 40, 50])

v = x[1:4]
v[0] = 999

print(v)  # [999  30  40]
print(x)  # [ 10 999  30  40  50]
```

`v` 改变后，`x` 也变了，因为 `v` 和 `x` 共享底层内存。

可以用 `np.shares_memory` 检查两个数组是否共享内存：

```python
x = np.array([10, 20, 30, 40, 50])
v = x[1:4]

print(np.shares_memory(x, v))  # True
```

## 显式 copy

如果你需要一个独立数组，用 `.copy()`。

```python
x = np.array([10, 20, 30, 40, 50])

y = x[1:4].copy()
y[0] = 999

print(y)  # [999  30  40]
print(x)  # [10 20 30 40 50]
```

实战里，只要你准备修改一个切片，同时又不希望影响原始数据，就应该显式写 `.copy()`。这比依赖隐式行为更清楚。

## 布尔索引

布尔索引用一个同形状的 True/False 数组筛选元素。

```python
x = np.array([0.01, -0.02, 0.03, -0.01, 0.00])

mask = x > 0
print(mask)     # [ True False  True False False]
print(x[mask])  # [0.01 0.03]
```

布尔索引常用于筛选满足条件的样本：

```python
returns = np.array([0.01, -0.02, 0.03, -0.01, 0.00])
volume = np.array([1000, 200, 1500, 3000, 100])

liquid_positive = (returns > 0) & (volume > 500)
print(returns[liquid_positive])  # [0.01 0.03]
```

注意：多个条件要用 `&`、`|`、`~`，并且每个条件最好用括号包起来。

```python
mask = (returns > 0) & (volume > 500)
```

不要写成：

```python
# mask = returns > 0 and volume > 500
```

`and` 是 Python 标量逻辑，不适用于 NumPy 数组的逐元素判断。

## 布尔索引赋值

直接对布尔索引位置赋值，会修改原数组。

```python
x = np.array([0.01, -0.02, 0.03, -0.01, 0.00])

x[x < 0] = 0.0

print(x)  # [0.01 0.   0.03 0.   0.  ]
```

这常用于 winsorize、截断异常值、填补特定条件下的缺失值。

```python
factor = np.array([0.2, 10.5, -9.8, 0.1, 0.3])
factor[factor > 3.0] = 3.0
factor[factor < -3.0] = -3.0

print(factor)  # [ 0.2  3.  -3.   0.1  0.3]
```

## 布尔索引读取通常是拷贝

布尔索引读取出来的结果通常是新数组，不和原数组共享内存。

```python
x = np.array([10, 20, 30, 40, 50])

y = x[x > 20]
y[0] = 999

print(y)  # [999  40  50]
print(x)  # [10 20 30 40 50]
```

如果你的目标是修改原数组，要对原数组本身做布尔索引赋值：

```python
x[x > 20] = 999
print(x)  # [ 10  20 999 999 999]
```

## 整数数组索引

整数数组索引可以按指定下标取元素。

```python
x = np.array([10, 20, 30, 40, 50])

idx = np.array([0, 3, 4])
print(x[idx])  # [10 40 50]
```

二维数组中，可以用整数数组选择行：

```python
m = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
])

rows = np.array([0, 2])
print(m[rows])
```

输出：

```text
[[1 2 3]
 [7 8 9]]
```

整数数组索引读取通常也会返回拷贝：

```python
x = np.array([10, 20, 30, 40, 50])
y = x[[0, 2, 4]]

print(np.shares_memory(x, y))  # False
```

## 实战例子：按流动性筛选横截面收益

假设某一天有 5 只股票的收益率、市值和成交额：

```python
import numpy as np

returns = np.array([0.012, -0.004, 0.021, -0.015, 0.006])
market_cap = np.array([80, 500, 1200, 60, 900])       # 亿元
turnover = np.array([0.03, 0.01, 0.08, 0.20, 0.04])  # 换手率

mask = (market_cap >= 100) & (turnover >= 0.03)
selected_returns = returns[mask]

print(mask)              # [False False  True False  True]
print(selected_returns)  # [0.021 0.006]
print(selected_returns.mean())  # 0.0135
```

这个例子展示了典型横截面筛选流程：

1. 每个条件生成一个布尔数组。
2. 用 `&` 合并条件。
3. 用布尔索引筛选对应样本。
4. 在筛选后的样本上计算统计量。

## 常见坑

### 1. 切片视图导致原数组被意外修改

```python
raw = np.array([1.0, 2.0, 3.0, 4.0])
window = raw[:3]

window -= window.mean()

print(raw)  # [-1.  0.  1.  4.]
```

如果你只想标准化临时窗口，应写：

```python
window = raw[:3].copy()
window -= window.mean()
```

### 2. 列切片变成一维数组

```python
m = np.arange(12).reshape(4, 3)

a = m[:, 0]
b = m[:, [0]]

print(a.shape)  # (4,)
print(b.shape)  # (4, 1)
```

`m[:, 0]` 取出一维数组，`m[:, [0]]` 保留二维形状。模型训练和矩阵乘法里，这个差别经常导致 shape 错误。

### 3. 混用切片和整数数组索引时要检查结果形状

```python
m = np.arange(12).reshape(4, 3)

print(m[:2, [0, 2]])
print(m[:2, [0, 2]].shape)  # (2, 2)
```

高级索引的 shape 规则比普通切片复杂。写研究代码时，不要猜，直接打印或 assert：

```python
out = m[:2, [0, 2]]
assert out.shape == (2, 2)
```

### 4. 链式索引容易误判是否修改原数组

```python
x = np.array([10, 20, 30, 40, 50])

x[x > 20][0] = 999

print(x)  # [10 20 30 40 50]
```

`x[x > 20]` 先生成了一个拷贝，后面的 `[0] = 999` 改的是这个临时拷贝，不是 `x`。应改成直接定位原数组：

```python
mask = x > 20
x[mask] = 999

print(x)  # [ 10  20 999 999 999]
```

## 实战提示

在涉及索引和赋值时，可以用下面的决策方式：

1. 只是读一段连续数据：用普通切片。
2. 要修改普通切片，但不能影响原数组：立刻加 `.copy()`。
3. 要按条件修改原数组：用 `arr[mask] = value`。
4. 要按条件取出样本做统计：用 `arr[mask]`，并记住它通常是拷贝。
5. 结果会进入模型或矩阵运算：立刻检查 `shape`。

对于关键逻辑，可以显式检查内存关系：

```python
view = x[1:4]
copy = x[[1, 2, 3]]

assert np.shares_memory(x, view)
assert not np.shares_memory(x, copy)
```

## 自检问题

1. `x[1:4]` 和 `x[[1, 2, 3]]` 在是否共享内存上有什么区别？
2. 为什么 `x[x > 0][0] = 999` 通常不会修改 `x`？
3. `m[:, 0]` 和 `m[:, [0]]` 的 shape 分别是什么？
4. 多个 NumPy 条件为什么要写 `(a > 0) & (b < 1)`，而不是 `a > 0 and b < 1`？
5. 如果你要修改一个滚动窗口里的临时数据，但不想改原始数组，应该怎么写？

