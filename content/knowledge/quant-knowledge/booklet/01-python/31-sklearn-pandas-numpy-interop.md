# 31. sklearn：与 pandas / numpy 数据形态互操作

## 核心概念

sklearn 的核心输入是二维特征矩阵 `X` 和一维标签 `y`：

```text
X.shape == (n_samples, n_features)
y.shape == (n_samples,)
```

它可以接收 NumPy 数组、pandas DataFrame / Series、SciPy 稀疏矩阵等对象。但要记住：

- sklearn 主要按“位置”处理样本，不会自动按 pandas index 对齐 `X` 和 `y`。
- DataFrame 的列名会被部分 estimator 记录为 `feature_names_in_`。
- Pipeline 和 transformer 中间步骤经常把 DataFrame 转成 NumPy 数组或稀疏矩阵。
- 如果需要保留列名，要使用 `get_feature_names_out()` 或 `set_output(transform="pandas")`。
- 预测时列名和列顺序应与训练时一致。

本节重点讲这些数据形态边界，避免模型训练时发生标签错位、列错位或形状错误。

## 准备环境

```python
import numpy as np
import pandas as pd
from scipy import sparse

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
```

构造一个小型分类数据集：

```python
X = pd.DataFrame({
    "momentum": [-1.2, -0.8, -0.4, 0.1, 0.5, 0.9, 1.3, 1.8],
    "volatility": [0.40, 0.35, 0.32, 0.28, 0.24, 0.21, 0.18, 0.15],
    "sector": ["tech", "finance", "tech", "energy", "finance", "tech", "energy", "health"],
})

y = pd.Series([0, 0, 0, 0, 1, 1, 1, 1], name="target")

print(X)
print(y)
```

## X 必须是二维

sklearn 要求 `X` 是二维。即使只有一个特征，也要保留二维形状。

```python
one_feature_series = X["momentum"]

print(one_feature_series.shape)
```

`Series` 是一维，直接传给 estimator 通常会报错。正确写法是传 DataFrame：

```python
one_feature_frame = X[["momentum"]]

print(one_feature_frame.shape)
```

NumPy 数组也一样：

```python
arr_1d = X["momentum"].to_numpy()
arr_2d = arr_1d.reshape(-1, 1)

print(arr_1d.shape)
print(arr_2d.shape)
```

`reshape(-1, 1)` 表示“多行一列”。

## y 通常是一维

标签 `y` 通常是一维。

```python
print(y.shape)
print(y.to_numpy().shape)
```

不要把单目标分类或回归标签传成 `(n_samples, 1)` 的二维 DataFrame，除非你明确在做多输出任务。

```python
y_frame = y.to_frame()

print(y_frame.shape)
```

很多 estimator 会接受二维 `y`，但可能触发警告或改变任务语义。普通监督学习里使用 Series 或一维数组更清楚。

## pandas index 不会自动对齐

pandas 的很多运算会按 index 对齐，但 sklearn 不会自动对齐 `X` 和 `y`。它按样本位置配对。

```python
X_bad = X.copy()
y_bad = y.sample(frac=1.0, random_state=42)

print(X_bad.index.to_list())
print(y_bad.index.to_list())
```

`X_bad` 和 `y_bad` 的 index 不一致，但长度相同。sklearn 会把 `X_bad` 第 1 行配 `y_bad` 第 1 个位置，这通常是标签错位。

训练前应显式检查：

```python
assert X.index.equals(y.index)
```

如果 y 被打乱了，应该先按 index 对齐：

```python
y_aligned = y_bad.loc[X_bad.index]

assert X_bad.index.equals(y_aligned.index)
```

## train_test_split 会保留 pandas 类型

`train_test_split` 会同步切分 `X` 和 `y`，并保留 DataFrame / Series 类型。

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

