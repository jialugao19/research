# 27. sklearn：preprocessing：StandardScaler、OneHotEncoder 与 ColumnTransformer

## 核心概念

机器学习模型通常要求输入是数值矩阵，但原始数据里经常同时有：

- 数值列：收益率、波动率、成交量、市值等。
- 类别列：行业、国家、交易所、风格标签等。
- 不同量纲：收益率是小数，成交量可能是百万或亿。

sklearn 的 preprocessing 工具负责把原始特征转换成模型可用的数值特征。

本节重点讲三个常用对象：

- `StandardScaler`：对数值列做标准化。
- `OneHotEncoder`：把类别列转成 one-hot 数值列。
- `ColumnTransformer`：对不同列应用不同预处理，再拼成一个特征矩阵。

核心原则：预处理器也是 estimator，必须只在训练数据上 `fit`，再对训练集和测试集分别 `transform`。交叉验证和调参时，应把预处理放进 Pipeline。

## 准备数据

```python
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
```

构造一个混合类型数据集：

```python
X = pd.DataFrame({
    "return_5d": [-0.04, -0.02, -0.01, 0.00, 0.01, 0.03, 0.04, 0.06],
    "vol_20d": [0.35, 0.30, 0.28, 0.25, 0.22, 0.20, 0.18, 0.16],
    "market_cap": [80, 120, 90, 150, 200, 240, 210, 260],
    "sector": ["tech", "finance", "tech", "energy", "finance", "tech", "energy", "health"],
    "country": ["US", "US", "CN", "US", "CN", "US", "CN", "US"],
})

y = pd.Series([0, 0, 0, 0, 1, 1, 1, 1], name="target")

print(X)
print(X.dtypes)
```

按列类型拆分：

```python
numeric_features = ["return_5d", "vol_20d", "market_cap"]
categorical_features = ["sector", "country"]
```

## StandardScaler：数值标准化

`StandardScaler` 对每列做：

```text
z = (x - mean) / std
```

```python
scaler = StandardScaler()

X_num = X[numeric_features]
X_num_scaled = scaler.fit_transform(X_num)

print(X_num_scaled)
print(scaler.mean_)
print(scaler.scale_)
```

`mean_` 和 `scale_` 是在 `fit` 阶段从数据学到的属性。

标准化后，每列大致均值为 0、标准差为 1：

```python
print(X_num_scaled.mean(axis=0))
print(X_num_scaled.std(axis=0))
```

这里的标准差是 NumPy 默认的总体标准差，和 `StandardScaler` 的定义一致。

## 训练集 fit，测试集 transform

正确流程是先切分，再 fit scaler。

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

scaler = StandardScaler()
scaler.fit(X_train[numeric_features])

X_train_num_scaled = scaler.transform(X_train[numeric_features])
X_test_num_scaled = scaler.transform(X_test[numeric_features])

print(X_train_num_scaled.mean(axis=0))
print(X_test_num_scaled.mean(axis=0))
```

测试集转换后的均值不一定是 0，因为 scaler 的均值和标准差来自训练集。这是正确的。

错误流程是在全数据上 `fit_transform` 后再切分，这会让测试集信息进入预处理参数。

## OneHotEncoder：类别编码

模型不能直接处理字符串类别。`OneHotEncoder` 会把类别列转成 0/1 指示列。

```python
encoder = OneHotEncoder(sparse_output=False)

X_cat = X[categorical_features]
X_cat_encoded = encoder.fit_transform(X_cat)

print(X_cat_encoded)
print(encoder.categories_)
print(encoder.get_feature_names_out(categorical_features))
```

例如 `sector=tech` 会被编码成对应的 one-hot 列为 1，其他 sector 列为 0。

`sparse_output=False` 表示输出普通 NumPy 数组，方便小样本查看。真实大规模高基数类别特征通常更适合稀疏输出。

## handle_unknown：处理新类别

训练时没见过的类别，在测试或线上数据里可能出现。

默认情况下，`OneHotEncoder` 遇到未知类别会报错。更稳妥的生产设置常用 `handle_unknown="ignore"`：

```python
train_cat = pd.DataFrame({
    "sector": ["tech", "finance", "energy"],
    "country": ["US", "CN", "US"],
})

