# 29. sklearn：model selection：GridSearchCV、RandomizedSearchCV 与泄露风险

## 核心概念

模型选择不是单纯训练一个模型，而是在多个候选配置中选择一个。候选配置可能包括：

- 模型类型。
- 超参数，例如 `C`、`alpha`、`max_depth`、`min_samples_leaf`。
- 预处理方式。
- 特征集合。
- 评分指标和切分方式。

sklearn 常用工具：

- `GridSearchCV`：枚举参数网格中的所有组合。
- `RandomizedSearchCV`：从参数分布或候选集合中随机采样固定次数。
- `cv_results_`：保存每组参数的交叉验证结果。
- `best_params_`：交叉验证中表现最好的参数。
- `best_estimator_`：用最佳参数在完整训练集上重新 fit 的 estimator。

核心原则：参数搜索只能使用训练集内部的交叉验证；独立测试集应留到最后，只评估一次。

## 准备环境

```python
import numpy as np
import pandas as pd

from scipy.stats import loguniform, randint
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, mean_absolute_error, roc_auc_score
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedKFold,
    TimeSeriesSplit,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
```

本节先用二分类例子讲模型选择，再用回归和时间序列例子说明评分和切分方式。

## 分类数据

```python
X = pd.DataFrame({
    "momentum": [-2.5, -2.1, -1.8, -1.4, -1.1, -0.8, -0.4, -0.1,
                 0.1, 0.4, 0.7, 1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8],
    "volatility": [0.45, 0.42, 0.39, 0.37, 0.34, 0.32, 0.30, 0.28,
                   0.27, 0.25, 0.24, 0.22, 0.21, 0.19, 0.18, 0.17, 0.16, 0.15],
    "liquidity": [7, 8, 9, 10, 11, 12, 13, 14,
                  15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
})

y = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0,
               1, 1, 1, 1, 1, 1, 1, 1, 1], name="target")

print(X.shape)
print(y.value_counts().sort_index())
```

先保留一个最终测试集：

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

print(X_train.shape)
print(X_test.shape)
```

后面的参数搜索只在 `X_train, y_train` 上进行。`X_test, y_test` 留到最后。

## Pipeline 是搜索对象

参数搜索时，应把预处理和模型一起放进 Pipeline。

```python
logit_pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000, solver="liblinear")),
])

print(logit_pipe.get_params().keys())
```

Pipeline 参数使用双下划线命名：

```text
step_name__parameter_name
```

例如：

- `model__C`
- `model__penalty`
- `scale__with_mean`

## GridSearchCV：枚举参数组合

`GridSearchCV` 会枚举参数网格中所有组合。

```python
param_grid = {
    "model__C": [0.1, 1.0, 10.0],
    "model__penalty": ["l1", "l2"],
}

cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

grid = GridSearchCV(
    estimator=logit_pipe,
    param_grid=param_grid,
    scoring="roc_auc",
    cv=cv,
    refit=True,
    return_train_score=True,
)

grid.fit(X_train, y_train)

print(grid.best_params_)
print(grid.best_score_)
print(grid.best_estimator_)
```

`best_score_` 是训练集内部交叉验证的平均分，不是最终测试集分数。

因为 `refit=True`，搜索结束后 sklearn 会用最佳参数在整个训练集上重新 fit 一个 `best_estimator_`。

## 查看 cv_results_

`cv_results_` 可以转成 DataFrame 观察每组参数。

```python
results = pd.DataFrame(grid.cv_results_)

cols = [
    "param_model__C",
    "param_model__penalty",
    "mean_train_score",
    "mean_test_score",
    "std_test_score",
    "rank_test_score",
]

print(results[cols].sort_values("rank_test_score"))
```

`mean_test_score` 中的 test 指的是交叉验证的验证折，不是最终测试集。这个命名容易误解。

如果训练分数明显高于验证分数，可能存在过拟合：

```python
results["train_test_gap"] = results["mean_train_score"] - results["mean_test_score"]

print(results[["param_model__C", "param_model__penalty", "train_test_gap"]])
```

## 最终测试集只评估一次

参数搜索完成后，再用最终测试集评估。

```python
best_model = grid.best_estimator_

test_prob = best_model.predict_proba(X_test)[:, 1]
test_pred = best_model.predict(X_test)

test_auc = roc_auc_score(y_test, test_prob)
test_accuracy = accuracy_score(y_test, test_pred)

