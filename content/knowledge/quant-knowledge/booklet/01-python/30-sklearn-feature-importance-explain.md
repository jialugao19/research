# 30. sklearn：feature importance、permutation importance 与模型解释

## 核心概念

模型解释的目标是回答：

- 哪些特征对模型预测更重要？
- 某个特征的方向是正向还是负向？
- 模型依赖的是稳定信号，还是数据泄露、ID、噪声或偶然相关？

sklearn 中常见的解释入口包括：

- 线性模型的 `coef_`：系数大小和符号。
- 树模型的 `feature_importances_`：基于树切分带来的 impurity 减少。
- `permutation_importance`：在验证集或测试集上打乱某个特征，看模型分数下降多少。

重要提醒：feature importance 解释的是“模型如何使用特征”，不是因果关系，也不保证特征本身有真实经济含义。

## 准备环境

```python
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
```

本节使用一个混合数值和类别特征的二分类例子。

## 准备数据

```python
X = pd.DataFrame({
    "momentum": [-2.5, -2.1, -1.8, -1.4, -1.1, -0.8, -0.4, -0.1,
                 0.1, 0.4, 0.7, 1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8],
    "volatility": [0.45, 0.42, 0.39, 0.37, 0.34, 0.32, 0.30, 0.28,
                   0.27, 0.25, 0.24, 0.22, 0.21, 0.19, 0.18, 0.17, 0.16, 0.15],
    "liquidity": [7, 8, 9, 10, 11, 12, 13, 14,
                  15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    "sector": ["energy", "finance", "energy", "tech", "finance", "health", "energy", "finance",
               "tech", "health", "finance", "tech", "energy", "health", "tech", "finance", "tech", "health"],
})

y = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0,
               1, 1, 1, 1, 1, 1, 1, 1, 1], name="target")

numeric_features = ["momentum", "volatility", "liquidity"]
categorical_features = ["sector"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.33,
    random_state=42,
    stratify=y,
)

print(X_train.shape)
print(X_test.shape)
```

构造统一预处理器：

```python
preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
    ],
)
```

## 树模型 feature_importances_

树模型和随机森林拟合后通常有 `feature_importances_`。

```python
forest_pipe = Pipeline([
    ("preprocess", preprocess),
    ("model", RandomForestClassifier(
        n_estimators=80,
        max_depth=3,
        random_state=42,
    )),
])

forest_pipe.fit(X_train, y_train)

test_prob = forest_pipe.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, test_prob)

print(test_auc)
```

取出预处理后的特征名和随机森林重要性：

```python
feature_names = forest_pipe.named_steps["preprocess"].get_feature_names_out()
forest_importance = forest_pipe.named_steps["model"].feature_importances_

forest_importance_s = (
    pd.Series(forest_importance, index=feature_names, name="importance")
    .sort_values(ascending=False)
)

print(forest_importance_s)
print(forest_importance_s.sum())
```

这些重要性对应的是预处理后的特征，例如：

- `num__momentum`
- `num__volatility`
- `cat__sector_tech`

如果类别列被 one-hot 成多列，树模型会给每个 one-hot 列单独的重要性。

## feature_importances_ 的含义和局限

随机森林的 `feature_importances_` 通常基于 impurity 减少。直觉是：某个特征越能帮助树切分样本，它的重要性越高。

但它有局限：

- 对高基数特征可能偏高。
- 对强相关特征，重要性可能被分散或被其中一个特征吸走。
- 它是在训练好的模型内部计算，不直接衡量验证集上打乱特征后的性能损失。
- 它不提供方向：只说重要，不说正向还是负向。

因此不要只凭 `feature_importances_` 做业务结论。

## 线性模型系数 coef_

线性模型的系数有方向。正系数表示特征增加会提高正类 log-odds，负系数表示降低。

```python
logit_pipe = Pipeline([
    ("preprocess", preprocess),
    ("model", LogisticRegression(max_iter=1000, solver="liblinear")),
])

logit_pipe.fit(X_train, y_train)

logit_names = logit_pipe.named_steps["preprocess"].get_feature_names_out()
coef = logit_pipe.named_steps["model"].coef_[0]

coef_s = (
    pd.Series(coef, index=logit_names, name="coef")
    .sort_values(key=np.abs, ascending=False)
)

print(coef_s)
```

