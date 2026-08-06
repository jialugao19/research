# scipy：与 numpy 的关系、常用子模块、ndarray 互操作

## 核心概念

NumPy 提供数组和基础数值计算；SciPy 在 NumPy 数组之上提供更丰富的科学计算算法。

可以把二者理解为：

- NumPy：`ndarray`、广播、基础统计、基础线性代数、随机数。
- SciPy：优化、统计分布、稀疏矩阵、高级线性代数、积分、插值、信号处理、距离计算等。

SciPy 不是 pandas 的替代品，也不是新的数据容器。大多数 SciPy 函数接收 array-like 输入，内部按 NumPy 数组处理，返回标量、`ndarray`、稀疏矩阵或结果对象。它通常不会替你保留 pandas 的 index 和 columns。

## 准备环境

```python
import numpy as np
import pandas as pd
import scipy

from scipy import integrate
from scipy import special
from scipy.interpolate import interp1d
from scipy.spatial.distance import cdist

print(scipy.__version__)
```

这里不依赖具体版本号，只是确认 SciPy 已经可以导入。

## SciPy 常用子模块地图

初学 SciPy 时，不需要一次记住所有 API。先知道常用子模块负责什么：

- `scipy.stats`：概率分布、密度函数、分位数、假设检验、相关统计。
- `scipy.optimize`：函数最小化、约束优化、根查找。
- `scipy.linalg`：比 `numpy.linalg` 更完整的线性代数工具。
- `scipy.sparse`：稀疏矩阵格式和稀疏线性代数。
- `scipy.special`：sigmoid、gamma、beta、erf 等特殊函数。
- `scipy.spatial`：距离矩阵、KDTree、空间结构。
- `scipy.interpolate`：一维和多维插值。
- `scipy.integrate`：数值积分和微分方程求解。
- `scipy.signal`：滤波、卷积、频域分析等信号处理。

后续小节会重点展开 `stats`、`optimize`、`linalg`、`sparse`。本节先建立使用方式和数据形态。

## ndarray 输入，ndarray 输出

SciPy 的许多函数可以直接处理 NumPy 数组。

```python
x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])

prob = special.expit(x)
logit_back = special.logit(prob)

print(prob)
print(logit_back)
```

`special.expit` 是 sigmoid 函数：

```text
expit(x) = 1 / (1 + exp(-x))
```

它对数组逐元素计算，返回同形状的数组。

```python
print(type(prob))
print(prob.shape)
```

如果输入是二维数组，SciPy 函数通常也会保留数组维度，或者通过 `axis` 控制计算方向。

```python
scores = np.array([
    [1.0, 2.0, 3.0],
    [1.0, 1.0, 1.0],
])

row_prob = special.softmax(scores, axis=1)
col_prob = special.softmax(scores, axis=0)

print(row_prob)
print(row_prob.sum(axis=1))
print(col_prob)
print(col_prob.sum(axis=0))
```

理解 `axis` 的含义仍然是 NumPy 那套规则：`axis=0` 沿行方向压缩，`axis=1` 沿列方向压缩。

## array-like 输入会被当作数组

很多 SciPy 函数接受 list、tuple 或 pandas 对象，但实战里建议显式转成 NumPy 数组。

```python
values = [0.0, 1.0, 2.0]
out = special.expit(values)

print(out)
print(type(out))
```

这能运行，因为 list 是 array-like。但对于研究代码，推荐明确写出：

```python
arr = np.asarray(values, dtype=float)
out = special.expit(arr)
```

这样可以更早发现 dtype、缺失值和形状问题。

## pandas 互操作：显式保存标签

SciPy 主要处理数值数组，不负责 pandas 标签语义。假设有一个价格表：

```python
prices = pd.DataFrame(
    {
        "AAA": [100.0, 102.0, 101.0],
        "BBB": [50.0, 49.0, 51.0],
    },
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
)

print(prices)
```

如果要把它交给 SciPy 或 NumPy 数值函数，先保存标签，再取数组：

```python
idx = prices.index
cols = prices.columns
arr = prices.to_numpy(dtype=float)

scaled_arr = special.expit((arr - arr.mean(axis=0, keepdims=True)) / arr.std(axis=0, keepdims=True))

scaled = pd.DataFrame(scaled_arr, index=idx, columns=cols)

print(scaled)
```

这一段做了三件事：

1. 用 pandas 管理日期和资产标签。
2. 用 NumPy 数组交给数值函数计算。
3. 把结果重新包回 DataFrame，并恢复原来的 index 和 columns。

这比让 SciPy 函数直接接收 DataFrame 更可控。

## shape 很重要

SciPy 函数经常对输入形状有明确要求。例如距离矩阵 `cdist` 需要两个二维数组：

```python
a = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
])

b = np.array([
    [0.0, 1.0],
    [1.0, 1.0],
    [2.0, 1.0],
])

distance = cdist(a, b, metric="euclidean")

print(distance)
print(distance.shape)
```

这里 `a.shape == (2, 2)`，`b.shape == (3, 2)`，最后结果是 `(2, 3)`：`a` 的每一行到 `b` 的每一行的距离。

如果只有一个点，也要写成二维：

```python
point = np.array([0.0, 0.0])
point_2d = point.reshape(1, -1)

distance_from_point = cdist(point_2d, b)

print(distance_from_point)
print(distance_from_point.shape)
```

`reshape(1, -1)` 表示“1 行，多列”。很多 SciPy 函数会区分一维向量和二维样本矩阵。

