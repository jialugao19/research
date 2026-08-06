# 43. Python 理解项：memory layout 内存布局、连续性、视图与拷贝

## 核心概念

NumPy 数组不是“嵌套 Python 列表”。它更像一段连续或规则跳步的内存，加上一组解释这段内存的元数据。

最重要的元数据是：

- `dtype`：每个元素是什么类型，占多少字节。
- `shape`：数组有几维，每一维多长。
- `strides`：每一维移动一步，需要在内存中跳过多少字节。
- `flags`：数组是否 C 连续、Fortran 连续、是否可写等。

理解 memory layout 可以解释很多现象：

- 为什么切片常常是视图。
- 为什么转置通常不复制数据。
- 为什么某些 `reshape` 很便宜，某些会复制。
- 为什么 `flatten` 和 `ravel` 不一样。
- 为什么非连续数组传给底层库时可能被隐式复制。
- 为什么看似很小的切片可能让一个大数组无法释放。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一个二维数组：

```python
x = np.arange(12, dtype=np.float64).reshape(3, 4)

print(x)
print(x.dtype)
print(x.shape)
print(x.strides)
print(x.flags["C_CONTIGUOUS"])
```

`float64` 每个元素占 8 字节。`shape == (3, 4)` 表示 3 行 4 列。

## strides 如何解释二维数组

对 C 连续的二维数组：

```python
x = np.arange(12, dtype=np.float64).reshape(3, 4)

print(x.strides)
```

输出通常是：

```text
(32, 8)
```

含义：

- 行方向移动一步，跳过 32 字节，也就是 4 个 `float64`。
- 列方向移动一步，跳过 8 字节，也就是 1 个 `float64`。

访问 `x[i, j]` 时，内存偏移大致是：

```text
offset = i * stride_row + j * stride_col
```

所以 `shape` 决定逻辑形状，`strides` 决定如何在内存里走。

## itemsize 和 nbytes

```python
print(x.dtype.itemsize)
print(x.size)
print(x.nbytes)
```

对 `float64`：

```text
nbytes = size * itemsize
```

这个例子里有 12 个元素，每个 8 字节，所以数据本身占 96 字节。注意这只是数组数据区大小，不包括 Python 对象元数据。

## C 连续和 Fortran 连续

NumPy 常见两种连续布局：

- C order：最后一维连续，行优先。
- Fortran order：第一维连续，列优先。

```python
c_order = np.arange(12, dtype=np.float64).reshape(3, 4)
f_order = np.asfortranarray(c_order)

print(c_order.strides)
print(f_order.strides)

print(c_order.flags["C_CONTIGUOUS"], c_order.flags["F_CONTIGUOUS"])
print(f_order.flags["C_CONTIGUOUS"], f_order.flags["F_CONTIGUOUS"])
```

对同样的 `shape == (3, 4)`：

- C order 的 strides 通常是 `(32, 8)`。
- Fortran order 的 strides 通常是 `(8, 24)`。

两者数值内容可以一样，但内存排列不同。

## 转置通常是视图

转置并不一定复制数据。它通常只是交换 `shape` 和 `strides`。

```python
x = np.arange(12, dtype=np.float64).reshape(3, 4)
xt = x.T

print(xt.shape)
print(xt.strides)
print(np.shares_memory(x, xt))
print(xt.flags["C_CONTIGUOUS"])
```

`xt` 和 `x` 共享内存。修改 `xt` 会影响 `x`。

```python
xt[0, 0] = 999.0

print(x[0, 0])
```

这也是为什么要谨慎修改转置、切片等视图。

## 切片和步长

普通切片通常是视图。

```python
x = np.arange(12, dtype=np.float64).reshape(3, 4)

view = x[:, ::2]

print(view)
print(view.shape)
print(view.strides)
print(np.shares_memory(x, view))
print(view.flags["C_CONTIGUOUS"])
```

