# Transformer for Time Series

## 核心概念

Transformer for TS 是用于 time series 的 Transformer。

Transformer 原本常用于 NLP。

它的核心机制是 attention。

在时间序列里，它可以让模型在一个窗口内学习：

```text
当前预测应该关注哪些历史时点？
```

例如：

```text
预测 t+1 的收益时，模型可能关注 t、t-1、t-5、t-20 等时点。
```

和 RNN / LSTM / GRU 不同，Transformer 不一定按顺序一步步递推。

它可以并行处理整个序列窗口。

## 时间序列 token

在 NLP 中，一个 token 可以是一个词。

在时间序列中，一个 token 通常是一个时点的特征向量。

例如：

```text
过去 20 天
每天 6 个特征
```

就可以看成：

```text
20 个 token，每个 token 是 6 维向量
```

小例子：

```python
sequence_length = 20
feature_dim = 6

num_input_values = sequence_length * feature_dim

print(num_input_values)
```

结果：

```text
120
```

一个样本包含 `120` 个输入数值。

## embedding

Transformer 通常先把原始特征映射到模型维度 `d_model`。

```text
raw feature_dim -> d_model
```

比如：

```text
6 维原始特征 -> 32 维 embedding
```

小例子：

```python
feature_dim = 6
d_model = 32

linear_projection_params = feature_dim * d_model + d_model

print(linear_projection_params)
```

结果：

```text
224
```

这里包括权重和 bias。

## 为什么需要位置编码

attention 本身不天然知道顺序。

如果不给位置信息，它只看到一组 token。

时间序列里，顺序非常重要。

```text
t-1 和 t-20 不是同一个含义
```

所以 Transformer 要加入 positional encoding 或 temporal embedding。

位置编码可以告诉模型：

```text
这个 token 位于序列的第几个位置
```

更精确地说，不含位置信息的 self-attention 对排列是等变的：如果把输入 token 一起换序，输出只会跟着换序。模型仍能比较内容，却不知道相同内容出现在 `t-1` 还是 `t-20`。

位置表示可以提供不同类型的归纳偏置：

- 固定正弦位置编码：用不同频率提供绝对位置坐标。
- 可学习位置向量：直接从训练数据学习每个位置的表示。
- 相对位置或旋转位置编码：更直接地表达 token 之间的距离或相对关系。

原始设计把 token embedding 与同维度位置向量相加，因此不会改变 `d_model`。相加很简洁，但不是唯一选择；训练窗口以外的长度外推能力也需要单独验证。

## 简单位置编码

最简单的位置编码可以是位置编号。

```python
sequence_length = 5

positions = list(range(sequence_length))

print(positions)
```

结果：

```text
[0, 1, 2, 3, 4]
```

真实 Transformer 会把位置编号映射成向量。

例如：

```text
position 0 -> vector
position 1 -> vector
...
```

后面 `temporal embedding` 会单独展开。

## query、key、value

attention 里每个 token 会生成三个向量：

```text
query: 我想找什么信息
key: 我提供什么索引信息
value: 我真正携带的内容
```

注意力权重由 query 和 key 的相似度决定。

然后用这些权重加权 value。

可以把它理解成一次动态检索：query 表达当前时点需要什么，key 提供每个历史时点用于匹配的索引，value 承载真正被读取的内容。Q、K、V 是三个可学习角色，不代表它们必须对应三种人工指定的金融含义。

简化：

```text
attention_scores = Q K^T
attention_weights = softmax(attention_scores)
output = attention_weights V
```

## dot-product attention

先看一个最小例子。

一个 query 和两个 key。

```python
query = [1.0, 0.0]
keys = [
    [1.0, 0.0],
    [0.0, 1.0],
]

scores = [
    sum(q * k for q, k in zip(query, key))
    for key in keys
]

print(scores)
```

结果：

```text
[1.0, 0.0]
```

query 和第一个 key 更相似。

所以第一个 token 会得到更高注意力。

## softmax

attention score 会经过 softmax，变成权重。

