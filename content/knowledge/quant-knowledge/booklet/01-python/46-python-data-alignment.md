# Python 理解项：数据对齐的语义、风险与调试方法

## 核心概念

数据对齐不是简单的“两个数组长度一样”。它回答的是：

```text
这一行数据和另一行数据，是否代表同一个样本、同一个时间点、同一个资产、同一个特征顺序？
```

在 Python 数据分析中，对齐规则很容易跨库改变：

- pandas：大多数运算按 index / columns 标签对齐。
- NumPy：按位置和 shape 计算，不理解 index。
- sklearn：训练时通常按行位置配对 `X` 和 `y`，不会自动按 pandas index 对齐。
- 时间序列：还要区分预测时点、特征可见时点和标签发生时点。

数据错位通常不会报错。它更危险：代码能跑，结果却是错的。

本节关注：

- pandas 按标签对齐的语义。
- NumPy / sklearn 按位置处理的风险。
- 时间序列特征和标签如何显式对齐。
- MultiIndex 面板数据如何检查对齐。
- 常用调试断言和排查方法。

## 准备环境

```python
import numpy as np
import pandas as pd
```

准备一些基础数据：

```python
dates = pd.to_datetime([
    "2024-01-02",
    "2024-01-03",
    "2024-01-04",
    "2024-01-05",
])

assets = ["AAA", "BBB", "CCC"]
```

## pandas 按标签对齐

pandas 的 Series 运算按 index 对齐，而不是按行号对齐。

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

虽然 `weights` 的顺序是 `AAA, CCC, BBB`，pandas 仍然会按资产代码对齐。

这通常是好事：金融数据来自不同数据源时，资产顺序经常不一致。

## NumPy 按位置计算

一旦转成 NumPy，就没有 index 保护。

```python
weighted_positional = returns.to_numpy() * weights.to_numpy()

print(weighted_positional)
print(weighted_positional.sum())
```

这段计算会按当前位置相乘：

```text
AAA return * AAA weight
BBB return * CCC weight
CCC return * BBB weight
```

第二、第三项已经错位，但 NumPy 不知道。进入 NumPy 前，要先显式对齐：

```python
weights_aligned = weights.reindex(returns.index)

weighted_numpy_safe = returns.to_numpy() * weights_aligned.to_numpy()

print(weighted_numpy_safe)
```

关键原则：

```text
转成 NumPy 前，先用 pandas 对齐并固定顺序。
```

## 对齐失败会产生 NaN

如果标签不完全匹配，pandas 会在无法对齐的位置产生缺失。

```python
left = pd.Series([1.0, 2.0], index=["AAA", "BBB"])
right = pd.Series([10.0, 30.0], index=["AAA", "CCC"])

combined = left + right

print(combined)
```

结果里只有 `AAA` 可以相加，`BBB` 和 `CCC` 会变成 `NaN`。

不要看到 NaN 就立刻填 0。缺失可能表示：

- 确实没有持仓，权重可以是 0。
- 数据源缺失，需要排查。
- 资产池不一致，需要取交集。
- 日期不一致，需要重新定义样本范围。

## 显式选择 inner / outer 对齐

`align` 可以把对齐方式写清楚。

```python
left_inner, right_inner = left.align(right, join="inner")

print(left_inner)
print(right_inner)
```

`join="inner"` 只保留共同标签。

```python
left_outer, right_outer = left.align(right, join="outer")

print(left_outer)
print(right_outer)
```

`join="outer"` 保留两边所有标签，缺失处为 NaN。

在研究代码里，建议显式写出你的选择，而不是让默认行为悄悄决定样本。

## DataFrame 行列同时对齐

DataFrame 运算会同时对齐 index 和 columns。

```python
ret_wide = pd.DataFrame(
    {
        "AAA": [0.01, 0.02],
        "BBB": [-0.02, 0.01],
    },
    index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
)

weight_wide = pd.DataFrame(
    {
        "BBB": [0.4, 0.5],
        "CCC": [0.6, 0.5],
    },
    index=pd.to_datetime(["2024-01-03", "2024-01-04"]),
)

product = ret_wide * weight_wide

print(product)
```

只有日期和资产都匹配的位置才会有数值。这个例子里，只有 `2024-01-03` 的 `BBB` 同时存在。

如果你的目标是组合收益，通常要先决定：

- 日期取交集还是并集？
- 资产取交集还是按目标资产池补 0？
- 缺失收益和缺失权重分别如何处理？

## 写断言检查 index

最简单的调试工具是断言 index 完全一致。

```python
def assert_same_index(left, right, left_name="left", right_name="right"):
    if not left.index.equals(right.index):
        missing_left = right.index.difference(left.index)
        missing_right = left.index.difference(right.index)
        raise ValueError(
            f"{left_name} and {right_name} index mismatch; "
            f"missing_in_left={list(missing_left[:5])}, "
            f"missing_in_right={list(missing_right[:5])}"
        )
```

