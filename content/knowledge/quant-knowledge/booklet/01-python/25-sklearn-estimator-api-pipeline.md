# sklearn：estimator API：fit / predict / transform 与 Pipeline 基础

## 核心概念

scikit-learn 的核心设计是统一的 estimator API。无论是模型、预处理器、降维器还是 Pipeline，基本都遵循同一套接口：

- `fit(X, y=None)`：从数据中学习参数。
- `transform(X)`：把输入特征转换成新的特征。
- `fit_transform(X, y=None)`：先 `fit`，再 `transform`。
- `predict(X)`：对样本做预测。
- `predict_proba(X)`：输出类别概率，只有部分分类器支持。
- `score(X, y)`：用默认指标评估模型。

常见对象可以分成三类：

- transformer：有 `fit` 和 `transform`，例如 `StandardScaler`。
- predictor：有 `fit` 和 `predict`，例如 `LogisticRegression`。
- pipeline：把多个步骤串起来，前面通常是 transformer，最后通常是 predictor。

理解这套接口，比记住单个模型的参数更重要。

## 准备数据

```python
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
```

构造一个很小的二分类数据集。每行代表一个样本，每列代表一个特征。

```python
X = pd.DataFrame({
    "momentum": [-1.2, -0.8, -0.5, -0.1, 0.2, 0.5, 0.9, 1.3],
    "volatility": [0.40, 0.35, 0.33, 0.30, 0.25, 0.20, 0.18, 0.15],
    "size": [1.0, 1.2, 1.1, 1.5, 1.7, 2.0, 2.2, 2.4],
})

y = pd.Series([0, 0, 0, 0, 1, 1, 1, 1], name="next_up")

print(X)
print(y)
```

在 sklearn 中，`X` 通常是二维，形状是 `(n_samples, n_features)`；`y` 通常是一维，长度是 `n_samples`。

```python
print(X.shape)
print(y.shape)

assert X.ndim == 2
assert y.ndim == 1
assert len(X) == len(y)
```

## estimator 的参数和学到的属性

创建 estimator 时传入的是“构造参数”。

```python
scaler = StandardScaler(with_mean=True, with_std=True)

print(scaler)
print(scaler.get_params())
```

此时它还没有见过数据，因此没有学到均值和标准差。

```python
try:
    scaler.transform(X)
except NotFittedError as exc:
    print(type(exc).__name__)
```

调用 `fit` 后，scaler 会学到训练数据的均值和尺度。这些学到的属性通常以 `_` 结尾。

```python
returned = scaler.fit(X)

print(returned is scaler)
print(scaler.mean_)
print(scaler.scale_)
print(scaler.feature_names_in_)
```

sklearn 的一个重要约定是：

- 构造参数没有下划线，例如 `with_mean`、`C`、`max_iter`。
- `fit` 后学到的属性有下划线，例如 `mean_`、`scale_`、`coef_`、`classes_`。

## transform：转换特征

已经 fit 过的 transformer 可以调用 `transform`。

```python
X_scaled = scaler.transform(X)

print(type(X_scaled))
print(X_scaled.shape)
print(X_scaled.mean(axis=0))
print(X_scaled.std(axis=0))
```

`StandardScaler` 默认返回 NumPy 数组，不会自动保留 pandas 的 index 和 columns。

如果需要恢复标签，可以手动包回 DataFrame：

```python
X_scaled_df = pd.DataFrame(
    X_scaled,
    index=X.index,
    columns=X.columns,
)

print(X_scaled_df)
```

更细的 pandas 互操作会在后续 sklearn 小节展开。

## fit_transform

很多 transformer 都支持 `fit_transform`。

```python
scaler_2 = StandardScaler()
X_scaled_2 = scaler_2.fit_transform(X)

print(np.allclose(X_scaled, X_scaled_2))
```

`fit_transform` 表示先从 `X` 学习参数，再把同一个 `X` 转换。它常用于训练阶段。

预测阶段或测试阶段不能重新 `fit_transform`，否则会用新数据重新学习预处理参数，造成评估口径错误，甚至信息泄露。更稳妥的做法是让 Pipeline 管理这件事。

## predictor：fit 和 predict

分类模型通常是 predictor。

```python
model = LogisticRegression(max_iter=1000)

model.fit(X_scaled, y)

pred = model.predict(X_scaled)
prob = model.predict_proba(X_scaled)

print(pred)
print(prob)
print(model.classes_)
print(model.coef_)
print(model.intercept_)
```

`predict` 输出类别标签。`predict_proba` 输出每个类别的概率，列顺序由 `model.classes_` 决定。

```python
prob_df = pd.DataFrame(
    prob,
    columns=[f"prob_class_{cls}" for cls in model.classes_],
    index=X.index,
)

print(prob_df)
```

不是所有模型都有 `predict_proba`。例如有些模型只有 `decision_function` 或只支持 `predict`。写通用代码时要先确认接口存在。

## score：默认评估指标

很多 predictor 有 `score` 方法。

```python
training_score = model.score(X_scaled, y)

print(training_score)
```

对分类器，默认通常是 accuracy；对回归器，默认通常是 R-squared。

不要过度依赖 `score` 的默认含义。真实项目里应明确使用任务对应的指标，例如 AUC、log loss、MAE、RMSE、RankIC 等。指标会在监督学习小节展开。

## Pipeline：把步骤串起来

手动写法是：

```python
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(max_iter=1000)
model.fit(X_scaled, y)
```

Pipeline 把这两步组织成一个 estimator：

```python
pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])

pipe.fit(X, y)

pipe_pred = pipe.predict(X)
pipe_prob = pipe.predict_proba(X)

print(pipe_pred)
print(pipe_prob)
```