test_cat = pd.DataFrame({
    "sector": ["health", "tech"],
    "country": ["US", "JP"],
})

safe_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
safe_encoder.fit(train_cat)

encoded_test = safe_encoder.transform(test_cat)

print(safe_encoder.get_feature_names_out())
print(encoded_test)
```

未知类别对应的已知类别列都会是 0。这个行为不代表模型理解了新类别，只是避免预测时报错。

## drop：避免完全共线

One-hot 编码后，同一个类别特征的所有 dummy 列相加等于 1。在线性模型里，有时会用 `drop="first"` 去掉每组的第一列。

```python
drop_encoder = OneHotEncoder(drop="first", sparse_output=False)
drop_encoded = drop_encoder.fit_transform(X_cat)

print(drop_encoder.get_feature_names_out(categorical_features))
print(drop_encoded.shape)
```

是否要 drop 取决于模型和解释需求。树模型通常不需要；带截距的线性模型为了避免完全共线，常见做法是 drop 一列或使用正则化。

## ColumnTransformer：不同列不同处理

`ColumnTransformer` 可以把不同列送到不同 transformer。

```python
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
    ],
)

X_prepared = preprocessor.fit_transform(X)

print(type(X_prepared))
print(X_prepared.shape)
print(preprocessor.get_feature_names_out())
```

输出列包括：

- 标准化后的数值列。
- one-hot 后的类别列。

默认 `get_feature_names_out()` 会给列名加上 transformer 前缀，例如 `num__return_5d`、`cat__sector_tech`。

## set_output：输出 pandas DataFrame

sklearn 1.5 支持让很多 transformer 输出 pandas。

```python
preprocessor_pd = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
    ],
)

preprocessor_pd.set_output(transform="pandas")

X_prepared_df = preprocessor_pd.fit_transform(X)

print(type(X_prepared_df))
print(X_prepared_df)
```

这对调试很有用，因为列名会被保留下来。不过生产流程中仍要注意后续模型是否需要 NumPy、pandas 或稀疏矩阵。

## remainder：保留未指定列

默认情况下，`ColumnTransformer` 会丢弃没有列在任何 transformer 中的列。如果想保留它们，可以设置 `remainder="passthrough"`。

```python
preprocessor_remainder = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["return_5d", "vol_20d"]),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["sector"]),
    ],
    remainder="passthrough",
)

X_remainder = preprocessor_remainder.fit_transform(X)

print(X_remainder.shape)
print(preprocessor_remainder.get_feature_names_out())
```

`remainder="passthrough"` 方便保留少量无需转换的列，但也容易不小心把不该进模型的列带进去。生产代码里最好显式列出特征列。

## make_column_selector：按 dtype 选择列

如果列很多，可以按 dtype 自动选择。

```python
auto_preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), make_column_selector(dtype_include=np.number)),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), make_column_selector(dtype_include=object)),
    ],
)

auto_features = auto_preprocessor.fit_transform(X)

print(auto_features.shape)
print(auto_preprocessor.get_feature_names_out())
```

自动选择很方便，但也要检查列是否符合预期。比如数值型 ID、日期编码、标签泄露列可能被自动选进去。

## 放进 Pipeline

预处理和模型应该放进同一个 Pipeline。

```python
model_pipe = Pipeline([
    ("preprocess", ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
        ],
    )),
    ("model", LogisticRegression(max_iter=1000)),
])

model_pipe.fit(X_train, y_train)

pred = model_pipe.predict(X_test)
prob = model_pipe.predict_proba(X_test)

