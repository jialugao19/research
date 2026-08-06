# 机器学习：sequence modeling 的输入窗口、标签对齐和防泄露评估

## 核心概念

sequence modeling 是序列建模。

它的核心不是换一个复杂模型，而是先把数据组织成：

```text
一段历史输入 -> 一个或多个未来标签
```

在时间序列预测里，最常见的问题是：

```text
用过去 N 个时点的信息，预测未来某个时点或未来一段区间。
```

例如：

```text
用过去 20 日特征预测明日收益
用过去 60 分钟盘口预测未来 5 分钟价格方向
用过去 252 日因子序列预测下月风险
```

sequence modeling 的难点通常不在模型名字，而在窗口、标签和切分是否对齐。

## 从序列生成样本

原始序列通常是一条连续数据。

模型训练需要把它切成很多样本。

小例子：

```python
prices = [100, 101, 103, 102, 105]
window = 3

samples = []
for end in range(window, len(prices)):
    x = prices[end - window:end]
    y = prices[end]
    samples.append((x, y))

print(samples)
```

结果：

```text
[([100, 101, 103], 102), ([101, 103, 102], 105)]
```

第一个样本表示：

```text
用 [100, 101, 103] 预测 102
```

第二个样本表示：

```text
用 [101, 103, 102] 预测 105
```

这就是滑动窗口。

## window 和 horizon

sequence modeling 里有两个基础参数：

```text
window: 输入历史长度
horizon: 预测向前看的距离
```

如果 `window = 3`，`horizon = 1`，就是用过去 3 个值预测下一个值。

```python
returns = [0.01, -0.02, 0.03, 0.00, 0.02]
window = 3
horizon = 1

samples = []
for start in range(len(returns) - window - horizon + 1):
    x = returns[start:start + window]
    y = returns[start + window + horizon - 1]
    samples.append((x, y))

print(samples)
```

结果：

```text
[([0.01, -0.02, 0.03], 0.0), ([-0.02, 0.03, 0.0], 0.02)]
```

如果 `horizon` 变大，标签就会离输入窗口更远。

例如预测未来 5 日收益、未来 20 日波动率，都属于更长 horizon。

## 标签对齐

时间序列里最常见的错误是标签没有向未来移动。

假设特征是今天收盘前可见的信息，标签是明天收益。

正确对齐是：

```python
features = [10, 20, 30, 40]
labels = [0.1, 0.2, 0.3, 0.4]

aligned = list(zip(features[:-1], labels[1:]))

print(aligned)
```

结果：

```text
[(10, 0.2), (20, 0.3), (30, 0.4)]
```

`feature[0]` 对应 `label[1]`。

这表示：

```text
用今天特征预测明天标签
```

错误对齐是：

```python
features = [10, 20, 30, 40]
labels = [0.1, 0.2, 0.3, 0.4]

wrong = list(zip(features, labels))

print(wrong)
```

结果：

```text
[(10, 0.1), (20, 0.2), (30, 0.3), (40, 0.4)]
```

如果 `labels` 是同一时点之后才能知道的结果，这样就可能泄露未来。

## many-to-one

many-to-one 是最常见的金融预测结构。

它表示：

```text
多个历史时点 -> 一个标签
```

例如用过去 20 日数据预测明日收益。

```python
sequence = [1, 2, 3, 4]
labels = [10, 20, 30, 40]

many_to_one = (sequence, labels[-1])

print(many_to_one)
```

结果：

```text
([1, 2, 3, 4], 40)
```

在模型层面，可以写成伪代码：

```text
hidden = encode(sequence)
prediction = head(hidden_last)
loss = compare(prediction, future_label)
```

LSTM、GRU、Transformer 都可以用于 many-to-one。

区别只在 `encode(sequence)` 的实现。

## many-to-many

many-to-many 表示：

```text
多个历史时点 -> 多个输出
```

例如对输入窗口里的每个时点都预测一个标签。

```python
sequence = [1, 2, 3, 4]
labels = [10, 20, 30, 40]

many_to_many = list(zip(sequence, labels))

print(many_to_many)
```

结果：

```text
[(1, 10), (2, 20), (3, 30), (4, 40)]
```

many-to-many 常见于：

```text
逐分钟预测下一分钟方向
逐 token 输出状态
对整个路径生成预测序列
```

伪代码：

```text
hidden_sequence = encode(sequence)
predictions = head(hidden_sequence)
loss = sum(compare(prediction_t, label_t) for each t)
```

需要特别注意，每个 `label_t` 必须只使用当时允许看到的信息定义。

## recursive 和 direct 多步预测

多步预测有两种常见做法。

第一种是 recursive。

