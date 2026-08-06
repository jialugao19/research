# XGBoost & LightGBM

## 核心概念

XGBoost 和 LightGBM 都属于 gradient boosting tree。

它们和随机森林的关键区别是：

```text
随机森林：很多树并行训练，最后平均或投票。
boosting：树一棵接一棵训练，每棵新树修正前面模型的错误。
```

随机森林主要降低方差。

boosting 更强调逐步降低偏差。

简化理解：

```text
第 1 棵树先做一个粗预测
第 2 棵树学习第 1 棵树没解释好的部分
第 3 棵树继续修正剩余错误
...
```

最终模型是很多棵弱树的加和。

## boosting 的加法模型

boosting 模型可以写成：

```text
prediction = tree_1(x) + tree_2(x) + ... + tree_M(x)
```

每一棵树不是独立投票。

它们是累加关系。

小例子：

```python
tree_outputs = [0.10, -0.03, 0.02]

prediction = sum(tree_outputs)

print(prediction)
```

结果：

```text
0.09000000000000001
```

第一棵树给 `0.10`。

第二棵树修正 `-0.03`。

第三棵树再修正 `0.02`。

最终预测是 `0.09`。

## 残差直觉

对平方误差回归来说，最简单的 boosting 可以理解为拟合残差。

假设真实值是：

```python
y_true = [0.05, -0.02, 0.03]
y_pred = [0.02, 0.00, 0.01]

residuals = [
    true - pred
    for true, pred in zip(y_true, y_pred)
]

print(residuals)
```

结果：

```text
[0.030000000000000002, -0.02, 0.019999999999999997]
```

下一棵树要学习这些残差。

如果新树能预测残差，累加后误差会下降。

## 学习率

boosting 不会把每棵树的输出完整加上去。

通常会乘以 learning rate。

```text
new_prediction = old_prediction + learning_rate * new_tree_output
```

小例子：

```python
old_prediction = 0.02
new_tree_output = 0.03
learning_rate = 0.10

new_prediction = old_prediction + learning_rate * new_tree_output

print(new_prediction)
```

结果：

```text
0.023
```

学习率越小，更新越慢，通常需要更多树。

学习率越大，训练更快，但更容易过拟合。

常见做法：

```text
较小 learning_rate + 较多 n_estimators
```

## 逐步更新

多轮 boosting 更新可以这样理解：

```python
prediction = 0.0
learning_rate = 0.2
tree_outputs = [0.50, -0.10, 0.05]

history = []
for output in tree_outputs:
    prediction += learning_rate * output
    history.append(prediction)

print(history)
```

结果：

```text
[0.1, 0.08, 0.09]
```

每一轮都只是小步修正。

这就是 shrinkage。

## 梯度的直觉

对一般损失函数，boosting 不一定直接拟合普通残差。

它拟合的是损失函数的负梯度方向。

简化理解：

```text
梯度告诉模型：当前预测应该往哪个方向改，损失下降最快。
```

平方误差：

```text
loss = 1/2 * (y - pred)^2
negative_gradient = y - pred
```

所以平方误差下，负梯度就是残差。

小例子：

```python
y = 0.05
pred = 0.02

negative_gradient = y - pred

print(negative_gradient)
```

结果：

```text
0.030000000000000002
```

分类、排序和其他目标函数下，梯度形式不同。

但思想仍然是：

```text
下一棵树学习如何让损失下降
```

## XGBoost 的二阶信息

XGBoost 不只用一阶梯度。

它还使用二阶梯度，也就是 Hessian。

简化理解：

```text
gradient: 往哪个方向改
hessian: 当前损失曲线有多陡、多弯
```

在节点分裂时，XGBoost 会汇总样本的 gradient 和 hessian 来计算 split gain。

一个简化的叶子权重公式：

```text
leaf_weight = -G / (H + lambda)
```

其中：

- `G` 是该叶子内 gradient 之和。
- `H` 是该叶子内 hessian 之和。
- `lambda` 是 L2 正则。

小例子：

```python
G = -2.0
H = 5.0
reg_lambda = 1.0

leaf_weight = -G / (H + reg_lambda)

print(leaf_weight)
```

结果：

```text
0.3333333333333333
```

`lambda` 越大，叶子权重越保守。

