# 101. 机器学习：linear model baseline 的线性回归、逻辑回归、L1/L2 正则和损失函数

## 核心概念

linear model baseline 是线性模型基线。

在机器学习项目里，它回答的是：

```text
不用复杂模型，只用最简单、最可解释的线性关系，能做到什么水平？
```

常见线性基线包括：

- 线性回归。
- Ridge 回归。
- Lasso 回归。
- Elastic Net。
- 逻辑回归。

在量化研究里，线性基线非常重要。

因为如果一个复杂模型只比线性模型好一点点，但复杂度、换手、过拟合风险都更高，它未必值得使用。

## 为什么要先做线性基线

线性模型有几个优点：

- 快。
- 可解释。
- 不容易过拟合到极端复杂规则。
- 系数方向清晰。
- 方便检查数据泄露。
- 方便做样本外和分组诊断。
- 是复杂模型的参照物。

常见研究流程：

```text
先做线性基线
再做树模型 / boosting / 神经网络
比较复杂模型是否真的带来样本外净收益提升
```

如果复杂模型打不过线性模型，要先怀疑：

- 数据太少。
- 信号偏线性。
- 复杂模型过拟合。
- 调参不合理。
- 标签噪声太大。
- 评估方法有问题。

## 线性回归形式

线性回归假设：

```text
y = b + w_1 x_1 + w_2 x_2 + ... + w_p x_p + error
```

其中：

- `y` 是目标。
- `x_i` 是特征。
- `w_i` 是系数。
- `b` 是截距。

小例子：

```python
features = {
    "momentum": 0.20,
    "value": -0.10,
    "quality": 0.30,
}

weights = {
    "momentum": 0.05,
    "value": -0.02,
    "quality": 0.04,
}

intercept = 0.001

prediction = intercept + sum(
    features[name] * weights[name]
    for name in features
)

print(prediction)
```

结果：

```text
0.025
```

这个预测是三个特征的加权和。

## 系数方向

线性模型系数有明确方向。

```text
w_i > 0: 特征越大，预测值越大
w_i < 0: 特征越大，预测值越小
w_i = 0: 模型没有使用这个特征
```

例如：

```python
weights = {
    "momentum": 0.05,
    "value": -0.02,
    "quality": 0.04,
}

positive_features = [
    name
    for name, weight in weights.items()
    if weight > 0
]

print(positive_features)
```

结果：

```text
['momentum', 'quality']
```

这说明模型认为 `momentum` 和 `quality` 与预测目标正相关。

但要注意：

```text
系数方向是条件相关，不是因果关系。
```

如果特征高度相关，系数也可能不稳定。

## 平方误差损失

线性回归最常见目标是最小化平方误差。

```text
loss = mean((y_true - y_pred) ** 2)
```

小例子：

```python
y_true = [0.03, -0.01, 0.02]
y_pred = [0.02, 0.00, 0.01]

squared_errors = [
    (true - pred) ** 2
    for true, pred in zip(y_true, y_pred)
]

mse = sum(squared_errors) / len(squared_errors)

print(squared_errors)
print(mse)
```

结果：

```text
[9.999999999999996e-05, 0.0001, 0.0001]
9.999999999999999e-05
```

平方误差会惩罚大误差。

如果目标里有极端值，OLS 容易受影响。

## 一元线性回归的闭式解

只有一个特征时，斜率可以写成：

```text
w = cov(x, y) / var(x)
```

小例子：

```python
x = [1, 2, 3]
y = [2, 4, 6]

x_mean = sum(x) / len(x)
y_mean = sum(y) / len(y)

cov_xy = sum(
    (xi - x_mean) * (yi - y_mean)
    for xi, yi in zip(x, y)
)
var_x = sum(
    (xi - x_mean) ** 2
    for xi in x
)

slope = cov_xy / var_x
intercept = y_mean - slope * x_mean

print(slope)
print(intercept)
```

结果：

```text
2.0
0.0
```

这里 `y = 2x`。

线性回归准确恢复斜率 `2`。

## 矩阵形式

多元线性回归可以写成：

```text
y = X beta + error
```

OLS 的闭式解是：

```text
beta = (X'X)^(-1) X'y
```

前提是 `X'X` 可逆。

如果特征共线性很强，`X'X` 会不稳定。

这也是为什么需要正则化。

伪代码：

```python
beta = inverse(transpose(X) @ X) @ transpose(X) @ y
prediction = X_new @ beta
```

