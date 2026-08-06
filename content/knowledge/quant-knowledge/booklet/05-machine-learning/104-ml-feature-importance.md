# Feature Importance

## 核心概念

feature importance 是特征重要性。

它想回答：

```text
模型预测主要受哪些特征影响？
```

但不同方法回答的问题不一样。

常见问题包括：

- 哪些特征让模型表现下降最多？
- 哪些特征系数最大？
- 哪些特征改变后，预测变化最大？
- 哪些特征在不同时间窗口里稳定重要？
- 哪些特征只是和其他特征一起重要？
- 哪些特征可能泄露了未来信息？

所以 feature importance 不是一个单一指标。

它是一组解释工具。

## 为什么要做 feature importance

在量化机器学习里，feature importance 常用于：

- 排查泄露。
- 解释模型行为。
- 做特征筛选。
- 比较不同模型依赖的信号。
- 判断复杂模型是否只学到了少数代理变量。
- 检查信号是否符合经济直觉。
- 检查样本外稳定性。

但要记住：

```text
重要性不等于因果。
重要性不等于可交易。
重要性不等于样本外稳定。
```

一个特征很重要，只说明模型在某个训练流程里依赖它。

是否有交易价值，还要看样本外净收益。

## 方法分类

常见 feature importance 方法可以分成几类：

```text
模型内部方法:
    线性模型系数
    树模型 impurity / gain importance

模型无关方法:
    permutation importance
    drop-column importance

局部解释方法:
    SHAP
    LIME

响应曲线方法:
    PDP
    ICE
```

第 100 篇已经讲过树模型内部重要性。

本篇重点是更通用的方法。

## 线性模型系数

线性模型的预测是：

```text
prediction = b + w_1 x_1 + ... + w_p x_p
```

如果特征已经标准化，系数绝对值可以粗略表示影响大小。

```python
weights = {
    "momentum": 0.04,
    "value": -0.02,
    "quality": 0.01,
}

importance = {
    feature: abs(weight)
    for feature, weight in weights.items()
}

print(importance)
```

结果：

```text
{'momentum': 0.04, 'value': 0.02, 'quality': 0.01}
```

这里 `momentum` 的绝对系数最大。

但系数解释有前提：

- 特征尺度要可比。
- 特征不能严重共线。
- 模型形式要合适。
- 系数稳定性要检查。

## 系数方向

线性模型系数还能给方向。

```python
weights = {
    "momentum": 0.04,
    "value": -0.02,
    "quality": 0.01,
}

directions = {
    feature: "positive" if weight > 0 else "negative"
    for feature, weight in weights.items()
}

print(directions)
```

结果：

```text
{'momentum': 'positive', 'value': 'negative', 'quality': 'positive'}
```

但这仍然不是因果方向。

它只是：

```text
在其他特征不变的线性模型里，这个特征的条件方向。
```

如果特征高度相关，方向可能随训练窗口变化。

## permutation importance

permutation importance 是模型无关方法。

思路：

```text
先计算 baseline score。
然后打乱某个特征，重新算 score。
score 下降越多，特征越重要。
```

小例子：

```python
baseline_score = 0.12
permuted_scores = {
    "momentum": 0.05,
    "value": 0.09,
    "quality": 0.115,
}

importance = {
    feature: baseline_score - score
    for feature, score in permuted_scores.items()
}

print(importance)
```

结果：

```text
{'momentum': 0.06999999999999999, 'value': 0.03, 'quality': 0.0050000000000000044}
```

打乱 `momentum` 后 score 下降最多。

说明模型最依赖它。

## permutation 的优点

permutation importance 的优点：

- 适用于任何模型。
- 不依赖模型内部结构。
- 可以在验证集或测试集上计算。
- 直接衡量对评估指标的影响。

它可以用于：

```text
线性模型
树模型
SVM
神经网络
集成模型
```

只要模型能预测，就能打乱特征后重算指标。

## permutation 的问题

permutation 也有问题。

第一，相关特征会互相替代。

如果 `momentum_20d` 和 `momentum_21d` 高度相关，打乱一个特征时，另一个特征仍然提供类似信息。

重要性可能被低估。

```python
baseline_score = 0.10
score_shuffle_one = 0.095
score_shuffle_group = 0.060

one_feature_loss = baseline_score - score_shuffle_one
group_loss = baseline_score - score_shuffle_group

print(one_feature_loss)
print(group_loss)
```

结果：

```text
0.0050000000000000044
0.04000000000000001
```

打乱一个 momentum 特征影响很小。

但打乱整个 momentum 特征组，影响很大。

第二，打乱特征可能产生不真实的样本。

例如：

```text
低市值 + 超高流动性 + 极低 spread
```

这种组合可能在真实市场中很少出现。

打乱后模型表现下降，部分原因可能是样本变得不自然。

## drop-column importance

drop-column importance 是删除特征后重新训练模型。

