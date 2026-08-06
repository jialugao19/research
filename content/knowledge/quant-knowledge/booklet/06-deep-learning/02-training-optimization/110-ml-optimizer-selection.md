# 110. 优化器选择：AdamW、Muon 与参数分组

## 核心概念

AdamW 和 Muon 解决的不是同一个问题：

```text
AdamW：把权重衰减与 Adam 的自适应梯度缩放解耦。
Muon：把二维隐藏层权重当作矩阵，对动量更新做近似正交化。
```

因此，现代训练中常见的做法不是“二选一”，而是显式参数分组：二维 hidden weight 可以实验 Muon，bias、normalization、embedding 和其它参数继续使用 AdamW。

## L2 正则和 weight decay 的差别

在普通 SGD 中，把 `lambda * weight` 加到梯度，与每步按比例缩小参数可以建立对应关系。但 Adam 会按每个坐标的二阶矩缩放梯度。如果 L2 惩罚混进梯度，它也会被不同尺度地处理。

AdamW 把衰减单独作用在参数上：

```text
parameter = (1 - learning_rate * weight_decay) * parameter
parameter = parameter - adaptive_adam_update
```

下面的最小例子展示“先混进梯度”和“解耦衰减”的操作位置不同：

```python
parameter = 2.0
task_gradient = 0.4
learning_rate = 0.1
weight_decay = 0.05
preconditioner = 0.5

l2_mixed = parameter - learning_rate * (
    task_gradient + weight_decay * parameter
) * preconditioner

adamw = (
    parameter * (1.0 - learning_rate * weight_decay)
    - learning_rate * task_gradient * preconditioner
)

print(l2_mixed, adamw)
```

真实 AdamW 还维护偏差修正后的一阶和二阶矩；这里仅用固定 `preconditioner` 表示自适应缩放。

## 哪些参数通常不衰减

常见经验是不给 bias 与归一化缩放参数做 weight decay，但这不是无需验证的定律。关键是把规则写成可审计的参数组，而不是依赖名称模糊匹配后不检查。

```python
parameter_names = [
    "encoder.weight",
    "encoder.bias",
    "norm.weight",
    "embedding.weight",
]

decay = []
no_decay = []

for name in parameter_names:
    if name.endswith(".bias") or "norm." in name:
        no_decay.append(name)
    else:
        decay.append(name)

print("decay:", decay)
print("no_decay:", no_decay)
```

实际项目还应检查共享参数、输出头和 embedding 是否符合规则，并验证每个可训练参数只出现一次。

## Muon 在做什么

Muon 先形成矩阵梯度的动量，再把整个更新矩阵映射到更均衡的奇异值尺度。直觉上，它利用了二维权重的矩阵结构，而不是只为每个元素设置独立步长。

完整 SVD 每步成本高，因此实现通常用有限次 Newton–Schulz 迭代近似正交化。这里有三个重要边界：

- 它主要面向二维隐藏层矩阵，不是所有张量通用的 Adam 替代品。
- 迭代前的矩阵缩放、迭代次数和最终更新缩放都是算法实现的一部分。
- embedding、bias 和 norm 等参数通常仍交给 AdamW。

## 参数分组检查

在创建优化器之前，至少检查：

```text
所有 requires_grad 参数是否都被覆盖？
是否有参数出现在两个组？
二维矩阵是否误把 embedding 或共享输出头分到 Muon？
每组的 learning rate、weight decay 和状态精度是什么？
checkpoint 能否恢复组映射和全部优化器状态？
```

参数总量可以用集合做一次机械核对：

```python
all_params = {"a", "b", "c", "d"}
adamw_group = {"b", "c", "d"}
muon_group = {"a"}

assert adamw_group.isdisjoint(muon_group)
assert adamw_group | muon_group == all_params
```

## 如何公平比较

比较纯 AdamW 与 AdamW+Muon 时要固定：

- 模型初始化和数据顺序。
- 训练 token 数或样本数。
- 学习率搜索预算。
- warmup、weight decay 和 batch size。
- 验证指标、峰值显存和端到端吞吐。

单个 optimizer step 更慢不代表总训练更慢；反过来，较快下降的训练 loss 也不代表样本外泛化更好。应同时报告达到同等验证指标所需的 wall time 和资源。

## 常见坑

- 把 AdamW 误写成在 loss 中加 L2，而没有真正解耦。
- 只按 `parameter.ndim == 2` 分组，把不合适的 embedding 交给 Muon。
- 比较优化器时给其中一个更大的调参预算。
- checkpoint 只保存模型，没有保存两个参数组的优化器状态。
- 只看最终 loss，不看更新范数、状态内存和训练稳定性。

## 自检问题

1. 为什么 L2 正则在 Adam 中不等于统一的 weight decay？
2. Muon 为什么通常只用于一部分二维参数？
3. 参数组重复或遗漏会出现什么现象？
4. 如何设计一个公平的 AdamW 与 AdamW+Muon 对照实验？

## 延伸阅读与来源

- [Datawhale / jshn9515 Deep Learning Notes](https://datawhalechina.github.io/deep-learning-notes/zh/index.html)：用于核对 AdamW 与 Muon 的课程组织；原资料采用 CC BY-NC 4.0。
- [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101)：AdamW 的原始论文。
- [Muon technical note](https://kellerjordan.github.io/posts/muon/)：Muon 的算法说明与适用参数边界。
- 本文为面向实验对照与参数审计的原创归纳。
