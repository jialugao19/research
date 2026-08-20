---
id: article-normalization-statistics
slug: normalization-statistics
title: 归一化统计维度：InstanceNorm 与 GroupNorm
concepts:
- instance-normalization
- group-normalization
learning_units:
- instance-normalization-overview
- group-normalization-overview
domain: computer_vision
level: intermediate
content_type: theory
depth_level: level_3_deep_dive
target_chars:
  minimum: 3000
  maximum: 5000
keywords:
- Instance Normalization
- InstanceNorm
- computer vision
- intermediate
- normalization
- convolutional neural network
- batch normalization
- layer normalization
profile:
  required_sections:
  - 背景与变体
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 假设与限制
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-normalization-statistics
  covered_concepts: 2
  primary_concept: instance-normalization
confidence:
  concept: 0.97
  prerequisite: 0.92
  prerequisite_path_eligible: true
generated_version:
  model: curated-catalog-v3
  prompt_version: chapter-profile-v3
review:
  state: automated_editorial
  last_review: null
  reviewer: null
  triggers:
  - high_impact_or_deep_article
  - multi_concept_article
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
- title: 'Instance Normalization: The Missing Ingredient for Fast Stylization'
  url: https://arxiv.org/abs/1607.08022
  type: paper
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Group Normalization
  url: https://arxiv.org/abs/1803.08494
  type: paper
---
# 归一化统计维度：InstanceNorm 与 GroupNorm

对每个样本的每个通道独立使用空间位置统计量进行标准化的归一化方法。 本文把 Instance Normalization、Group Normalization 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：Instance Normalization
- InstanceNorm
- computer vision
- intermediate
- normalization
- convolutional neural network
- batch normalization
- layer normalization

## 背景与变体

归一化层共享“计算统计量、标准化、仿射变换”的骨架。差异来自统计集合，而不是公式外观。

BatchNorm 跨样本统计，因此受 batch size 与训练模式影响。LayerNorm、InstanceNorm 和 GroupNorm 不需要跨样本共享统计量。

InstanceNorm 为每个样本的每个通道单独统计。GroupNorm 则让同一样本中的一组通道共享统计量。

选择方法前应先写清输入维度语义、统计维度和保留维度。图像、token 序列和时间序列不能机械套用同一解释。

小 batch 视觉任务还要核对 running statistics 是否稳定。分布式训练则要说明统计量是否跨设备同步。

时间序列尤其需要限定可见窗口。若统计集合包含预测时点之后的数据，归一化本身就会制造未来信息泄漏。

最终选择必须由同一数据切分下的收敛、泛化和部署行为共同支持。

## 为什么需要它

风格和生成任务常希望移除单个样本内各通道的对比度统计，又不能依赖 batch 中其它样本。

这些概念放在一起看，是因为它们共享 Instance Normalization 这条主线。

先看主线，再看 Group Normalization 的分工，能减少概念之间的跳跃感。

学习这个概念时，先固定样本空间、变量定义和条件，再解释核心关系：训练与推理通常都使用当前实例统计量，不跨样本也不跨通道。是否使用 affine 和 running stats 要显式确认。

Instance Normalization 的价值在于给模糊问题划出可推理的边界。定义清楚以后，后续公式、例子和误区才有共同口径。

学习时可以从“风格迁移网络对每张图的每个通道独立归一化，从而弱化实例级亮度与对比度差异”开始，再回到定义检查哪些条件被默认使用。

## 核心直觉

- 输入：Instance Normalization 所处理的数据、状态或评价对象。
- 操作：训练与推理通常都使用当前实例统计量，不跨样本也不跨通道。是否使用 affine 和 running stats 要显式确认。
- 观察结果：风格和生成任务常希望移除单个样本内各通道的对比度统计，又不能依赖 batch 中其它样本。

对 NCHW 张量固定 n 和 c，只把该通道的 H×W 像素放进同一个统计集合。

例子：风格迁移网络对每张图的每个通道独立归一化，从而弱化实例级亮度与对比度差异。

Instance Normalization 的子概念分工：
- **Group Normalization**：把单个样本的通道划分为若干组，并在每组通道与空间位置上计算统计量的归一化方法。

## 数学定义

对归一化集合 (S)，共同骨架是：

$$
\mu_S=\frac1{|S|}\sum_{i\in S}x_i,\qquad \sigma_S^2=\frac1{|S|}\sum_{i\in S}(x_i-\mu_S)^2
$$

$$
\hat x_i=\frac{x_i-\mu_S}{\sqrt{\sigma_S^2+\varepsilon}},\qquad y_i=\gamma_i\hat x_i+\beta_i
$$

### 变量解释

- (S) 是共享统计量的元素集合。
- (\mu_S,\sigma_S^2) 是集合均值与方差。
- (\gamma_i,\beta_i) 是可学习仿射参数。

### 含义

对 NCHW 图像张量，InstanceNorm 固定样本 (n) 和通道 (c)，集合 (S) 只包含 H×W 空间位置。GroupNorm 把 C 个通道分成 G 组，固定样本与组，在组内通道及 H×W 上统计。

## 推导

关键不是再背一套标准化公式，而是先标出“统计维度”和“保留维度”。InstanceNorm 的统计维度是 H、W，保留 N、C，因此每个样本的每个通道有一组统计量。GroupNorm 先把输入 reshape 为 N×G×(C/G)×H×W，再沿最后三个维度统计，保留 N、G。

当 G=C 时，每组只有一个通道，统计方式等价于 InstanceNorm。当 G=1 时，所有通道和空间位置共享统计量，统计范围接近对 C、H、W 做 LayerNorm；但两者默认仿射参数形状仍可能不同。

## 假设与限制

InstanceNorm 与 GroupNorm 都不跨样本统计，因此不依赖 batch size，也不需要训练期 running mean 与 variance。代价是它们改变了不同的特征信息：InstanceNorm 强烈移除单通道的实例级外观统计，适合风格迁移但可能伤害依赖绝对对比度的分类任务。

GroupNorm 要求通道数能被组数整除。组数是建模选择，不是越多越好；小通道数、不同 backbone 或时序张量的维度语义都需要重新验证。训练与推理前还要核对框架 API 的输入布局、affine 默认值和数值 epsilon。

## 常见误区

### 概念误解
- InstanceNorm 会移除部分实例外观信息，因此不能因为不依赖 batch 就默认优于 BatchNorm。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Instance Normalization 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Instance Normalization 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它主要用于风格迁移、图像生成和部分低层视觉任务。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Normalization
- Convolutional Neural Network

### 关联
- Group Normalization

### 延伸
- Batch Normalization
- Layer Normalization
- Group Normalization
- Instance Normalization

## 延伸阅读

- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
- **Instance Normalization: The Missing Ingredient for Fast Stylization**：https://arxiv.org/abs/1607.08022。用途：追溯原始方法、关键假设和实验设定。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Group Normalization**：https://arxiv.org/abs/1803.08494。用途：追溯原始方法、关键假设和实验设定。
