# sklearn：train / test split、交叉验证与时间序列切分

## 核心概念

模型评估的核心问题是：用没参与训练的数据估计泛化能力。

sklearn 常见切分工具包括：

- `train_test_split`：一次性切出训练集和测试集。
- `KFold`：普通 K 折交叉验证。
- `StratifiedKFold`：分类任务中保持每折类别比例。
- `cross_val_score` / `cross_validate`：按指定切分器重复训练和评估。
- `TimeSeriesSplit`：时间序列任务中按时间顺序滚动切分。
- `GroupKFold`：同一组样本不能同时出现在训练和测试中。

最重要的原则：测试集不能参与训练、预处理参数学习、调参和模型选择。时间序列任务还要保证训练数据发生在测试数据之前。

## 准备数据

```python
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import (
    GroupKFold,
    KFold,
    StratifiedKFold,
    TimeSeriesSplit,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
```

先构造一个二分类数据集，假设样本之间可以近似视为独立同分布。

```python
X = pd.DataFrame({
    "signal": [-2.4, -1.8, -1.4, -0.9, -0.4, -0.1, 0.2, 0.6, 0.9, 1.3, 1.8, 2.4],
    "risk": [0.42, 0.39, 0.37, 0.34, 0.31, 0.28, 0.27, 0.24, 0.22, 0.20, 0.18, 0.16],
    "liquidity": [10, 12, 11, 13, 15, 14, 16, 18, 19, 21, 20, 23],
})

y = pd.Series([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], name="target")

print(X)
print(y.value_counts().sort_index())
```

后续例子都会用 Pipeline，把 scaler 放进交叉验证内部。

```python
clf_pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])
```

## train_test_split：一次性切分

最基本的切分方式：

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
print(y_train.value_counts().sort_index())
print(y_test.value_counts().sort_index())
```

参数含义：

- `test_size=0.25`：25% 样本作为测试集。
- `random_state=42`：固定随机切分，便于复现。
- `stratify=y`：保持训练集和测试集里的类别比例接近原始数据。

训练和评估：

```python
clf_pipe.fit(X_train, y_train)

y_pred = clf_pipe.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)

print(y_pred)
print(test_accuracy)
```

`train_test_split` 会同步打乱和切分 `X`、`y`，保持样本对齐。不要分别对 `X` 和 `y` 独立切分。

## 为什么分类任务常用 stratify

如果类别不平衡，随机切分可能导致测试集中少数类太少，甚至没有少数类。`stratify=y` 会尽量保持类别比例。

```python
y_imbalanced = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1], name="target")

_, _, y_train_s, y_test_s = train_test_split(
    X,
    y_imbalanced,
    test_size=0.25,
    random_state=7,
    stratify=y_imbalanced,
)

print(y_imbalanced.value_counts(normalize=True).sort_index())
print(y_train_s.value_counts(normalize=True).sort_index())
print(y_test_s.value_counts(normalize=True).sort_index())
```

分层切分不是让训练集和测试集完全一样，而是降低类别比例随机偏差。

## 训练集、验证集、测试集

常见实践是：

- 训练集：拟合模型参数。
- 验证集：选择模型、调超参数、比较方案。
- 测试集：最终只用一次，估计最终泛化表现。

可以用两次 `train_test_split` 切出三份数据：

```python
X_train_val, X_test_final, y_train_val, y_test_final = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y,
)

X_train_only, X_val, y_train_only, y_val = train_test_split(
    X_train_val,
    y_train_val,
    test_size=1 / 3,
    random_state=43,
    stratify=y_train_val,
)

print(X_train_only.shape)
print(X_val.shape)
print(X_test_final.shape)
```

测试集如果被反复用来调参，就不再是干净测试集。

## KFold：普通交叉验证

K 折交叉验证把数据分成 K 份，每次用其中一份做验证，其余做训练。

```python
kfold = KFold(n_splits=3, shuffle=True, random_state=42)

for fold, (train_idx, test_idx) in enumerate(kfold.split(X), start=1):
    print(fold, train_idx, test_idx)
```

`shuffle=True` 表示先随机打乱再分折；`random_state` 保证可复现。

直接使用 `cross_val_score`：

```python
kfold_scores = cross_val_score(
    clf_pipe,
    X,
    y,
    cv=kfold,
    scoring="accuracy",
)

print(kfold_scores)
print(kfold_scores.mean())
```

每一折里，sklearn 都会重新 clone 一个干净的 Pipeline，先在训练折上 `fit`，再在验证折上 `score`。

## StratifiedKFold：分类更常用

分类任务里，更常用 `StratifiedKFold`，每折都尽量保持类别比例。

```python
skfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

