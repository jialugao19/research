# 机器学习：hyperparameter tuning 的搜索空间、验证集、随机搜索、贝叶斯优化和调参过拟合

## 核心概念

hyperparameter tuning 是超参数调优。

超参数是训练前设定的参数。

例如：

- 线性模型的 `alpha`。
- SVM 的 `C` 和 `gamma`。
- 树模型的 `max_depth`、`min_samples_leaf`。
- XGBoost / LightGBM 的 `learning_rate`、`num_leaves`。
- 神经网络的学习率、层数、batch size。

它们和模型训练得到的参数不同。

```text
参数：模型从数据中学出来，例如线性回归系数
超参数：训练前人为设定，例如正则强度
```

调参的目标是：

```text
在不泄露未来信息的验证框架下，找到样本外表现更好的超参数。
```

## 调参不是越多越好

调参有收益，也有风险。

收益：

- 找到更合适的模型复杂度。
- 降低欠拟合或过拟合。
- 改善样本外表现。

风险：

- 在验证集上过拟合。
- 搜索空间太大导致偶然好结果。
- 反复看 test set 导致测试集失效。
- 调参过程引入未来信息泄露。

在量化里，调参过拟合非常常见。

## 搜索空间

搜索空间定义你要尝试哪些超参数。

例如树模型：

```python
search_space = {
    "max_depth": [2, 4, 6],
    "min_samples_leaf": [20, 50],
}

configs = []
for depth in search_space["max_depth"]:
    for leaf in search_space["min_samples_leaf"]:
        configs.append({
            "max_depth": depth,
            "min_samples_leaf": leaf,
        })

print(configs)
```

结果：

```text
[{'max_depth': 2, 'min_samples_leaf': 20}, {'max_depth': 2, 'min_samples_leaf': 50}, {'max_depth': 4, 'min_samples_leaf': 20}, {'max_depth': 4, 'min_samples_leaf': 50}, {'max_depth': 6, 'min_samples_leaf': 20}, {'max_depth': 6, 'min_samples_leaf': 50}]
```

这里一共有 `3 * 2 = 6` 组配置。

## 搜索空间要有尺度感

搜索空间不应该随便设。

例如正则强度常用 log scale：

```python
alphas = [0.001, 0.01, 0.1, 1.0, 10.0]

ratios = [
    alphas[i + 1] / alphas[i]
    for i in range(len(alphas) - 1)
]

print(ratios)
```

结果：

```text
[10.0, 10.0, 10.0, 10.0]
```

每一步都是 10 倍。

这比在线性尺度上尝试：

```text
0.001, 1.001, 2.001, ...
```

更合理。

## 验证集

调参必须基于验证集。

典型数据划分：

```text
train: 训练模型参数
valid: 选择超参数
test: 最后只评估一次
```

不要在 test set 上反复调参。

一旦你根据 test 表现改参数，test 就变成了 valid。

在金融时间序列里，划分应该按时间：

```text
train: 2016-2018
valid: 2019
test: 2020
```

而不是随机打散。

## walk-forward 调参

更稳健的方式是多个时间切分。

伪代码：

```python
for config in configs:
    scores = []
    for train_period, valid_period in walk_forward_splits:
        model = build_model(config)
        model.fit(x[train_period], y[train_period])
        pred = model.predict(x[valid_period])
        scores.append(evaluate(pred, y[valid_period]))
    config_score = mean(scores)
```

这比单个验证期更可靠。

因为它能检查参数是否跨时间稳定。

## grid search

grid search 是穷举网格。

优点：

- 简单。
- 可复现。
- 覆盖明确。

缺点：

- 维度高时组合爆炸。
- 很多参数组合其实不值得尝试。
- 如果网格设计不好，会浪费计算。

组合数量：

```python
space_sizes = {
    "max_depth": 4,
    "learning_rate": 5,
    "min_samples_leaf": 3,
}

num_configs = 1
for size in space_sizes.values():
    num_configs *= size

print(num_configs)
```

结果：

```text
60
```

三个参数就有 60 组。

更多参数会迅速变大。

## random search

random search 是从搜索空间随机采样。

它常常比 grid search 更有效。

原因是：

```text
不是所有超参数都同样重要。
随机搜索能在重要维度上探索更多不同取值。
```

小例子：

```python
import random

random.seed(7)

depth_choices = [2, 3, 4, 5, 6]
leaf_choices = [10, 20, 50, 100]

samples = []
for _ in range(3):
    samples.append({
        "max_depth": random.choice(depth_choices),
        "min_samples_leaf": random.choice(leaf_choices),
    })

print(samples)
```

结果：

```text
[{'max_depth': 4, 'min_samples_leaf': 20}, {'max_depth': 5, 'min_samples_leaf': 10}, {'max_depth': 2, 'min_samples_leaf': 10}]
```

固定随机种子可以保证结果可复现。

## 从验证集选择最优

调参时，不看训练分数，而看验证分数。

```python
results = [
    {"config": "small", "train": 0.05, "valid": 0.04},
    {"config": "medium", "train": 0.10, "valid": 0.06},
    {"config": "large", "train": 0.20, "valid": 0.03},
]

best = max(results, key=lambda row: row["valid"])

print(best)
```

