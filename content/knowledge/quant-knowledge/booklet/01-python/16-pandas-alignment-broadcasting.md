# 16. pandas：数据对齐与广播

## 核心概念

pandas 的算术运算默认按标签对齐，而不是按位置对齐。

- `Series` 运算按 index 对齐。
- `DataFrame` 运算按 index 和 columns 对齐。
- DataFrame 和 Series 运算时，默认尝试按列名对齐。
- 对齐失败的位置会产生 `NaN`。

这和 NumPy 很不同。NumPy 主要按 shape 和位置计算；pandas 会先看标签。

```python
import pandas as pd

a = pd.Series([1.0, 2.0, 3.0], index=["AAA", "BBB", "CCC"])
b = pd.Series([10.0, 20.0, 30.0], index=["CCC", "AAA", "BBB"])

print(a + b)
```

结果按资产代码对齐，不按顺序相加。

## Series 按 index 对齐

```python
returns = pd.Series(
    [0.01, -0.02, 0.03],
    index=["AAA", "BBB", "CCC"],
    name="return",
)

weights = pd.Series(
    [0.5, 0.3, 0.2],
    index=["AAA", "CCC", "BBB"],
    name="weight",
)

weighted = returns * weights

print(weighted)
print(weighted.sum())
```

虽然 `weights` 的顺序不是 `AAA, BBB, CCC`，但 pandas 会按 index 对齐：

```text
AAA: 0.01 * 0.5
BBB: -0.02 * 0.2
CCC: 0.03 * 0.3
```

这对金融数据非常重要，因为不同数据源的资产顺序经常不一致。

## 对齐带来的 NaN

如果两边标签不完全一致，缺失匹配的位置会变成 `NaN`。

```python
left = pd.Series([1.0, 2.0], index=["AAA", "BBB"])
right = pd.Series([10.0, 30.0], index=["AAA", "CCC"])

print(left + right)
```

输出中：

- `AAA` 两边都有，可以相加。
- `BBB` 只在左边，结果是 `NaN`。
- `CCC` 只在右边，结果是 `NaN`。

如果你希望缺失位置当作 0，可以使用显式方法：

```python
print(left.add(right, fill_value=0.0))
```

不要在不理解业务含义时随手填 0。缺失权重、缺失收益和缺失因子值含义不同。

## DataFrame 按 index 和 columns 对齐

DataFrame 运算会同时对齐行索引和列索引。

```python
df1 = pd.DataFrame(
    {
        "AAA": [1.0, 2.0],
        "BBB": [3.0, 4.0],
    },
    index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
)

df2 = pd.DataFrame(
    {
        "BBB": [10.0, 20.0],
        "CCC": [30.0, 40.0],
    },
    index=pd.to_datetime(["2024-01-03", "2024-01-04"]),
)

print(df1 + df2)
```

只有行和列同时匹配的位置才会得到数值。这个例子里，只有 `2024-01-03` 的 `BBB` 同时存在。

## reindex：显式对齐到目标标签

`reindex` 可以把对象对齐到指定 index 或 columns。

```python
target_assets = ["AAA", "BBB", "CCC"]

weights = pd.Series([0.5, 0.3], index=["AAA", "CCC"])
weights_aligned = weights.reindex(target_assets)

print(weights_aligned)
```

`BBB` 不在原始 weights 中，因此变成缺失。

如果你明确希望缺失权重为 0：

```python
weights_filled = weights.reindex(target_assets, fill_value=0.0)

print(weights_filled)
```

在组合计算里，缺失权重是否应为 0 取决于你的组合定义。对“未持仓资产”可以是 0；对“数据缺失”则不一定。

## align：同时对齐两个对象

`align` 可以同时对齐两个 Series 或 DataFrame。

```python
r1 = pd.Series([0.01, -0.02], index=["AAA", "BBB"])
r2 = pd.Series([0.03, 0.04], index=["BBB", "CCC"])

a1, a2 = r1.align(r2, join="outer")

print(a1)
print(a2)
```

`join` 可以是：

- `"outer"`：保留两边所有标签。
- `"inner"`：只保留两边共有标签。
- `"left"`：按左边标签对齐。
- `"right"`：按右边标签对齐。

如果只想比较共同资产：

```python
c1, c2 = r1.align(r2, join="inner")

print(c1)
print(c2)
```

## DataFrame 与 Series 广播：默认按列

DataFrame 和 Series 运算时，默认把 Series 的 index 当作列名，对齐到 DataFrame 的 columns。

```python
returns = pd.DataFrame(
    {
        "AAA": [0.01, 0.03],
        "BBB": [-0.02, 0.00],
        "CCC": [0.02, -0.01],
    },
    index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
)

weights = pd.Series([0.5, 0.3, 0.2], index=["AAA", "BBB", "CCC"])

weighted = returns * weights

print(weighted)
```

这里 `weights` 会按列广播到每一天。组合收益可以写成：

```python
portfolio_return = weighted.sum(axis=1)

print(portfolio_return)
```

## 按行广播：使用 axis

如果你想按行 index 对齐，需要使用算术方法并指定 `axis=0`。

```python
daily_cost = pd.Series(
    [0.001, 0.002],
    index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
)

net_returns = returns.sub(daily_cost, axis=0)

print(net_returns)
```

`axis=0` 表示把 `daily_cost` 按行 index 对齐，然后从每一行的所有列中减去对应成本。

如果直接写：

