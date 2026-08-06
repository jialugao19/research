# 机器学习：LSTM 的序列输入、隐藏状态、门控机制和时间序列建模

## 核心概念

LSTM 是 long short-term memory。

它是一种 RNN 结构，用来处理序列数据。

普通前馈神经网络通常把每个样本独立处理。

LSTM 则会按时间顺序处理输入：

```text
x_1, x_2, x_3, ...
```

并维护内部状态，用来记住过去的信息。

在金融机器学习里，LSTM 常被用于：

- 价格序列。
- 收益率序列。
- 成交量序列。
- 订单簿序列。
- 多因子时间窗口。
- 宏观时间序列。

但 LSTM 不会自动解决非平稳、噪声和未来信息泄露。

## 为什么需要序列模型

很多问题不是单个时点能解释的。

例如：

```text
过去 20 天收益路径
过去 60 分钟成交量变化
过去 10 个 tick 的 order imbalance
```

顺序本身可能包含信息。

```python
sequence_a = [0.01, 0.02, 0.03]
sequence_b = [0.03, 0.02, 0.01]

print(sum(sequence_a))
print(sum(sequence_b))
```

结果：

```text
0.06
0.06
```

两个序列总和相同。

但一个是逐步上升，一个是逐步下降。

序列模型可以尝试利用这种路径差异。

## 输入形状

LSTM 输入通常是三维：

```text
batch_size, sequence_length, feature_dim
```

例如：

```text
32 只股票
每只股票过去 20 天
每天 5 个特征
```

输入形状就是：

```text
(32, 20, 5)
```

小例子：

```python
batch_size = 32
sequence_length = 20
feature_dim = 5

num_values = batch_size * sequence_length * feature_dim

print(num_values)
```

结果：

```text
3200
```

这表示一个 batch 里有 3200 个输入数值。

## RNN 的隐藏状态

普通 RNN 会维护隐藏状态 `h_t`。

简化更新：

```text
h_t = activation(W_x x_t + W_h h_{t-1} + b)
```

小例子：

```python
def tanh(x):
    import math
    return math.tanh(x)

x_t = 0.5
h_prev = 0.2

w_x = 0.8
w_h = 0.4
b = 0.1

h_t = tanh(w_x * x_t + w_h * h_prev + b)

print(h_t)
```

结果：

```text
0.5226654296858209
```

隐藏状态把当前输入和过去状态混合起来。

## 普通 RNN 的问题

普通 RNN 很难记住很长的依赖。

原因之一是梯度在时间上反复相乘，可能：

- 越来越小，形成 vanishing gradient。
- 越来越大，形成 exploding gradient。

这会让模型很难学习长期关系。

LSTM 的设计目标就是缓解这个问题。

它通过 cell state 和门控机制来控制信息保留、写入和输出。

## LSTM 的两个状态

LSTM 有两个核心状态：

```text
h_t: hidden state，给外部和下一步使用的短期表示
c_t: cell state，沿时间传递的记忆通道
```

可以粗略理解为：

```text
h_t 更像当前输出
c_t 更像长期记忆
```

LSTM 每一步会决定：

- 忘掉多少旧记忆。
- 写入多少新信息。
- 输出多少当前状态。

这些决定由 gate 控制。

## sigmoid gate

gate 通常用 sigmoid 输出 `0` 到 `1` 之间的数。

```python
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

gate_values = [
    sigmoid(-2.0),
    sigmoid(0.0),
    sigmoid(2.0),
]

print(gate_values)
```

结果：

```text
[0.11920292202211755, 0.5, 0.8807970779778823]
```

接近 `0` 表示少通过。

接近 `1` 表示多通过。

## forget gate

forget gate 决定保留多少旧 cell state。

```text
f_t = sigmoid(...)
c_old_kept = f_t * c_{t-1}
```

小例子：

```python
c_prev = 0.8
forget_gate = 0.25

kept_memory = forget_gate * c_prev

print(kept_memory)
```

结果：

```text
0.2
```

如果 forget gate 是 `0.25`，只保留 25% 的旧记忆。

## input gate 和 candidate

input gate 决定写入多少新信息。

candidate 是候选新记忆。

```text
i_t = sigmoid(...)
g_t = tanh(...)
new_written = i_t * g_t
```

```python
input_gate = 0.6
candidate = 0.5

new_written = input_gate * candidate

print(new_written)
```

结果：

```text
0.3
```

候选新记忆是 `0.5`，input gate 只允许写入 60%。

## cell state 更新

LSTM 的 cell state 更新可以简化为：

```text
c_t = f_t * c_{t-1} + i_t * g_t
```

小例子：

```python
c_prev = 0.8
forget_gate = 0.25
input_gate = 0.6
candidate = 0.5

c_t = forget_gate * c_prev + input_gate * candidate

print(c_t)
```

结果：

```text
0.5
```

旧记忆留下 `0.2`。

新记忆写入 `0.3`。

最终 cell state 是 `0.5`。

## output gate

output gate 决定从 cell state 输出多少到 hidden state。

```text
h_t = o_t * tanh(c_t)
```

