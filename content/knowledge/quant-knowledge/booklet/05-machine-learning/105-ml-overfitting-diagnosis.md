# 105. 机器学习：overfitting diagnosis 的训练/验证差距、学习曲线、泄露排查和复杂度控制

## 核心概念

overfitting diagnosis 是过拟合诊断。

它要回答：

```text
模型是真的学到了可泛化规律，还是只记住了训练集噪声？
```

过拟合的典型表现是：

```text
训练集表现很好
验证集 / 测试集表现明显差
```

在金融机器学习里，过拟合尤其常见。

原因包括：

- 信号弱。
- 噪声大。
- 非平稳。
- 特征很多。
- 样本有效独立性低。
- 调参次数多。
- 回测选择偏差强。
- 很容易发生未来信息泄露。

## 训练验证差距

最直接的诊断是看 train score 和 valid score 的差距。

```python
train_score = 0.18
valid_score = 0.04

gap = train_score - valid_score
is_suspicious = gap > 0.08

print(gap)
print(is_suspicious)
```

结果：

```text
0.13999999999999999
True
```

训练表现远好于验证表现。

这说明模型可能过拟合。

这里的阈值 `0.08` 不是定理，只是例子。

实际要结合指标波动、业务场景和样本量判断。

## 低训练低验证：欠拟合

如果训练和验证表现都差，可能是欠拟合。

```python
train_score = 0.01
valid_score = 0.008

gap = train_score - valid_score
underfit = train_score < 0.02 and valid_score < 0.02

print(gap)
print(underfit)
```

结果：

```text
0.002
True
```

欠拟合说明模型连训练集规律都没学到。

可能原因：

- 特征没有信号。
- 模型太简单。
- 正则太强。
- 标签太噪。
- 目标定义不合理。

## 高训练低验证：过拟合

过拟合的典型情况：

```python
train_score = 0.25
valid_score = 0.02

overfit = train_score > 0.10 and valid_score < 0.05

print(overfit)
```

结果：

```text
True
```

训练集学得很好，但验证集几乎没有效果。

在量化里，这种模型通常不能上线。

即使回测图很好，也要优先怀疑：

- 调参过度。
- 特征泄露。
- 训练窗口偶然有效。
- 模型复杂度太高。
- 交易成本没有正确扣除。

## 学习曲线

学习曲线看的是：

```text
随着训练样本增加，训练表现和验证表现如何变化？
```

简化例子：

```python
sample_sizes = [100, 300, 1000]
train_scores = [0.30, 0.22, 0.16]
valid_scores = [0.02, 0.05, 0.09]

gaps = [
    train - valid
    for train, valid in zip(train_scores, valid_scores)
]

print(gaps)
```

结果：

```text
[0.27999999999999997, 0.16999999999999998, 0.07]
```

样本增加后，gap 变小。

这说明增加数据可能缓解过拟合。

如果 gap 一直很大，可能需要降低复杂度或改特征。

## 复杂度曲线

复杂度曲线看模型越来越复杂时，训练和验证表现如何变化。

例如树深度：

```python
results = [
    {"max_depth": 2, "train": 0.04, "valid": 0.035},
    {"max_depth": 4, "train": 0.09, "valid": 0.060},
    {"max_depth": 8, "train": 0.20, "valid": 0.030},
]

best = max(results, key=lambda row: row["valid"])

print(best)
```

结果：

```text
{'max_depth': 4, 'train': 0.09, 'valid': 0.06}
```

`max_depth=8` 的训练分数最高。

但验证分数下降。

所以应该选 `max_depth=4`。

## 验证集波动

单个验证集结果可能偶然。

要看多个时间切分。

```python
valid_scores = [0.04, 0.03, -0.01, 0.05, 0.00]

mean_score = sum(valid_scores) / len(valid_scores)
positive_ratio = sum(score > 0 for score in valid_scores) / len(valid_scores)
worst_score = min(valid_scores)

print(mean_score)
print(positive_ratio)
print(worst_score)
```

结果：

```text
0.022
0.6
-0.01
```

平均为正，但只有 `60%` 的窗口为正。

这说明模型稳定性一般。

如果某些年份完全失效，要分 regime 和市场环境继续检查。

## 时间切分

金融数据不能随便随机切分。

正确方向是：

```text
train 在过去
valid 在未来
test 在更未来
```

伪代码：

```python
splits = [
    ("2016-2018", "2019"),
    ("2017-2019", "2020"),
    ("2018-2020", "2021"),
]

for train_period, valid_period in splits:
    model.fit(features[train_period], labels[train_period])
    pred = model.predict(features[valid_period])
    score = evaluate(pred, labels[valid_period])
```

如果随机切分时间序列，模型可能看到未来分布。

验证结果会偏乐观。

## 泄露排查

过拟合和泄露经常混在一起。

如果模型表现异常好，要先排查泄露。

常见泄露：

- 特征用了未来收益。
- rolling 没有 shift。
- 标准化用全样本 fit。
- 特征选择用了测试集。
- 标签和特征日期错位。
- 成分股或基本面数据使用了事后信息。
- 目标变量被直接或间接放进特征。

简化检查：

