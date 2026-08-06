# 机器学习：SVM 的最大间隔、hinge loss、核函数和分类边界

## 核心概念

SVM 是 support vector machine，支持向量机。

它最常用于分类。

SVM 的核心思想是：

```text
在能分开样本的分类边界中，选择间隔最大的那一个。
```

这个“间隔”指的是样本点到分类边界的距离。

间隔越大，模型对小扰动越不敏感，泛化可能更好。

## 线性分类边界

线性 SVM 的决策函数是：

```text
score = w · x + b
```

分类规则：

```text
score >= 0 -> 正类
score < 0  -> 负类
```

小例子：

```python
features = [0.5, -0.2]
weights = [1.0, 2.0]
bias = -0.09

score = sum(x * w for x, w in zip(features, weights)) + bias
label = 1 if score >= 0 else -1

print(score)
print(label)
```

结果：

```text
0.009999999999999981
1
```

这个样本在分类边界的正侧。

所以归为正类。

## 几何间隔

点到超平面 `w · x + b = 0` 的距离是：

```text
distance = abs(w · x + b) / ||w||
```

小例子：

```python
import math

features = [2.0, 1.0]
weights = [1.0, 0.0]
bias = -1.0

score = sum(x * w for x, w in zip(features, weights)) + bias
norm_w = math.sqrt(sum(w ** 2 for w in weights))
distance = abs(score) / norm_w

print(score)
print(distance)
```

结果：

```text
1.0
1.0
```

分类边界是 `x_1 - 1 = 0`。

点 `[2, 1]` 到边界的距离是 `1`。

## 最大间隔

SVM 希望分类正确，同时让间隔尽量大。

在线性可分情况下，它的目标可以理解为：

```text
minimize 1/2 * ||w||^2
subject to y_i * (w · x_i + b) >= 1
```

为什么最小化 `||w||` 等价于最大化间隔？

因为间隔和 `1 / ||w||` 成正比。

```python
import math

norms = [0.5, 1.0, 2.0]
margins = [1 / norm for norm in norms]

print(margins)
```

结果：

```text
[2.0, 1.0, 0.5]
```

`||w||` 越小，间隔越大。

## 支持向量

支持向量是离分类边界最近的样本。

它们决定了边界位置。

在标准 SVM 约束里，支持向量通常满足：

```text
y_i * (w · x_i + b) = 1
```

小例子：

```python
samples = [
    {"name": "A", "y": 1, "score": 1.0},
    {"name": "B", "y": 1, "score": 2.5},
    {"name": "C", "y": -1, "score": -1.0},
    {"name": "D", "y": -1, "score": -3.0},
]

support_vectors = [
    row["name"]
    for row in samples
    if row["y"] * row["score"] == 1.0
]

print(support_vectors)
```

结果：

```text
['A', 'C']
```

`A` 和 `C` 正好在 margin 上。

它们是支持向量。

## hinge loss

现实数据通常不能完全线性分开。

SVM 使用 hinge loss 惩罚分错或离边界太近的样本。

公式：

```text
hinge_loss = max(0, 1 - y * score)
```

其中 `y` 是 `+1` 或 `-1`。

```python
def hinge_loss(y, score):
    return max(0.0, 1 - y * score)

examples = [
    (1, 2.0),
    (1, 0.5),
    (-1, -0.2),
    (-1, 1.0),
]

losses = [
    hinge_loss(y, score)
    for y, score in examples
]

print(losses)
```

结果：

```text
[0.0, 0.5, 0.8, 2.0]
```

解释：

- `(1, 2.0)` 正类且分数足够高，没有损失。
- `(1, 0.5)` 分类正确，但离边界太近，有损失。
- `(-1, -0.2)` 分类正确，但 margin 不够，有损失。
- `(-1, 1.0)` 分错，损失很大。

## C 参数

SVM 的 `C` 控制分类错误惩罚强度。

简化目标：

```text
loss = margin_penalty + C * classification_penalty
```

`C` 越大，模型越重视训练样本分类正确。

`C` 越小，模型越允许一些训练错误，以换取更大的间隔。

小例子：

```python
margin_penalty = 0.4
classification_penalty = 1.5

for C in [0.1, 1.0, 10.0]:
    total_loss = margin_penalty + C * classification_penalty
    print(C, total_loss)
```

结果：

```text
0.1 0.55
1.0 1.9
10.0 15.4
```

`C` 大时，分类错误代价被放大。

这可能降低训练错误，但增加过拟合风险。

## soft margin

不可分数据需要 soft margin。

soft margin 允许部分样本违反 margin，甚至被分错。

直觉：

```text
与其为了一个噪声点扭曲边界，不如允许它出错。
```

量化数据噪声很大。

所以 soft margin 通常比 hard margin 更现实。

伪代码：

```python
model = SVC(C=1.0, kernel="linear")
model.fit(train_x, train_y)
```

调参时，`C` 应该用时间序列验证选择。

## 核函数

线性 SVM 只能学线性边界。

核函数让 SVM 可以学习非线性边界。

常见 kernel：

```text
linear
poly
rbf
sigmoid
```

核函数本质上计算样本之间的相似度。

例如线性核：

```text
K(x, z) = x · z
```

```python
x = [1.0, 2.0]
z = [3.0, 4.0]

linear_kernel = sum(a * b for a, b in zip(x, z))

print(linear_kernel)
```

结果：

```text
11.0
```

## polynomial kernel

多项式核：

```text
K(x, z) = (gamma * x · z + coef0) ** degree
```