由于数值列经过了 `StandardScaler`，数值系数大致可以在标准化尺度上比较。one-hot 类别列的系数则相对于模型截距和其他类别列共同解释。

## 系数解释的注意点

线性系数也不能直接当成因果影响。

常见注意点：

- 特征缩放会影响系数大小。
- 相关特征会让系数不稳定。
- 正则化强度会压缩系数。
- one-hot 类别系数取决于编码方式和基准含义。
- 线性模型只表达线性方向，不能捕捉复杂非线性关系。

如果要比较数值特征系数，应确保它们在相似尺度上，例如使用 `StandardScaler`。

## permutation_importance：打乱特征看性能下降

`permutation_importance` 的思路是：

1. 在验证集或测试集上计算原始分数。
2. 打乱某一列特征。
3. 重新计算分数。
4. 分数下降越多，说明模型越依赖该特征。

对 Pipeline 调用时，可以直接传入原始 DataFrame。这样打乱的是原始列，而不是 one-hot 后的列。

```python
perm = permutation_importance(
    forest_pipe,
    X_test,
    y_test,
    scoring="roc_auc",
    n_repeats=20,
    random_state=42,
)

perm_importance = (
    pd.DataFrame({
        "feature": X_test.columns,
        "importance_mean": perm.importances_mean,
        "importance_std": perm.importances_std,
    })
    .sort_values("importance_mean", ascending=False)
)

print(perm_importance)
```

`importance_mean` 表示打乱该列后平均分数下降多少。它可以为负，表示打乱后分数反而略有提升，通常说明这个特征在当前样本上没有稳定贡献，或样本太小导致噪声。

## permutation_importance 应该在哪个数据上算

不要在训练集上解释泛化表现。更推荐在：

- 验证集上计算，用于模型诊断。
- 独立测试集上计算，用于最终分析，但不要反复据此调模型。
- 时间序列任务的未来窗口上计算，保持时间顺序。

```python
train_perm = permutation_importance(
    forest_pipe,
    X_train,
    y_train,
    scoring="roc_auc",
    n_repeats=10,
    random_state=42,
)

print(train_perm.importances_mean)
```

训练集上的 importance 可能更乐观，尤其是过拟合模型。

## 比较两种重要性

模型内部重要性和 permutation importance 回答的问题不同。

```python
internal_by_raw_feature = pd.Series(0.0, index=X.columns, name="internal_importance")

for name, value in forest_importance_s.items():
    if name.startswith("num__"):
        raw_name = name.replace("num__", "")
    elif name.startswith("cat__sector_"):
        raw_name = "sector"
    else:
        raw_name = name
    internal_by_raw_feature.loc[raw_name] += value

comparison = perm_importance.set_index("feature").join(internal_by_raw_feature)

print(comparison)
```

内部重要性按预处理后特征计算；这里把 one-hot 的 sector 列合并回原始 `sector` 特征，方便和 permutation importance 对比。

两者不一致并不奇怪。比如一个特征在训练树切分时常被使用，但在测试集上打乱它并不明显降低 AUC，说明它的泛化贡献可能有限。

## 相关特征会影响解释

如果两个特征高度相关，打乱其中一个时，另一个仍然保留类似信息，permutation importance 可能低估单个特征的重要性。

```python
X_corr = X.copy()
X_corr["momentum_copy"] = X_corr["momentum"] + 0.01

numeric_corr = ["momentum", "momentum_copy", "volatility", "liquidity"]

corr_preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_corr),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
    ],
)

corr_pipe = Pipeline([
    ("preprocess", corr_preprocess),
    ("model", RandomForestClassifier(n_estimators=80, max_depth=3, random_state=42)),
])

X_corr_train = X_corr.loc[X_train.index]
X_corr_test = X_corr.loc[X_test.index]

corr_pipe.fit(X_corr_train, y_train)

corr_perm = permutation_importance(
    corr_pipe,
    X_corr_test,
    y_test,
    scoring="roc_auc",
    n_repeats=20,
    random_state=42,
)

corr_perm_s = pd.Series(corr_perm.importances_mean, index=X_corr_test.columns).sort_values(ascending=False)

print(corr_perm_s)
```