```python
import math

scores = [1.0, 0.0]

exp_scores = [math.exp(score) for score in scores]
total = sum(exp_scores)
weights = [
    value / total
    for value in exp_scores
]

print(weights)
```

结果：

```text
[0.7310585786300049, 0.2689414213699951]
```

权重和为 `1`。

第一个 token 权重更大。

## 加权 value

有了注意力权重，就对 value 做加权平均。

```python
weights = [0.7310585786300049, 0.2689414213699951]
values = [
    [2.0, 0.0],
    [0.0, 4.0],
]

output = []
for dim in range(len(values[0])):
    output.append(sum(
        weight * value[dim]
        for weight, value in zip(weights, values)
    ))

print(output)
```

结果：

```text
[1.4621171572600098, 1.0757656854799804]
```

输出是两个 value 的加权组合。

## scaled dot-product

Transformer 会把 dot product 除以 `sqrt(d_k)`。

```text
score = q · k / sqrt(d_k)
```

这样可以避免维度高时 score 太大，softmax 过于尖锐。

```python
import math

dot_product = 8.0
d_k = 4

scaled_score = dot_product / math.sqrt(d_k)

print(scaled_score)
```

结果：

```text
4.0
```

维度越高，缩放越重要。

## self-attention

self-attention 表示：

```text
同一个序列内部的 token 互相关注。
```

例如三个时间点：

```text
t-2, t-1, t
```

每个时间点都可以根据注意力权重聚合其他时间点的信息。

```python
attention_weights_for_t = [0.2, 0.3, 0.5]
values = [0.01, 0.02, -0.01]

context = sum(
    weight * value
    for weight, value in zip(attention_weights_for_t, values)
)

print(context)
```

结果：

```text
0.003
```

当前时点的表示包含了历史几个时点的信息。

## causal mask

做时间序列预测时，不能让过去位置看到未来。

causal mask 用来禁止 attention 看未来 token。

例如长度为 4 的序列。

第 0 个位置只能看 0。

第 1 个位置能看 0、1。

第 2 个位置能看 0、1、2。

```python
sequence_length = 4

mask = []
for i in range(sequence_length):
    row = []
    for j in range(sequence_length):
        row.append(j <= i)
    mask.append(row)

print(mask)
```

结果：

```text
[[True, False, False, False], [True, True, False, False], [True, True, True, False], [True, True, True, True]]
```

`False` 的位置表示不能看。

如果没有 causal mask，模型可能使用未来信息。

mask 应在 softmax 之前作用到 score。causal mask 遮住未来位置，padding mask 遮住补齐位置；两者目的不同，但在变长序列中常需要同时正确合并。若在 softmax 后才把权重置零，剩余权重还需要重新归一化，否则输出口径已经改变。

## many-to-one 预测

很多金融任务是：

```text
过去 T 个时点 -> 未来一个收益标签
```

常见做法：

- 用最后一个 token 的输出做预测。
- 加一个 special token 汇总序列。
- 对所有 token pooling 后预测。

伪代码：

```python
emb = input_projection(sequence)
emb = emb + positional_encoding
encoded = transformer_encoder(emb, causal_mask=True)
last_state = encoded[-1]
prediction = linear_head(last_state)
```

注意：

```text
输入 sequence 只能包含预测时点可见的信息。
```

## many-to-many 预测

也可以每个时间点输出一个预测。

例如：

```text
每分钟盘口特征 -> 每分钟下一分钟收益预测
```

伪代码：

```python
encoded = transformer_encoder(emb, causal_mask=True)
predictions = [linear_head(state) for state in encoded]
```

这时标签对齐尤其关键。

第 `t` 个输出不能预测时使用 `t+1` 之后的信息。

## encoder-only 和 decoder-only

时间序列 Transformer 常见两类：

```text
encoder-only:
    输入一个历史窗口，输出预测

decoder-only:
    用 causal mask 自回归建模
```

量化预测里，很多任务用 encoder-only 就够了。

如果做逐步生成或自回归预测，decoder-only 更常见。

## Transformer 和 RNN 的差别

RNN / LSTM / GRU：