print(test_auc)
print(test_accuracy)
```

如果你根据测试集表现继续改网格、改特征、改模型，测试集就参与了模型选择，测试分数会变得偏乐观。

## RandomizedSearchCV：随机搜索

当参数空间很大时，网格搜索会迅速膨胀。`RandomizedSearchCV` 每次随机采样一组参数，固定采样次数 `n_iter`。

```python
forest_pipe = Pipeline([
    ("model", RandomForestClassifier(random_state=42)),
])

param_distributions = {
    "model__n_estimators": randint(20, 80),
    "model__max_depth": [2, 3, 4, None],
    "model__min_samples_leaf": randint(1, 5),
}

random_search = RandomizedSearchCV(
    estimator=forest_pipe,
    param_distributions=param_distributions,
    n_iter=8,
    scoring="roc_auc",
    cv=cv,
    random_state=42,
    refit=True,
)

random_search.fit(X_train, y_train)

print(random_search.best_params_)
print(random_search.best_score_)
```

`random_state` 控制采样可复现。`n_iter` 越大，探索越充分，但计算成本越高。

随机搜索适合：

- 参数很多。
- 不知道哪些参数重要。
- 连续参数范围较大。
- 想先快速探索合理区域。

## 连续参数分布：loguniform

正则化强度这类参数常跨多个数量级，适合用 log-uniform 分布。

```python
random_logit = RandomizedSearchCV(
    estimator=logit_pipe,
    param_distributions={
        "model__C": loguniform(1e-2, 1e2),
        "model__penalty": ["l1", "l2"],
    },
    n_iter=6,
    scoring="roc_auc",
    cv=cv,
    random_state=7,
    refit=True,
)

random_logit.fit(X_train, y_train)

print(random_logit.best_params_)
print(random_logit.best_score_)
```

如果直接在 `[0.01, 100]` 上均匀采样，大部分样本会落在大数区域；`loguniform` 更适合跨数量级搜索。

## 多指标评分

可以同时评估多个指标，但必须指定用哪个指标 refit。

```python
multi_metric_grid = GridSearchCV(
    estimator=logit_pipe,
    param_grid=param_grid,
    scoring={
        "auc": "roc_auc",
        "accuracy": "accuracy",
    },
    refit="auc",
    cv=cv,
)

multi_metric_grid.fit(X_train, y_train)

print(multi_metric_grid.best_params_)
print(multi_metric_grid.best_score_)

multi_results = pd.DataFrame(multi_metric_grid.cv_results_)
print(multi_results[["mean_test_auc", "mean_test_accuracy", "rank_test_auc"]])
```

这里 `refit="auc"` 表示用 AUC 选最佳参数，并用最佳参数重新训练最终 estimator。

## 回归任务的 GridSearchCV

回归任务也可以搜索参数。这里用 Ridge 的 `alpha`。

```python
X_reg = pd.DataFrame({
    "value_score": [-1.5, -1.2, -0.9, -0.6, -0.3, 0.0, 0.2, 0.4,
                    0.7, 0.9, 1.1, 1.4, 1.6, 1.8, 2.0, 2.3],
    "quality_score": [0.2, 0.3, 0.25, 0.35, 0.40, 0.45, 0.50, 0.55,
                      0.60, 0.65, 0.70, 0.78, 0.80, 0.85, 0.90, 0.95],
    "volatility": [0.40, 0.38, 0.36, 0.35, 0.33, 0.31, 0.30, 0.28,
                   0.26, 0.25, 0.23, 0.22, 0.21, 0.20, 0.18, 0.17],
})

y_reg = pd.Series(
    [-0.030, -0.024, -0.020, -0.014, -0.010, -0.004, 0.002, 0.006,
     0.012, 0.017, 0.021, 0.028, 0.032, 0.036, 0.041, 0.047],
    name="future_return",
)

ridge_pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", Ridge()),
])

ridge_grid = GridSearchCV(
    ridge_pipe,
    param_grid={"model__alpha": [0.01, 0.1, 1.0, 10.0]},
    scoring="neg_mean_absolute_error",
    cv=4,
    refit=True,
)

ridge_grid.fit(X_reg, y_reg)

print(ridge_grid.best_params_)
print(-ridge_grid.best_score_)
```

损失类指标在 sklearn 里通常取负号，因为模型选择统一遵循“越大越好”。这里 `-ridge_grid.best_score_` 才是 MAE。

## 时间序列调参

时间序列任务不能用随机 KFold。应使用顺序切分，例如 `TimeSeriesSplit`。

```python
dates = pd.bdate_range("2024-01-02", periods=len(X_reg))
X_reg_ts = X_reg.copy()
X_reg_ts.index = dates
y_reg_ts = y_reg.copy()
y_reg_ts.index = dates

