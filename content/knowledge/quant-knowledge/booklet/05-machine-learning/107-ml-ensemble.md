# 107. 机器学习：ensemble 的 bagging、boosting、stacking、blending 和模型组合风险

## 核心概念

ensemble 是集成学习。

它的核心思想是：

```text
把多个模型组合起来，希望整体比单个模型更稳健。
```

单个模型可能有偏差、方差或特定 regime 下失效。

多个模型如果错误不完全相同，组合后可能：

- 降低波动。
- 提高样本外稳定性。
- 捕捉不同类型信号。
- 降低单模型失效风险。

但 ensemble 也会带来新风险：

- 复杂度更高。
- 更难解释。
- 更容易调参过拟合。
- stacking 容易泄露。
- 多个模型可能其实高度相关。

## 平均集成

最简单的 ensemble 是平均预测。

```python
predictions = [0.03, 0.01, 0.02]

ensemble_pred = sum(predictions) / len(predictions)

print(ensemble_pred)
```

结果：

```text
0.02
```

如果三个模型都在预测未来收益，平均后得到一个更平滑的预测。

平均集成适合：

- 模型表现接近。
- 模型错误不完全相关。
- 不想引入额外调参。

## 加权平均

如果模型质量不同，可以用加权平均。

```python
predictions = {
    "linear": 0.01,
    "tree": 0.03,
    "boosting": 0.02,
}

weights = {
    "linear": 0.2,
    "tree": 0.3,
    "boosting": 0.5,
}

ensemble_pred = sum(
    predictions[name] * weights[name]
    for name in predictions
)

print(ensemble_pred)
```

结果：

```text
0.020999999999999998
```

权重越高，模型对最终预测影响越大。

权重要用验证集选择，不能用测试集事后调。

## 权重归一化

权重通常需要归一化，让总和为 `1`。

```python
raw_weights = {
    "linear": 1.0,
    "tree": 2.0,
    "boosting": 3.0,
}

total = sum(raw_weights.values())
weights = {
    name: value / total
    for name, value in raw_weights.items()
}

print(weights)
```

结果：

```text
{'linear': 0.16666666666666666, 'tree': 0.3333333333333333, 'boosting': 0.5}
```

未归一化权重不一定错，但归一化更容易解释。

## 分类投票

分类 ensemble 可以用投票。

```python
votes = ["buy", "hold", "buy", "sell", "buy"]

counts = {}
for vote in votes:
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

多数模型投 `buy`，最终信号是 `buy`。

投票适合离散分类。

如果模型能输出概率，平均概率通常更细腻。

## 概率平均

分类模型常输出正类概率。

可以平均概率，再设阈值。

```python
probabilities = [0.55, 0.70, 0.60]

avg_probability = sum(probabilities) / len(probabilities)
signal = 1 if avg_probability >= 0.60 else 0

print(avg_probability)
print(signal)
```

结果：

```text
0.6166666666666667
1
```

平均概率超过阈值 `0.60`，所以给出正信号。

交易阈值应该考虑成本，而不是机械用 `0.5`。

## bagging

bagging 是 bootstrap aggregating。

它训练很多个同类模型，每个模型使用 bootstrap 样本。

随机森林就是典型 bagging 思想。

伪代码：

```python
models = []
for seed in seeds:
    sample = bootstrap_sample(train_data, seed)
    model = train_model(sample)
    models.append(model)

prediction = average(model.predict(x) for model in models)
```

bagging 主要降低方差。

它适合单模型不稳定、对样本扰动敏感的场景。

## bootstrap 多样性

bootstrap 会让不同模型看到不同训练样本。

```python
import random

data = ["A", "B", "C", "D"]

random.seed(1)
sample_1 = [random.choice(data) for _ in data]

random.seed(2)
sample_2 = [random.choice(data) for _ in data]

print(sample_1)
print(sample_2)
```

结果：

```text
['B', 'A', 'C', 'A']
['A', 'A', 'A', 'C']
```

不同样本会训练出不同模型。

如果这些模型错误不完全相同，平均后可能更稳。

## boosting

boosting 是顺序训练模型。

每个新模型修正前面模型的错误。

XGBoost 和 LightGBM 都属于 boosting tree。

简化更新：

```python
prediction = 0.0
learning_rate = 0.1
tree_outputs = [0.5, -0.2, 0.1]

for output in tree_outputs:
    prediction += learning_rate * output

print(prediction)
```

结果：

```text
0.04
```

boosting 通常偏强，但也更需要正则、早停和时间验证。

## stacking

stacking 是把多个 base model 的预测作为新特征，再训练 meta model。

结构：

```text
原始特征 -> base models -> out-of-fold predictions -> meta model
```

关键是：

```text
meta model 训练时，必须使用 out-of-fold 预测。
```

如果用 base model 在训练集上的 in-sample 预测训练 meta model，会严重泄露。

伪代码：

```python
for fold in folds:
    base_model.fit(train_folds)
    oof_pred[valid_fold] = base_model.predict(valid_fold)

meta_model.fit(oof_pred, y)
```

## stacking 的小例子

假设两个 base model 的 out-of-fold 预测是：

```python
base_preds = [
    {"linear": 0.01, "tree": 0.03, "y": 0.02},
    {"linear": 0.02, "tree": 0.01, "y": 0.00},
    {"linear": -0.01, "tree": -0.02, "y": -0.01},
]

meta_features = [
    [row["linear"], row["tree"]]
    for row in base_preds
]

