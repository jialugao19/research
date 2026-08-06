# 机器学习：GRU 的 update gate、reset gate、候选隐藏状态和 LSTM 对比

## 核心概念

GRU 是 gated recurrent unit。

它和 LSTM 一样，是处理序列数据的门控 RNN。

GRU 的目标也是：

```text
在时间序列中保留有用的过去信息，过滤掉不重要的信息。
```

但 GRU 比 LSTM 结构更简单。

LSTM 有：

```text
cell state
hidden state
forget gate
input gate
output gate
```

GRU 通常只有：

```text
hidden state
update gate
reset gate
```

参数更少，训练可能更快。

## GRU 处理什么数据

GRU 适合序列输入。

例如：

- 过去 N 天收益率。
- 过去 N 分钟成交量。
- 过去 N 个 tick 的盘口特征。
- 多因子时间窗口。
- 宏观变量时间序列。

输入形状和 LSTM 类似：

```text
batch_size, sequence_length, feature_dim
```

小例子：

```python
batch_size = 16
sequence_length = 30
feature_dim = 8

num_values = batch_size * sequence_length * feature_dim

print(num_values)
```

结果：

```text
3840
```

一个 batch 中有 `3840` 个输入数值。

## update gate

update gate 控制保留多少旧隐藏状态。

可以粗略理解为：

```text
update gate 大 -> 更多保留过去
update gate 小 -> 更多使用新候选状态
```

GRU 的隐藏状态更新常写成：

```text
h_t = z_t * h_{t-1} + (1 - z_t) * candidate
```

其中 `z_t` 是 update gate。

小例子：

```python
h_prev = 0.8
candidate = 0.2
update_gate = 0.75

h_t = update_gate * h_prev + (1 - update_gate) * candidate

print(h_t)
```

结果：

```text
0.6500000000000001
```

`update_gate = 0.75`，所以大部分保留旧状态。

## update gate 的极端情况

如果 update gate 接近 `1`，几乎保留旧状态。

如果接近 `0`，几乎使用新候选状态。

```python
h_prev = 0.8
candidate = 0.2

for update_gate in [0.0, 0.5, 1.0]:
    h_t = update_gate * h_prev + (1 - update_gate) * candidate
    print(update_gate, h_t)
```

结果：

```text
0.0 0.2
0.5 0.5
1.0 0.8
```

这就是 GRU 控制记忆更新的核心机制。

## reset gate

reset gate 控制计算候选状态时，使用多少旧隐藏状态。

简化形式：

```text
candidate = tanh(W_x x_t + W_h (r_t * h_{t-1}) + b)
```

其中 `r_t` 是 reset gate。

小例子：

```python
import math

x_t = 0.5
h_prev = 0.8
reset_gate = 0.25

w_x = 0.7
w_h = 0.4
b = 0.1

candidate = math.tanh(w_x * x_t + w_h * (reset_gate * h_prev) + b)

print(candidate)
```

结果：

```text
0.4853810906053715
```

reset gate 是 `0.25`。

所以旧状态只以 25% 的比例参与候选状态计算。

## reset gate 的直觉

reset gate 小，表示：

```text
计算新候选状态时，少参考过去。
```

reset gate 大，表示：

```text
计算新候选状态时，多参考过去。
```

```python
import math

x_t = 0.5
h_prev = 0.8
w_x = 0.7
w_h = 0.4
b = 0.1

for reset_gate in [0.0, 0.5, 1.0]:
    candidate = math.tanh(w_x * x_t + w_h * (reset_gate * h_prev) + b)
    print(reset_gate, candidate)
```

结果：

```text
0.0 0.4218990052500079
0.5 0.5441270985226501
1.0 0.6469294504417666
```

reset gate 越大，旧状态对候选状态影响越强。

## sigmoid gate

GRU 的 gate 通常也是 sigmoid 输出。

```python
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

values = [-1.0, 0.0, 1.0]
gates = [sigmoid(x) for x in values]

print(gates)
```

结果：

```text
[0.2689414213699951, 0.5, 0.7310585786300049]
```

gate 值在 `0` 和 `1` 之间。

所以可以作为“通过比例”。

## 一步 GRU 简化计算

把 reset gate、candidate、update gate 放在一起。

```python
import math

x_t = 0.5
h_prev = 0.8

reset_gate = 0.25
update_gate = 0.75

w_x = 0.7
w_h = 0.4
b = 0.1

candidate = math.tanh(w_x * x_t + w_h * (reset_gate * h_prev) + b)
h_t = update_gate * h_prev + (1 - update_gate) * candidate

print(candidate)
print(h_t)
```