```text
按时间顺序递推隐藏状态
```

Transformer：

```text
用 attention 在窗口内直接连接不同时间点
```

优点：

- 并行度更高。
- 长距离依赖更直接。
- 容易扩展到多变量序列。

缺点：

- 对数据量要求高。
- 注意力计算成本随序列长度增长。
- 容易过拟合。
- 位置和时间信息需要额外设计。

## 注意力复杂度

标准 self-attention 需要计算每两个 token 的关系。

复杂度大约是：

```text
O(T^2)
```

其中 `T` 是 sequence length。

```python
for sequence_length in [10, 100, 1000]:
    num_pair_scores = sequence_length ** 2
    print(sequence_length, num_pair_scores)
```

结果：

```text
10 100
100 10000
1000 1000000
```

长序列会非常贵。

所以时间序列 Transformer 常需要控制窗口长度。

## 量化中的输入设计

Transformer for TS 的输入可以是：

- 每日因子序列。
- 每分钟成交量和收益率序列。
- order book 多档盘口。
- 多资产相关特征。
- 宏观变量时间序列。

常见特征：

```text
return
volatility
volume
spread
order imbalance
cross-sectional rank
calendar feature
regime feature
```

输入设计仍然比模型结构更重要。

## 标准化和泄露

Transformer 输入通常也要标准化。

标准化只能用训练期统计量。

```python
train_values = [1.0, 2.0, 3.0, 4.0]
test_value = 5.0

train_mean = sum(train_values) / len(train_values)
train_std = (
    sum((x - train_mean) ** 2 for x in train_values) / len(train_values)
) ** 0.5

scaled_test = (test_value - train_mean) / train_std

print(train_mean)
print(train_std)
print(scaled_test)
```

结果：

```text
2.5
1.118033988749895
2.23606797749979
```

不能用全样本均值和标准差。

## 时间序列验证

Transformer 必须按时间验证。

伪代码：

```python
for train_period, valid_period in walk_forward_splits:
    scaler.fit(raw_features[train_period])
    train_seq = build_sequences(scaler.transform(raw_features[train_period]))
    valid_seq = build_sequences(scaler.transform(raw_features[valid_period]))

    model = TransformerTimeSeries(config)
    model.fit(train_seq, y_train, valid_data=(valid_seq, y_valid))
    pred = model.predict(valid_seq)
    score = evaluate_net_performance(pred, y_valid, costs[valid_period])
```

必须检查：

- 输入窗口是否含未来。
- mask 是否正确。
- 标签是否正确 shift。
- 标准化是否泄露。
- early stopping 是否只看验证集。

## 常见误区

第一，没有 causal mask，却做自回归预测。

第二，位置编码或时间特征设计不清楚。

第三，输入窗口包含标签期信息。

第四，序列太长，模型巨大，样本太少。

第五，只看训练 loss，不看样本外净收益。

第六，不和 LSTM、GRU、树模型和线性模型比较。

第七，以为 attention 权重就是因果解释。

第八，把位置编码当成自然时间间隔本身；不规则交易日、停牌和跨市场日历仍需显式时间特征。

## 小结

Transformer for TS 用 self-attention 处理时间序列窗口。

它的关键组件是：

```text
token / embedding
query, key, value
scaled dot-product attention
positional encoding
causal mask
prediction head
```

在量化机器学习里，Transformer 的优势是表达能力强、能直接建模远距离关系。

但风险同样明显：

```text
需要更多数据
更容易过拟合
更容易因 mask 或对齐错误泄露未来
解释更困难
计算成本更高
```

所以它必须在严格时间样本外验证和扣成本评估下使用。

## 延伸阅读与来源

- [Datawhale / jshn9515 Deep Learning Notes](https://datawhalechina.github.io/deep-learning-notes/zh/index.html)：用于核对 self-attention、位置编码、mask 与 Transformer 结构直觉；原资料采用 CC BY-NC 4.0。
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)：核对 scaled dot-product attention、multi-head attention 与正弦位置编码。
- 本章补充内容为面向时间序列可见性和长度外推的原创归纳。
