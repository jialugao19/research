# 92. 机器学习：stability 的样本扰动、随机种子、参数敏感性和模型一致性

## 核心概念

stability 是稳定性。

在机器学习中，它问的是：

```text
训练数据、随机种子、超参数、样本切分稍微变化时，模型结果是否大体一致？
```

稳定性关注的是模型估计过程本身是否可靠。

典型问题：

- 换一个 random seed，指标是否大幅变化？
- bootstrap 抽样后，特征重要性是否差不多？
- 超参数小幅变化，表现是否平滑？
- 时间切分换一下，模型结论是否一致？
- 同一信号在不同样本上方向是否稳定？

如果模型很不稳定，说明它可能：

- 过拟合。
- 样本太少。
- 信号太弱。
- 特征强共线。
- 超参数过于敏感。
- 训练过程随机性太强。

## stability 和 robustness 的区别

可以这样区分：

```text
robustness: 面对外部扰动、异常值、成本变化、regime 变化，结果是否仍可接受
stability: 面对训练过程和样本估计扰动，模型结论是否一致
```

例子：

```text
交易成本翻倍后策略是否还赚钱 -> robustness
换 random seed 后模型指标是否差不多 -> stability
```

两者相关，但不完全相同。

一个模型可以对异常值稳健，却对训练样本抽样很不稳定。

## 样本均值的稳定性

先看最简单的估计：均值。

```python
returns = [0.01, 0.02, -0.01, 0.00, 0.03, 0.01]

mean_return = sum(returns) / len(returns)

print(mean_return)
```

结果：

```text
0.01
```

如果删掉一个样本，均值会怎样？

```python
leave_one_out_means = []

for i in range(len(returns)):
    sample = returns[:i] + returns[i + 1:]
    leave_one_out_means.append(sum(sample) / len(sample))

print(leave_one_out_means)
print(max(leave_one_out_means) - min(leave_one_out_means))
```

结果：

```text
[0.01, 0.008, 0.014, 0.012, 0.006, 0.01]
0.008
```

删掉不同样本后，均值在 `0.006` 到 `0.014` 之间变化。

这就是一个简单稳定性检查。

## bootstrap 稳定性

bootstrap 是有放回抽样。

它可以估计统计量在样本扰动下的波动。

```python
import random

returns = [0.01, 0.02, -0.01, 0.00, 0.03, 0.01]

random.seed(7)
bootstrap_means = []

for _ in range(100):
    sample = [random.choice(returns) for _ in returns]
    bootstrap_means.append(sum(sample) / len(sample))

print(min(bootstrap_means))
print(max(bootstrap_means))
```

一种结果：

```text
-5.782411586589357e-19
0.023333333333333334
```

样本很小时，bootstrap 均值范围很宽。

这提醒你：

```text
样本均值 1% 不一定很稳定
```

## 方向稳定性

量化信号里，方向比精确数值更重要。

例如一个特征的 IC 在多个窗口中：

```python
ics = [0.03, 0.02, -0.01, 0.04, 0.01]

positive_ratio = sum(x > 0 for x in ics) / len(ics)
mean_ic = sum(ics) / len(ics)

print(mean_ic)
print(positive_ratio)
```

结果：

```text
0.018000000000000002
0.8
```

平均 IC 是正的，但有一个窗口为负。

如果很多窗口方向翻转，信号稳定性就差。

常见检查：

```text
正 IC 比例
IC 均值 / IC 标准差
最差窗口 IC
不同年份符号是否一致
```

## 特征重要性稳定性

复杂模型的 feature importance 可能不稳定。

假设两次训练得到重要性：

```python
importance_1 = {
    "momentum": 0.40,
    "value": 0.25,
    "size": 0.20,
    "quality": 0.15,
}

importance_2 = {
    "momentum": 0.35,
    "value": 0.15,
    "size": 0.30,
    "quality": 0.20,
}

def rank_features(importance):
    return [
        feature
        for feature, _ in sorted(importance.items(), key=lambda x: -x[1])
    ]

print(rank_features(importance_1))
print(rank_features(importance_2))
```

结果：

```text
['momentum', 'value', 'size', 'quality']
['momentum', 'size', 'quality', 'value']
```

第一名稳定是 `momentum`。

但后面几个特征顺序变化明显。

这可能来自：

- 特征相关性。
- 样本噪声。
- 模型随机性。
- 分裂增益的替代关系。

## Jaccard 相似度

如果只关心 top-k 特征集合，可以用 Jaccard 相似度：

```text
Jaccard(A, B) = |A intersection B| / |A union B|
```

```python
def jaccard(a, b):
    a = set(a)
    b = set(b)
    return len(a & b) / len(a | b)

top3_1 = rank_features(importance_1)[:3]
top3_2 = rank_features(importance_2)[:3]

print(top3_1)
print(top3_2)
print(jaccard(top3_1, top3_2))
```

结果：

```text
['momentum', 'value', 'size']
['momentum', 'size', 'quality']
0.5
```

top-3 只有 2 个共同特征。

Jaccard 是：

```text
2 / 4 = 0.5
```

这说明特征选择结果不算特别稳定。

## 随机种子稳定性

很多模型有随机性：

- train/test split。
- bagging 抽样。
- 随机森林特征子采样。
- 神经网络初始化。
- mini-batch 顺序。

如果多个 seed 的指标差异很大，就不能只汇报最好的 seed。

```python
scores_by_seed = [0.61, 0.58, 0.63, 0.57, 0.62]

mean_score = sum(scores_by_seed) / len(scores_by_seed)
score_range = max(scores_by_seed) - min(scores_by_seed)

print(mean_score)
print(score_range)
```

结果：