相关特征解释时，最好结合领域知识、相关矩阵、分组 permutation 或特征消融实验。

## 解释不是因果

即使某个特征 importance 很高，也只能说明模型依赖它做预测。它可能是：

- 真正有预测信息的特征。
- 另一个隐藏变量的代理变量。
- 数据泄露列。
- 与标签构造方式机械相关的列。
- 训练样本中的偶然相关。

例如，如果把未来收益或标签本身误放进特征，importance 会非常高，但模型完全不可用。

```python
X_leaky = X.copy()
X_leaky["target_leak"] = y

leaky_train = X_leaky.loc[X_train.index]
leaky_test = X_leaky.loc[X_test.index]

leaky_features = numeric_features + ["target_leak"]

leaky_preprocess = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), leaky_features),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
    ],
)

leaky_pipe = Pipeline([
    ("preprocess", leaky_preprocess),
    ("model", RandomForestClassifier(n_estimators=50, random_state=42)),
])

leaky_pipe.fit(leaky_train, y_train)

leaky_auc = roc_auc_score(y_test, leaky_pipe.predict_proba(leaky_test)[:, 1])

print(leaky_auc)
```

这类高分和高 importance 是危险信号，不是好模型。

## 常见坑

第一，把 feature importance 当作因果解释。

importance 只能说明模型用没用某个特征，不能说明改变该特征会导致结果改变。

第二，在训练集上解释过拟合模型。

训练集 importance 很高，可能只是模型记住了训练样本。应优先在验证集或独立测试集上看 permutation importance。

第三，忽略预处理后的特征名。

Pipeline 里 one-hot 后的特征名会变化。解释 `feature_importances_` 前，必须用 `get_feature_names_out()` 对齐列名。

第四，忽略相关特征。

强相关特征会让重要性分摊或互相替代。单个特征 importance 低，不代表整组信息没用。

第五，看到泄露特征高 importance 还当作发现了强信号。

任何和标签构造、未来数据、样本 ID 强相关的高 importance 特征，都应优先怀疑泄露。

## 实战提示

解释模型前，先确认这些基本条件：

```python
assert X_test.index.equals(y_test.index)
assert set(X_train.columns) == set(X_test.columns)
assert hasattr(forest_pipe.named_steps["model"], "feature_importances_")
```

提取内部重要性时：

```python
feature_names = forest_pipe.named_steps["preprocess"].get_feature_names_out()
importance = forest_pipe.named_steps["model"].feature_importances_

assert len(feature_names) == len(importance)
```

做 permutation importance 时：

```python
perm = permutation_importance(
    forest_pipe,
    X_test,
    y_test,
    scoring="roc_auc",
    n_repeats=20,
    random_state=42,
)

assert len(perm.importances_mean) == X_test.shape[1]
```

模型解释报告里建议同时写清楚：

- 使用的是内部 importance 还是 permutation importance。
- importance 是在哪个数据集上算的。
- 使用的评分指标。
- 是否经过 Pipeline 和 one-hot。
- 相关特征和潜在泄露风险。

## 小结

sklearn 中常见解释方式有三类：

- 线性模型 `coef_`：有方向，但受缩放、相关性和正则化影响。
- 树模型 `feature_importances_`：模型内部切分贡献，方便但有偏差。
- `permutation_importance`：打乱特征看验证性能下降，更贴近泛化贡献，但受样本量和相关特征影响。

解释模型时，最重要的是不要把“模型依赖”误读成“真实因果”，也不要忽视泄露和相关特征带来的误导。

## 自检问题

1. 树模型的 `feature_importances_` 和 `permutation_importance` 分别回答什么问题？
2. 为什么解释 Pipeline 中的树模型时要用 `get_feature_names_out()`？
3. 线性模型系数为什么受特征缩放影响？
4. 强相关特征会如何影响 permutation importance？
5. 为什么高 importance 的特征反而可能是泄露风险信号？