使用：

```python
assert_same_index(returns, weights_aligned, "returns", "weights")
```

如果函数抛错，错误信息会展示两边差异的一部分。

## 检查 columns 顺序

模型特征尤其要检查列顺序。

```python
feature_columns = ["momentum", "value", "volatility"]

X_train = pd.DataFrame(
    {
        "momentum": [0.1, 0.2, 0.3],
        "value": [1.0, 0.5, -0.2],
        "volatility": [0.2, 0.3, 0.4],
    },
    index=["s1", "s2", "s3"],
)

X_predict = X_train[["volatility", "momentum", "value"]]

print(X_predict.columns)
```

修正方式：

```python
X_predict_aligned = X_predict.reindex(columns=feature_columns)

print(X_predict_aligned.columns)
```

如果进入 NumPy 或模型预测前不固定列顺序，模型可能把 `volatility` 当成 `momentum` 使用。

## sklearn 的 X 和 y 不自动按 index 对齐

即使 `X` 和 `y` 都是 pandas 对象，很多 sklearn 逻辑仍然按行位置配对。

```python
X = pd.DataFrame({
    "feature": [10.0, 20.0, 30.0],
}, index=["a", "b", "c"])

y = pd.Series([1, 0, 1], index=["a", "b", "c"], name="target")

y_shuffled = y.loc[["c", "a", "b"]]

print(X.index)
print(y_shuffled.index)
```

长度一样不代表样本对齐。

```python
print(X["feature"].to_numpy())
print(y_shuffled.to_numpy())
```

这会把 `X` 的第 1 行配给 `y_shuffled` 的第 1 个位置。正确做法：

```python
y_aligned = y_shuffled.loc[X.index]

assert X.index.equals(y_aligned.index)
```

训练前应该把这个检查写成习惯。

## 时间序列：特征和标签时点

时间序列对齐不只是 index 相等，还要看信息时点。

```python
close = pd.Series(
    [100.0, 102.0, 101.0, 103.0, 104.0],
    index=pd.to_datetime([
        "2024-01-02",
        "2024-01-03",
        "2024-01-04",
        "2024-01-05",
        "2024-01-08",
    ]),
    name="close",
)

ret = close.pct_change(fill_method=None)

feature = ret.shift(1).rename("return_lag_1d")
label = (close.shift(-1) / close - 1.0).rename("return_fwd_1d")

dataset = pd.concat([feature, label], axis=1).dropna()

print(dataset)
```

这里每一行的语义是：

- `return_lag_1d`：截至前一日已知的收益。
- `return_fwd_1d`：从当前日到下一日的未来收益，作为标签。

两列 index 相同，但含义不同。名字要明确标出 lag / fwd，避免把未来收益误当特征。

## 不同频率数据的 asof 对齐

有些数据不是同频的。例如因子每天有，宏观数据每月发布一次。不能简单 forward fill，必须确认发布时间。

一个简化例子：

```python
daily = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-03", "2024-01-10", "2024-02-05"]),
    "asset": ["AAA", "AAA", "AAA"],
    "factor": [0.2, 0.4, 0.1],
})

macro = pd.DataFrame({
    "release_date": pd.to_datetime(["2024-01-01", "2024-02-01"]),
    "macro_value": [3.1, 3.3],
})

aligned = pd.merge_asof(
    daily.sort_values("date"),
    macro.sort_values("release_date"),
    left_on="date",
    right_on="release_date",
    direction="backward",
)

print(aligned)
```

`direction="backward"` 表示每个日期只能使用当时已经发布的最近宏观数据。对于有发布时间的数据，这是比随手 `ffill` 更明确的写法。

## MultiIndex 面板对齐

长表因子数据常用 `(date, asset)` 作为键。

```python
index = pd.MultiIndex.from_product(
    [pd.to_datetime(["2024-01-02", "2024-01-03"]), ["AAA", "BBB"]],
    names=["date", "asset"],
)

factor = pd.Series([0.1, -0.2, 0.3, 0.4], index=index, name="factor")

label = pd.Series(
    [0.02, -0.01, 0.03, 0.00],
    index=index[[2, 0, 3, 1]],
    name="future_return",
)

panel = pd.concat([factor, label], axis=1)

print(panel)
```

pandas 会按 MultiIndex 对齐，即使 `label` 的顺序被打乱，拼接后仍然按 `(date, asset)` 匹配。

进入 NumPy 前要固定顺序：

```python
panel_sorted = panel.sort_index()

X_np = panel_sorted[["factor"]].to_numpy()
y_np = panel_sorted["future_return"].to_numpy()

print(X_np.shape)
print(y_np.shape)
```