```python
feature_names = ["momentum_20d", "future_return_5d", "value"]

leakage_like = [
    name
    for name in feature_names
    if "future" in name
]

print(leakage_like)
```

结果：

```text
['future_return_5d']
```

名字里出现 `future` 不一定必然错误。

但它必须触发人工检查。

## 随机标签测试

如果把标签随机打乱，模型应该失效。

如果随机标签还能表现很好，很可能存在泄露或评估错误。

```python
real_label_score = 0.06
shuffled_label_score = 0.05

test_failed = shuffled_label_score > real_label_score * 0.5

print(test_failed)
```

结果：

```text
True
```

随机标签分数仍然接近真实标签。

这很可疑。

可能问题：

- train / valid 混在一起。
- 标签没有真正打乱。
- 指标计算有 bug。
- 特征含有标签泄露。

## 噪声特征测试

加入随机噪声特征后，如果噪声特征很重要，要警惕。

```python
feature_importance = {
    "momentum": 0.04,
    "value": 0.03,
    "random_noise": 0.08,
}

noise_too_important = feature_importance["random_noise"] > max(
    feature_importance["momentum"],
    feature_importance["value"],
)

print(noise_too_important)
```

结果：

```text
True
```

随机噪声比真实特征还重要。

这说明模型可能在数据挖掘噪声。

## 调参过拟合

如果尝试了大量参数组合，总会有一些组合在验证集上偶然好。

```python
num_trials = 200
best_score = 0.09
median_score = 0.02

selection_gap = best_score - median_score
too_many_trials = num_trials > 100 and selection_gap > 0.05

print(selection_gap)
print(too_many_trials)
```

结果：

```text
0.06999999999999999
True
```

尝试太多组合后，最佳结果可能是验证集噪声。

应该保留独立 test set 或做嵌套验证。

## 模型复杂度信号

复杂模型更容易过拟合。

常见危险信号：

- 树太深。
- 叶子样本太少。
- 神经网络参数远多于有效样本。
- 特征数量远大于样本数。
- 正则太弱。
- 训练轮数太多。
- 早停没有独立验证集。

简化判断：

```python
n_samples = 500
n_features = 2000

high_dimensional = n_features > n_samples

print(high_dimensional)
```

结果：

```text
True
```

特征比样本多，必须更强正则和更严格验证。

## 处理过拟合

常见处理方法：

- 降低模型复杂度。
- 增加正则。
- 减少特征。
- 增加样本。
- 更严格时间验证。
- 早停。
- 增大叶子最小样本数。
- 降低树深度或 `num_leaves`。
- 加 dropout 或 weight decay。
- 降低调参次数。
- 使用更简单的 baseline。

例如调低复杂度：

```python
params = {
    "max_depth": 8,
    "min_samples_leaf": 5,
}

params["max_depth"] = 4
params["min_samples_leaf"] = 50

print(params)
```

结果：

```text
{'max_depth': 4, 'min_samples_leaf': 50}
```

树更浅，叶子样本更多。

模型会更保守。

## 早停

early stopping 可以防止训练轮数过多。

```python
valid_scores = [0.02, 0.04, 0.05, 0.049, 0.048]
best_score = float("-inf")
bad_rounds = 0
patience = 2

for step, score in enumerate(valid_scores, start=1):
    if score > best_score:
        best_score = score
        best_step = step
        bad_rounds = 0
    else:
        bad_rounds += 1

    if bad_rounds >= patience:
        break

print(best_score)
print(best_step)
print(step)
```

结果：

```text
0.05
3
5
```

第 3 轮最好。

第 5 轮触发早停。

## 训练指标不等于交易指标

模型可能在预测指标上过拟合，也可能在交易规则上过拟合。

例如：

```python
gross_ic = 0.04
turnover_cost = 0.05

net_score = gross_ic - turnover_cost

print(net_score)
print(net_score > 0)
```

结果：

```text
-0.010000000000000002
False
```

预测看起来有信号。

但交易成本后没有价值。

这也是一种“研究过拟合”。

## 实战检查清单

诊断过拟合时，至少检查：

- train / valid gap 是否过大。
- 学习曲线是否随样本增加收敛。
- 复杂度增加后 valid 是否下降。
- 多个时间窗口表现是否稳定。
- 是否有未来信息泄露。
- 随机标签测试是否失效。
- 噪声特征是否异常重要。
- 调参次数是否过多。
- 是否保留独立 test set。
- 是否扣除交易成本。
- 是否与简单 baseline 比较。

## 常见误区

第一，只看训练集表现。

第二，用随机切分验证金融时间序列。

第三，在测试集上反复调参。

第四，发现高收益后不做泄露排查。

第五，只看平均表现，不看最差年份。

第六，复杂模型没有打败线性基线还继续使用。

第七，忽略交易成本导致的净收益过拟合。

## 小结

overfitting diagnosis 的核心是证明模型不是只记住训练集噪声。

最重要的证据包括：

```text
训练/验证差距合理
多个时间窗口样本外稳定
复杂度增加不会只提升训练集
随机标签测试失效
无未来信息泄露
扣成本后仍有价值
```

在金融机器学习里，过拟合不是例外，而是默认风险。

所以每个模型都应该先被怀疑，再用严格证据证明它值得相信。