print(type(X_train))
print(type(y_train))
print(X_train.index)
print(y_train.index)
```

切分后仍应检查：

```python
assert X_train.index.equals(y_train.index)
assert X_test.index.equals(y_test.index)
```

这对后续把预测结果重新包回 pandas 很有用。

## DataFrame 列名和 feature_names_in_

如果 estimator 用 DataFrame 拟合，很多 sklearn 对象会记录特征名。

```python
model = LogisticRegression(max_iter=1000)
model.fit(X[["momentum", "volatility"]], y)

print(model.feature_names_in_)
print(model.coef_)
```

预测时传入的列名和顺序应与训练时一致。

```python
try:
    model.predict(X[["volatility", "momentum"]])
except ValueError as exc:
    print(type(exc).__name__)
```

在 sklearn 1.5 中，列顺序变化会报错，因为特征名不再匹配训练时的顺序。生产预测前应固定特征列顺序：

```python
feature_columns = ["momentum", "volatility"]

pred = model.predict(X[feature_columns])

print(pred)
```

## NumPy 数组没有列名保护

如果把 DataFrame 转成 NumPy 数组，列名保护就消失了。

```python
X_np = X[feature_columns].to_numpy()

model_np = LogisticRegression(max_iter=1000)
model_np.fit(X_np, y.to_numpy())

pred_np = model_np.predict(X_np[:, ::-1])

print(pred_np)
```

这段代码可以运行，但 `X_np[:, ::-1]` 把列顺序反了，模型并不知道。这是使用 NumPy 数组时最常见的风险之一。

如果需要用 NumPy，建议保留一份特征列清单：

```python
feature_columns = list(X[["momentum", "volatility"]].columns)

print(feature_columns)
```

## transformer 默认可能返回 NumPy

许多 transformer 即使输入 DataFrame，也默认输出 NumPy 数组。

```python
scaler = StandardScaler()

scaled = scaler.fit_transform(X[["momentum", "volatility"]])

print(type(scaled))
print(scaled.shape)
```

需要列名时，可以用 `set_output(transform="pandas")`：

```python
scaler_pd = StandardScaler().set_output(transform="pandas")

scaled_df = scaler_pd.fit_transform(X[["momentum", "volatility"]])

print(type(scaled_df))
print(scaled_df)
```

这对调试很有帮助。

## ColumnTransformer 的输出列名

混合数值和类别特征时，常用 `ColumnTransformer`。

```python
preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["momentum", "volatility"]),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["sector"]),
    ],
)

prepared = preprocess.fit_transform(X)

print(type(prepared))
print(prepared.shape)
print(preprocess.get_feature_names_out())
```

默认输出通常是 NumPy 数组，但可以通过 `get_feature_names_out()` 拿到转换后的列名。

手动包回 DataFrame：

```python
prepared_df = pd.DataFrame(
    prepared,
    index=X.index,
    columns=preprocess.get_feature_names_out(),
)

print(prepared_df)
```

也可以让 transformer 输出 pandas：

```python
preprocess_pd = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["momentum", "volatility"]),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["sector"]),
    ],
).set_output(transform="pandas")

prepared_df_2 = preprocess_pd.fit_transform(X)

print(type(prepared_df_2))
print(prepared_df_2)
```

## 稀疏输出

`OneHotEncoder` 默认可能输出稀疏矩阵。

```python
encoder_sparse = OneHotEncoder(handle_unknown="ignore")

sector_sparse = encoder_sparse.fit_transform(X[["sector"]])

print(type(sector_sparse))
print(sector_sparse.shape)
print(sector_sparse.nnz)
```

稀疏矩阵没有 pandas index 和 columns。需要列名时，使用：

```python
sector_names = encoder_sparse.get_feature_names_out(["sector"])

print(sector_names)
```

如果数据规模小、需要调试，可以设置 `sparse_output=False`。如果类别很多，稀疏输出通常更省内存。

## Pipeline 预测结果包回 pandas

Pipeline 预测返回 NumPy 数组。可以用测试集 index 包回 Series 或 DataFrame。

```python
pipe = Pipeline([
    ("preprocess", preprocess),
    ("model", LogisticRegression(max_iter=1000)),
])