小例子：

```python
x = [1.0, 2.0]
z = [3.0, 4.0]
gamma = 0.5
coef0 = 1.0
degree = 2

dot = sum(a * b for a, b in zip(x, z))
poly_kernel = (gamma * dot + coef0) ** degree

print(poly_kernel)
```

结果：

```text
42.25
```

多项式核可以表达特征交互。

但 degree 太高容易过拟合。

## RBF kernel

RBF kernel 也叫 Gaussian kernel。

公式：

```text
K(x, z) = exp(-gamma * ||x - z||^2)
```

小例子：

```python
import math

x = [1.0, 2.0]
z = [2.0, 4.0]
gamma = 0.5

squared_distance = sum(
    (a - b) ** 2
    for a, b in zip(x, z)
)
rbf_kernel = math.exp(-gamma * squared_distance)

print(squared_distance)
print(rbf_kernel)
```

结果：

```text
5.0
0.0820849986238988
```

距离越远，相似度越接近 `0`。

RBF 很灵活，但也容易过拟合。

## gamma 参数

RBF 的 `gamma` 控制单个样本影响范围。

```text
gamma 大 -> 影响范围小，边界更复杂
gamma 小 -> 影响范围大，边界更平滑
```

```python
import math

squared_distance = 5.0

for gamma in [0.1, 0.5, 2.0]:
    similarity = math.exp(-gamma * squared_distance)
    print(gamma, similarity)
```

结果：

```text
0.1 0.6065306597126334
0.5 0.0820849986238988
2.0 4.5399929762484854e-05
```

`gamma` 越大，远处样本相似度衰减越快。

## 特征标准化

SVM 对特征尺度非常敏感。

因为距离、点积、margin 都依赖特征尺度。

例如一个特征是价格 `1000`，另一个特征是收益率 `0.01`。

如果不标准化，大尺度特征会主导距离和分类边界。

小例子：

```python
x = [1000.0, 0.01]
z = [1001.0, 0.02]

squared_distance = sum(
    (a - b) ** 2
    for a, b in zip(x, z)
)

print(squared_distance)
```

结果：

```text
1.0001
```

距离几乎完全由第一个特征决定。

所以 SVM 前通常需要标准化。

并且标准化参数只能在训练集上 fit。

## SVM 输出分数和概率

SVM 原生输出的是 decision score，不是概率。

```python
score = -0.35
label = 1 if score >= 0 else -1

print(label)
```

结果：

```text
-1
```

如果需要概率，通常要做校准。

例如 Platt scaling 或 isotonic calibration。

在量化里，直接用 decision score 做排序也很常见。

但要验证：

- score 和未来收益是否单调。
- score 分组收益是否稳定。
- score 交易阈值是否覆盖成本。

## 类别不平衡

如果正负类比例不平衡，SVM 边界可能偏向多数类。

小例子：

```python
labels = [0] * 90 + [1] * 10

positive_ratio = labels.count(1) / len(labels)

print(positive_ratio)
```

结果：

```text
0.1
```

只有 `10%` 正类。

这时要考虑：

- class_weight。
- 调整阈值。
- 看 precision / recall。
- 看交易后净收益，而不只是 accuracy。

## SVM 在量化中的用途

SVM 可以用于：

- 二分类方向预测。
- 买入 / 不买入分类。
- 非线性分类边界。
- 小样本场景的稳健分类。
- 用 decision score 做横截面排序。

但它不一定适合大规模股票池和高维特征。

原因包括：

- 核 SVM 训练和预测可能很慢。
- 参数 `C`、`gamma` 对结果敏感。
- 概率解释不如逻辑回归直接。
- 非线性核的解释性较弱。
- 金融样本非平稳，复杂边界容易失效。

## 时间序列验证

SVM 也必须用时间序列验证。

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    scaler.fit(x[train_period])
    x_train = scaler.transform(x[train_period])
    x_valid = scaler.transform(x[valid_period])

    model = SVC(C=C, gamma=gamma, kernel=kernel)
    model.fit(x_train, y[train_period])
    score = model.decision_function(x_valid)
    evaluate(score, y[valid_period], costs[valid_period])
```

关键点：

```text
scaler 只能在训练集 fit
C / gamma / kernel 只能用验证集选择
不要随机打散金融时间序列
```

## SVM 和逻辑回归对比

逻辑回归：

- 输出概率更自然。
- 训练通常更快。
- 可解释性更强。
- 适合线性基线。

SVM：

- 最大间隔思想清晰。
- hinge loss 关注 margin。
- 核函数可以建模非线性边界。
- 对参数和尺度更敏感。

简化区别：

```text
逻辑回归关心概率拟合
SVM 关心分类边界和最大间隔
```

## 常见误区

第一，不标准化特征。

第二，用 RBF kernel 后不严格调 `C` 和 `gamma`。

第三，用随机 CV 评估金融时间序列。

第四，把 SVM decision score 当成概率。

第五，只看 accuracy，不看分组收益和交易成本。

第六，在大规模高维数据上盲目使用核 SVM。

第七，用复杂核函数拟合噪声。

## 小结

SVM 的核心是最大间隔分类。

它通过 hinge loss 和 `C` 参数在两个目标之间权衡：

```text
间隔尽量大
训练错误尽量少
```

核函数让 SVM 可以学习非线性边界。

但在金融机器学习里，要特别注意：

```text
特征标准化
时间序列验证
C 和 gamma 的敏感性
decision score 的校准和交易阈值
扣成本后的样本外表现
```