for fold, (train_idx, test_idx) in enumerate(skfold.split(X, y), start=1):
    print(fold)
    print(y.iloc[train_idx].value_counts().sort_index().to_dict())
    print(y.iloc[test_idx].value_counts().sort_index().to_dict())
```

用分层交叉验证评估：

```python
stratified_scores = cross_val_score(
    clf_pipe,
    X,
    y,
    cv=skfold,
    scoring="accuracy",
)

print(stratified_scores)
print(stratified_scores.mean())
```

对于分类任务，如果类别分布不均衡，优先考虑 `StratifiedKFold`。

## cross_validate：返回更多信息

`cross_val_score` 只返回测试分数。`cross_validate` 可以同时返回训练分数、拟合时间、评分时间等。

```python
cv_result = cross_validate(
    clf_pipe,
    X,
    y,
    cv=skfold,
    scoring="accuracy",
    return_train_score=True,
)

print(cv_result.keys())
print(cv_result["train_score"])
print(cv_result["test_score"])
```

如果训练分数远高于验证分数，可能存在过拟合。不过小样本下波动很大，不能只看单次结果。

## Pipeline 能避免预处理泄露

错误写法是先在全数据上 fit scaler，再做交叉验证：

```python
scaler = StandardScaler()
X_scaled_bad = scaler.fit_transform(X)

bad_scores = cross_val_score(
    LogisticRegression(max_iter=1000),
    X_scaled_bad,
    y,
    cv=skfold,
    scoring="accuracy",
)

print(bad_scores)
```

这里 scaler 的均值和标准差来自全数据，包括验证折。对于真实评估，这是预处理泄露。

推荐写法是把 scaler 放进 Pipeline：

```python
good_scores = cross_val_score(
    clf_pipe,
    X,
    y,
    cv=skfold,
    scoring="accuracy",
)

print(good_scores)
```

Pipeline 会在每个训练折上单独 `fit` scaler，然后只对对应验证折 `transform`。

## 时间序列不能随机打乱

对于时间序列预测，随机切分通常会让未来样本进入训练集。

构造一个小型时间序列回归数据集：

```python
dates = pd.bdate_range("2024-01-02", periods=12)

X_ts = pd.DataFrame({
    "lag_return": [-0.02, 0.01, 0.00, 0.02, -0.01, 0.03, 0.01, -0.02, 0.02, 0.01, -0.01, 0.02],
    "lag_vol": [0.20, 0.18, 0.19, 0.17, 0.21, 0.16, 0.15, 0.22, 0.18, 0.17, 0.20, 0.16],
}, index=dates)

y_ts = pd.Series(
    [0.010, -0.004, 0.006, 0.012, -0.003, 0.015, 0.008, -0.006, 0.011, 0.004, -0.002, 0.009],
    index=dates,
    name="future_return",
)

print(X_ts)
print(y_ts)
```

如果只做一个简单时间顺序 holdout，可以写：

```python
X_ts_train, X_ts_test, y_ts_train, y_ts_test = train_test_split(
    X_ts,
    y_ts,
    test_size=0.25,
    shuffle=False,
)

print(X_ts_train.index.min(), X_ts_train.index.max())
print(X_ts_test.index.min(), X_ts_test.index.max())
```

`shuffle=False` 保证测试集在训练集之后。但时间序列评估更常见的是滚动切分。

## TimeSeriesSplit

`TimeSeriesSplit` 会让训练窗口始终早于测试窗口。

```python
tscv = TimeSeriesSplit(n_splits=3, test_size=2)

for fold, (train_idx, test_idx) in enumerate(tscv.split(X_ts), start=1):
    train_dates = X_ts.index[train_idx]
    test_dates = X_ts.index[test_idx]
    print(fold, train_dates.min(), train_dates.max(), test_dates.min(), test_dates.max())
```

每一折里，训练集都发生在测试集之前。

用 Pipeline 做时间序列交叉验证：

```python
reg_pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", LinearRegression()),
])

neg_mae = cross_val_score(
    reg_pipe,
    X_ts,
    y_ts,
    cv=tscv,
    scoring="neg_mean_absolute_error",
)

mae = -neg_mae

print(mae)
print(mae.mean())
```

sklearn 的损失类指标常用“越大越好”的约定，因此 `neg_mean_absolute_error` 返回负数。取负号后才是 MAE。

## gap：给时间序列留隔离带

有些任务中，训练窗口和测试窗口之间需要留出 gap，避免标签重叠或信息延迟。

```python
tscv_gap = TimeSeriesSplit(n_splits=3, test_size=2, gap=1)

for fold, (train_idx, test_idx) in enumerate(tscv_gap.split(X_ts), start=1):
    print(fold, train_idx, test_idx)
    print(train_idx.max(), test_idx.min())
