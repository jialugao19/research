# 机器学习：树模型特征重要性的 impurity importance、permutation importance 和解释风险

## 核心概念

树模型特征重要性回答的是：

```text
模型主要依赖哪些特征做预测？
```

对决策树、随机森林、XGBoost、LightGBM 来说，特征重要性很常见。

但它很容易被误读。

重要性高只能说明：

```text
这个模型在这批数据和这个训练方式下，经常使用或依赖这个特征。
```

它不等于：

- 因果关系。
- 稳定 alpha。
- 样本外一定有效。
- 交易后一定赚钱。
- 这个特征单独就有预测力。

在量化里，特征重要性更适合作为诊断工具，而不是最终结论。

## 常见重要性类型

树模型里常见三类重要性：

```text
impurity importance: 看特征带来的分裂增益
permutation importance: 打乱特征后，看模型表现下降多少
drop-column importance: 删除特征重新训练，看表现下降多少
```

不同方法回答的问题不同。

```text
impurity importance:
    训练过程中，哪个特征经常带来 split gain？

permutation importance:
    训练好的模型如果失去某个特征，验证表现会掉多少？

drop-column importance:
    从头训练时，没有这个特征会差多少？
```

不要把它们混为一谈。

## impurity importance

impurity importance 也叫 split gain importance。

基本思想：

```text
某个特征用于 split 时，如果让不纯度或损失下降很多，就给它记功。
```

简化例子：

```python
split_gains = [
    ("momentum", 0.12),
    ("value", 0.05),
    ("momentum", 0.08),
    ("size", 0.03),
]

importance = {}
for feature, gain in split_gains:
    importance[feature] = importance.get(feature, 0.0) + gain

print(importance)
```

结果：

```text
{'momentum': 0.2, 'value': 0.05, 'size': 0.03}
```

`momentum` 被用于两次 split，总 gain 最高。

所以它的重要性最高。

## 归一化重要性

很多库会把重要性归一化，让总和为 `1`。

```python
importance = {"momentum": 0.20, "value": 0.05, "size": 0.03}

total = sum(importance.values())
normalized = {
    feature: value / total
    for feature, value in importance.items()
}

print(normalized)
```

结果：

```text
{'momentum': 0.7142857142857143, 'value': 0.17857142857142858, 'size': 0.10714285714285714}
```

这表示在这个模型的 split gain 里，`momentum` 贡献了约 `71.4%`。

但这个数字不是收益贡献。

它只是模型训练过程中累计 gain 的比例。

## frequency importance

有些实现还会报告 split 次数。

```python
split_features = ["momentum", "value", "momentum", "size", "momentum"]

frequency = {}
for feature in split_features:
    frequency[feature] = frequency.get(feature, 0) + 1

print(frequency)
```

结果：

```text
{'momentum': 3, 'value': 1, 'size': 1}
```

split 次数多，不一定说明特征真的更有价值。

一个特征可能被频繁用于小 gain 的 split。

另一个特征可能很少使用，但每次 gain 很大。

所以要区分：

```text
split frequency
split gain
permutation impact
```

## permutation importance

permutation importance 的思路是：

```text
保持标签和其他特征不变，只打乱某个特征。
如果模型表现大幅下降，说明模型依赖这个特征。
```

简化例子：

```python
baseline_score = 0.08
score_after_permutation = {
    "momentum": 0.03,
    "value": 0.06,
    "size": 0.079,
}

permutation_importance = {
    feature: baseline_score - score
    for feature, score in score_after_permutation.items()
}

print(permutation_importance)
```

结果：

```text
{'momentum': 0.05, 'value': 0.020000000000000004, 'size': 0.0010000000000000009}
```

打乱 `momentum` 后，score 从 `0.08` 降到 `0.03`。

下降最大，所以模型最依赖它。

## permutation 要在验证集上做

permutation importance 应该在验证集或测试集上算。

不要只在训练集上算。

训练集上的重要性可能反映过拟合。

伪代码：