## XGBoost split gain

XGBoost 的 split gain 可以简化理解为：

```text
分裂后左右叶子的目标改善 - 分裂前父节点的目标改善 - 分裂惩罚
```

常见简化公式：

```text
gain = 1/2 * (
    G_L^2 / (H_L + lambda)
    + G_R^2 / (H_R + lambda)
    - G^2 / (H + lambda)
) - gamma
```

小例子：

```python
G_left = -1.5
H_left = 3.0
G_right = -0.5
H_right = 2.0
reg_lambda = 1.0
gamma = 0.0

G_parent = G_left + G_right
H_parent = H_left + H_right

gain = 0.5 * (
    G_left ** 2 / (H_left + reg_lambda)
    + G_right ** 2 / (H_right + reg_lambda)
    - G_parent ** 2 / (H_parent + reg_lambda)
) - gamma

print(gain)
```

结果：

```text
-0.01041666666666663
```

这个 gain 是负的，说明这个 split 不值得做。

如果设置 `gamma > 0`，模型会更不愿意分裂。

## 正则化

XGBoost 和 LightGBM 都很重视正则化。

常见控制项：

```text
max_depth / num_leaves
min_child_weight / min_data_in_leaf
lambda_l1 / lambda_l2
gamma / min_split_gain
subsample
colsample_bytree / feature_fraction
learning_rate
```

这些参数的目的都是降低过拟合。

例如 L2 正则会缩小叶子权重：

```python
G = -2.0
H = 5.0

for reg_lambda in [0.0, 1.0, 5.0]:
    leaf_weight = -G / (H + reg_lambda)
    print(reg_lambda, leaf_weight)
```

结果：

```text
0.0 0.4
1.0 0.3333333333333333
5.0 0.2
```

正则越强，叶子输出越小。

模型更新更保守。

## subsample 和 feature_fraction

boosting 也可以引入随机性。

常见方法：

- 每棵树只用一部分样本：`subsample`。
- 每棵树只用一部分特征：`colsample_bytree` 或 `feature_fraction`。

小例子：

```python
n_samples = 1000
subsample = 0.8

used_samples = int(n_samples * subsample)

print(used_samples)
```

结果：

```text
800
```

这可以降低过拟合，也可以加速训练。

但如果样本本来就少，subsample 太低可能让模型不稳定。

## XGBoost 和 LightGBM 的差异

简化对比：

```text
XGBoost:
    经典、稳健、正则化设计强
    通常 level-wise 生长或受 max_depth 控制
    工程成熟，使用广泛

LightGBM:
    训练速度快，适合大数据
    常用 histogram 算法
    leaf-wise 生长，配合 num_leaves 控制复杂度
    对类别特征和高维稀疏特征有工程优化
```

不要把它们理解成谁绝对更好。

在实际项目里，要看：

- 数据规模。
- 特征数量。
- 稀疏程度。
- 是否需要速度。
- 是否容易过拟合。
- 验证集表现。

## level-wise 和 leaf-wise

level-wise 生长倾向于一层一层扩展。

leaf-wise 生长每次选择当前最能降低损失的叶子继续分裂。

简化例子：

```python
leaf_gains = {
    "leaf_A": 0.02,
    "leaf_B": 0.15,
    "leaf_C": 0.04,
}

next_leaf = max(leaf_gains, key=leaf_gains.get)

print(next_leaf)
```

结果：

```text
leaf_B
```

leaf-wise 会优先分裂 `leaf_B`。

它可能更快降低训练误差，但也更容易在小样本上过拟合。

所以 LightGBM 的 `num_leaves`、`min_data_in_leaf` 很重要。

## histogram 分裂

LightGBM 常用 histogram 方法加速分裂搜索。

它不是对每个连续取值都尝试 split。

而是先把连续特征分桶。

```python
values = [0.12, 0.18, 0.35, 0.42, 0.77]
bins = []

for value in values:
    if value < 0.30:
        bins.append("low")
    elif value < 0.60:
        bins.append("mid")
    else:
        bins.append("high")

print(bins)
```

结果：

```text
['low', 'low', 'mid', 'mid', 'high']
```

分桶后，搜索 split 的候选数量减少。

训练速度和内存效率会更好。

