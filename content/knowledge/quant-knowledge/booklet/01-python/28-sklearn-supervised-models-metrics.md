# 28. sklearn：监督学习基础：线性模型、树模型、分类与回归指标

## 核心概念

监督学习的输入是特征 `X` 和标签 `y`：

- 分类任务：`y` 是类别，例如涨/跌、违约/不违约、买/卖/持有。
- 回归任务：`y` 是连续值，例如未来收益、成交量、波动率、价格变化。

sklearn 里监督学习模型大多遵循同一套接口：

- `fit(X, y)`：训练模型。
- `predict(X)`：输出类别或连续预测值。
- `predict_proba(X)`：分类概率，部分分类器支持。
- `score(X, y)`：默认评估指标，分类通常是 accuracy，回归通常是 R-squared。

本节聚焦常见模型和常见指标：

- 线性模型：`LogisticRegression`、`LinearRegression`、`Ridge`。
- 树模型：`DecisionTreeClassifier`、`DecisionTreeRegressor`。
- 集成树：`RandomForestClassifier`、`RandomForestRegressor`。
- 分类指标：accuracy、precision、recall、F1、confusion matrix、ROC AUC。
- 回归指标：MAE、RMSE、R-squared。

## 准备环境

```python
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
```

## 分类数据

构造一个小型二分类数据集。目标是预测下一期是否上涨。

```python
X_cls = pd.DataFrame({
    "momentum": [-2.4, -2.0, -1.7, -1.3, -0.9, -0.6, -0.3, -0.1,
                 0.2, 0.5, 0.8, 1.1, 1.4, 1.8, 2.1, 2.5],
    "volatility": [0.42, 0.40, 0.38, 0.36, 0.34, 0.32, 0.30, 0.28,
                   0.27, 0.25, 0.23, 0.21, 0.20, 0.18, 0.17, 0.15],
    "liquidity": [8, 9, 10, 11, 11, 12, 13, 14,
                  15, 16, 17, 18, 19, 20, 21, 22],
})

y_cls = pd.Series([0, 0, 0, 0, 0, 0, 0, 0,
                   1, 1, 1, 1, 1, 1, 1, 1], name="up_next")

print(X_cls.head())
print(y_cls.value_counts().sort_index())
```

切出训练集和测试集：

```python
X_cls_train, X_cls_test, y_cls_train, y_cls_test = train_test_split(
    X_cls,
    y_cls,
    test_size=0.25,
    random_state=42,
    stratify=y_cls,
)

print(X_cls_train.shape)
print(X_cls_test.shape)
```

`stratify=y_cls` 保证训练集和测试集里两个类别都有合理比例。

## LogisticRegression：线性分类模型

逻辑回归是线性分类模型。它学习的是特征到类别概率的线性边界。

数值特征量纲不同，线性模型通常建议配合标准化：

```python
logit_pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])

logit_pipe.fit(X_cls_train, y_cls_train)

pred_label = logit_pipe.predict(X_cls_test)
pred_prob = logit_pipe.predict_proba(X_cls_test)

print(pred_label)
print(pred_prob)
```

`predict` 输出类别；`predict_proba` 输出每个类别的概率。

```python
classes = logit_pipe.named_steps["model"].classes_

prob_df = pd.DataFrame(
    pred_prob,
    index=X_cls_test.index,
    columns=[f"prob_class_{cls}" for cls in classes],
)

print(prob_df)
```

如果正类是 `1`，通常取 `prob_class_1` 作为打分：

```python
positive_score = pred_prob[:, list(classes).index(1)]

print(positive_score)
```

## 分类指标：accuracy、precision、recall、F1

```python
acc = accuracy_score(y_cls_test, pred_label)
precision = precision_score(y_cls_test, pred_label)
recall = recall_score(y_cls_test, pred_label)
f1 = f1_score(y_cls_test, pred_label)

print(acc)
print(precision)
print(recall)
print(f1)
```

含义：

- accuracy：预测对的比例。
- precision：预测为正的样本中，有多少是真的正。
- recall：真实为正的样本中，有多少被找出来。
- F1：precision 和 recall 的调和平均。

不同任务关注不同指标。比如风控里可能更重视 recall，交易信号里可能更重视 precision，排序模型里可能更关注 AUC 或 RankIC。

## confusion matrix

混淆矩阵能展示预测类别和真实类别的对应关系。

```python
cm = confusion_matrix(y_cls_test, pred_label, labels=[0, 1])

print(cm)
```

对于二分类，矩阵含义是：

```text
[[TN, FP],
 [FN, TP]]
```

可以和 `classification_report` 一起查看：

```python
report = classification_report(y_cls_test, pred_label, zero_division=0)

print(report)
```

