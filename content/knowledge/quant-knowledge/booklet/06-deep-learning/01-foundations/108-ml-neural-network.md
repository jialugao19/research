# 机器学习：NN 的神经元、层、激活函数、前向传播、损失和反向传播直觉

## 核心概念

NN 是 neural network，神经网络。

最基础的神经网络可以理解为：

```text
很多个线性变换 + 非线性激活函数 叠在一起。
```

线性模型只能表达：

```text
y = w · x + b
```

神经网络通过多层结构和非线性激活，可以表达更复杂的关系。

但更强的表达能力也带来更高的过拟合风险。

在金融机器学习里，NN 不应该被当成默认更强的模型。

它必须和线性模型、树模型等基线比较。

## 从计算图看一次训练

神经网络可以先不看成“很多层”，而看成一张记录依赖关系的计算图：节点是变量或运算，边表示数据如何流动。

```text
features -> linear -> activation -> prediction -> loss
```

前向传播沿箭头方向计算每个节点的值，并保存反向所需的中间量。反向传播从 loss 出发沿反方向回溯，把上游梯度与每个节点的局部导数组合起来。

这一区分很重要：

```text
计算图：记录谁依赖谁
反向传播：沿依赖图计算梯度
优化器：使用梯度更新参数
```

自动微分框架并不是先把整个网络化成一条巨大符号公式。它更像在前向时记录运算账本，在 `backward()` 时按局部规则逐项结算。梯度为零也不自动代表全局最优，它还可能对应局部极值或鞍点。

## 神经元

一个神经元先做线性加权，再过激活函数。

```text
z = w · x + b
a = activation(z)
```

小例子：

```python
features = [0.5, -0.2, 0.1]
weights = [0.4, -0.3, 0.2]
bias = 0.1

z = sum(x * w for x, w in zip(features, weights)) + bias

print(z)
```

结果：

```text
0.38
```

这个 `z` 还只是线性分数。

下一步要通过激活函数。

## ReLU

ReLU 是常见激活函数。

公式：

```text
ReLU(x) = max(0, x)
```

```python
def relu(x):
    return max(0.0, x)

values = [-1.0, 0.0, 0.5]
activated = [relu(x) for x in values]

print(activated)
```

结果：

```text
[0.0, 0.0, 0.5]
```

ReLU 会把负数截成 `0`。

它简单、计算快，是很多深度网络的默认选择。

## sigmoid

sigmoid 常用于二分类输出层。

公式：

```text
sigmoid(x) = 1 / (1 + exp(-x))
```

```python
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

print(sigmoid(0.0))
print(sigmoid(1.0))
```

结果：

```text
0.5
0.7310585786300049
```

输出在 `0` 到 `1` 之间，可以解释为概率。

## 激活函数的角色并不相同

隐藏层激活主要决定网络如何形成非线性表示；输出层变换则要和任务及损失函数配套。

- ReLU 在正半轴梯度直接，但神经元长期落在负半轴时可能不再更新。
- sigmoid 和 tanh 在大幅值区域容易饱和，局部导数会变小。
- softmax 面向一整组类别 logits；提高一个类别的概率会同时压低其它类别，因此它不是逐元素 sigmoid。

“输出形状没有改变”不能证明函数逐元素作用。softmax 的每个输出依赖同一样本的全部 logits，反向传播需要考虑类别之间的耦合。

## 一层隐藏层

一个简单网络可以有：

```text
输入层 -> 隐藏层 -> 输出层
```

隐藏层的每个神经元都接收同一组输入。

```python
def relu(x):
    return max(0.0, x)

features = [1.0, 2.0]

hidden_weights = [
    [0.5, -0.2],
    [-0.1, 0.4],
]
hidden_biases = [0.0, 0.1]

hidden = []
for weights, bias in zip(hidden_weights, hidden_biases):
    z = sum(x * w for x, w in zip(features, weights)) + bias
    hidden.append(relu(z))

print(hidden)
```

结果：

```text
[0.09999999999999998, 0.8]
```

隐藏层把输入转换成新的表示。

## 输出层

输出层把隐藏层表示转成最终预测。