pipe.fit(X_train, y_train)

pred = pipe.predict(X_test)
prob = pipe.predict_proba(X_test)

pred_s = pd.Series(pred, index=X_test.index, name="prediction")
prob_df = pd.DataFrame(
    prob,
    index=X_test.index,
    columns=[f"prob_{cls}" for cls in pipe.named_steps["model"].classes_],
)

print(pred_s)
print(prob_df)
```

这样预测结果可以和原始样本重新 join。

```python
scored = X_test.join(pred_s).join(prob_df)

print(scored)
```

## sample_weight 也是按位置匹配

很多 estimator 支持 `sample_weight`。它也必须和训练样本按位置一致。

```python
sample_weight = pd.Series(
    np.where(y_train == 1, 2.0, 1.0),
    index=y_train.index,
    name="sample_weight",
)

weighted_model = LogisticRegression(max_iter=1000)
weighted_model.fit(
    X_train[["momentum", "volatility"]],
    y_train,
    sample_weight=sample_weight,
)

print(weighted_model.coef_)
```

如果 sample weight 被打乱但长度一样，sklearn 不会按 index 自动对齐。训练前应检查：

```python
assert X_train.index.equals(sample_weight.index)
```

Pipeline 中给某一步传 sample weight，要用 `step__sample_weight`：

```python
pipe.fit(
    X_train,
    y_train,
    model__sample_weight=sample_weight,
)
```

## 常见坑

第一，把一维 Series 当作 `X`。

```python
# 不推荐
# model.fit(X["momentum"], y)

# 推荐
model.fit(X[["momentum"]], y)
```

第二，认为 sklearn 会按 pandas index 自动对齐 `X` 和 `y`。

sklearn 按位置配对样本。训练前要检查 `X.index.equals(y.index)`。

第三，训练和预测列顺序不一致。

DataFrame 可能报错，NumPy 数组可能静默错误。生产预测前固定 `feature_columns`。

第四，transform 后丢失列名却继续解释系数或 importance。

使用 `get_feature_names_out()` 或 `set_output(transform="pandas")`。

第五，把稀疏矩阵随手转 dense。

one-hot 后的矩阵可能很大。只有调试小样本时才适合 `.toarray()`。

## 实战提示

训练前做这些检查：

```python
assert isinstance(X, pd.DataFrame)
assert isinstance(y, pd.Series)
assert X.index.equals(y.index)
assert X.columns.is_unique
assert y.notna().all()
```

固定特征列：

```python
feature_columns = ["momentum", "volatility", "sector"]

X_model = X[feature_columns]
```

预测前检查列：

```python
assert list(X_model.columns) == feature_columns
```

转换后检查形状：

```python
prepared = preprocess.fit_transform(X_model)

assert prepared.shape[0] == len(X_model)
```

输出结果时恢复 index：

```python
pred = pipe.predict(X_test)
pred = pd.Series(pred, index=X_test.index, name="prediction")
```

这些检查能防止多数形状错位、标签错位和列错位问题。

## 小结

sklearn 与 pandas / NumPy 互操作时，最重要的是明确边界：

- pandas 负责标签、列名、index 语义。
- NumPy 和稀疏矩阵负责数值矩阵。
- sklearn estimator 主要按位置处理样本。
- DataFrame 特征名能提供一定保护，但不要依赖它替代特征列管理。
- Pipeline 中间步骤可能丢失 pandas 标签，需要用 `get_feature_names_out()` 或 `set_output` 恢复。

可靠的建模代码通常会固定 `feature_columns`，在训练和预测前检查 index、列名和 shape。

## 自检问题

1. 为什么只有一个特征时也要传二维 `X`？
2. sklearn 会不会自动按 pandas index 对齐 `X` 和 `y`？
3. 为什么用 NumPy 数组训练时更容易发生列顺序静默错误？
4. `get_feature_names_out()` 和 `set_output(transform="pandas")` 分别解决什么问题？
5. `sample_weight` 为什么也要检查 index 和训练样本一致？
