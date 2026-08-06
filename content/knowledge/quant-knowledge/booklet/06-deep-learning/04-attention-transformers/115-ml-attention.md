# Attention

## 核心概念

attention 是注意力机制。

它的核心问题是：

```text
当前 token 应该从其他 token 中读取多少信息？
```

在时间序列里，可以理解为：

```text
预测当前时点时，模型应该关注哪些历史时点？
```

attention 会为不同 token 分配权重。

权重越大，表示当前计算中更多使用该 token 的 value。

但要注意：

```text
attention 权重不是因果解释。
```

它只是模型内部的一种加权机制。

从信息流角度，attention 不是静态地给输入贴“重要性”标签，而是一次随 query 改变的动态检索。同一个历史时点面对不同预测位置或不同样本，可以得到完全不同的权重。

## query、key、value

attention 使用三个向量：

```text
query: 当前 token 想找什么
key: 其他 token 提供的匹配索引
value: 真正被读取的信息内容
```

流程：

```text
query 和 key 算相似度
相似度经过 softmax 得到权重
权重对 value 加权求和
```

小例子：

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

## softmax 权重

相似度分数要经过 softmax，变成非负且总和为 `1` 的权重。

```python
import math

scores = [1.0, 0.0]

exp_scores = [math.exp(score) for score in scores]
total = sum(exp_scores)
weights = [
    score / total
    for score in exp_scores
]

print(weights)
print(sum(weights))
```

结果：

```text
[0.7310585786300049, 0.2689414213699951]
1.0
```

第一个 token 的权重更高。

但第二个 token 也还有一定权重。

数值实现通常先从每组 score 中减去最大值，再计算指数。减去同一个常数不会改变 softmax 结果，却可以降低指数溢出风险。softmax 输出和为 1 只说明它形成了归一化权重，不说明这些权重已经校准或具有因果含义。

## 温度和尖锐程度

如果 score 差距很大，softmax 会很尖锐。

```python
import math

scores = [5.0, 0.0]

exp_scores = [math.exp(score) for score in scores]
total = sum(exp_scores)
weights = [score / total for score in exp_scores]

print(weights)
```

结果：

```text
[0.9933071490757153, 0.006692850924284856]
```

第一个 token 几乎拿到全部权重。

这就是为什么 scaled dot-product 要除以 `sqrt(d_k)`。

否则维度高时 dot product 过大，softmax 可能过于尖锐。

## scaled dot-product

scaled dot-product attention 使用：

```text
score = q · k / sqrt(d_k)
```

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

缩放不会改变机制本质。

它让训练更稳定。

## 加权 value

attention 输出是 value 的加权和。

```python
weights = [0.75, 0.25]
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
[1.5, 1.0]
```

注意力不是选择一个 token。

它通常是对多个 value 做加权组合。

## self-attention

self-attention 表示 query、key、value 都来自同一个序列。

例如时间序列窗口：

```text
t-3, t-2, t-1, t
```

每个位置都可以关注窗口内其他位置。

```python
values = [0.01, -0.02, 0.03, 0.00]
weights_for_last_token = [0.1, 0.2, 0.6, 0.1]

context = sum(
    weight * value
    for weight, value in zip(weights_for_last_token, values)
)

print(context)
```

结果：

```text
0.015
```

最后一个位置主要关注 `t-1`，因为权重是 `0.6`。

## cross-attention

cross-attention 中，query 来自一个序列，key/value 来自另一个序列。

例如：

```text
query: 某只股票的表示
key/value: 市场或行业上下文
```

伪代码：

```python
stock_query = stock_encoder(stock_features)
market_keys, market_values = market_encoder(market_features)
stock_context = attention(stock_query, market_keys, market_values)
```

cross-attention 在多源数据中常见。

例如价格序列关注新闻序列，或个股关注市场状态序列。

## multi-head attention

multi-head attention 是多组 attention 并行。

每个 head 可以学习不同的关注模式。

例如：

```text
head 1 关注最近几天
head 2 关注波动率突变
head 3 关注月度周期
```

小例子：两个 head 的输出拼接。

```python
head_1 = [0.1, 0.2]
head_2 = [-0.3, 0.4]

combined = head_1 + head_2

print(combined)
```

结果：

```text
[0.1, 0.2, -0.3, 0.4]
```

真实模型里，拼接后通常还会接一个线性层。

多头通常不是复制多个完整的 `d_model` attention。若总维度是 `d_model`、头数是 `h`，常见做法是让每个头使用 `d_model / h` 维，再把结果拼回总维度并通过输出投影 `W_O` 融合。

每个 head 获得独立投影视角，但不能预先断言“第一个头必然看短期、第二个头必然看波动”。这些模式若存在，也是训练中学到的，且未必稳定或具有人类可命名语义。

## head 维度

如果 `d_model = 64`，`num_heads = 4`，每个 head 的维度通常是：

```python
d_model = 64
num_heads = 4

head_dim = d_model // num_heads

print(head_dim)
```

结果：