```text
importance(feature) = baseline_score - score_without_feature
```

小例子：

```python
baseline_score = 0.11
score_without = {
    "momentum": 0.07,
    "value": 0.10,
    "quality": 0.105,
}

drop_importance = {
    feature: baseline_score - score
    for feature, score in score_without.items()
}

print(drop_importance)
```

结果：

```text
{'momentum': 0.039999999999999994, 'value': 0.009999999999999995, 'quality': 0.0050000000000000044}
```

它回答的是：

```text
如果整个训练流程都没有这个特征，会损失多少表现？
```

## drop-column 的代价

drop-column 更接近完整实验。

但代价很高：

```text
每删除一个特征，都要重新训练一次模型。
```

如果有 500 个特征，就要训练 501 次。

而且训练随机性会影响结果。

真实项目里常用折中方案：

- 按特征组 drop。
- 只对候选 top 特征 drop。
- 固定 random seed。
- 用多个时间切分取均值。

## group importance

量化特征经常成组。

比如：

```text
momentum_5d, momentum_20d, momentum_60d
value_pe, value_pb
liquidity_turnover, liquidity_spread
```

按组看重要性通常更稳定。

```python
feature_importance = {
    "momentum_5d": 0.03,
    "momentum_20d": 0.04,
    "value_pe": 0.02,
    "liquidity_spread": 0.01,
}

feature_group = {
    "momentum_5d": "momentum",
    "momentum_20d": "momentum",
    "value_pe": "value",
    "liquidity_spread": "liquidity",
}

group_importance = {}
for feature, value in feature_importance.items():
    group = feature_group[feature]
    group_importance[group] = group_importance.get(group, 0.0) + value

print(group_importance)
```

结果：

```text
{'momentum': 0.07, 'value': 0.02, 'liquidity': 0.01}
```

这比单个特征排名更容易解释。

## SHAP 直觉

SHAP 是一种局部解释方法。

它把某个样本的预测拆成：

```text
prediction = baseline + feature_contribution_1 + ... + feature_contribution_p
```

其中每个 contribution 表示某个特征把预测从 baseline 推高或拉低多少。

简化例子：

```python
baseline = 0.01
shap_values = {
    "momentum": 0.03,
    "value": -0.01,
    "quality": 0.02,
}

prediction = baseline + sum(shap_values.values())

print(prediction)
```

结果：

```text
0.05
```

这里：

- baseline 是 `0.01`。
- momentum 把预测推高 `0.03`。
- value 把预测拉低 `0.01`。
- quality 把预测推高 `0.02`。

最终预测是 `0.05`。

## 全局 SHAP importance

局部 SHAP 可以聚合成全局重要性。

常见做法是取平均绝对值。

```python
shap_by_sample = [
    {"momentum": 0.03, "value": -0.01},
    {"momentum": 0.02, "value": 0.00},
    {"momentum": -0.04, "value": 0.02},
]

features = ["momentum", "value"]

mean_abs_shap = {}
for feature in features:
    mean_abs_shap[feature] = sum(
        abs(row[feature])
        for row in shap_by_sample
    ) / len(shap_by_sample)

print(mean_abs_shap)
```

结果：

```text
{'momentum': 0.03, 'value': 0.01}
```

这表示 `momentum` 对单个样本预测的平均影响更大。

## SHAP 的注意点

SHAP 很有用，但也要谨慎。

注意：

- SHAP 解释的是模型，不是世界。
- 高 SHAP 不等于因果影响。
- 相关特征会影响归因分配。
- background data 选择会影响结果。
- 样本外稳定性仍然要检查。
- 金融数据中要特别排查泄露特征。

在量化里，SHAP 更适合回答：

```text
这个模型为什么给这个股票/日期较高分？
```

而不是直接证明：

```text
这个因子一定有效。
```

## PDP

PDP 是 partial dependence plot。

它看的是：

```text
把某个特征固定到不同值，模型平均预测如何变化？
```

简化例子：

```python
def model_predict(momentum, value):
    return 0.02 * momentum - 0.01 * value

data = [
    {"momentum": 0.0, "value": 1.0},
    {"momentum": 0.0, "value": 2.0},
    {"momentum": 0.0, "value": 3.0},
]

pdp = {}
for fixed_momentum in [0.0, 1.0, 2.0]:
    predictions = [
        model_predict(fixed_momentum, row["value"])
        for row in data
    ]
    pdp[fixed_momentum] = sum(predictions) / len(predictions)

print(pdp)
```

结果：

```text
{0.0: -0.02, 1.0: 5.782411586589357e-19, 2.0: 0.02}
```

这里 momentum 越高，平均预测越高。

## ICE

ICE 是 individual conditional expectation。

PDP 看平均曲线。

ICE 看每个样本自己的曲线。

