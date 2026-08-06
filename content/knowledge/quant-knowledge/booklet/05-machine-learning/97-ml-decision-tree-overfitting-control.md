# 97. 机器学习：决策树的深度、叶子样本、剪枝和过拟合控制

## 核心概念

决策树很容易过拟合。

原因很直接：

```text
只要允许树不断分裂，它可以把训练样本切得非常细。
```

如果一棵树长到每个叶子只有 1 个样本，它几乎可以记住训练集。

但金融数据噪声很大。

训练集里看似有效的切分，可能只是：

- 某几天的极端行情。
- 某个股票的异常点。
- 数据对齐错误。
- 偶然的样本噪声。
- 未来信息泄露。

所以决策树训练时必须控制复杂度。

## 过拟合的直觉

过拟合树的典型表现：

```text
训练集表现很好
验证集或测试集表现明显变差
```

简化例子：

```python
train_accuracy = 0.98
valid_accuracy = 0.55

gap = train_accuracy - valid_accuracy
is_overfit = gap > 0.20

print(gap)
print(is_overfit)
```

结果：

```text
0.42999999999999994
True
```

训练集准确率接近完美，但验证集只有 `55%`。

这通常说明树记住了训练集噪声。

## 控制树深度

`max_depth` 限制树最多能分裂多少层。

深度越大，树越复杂。

```text
max_depth = 1  -> 只有一个根节点 split，像一个简单规则
max_depth = 3  -> 最多 8 个叶子
max_depth = 10 -> 最多 1024 个叶子
```

满二叉树的叶子数量上限：

```text
leaf_count <= 2 ** max_depth
```

```python
for max_depth in [1, 2, 3, 5, 10]:
    max_leaves = 2 ** max_depth
    print(max_depth, max_leaves)
```

结果：

```text
1 2
2 4
3 8
5 32
10 1024
```

深度从 `3` 增加到 `10`，叶子上限从 `8` 增加到 `1024`。

复杂度增长很快。

## max_depth 的效果

可以把 `max_depth` 看成规则复杂度。

例如：

```text
depth=1:
    volatility <= 0.2

depth=3:
    volatility <= 0.2
    momentum <= 0.05
    spread <= 0.001
```

深树能表达更复杂的交互。

但也更容易学到偶然关系。

在量化里，单棵树通常不宜太深。

因为：

- 信号弱。
- 样本非平稳。
- 特征很多且相关。
- 深层叶子样本少。
- 深层规则很难稳定复现。

## 叶子样本数

`min_samples_leaf` 控制每个叶子至少要有多少样本。

它是决策树里非常重要的防过拟合参数。

如果叶子只包含 1 个样本，预测值就是这个样本的标签。

这非常不稳定。

小例子：

```python
leaf_values = [0.04]
prediction = sum(leaf_values) / len(leaf_values)

print(prediction)
```

结果：

```text
0.04
```

这个叶子预测未来收益 `4%`。

但它只来自一个样本，可信度很低。

如果叶子有更多样本：

```python
leaf_values = [0.04, -0.01, 0.02, 0.00, 0.01]
prediction = sum(leaf_values) / len(leaf_values)

print(prediction)
```

结果：

```text
0.012
```

预测值更保守，也更稳定。

## min_samples_leaf 过滤 split

如果一个候选 split 会产生太小的叶子，就应该拒绝。

```python
left_count = 3
right_count = 27
min_samples_leaf = 5

is_allowed = left_count >= min_samples_leaf and right_count >= min_samples_leaf

print(is_allowed)
```

结果：

```text
False
```

左叶子只有 3 个样本，小于要求。

这个 split 即使训练集 gain 很高，也不能用。

## min_samples_split

`min_samples_split` 控制一个节点至少有多少样本才允许继续分裂。

例如：

```python
node_sample_count = 18
min_samples_split = 20

can_split = node_sample_count >= min_samples_split

print(can_split)
```

结果：

```text
False
```

这个节点只有 18 个样本，不允许继续分裂。

它和 `min_samples_leaf` 的区别：

```text
min_samples_split: 节点能不能尝试分裂
min_samples_leaf: 分裂后每个叶子是否足够大
```

两者通常一起使用。

## max_leaf_nodes

`max_leaf_nodes` 直接限制叶子总数。