```python
baseline_score = evaluate(model, valid_x, valid_y)

for feature in features:
    shuffled_x = valid_x.copy()
    shuffled_x[feature] = shuffle(shuffled_x[feature])
    shuffled_score = evaluate(model, shuffled_x, valid_y)
    importance[feature] = baseline_score - shuffled_score
```

在量化里，验证集还应该按时间切分。

如果用随机验证集，仍可能高估重要性稳定性。

## drop-column importance

drop-column importance 是删除一个特征后重新训练模型。

```text
importance(feature) = baseline_score - score_without_feature
```

小例子：

```python
baseline_score = 0.075
score_without_feature = {
    "momentum": 0.040,
    "value": 0.060,
    "size": 0.074,
}

drop_column_importance = {
    feature: baseline_score - score
    for feature, score in score_without_feature.items()
}

print(drop_column_importance)
```

结果：

```text
{'momentum': 0.034999999999999996, 'value': 0.014999999999999999, 'size': 0.000999999999999987}
```

drop-column 更接近：

```text
没有这个特征，整个训练流程会损失多少？
```

但它计算很贵。

每个特征都要重新训练一次模型。

## 相关特征会分摊重要性

如果两个特征高度相关，重要性可能被分摊。

例如 `momentum_20d` 和 `momentum_21d` 几乎一样。

模型用哪个都可以。

```python
importance = {
    "momentum_20d": 0.12,
    "momentum_21d": 0.10,
    "value": 0.04,
}

momentum_group_importance = importance["momentum_20d"] + importance["momentum_21d"]

print(momentum_group_importance)
```

结果：

```text
0.22
```

如果只看单个特征，`momentum_20d` 似乎只是 `0.12`。

但整个 momentum 特征族加起来是 `0.22`。

所以解释时常常要按特征组看。

## 替代特征问题

如果一个特征被删除，模型可能用相似特征替代它。

这会让 drop-column importance 看起来偏低。

```python
baseline_score = 0.080
score_without_momentum_20d = 0.076
score_without_all_momentum = 0.050

single_drop_loss = baseline_score - score_without_momentum_20d
group_drop_loss = baseline_score - score_without_all_momentum

print(single_drop_loss)
print(group_drop_loss)
```

结果：

```text
0.0040000000000000036
0.03
```

删除一个 momentum 特征影响不大。

但删除整个 momentum 特征族，影响很大。

这是相关特征解释中的常见现象。

## 高基数特征偏差

impurity importance 对取值种类多的特征可能有偏。

原因是：

```text
可选 split 越多，越容易偶然找到训练集 gain 高的 split。
```

例如：

- 连续变量通常有很多候选阈值。
- 高基数类别变量可能有很多切法。
- 随机 ID 如果处理不当，也可能看起来重要。

小例子：

```python
candidate_splits = {
    "sector": 10,
    "stock_id": 1000,
    "momentum": 80,
}

most_split_options = max(candidate_splits, key=candidate_splits.get)

print(most_split_options)
```

结果：

```text
stock_id
```

`stock_id` 的候选切分很多。

它可能在训练集里制造看似有效的规则。

这不代表它有稳定预测能力。

## 泄露特征会显得极其重要

如果某个特征含有未来信息，树模型会非常容易发现它。

```python
importance = {
    "future_return_1d": 0.90,
    "momentum": 0.05,
    "value": 0.03,
    "size": 0.02,
}

top_feature = max(importance, key=importance.get)

print(top_feature)
```

结果：

```text
future_return_1d
```

如果你看到某个特征重要性异常高，要先怀疑：

- 是否使用了未来收益。
- 是否使用了未来成分股。
- 是否使用了事后修正数据。
- 是否标签和特征没有正确 shift。
- 是否在全样本上做了标准化或分位数。

高重要性不一定是好消息。

它可能是泄露警报。

## 稳定性比单次排名更重要

不要只看一次训练的 feature importance。

应该看多个时间窗口、多个随机种子下的重要性是否稳定。

```python
rankings = [
    ["momentum", "value", "quality"],
    ["momentum", "quality", "value"],
    ["value", "momentum", "quality"],
]

top1_count = {}
for ranking in rankings:
    top1 = ranking[0]
    top1_count[top1] = top1_count.get(top1, 0) + 1

print(top1_count)
```