结果：

```text
0.4853810906053715
0.7213452726513429
```

旧状态是 `0.8`。

候选状态是 `0.485...`。

update gate 是 `0.75`，所以最终状态更接近旧状态。

## GRU 和 LSTM 对比

简化对比：

```text
LSTM:
    有 cell state 和 hidden state
    gate 更多
    参数更多
    表达能力强

GRU:
    通常只有 hidden state
    gate 更少
    参数更少
    训练可能更快
```

经验上：

- 数据量不大时，GRU 可能更稳。
- 长期依赖很强时，LSTM 可能更有优势。
- 实际效果要靠时间序列验证。

不要假设 LSTM 一定优于 GRU。

## many-to-one

GRU 也常用于 many-to-one 预测。

例如：

```text
过去 30 天特征序列 -> 未来 5 天收益
```

伪代码：

```python
sequence = features[t - 29 : t + 1]
hidden_states = gru(sequence)
last_hidden = hidden_states[-1]
prediction = linear_head(last_hidden)
```

这种结构适合把整个过去窗口压缩成一个表示。

## many-to-many

GRU 也可以每个时间步输出一个预测。

例如：

```text
每分钟盘口特征 -> 每分钟交易信号
```

伪代码：

```python
hidden_states = gru(sequence)
predictions = [linear_head(h) for h in hidden_states]
```

要注意：

```text
第 t 步预测只能使用 t 时刻之前或当时可见的数据。
```

## sequence length

窗口长度是 GRU 的重要超参数。

```python
total_steps = 1000
sequence_length = 50

num_sequences = total_steps - sequence_length + 1

print(num_sequences)
```

结果：

```text
951
```

窗口越长，模型看到的历史越多。

但窗口太长也可能：

- 加入噪声。
- 降低样本数量。
- 增加训练难度。
- 增加过拟合风险。

## GRU 在量化中的用途

GRU 可以用于：

- 收益率序列预测。
- 高频盘口序列。
- 因子时间窗口建模。
- regime 状态序列。
- 多资产序列表示。

相比 LSTM，GRU 参数更少。

在样本较少、训练成本敏感的量化任务里，GRU 经常是一个合理候选。

但它仍然需要和简单基线比较：

- 线性模型。
- 树模型。
- 简单 rolling 特征。
- LSTM。

## 标准化和泄露

GRU 输入也必须标准化。

标准化参数只能在训练期估计。

```python
train_values = [2.0, 4.0, 6.0]
valid_values = [8.0]

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
4.0
1.632993161855452
[2.449489742783178]
```

不要用全样本 fit 标准化器。

否则未来信息会进入训练过程。

## 训练风险

GRU 常见风险：

- 样本少。
- 标签噪声大。
- 模型对 seed 敏感。
- sequence length 选择过拟合。
- 输入窗口含未来信息。
- 标准化泄露。
- 训练 loss 下降但交易指标无改善。

金融时间序列里，模型复杂度通常不是最大瓶颈。

数据质量、非平稳和验证方式更关键。

## 时间序列验证

GRU 必须用时间切分验证。

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    scaler.fit(raw_features[train_period])

    train_sequences = build_sequences(
        scaler.transform(raw_features[train_period])
    )
    valid_sequences = build_sequences(
        scaler.transform(raw_features[valid_period])
    )

    model = GRUModel(config)
    model.fit(train_sequences, y_train, valid_data=(valid_sequences, y_valid))
    pred = model.predict(valid_sequences)
    score = evaluate_net_performance(pred, y_valid, costs[valid_period])
```

所有序列构造都要遵守：

```text
输入窗口不能包含标签期的信息。
```

## 常见误区

第一，认为 GRU 比 LSTM 简单，所以不会过拟合。

第二，窗口构造包含未来数据。

第三，标准化用全样本。

第四，只看训练 loss。

第五，不和简单 rolling 特征比较。

第六，不检查不同 random seed 稳定性。

第七，忽略交易成本和换手。

## 小结

GRU 是一种门控 RNN。

它用：

```text
update gate 控制保留多少旧状态
reset gate 控制候选状态参考多少过去
candidate hidden state 表示新信息
```

相比 LSTM，GRU 结构更简单、参数更少。

在量化机器学习里，GRU 可以作为序列模型候选。

但最终是否有价值，要看：

```text
时间样本外验证
和简单基线比较
无未来信息泄露
扣成本后是否提升
跨 seed 和跨 regime 是否稳定
```