Pipeline 本身也有 `fit`、`predict`、`score` 等方法。调用 `pipe.fit(X, y)` 时：

1. `scale.fit_transform(X, y)` 先运行。
2. 转换后的特征传给 `model.fit(...)`。

调用 `pipe.predict(X)` 时：

1. `scale.transform(X)` 先运行。
2. 转换后的特征传给 `model.predict(...)`。

这能避免训练阶段和预测阶段的预处理逻辑不一致。

## named_steps：访问内部步骤

Pipeline 拟合后，可以通过 `named_steps` 访问内部对象。

```python
fitted_scaler = pipe.named_steps["scale"]
fitted_model = pipe.named_steps["model"]

print(fitted_scaler.mean_)
print(fitted_model.coef_)
```

注意，`pipe.named_steps["model"]` 是已经 fit 过的模型。不要把它和创建 Pipeline 前的原始对象混淆。

## get_params 和 set_params

sklearn estimator 都支持 `get_params` 和 `set_params`。

```python
params = pipe.get_params()

print(params["model__C"])
print(params["model__max_iter"])
```

Pipeline 中的参数用双下划线连接：

```text
step_name__parameter_name
```

例如修改逻辑回归的正则强度：

```python
pipe_small_c = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])

pipe_small_c.set_params(model__C=0.5)
pipe_small_c.fit(X, y)

print(pipe_small_c.get_params()["model__C"])
print(pipe_small_c.named_steps["model"].coef_)
```

这套命名规则是后续 `GridSearchCV` 做参数搜索的基础。

## make_pipeline：自动命名

`make_pipeline` 可以自动生成步骤名称。

```python
auto_pipe = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=1000),
)

auto_pipe.fit(X, y)

print(auto_pipe.named_steps.keys())
print(auto_pipe.predict(X))
```

自动名称通常来自类名的小写形式，例如 `standardscaler`、`logisticregression`。

如果后续要手写参数网格，显式命名通常更清楚；如果只是快速实验，`make_pipeline` 很方便。

## Pipeline 也可以只做特征转换

如果最后一步也是 transformer，Pipeline 会提供 `transform`。

```python
feature_pipe = Pipeline([
    ("scale", StandardScaler()),
])

features = feature_pipe.fit_transform(X)

print(features.shape)
print(feature_pipe.transform(X).shape)
```

这类 Pipeline 可以作为更大 Pipeline 的一部分，也可以用于统一管理特征处理流程。

## clone：复制未拟合配置

`clone` 会复制 estimator 的构造参数，但不会复制 fit 后学到的属性。

```python
fresh_pipe = clone(pipe)

print(fresh_pipe.get_params()["model__max_iter"])
print(hasattr(fresh_pipe.named_steps["model"], "coef_"))
```

这对交叉验证很重要。每个 fold 都应该从一个干净的、未拟合的 estimator 开始，而不是复用已经学过数据的对象。

## 常见坑

第一，在 `fit` 前调用 `transform` 或 `predict`。

```python
unfitted_model = LogisticRegression()

try:
    unfitted_model.predict(X)
except NotFittedError as exc:
    print(type(exc).__name__)
```

第二，混淆构造参数和学到的属性。

```python
print(pipe.named_steps["model"].C)
print(pipe.named_steps["model"].coef_)
```

`C` 是创建模型时的超参数，`coef_` 是 `fit` 之后从数据学到的系数。

第三，测试阶段重新 `fit_transform`。

```python
# 不推荐
# X_test_scaled = StandardScaler().fit_transform(X_test)
```

测试数据应该使用训练阶段学到的 scaler 参数做 `transform`。Pipeline 会在训练和预测之间复用同一个 fitted scaler。

第四，忘记 sklearn 默认不总是保留 pandas 标签。

很多 transformer 返回 NumPy 数组。需要标签时，自己保存 index 和 columns，或使用 sklearn 的 pandas 输出设置。更详细的数据形态互操作后续单独讲。

第五，修改已拟合模型参数后不重新 fit。

```python
pipe.set_params(model__C=2.0)
```

修改超参数后，应重新 `fit`。否则对象里可能同时存在旧数据学到的属性和新的超参数设置，语义会变得混乱。

## 实战提示

训练一个 sklearn 流水线前，可以做基本检查：

```python
assert X.ndim == 2
assert y.ndim == 1
assert len(X) == len(y)
assert X.columns.is_unique
assert y.notna().all()
```

拟合后检查：

```python
pipe.fit(X, y)

assert hasattr(pipe.named_steps["scale"], "mean_")
assert hasattr(pipe.named_steps["model"], "classes_")
assert len(pipe.predict(X)) == len(X)
```

实际项目中，推荐尽早把预处理和模型放进 Pipeline。这样后续做 train/test split、交叉验证、参数搜索时，流程更不容易泄露或错位。

## 小结

sklearn 的统一 API 可以概括为：

- transformer：`fit` 学习转换规则，`transform` 应用转换。
- predictor：`fit` 学习模型，`predict` 输出预测。
- Pipeline：把多个 estimator 串成一个 estimator。
- 构造参数没有下划线，fit 后属性通常有下划线。
- Pipeline 参数使用 `step__param` 命名。

后续的交叉验证、预处理、模型选择和解释，都建立在这套 estimator API 之上。

## 自检问题

1. `fit`、`transform`、`predict` 分别对应什么动作？
2. 为什么 sklearn 学到的属性通常以 `_` 结尾？
3. Pipeline 在 `fit` 和 `predict` 时分别如何调用内部步骤？
4. `model__C` 这种双下划线参数名表示什么？
5. 为什么测试阶段不应该重新 `fit_transform` 一个 scaler？