```text
先预测 t+1
把 t+1 的预测值放回输入
再预测 t+2
继续滚动
```

它节省模型数量，但误差会逐步累积。

第二种是 direct。

```text
直接训练预测 t+1、t+2、...、t+k
```

它更直接，但输出结构更大。

在金融预测里，如果交易决策只需要一个固定 horizon，通常先做 direct 更清楚。

例如：

```text
用过去 60 分钟预测未来 5 分钟收益
```

这个任务不需要一步步生成未来 1、2、3、4、5 分钟。

## 防止窗口跨越训练边界

时间序列切分不能像普通样本一样随便 shuffle。

训练集窗口不能借用验证集未来数据。

例如只允许使用前三个时点作为训练区间：

```python
returns = [0.01, -0.02, 0.03, 0.04]
window = 2
train_end = 3

train_samples = []
for end in range(window, train_end):
    train_samples.append(returns[end - window:end])

print(train_samples)
```

结果：

```text
[[0.01, -0.02]]
```

这里训练样本只使用训练区间内部的历史窗口。

不能为了多造样本，把验证区间的数据拼进训练输入。

## 特征标准化也要按时间切分

sequence modeling 里的泄露不只来自标签。

标准化也会泄露。

如果用全样本均值标准化训练窗口，就把未来分布信息带进了训练。

正确做法是只用训练区间估计标准化参数。

小例子：

```python
series = [2, 4, 6, 8]

mean = sum(series[:2]) / 2
centered = [value - mean for value in series]

print(mean)
print(centered)
```

结果：

```text
3.0
[-1.0, 1.0, 3.0, 5.0]
```

这里均值只来自前两个训练样本。

验证和测试可以使用这个训练均值变换，但不能反过来参与均值估计。

## panel sequence

金融数据常常不是单条序列，而是多资产面板。

例如：

```text
date, asset, features
```

此时要按资产分别构造窗口。

不能把 `AAA` 的昨天和 `BBB` 的今天拼成一条序列。

```python
assets = {
    "AAA": [1.0, 1.1, 1.2, 1.3],
    "BBB": [2.0, 2.1, 2.2, 2.3],
}
window = 2

rows = []
for asset, values in assets.items():
    for end in range(window, len(values)):
        rows.append((asset, values[end - window:end], values[end]))

print(rows)
```

结果：

```text
[('AAA', [1.0, 1.1], 1.2), ('AAA', [1.1, 1.2], 1.3), ('BBB', [2.0, 2.1], 2.2), ('BBB', [2.1, 2.2], 2.3)]
```

真实项目里还要处理：

```text
不同资产上市时间不同
停牌导致缺口
跨市场时区不同
横截面标签同时点对齐
行业、市值等静态特征如何并入序列
```

## padding 和 mask

不同样本的序列长度可能不同。

模型通常需要固定形状输入，所以会使用 padding。

padding 后要配合 mask。

```python
values = [0.5, -0.1, 0.0, 0.0]
mask = [1, 1, 0, 0]

valid_values = [
    value
    for value, keep in zip(values, mask)
    if keep
]

print(valid_values)
```

结果：

```text
[0.5, -0.1]
```

`0.0` 可能是真实值，也可能是 padding。

mask 告诉模型哪些位置是真实输入。

否则模型可能把填充值当成有效信号。

## 评估方式

sequence modeling 的评估必须保持时间顺序。

常见方式：

```text
固定训练集 + 后续验证集
rolling window walk-forward
expanding window walk-forward
按日期切分，再在每个日期内做横截面评估
```

不建议在时间序列样本上随机打散后做普通交叉验证。

因为相邻窗口高度重叠。

随机切分会让训练集和测试集共享大量近似相同的历史片段。

这会高估效果。

## 实战检查清单

构造 sequence modeling 数据集时，至少检查：

```text
每个输入窗口是否只包含预测时已知的信息
标签是否相对特征正确 shift
window 和 horizon 是否与交易决策一致
训练、验证、测试是否按时间分开
标准化、缺失值填充、类别映射是否只在训练集 fit
多资产窗口是否按 asset 分组构造
padding 位置是否有 mask
评估样本是否避免高度重叠造成的虚高
```

如果这些检查没通过，换成更复杂的 LSTM、GRU 或 Transformer 也没有意义。

## 小结

sequence modeling 的本质是把时间序列问题变成有清晰边界的监督学习样本。

关键不是模型越复杂越好，而是：

```text
输入窗口定义清楚
标签对齐无泄露
训练验证按时间隔离
评估方式贴近实际交易
```

到这里，机器学习部分的深度学习小节已经完成。

下一部分进入市场微观结构，从 bid-ask spread 开始。
