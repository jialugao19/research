# 机器学习：随机森林的 bagging、特征随机子采样、OOB 评估和稳定性

## 核心概念

随机森林是很多棵决策树组成的 ensemble。

它的基本思想是：

```text
单棵树很容易过拟合，也很不稳定。
训练很多棵不同的树，再把结果平均或投票，可以降低方差。
```

随机森林中的“随机”主要来自两处：

- 每棵树使用 bootstrap 抽样得到的不同训练样本。
- 每个节点分裂时只看一部分随机选择的特征。

所以随机森林不是简单复制很多棵一样的树。

它刻意让树之间有差异，然后用集成降低单棵树的噪声。

## bagging

bagging 是 bootstrap aggregating。

步骤：

```text
1. 从训练集有放回抽样，得到一个 bootstrap 样本。
2. 在这个样本上训练一棵树。
3. 重复很多次。
4. 分类任务投票，回归任务平均。
```

有放回抽样意味着：

```text
同一个样本可能被抽到多次，也可能一次都没被抽到。
```

小例子：

```python
import random

data = ["A", "B", "C", "D", "E"]

random.seed(7)
bootstrap_sample = [
    random.choice(data)
    for _ in range(len(data))
]

print(bootstrap_sample)
```

结果：

```text
['C', 'B', 'D', 'A', 'A']
```

`A` 出现了两次，`E` 没有出现。

这就是 bootstrap 样本。

## 为什么 bagging 能降低方差

单棵树对训练数据非常敏感。

如果不同树的误差不完全相同，平均后波动会下降。

简化例子：三棵回归树对同一个样本的预测：

```python
tree_predictions = [0.03, 0.01, 0.02]

forest_prediction = sum(tree_predictions) / len(tree_predictions)

print(forest_prediction)
```

结果：

```text
0.02
```

单棵树可能偏高或偏低。

平均后结果更平滑。

如果树之间高度相关，平均的好处会变小。

所以随机森林不仅 bootstrap 样本，还随机抽特征。

## 分类投票

分类随机森林通常用多数投票。

```python
tree_votes = ["buy", "hold", "buy", "sell", "buy"]

counts = {}
for vote in tree_votes:
    counts[vote] = counts.get(vote, 0) + 1

final_vote = max(counts, key=counts.get)

print(counts)
print(final_vote)
```

结果：

```text
{'buy': 3, 'hold': 1, 'sell': 1}
buy
```

五棵树里三棵投 `buy`，最终分类为 `buy`。

也可以把票数转成概率：

```python
prob_buy = counts["buy"] / len(tree_votes)

print(prob_buy)
```

结果：

```text
0.6
```

这可以作为分类置信度的粗略估计。

## 回归平均

回归随机森林通常对每棵树预测取平均。

```python
tree_predictions = [0.012, 0.018, 0.006, 0.014]

prediction = sum(tree_predictions) / len(tree_predictions)

print(prediction)
```

结果：

```text
0.0125
```

在量化里，这个预测可能是：

- 未来收益。
- 超额收益。
- 风险调整收益。
- 某个 alpha score。

平均可以降低单棵树的极端预测。

## 特征随机子采样

随机森林在每个 split 处不会看全部特征。

它会随机抽一部分特征作为候选。

这样做的目的：

```text
降低树之间的相关性
```

如果每棵树每个节点都看全部特征，那么最强特征可能总是被选中。

很多树会长得很像。

小例子：

```python
import random

features = ["momentum", "value", "size", "quality", "volatility"]

random.seed(3)
candidate_features = random.sample(features, 3)

print(candidate_features)
```

结果：

```text
['value', 'volatility', 'quality']
```

这个节点只在这 3 个特征里寻找最佳 split。

下一个节点会重新随机抽一组特征。

## max_features

`max_features` 控制每次 split 看到多少特征。

常见设置：

```text
分类：sqrt(n_features)
回归：n_features / 3 或 sqrt(n_features)
```

简化计算：

```python
import math

n_features = 25

sqrt_features = int(math.sqrt(n_features))
third_features = n_features // 3

print(sqrt_features)
print(third_features)
```

结果：

```text
5
8
```

`max_features` 越小，树之间差异越大。

但单棵树可能变弱。

`max_features` 越大，单棵树更强，但树之间更相似。

## bootstrap 中的 OOB 样本

OOB 是 out-of-bag。

对某一棵树来说，没有被它的 bootstrap 样本抽到的训练样本，就是这棵树的 OOB 样本。

这些样本没有参与这棵树训练，可以用来估计样本外误差。

小例子：

```python
data = list(range(6))
bootstrap_sample = [0, 1, 1, 3, 3, 5]

in_bag = set(bootstrap_sample)
oob = [
    item
    for item in data
    if item not in in_bag
]

print(oob)
```

结果：

```text
[2, 4]
```

样本 `2` 和 `4` 没被这棵树抽到。

它们可以用来评估这棵树。

## OOB 覆盖率

当样本数足够大时，一个样本在一次 bootstrap 中没被抽到的概率约为：

```text
(1 - 1/n) ** n ≈ exp(-1) ≈ 36.8%
```

小例子：

```python
import math

n = 100
oob_probability = (1 - 1 / n) ** n

print(oob_probability)
print(math.exp(-1))
```

结果：

```text
0.3660323412732292
0.36787944117144233
```

所以每棵树大约有三分之一训练样本是 OOB。

随机森林可以把每个样本在 OOB 树上的预测汇总起来，得到 OOB score。

## OOB 预测

假设某个样本没有参与三棵树的训练。

这三棵树对它的预测是：