代价是 split 精度会有近似。

## early stopping

boosting 容易随着树越来越多而过拟合。

所以常用 early stopping。

思想：

```text
如果验证集指标连续多轮不提升，就停止训练。
```

小例子：

```python
valid_scores = [0.02, 0.04, 0.05, 0.049, 0.048, 0.047]
patience = 2

best_score = float("-inf")
best_round = None
bad_rounds = 0

for round_idx, score in enumerate(valid_scores, start=1):
    if score > best_score:
        best_score = score
        best_round = round_idx
        bad_rounds = 0
    else:
        bad_rounds += 1

    if bad_rounds >= patience:
        break

print(best_score)
print(best_round)
print(round_idx)
```

结果：

```text
0.05
3
5
```

第 3 轮验证集最好。

之后连续 2 轮没有提升，在第 5 轮停止。

## 参数的基本关系

常见调参关系：

```text
learning_rate 下降 -> n_estimators 通常要增加
max_depth / num_leaves 增大 -> 模型更复杂
min_child_weight / min_data_in_leaf 增大 -> 模型更保守
subsample / colsample 降低 -> 随机性更强
lambda / gamma 增大 -> 正则更强
```

简化判断：

```python
train_score = 0.12
valid_score = 0.03

overfit_gap = train_score - valid_score
need_more_regularization = overfit_gap > 0.05

print(overfit_gap)
print(need_more_regularization)
```

结果：

```text
0.09
True
```

训练表现远好于验证表现，说明需要更强正则、更浅树或更早停止。

## 在量化中的使用

XGBoost / LightGBM 在量化里常用于：

- 横截面收益预测。
- 分类买入 / 持有 / 卖出。
- 因子非线性组合。
- 风险模型残差预测。
- 事件后收益预测。
- 信号筛选或 stacking。

但它们不是“自动赚钱机器”。

金融数据里常见问题仍然存在：

- 标签噪声大。
- 非平稳。
- 特征相关。
- 样本外衰减。
- 成本和换手。
- 前视偏差。
- 行业、市值和流动性暴露。

## 时间序列验证

boosting 模型很强，尤其需要严格验证。

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    model = LGBMRegressor(params)
    model.fit(
        x_train[train_period],
        y_train[train_period],
        eval_set=[(x_valid[valid_period], y_valid[valid_period])],
        early_stopping_rounds=50,
    )
    pred = model.predict(x_valid[valid_period])
    score = evaluate_net_ic_and_return(pred, y_valid[valid_period], cost[valid_period])
```

不要随机打散时间序列后直接交叉验证。

尤其不要让同一时间附近的重叠标签同时出现在 train 和 valid。

## 量化调参起点

一个保守起点：

```text
learning_rate: 小一些，例如 0.01 到 0.05
n_estimators: 配合 early stopping
max_depth / num_leaves: 不要太大
min_data_in_leaf: 设得足够大
subsample / feature_fraction: 0.6 到 0.9
lambda_l1 / lambda_l2: 用验证集选择
```

更重要的是：

```text
按时间验证，而不是只调训练指标
```

如果验证表现非常不稳定，先降低模型复杂度。

## 常见误区

第一，认为 LightGBM / XGBoost 一定比线性模型好。

如果信号弱、样本少、噪声大，复杂模型可能更差。

第二，用随机 CV 调参。

金融时序里这很容易乐观。

第三，只看 AUC、MSE 或 IC，不看扣成本后的收益。

第四，特征泄露后模型表现异常好，却误以为模型强。

第五，树太深、叶子太小、树太多。

第六，把 feature importance 当作稳定解释。

第七，不做分年份、分 regime、分股票池稳定性检查。

## 小结

XGBoost 和 LightGBM 的核心是 gradient boosting tree。

它们通过一棵棵树逐步修正前面模型的错误。

需要重点理解：

```text
boosting 是加法模型
每轮学习损失下降方向
learning_rate 控制每轮步长
正则化控制叶子权重和树复杂度
early stopping 防止树数过多
XGBoost 更强调正则化框架
LightGBM 更强调高效分裂和大规模训练
```

在量化机器学习里，它们是强大的非线性模型。

但越强的模型越需要严格防泄露、严肃验证和扣成本评估。