```

`gap=1` 表示每折训练集末尾和测试集开头之间隔开 1 个样本。

检查这个关系：

```python
for train_idx, test_idx in tscv_gap.split(X_ts):
    assert train_idx.max() + 1 < test_idx.min()
```

如果标签是未来 5 天收益，或者特征公布有延迟，gap 往往很重要。

## max_train_size：滚动窗口

默认情况下，`TimeSeriesSplit` 的训练窗口会扩张。也可以限制最大训练长度。

```python
rolling_tscv = TimeSeriesSplit(n_splits=3, test_size=2, max_train_size=5)

for fold, (train_idx, test_idx) in enumerate(rolling_tscv.split(X_ts), start=1):
    print(fold, len(train_idx), train_idx, test_idx)
```

这更接近“只用最近一段历史训练”的设定。扩张窗口还是滚动窗口，取决于任务是否认为很久以前的数据仍然有参考价值。

## GroupKFold：避免同组泄露

有些数据不是时间序列，但同一组样本之间高度相关。例如同一个用户、同一只股票、同一个交易日、同一个实验批次。

```python
groups = pd.Series(
    ["A", "A", "A", "B", "B", "B", "C", "C", "C", "D", "D", "D"],
    name="group",
)

group_cv = GroupKFold(n_splits=4)

for fold, (train_idx, test_idx) in enumerate(group_cv.split(X, y, groups=groups), start=1):
    train_groups = set(groups.iloc[train_idx])
    test_groups = set(groups.iloc[test_idx])
    print(fold, train_groups, test_groups, train_groups & test_groups)
```

每一折中，测试组不会出现在训练组里。

```python
group_scores = cross_val_score(
    clf_pipe,
    X,
    y,
    cv=group_cv,
    groups=groups,
    scoring="accuracy",
)

print(group_scores)
```

如果同一实体的多条样本同时出现在训练和测试中，模型可能记住实体特征，而不是真正学会泛化。

## 常见坑

第一，用随机切分评估时间序列。

```python
# 不推荐用于时间序列预测
# train_test_split(X_ts, y_ts, test_size=0.25, shuffle=True)
```

这会让未来样本进入训练集。

第二，在切分前对全数据做预处理。

```python
# 不推荐
# X_scaled = StandardScaler().fit_transform(X)
# cross_val_score(model, X_scaled, y, cv=skfold)
```

应把预处理放进 Pipeline。

第三，把测试集当验证集反复调参。

如果多次看测试集表现并据此改模型，测试集就已经参与模型选择，最终分数会偏乐观。

第四，分类任务忘记分层。

小样本或类别不均衡时，不分层可能导致某折类别比例异常，甚至某一类缺失。

第五，忽略 group leakage。

如果样本有用户、股票、日期、实验批次等分组，普通 KFold 可能把同组样本拆到训练和测试两边。

## 实战提示

选择切分方式时，先回答：

1. 样本是否可以近似独立同分布？
2. 是否有时间顺序？
3. 是否有不能跨训练和测试的 group？
4. 任务是分类还是回归？
5. 是否需要保留最终测试集，只用一次？

基本检查可以写成：

```python
assert len(X) == len(y)
assert X.index.is_unique
assert y.index.is_unique
assert X.index.equals(y.index)
```

时间序列还应检查：

```python
assert X_ts.index.is_monotonic_increasing
assert y_ts.index.is_monotonic_increasing
assert X_ts.index.equals(y_ts.index)
```

交叉验证时，优先把完整流程放进 Pipeline：

```python
scores = cross_val_score(
    clf_pipe,
    X,
    y,
    cv=skfold,
    scoring="accuracy",
)

print(scores.mean())
```

## 小结

sklearn 的切分和交叉验证工具解决的是评估流程问题：

- `train_test_split` 适合简单 holdout。
- 分类任务常用 `stratify` 或 `StratifiedKFold`。
- `cross_val_score` 和 `cross_validate` 会在每折重新训练 estimator。
- Pipeline 可以避免预处理参数从验证折泄露到训练流程。
- 时间序列应使用顺序切分或 `TimeSeriesSplit`。
- 有实体或批次相关性时，应考虑 `GroupKFold`。

评估结果是否可信，首先取决于切分方式是否匹配数据生成过程。

## 自检问题

1. 为什么分类任务常用 `stratify=y` 或 `StratifiedKFold`？
2. 为什么预处理应放进 Pipeline 再做交叉验证？
3. `TimeSeriesSplit` 和普通 `KFold` 的关键区别是什么？
4. `gap` 在时间序列切分里解决什么问题？
5. 什么情况下应该考虑 `GroupKFold`？
