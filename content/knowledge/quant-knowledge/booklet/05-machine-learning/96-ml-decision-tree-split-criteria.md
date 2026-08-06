# 机器学习：决策树分裂准则的 Gini、entropy、MSE 和 split gain

## 核心概念

决策树是一种按条件递归切分样本的模型。

每个内部节点都问一个问题：

```text
某个特征是否小于等于某个阈值？
```

例如：

```text
volatility <= 0.20 ?
momentum <= 0.05 ?
spread <= 0.001 ?
```

样本被不断分到左子树或右子树，最后落到叶子节点。

叶子节点给出预测：

- 分类树：预测类别或类别概率。
- 回归树：预测目标均值。

决策树训练的核心是：

```text
在每个节点，选择哪个特征和阈值来分裂？
```

这个选择就依赖分裂准则。

## 分裂准则在做什么

一个好的 split 应该让子节点更“纯”。

分类任务里，纯度可以理解为：

```text
一个节点里的样本尽量属于同一类
```

回归任务里，纯度可以理解为：

```text
一个节点里的 y 尽量接近同一个数
```

所以分裂准则通常比较：

```text
分裂前的不纯度
分裂后的加权不纯度
```

如果分裂后不纯度明显下降，这个 split 就更好。

简化公式：

```text
gain = impurity(parent) - weighted_impurity(children)
```

gain 越大，分裂越有价值。

## 分类树：Gini impurity

Gini impurity 衡量一个节点的类别混杂程度。

公式：

```text
Gini = 1 - sum(p_k ** 2)
```

其中 `p_k` 是第 `k` 类的比例。

如果一个节点全是同一类：

```text
Gini = 0
```

如果二分类节点里正负样本各一半：

```text
Gini = 0.5
```

小例子：

```python
def gini(labels):
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    total = len(labels)
    impurity = 1.0
    for count in counts.values():
        p = count / total
        impurity -= p ** 2
    return impurity

print(gini([1, 1, 1, 1]))
print(gini([1, 1, 0, 0]))
```

结果：

```text
0.0
0.5
```

第一个节点完全纯。

第二个节点正负各半，不纯度更高。

## Gini split gain

假设父节点有 6 个样本。

```python
parent = [1, 1, 1, 0, 0, 0]
left = [1, 1, 1]
right = [0, 0, 0]

def weighted_child_gini(left, right):
    n = len(left) + len(right)
    return len(left) / n * gini(left) + len(right) / n * gini(right)

gain = gini(parent) - weighted_child_gini(left, right)

print(gini(parent))
print(weighted_child_gini(left, right))
print(gain)
```

结果：

```text
0.5
0.0
0.5
```

这个分裂把正负样本完全分开。

所以分裂后不纯度为 `0`，gain 很大。

如果换一个较差的 split：

```python
left = [1, 0, 0]
right = [1, 1, 0]

gain = gini(parent) - weighted_child_gini(left, right)

print(weighted_child_gini(left, right))
print(gain)
```

结果：

```text
0.4444444444444444
0.05555555555555558
```

这个 split 没有把类别分干净，gain 很小。

## 分类树：entropy

entropy 也衡量类别混杂程度。

公式：

```text
Entropy = -sum(p_k * log2(p_k))
```

二分类时：

- 全是同一类，entropy 为 `0`。
- 正负各一半，entropy 为 `1`。

```python
import math

def entropy(labels):
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    total = len(labels)
    value = 0.0
    for count in counts.values():
        p = count / total
        value -= p * math.log2(p)
    return value

print(entropy([1, 1, 1, 1]))
print(entropy([1, 1, 0, 0]))
```

结果：

```text
0.0
1.0
```

entropy 和 Gini 经常给出相似的分裂。

Gini 计算更简单，很多实现默认使用 Gini。

## information gain

用 entropy 计算的 split gain 常叫 information gain。

```python
parent = [1, 1, 1, 0, 0, 0]
left = [1, 1, 1]
right = [0, 0, 0]

def weighted_child_entropy(left, right):
    n = len(left) + len(right)
    return len(left) / n * entropy(left) + len(right) / n * entropy(right)

info_gain = entropy(parent) - weighted_child_entropy(left, right)

print(entropy(parent))
print(weighted_child_entropy(left, right))
print(info_gain)
```

结果：

```text
1.0
0.0
1.0
```

完美分裂的信息增益是 `1`。

## 回归树：MSE 分裂准则

回归树没有类别纯度。

它通常让子节点的目标值更集中。

最常见准则是平方误差：

```text
MSE = mean((y_i - mean(y)) ** 2)
```

小例子：

```python
def mse(values):
    avg = sum(values) / len(values)
    return sum((x - avg) ** 2 for x in values) / len(values)

print(mse([1.0, 1.0, 1.0]))
print(mse([1.0, 2.0, 3.0]))
```

结果：

```text
0.0
0.6666666666666666
```

第一个节点所有 y 都相同，误差为 `0`。

第二个节点内部差异更大。

## MSE split gain

假设父节点目标值是：

```python
parent_y = [1.0, 1.2, 1.1, 3.0, 3.2, 2.9]
left_y = [1.0, 1.2, 1.1]
right_y = [3.0, 3.2, 2.9]

def weighted_child_mse(left, right):
    n = len(left) + len(right)
    return len(left) / n * mse(left) + len(right) / n * mse(right)

gain = mse(parent_y) - weighted_child_mse(left_y, right_y)

print(mse(parent_y))
print(weighted_child_mse(left_y, right_y))
print(gain)
```