print(pred)
print(prob)
print(model_pipe.score(X_test, y_test))
```

调用 `model_pipe.fit` 时，`preprocess` 只在训练集上 fit。调用 `predict` 时，测试集只经过已经 fit 好的预处理器做 transform。

## 交叉验证中的预处理

交叉验证时也应把预处理放进 Pipeline。

```python
cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)

scores = cross_val_score(
    model_pipe,
    X,
    y,
    cv=cv,
    scoring="accuracy",
)

print(scores)
print(scores.mean())
```

每一折都会重新 fit 一个干净的 Pipeline，预处理参数只来自当前训练折。

## sparse_output 和稀疏矩阵

`OneHotEncoder` 默认 `sparse_output=True`，适合高基数类别。

```python
sparse_encoder = OneHotEncoder(handle_unknown="ignore")
sparse_encoded = sparse_encoder.fit_transform(X_cat)

print(type(sparse_encoded))
print(sparse_encoded.shape)
print(sparse_encoded.nnz)
```

如果 `ColumnTransformer` 中有稀疏输出，它可能返回稀疏矩阵，也可能因为稀疏比例不够低而返回 dense 数组。由参数 `sparse_threshold` 控制。

```python
sparse_preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ],
)

sparse_like = sparse_preprocessor.fit_transform(X)

print(type(sparse_like))
print(sparse_preprocessor.sparse_output_)
```

小数据上 dense 和 sparse 的区别不大；大规模类别特征时，输出格式会影响内存和模型选择。

## 常见坑

第一，在全数据上 fit 预处理器。

```python
# 不推荐
# X_prepared = preprocessor.fit_transform(X)
# cross_val_score(model, X_prepared, y, cv=cv)
```

这会把验证折的信息泄露给预处理器。应使用 Pipeline。

第二，测试集出现新类别时报错。

```python
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
```

如果线上类别可能变化，通常要设置 `handle_unknown="ignore"`，并监控新类别比例。

第三，忘记 StandardScaler 不适合直接处理类别列。

类别列应先编码；数值列和类别列要分开处理。

第四，自动选择列时把标签或 ID 带入特征。

`make_column_selector` 很方便，但不能代替特征审核。

第五，假设 transform 后一定保留 pandas 标签。

默认输出经常是 NumPy 数组或稀疏矩阵。需要列名时，使用 `get_feature_names_out()` 或 `set_output(transform="pandas")`。

## 实战提示

训练前可以检查列集合：

```python
assert set(numeric_features).isdisjoint(categorical_features)
assert set(numeric_features + categorical_features).issubset(X.columns)
assert y.notna().all()
```

拟合后检查输出形状和列名：

```python
model_pipe.fit(X_train, y_train)

preprocess = model_pipe.named_steps["preprocess"]
feature_names = preprocess.get_feature_names_out()

print(feature_names)
print(len(feature_names))
```

如果要调试某一行的处理结果：

```python
one_row_prepared = preprocess.transform(X_test.iloc[[0]])

print(one_row_prepared)
```

把预处理放进 Pipeline，是防止训练/测试处理不一致和预处理泄露的默认做法。

## 小结

sklearn preprocessing 的基本套路是：

- 数值列用 `StandardScaler` 等数值 transformer。
- 类别列用 `OneHotEncoder` 等编码器。
- 多种列类型用 `ColumnTransformer` 统一组织。
- 预处理和模型放进 Pipeline。
- 交叉验证时对 Pipeline 做 `cross_val_score`，不要先全量预处理再交叉验证。

掌握这套结构后，后续加入缺失值处理、文本特征、日期特征和模型选择都会更稳。

## 自检问题

1. `StandardScaler` 的 `mean_` 和 `scale_` 是什么时候学到的？
2. 为什么测试集只能 `transform`，不能重新 `fit_transform`？
3. `OneHotEncoder(handle_unknown="ignore")` 遇到新类别会怎么处理？
4. `ColumnTransformer` 的作用是什么？
5. 为什么预处理步骤应该放进 Pipeline 再做交叉验证？