```python
wrong = returns - daily_cost

print(wrong)
```

pandas 会尝试把 `daily_cost.index` 当作列名对齐，通常会得到意外的列和大量 `NaN`。

## 常用算术方法

pandas 提供显式算术方法，常用于控制对齐和缺失填充：

- `add`
- `sub`
- `mul`
- `div`

```python
left = pd.Series([1.0, 2.0], index=["AAA", "BBB"])
right = pd.Series([10.0, 30.0], index=["AAA", "CCC"])

print(left.add(right, fill_value=0.0))
```

DataFrame 中指定方向：

```python
print(returns.mul(weights, axis=1))
print(returns.sub(daily_cost, axis=0))
```

`axis=1` 表示按列对齐，`axis=0` 表示按行对齐。

## 实战例子：组合收益计算

假设收益矩阵是宽表，行是日期，列是资产：

```python
returns = pd.DataFrame(
    {
        "AAA": [0.01, 0.03],
        "BBB": [-0.02, 0.00],
        "CCC": [0.02, -0.01],
    },
    index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
)

weights = pd.Series(
    [0.5, 0.2, 0.3],
    index=["AAA", "CCC", "BBB"],
)

weights = weights.reindex(returns.columns)
portfolio_return = returns.mul(weights, axis=1).sum(axis=1)

print(weights)
print(portfolio_return)
```

即使权重原始顺序不同，`reindex(returns.columns)` 也能把顺序显式对齐到收益矩阵列顺序。

如果权重缺少某个资产，`reindex` 会产生缺失。此时应该主动检查：

```python
assert weights.notna().all()
```

这比让缺失权重默默进入组合计算更安全。

## 实战例子：横截面去均值

假设每天要从每只股票收益中减去当天横截面均值：

```python
daily_mean = returns.mean(axis=1)
demeaned = returns.sub(daily_mean, axis=0)

print(daily_mean)
print(demeaned)
```

这里必须使用 `axis=0`，因为 `daily_mean.index` 是日期，要按行对齐。

如果写成：

```python
wrong = returns - daily_mean
```

pandas 会默认按列对齐，结果通常不是想要的横截面去均值。

## 实战例子：行业暴露矩阵对齐

假设有股票行业暴露矩阵和资产权重：

```python
exposure = pd.DataFrame(
    {
        "tech": [1.0, 0.0, 1.0],
        "finance": [0.0, 1.0, 0.0],
    },
    index=["AAA", "BBB", "CCC"],
)

weights = pd.Series([0.5, 0.3, 0.2], index=["AAA", "BBB", "CCC"])

industry_weight = exposure.mul(weights, axis=0).sum(axis=0)

print(industry_weight)
```

`axis=0` 表示把权重按股票 index 对齐到 exposure 的行。结果是组合在每个行业上的权重。

## 与 NumPy 的区别

```python
a = pd.Series([1.0, 2.0], index=["AAA", "BBB"])
b = pd.Series([10.0, 20.0], index=["BBB", "AAA"])

print(a + b)
print(a.to_numpy() + b.to_numpy())
```

pandas 结果按标签：

```text
AAA    21.0
BBB    12.0
dtype: float64
```

NumPy 结果按位置：

```text
[11. 22.]
```

进入机器学习模型或 NumPy 矩阵运算前，如果使用 `.to_numpy()`，必须确认行列顺序已经固定。

## 常见坑

### 1. 以为 pandas 按位置计算

两个 Series 顺序不同但 index 相同，pandas 会按 index 对齐。多数时候这是保护，但如果 index 错了，就是风险。

### 2. DataFrame 减 Series 时方向错

```python
# 通常不是横截面去均值
wrong = returns - returns.mean(axis=1)
```

正确写法：

```python
right = returns.sub(returns.mean(axis=1), axis=0)
```

### 3. fill_value=0 掩盖数据问题

```python
left.add(right, fill_value=0)
```

这会把缺失匹配当成 0。对于持仓权重可能合理，对于缺失收益或缺失因子值可能不合理。

### 4. reindex 后不检查 NaN

```python
weights = weights.reindex(returns.columns)
```

如果权重少了某只股票，会出现 `NaN`。后续应检查：

```python
assert weights.notna().all()
```

### 5. to_numpy 后丢失标签保护

`to_numpy()` 后就不再按 index/columns 对齐。矩阵乘法前必须确认 `returns.columns` 和 `weights.index` 顺序一致。

## 实战提示

写 pandas 对齐代码时，建议显式表达方向：

```python
# 按资产列对齐
weighted = returns.mul(weights, axis=1)

# 按日期行对齐
demeaned = returns.sub(returns.mean(axis=1), axis=0)
```

关键计算前加检查：

```python
weights = weights.reindex(returns.columns)
assert weights.index.equals(returns.columns)
assert weights.notna().all()

portfolio_return = returns.mul(weights, axis=1).sum(axis=1)
```

如果要转 NumPy：

```python
X = returns.to_numpy()
w = weights.reindex(returns.columns).to_numpy()
```

先对齐，再转换。

## 自检问题

1. pandas 的 Series 运算默认按位置对齐还是按 index 对齐？
2. DataFrame 和 Series 相乘时，默认按 DataFrame 的行还是列对齐？
3. `returns.sub(daily_mean, axis=0)` 里的 `axis=0` 表示什么？
4. `reindex` 后为什么要检查缺失值？
5. 为什么 `.to_numpy()` 前必须确认行列顺序？