`x[:, ::2]` 每隔一列取一次，所以列方向 stride 变大。这个 `view` 不是 C 连续数组。

非连续视图很常见。它能避免复制，但有些底层库要求连续输入，这时可能发生隐式复制。

## copy：显式断开共享内存

如果你要修改切片，但不希望影响原数组，就显式复制。

```python
x = np.arange(12, dtype=np.float64).reshape(3, 4)

view = x[:, ::2]
copy = view.copy()

copy[0, 0] = -1.0

print(x[0, 0])
print(copy[0, 0])
print(np.shares_memory(x, copy))
```

`.copy()` 会创建独立数据区。代码里显式写 `.copy()`，比依赖隐式行为更安全。

## ravel 和 flatten

`ravel` 尽量返回视图；`flatten` 总是返回拷贝。

```python
x = np.arange(12, dtype=np.float64).reshape(3, 4)

r = x.ravel()
f = x.flatten()

print(np.shares_memory(x, r))
print(np.shares_memory(x, f))
```

修改 `r` 可能影响 `x`；修改 `f` 不会。

```python
r[0] = 100.0
f[1] = 200.0

print(x[0, 0])
print(x[0, 1])
```

如果你明确需要独立一维数组，用 `flatten()` 或 `ravel().copy()`。

## 非连续数组的 ravel 可能复制

对非连续数组，`ravel(order="C")` 通常需要复制。

```python
x = np.arange(12, dtype=np.float64).reshape(3, 4)
xt = x.T

ravel_xt = xt.ravel(order="C")

print(np.shares_memory(xt, ravel_xt))
print(ravel_xt.flags["C_CONTIGUOUS"])
```

因为 `xt` 的 C 顺序遍历无法直接用原始内存中的简单连续视图表达，所以 NumPy 会创建新数组。

这类行为不应该靠猜。需要确认时，用 `np.shares_memory` 和 `arr.flags` 检查。

## reshape 可能是视图，也可能是拷贝

连续数组 reshape 通常很便宜。

```python
x = np.arange(12, dtype=np.float64)

y = x.reshape(3, 4)

print(np.shares_memory(x, y))
print(y.shape)
```

但对非连续数组，某些 reshape 需要复制。

```python
z = y[:, ::2]
z_reshaped = z.reshape(-1)

print(z.flags["C_CONTIGUOUS"])
print(np.shares_memory(z, z_reshaped))
```

不要假设 `reshape` 一定不复制。看 `strides`、`flags`，或者用 `np.shares_memory` 验证。

## ascontiguousarray

如果某个底层函数需要 C 连续数组，可以显式转换。

```python
x = np.arange(12, dtype=np.float64).reshape(3, 4)
view = x[:, ::2]

contiguous = np.ascontiguousarray(view)

print(view.flags["C_CONTIGUOUS"])
print(contiguous.flags["C_CONTIGUOUS"])
print(np.shares_memory(view, contiguous))
```

如果输入已经 C 连续，`np.ascontiguousarray` 通常不会复制；如果不是连续的，它会复制。

```python
same = np.ascontiguousarray(x)

print(np.shares_memory(x, same))
```

这比让底层库隐式复制更可控。

## 高级索引通常复制

布尔索引和整数数组索引通常会创建拷贝。

```python
x = np.arange(10, dtype=np.float64)

mask = x % 2 == 0
even = x[mask]
picked = x[[0, 2, 4]]

print(np.shares_memory(x, even))
print(np.shares_memory(x, picked))
```

如果你的目标是修改原数组，要对原数组做布尔赋值：

```python
x[x % 2 == 0] = -1.0

print(x)
```

读取出来再改，通常不会改回原数组。

## 小切片可能保留大数组

视图会持有对底层数据的引用。一个很小的切片可能让大数组无法释放。

```python
large = np.arange(1_000_000, dtype=np.float64)
small_view = large[:5]

print(np.shares_memory(large, small_view))
print(small_view.base is not None)
```