结果：

```text
{'config': 'medium', 'train': 0.1, 'valid': 0.06}
```

`large` 训练分数最高，但验证分数较差。

所以选择 `medium`。

## 调参过拟合

尝试的配置越多，越容易找到验证集上的偶然好结果。

小例子：

```python
num_trials = 300
best_valid_score = 0.08
median_valid_score = 0.02

selection_gap = best_valid_score - median_valid_score
over_tuned = num_trials > 100 and selection_gap > 0.04

print(selection_gap)
print(over_tuned)
```

结果：

```text
0.06
True
```

这不证明一定过拟合。

但说明要谨慎：

- 保留独立 test set。
- 减少搜索空间。
- 用多个时间切分。
- 检查最优参数附近是否也稳定。

## 参数稳定性

如果最优参数只在一个点好，周围都差，要警惕。

```python
valid_by_depth = {
    2: 0.04,
    3: 0.055,
    4: 0.060,
    5: 0.058,
    6: 0.020,
}

best_depth = max(valid_by_depth, key=valid_by_depth.get)
neighbor_scores = [
    valid_by_depth[depth]
    for depth in [best_depth - 1, best_depth + 1]
    if depth in valid_by_depth
]

stable_peak = all(score > 0.05 for score in neighbor_scores)

print(best_depth)
print(neighbor_scores)
print(stable_peak)
```

结果：

```text
4
[0.055, 0.058]
True
```

`max_depth=4` 最好。

相邻参数也不错。

这比孤立尖峰更可信。

## 贝叶斯优化直觉

贝叶斯优化不是随机盲试。

它会根据已经试过的结果，决定下一组更可能好的参数。

直觉：

```text
用一个代理模型估计哪里可能高分
在“已知好区域附近开发”和“未知区域探索”之间权衡
```

伪代码：

```python
history = []

for step in range(max_trials):
    config = propose_next_config(history)
    score = evaluate_config(config)
    history.append((config, score))
```

贝叶斯优化适合：

- 单次训练成本高。
- 参数空间较大。
- 评估噪声不是极端大。

但它仍然可能过拟合验证集。

## early stopping 也是调参

对 boosting 和神经网络来说，训练轮数本身也是超参数。

early stopping 用验证集决定什么时候停止。

```python
valid_scores = [0.03, 0.05, 0.055, 0.054, 0.053]
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
0.055
3
5
```

第 3 轮最好。

第 5 轮触发停止。

## 不同模型的关键超参数

常见关键参数：

```text
Ridge / Lasso:
    alpha

SVM:
    C, gamma, kernel

Random Forest:
    n_estimators, max_depth, min_samples_leaf, max_features

XGBoost / LightGBM:
    learning_rate, n_estimators, max_depth / num_leaves,
    min_child_weight / min_data_in_leaf,
    subsample, colsample / feature_fraction,
    lambda / alpha

Neural Network:
    learning_rate, batch_size, layers, hidden size,
    dropout, weight_decay, epochs
```

调参时先抓主要参数。

不要一开始就把所有参数都放进搜索空间。

## 量化中的调参指标

不要只用通用机器学习指标。

量化调参常用：

- 样本外 IC / RankIC。
- 分组收益。
- long-short return。
- Sharpe。
- drawdown。
- turnover。
- 扣成本后收益。
- 分年份稳定性。

小例子：

```python
gross_score = 0.07
turnover_penalty = 0.03

net_score = gross_score - turnover_penalty

print(net_score)
```

结果：

```text
0.04000000000000001
```

如果只看 gross score，可能选出高换手模型。

## nested validation

如果你既要调参又要估计最终泛化表现，可以用 nested validation。

直觉：

```text
内层 valid 用来选参数
外层 test 用来评估选出来的流程
```

伪代码：

```python
for outer_train, outer_test in outer_splits:
    best_config = tune_hyperparameters(outer_train)
    model = train_model(outer_train, best_config)
    score = evaluate(model, outer_test)
```

这比单次 train/valid/test 更复杂。

但可以减少调参过程带来的乐观偏差。

## 常见误区

第一，在 test set 上反复调参。

第二，用随机切分调金融时间序列。

第三，搜索空间过大，最后选择验证集偶然最优。

第四，只看训练分数或 gross score。

第五，不记录尝试过的参数和结果。

第六，没有固定 random seed。

第七，最优参数是孤立尖峰却直接相信。

第八，不和简单 baseline 比较。

## 实战检查清单

调参时至少记录：

- 搜索空间。
- 每组参数的验证分数。
- 时间切分方式。
- 随机种子。
- 最优参数。
- 最优参数附近的表现。
- 是否使用 early stopping。
- 是否保留最终 test set。
- 指标是否扣除交易成本。
- 试验次数是否过多。

## 小结

hyperparameter tuning 的本质是：

```text
用验证集选择模型复杂度和训练设置。
```

它能提升模型表现，也能制造过拟合。

在量化机器学习里，可靠调参需要：

```text
按时间切分
合理搜索空间
控制试验次数
看样本外净指标
检查参数稳定性
保留独立测试集
记录完整调参过程
```