它比 `max_depth` 更直接控制模型大小。

```python
candidate_leaf_counts = [4, 8, 16, 32]
max_leaf_nodes = 16

allowed = [
    count
    for count in candidate_leaf_counts
    if count <= max_leaf_nodes
]

print(allowed)
```

结果：

```text
[4, 8, 16]
```

叶子越多，树能记住的局部模式越多。

但样本外稳定性可能下降。

## min_impurity_decrease

`min_impurity_decrease` 要求 split 至少带来一定的不纯度下降。

如果 gain 太小，就不分裂。

```python
candidate_gains = [0.20, 0.03, 0.005]
min_impurity_decrease = 0.01

accepted_gains = [
    gain
    for gain in candidate_gains
    if gain >= min_impurity_decrease
]

print(accepted_gains)
```

结果：

```text
[0.2, 0.03]
```

很小的 gain 可能只是噪声。

设置最低增益可以避免树为了微小训练集收益继续变复杂。

## 前剪枝

前剪枝是在树生长过程中提前停止。

常见前剪枝条件：

- 达到 `max_depth`。
- 节点样本数小于 `min_samples_split`。
- 分裂后叶子小于 `min_samples_leaf`。
- gain 小于 `min_impurity_decrease`。
- 叶子数达到 `max_leaf_nodes`。

伪代码：

```python
def grow_tree(node):
    if node.depth >= max_depth:
        return make_leaf(node)
    if node.sample_count < min_samples_split:
        return make_leaf(node)

    best_split = find_best_split(node)
    if best_split.gain < min_impurity_decrease:
        return make_leaf(node)
    if best_split.left_count < min_samples_leaf:
        return make_leaf(node)
    if best_split.right_count < min_samples_leaf:
        return make_leaf(node)

    node.left = grow_tree(best_split.left)
    node.right = grow_tree(best_split.right)
```

前剪枝简单有效。

但如果限制太强，模型可能欠拟合。

## 后剪枝

后剪枝是先长一棵比较大的树，再把不值得保留的分支剪掉。

思想是：

```text
如果一个子树带来的训练误差下降很小，但复杂度增加很多，就剪掉。
```

sklearn 里常见的是 cost-complexity pruning。

它的目标可以简化理解为：

```text
score = training_error + alpha * leaf_count
```

`alpha` 越大，越惩罚复杂树。

小例子：

```python
trees = [
    {"name": "small", "train_error": 0.18, "leaf_count": 4},
    {"name": "medium", "train_error": 0.12, "leaf_count": 12},
    {"name": "large", "train_error": 0.08, "leaf_count": 30},
]

alpha = 0.005

scores = {
    tree["name"]: tree["train_error"] + alpha * tree["leaf_count"]
    for tree in trees
}

best = min(scores, key=scores.get)

print(scores)
print(best)
```

结果：

```text
{'small': 0.19999999999999998, 'medium': 0.18, 'large': 0.22999999999999998}
medium
```

大树训练误差最低。

但复杂度惩罚后，中等树最好。

## ccp_alpha

在 sklearn 中，`ccp_alpha` 控制 cost-complexity pruning。

简化理解：

```text
ccp_alpha = 0      -> 不惩罚叶子数，树可能很大
ccp_alpha 较大    -> 更强剪枝，树更小
```

伪代码：

```python
for alpha in candidate_ccp_alpha:
    model = DecisionTreeRegressor(ccp_alpha=alpha)
    model.fit(train_x, train_y)
    score = evaluate(model, valid_x, valid_y)
    record(alpha, score)

best_alpha = alpha_with_best_validation_score()
```

剪枝强度应该用验证集选择。

不要只看训练集误差。

## 验证集选择复杂度

树的复杂度参数要看样本外表现。

简化例子：

```python
results = [
    {"max_depth": 2, "train_ic": 0.03, "valid_ic": 0.025},
    {"max_depth": 4, "train_ic": 0.08, "valid_ic": 0.040},
    {"max_depth": 8, "train_ic": 0.20, "valid_ic": 0.010},
]

best = max(results, key=lambda row: row["valid_ic"])

print(best)
```

结果：

```text
{'max_depth': 4, 'train_ic': 0.08, 'valid_ic': 0.04}
```

`max_depth=8` 的训练 IC 最高。

但验证 IC 明显下降。