```python
hidden = [0.09999999999999998, 0.8]
output_weights = [0.3, -0.2]
output_bias = 0.05

prediction = sum(
    h * w
    for h, w in zip(hidden, output_weights)
) + output_bias

print(prediction)
```

结果：

```text
-0.08000000000000002
```

如果这是回归模型，`prediction` 可以直接作为预测收益。

如果是二分类模型，还可以再接 sigmoid。

## 前向传播

前向传播就是从输入一路算到输出。

```python
def relu(x):
    return max(0.0, x)

def forward(features):
    hidden_weights = [
        [0.5, -0.2],
        [-0.1, 0.4],
    ]
    hidden_biases = [0.0, 0.1]
    output_weights = [0.3, -0.2]
    output_bias = 0.05

    hidden = []
    for weights, bias in zip(hidden_weights, hidden_biases):
        z = sum(x * w for x, w in zip(features, weights)) + bias
        hidden.append(relu(z))

    return sum(h * w for h, w in zip(hidden, output_weights)) + output_bias

print(forward([1.0, 2.0]))
```

结果：

```text
-0.08000000000000002
```

训练前，前向传播只是根据当前权重给出预测。

训练的任务是调整权重，让预测更接近标签。

## 损失函数

回归任务常用 MSE。

```python
y_true = [0.02, -0.01, 0.03]
y_pred = [0.01, 0.00, 0.025]

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
[0.0001, 0.0001, 2.4999999999999988e-05]
7.499999999999999e-05
```

损失越小，预测越接近真实值。

但金融标签噪声很大，低训练损失不一定代表样本外有收益。

## 二分类损失

二分类常用 log loss。

```python
import math

y = 1
p = 0.7

loss = -y * math.log(p) - (1 - y) * math.log(1 - p)

print(loss)
```

结果：

```text
0.35667494393873245
```

如果真实标签是 `1`，预测概率越低，损失越大。

多分类时常把 softmax 与交叉熵合在一起。对真实类别 `y`：

```text
loss = -log(softmax(logits)[y])
```

工程上通常直接把原始 logits 传给框架的交叉熵损失。损失内部使用稳定的 log-sum-exp 计算，避免先 softmax、再取 log 造成的数值问题。两者合并后的梯度也很清楚：

```text
d loss / d logits = predicted_probabilities - one_hot_label
```

所以交叉熵不只检查类别有没有排第一，还会惩罚错误置信度。低训练交叉熵仍不等于样本外概率已经校准。

## 反向传播直觉

反向传播是计算每个参数对损失的影响。

它回答：

```text
如果某个权重稍微变大，损失会增加还是减少？
```

这个影响就是梯度。

训练时用梯度下降更新参数：

```text
w_new = w_old - learning_rate * gradient
```

小例子：

```python
w = 0.5
gradient = 0.2
learning_rate = 0.1

w_new = w - learning_rate * gradient

print(w_new)
```

结果：

```text
0.48
```

梯度为正，说明增大 `w` 会增加损失。

所以更新会让 `w` 变小。

## 单参数梯度例子

考虑一个最简单模型：

```text
pred = w * x
loss = 1/2 * (pred - y)^2
```

梯度是：

```text
d loss / d w = (pred - y) * x
```

```python
x = 2.0
y = 5.0
w = 1.0
learning_rate = 0.1

pred = w * x
gradient = (pred - y) * x
w_new = w - learning_rate * gradient

print(pred)
print(gradient)
print(w_new)
```

结果：

```text
2.0
-6.0
1.6
```

预测太低，梯度为负。

更新后 `w` 增大。

## batch 和 epoch

训练神经网络通常分 batch。

```text
batch: 一次用于计算梯度的一小批样本
epoch: 完整扫过训练集一遍
```

如果训练集有 1000 个样本，batch size 是 100：

```python
n_samples = 1000
batch_size = 100

steps_per_epoch = n_samples // batch_size

print(steps_per_epoch)
```

结果：

```text
10
```

一个 epoch 有 10 次参数更新。

## 学习率

learning rate 控制每次更新步长。

学习率太大，训练可能震荡。

学习率太小，训练很慢。