如果你只需要这 5 个值，并希望大数组可以被释放，应该复制：

```python
small_copy = large[:5].copy()

print(np.shares_memory(large, small_copy))
```

在长时间运行的任务里，这类“很小的视图持有很大的底层数组”会造成隐性内存占用。

## pandas 到 NumPy 的内存注意点

pandas DataFrame 不是简单二维 NumPy 数组。它可能按列、dtype block 或扩展数组组织。

```python
df_numeric = pd.DataFrame({
    "a": [1.0, 2.0, 3.0],
    "b": [4.0, 5.0, 6.0],
})

arr_numeric = df_numeric.to_numpy(copy=False)

print(arr_numeric.dtype)
print(arr_numeric.shape)
```

`copy=False` 是“尽量不复制”，不是保证不复制。不同 dtype、扩展类型、列布局都可能导致复制。

混合类型更明显：

```python
df_mixed = pd.DataFrame({
    "a": [1.0, 2.0, 3.0],
    "label": ["x", "y", "z"],
})

arr_mixed = df_mixed.to_numpy()

print(arr_mixed.dtype)
```

混合数值和字符串时，结果通常是 `object` 数组。它不适合高性能数值计算。

## 常见坑

第一，以为转置一定复制。

转置通常只是视图，修改转置结果可能影响原数组。

第二，以为 reshape 一定不复制。

连续数组 reshape 通常是视图；非连续数组 reshape 可能复制。

第三，把非连续数组传给底层库时忽略隐式复制。

很多底层算法需要连续内存。显式使用 `np.ascontiguousarray` 可以让复制更可控。

第四，过度依赖 `arr.base` 判断共享。

`arr.base` 有时能提供线索，但更推荐用 `np.shares_memory(a, b)` 检查两个数组是否共享内存。

第五，忽略 pandas 的数据组织。

DataFrame 的 `to_numpy(copy=False)` 不保证零拷贝。混合 dtype 还可能得到 `object` 数组。

## 实战提示

排查内存布局问题时，先打印：

```python
def describe_array(name, arr):
    print(name)
    print("  shape:", arr.shape)
    print("  dtype:", arr.dtype)
    print("  strides:", arr.strides)
    print("  nbytes:", arr.nbytes)
    print("  C contiguous:", arr.flags["C_CONTIGUOUS"])
    print("  F contiguous:", arr.flags["F_CONTIGUOUS"])
    print("  writeable:", arr.flags["WRITEABLE"])


describe_array("x", x)
describe_array("x.T", x.T)
```

经验规则：

1. 要修改切片且不影响原数组：显式 `.copy()`。
2. 要传给要求 C 连续的底层函数：显式 `np.ascontiguousarray(...)`。
3. 要确认是否共享内存：用 `np.shares_memory(...)`。
4. 要从 pandas 进入 NumPy 数值计算：先确认 dtype，不要让 `object` 数组混入。
5. 大数组切出小片段并长期保存时，考虑 `.copy()` 释放大数组引用。

## 小结

本节的重点：

- NumPy 数组由数据区加 `dtype`、`shape`、`strides` 等元数据组成。
- `strides` 决定每一维移动一步在内存里跳多少字节。
- C 连续和 Fortran 连续是两种常见布局。
- 切片和转置通常是视图，可能共享内存。
- `flatten()` 总是拷贝，`ravel()` 尽量返回视图。
- 非连续数组 reshape、ravel 或传给底层库时可能复制。
- pandas 的 `to_numpy(copy=False)` 不保证零拷贝，混合 dtype 可能变成 `object` 数组。

## 自检问题

1. `shape` 和 `strides` 分别描述什么？
2. C 连续数组和 Fortran 连续数组有什么区别？
3. 为什么转置通常可以不复制数据？
4. `ravel()` 和 `flatten()` 在拷贝行为上有什么区别？
5. 为什么一个很小的切片可能让大数组无法释放？