真实项目里通常直接用数值库或 sklearn，不手写矩阵逆。

## 梯度下降直觉

线性模型也可以用梯度下降估计参数。

对平方误差来说：

```text
error = prediction - y
gradient_w = mean(error * x)
```

小例子：单个样本的一步更新。

```python
x = 2.0
y = 5.0
w = 1.0
learning_rate = 0.1

prediction = w * x
error = prediction - y
gradient = error * x
w_new = w - learning_rate * gradient

print(prediction)
print(error)
print(gradient)
print(w_new)
```

结果：

```text
2.0
-3.0
-6.0
1.6
```

模型预测太低，所以梯度更新把 `w` 从 `1.0` 提高到 `1.6`。

## Ridge：L2 正则

Ridge 回归在线性回归损失上加 L2 惩罚。

```text
loss = mse + alpha * sum(w_i ** 2)
```

L2 正则会让系数变小，但通常不会精确变成 0。

小例子：

```python
weights = [0.5, -0.2, 0.1]
alpha = 0.1

l2_penalty = alpha * sum(w ** 2 for w in weights)

print(l2_penalty)
```

结果：

```text
0.030000000000000006
```

较大的系数会受到更强惩罚。

Ridge 适合处理：

- 特征很多。
- 特征相关。
- 系数估计不稳定。
- 需要收缩但不想直接删特征。

## Lasso：L1 正则

Lasso 加的是 L1 惩罚。

```text
loss = mse + alpha * sum(abs(w_i))
```

L1 正则可以把一些系数压到 0。

所以它有特征选择效果。

```python
weights = [0.5, -0.2, 0.1]
alpha = 0.1

l1_penalty = alpha * sum(abs(w) for w in weights)

print(l1_penalty)
```

结果：

```text
0.08000000000000002
```

如果你希望模型更稀疏，可以考虑 Lasso。

但在高度相关特征里，Lasso 可能随机选择其中一个，导致解释不稳定。

## L1 的软阈值直觉

Lasso 的一个直觉是 soft threshold。

如果某个未正则化系数很小，L1 会把它压成 0。

```python
def soft_threshold(value, penalty):
    if value > penalty:
        return value - penalty
    if value < -penalty:
        return value + penalty
    return 0.0

raw_weights = [0.30, 0.05, -0.20]
penalty = 0.10

shrunk = [
    soft_threshold(weight, penalty)
    for weight in raw_weights
]

print(shrunk)
```

结果：

```text
[0.19999999999999998, 0.0, -0.1]
```

`0.05` 被压成了 `0`。

这就是 L1 稀疏性的直觉。

## Elastic Net

Elastic Net 同时使用 L1 和 L2。

```text
loss = mse + alpha_1 * sum(abs(w_i)) + alpha_2 * sum(w_i ** 2)
```

它介于 Ridge 和 Lasso 之间。

```python
weights = [0.5, -0.2, 0.1]
alpha_l1 = 0.05
alpha_l2 = 0.10

penalty = (
    alpha_l1 * sum(abs(w) for w in weights)
    + alpha_l2 * sum(w ** 2 for w in weights)
)

print(penalty)
```

结果：

```text
0.07000000000000002
```

Elastic Net 常用于特征很多且相关的场景。

## 逻辑回归

逻辑回归用于分类。

它先计算线性分数：

```text
z = b + w_1 x_1 + ... + w_p x_p
```

再用 sigmoid 把分数映射成概率：

```text
p = 1 / (1 + exp(-z))
```

小例子：

```python
import math

z = 0.7
p = 1 / (1 + math.exp(-z))

print(p)
```

结果：

```text
0.6681877721681662
```

`z` 越大，预测为正类的概率越高。

## 逻辑损失

二分类逻辑损失是：

```text
loss = -y * log(p) - (1 - y) * log(1 - p)
```

如果真实标签是 `1`，但模型给的概率很低，损失会很大。

```python
import math

y = 1
p = 0.8

log_loss = -y * math.log(p) - (1 - y) * math.log(1 - p)

print(log_loss)
```

结果：

```text
0.2231435513142097
```

如果概率只有 `0.2`：

```python
p = 0.2
log_loss = -y * math.log(p) - (1 - y) * math.log(1 - p)

print(log_loss)
```

结果：

```text
1.6094379124341003
```

模型越自信地错，惩罚越大。

## 分类阈值

逻辑回归输出概率。

是否交易，不一定用 `0.5` 作为阈值。

有交易成本时，阈值应该更高。