```text
0.602
0.06000000000000005
```

如果 AUC 在不同 seed 下能差 `0.06`，模型稳定性值得怀疑。

报告时最好写：

```text
mean +/- std across seeds
```

而不是只写最大值。

## 超参数邻域稳定性

如果模型只在一个超参数点表现好，而附近都差，要警惕。

```python
depth_to_score = {
    2: 0.58,
    3: 0.61,
    4: 0.62,
    5: 0.615,
    6: 0.60,
}

best_depth = max(depth_to_score, key=depth_to_score.get)
neighbor_scores = [depth_to_score[d] for d in [3, 4, 5]]

print(best_depth)
print(neighbor_scores)
print(max(neighbor_scores) - min(neighbor_scores))
```

结果：

```text
4
[0.61, 0.62, 0.615]
0.010000000000000009
```

`max_depth=4` 最好，但 `3` 和 `5` 也接近。

这比下面这种情况更可信：

```text
depth=4: 0.62
depth=3: 0.51
depth=5: 0.50
```

后者更像调参偶然命中。

## 时间窗口稳定性

在时间序列和量化里，稳定性必须按时间看。

```python
year_to_score = {
    2019: 0.04,
    2020: 0.03,
    2021: -0.01,
    2022: 0.02,
    2023: 0.01,
}

positive_year_ratio = sum(x > 0 for x in year_to_score.values()) / len(year_to_score)
worst_year = min(year_to_score, key=year_to_score.get)

print(positive_year_ratio)
print(worst_year)
```

结果：

```text
0.8
2021
```

如果某一年明显失效，要分析原因：

- regime 变化。
- 数据口径变化。
- 交易成本变化。
- 样本太少。
- 策略拥挤。

## 预测稳定性

即使指标差不多，单个样本预测也可能不稳定。

例如两个模型版本对同一批股票的分数：

```python
pred_1 = {
    "A": 0.80,
    "B": 0.75,
    "C": 0.20,
    "D": 0.10,
}

pred_2 = {
    "A": 0.78,
    "B": 0.77,
    "C": 0.22,
    "D": 0.08,
}

changes = {
    symbol: abs(pred_2[symbol] - pred_1[symbol])
    for symbol in pred_1
}

print(changes)
print(max(changes.values()))
```

结果：

```text
{'A': 0.020000000000000018, 'B': 0.020000000000000018, 'C': 0.01999999999999999, 'D': 0.020000000000000004}
0.020000000000000018
```

最大预测变化约 `0.02`，比较稳定。

如果 top 股票分数大幅跳动，会带来高换手。

## 模型选择稳定性

如果每次重训都选出完全不同的模型，说明选择过程不稳定。

例如：

```text
split 1: best = random forest
split 2: best = logistic regression
split 3: best = xgboost
split 4: best = random forest
```

可能原因：

- 模型差距很小。
- 验证集太小。
- 指标噪声大。
- 超参数搜索空间太大。
- 数据分布变化。

这种情况下，不应过度解读“赢家模型”。

更稳妥的是看：

```text
多个模型的均值表现
方差
最差窗口
是否有简单 baseline 接近复杂模型
```

## stability 和 overfitting

不稳定往往是过拟合信号。

如果模型对训练集的微小变化非常敏感，说明它可能学到了样本噪声。

降低不稳定性的方法：

- 简化模型。
- 增加正则化。
- 增加样本。
- 降低特征数量。
- 做特征去相关。
- 使用 bagging / ensemble。
- 限制树深度。
- 使用更稳定的验证方案。

不过稳定不代表一定准确。

一个总是预测均值的模型很稳定，但可能没什么预测力。

## 常见错误

### 错误 1：只汇报最好 seed

最好 seed 可能只是运气。

要看多个 seed 的均值和方差。

### 错误 2：特征重要性排序当成绝对真理

特征重要性可能随样本和模型随机性变化。

尤其当特征高度相关时，重要性会在相关特征之间转移。

### 错误 3：只看平均指标不看波动

两个模型平均 AUC 都是 `0.60`。

一个每次都在 `0.59-0.61`，另一个在 `0.52-0.68`。

前者更稳定。

### 错误 4：把稳定当成好模型的充分条件

稳定只是必要检查之一。

模型还要有样本外预测力、经济逻辑和可执行性。

### 错误 5：忽略时间序列切分

随机 K-fold 稳定不代表时间样本外稳定。

量化问题必须看时间顺序下的稳定性。

## 实战检查清单

做 stability 检查时可以问：

1. 多个 random seed 下指标均值和标准差是多少？
2. bootstrap 或子样本下特征重要性是否一致？
3. 超参数附近表现是否平滑？
4. 不同时间窗口中指标方向是否一致？
5. top-k 预测集合的重叠率是否稳定？
6. 简单 baseline 是否和复杂模型接近？
7. 模型选择结果是否依赖某个偶然切分？

## 记忆要点

- stability 关注训练过程和估计结果是否对扰动敏感。
- leave-one-out 和 bootstrap 可以检查统计量稳定性。
- 多 seed 结果要看均值和方差。
- 特征重要性和 top-k 特征集合需要稳定性检查。
- 超参数邻域表现平滑比孤立尖峰更可信。
- 时间窗口稳定性对量化尤其重要。
- 不稳定常常提示过拟合或样本不足。
- 稳定不等于准确，但不稳定会降低可信度。

## 自测题

1. stability 和 robustness 的区别是什么？
2. 为什么只汇报最好 random seed 有问题？
3. 如何用 bootstrap 检查均值估计稳定性？
4. 为什么特征高度相关时 feature importance 可能不稳定？
5. 为什么量化模型必须检查时间窗口稳定性？
