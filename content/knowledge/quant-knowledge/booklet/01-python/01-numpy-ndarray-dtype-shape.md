# 01. NumPy：ndarray、dtype 与 shape

## 核心概念

`numpy.ndarray` 是 NumPy 最核心的数据结构。它可以理解为一个固定类型、固定维度布局的多维数组。

一个数组最重要的几个属性是：

- `shape`：每个维度的长度，例如 `(3, 4)` 表示 3 行 4 列。
- `ndim`：维度数量，例如二维矩阵的 `ndim == 2`。
- `size`：元素总数，等于 `shape` 各维度相乘。
- `dtype`：每个元素的数据类型，例如 `int64`、`float64`、`bool`。
- `itemsize`：单个元素占用的字节数。
- `nbytes`：数组整体占用的字节数，通常等于 `size * itemsize`。

这些属性决定了数组能表达什么数据、会占用多少内存，以及后续计算是否稳定。

## 最小例子

```python
import numpy as np

x = np.array([[1, 2, 3], [4, 5, 6]])

print(x)
print(x.shape)     # (2, 3)
print(x.ndim)      # 2
print(x.size)      # 6
print(x.dtype)     # int64 或 int32，取决于平台
print(x.itemsize)  # 单个整数占用字节数
print(x.nbytes)    # 整个数组占用字节数
```

输出中的 `shape == (2, 3)` 表示这个数组有 2 行、3 列。量化研究中经常把二维数组约定成：

- 行：时间，例如交易日、分钟、tick。
- 列：资产、特征或不同策略。

例如一个收益率矩阵可以写成：

```python
returns = np.array([
    [0.01, -0.02, 0.00],
    [0.03,  0.01, -0.01],
    [-0.01, 0.02, 0.04],
])

print(returns.shape)  # (3, 3): 3 个时间点，3 个资产
```

## dtype 为什么重要

`dtype` 不是显示细节，而是计算语义的一部分。不同 dtype 会影响精度、内存和异常行为。

```python
prices_int = np.array([100, 101, 102])
prices_float = np.array([100.0, 101.0, 102.0])

print(prices_int.dtype)    # int64 或 int32
print(prices_float.dtype)  # float64
```

金融数据通常更适合用浮点数保存，因为收益率、价格调整、缺失值都会自然产生小数或 `nan`。

```python
x = np.array([1, 2, 3], dtype=float)
x[1] = np.nan

print(x)        # [ 1. nan  3.]
print(x.dtype)  # float64
```

如果数组是整数 dtype，直接放入 `np.nan` 会失败：

```python
y = np.array([1, 2, 3], dtype=int)

# y[1] = np.nan
# ValueError: cannot convert float NaN to integer
```

因此，带缺失值的数值数据通常要用 `float` dtype，或者在 pandas 中使用 nullable integer dtype。

## shape 与 reshape

`reshape` 可以改变数组的视图形状，但元素总数必须保持一致。

```python
x = np.arange(12)
print(x.shape)  # (12,)

m = x.reshape(3, 4)
print(m)
print(m.shape)  # (3, 4)
```

输出：

```text
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
```

下面这个 reshape 会报错，因为 12 个元素不能重排成 5 行 3 列：

```python
# x.reshape(5, 3)
# ValueError: cannot reshape array of size 12 into shape (5,3)
```

可以用 `-1` 让 NumPy 自动推断某一个维度：

```python
x = np.arange(12)

print(x.reshape(3, -1).shape)  # (3, 4)
print(x.reshape(-1, 6).shape)  # (2, 6)
```

但一个 shape 里只能有一个 `-1`，否则无法唯一推断。

## 实战例子：检查特征矩阵

假设你要训练一个模型，输入是 `X`，标签是 `y`：

```python
import numpy as np

X = np.array([
    [0.12, 1.3,  0.5],
    [0.08, 1.1, -0.2],
    [0.15, 0.9,  0.1],
    [0.03, 1.5, -0.4],
])

y = np.array([1, 0, 1, 0])

print(X.shape)  # (4, 3): 4 个样本，3 个特征
print(y.shape)  # (4,): 4 个标签

assert X.ndim == 2
assert y.ndim == 1
assert X.shape[0] == y.shape[0]
```

这三个 `assert` 很实用：它们能提前发现样本数不一致、标签维度错误、特征矩阵被错误转置等问题。

## 常见坑

### 1. 一维数组不是行向量也不是列向量

```python
x = np.array([1, 2, 3])

print(x.shape)  # (3,)
```

`(3,)` 是一维数组，不是 `(1, 3)`，也不是 `(3, 1)`。如果需要明确的二维形状：

```python
row = x.reshape(1, -1)
col = x.reshape(-1, 1)

print(row.shape)  # (1, 3)
print(col.shape)  # (3, 1)
```

这个区别会影响矩阵乘法、拼接和广播。

### 2. object dtype 通常是坏信号

```python
bad = np.array([1.0, 2.0, "missing"])

print(bad.dtype)  # <U32 或 object，取决于输入
```

一旦数值数组混入字符串或复杂 Python 对象，NumPy 很难继续使用高效的底层数值计算。量化数据清洗时，如果本该是数值的数组出现 `object` dtype，要优先排查原始数据是否混入了文本、空字符串或异常标记。

### 3. dtype 过小可能溢出

```python
x = np.array([120, 121, 122], dtype=np.int8)
print(x + 10)  # [-126 -125 -124]
```

`int8` 的范围是 -128 到 127。超过范围后会发生整数溢出。为了省内存主动压缩 dtype 时，必须确认取值范围。

## 实战提示

在写任何 NumPy 计算前，先问三个问题：

1. 这个数组的每个维度分别代表什么？
2. 这个数组是否需要表达缺失值？
3. 这个 dtype 是否足够精确、足够安全？

对于研究代码，建议在关键函数入口加轻量检查：

```python
def fit_factor_model(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    assert X.ndim == 2, "X must be a 2D feature matrix"
    assert y.ndim == 1, "y must be a 1D target array"
    assert X.shape[0] == y.shape[0], "X and y must have the same number of rows"

    # 后续模型拟合逻辑
```

这样做可以把很多隐蔽的数据形状错误提前暴露出来。

## 自检问题

1. `np.array([1, 2, 3]).shape` 是什么？它和 `(1, 3)` 有什么区别？
2. 为什么带有 `np.nan` 的数值数组通常要用 float dtype？
3. 一个 shape 为 `(252, 500)` 的收益率矩阵，如果约定行是日期、列是股票，那么 `shape[0]` 和 `shape[1]` 分别代表什么？
4. 为什么 `np.array([1.0, "2.0"])` 对后续数值计算可能有风险？
5. `np.arange(20).reshape(4, -1)` 的结果 shape 是什么？