`zero_division=0` 表示如果某个类别没有被预测出来，相关指标记为 0，避免警告干扰。

## ROC AUC：使用概率或分数

ROC AUC 衡量模型把正类排在负类前面的能力。它使用连续分数，而不是硬标签。

```python
auc = roc_auc_score(y_cls_test, positive_score)

print(auc)
```

不要把 `predict` 的 0/1 标签当作 AUC 的主要输入。AUC 更适合接收概率、`decision_function` 或其他连续分数。

## 阈值影响 precision 和 recall

默认 `predict` 通常使用 0.5 作为概率阈值。你可以自己改阈值。

```python
threshold = 0.6
pred_label_06 = (positive_score >= threshold).astype(int)

print(pred_label_06)
print(precision_score(y_cls_test, pred_label_06, zero_division=0))
print(recall_score(y_cls_test, pred_label_06, zero_division=0))
```

提高阈值通常会减少正类预测，可能提升 precision，但降低 recall。具体取舍取决于业务成本。

## accuracy 在类别不平衡时会误导

如果 90% 样本都是 0，一个永远预测 0 的模型也有 90% accuracy。

```python
y_true_imbalanced = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
y_pred_all_zero = np.zeros_like(y_true_imbalanced)

print(accuracy_score(y_true_imbalanced, y_pred_all_zero))
print(precision_score(y_true_imbalanced, y_pred_all_zero, zero_division=0))
print(recall_score(y_true_imbalanced, y_pred_all_zero, zero_division=0))
```

这说明 accuracy 不能单独评价不平衡分类任务。至少要同时看 confusion matrix、precision、recall 或 AUC。

## 树分类模型

决策树通过切分特征空间做分类。

```python
tree_clf = DecisionTreeClassifier(max_depth=2, random_state=42)
tree_clf.fit(X_cls_train, y_cls_train)

tree_pred = tree_clf.predict(X_cls_test)

print(tree_pred)
print(accuracy_score(y_cls_test, tree_pred))
print(tree_clf.feature_importances_)
```

树模型通常不需要标准化，因为它根据阈值切分特征，不依赖距离或线性尺度。

随机森林是多棵树的集成：

```python
forest_clf = RandomForestClassifier(
    n_estimators=50,
    max_depth=3,
    random_state=42,
)

forest_clf.fit(X_cls_train, y_cls_train)

forest_pred = forest_clf.predict(X_cls_test)
forest_prob = forest_clf.predict_proba(X_cls_test)[:, 1]

print(forest_pred)
print(accuracy_score(y_cls_test, forest_pred))
print(roc_auc_score(y_cls_test, forest_prob))
```

随机森林通常比单棵树更稳定，但可解释性更弱，训练和预测成本也更高。

## 分类交叉验证

单次切分可能有偶然性。可以使用交叉验证估计平均表现。

```python
cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=42)

cv_auc = cross_val_score(
    logit_pipe,
    X_cls,
    y_cls,
    cv=cv,
    scoring="roc_auc",
)

print(cv_auc)
print(cv_auc.mean())
```

交叉验证会在每一折重新 fit Pipeline。预处理、模型训练和评分都在当前折内完成。

## 回归数据

回归任务的标签是连续值。下面构造一个未来收益预测的小例子。

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

X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    X_reg,
    y_reg,
    test_size=0.25,
    random_state=42,
)
```

## LinearRegression 和 Ridge

线性回归拟合：

```text
y = beta_0 + beta_1 x_1 + ... + beta_p x_p + error
```

```python
lin_pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", LinearRegression()),
])

lin_pipe.fit(X_reg_train, y_reg_train)

reg_pred = lin_pipe.predict(X_reg_test)

print(reg_pred)
print(lin_pipe.named_steps["model"].coef_)
print(lin_pipe.named_steps["model"].intercept_)
```

`Ridge` 是带 L2 正则化的线性回归，能在特征相关、样本较少时让系数更稳定。

```python
ridge_pipe = Pipeline([
    ("scale", StandardScaler()),
    ("model", Ridge(alpha=1.0)),
])

ridge_pipe.fit(X_reg_train, y_reg_train)

ridge_pred = ridge_pipe.predict(X_reg_test)

print(ridge_pred)
print(ridge_pipe.named_steps["model"].coef_)
```

`alpha` 越大，正则化越强，系数会被压得更小。参数选择会在 model selection 小节展开。

## 回归指标：MAE、RMSE、R-squared

```python
mae = mean_absolute_error(y_reg_test, reg_pred)
rmse = np.sqrt(mean_squared_error(y_reg_test, reg_pred))
r2 = r2_score(y_reg_test, reg_pred)

