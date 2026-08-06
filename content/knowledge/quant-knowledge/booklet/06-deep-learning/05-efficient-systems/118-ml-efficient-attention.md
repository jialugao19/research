# 118. 高效 Attention：IO 瓶颈与 FlashAttention

## 核心概念

标准 attention 的计算可以写成：

```text
scores = Q @ K.T
probabilities = softmax(scores)
output = probabilities @ V
```

复杂度是 `O(N^2 * d)`。但运行慢不一定只是 FLOPs 太多；若实现显式保存 `N x N` 的 scores 和 probabilities，它们还要在显存中反复写入和读取，长序列会形成严重 IO 压力。

FlashAttention 的关键不是近似，而是改变执行顺序：分块计算、融合算子，用 online softmax 边扫描边维护归一化统计量，不把完整注意力矩阵落到 HBM。

## 先估算中间矩阵

单个 `float32` 的 `N x N` 矩阵占用：

```python
def matrix_mib(sequence_length, bytes_per_value=4):
    return sequence_length ** 2 * bytes_per_value / 1024 ** 2


for n in [512, 1024, 4096, 8192]:
    print(n, matrix_mib(n))
```

`N=4096` 时，一个矩阵约为 `64 MiB`。标准实现还可能保存 softmax 结果、多头、多 batch 和反向中间状态，所以不能只用这一个数字估峰值显存。

## 为什么是 IO 问题

两次大矩阵乘法本身适合 GPU。但如果中间的 scores 写回 HBM，softmax 再读出、写回 probabilities，最后第二次矩阵乘法又读入 probabilities，数据搬运可能限制吞吐。

因此性能分析至少同时记录：

- FLOPs。
- 峰值中间状态。
- HBM 读写量。
- 算术强度。
- 实际 kernel、dtype 和张量形状。

“计算量大”不自动等于 compute-bound。

## online softmax

普通稳定 softmax 先减去全局最大值。如果分块读取分数，每个块有自己的最大值，合并时必须把旧统计量和新块重新缩放到同一标尺。

下面用纯 Python 合并两个块，并与一次性 softmax 比较：

```python
import math


def summarize_block(values):
    maximum = max(values)
    normalizer = sum(math.exp(value - maximum) for value in values)
    return maximum, normalizer


def merge_summaries(left, right):
    left_max, left_sum = left
    right_max, right_sum = right
    new_max = max(left_max, right_max)
    new_sum = (
        math.exp(left_max - new_max) * left_sum
        + math.exp(right_max - new_max) * right_sum
    )
    return new_max, new_sum


scores = [1.0, 3.0, -2.0, 4.0]
merged = merge_summaries(
    summarize_block(scores[:2]),
    summarize_block(scores[2:]),
)
whole = summarize_block(scores)

print("merged:", merged)
print("whole:", whole)
```

真实 FlashAttention 还会同步维护加权 `V` 的输出累积。当新块出现更大最大值时，旧输出也要按新标尺重缩放。

## FlashAttention 改了什么

核心流程是：

```text
把 Q 分成行块
把 K、V 分成列块
在片上存储计算局部分数
更新每行最大值、归一化和与输出累积
只把最终输出写回 HBM
```

反向传播通常不保存完整 probabilities，而是根据前向保存的小统计量重算局部块。这是用额外计算换更少的显存读写。

FlashAttention 仍然计算密集标准 attention，复杂度没有变成 `O(N)`。它也不保证所有形状更快：短序列、小 batch、不受支持的 head dimension 或特殊 mask 都可能让收益变小，甚至触发普通后端回退。

## 框架使用检查

使用框架 fused attention 时检查：

- Q、K、V 的 batch、head、sequence、dimension 顺序。
- causal mask、padding mask 和自定义 mask 的广播语义。
- dtype、设备和 head dimension 是否支持目标后端。
- 是否真的命中 FlashAttention kernel，而不是静默回退。
- 前向输出和反向梯度是否与参考实现一致。
- benchmark 是否预热、同步并重复多次。

不要为了命中高效 kernel 改错 mask。对时间序列预测，causal 语义错误会直接造成未来信息泄漏。

## 公平 benchmark

固定这些变量后再比较：

```text
batch size
number of heads
sequence length
head dimension
dtype
causal / padding mask
dropout
training or inference mode
```

同时报告峰值显存、预热后延迟、吞吐和输出误差。训练 benchmark 要包含 backward；自回归推理还要把 KV cache 单独纳入口径。

## 常见坑

- 用第一次运行计时，把编译和缓存初始化算进 steady-state 延迟。
- 只比较前向，没有比较梯度。
- 一个实现启用 dropout，另一个关闭。
- 只看理论复杂度，不确认实际执行 kernel。
- 把 FlashAttention 误解成稀疏或近似 attention。
- 时间序列 mask 方向写反，模型看到未来。

## 自检问题

1. 为什么 `O(N^2 d)` 的算子不一定 compute-bound？
2. online softmax 合并新块时为什么要重缩放旧统计量？
3. FlashAttention 为什么仍是精确 attention？
4. 怎样证明性能提升不是由 dtype、mask 或 dropout 不一致造成？

## 延伸阅读与来源

- [Datawhale / jshn9515 Deep Learning Notes](https://datawhalechina.github.io/deep-learning-notes/zh/index.html)：用于核对 Attention IO 与 FlashAttention 的教学主线；原资料采用 CC BY-NC 4.0。
- [FlashAttention paper](https://arxiv.org/abs/2205.14135)：核对 IO-aware 精确 attention 的算法与复杂度。
- [PyTorch scaled dot product attention](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)：核对框架接口和后端选择。
- 本文为面向性能测量与时间序列防泄漏的原创归纳。
