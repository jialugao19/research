# 111. 归一化统计维度：Batch、Layer、Instance 与 Group

## 核心概念

归一化方法的共同骨架很相似：计算一组元素的均值和方差，再做中心化、尺度调整和可学习仿射变换。真正不同的是：

```text
哪些元素共享同一组统计量？
```

对图像张量 `(N, C, H, W)`：

- BatchNorm 固定通道，沿 `N, H, W` 统计。
- LayerNorm 固定样本，按 `normalized_shape` 覆盖的尾部维度统计。
- InstanceNorm 固定样本和通道，沿 `H, W` 统计。
- GroupNorm 固定样本和通道组，沿组内通道、`H, W` 统计。

四种方法不是四套互不相关的公式。更稳定的理解顺序是：先圈出共享同一组统计量的元素集合，再确定哪些维度被保留，最后检查仿射参数、训练/推理模式和框架默认值。

## 为什么标准化后还要仿射变换

若标准化永远强制输出保持零均值、单位方差，可能会移除网络已经学到的有用尺度。因此常在标准化后加入可学习参数：

```text
x_hat = (x - mean) / sqrt(variance + epsilon)
y = gamma * x_hat + beta
```

`gamma` 和 `beta` 让模型在统一坐标系上重新选择合适尺度和偏移。它们不会改变“哪些元素共享统计量”，但参数形状可能不同：BatchNorm 通常每通道一组，LayerNorm 通常与 `normalized_shape` 同形。

## 统计维度和保留维度

“统计维度”会被均值与方差归约；“保留维度”决定要维护多少组独立统计量。下面用 NumPy 直接观察形状：

```python
import numpy as np

x = np.arange(2 * 4 * 3 * 3, dtype=float).reshape(2, 4, 3, 3)

batch_norm_mean = x.mean(axis=(0, 2, 3), keepdims=True)
layer_norm_mean = x.mean(axis=(1, 2, 3), keepdims=True)
instance_norm_mean = x.mean(axis=(2, 3), keepdims=True)

print("BatchNorm stats:", batch_norm_mean.shape)
print("LayerNorm stats:", layer_norm_mean.shape)
print("InstanceNorm stats:", instance_norm_mean.shape)
```

输出形状分别是 `(1, C, 1, 1)`、`(N, 1, 1, 1)` 和 `(N, C, 1, 1)`。

## GroupNorm 的 reshape 视角

若通道数 `C=4`，分成 `G=2` 组，可先把输入改写为 `(N, G, C/G, H, W)`，再沿最后三个维度统计：

```python
groups = 2
n, c, h, w = x.shape
grouped = x.reshape(n, groups, c // groups, h, w)
group_mean = grouped.mean(axis=(2, 3, 4), keepdims=True)

print(grouped.shape)
print(group_mean.shape)
```

这让两个边界关系非常直观：

```text
G = C：每组一个通道，统计方式等价于 InstanceNorm。
G = 1：所有通道和空间位置共享统计量，范围接近 LayerNorm(C,H,W)。
```

“统计方式接近”不代表 API 完全相同。GroupNorm 默认仿射参数通常按通道设置；LayerNorm 的参数形状由 `normalized_shape` 决定。

## batch 依赖

BatchNorm 的当前样本会受到 batch 中其它样本影响，训练期还会更新 running statistics。因此：

- 小 batch 下统计噪声可能很大。
- 多卡训练的 local batch 不同会改变统计口径。
- 训练和推理使用的统计量不同。

训练期当前 batch 的方差、running variance 的更新口径以及框架中的 `momentum` 定义可能不同。需要复现实验时，应以具体框架文档和保存的 state 为准，不要只根据手写公式猜测。

InstanceNorm 与 GroupNorm 不跨样本，通常训练和推理使用同一种当前输入统计方式，也不需要跨设备同步 batch statistics。

## 方法选择

可以从任务与张量语义出发：

- 大 batch CNN 分类：BatchNorm 是常见基线。
- Transformer token 表示：通常使用 LayerNorm 或 RMSNorm。
- 风格迁移和部分生成任务：InstanceNorm 可弱化实例级对比度与风格统计。
- 小 batch 检测、分割和高分辨率 CNN：GroupNorm 常比 BatchNorm 稳定。

不要只按“batch 小”机械选择。InstanceNorm 可能移除分类需要的绝对外观信息；GroupNorm 的组数也需要随通道数和 backbone 验证。

## 时间序列中的维度检查

时间序列常用 `(batch, time, feature)`。此时不能把图像里的 `C, H, W` 解释直接照搬。先写清楚想让哪些位置共享统计量：

```text
每个时点独立规范 feature？
同一样本跨 time 统计？
跨 batch 统计是否会让当前样本受其它样本影响？
训练和线上 batch 口径是否一致？
```

若把测试期未来时点也放进同一个统计集合，甚至可能形成时间泄漏。

## 常见坑

- 只说“LayerNorm 在样本内归一化”，却不写 `normalized_shape` 覆盖哪些尾部维度。
- GroupNorm 的 `num_groups` 不能整除通道数。
- 训练使用 BatchNorm，小 batch 推理或分布漂移时仍相信旧 running statistics。
- 把 `train()` / `eval()` 行为差异混淆为模型参数变化。
- 在时间序列上跨未来窗口计算均值和方差。
- 忽略 `affine`、`track_running_stats` 和 `epsilon` 的框架默认值。

## 自检问题

1. 对 `(N,C,H,W)` 输入，四种方法分别沿哪些维度统计？
2. 为什么 `GroupNorm(C,C)` 与 InstanceNorm 的统计方式等价？
3. 为什么 `GroupNorm(1,C)` 与 LayerNorm 仍可能有参数化差异？
4. 时间序列归一化如何避免未来信息泄漏？
5. gamma 与 beta 为什么不等于撤销归一化？它们的参数形状由什么决定？

## 延伸阅读与来源

- [Datawhale / jshn9515 Deep Learning Notes](https://datawhalechina.github.io/deep-learning-notes/zh/index.html)：用于核对归一化统一视角；原资料采用 CC BY-NC 4.0。
- [Instance Normalization paper](https://arxiv.org/abs/1607.08022) 与 [Group Normalization paper](https://arxiv.org/abs/1803.08494)：核对原始动机与实验边界。
- [PyTorch normalization layers](https://pytorch.org/docs/stable/nn.html#normalization-layers)：核对输入形状和默认参数。
- 本文为面向图像与时间序列维度审计的原创归纳。