结果：

```text
0.9455555555555555
0.011111111111111124
0.9344444444444444
```

这个分裂把低收益样本和高收益样本分开。

分裂后每个子节点内部更集中，所以 gain 很大。

## 如何枚举候选 split

训练决策树时，会对特征和阈值做搜索。

简化伪代码：

```python
best_gain = -inf
best_feature = None
best_threshold = None

for feature in features:
    for threshold in candidate_thresholds(feature):
        left, right = split_samples(data, feature, threshold)
        gain = impurity(parent) - weighted_impurity(left, right)

        if gain > best_gain:
            best_gain = gain
            best_feature = feature
            best_threshold = threshold
```

真实实现会做很多工程优化。

但基本思想就是：

```text
找出让不纯度下降最多的特征和阈值
```

## 手写一个阈值搜索

用一个特征 `x` 预测二分类标签 `y`。

```python
x = [0.10, 0.20, 0.35, 0.60, 0.80]
y = [0, 0, 1, 1, 1]

thresholds = [0.15, 0.275, 0.475, 0.70]

best = None
for threshold in thresholds:
    left = [label for value, label in zip(x, y) if value <= threshold]
    right = [label for value, label in zip(x, y) if value > threshold]
    child_impurity = weighted_child_gini(left, right)
    gain = gini(y) - child_impurity

    candidate = (gain, threshold, left, right)
    if best is None or candidate[0] > best[0]:
        best = candidate

print(best)
```

结果：

```text
(0.48, 0.275, [0, 0], [1, 1, 1])
```

阈值 `0.275` 把标签完全分开。

这是这个例子里的最佳 split。

## 多分类情况

Gini 和 entropy 都自然支持多分类。

```python
labels = ["up", "flat", "down", "up", "up", "flat"]

print(gini(labels))
print(entropy(labels))
```

结果：

```text
0.611111111111111
1.4591479170272448
```

类别越分散，不纯度越高。

在量化里，多分类标签可以是：

```text
上涨 / 横盘 / 下跌
高收益组 / 中性组 / 低收益组
买入 / 持有 / 卖出
```

但类别越多，每个叶子里需要更多样本。

## split gain 不等于真实收益

树模型优化的是训练目标。

分类树用 Gini 或 entropy。

回归树用 MSE。

但量化交易最终关心的是：

```text
扣成本后的组合收益和风险
```

一个 split 在训练集上让 Gini 降很多，不代表它一定有交易价值。

原因包括：

- 分裂可能过拟合噪声。
- 标签可能没有扣交易成本。
- split 可能只在某个时间段有效。
- 叶子样本太少，未来不稳定。
- 特征阈值可能来自数据挖掘。

所以树模型分裂准则只是训练机制。

最终仍要用 out-of-sample 表现验证。

## sklearn 中的 criterion

在 sklearn 里，常见参数是 `criterion`。

分类树常见：

```python
DecisionTreeClassifier(criterion="gini")
DecisionTreeClassifier(criterion="entropy")
DecisionTreeClassifier(criterion="log_loss")
```

回归树常见：

```python
DecisionTreeRegressor(criterion="squared_error")
DecisionTreeRegressor(criterion="absolute_error")
```

这里不展开库调用，因为前面 sklearn 章节已经讲过 estimator API。

要记住的是：

```text
criterion 决定每个节点如何评价候选分裂
```

## 和随机森林、GBDT 的关系

随机森林、XGBoost、LightGBM 都建立在树的 split 上。

但它们选择 split 的方式有差异。

简化理解：

```text
单棵决策树：直接降低节点不纯度或误差
随机森林：训练很多棵随机化的树，再平均或投票
GBDT / XGBoost / LightGBM：每棵新树拟合前面模型的残差或梯度
```

GBDT 系列中的 split gain 通常和梯度、Hessian、正则化有关。

伪代码：

```python
for each candidate_split:
    left_grad, left_hess = aggregate_gradient(left_samples)
    right_grad, right_hess = aggregate_gradient(right_samples)
    gain = objective_gain(left_grad, left_hess, right_grad, right_hess, regularization)
```

虽然公式不同，但本质仍是：

```text
选择让目标函数下降最多的 split
```

## 常见误区

第一，认为树模型不需要特征处理。

树不需要标准化，但仍需要处理：

- 缺失值。
- 异常值。
- 时间对齐。
- 未来信息泄露。
- 类别变量编码。

第二，只看训练集 split gain。

训练集 gain 很高可能只是过拟合。

第三，让叶子节点样本太少。

金融数据噪声很大，太小的叶子通常不稳定。

第四，用事后标签或未来统计量做特征。

树模型非常容易利用泄露信息。

第五，把 feature importance 当作稳定因果解释。

树的重要性会受特征相关性、取值尺度和可分裂点数量影响。

## 小结

决策树分裂准则的核心是：

```text
选择一个特征和阈值，让子节点比父节点更纯
```

分类树常用：

```text
Gini impurity
entropy / information gain
```

回归树常用：

```text
MSE / squared error
```

在量化机器学习里，split gain 只是模型内部的优化指标。

真正要验证的是：

```text
分裂学到的关系在样本外是否稳定，扣成本后是否仍然有交易价值
```