```python
w = 1.0
gradient = -0.5

for learning_rate in [0.01, 0.1, 1.0]:
    updated = w - learning_rate * gradient
    print(learning_rate, updated)
```

结果：

```text
0.01 1.005
0.1 1.05
1.0 1.5
```

同一个梯度下，学习率越大，更新幅度越大。

## 过拟合风险

神经网络参数很多，容易过拟合。

简化参数量：

```python
input_dim = 20
hidden_dim = 64
output_dim = 1

num_params = input_dim * hidden_dim + hidden_dim + hidden_dim * output_dim + output_dim

print(num_params)
```

结果：

```text
1409
```

这只是一个很小的网络。

更深更宽的网络参数量会快速变大。

金融数据有效样本不多时，要特别谨慎。

## 常见正则手段

NN 常见正则化：

- weight decay。
- dropout。
- early stopping。
- batch normalization。
- 降低网络宽度和深度。
- 增加数据。
- 数据增强。
- 更严格时间验证。

dropout 的直觉：

```text
训练时随机关闭一部分神经元，防止模型过度依赖某几个路径。
```

简化例子：

```python
hidden = [0.2, 0.5, 0.1]
dropout_mask = [1, 0, 1]

dropped = [
    h * m
    for h, m in zip(hidden, dropout_mask)
]

print(dropped)
```

结果：

```text
[0.2, 0.0, 0.1]
```

第二个神经元这次被关闭。

常见框架使用 inverted dropout：保留下来的激活还会除以保留概率 `1-p`。这样训练输出的期望与原激活一致，推理时可以直接关闭 dropout 并使用完整网络。

保持的是期望，不是每次输出或方差。Dropout 也不是剪枝、归一化或梯度裁剪；它先随机改变前向计算路径，梯度再沿当前这张计算图传播。

## NN 在量化中的用途

NN 可以用于：

- 非线性横截面预测。
- 多因子组合。
- 时间序列预测。
- 表征学习。
- 高频特征建模。
- 多模态数据，例如文本、盘口、价格序列。

但基础 NN 对时间依赖没有特殊结构。

如果要建模序列，通常会考虑：

- RNN。
- LSTM。
- GRU。
- Transformer。

这些后面会单独写。

## 时间序列验证

NN 也必须严格按时间验证。

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    scaler.fit(x[train_period])
    x_train = scaler.transform(x[train_period])
    x_valid = scaler.transform(x[valid_period])

    model = NeuralNetwork(config)
    model.fit(x_train, y[train_period], valid_data=(x_valid, y[valid_period]))
    pred = model.predict(x_valid)
    score = evaluate_net_performance(pred, y[valid_period], costs[valid_period])
```

注意：

```text
标准化、特征选择、early stopping 都不能使用未来数据。
```

## 常见误区

第一，认为 NN 一定比树模型或线性模型好。

第二，样本少但网络很大。

第三，只看训练 loss，不看样本外净收益。

第四，标准化使用全样本。

第五，没有 early stopping。

第六，不固定随机种子，结果难以复现。

第七，忽略交易成本和换手。

第八，给框架交叉熵传入已经 softmax 的概率，重复归一化并损失数值稳定性。

第九，忘记梯度默认可能累加，在下一次更新前没有正确清零。

## 小结

基础 NN 是多层线性变换和非线性激活的组合。

核心流程是：

```text
前向传播得到预测
损失函数衡量误差
反向传播计算梯度
优化器更新参数
```

在量化机器学习里，NN 的优势是表达能力强。

风险是：

```text
参数多
容易过拟合
调参复杂
解释困难
对数据泄露极其敏感
```

所以 NN 必须和简单基线比较，并用严格时间样本外验证。

## 延伸阅读与来源

- [Datawhale / jshn9515 Deep Learning Notes](https://datawhalechina.github.io/deep-learning-notes/zh/index.html)：用于核对计算图、自动微分、激活函数与 softmax 交叉熵的教学主线；原资料采用 CC BY-NC 4.0。
- [PyTorch autograd](https://pytorch.org/docs/stable/autograd.html) 与 [CrossEntropyLoss](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)：核对梯度累加、输入约定和数值稳定实现。
- 本章补充内容为面向量化建模训练边界的原创归纳。