print(meta_features)
```

结果：

```text
[[0.01, 0.03], [0.02, 0.01], [-0.01, -0.02]]
```

这些 `meta_features` 可以用来训练第二层模型。

但前提是它们必须是 out-of-fold 预测。

## blending

blending 和 stacking 类似。

区别是 blending 通常留出一个 holdout set 来训练 meta model。

流程：

```text
train_base: 训练 base models
holdout: 生成 base predictions，训练 meta model
test: 最终评估
```

优点：

- 实现简单。
- 不需要复杂交叉验证。

缺点：

- 浪费一部分训练数据。
- holdout 太小会不稳定。
- 时间序列里仍要按时间划分。

## 模型多样性

ensemble 的收益来自多样性。

如果模型预测高度相关，组合收益有限。

```python
model_a = [0.01, 0.02, 0.03]
model_b = [0.011, 0.021, 0.031]

differences = [
    abs(a - b)
    for a, b in zip(model_a, model_b)
]

avg_difference = sum(differences) / len(differences)

print(avg_difference)
```

结果：

```text
0.0010000000000000009
```

两个模型几乎一样。

把它们 ensemble 起来，增益可能很小。

## 错误相关性

如果两个模型经常一起错，组合效果有限。

```python
errors_a = [0.01, -0.02, 0.03]
errors_b = [0.02, -0.01, 0.04]

same_direction = [
    (a > 0 and b > 0) or (a < 0 and b < 0)
    for a, b in zip(errors_a, errors_b)
]

same_direction_ratio = sum(same_direction) / len(same_direction)

print(same_direction_ratio)
```

结果：

```text
1.0
```

错误方向完全一致。

这说明两个模型可能缺乏互补性。

## 量化中的 ensemble

量化里常见 ensemble：

- 线性模型 + 树模型。
- 不同 horizon 的模型组合。
- 不同特征组模型组合。
- 不同 regime 模型组合。
- 不同 random seed 的神经网络平均。
- 多个 alpha signal 加权。

例如：

```text
value model
momentum model
quality model
liquidity model
```

可以组合成一个总分。

但组合权重要用样本外验证选择。

## 信号组合

多个 alpha signal 可以做加权组合。

```python
signals = {
    "value": 0.4,
    "momentum": 0.8,
    "quality": 0.2,
}

weights = {
    "value": 0.3,
    "momentum": 0.5,
    "quality": 0.2,
}

combined_signal = sum(
    signals[name] * weights[name]
    for name in signals
)

print(combined_signal)
```

结果：

```text
0.56
```

组合后得到一个综合 alpha score。

## ensemble 风险

ensemble 不是免费午餐。

风险包括：

- 增加系统复杂度。
- 增加调参空间。
- 更难排查错误。
- stacking 容易泄露。
- 模型可能高度相关。
- 权重可能在验证集上过拟合。
- 组合可能提高换手。

例如两个模型轮流给高信号，组合后可能更频繁调仓。

```python
turnover_model_a = 0.20
turnover_model_b = 0.25
turnover_ensemble = 0.35

extra_turnover = turnover_ensemble - max(turnover_model_a, turnover_model_b)

print(extra_turnover)
```

结果：

```text
0.09999999999999998
```

组合后换手比单模型更高。

需要检查交易成本。

## stacking 泄露风险

stacking 最常见错误：

```text
用 base model 的训练集内预测训练 meta model。
```

这会让 meta model 看到过拟合后的预测。

简化判断：

```python
base_train_score = 0.20
base_valid_score = 0.04

leakage_risk = base_train_score > base_valid_score * 3

print(leakage_risk)
```

结果：

```text
True
```

如果 base model 训练集预测远好于验证集，in-sample stacking 会非常危险。

必须使用 OOF 预测。

## 时间序列中的 stacking

金融时间序列不能随便 KFold。

stacking 的 OOF 预测也要按时间生成。

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    base_model.fit(x[train_period], y[train_period])
    oof_pred[valid_period] = base_model.predict(x[valid_period])

meta_model.fit(oof_pred[past_periods], y[past_periods])
```

不要让 meta model 训练时使用未来 fold 的信息。

## ensemble 是否值得

使用 ensemble 前先问：

- 单模型 baseline 有多强？
- 模型之间是否真的互补？
- 组合后样本外是否更稳定？
- 换手和成本是否上升？
- 权重是否稳定？
- 是否引入泄露风险？
- 是否值得增加系统复杂度？

小例子：

```python
single_model_score = 0.050
ensemble_score = 0.055
complexity_penalty = 0.010

net_gain = ensemble_score - single_model_score - complexity_penalty

print(net_gain)
```

结果：

```text
-0.005000000000000003
```

组合模型表面提高了 `0.005`。

但如果复杂度成本更高，未必值得。

## 实战检查清单

做 ensemble 时，至少检查：

- 每个 base model 的独立样本外表现。
- base model 之间预测相关性。
- base model 之间错误相关性。
- ensemble 是否提高稳定性。
- 权重是否用验证集选择。
- stacking 是否使用 OOF 预测。
- 是否按时间切分。
- 组合后 turnover 是否上升。
- 扣成本后是否仍然改善。
- ensemble 是否打败简单平均。

## 常见误区

第一，把很多弱模型堆起来，以为一定更强。

第二，用训练集内预测做 stacking。

第三，用测试集调 ensemble 权重。

第四，不检查模型相关性。

第五，只看 gross score，不看换手和成本。

第六，复杂 ensemble 没有明显打败简单平均。

第七，忽略系统复杂度和维护成本。

## 小结

ensemble 是模型组合。

常见方式包括：

```text
平均
加权平均
投票
bagging
boosting
stacking
blending
```

它的收益来自模型多样性和错误互补。

在量化机器学习里，ensemble 要特别注意：

```text
时间序列 OOF
避免 stacking 泄露
验证权重稳定性
检查换手和成本
确认复杂度带来的收益足够大
```