```python
import math

c_t = 0.5
output_gate = 0.7

h_t = output_gate * math.tanh(c_t)

print(h_t)
```

结果：

```text
0.3234820100820068
```

`h_t` 是当前时点输出给下一层或预测头的状态。

## 一步 LSTM 简化计算

把几个 gate 合在一起看。

```python
import math

c_prev = 0.8

forget_gate = 0.25
input_gate = 0.6
candidate = 0.5
output_gate = 0.7

c_t = forget_gate * c_prev + input_gate * candidate
h_t = output_gate * math.tanh(c_t)

print(c_t)
print(h_t)
```

结果：

```text
0.5
0.3234820100820068
```

这只是标量教学例子。

真实 LSTM 中，所有 gate 都是向量，并由当前输入和上一时刻 hidden state 计算出来。

## many-to-one

很多金融预测是 many-to-one。

即：

```text
输入过去 T 个时点
输出未来一个标签
```

例如：

```text
过去 20 天因子序列 -> 未来 5 天收益
```

伪代码：

```python
sequence = features[t - 19 : t + 1]
hidden_states = lstm(sequence)
last_hidden = hidden_states[-1]
prediction = linear_head(last_hidden)
```

注意：

```text
sequence 只能包含预测时点可见的信息。
```

## many-to-many

有些任务需要每个时点都有输出。

例如：

```text
每分钟输入盘口特征
每分钟输出交易信号
```

伪代码：

```python
hidden_states = lstm(sequence)
predictions = [
    linear_head(h_t)
    for h_t in hidden_states
]
```

这种结构是 many-to-many。

要特别注意标签对齐。

第 `t` 个输出不能使用 `t` 之后才知道的数据。

## sequence length

`sequence_length` 是输入窗口长度。

它是重要超参数。

```python
total_days = 252
sequence_length = 20

num_windows = total_days - sequence_length + 1

print(num_windows)
```

结果：

```text
233
```

窗口越长，可用训练窗口数越少。

窗口太短可能看不到长期模式。

窗口太长可能加入噪声，并增加训练难度。

## LSTM 和 feature engineering

LSTM 不代表不需要特征工程。

输入仍然要认真设计：

- 收益率而不是价格水平。
- 标准化后的成交量。
- rolling volatility。
- cross-sectional rank。
- 缺失值处理。
- 异常值处理。
- 时间对齐。

如果把泄露特征放进去，LSTM 会学得很快。

模型强不代表数据正确。

## 标准化

序列特征也要标准化。

但标准化必须只用训练期统计量。

```python
train_values = [1.0, 2.0, 3.0]
valid_values = [4.0, 5.0]

train_mean = sum(train_values) / len(train_values)
train_std = (
    sum((x - train_mean) ** 2 for x in train_values) / len(train_values)
) ** 0.5

valid_scaled = [
    (x - train_mean) / train_std
    for x in valid_values
]

print(train_mean)
print(train_std)
print(valid_scaled)
```

结果：

```text
2.0
0.816496580927726
[2.449489742783178, 3.6742346141747673]
```

不能用 valid 或 test 数据重新 fit 标准化器。

## LSTM 的风险

LSTM 在金融里常见风险：

- 样本少，参数多。
- 非平稳导致历史模式失效。
- 序列窗口构造泄露未来。
- 标签 horizon 和输入窗口不匹配。
- 训练慢，调参空间大。
- 结果对 random seed 敏感。
- 解释性弱。

尤其要注意：

```text
LSTM 不是时间序列预测的保证。
```

它只是一个能处理序列的模型结构。

## 时间序列验证

LSTM 必须用时间切分验证。

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    scaler.fit(sequence_features[train_period])
    x_train = build_sequences(scaler.transform(sequence_features[train_period]))
    x_valid = build_sequences(scaler.transform(sequence_features[valid_period]))

    model = LSTMModel(config)
    model.fit(x_train, y_train, valid_data=(x_valid, y_valid))
    pred = model.predict(x_valid)
    score = evaluate_net_performance(pred, y_valid, costs[valid_period])
```

构造序列时要保证：

```text
每个样本的输入窗口只包含该预测时点之前或当时可见的数据。
```

## 和 GRU 的关系

GRU 也是门控 RNN。

它比 LSTM 结构更简单。

粗略区别：

```text
LSTM: hidden state + cell state，三个主要 gate
GRU: 合并部分状态和门，参数更少
```

GRU 后面会单独写。

## 常见误区

第一，用未来窗口构造输入序列。

第二，对全样本做标准化。

第三，以为 LSTM 自动发现所有时间规律。

第四，样本很少但模型很大。

第五，只看训练 loss，不看样本外净收益。

第六，不和简单模型比较。

第七，忽略 sequence length 对样本数和噪声的影响。

## 小结

LSTM 是为序列数据设计的神经网络结构。

它通过：

```text
forget gate
input gate
candidate memory
output gate
cell state
hidden state
```

控制信息在时间上的保留、写入和输出。

在量化机器学习里，LSTM 可以用于时间序列和窗口特征建模。

但它必须满足：

```text
输入无未来信息
标准化只用训练期
按时间样本外验证
和简单基线比较
扣成本后仍然有效
```