print(mae)
print(rmse)
print(r2)
```

含义：

- MAE：平均绝对误差，单位和目标变量相同，抗极端值能力比 MSE 强。
- RMSE：均方误差开根号，对大误差更敏感。
- R-squared：相对“预测均值”的解释度，可能为负。

金融预测里，目标噪声往往很大，R-squared 很低并不罕见。指标解释要结合任务和基准模型。

## 树回归模型

决策树回归通过切分特征空间，预测每个叶子节点的平均目标值。

```python
tree_reg = DecisionTreeRegressor(max_depth=3, random_state=42)
tree_reg.fit(X_reg_train, y_reg_train)

tree_reg_pred = tree_reg.predict(X_reg_test)

print(tree_reg_pred)
print(mean_absolute_error(y_reg_test, tree_reg_pred))
```

随机森林回归是多棵回归树的平均：

```python
forest_reg = RandomForestRegressor(
    n_estimators=100,
    max_depth=4,
    random_state=42,
)

forest_reg.fit(X_reg_train, y_reg_train)

forest_reg_pred = forest_reg.predict(X_reg_test)

print(forest_reg_pred)
print(mean_absolute_error(y_reg_test, forest_reg_pred))
```

树模型能处理非线性和特征交互，但也容易过拟合。常见控制参数包括 `max_depth`、`min_samples_leaf`、`n_estimators`。

## 回归交叉验证

sklearn 的评分器约定“越大越好”，所以损失类指标会用负数形式。

```python
neg_mae = cross_val_score(
    ridge_pipe,
    X_reg,
    y_reg,
    cv=4,
    scoring="neg_mean_absolute_error",
)

mae_scores = -neg_mae

print(mae_scores)
print(mae_scores.mean())
```

看到 `neg_mean_absolute_error` 时，要记得取负号才是 MAE。

## 线性模型和树模型怎么选

线性模型常见特点：

- 训练快，参数少，容易解释。
- 对特征缩放更敏感，通常配合 `StandardScaler`。
- 表达能力受限，主要学习线性关系。
- 正则化模型如 Ridge、Lasso 在高维和共线场景里很常用。

树模型常见特点：

- 能学习非线性和特征交互。
- 通常不需要标准化数值特征。
- 单棵树容易过拟合。
- 随机森林更稳定，但更难解释，训练成本更高。

不要只凭训练集表现选模型。模型复杂度越高，越需要干净的验证流程。

## 常见坑

第一，只看 accuracy。

类别不平衡时，accuracy 可能很高但 recall 很差。分类任务至少同时看 confusion matrix、precision、recall、F1 或 AUC。

第二，把概率和类别混为一谈。

```python
label = logit_pipe.predict(X_cls_test)
score = logit_pipe.predict_proba(X_cls_test)[:, 1]
```

阈值前的 `score` 更适合排序和 AUC；阈值后的 `label` 用于混淆矩阵和准确率。

第三，用回归器默认 `score` 就结束评估。

回归默认 `score` 是 R-squared。实际项目还应看 MAE、RMSE、残差分布和业务损失。

第四，在树模型上完全不控复杂度。

不限制深度、叶子样本数的树，很容易记住训练集。至少关注 `max_depth`、`min_samples_leaf`。

第五，把本节模型比较当作最终模型选择。

真正的模型选择需要固定切分策略、参数搜索空间和评估指标。下一节会专门讲 `GridSearchCV`、`RandomizedSearchCV` 和泄露风险。

## 实战提示

分类任务的基本检查：

```python
assert set(np.unique(y_cls)).issubset({0, 1})
assert len(X_cls) == len(y_cls)

proba = logit_pipe.predict_proba(X_cls_test)
assert np.allclose(proba.sum(axis=1), 1.0)
```

回归任务的基本检查：

```python
assert len(X_reg) == len(y_reg)
assert np.isfinite(y_reg).all()

pred = lin_pipe.predict(X_reg_test)
assert pred.shape == y_reg_test.shape
```

记录模型表现时，不要只记平均分，也要记录：

- 切分方式。
- 随机种子。
- 使用的特征列。
- 评估指标。
- 模型参数。

否则不同实验之间很难比较。

## 小结

监督学习的基本流程是：

1. 明确分类还是回归。
2. 选择合适模型族，例如线性模型或树模型。
3. 使用 Pipeline 管理预处理和模型。
4. 用匹配任务的指标评估。
5. 用交叉验证减少单次切分偶然性。

分类重在类别、概率和阈值；回归重在误差大小、解释度和残差。模型越复杂，越要重视验证流程。

## 自检问题

1. `predict` 和 `predict_proba` 分别输出什么？
2. 为什么类别不平衡时 accuracy 可能误导？
3. MAE、RMSE、R-squared 分别描述什么？
4. 线性模型为什么通常要配合标准化，而树模型通常不需要？
5. 为什么单棵决策树容易过拟合？