```python
oob_predictions = [0.01, 0.03, 0.02]
oob_prediction = sum(oob_predictions) / len(oob_predictions)

print(oob_prediction)
```

结果：

```text
0.02
```

用 OOB 预测和真实标签比较，就可以估计泛化误差。

OOB 不是时间序列验证的替代品。

在金融数据中，最终仍要做按时间切分的样本外验证。

但 OOB 可以作为训练阶段的辅助诊断。

## 随机森林和单棵树对比

单棵树：

- 解释直观。
- 容易可视化。
- 方差高。
- 对样本扰动敏感。
- 过拟合风险大。

随机森林：

- 更稳健。
- 方差更低。
- 通常样本外表现更好。
- 解释性弱于单棵树。
- 预测速度和内存成本更高。

简化对比：

```python
single_tree_scores = [0.04, -0.01, 0.06, -0.03]
forest_scores = [0.02, 0.01, 0.03, 0.00]

def value_range(values):
    return max(values) - min(values)

print(value_range(single_tree_scores))
print(value_range(forest_scores))
```

结果：

```text
0.09
0.03
```

随机森林结果波动更小。

## 树的数量

`n_estimators` 控制森林里有多少棵树。

树越多，平均结果越稳定。

但计算成本也越高。

小例子：随着树数量增加，预测均值逐渐稳定。

```python
tree_predictions = [0.03, 0.01, 0.02, 0.00, 0.025]

running_means = []
for i in range(1, len(tree_predictions) + 1):
    running_means.append(sum(tree_predictions[:i]) / i)

print(running_means)
```

结果：

```text
[0.03, 0.02, 0.02, 0.015, 0.017]
```

树数量太少时，结果仍可能受个别树影响。

树数量足够后，继续增加树通常收益递减。

## 随机森林的主要参数

常见参数包括：

```text
n_estimators: 树的数量
max_depth: 单棵树最大深度
min_samples_leaf: 叶子最小样本数
max_features: 每次 split 可用特征数
bootstrap: 是否 bootstrap 抽样
oob_score: 是否计算 OOB 分数
class_weight: 分类任务的类别权重
random_state: 随机种子
```

伪代码：

```python
model = RandomForestRegressor(
    n_estimators=500,
    max_depth=5,
    min_samples_leaf=50,
    max_features="sqrt",
    bootstrap=True,
    oob_score=True,
    random_state=7,
)
```

金融数据里，`min_samples_leaf` 和时间序列验证非常重要。

不要因为随机森林比单棵树稳健，就放任单棵树长得很深。

## 随机森林的特征重要性

随机森林可以输出特征重要性。

常见有两种：

```text
impurity importance: 看每个特征带来的分裂增益
permutation importance: 打乱某个特征，看模型表现下降多少
```

但特征重要性要谨慎解释。

问题包括：

- 相关特征会互相分摊重要性。
- 取值种类多的特征可能更容易被 split 选中。
- 重要性不等于因果关系。
- 时序泄露特征可能显得极其重要。

树模型特征重要性后面会单独写一篇。

这里先记住：

```text
随机森林的重要性是模型内部诊断，不是稳定因果解释。
```

## 随机森林在量化中的优点

优点：

- 能捕捉非线性。
- 能捕捉特征交互。
- 不要求特征标准化。
- 对异常值比线性模型更不敏感。
- 比单棵树更稳健。
- 可以处理高维特征。

例如：

```text
低波动 + 高动量
高换手 + 小市值
低估值 + 高质量
```

这些交互关系，线性模型需要手动构造交互项。

随机森林可以通过树结构自动表达一部分。

## 随机森林在量化中的风险

风险：

- 仍然可能过拟合。
- 预测不容易外推。
- 特征重要性可能不稳定。
- 模型较大，解释困难。
- 在非平稳市场中，历史关系可能失效。
- 如果标签和特征对齐错了，森林会很快学到泄露。

尤其注意：

```text
随机森林不能解决未来信息泄露。
```

如果特征里混入未来数据，随机森林会非常有效地利用它。

回测结果会虚高。

## 时间序列验证仍然必要

OOB score 来自 bootstrap 抽样。

它不是严格时间样本外。

金融建模仍然应该做：

```text
train: 2016-2018, valid: 2019
train: 2017-2019, valid: 2020
train: 2018-2020, valid: 2021
```

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    model = RandomForestRegressor(params)
    model.fit(features[train_period], labels[train_period])
    pred = model.predict(features[valid_period])
    score = evaluate_net_performance(pred, labels[valid_period], costs[valid_period])
```

最终选择参数时，应该看：

- 样本外 IC / RankIC。
- 分组收益。
- long-short 收益。
- turnover。
- 扣成本后收益。
- 分 regime 稳定性。

## 常见误区

第一，认为随机森林不会过拟合。

随机森林降低方差，但不是免疫过拟合。

第二，只看 OOB score，不做时间样本外验证。

第三，把 `n_estimators` 调得很大，却不控制单棵树复杂度。

第四，把 feature importance 当作因果解释。

第五，不设随机种子，结果难以复现。

第六，在高度相关的特征上过度解读重要性排名。

第七，忽略交易成本和换手。

## 小结

随机森林通过两类随机性提高稳定性：

```text
bootstrap 样本随机
split 特征随机
```

它把很多棵高方差的树做平均或投票，从而降低单棵树的不稳定性。

在金融机器学习里，随机森林是很实用的非线性基线。

但它仍然需要：

```text
控制单棵树复杂度
使用时间序列验证
检查特征泄露
报告扣成本后的样本外表现
谨慎解释特征重要性
```