tscv = TimeSeriesSplit(n_splits=4, test_size=2)

ts_grid = GridSearchCV(
    ridge_pipe,
    param_grid={"model__alpha": [0.01, 0.1, 1.0, 10.0]},
    scoring="neg_mean_absolute_error",
    cv=tscv,
)

ts_grid.fit(X_reg_ts, y_reg_ts)

print(ts_grid.best_params_)
print(-ts_grid.best_score_)
```

时间序列调参时，切分策略是模型选择的一部分。随机切分会把未来样本泄露到训练折里。

## 常见泄露边界

最常见的错误是先全量预处理，再搜索：

```python
# 不推荐
# X_scaled = StandardScaler().fit_transform(X_train)
# grid = GridSearchCV(LogisticRegression(), param_grid, cv=cv)
# grid.fit(X_scaled, y_train)
```

这会让验证折的信息进入 scaler 的均值和标准差。

推荐：

```python
safe_grid = GridSearchCV(
    estimator=logit_pipe,
    param_grid=param_grid,
    scoring="roc_auc",
    cv=cv,
)

safe_grid.fit(X_train, y_train)
```

因为 scaler 在 Pipeline 内部，每一折只会在训练折上 fit。

## 外层测试集和内层搜索

如果你需要评估“模型选择流程”的泛化能力，可以把数据分成：

- 外层训练集：用于 GridSearchCV 内部交叉验证和参数选择。
- 外层测试集：只评估最终选择后的模型。

前面已经做了这个流程：

```python
grid.fit(X_train, y_train)
final_score = roc_auc_score(y_test, grid.best_estimator_.predict_proba(X_test)[:, 1])

print(final_score)
```

更严格的做法是嵌套交叉验证：外层 CV 评估流程，内层 CV 选择参数。本节先掌握 holdout 测试集 + 内层搜索的基本结构。

## 常见坑

第一，把 `best_score_` 当成最终测试分数。

`best_score_` 是内层交叉验证分数。它已经被用于选择参数，因此通常比真正外部测试表现更乐观。

第二，在测试集上反复改参数网格。

如果测试集结果影响了你的下一轮模型选择，测试集就不再独立。

第三，忘记把预处理放进 Pipeline。

标准化、编码、缺失值填充、特征选择都应在 Pipeline 内部参与交叉验证。

第四，时间序列任务使用随机 KFold。

时间序列应使用顺序切分，例如 `TimeSeriesSplit`，并根据标签重叠和数据延迟考虑 `gap`。

第五，参数网格过大但样本很少。

搜索组合越多，越容易在验证折上“碰巧”找到高分配置。参数空间应有业务和建模理由。

## 实战提示

运行搜索前，先明确四件事：

```python
print(param_grid)
print(cv)
print("scoring=roc_auc")
print("final test set size:", len(X_test))
```

搜索后保存关键结果：

```python
summary = pd.DataFrame(grid.cv_results_).sort_values("rank_test_score")

print(summary[["params", "mean_test_score", "std_test_score", "rank_test_score"]].head())
print(grid.best_params_)
```

最终评估时，只对独立测试集做一次：

```python
final_prob = grid.best_estimator_.predict_proba(X_test)[:, 1]
final_auc = roc_auc_score(y_test, final_prob)

print(final_auc)
```

如果要复现实验，应记录：

- 参数网格或参数分布。
- `cv` 切分器。
- `scoring`。
- 随机种子。
- 最终测试集定义。
- sklearn 版本。

## 小结

`GridSearchCV` 和 `RandomizedSearchCV` 解决的是参数选择问题：

- Grid search 枚举候选组合，适合小而明确的参数空间。
- Random search 随机采样，适合较大或连续的参数空间。
- `best_score_` 是内层 CV 分数，不是最终测试分数。
- `best_estimator_` 是用最佳参数在完整训练集上 refit 的模型。
- 预处理、特征选择和模型必须放进 Pipeline，避免验证折泄露。
- 时间序列要使用时间顺序切分。

模型选择的关键不是找到一个高分参数，而是建立一个不泄露、可复现、评估含义清楚的选择流程。

## 自检问题

1. `GridSearchCV.best_score_` 和最终测试集分数有什么区别？
2. 为什么参数搜索时要把预处理放进 Pipeline？
3. `GridSearchCV` 和 `RandomizedSearchCV` 适合的场景有什么不同？
4. 为什么时间序列调参不能使用随机 KFold？
5. 多指标搜索时，`refit="auc"` 这类设置是什么意思？