不要分别对 factor 和 label 转 NumPy 后再假设顺序一致。

## 重复 index 是危险信号

很多对齐逻辑默认 index 唯一。重复 index 会让结果难以解释。

```python
duplicate = pd.Series(
    [0.1, 0.2, 0.3],
    index=["AAA", "AAA", "BBB"],
    name="factor",
)

print(duplicate.index.is_unique)
```

如果重复是合法的，应该把缺失的键补上，例如使用 MultiIndex：

```python
duplicate_fixed = pd.Series(
    [0.1, 0.2, 0.3],
    index=pd.MultiIndex.from_tuples(
        [
            ("2024-01-02", "AAA"),
            ("2024-01-03", "AAA"),
            ("2024-01-02", "BBB"),
        ],
        names=["date", "asset"],
    ),
)

print(duplicate_fixed.index.is_unique)
```

如果重复是数据问题，应该在进入计算前报错，而不是让后续对齐隐式处理。

## 调试对齐问题的工具函数

可以准备一个统一检查函数。

```python
def alignment_report(left, right):
    return {
        "left_len": len(left),
        "right_len": len(right),
        "left_index_unique": left.index.is_unique,
        "right_index_unique": right.index.is_unique,
        "index_equal": left.index.equals(right.index),
        "left_only": left.index.difference(right.index).tolist(),
        "right_only": right.index.difference(left.index).tolist(),
    }
```

使用：

```python
report = alignment_report(returns, weights)

print(report)
```

正式代码里，建议在关键边界加断言：

- 训练前：`X.index.equals(y.index)`。
- 预测前：`X.columns.equals(expected_columns)`。
- 合并后：检查样本数是否符合预期。
- 转 NumPy 前：先排序、reindex、断言。

## 常见坑

第一，只检查长度。

`len(X) == len(y)` 不能证明样本对齐。必须检查 index 或键。

第二，过早转 NumPy。

NumPy 没有标签保护。进入 NumPy 前要先用 pandas 对齐好顺序。

第三，随手填充 NaN。

对齐产生的 NaN 是信号，不是噪声。先弄清是资产缺失、日期缺失、样本范围不一致，还是业务上应该填 0。

第四，特征和标签日期相同就以为没有泄露。

同一个 index 可能代表不同信息时点。必须明确预测时点、特征可见时点和标签期间。

第五，忽略重复 index。

重复 index 会让 join、concat、reindex 和 groupby 变得难以解释。能唯一标识样本的键必须明确。

## 实战提示

一个安全的数据对齐流程：

1. 定义样本键：例如 `date`、`asset`、`timestamp`、`id`。
2. 检查键是否唯一。
3. 明确 join 方式：inner、left、outer、asof。
4. 合并后检查行数、缺失值和重复键。
5. 训练前检查 `X.index.equals(y.index)`。
6. 预测前检查列顺序和列名。
7. 转 NumPy 前保存并断言 index / columns。
8. 时间序列中明确 lag / fwd 命名和预测时点。

一个训练数据准备模板：

```python
def make_training_matrix(features, label, feature_columns):
    if not features.index.is_unique:
        raise ValueError("features index is not unique")
    if not label.index.is_unique:
        raise ValueError("label index is not unique")

    aligned = features.join(label.rename("label"), how="inner")
    aligned = aligned.dropna(subset=feature_columns + ["label"])
    aligned = aligned.sort_index()

    X = aligned[feature_columns]
    y = aligned["label"]

    if not X.index.equals(y.index):
        raise ValueError("X and y are not aligned")
    if list(X.columns) != list(feature_columns):
        raise ValueError("feature columns changed")

    return X, y


features = panel_sorted[["factor"]]
label_series = panel_sorted["future_return"]

X_train, y_train = make_training_matrix(
    features,
    label_series,
    ["factor"],
)

print(X_train)
print(y_train)
```

这个模板把对齐、缺失处理、排序、列顺序和断言集中在一个入口，减少后续模型代码里的隐性错位。

## 小结

本节的重点：

- 数据对齐是样本语义问题，不只是长度问题。
- pandas 默认按标签对齐，NumPy 和 sklearn 通常按位置处理。
- 转 NumPy 前要先显式对齐并固定顺序。
- 时间序列要同时检查 index 和信息时点。
- MultiIndex 能明确面板数据的样本键。
- 重复 index 是危险信号，要补全键或提前报错。
- 关键边界要写断言：index、columns、样本数、缺失值。

## 自检问题

1. 为什么 `len(X) == len(y)` 不能证明样本对齐？
2. pandas 和 NumPy 在对齐语义上有什么根本区别？
3. sklearn 训练前为什么要检查 `X.index.equals(y.index)`？
4. 时间序列里，为什么同一个日期 index 仍然可能发生未来信息泄露？
5. 转 NumPy 前应该保存和检查哪些元数据？