```text
16
```

多头不是免费增加信息。

如果 head 太多，每个 head 维度太小，也可能影响表达能力。

## attention mask

mask 用来禁止某些 token 被关注。

常见 mask：

- padding mask：忽略补齐位置。
- causal mask：禁止看未来。
- custom mask：按业务规则限制关注范围。

小例子：把被 mask 的分数设成很小。

```python
scores = [1.0, 0.5, 2.0]
mask = [True, True, False]

masked_scores = [
    score if keep else -1_000_000.0
    for score, keep in zip(scores, mask)
]

print(masked_scores)
```

结果：

```text
[1.0, 0.5, -1000000.0]
```

经过 softmax 后，被 mask 的位置权重会接近 `0`。

mask 应在 softmax 前加入分数，并使用与框架约定一致的布尔方向或加性负无穷语义。causal mask 与 padding mask 合并错误，既可能泄露未来，也可能把有效历史全部遮掉。

## causal mask

时间序列预测常用 causal mask。

它保证第 `t` 个位置不能看未来位置。

```python
sequence_length = 3

causal_mask = []
for i in range(sequence_length):
    row = []
    for j in range(sequence_length):
        row.append(j <= i)
    causal_mask.append(row)

print(causal_mask)
```

结果：

```text
[[True, False, False], [True, True, False], [True, True, True]]
```

如果做自回归预测但没有 causal mask，就可能泄露未来。

## attention 和解释

attention 权重看起来像解释。

但要谨慎。

高权重只说明：

```text
这个模型在这一次前向传播中，从这个 token 的 value 读了较多信息。
```

它不必然表示：

- 这个时点因果上重要。
- 这个特征有稳定 alpha。
- 这个 token 对最终收益真的有贡献。
- attention 权重稳定。

attention 权重还会受 value、残差连接、后续层、归一化和 MLP 影响。

## 注意力稳定性

可以检查不同样本或不同时间窗口的 attention 是否稳定。

```python
weights_day_1 = [0.1, 0.2, 0.7]
weights_day_2 = [0.2, 0.2, 0.6]

difference = sum(
    abs(a - b)
    for a, b in zip(weights_day_1, weights_day_2)
)

print(difference)
```

结果：

```text
0.19999999999999996
```

如果 attention 权重剧烈变化，解释就不稳定。

## 时间序列里的常见关注模式

在金融时间序列里，attention 可能学到：

- 关注最近时点。
- 关注波动突变时点。
- 关注成交量异常时点。
- 关注月末、财报日、事件日。
- 关注 regime 切换前后的时点。

但这些模式必须用样本外验证支持。

不能只看一张 attention heatmap 就下结论。

## attention 的计算成本

标准 attention 要计算每两个 token 的关系。

```python
for sequence_length in [20, 100, 500]:
    pair_count = sequence_length ** 2
    print(sequence_length, pair_count)
```

结果：

```text
20 400
100 10000
500 250000
```

序列越长，计算和内存成本增长很快。

## 自回归推理与 KV cache

训练时整段目标通常已知，可以在 causal mask 下并行计算；自回归推理则必须逐 token 生成。若每一步都重新处理完整前缀，历史 token 的线性投影、前馈层和注意力会反复计算。

KV cache 保存每一层历史 token 的 key 和 value。生成新 token 时，只计算当前 token 的 query/key/value，并让当前 query 读取缓存中的历史 K/V。过去的 query 已经完成过去位置的输出，通常无需再缓存。

这不会消除当前 query 对全部历史位置的 attention。缓存还会随层数、KV head 数、序列长度和 head dimension 增长，因此它是：

```text
更多显存  <->  更少前缀重复计算
```

在服务端还要处理不同请求长度、批处理重排、分页和缓存回收，不能只看单条序列的理论节省。

## 量化建模注意事项

用 attention 做量化时间序列时，要检查：

- 是否有 causal mask。
- 输入窗口是否含未来。
- 位置或时间编码是否合理。
- 序列长度是否过长。
- attention 权重是否稳定。
- 是否和简单模型比较。
- 扣成本后是否仍有提升。

尤其是：

```text
attention 很强，但不能修复错误的数据对齐。
```

## 小结

attention 用 query、key、value 计算信息读取权重。

核心步骤：

```text
query-key 相似度
softmax 权重
加权 value
多头并行
mask 限制可见范围
```

在时间序列里，attention 可以建模不同历史时点之间的关系。

但要记住：

```text
attention 权重不是因果解释
没有 mask 会泄露未来
长序列成本很高
样本外验证仍然是最终标准
```

## 延伸阅读与来源

- [Datawhale / jshn9515 Deep Learning Notes](https://datawhalechina.github.io/deep-learning-notes/zh/index.html)：用于核对 Q/K/V 分工、多头维度、mask 与 KV cache 解释；原资料采用 CC BY-NC 4.0。
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)：核对 scaled dot-product 与 multi-head attention。
- 本章补充内容为面向量化时间序列信息可见性和推理成本的原创归纳。