```python
probabilities = [0.45, 0.55, 0.70]
threshold = 0.60

signals = [
    1 if p >= threshold else 0
    for p in probabilities
]

print(signals)
```

结果：

```text
[0, 0, 1]
```

`0.55` 虽然大于 `0.5`，但不足以覆盖更高交易门槛。

## 标准化很重要

线性模型尤其依赖特征尺度。

如果一个特征量纲很大，它可能主导正则化和梯度。

标准化常见做法：

```text
z = (x - mean) / std
```

小例子：

```python
values = [10, 20, 30]

mean = sum(values) / len(values)
variance = sum((x - mean) ** 2 for x in values) / len(values)
std = variance ** 0.5

standardized = [
    (x - mean) / std
    for x in values
]

print(mean)
print(std)
print(standardized)
```

结果：

```text
20.0
8.16496580927726
[-1.224744871391589, 0.0, 1.224744871391589]
```

注意：

```text
标准化参数必须只用训练集估计，不能用全样本。
```

否则会泄露未来信息。

## 线性模型和共线性

如果两个特征高度相关，线性模型系数可能不稳定。

例如：

```text
momentum_20d 和 momentum_21d 几乎一样
```

模型可能把权重分给其中一个，也可能在不同训练窗口中来回变化。

```python
weights_run1 = {"momentum_20d": 0.04, "momentum_21d": 0.01}
weights_run2 = {"momentum_20d": 0.01, "momentum_21d": 0.04}

group_weight_1 = weights_run1["momentum_20d"] + weights_run1["momentum_21d"]
group_weight_2 = weights_run2["momentum_20d"] + weights_run2["momentum_21d"]

print(group_weight_1)
print(group_weight_2)
```

结果：

```text
0.05
0.05
```

单个特征系数不稳定，但特征组整体权重稳定。

解释时要小心。

## 线性基线评估

回归任务常看：

- MSE / MAE。
- R2。
- IC / RankIC。
- 分组收益。
- long-short 收益。
- 扣成本后收益。

分类任务常看：

- accuracy。
- precision / recall。
- AUC。
- log loss。
- 分组收益。
- 交易阈值后的净收益。

简化例子：

```python
baseline_ic = 0.025
complex_model_ic = 0.028

improvement = complex_model_ic - baseline_ic

print(improvement)
```

结果：

```text
0.0030000000000000027
```

复杂模型只提高 `0.003`。

如果它带来更高换手和更强过拟合风险，未必值得。

## 时间序列验证

线性模型也必须按时间验证。

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    scaler.fit(x[train_period])
    x_train = scaler.transform(x[train_period])
    x_valid = scaler.transform(x[valid_period])

    model.fit(x_train, y[train_period])
    pred = model.predict(x_valid)
    score = evaluate(pred, y[valid_period])
```

关键点：

```text
scaler 只能在训练期 fit
正则参数只能用验证集选择
不能把未来数据用于标准化、筛选特征或调参
```

## 量化中的线性基线

在线性基线中，常见设定是：

```text
输入：标准化后的因子
目标：未来收益、超额收益、分组标签或方向标签
模型：Ridge / Lasso / LogisticRegression
验证：walk-forward
评估：IC、RankIC、分组收益、net return
```

伪代码：

```python
model = Ridge(alpha=alpha)
model.fit(train_features, train_forward_returns)
pred = model.predict(valid_features)
score = rank_ic(pred, valid_forward_returns)
```

对强噪声的金融数据，Ridge 经常是一个稳健起点。

Lasso 更适合做稀疏特征选择，但解释稳定性要额外检查。

## 常见误区

第一，不做线性基线，直接上复杂模型。

第二，用全样本标准化导致未来信息泄露。

第三，把系数当作因果解释。

第四，特征尺度差异很大却不标准化。

第五，只看训练集拟合效果。

第六，逻辑回归输出概率后直接用 `0.5` 交易，不考虑成本。

第七，忽略共线性导致的系数不稳定。

## 小结

linear model baseline 是机器学习研究里的基本参照物。

它帮助你判断：

```text
复杂模型是否真的有必要？
非线性是否真的带来样本外提升？
特征方向和尺度是否合理？
数据泄露是否已经出现？
```

线性回归关注平方误差。

逻辑回归关注分类概率和 log loss。

Ridge 用 L2 正则收缩系数。

Lasso 用 L1 正则产生稀疏性。

在量化机器学习里，线性基线不只是简单模型。

它是判断复杂模型是否值得信任的第一道检验。