结果：

```text
{'momentum': 2, 'value': 1}
```

`momentum` 多数时候排第一，但不是每次都排第一。

如果排名经常大幅变化，说明解释不稳定。

## Jaccard 检查 top-k 稳定性

可以比较不同训练结果的 top-k 特征集合。

```python
top3_a = {"momentum", "value", "quality"}
top3_b = {"momentum", "quality", "low_vol"}

jaccard = len(top3_a & top3_b) / len(top3_a | top3_b)

print(jaccard)
```

结果：

```text
0.5
```

两个 top-3 集合只有 2 个共同特征。

Jaccard 是：

```text
2 / 4 = 0.5
```

这说明 top 特征有一定重合，但不算非常稳定。

## 分组重要性

量化特征常常成组出现。

例如：

```text
momentum: momentum_5d, momentum_20d, momentum_60d
value: pe, pb, ev_ebitda
quality: roe, gross_margin, accruals
liquidity: turnover, volume, spread
```

可以把单个特征重要性合并到特征组。

```python
feature_to_group = {
    "momentum_5d": "momentum",
    "momentum_20d": "momentum",
    "pe": "value",
    "turnover": "liquidity",
}

importance = {
    "momentum_5d": 0.08,
    "momentum_20d": 0.12,
    "pe": 0.05,
    "turnover": 0.03,
}

group_importance = {}
for feature, value in importance.items():
    group = feature_to_group[feature]
    group_importance[group] = group_importance.get(group, 0.0) + value

print(group_importance)
```

结果：

```text
{'momentum': 0.2, 'value': 0.05, 'liquidity': 0.03}
```

分组后解释更贴近研究问题。

## 重要性和方向不同

树模型重要性通常不告诉你方向。

一个特征重要，只表示模型依赖它。

但它可能是：

```text
特征越高，预测越高
特征越高，预测越低
只有中间区间有效
和另一个特征交互后才有效
```

所以 feature importance 不能回答：

```text
这个因子是正向还是负向？
```

要看方向，可以结合：

- 分组收益。
- partial dependence。
- ICE curve。
- SHAP。
- 单变量 IC。
- 领域逻辑。

## 和全局 feature importance 的关系

outline 里后面还有单独的 `feature importance` 知识点。

这里讲的是树模型特有的重要性机制。

后面更通用的 feature importance 会再覆盖：

- permutation importance 的一般形式。
- SHAP / PDP / ICE 的解释思路。
- 线性模型系数解释。
- 不同模型之间的重要性比较。
- 解释稳定性和因果误读。

所以本篇重点是：

```text
树模型为什么会给出重要性，以及这些重要性有哪些坑。
```

## 实战检查清单

看树模型 feature importance 时，至少检查：

- 是 impurity、gain、frequency、permutation 还是 drop-column？
- 是否在验证集上计算？
- 是否按时间切分验证？
- 重要性在不同年份是否稳定？
- 重要性在不同随机种子下是否稳定？
- 是否有高度相关特征分摊重要性？
- 是否按特征组聚合过？
- 是否有高基数特征偏差？
- top 特征是否可能泄露未来？
- 重要性高的特征扣成本后是否真的有交易价值？

## 常见误区

第一，把 feature importance 当作因果解释。

第二，只看训练集 impurity importance。

第三，忽略相关特征导致的重要性分摊。

第四，用一次训练的排名做强结论。

第五，看到泄露特征很重要却误以为发现了强 alpha。

第六，用重要性判断方向。

第七，不按时间、regime、股票池检查稳定性。

## 小结

树模型特征重要性是有用的诊断工具。

但它回答的是：

```text
模型在这个训练流程里依赖了哪些特征？
```

而不是：

```text
哪些特征有稳定因果关系？
哪些特征一定能赚钱？
```

在量化机器学习里，比较可靠的做法是：

```text
用验证集 permutation importance
按时间窗口检查稳定性
按特征组聚合解释
排查泄露和高基数偏差
最后用样本外净收益验证交易价值
```