```python
def model_predict(momentum, value):
    return 0.02 * momentum - 0.01 * value

rows = [
    {"id": "A", "value": 1.0},
    {"id": "B", "value": 3.0},
]

ice = {}
for row in rows:
    curve = []
    for fixed_momentum in [0.0, 1.0, 2.0]:
        curve.append(model_predict(fixed_momentum, row["value"]))
    ice[row["id"]] = curve

print(ice)
```

结果：

```text
{'A': [-0.01, 0.01, 0.03], 'B': [-0.03, -0.009999999999999998, 0.010000000000000002]}
```

ICE 可以发现不同样本的响应是否一致。

如果 ICE 曲线方向差异很大，说明存在交互或非线性。

## PDP 的问题

PDP 会把特征固定到某个值，再和其他特征组合。

如果特征高度相关，PDP 可能制造不真实组合。

例如：

```text
极低市值 + 极高机构持仓 + 极低流动性
```

这些组合在真实数据里可能很少见。

所以 PDP 在相关特征上要谨慎。

可以结合：

- ICE。
- 分位数范围限制。
- 条件 PDP。
- 分组分析。
- 业务逻辑。

## 稳定性检查

feature importance 不能只看一次。

要看它是否跨时间稳定。

```python
importance_by_year = {
    2020: {"momentum": 0.04, "value": 0.02},
    2021: {"momentum": 0.03, "value": 0.025},
    2022: {"momentum": -0.01, "value": 0.03},
}

momentum_signs = [
    1 if values["momentum"] > 0 else -1
    for values in importance_by_year.values()
]

positive_ratio = sum(sign > 0 for sign in momentum_signs) / len(momentum_signs)

print(momentum_signs)
print(positive_ratio)
```

结果：

```text
[1, 1, -1]
0.6666666666666666
```

`momentum` 有一年方向变负。

这说明它的解释稳定性需要进一步检查。

## 排名稳定性

也可以看 top-k 特征集合是否稳定。

```python
top_features_a = {"momentum", "value", "quality"}
top_features_b = {"momentum", "quality", "liquidity"}

jaccard = len(top_features_a & top_features_b) / len(top_features_a | top_features_b)

print(jaccard)
```

结果：

```text
0.5
```

两个 top-3 集合重合 2 个，合并后共有 4 个。

Jaccard 是 `0.5`。

如果多个窗口的 Jaccard 很低，说明重要性排名不稳定。

## 泄露排查

feature importance 是排查泄露的好工具。

如果某个特征异常重要，要先问：

```text
这个特征在预测时点真的可见吗？
```

常见泄露特征：

- future return。
- 未来波动率。
- 未来成交量。
- 事后修正基本面。
- 未来成分股。
- 全样本标准化后的分位数。
- 用测试集选择出来的特征。

简化检查：

```python
top_features = ["future_return_5d", "momentum", "value"]

leakage_flags = [
    feature
    for feature in top_features
    if "future" in feature
]

print(leakage_flags)
```

结果：

```text
['future_return_5d']
```

如果 top 特征里出现这种名字，要优先排查。

## 解释和交易价值

高重要性不代表可交易。

还要看：

- 预测 horizon 是否匹配。
- 换手是否过高。
- 成本是否覆盖。
- 分组收益是否单调。
- long-short 是否稳定。
- 是否只在某个 regime 有效。

小例子：

```python
gross_alpha = 0.004
turnover_cost = 0.006

net_alpha = gross_alpha - turnover_cost

print(net_alpha)
print(net_alpha > 0)
```

结果：

```text
-0.002
False
```

即使特征重要，交易后也可能没有价值。

## 实战检查清单

做 feature importance 时，至少检查：

- 方法是哪一种：系数、permutation、drop-column、SHAP、PDP/ICE？
- 是否在时间验证集上计算？
- 是否按年份、regime、股票池检查稳定性？
- 是否考虑相关特征和特征组？
- 是否排查未来信息泄露？
- 是否解释了方向，而不只是强度？
- 是否和分组收益、IC、净收益一致？
- 是否考虑交易成本和换手？
- 是否只是在解释模型，而不是误当成因果结论？

## 常见误区

第一，把 feature importance 当成因果关系。

第二，只看训练集重要性。

第三，用一次训练结果做强结论。

第四，忽略特征相关性。

第五，忽略标准化对线性系数的影响。

第六，PDP 用在高度相关特征上却不检查不真实组合。

第七，高重要性特征不做泄露排查。

第八，不看扣成本后的交易价值。

## 小结

feature importance 是模型诊断和解释工具。

不同方法回答不同问题：

```text
线性系数：线性模型中方向和强度如何？
permutation：打乱特征后验证表现下降多少？
drop-column：没有这个特征重新训练会差多少？
SHAP：单个预测由哪些特征推高或拉低？
PDP/ICE：特征变化时模型预测如何响应？
```

在量化机器学习里，可靠解释需要同时满足：

```text
样本外计算
时间稳定
无未来信息泄露
符合经济直觉
扣成本后仍有价值
```