所以应该选 `max_depth=4`。

## 时间序列验证

金融数据不能随机打散后随便交叉验证。

因为时间序列有顺序。

如果随机切分，可能让模型看到未来分布。

更安全的方式是 walk-forward。

伪代码：

```python
splits = [
    ("2016-2018", "2019"),
    ("2017-2019", "2020"),
    ("2018-2020", "2021"),
]

for train_period, valid_period in splits:
    model = DecisionTreeRegressor(max_depth=depth, min_samples_leaf=leaf)
    model.fit(data[train_period].x, data[train_period].y)
    score = evaluate(model, data[valid_period].x, data[valid_period].y)
```

树模型非常容易利用泄露特征。

所以时间切分比普通随机 CV 更重要。

## 叶子预测的稳定性

回归树的叶子预测通常是叶子内 `y` 的均值。

叶子样本越少，均值越不稳定。

可以用 leave-one-out 看稳定性：

```python
leaf_values = [0.01, 0.02, -0.01, 0.00, 0.03]

leave_one_out_means = []
for i in range(len(leaf_values)):
    sample = leaf_values[:i] + leaf_values[i + 1:]
    leave_one_out_means.append(sum(sample) / len(sample))

print(leave_one_out_means)
print(max(leave_one_out_means) - min(leave_one_out_means))
```

结果：

```text
[0.01, 0.0075, 0.015, 0.012499999999999999, 0.004999999999999999]
0.01
```

删掉一个样本后，叶子均值变化范围约 `1%`。

如果叶子只有 2 到 3 个样本，这个波动通常更大。

## 类别不平衡

分类树在类别不平衡时也容易过拟合多数类。

```python
labels = [0] * 95 + [1] * 5

majority_accuracy = labels.count(0) / len(labels)

print(majority_accuracy)
```

结果：

```text
0.95
```

一个永远预测 `0` 的模型准确率就有 `95%`。

所以分类树不能只看 accuracy。

还要看：

- precision。
- recall。
- AUC。
- 分组收益。
- long-short 表现。
- 少数类样本是否足够。

## 树规则的稳定性

单棵树的规则可能很不稳定。

训练数据稍微变化，根节点 split 就可能变。

例如两个特征预测能力接近：

```python
split_gains_run1 = {"momentum": 0.031, "value": 0.030}
split_gains_run2 = {"momentum": 0.029, "value": 0.032}

root_1 = max(split_gains_run1, key=split_gains_run1.get)
root_2 = max(split_gains_run2, key=split_gains_run2.get)

print(root_1)
print(root_2)
```

结果：

```text
momentum
value
```

根节点变化后，整棵树的结构都可能变化。

这也是随机森林比单棵树更稳健的原因之一。

## 量化场景中的参数习惯

没有固定答案，但常见起点是：

```text
max_depth: 小到中等，例如 2 到 6
min_samples_leaf: 根据样本规模设得足够大
min_samples_split: 大于 min_samples_leaf
max_leaf_nodes: 控制规则数量
ccp_alpha: 用验证集选择
```

如果是横截面股票模型，要特别注意：

- 每个日期的样本数。
- 每个叶子是否跨日期稳定。
- 叶子里是否集中在少数行业。
- 是否只学到市值或流动性代理变量。
- 叶子预测扣成本后是否有价值。

## 常见误区

第一，只限制 `max_depth`，不限制 `min_samples_leaf`。

深度不大也可能产生很小的叶子。

第二，用训练集选择树复杂度。

训练集总是偏向更复杂的树。

第三，把单棵树规则当成稳定解释。

单棵树可解释，但不一定稳定。

第四，忽略时间切分。

随机 CV 在金融时序里容易产生乐观估计。

第五，只看 accuracy 或 MSE。

量化里最终要看样本外、扣成本后的收益和风险。

## 小结

决策树过拟合控制的核心是限制树的复杂度。

常用工具包括：

```text
max_depth
min_samples_leaf
min_samples_split
max_leaf_nodes
min_impurity_decrease
ccp_alpha
```

在金融机器学习里，单棵树尤其要小心。

它很容易把噪声切成看似漂亮的规则。

比较可靠的做法是：

```text
用时间序列验证选择复杂度
检查叶子样本数和稳定性
报告样本外 net performance
```