## 数值积分例子

`scipy.integrate` 可以做数值积分。已知一组网格点上的函数值，可以用梯形法近似积分。

```python
grid = np.linspace(0.0, 1.0, 6)
y = grid ** 2

area = integrate.trapezoid(y, x=grid)

print(grid)
print(y)
print(area)
```

真实积分是：

```text
integral_0^1 x^2 dx = 1 / 3
```

梯形法使用离散点近似，所以结果接近但不完全等于 `1/3`。网格越密，误差通常越小。

```python
fine_grid = np.linspace(0.0, 1.0, 101)
fine_area = integrate.trapezoid(fine_grid ** 2, x=fine_grid)

print(fine_area)
```

## 插值例子

`scipy.interpolate` 可以根据已知点构造插值函数。

```python
x_grid = np.array([0.0, 1.0, 2.0, 3.0])
y_grid = np.array([0.0, 1.0, 4.0, 9.0])

linear_func = interp1d(x_grid, y_grid, kind="linear")

query = np.array([0.5, 1.5, 2.5])
estimated = linear_func(query)

print(estimated)
```

这里真实函数看起来像 `y = x^2`，但我们指定的是线性插值，所以 `0.5` 的估计值是 `0` 和 `1` 之间的线性中点。

插值和预测不是一回事。插值默认在已有点之间估计；如果要外推到范围之外，需要明确设置 `fill_value`，并承担更高风险。

## dtype 和缺失值

SciPy 数值算法通常需要数值 dtype。含有字符串、对象 dtype 或无法解释的缺失值时，应先清洗。

```python
raw = pd.Series(["1.0", "2.5", None, "bad"])

numeric = pd.to_numeric(raw, errors="coerce")
arr = numeric.to_numpy(dtype=float)

print(arr)
print(np.isfinite(arr))
```

`errors="coerce"` 会把无法转换的值变成 `NaN`。接下来要按业务逻辑决定是删除、填充，还是让算法跳过。

```python
clean_arr = arr[np.isfinite(arr)]

print(clean_arr)
print(special.expit(clean_arr))
```

不要把数据清洗交给 SciPy 函数“碰碰运气”。先明确缺失值含义，后续结果才可解释。

## 和 NumPy 的分工

有些任务 NumPy 就够了：

```python
x = np.array([1.0, 2.0, 3.0])

print(np.mean(x))
print(np.std(x))
print(np.linalg.norm(x))
```

当你需要更专门的算法时，再使用 SciPy：

```python
print(special.expit(x))
print(cdist(x.reshape(1, -1), np.zeros((1, 3))))
```

经验上：

- 数组创建、广播、简单聚合：优先 NumPy。
- 数据清洗、标签对齐、表格组织：优先 pandas。
- 优化、概率分布、稀疏矩阵、特殊函数、积分插值：使用 SciPy。

## 常见坑

第一，以为 SciPy 会保留 pandas 标签。

```python
arr = prices.to_numpy(dtype=float)
result_arr = special.expit(arr)
result = pd.DataFrame(result_arr, index=prices.index, columns=prices.columns)
```

需要标签时，自己保存并恢复。

第二，输入形状不符合算法预期。

```python
# 一维向量
x = np.array([1.0, 2.0, 3.0])

# 一行三列的二维矩阵
x_row = x.reshape(1, -1)

print(x.shape)
print(x_row.shape)
```

很多距离、机器学习、优化接口对这两种形状的解释不同。

第三，不检查 `NaN` 和 `inf`。

```python
arr = np.array([1.0, np.nan, np.inf])

print(np.isfinite(arr))
```

进入 SciPy 算法前，应先确认是否允许这些值存在。

第四，过早使用 SciPy 替代简单 NumPy。

如果只是均值、标准差、简单矩阵乘法，用 NumPy 更直接。SciPy 的价值在更专业的数值算法。

## 实战提示

把 SciPy 放进研究流程时，可以采用固定边界：

```python
# 1. pandas 中完成清洗和对齐
df = prices.copy()

# 2. 显式转成 ndarray
arr = df.to_numpy(dtype=float)

# 3. 检查形状和有限值
assert arr.ndim == 2
assert np.isfinite(arr).all()

# 4. 调用 SciPy / NumPy 数值算法
out = special.expit(arr)

# 5. 恢复标签
out_df = pd.DataFrame(out, index=df.index, columns=df.columns)
```

这个模板能减少标签错位、dtype 错误和形状误解。

## 小结

SciPy 的定位是“围绕 NumPy 数组的科学计算算法库”。

- 它擅长高级数值算法，不负责表格标签管理。
- 使用前要明确 dtype、shape、axis 和缺失值。
- 与 pandas 配合时，推荐显式 `to_numpy`，计算后再包回 DataFrame。
- 后续的 `stats`、`optimize`、`linalg`、`sparse` 都建立在这些数组语义之上。

## 自检问题

1. NumPy、pandas、SciPy 在数据分析流程里的分工分别是什么？
2. 为什么把 pandas DataFrame 交给 SciPy 前，通常要显式保存 index 和 columns？
3. `x.shape == (3,)` 和 `x.reshape(1, -1).shape == (1, 3)` 在 SciPy 函数里可能有什么区别？
4. 进入 SciPy 数值算法前，为什么要检查 `NaN` 和 `inf`？
5. 什么时候使用 NumPy 就够了，什么时候应该考虑 SciPy？
