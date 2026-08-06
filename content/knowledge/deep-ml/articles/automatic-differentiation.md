---
id: article-automatic-differentiation
slug: automatic-differentiation
title: Automatic Differentiation：概念、直觉与边界
concepts:
- automatic-differentiation
learning_units:
- automatic-differentiation-overview
domain: deep_learning
level: intermediate
content_type: theory
depth_level: level_3_deep_dive
target_chars:
  minimum: 3000
  maximum: 5000
keywords:
- Automatic Differentiation
- autograd
- deep learning
- intermediate
- gradient descent
- backpropagation
- pytorch tensor
- tinygrad computation graph
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
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-automatic-differentiation
  covered_concepts: 1
  primary_concept: automatic-differentiation
confidence:
  concept: 0.94
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
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
---
# Automatic Differentiation：概念、直觉与边界

在程序执行时记录可导运算，并按局部求导规则组合梯度的技术。

关键词：Automatic Differentiation
- autograd
- deep learning
- intermediate
- gradient descent
- backpropagation
- pytorch tensor
- tinygrad computation graph

## 背景与变体

神经网络训练写出来的是普通前向程序：矩阵乘法、加法、激活和损失。自动微分要解决的不是把整个程序化成一个巨大符号公式，而是如何利用已经执行的运算高效得到梯度。

动态图框架在前向时记录结果由哪个操作产生、依赖哪些输入以及反向所需的中间量。反向模式再从标量损失出发，逐节点应用局部求导规则。它特别适合“一个损失、很多参数”的深度学习场景。

计算图是依赖结构，backpropagation 是沿图反向传播梯度的算法，autograd 是框架提供的自动微分系统。三者相关，但不是同一个概念。

## 为什么需要它

深度模型包含大量共享参数、分支与张量操作。若对每个参数分别展开全局导数或用有限差分扰动，推导和计算都会迅速失控。

自动微分把复杂程序拆成已有局部求导规则的基本操作，并沿实际依赖关系复用中间结果。对标量损失和大量参数，反向模式只需一次反向遍历，就能得到全部叶子参数的梯度。

它解决的是“给定这次程序执行，梯度怎样高效得到”，不负责决定损失是否合理、数据是否泄漏，也不负责选择参数更新策略。

## 核心直觉

可以把 autograd 看作两阶段账本：

- 前向传播计算数值，同时记录每个非叶子张量的产生方式。
- `backward()` 从输出发起回溯，把上游梯度与每个操作的局部规则组合起来。
- 需要梯度的叶子张量负责接收并累加最终结果；调用反向前，`.grad` 通常仍是 `None`。

这也解释了几个工程规则：同一计算图默认在反向后释放；多次更新前要显式清零梯度；`detach()`、`no_grad()` 和不当原地操作会改变依赖链。

### 叶子、非叶子与梯度落点

用户直接创建并声明需要梯度的参数通常是叶子张量。运算结果是非叶子张量，它们带有反向函数，用于继续追踪依赖。框架默认把最终梯度累加到叶子的 `.grad`；若调试时需要查看中间张量梯度，必须使用框架提供的保留机制，不能假设它会自动保存。

分支结构还会改变梯度流。若变量 `x` 同时经过两条路径影响损失，`x` 的梯度是两条路径贡献之和。共享参数正是依靠这种累加得到所有使用位置的总责任，而不是只保留最后一次调用。

### 非标量输出与 VJP

标量输出调用 `backward()` 时，隐含的上游梯度是 1。向量输出没有唯一的“对输入梯度”，需要先指定一个同形上游向量。框架计算的是该向量与 Jacobian 的乘积，而不是默认构造完整 Jacobian。

这一点对逐元素 loss、每样本梯度和多目标优化很重要。先做 `sum()`、`mean()`，或传入不同上游向量，会得到不同的梯度口径。验证实现时必须同时固定 reduction 和 batch 语义。

### 图生命周期与内存

反向传播需要读取部分前向中间量，因此激活会占用显存。默认反向完成后，已保存状态可被释放；若盲目保留计算图，会让多步训练不断积累内存。高阶导数需要显式创建可继续求导的反向图，普通训练不应默认启用。

`no_grad()` 适合验证和推理，`detach()` 用于显式切断一条依赖。Activation checkpointing 则不切断数学依赖，而是在反向时重算部分前向，用额外计算换更少的已保存激活。三者不能混为同一种“省显存”。

## 数学定义

### 表达方式

`如果 z = f(y), y = g(x)，则 dz/dx = dz/dy * dy/dx`

此处保留 Automatic Differentiation 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Automatic Differentiation 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Automatic Differentiation 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

### 使用读法

读 Automatic Differentiation 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

设中间变量 (y=g(x))、标量输出 (L=f(y))。反向传播先收到上游梯度 (\partial L/\partial y)，再与本地 Jacobian 组合：

$$
\frac{\partial L}{\partial x}
=\frac{\partial L}{\partial y}\frac{\partial y}{\partial x}
$$

框架通常不显式构造完整 Jacobian，而是直接计算 vector--Jacobian product。若一个张量沿多条分支影响损失，各路径贡献会在该节点相加。这样既复用上游梯度，也避免为每个参数重新执行完整前向。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。
- 应用到真实数据前，要检查这个前提是否和 `deep_learning` 领域的数据来源一致。
- 如果输入形态明显不同于“PyTorch 会记录 Tensor 操作。调用 backward 后，参数会得到 grad”，需要重新确认输出解释。

## 常见误区

- `requires_grad=True` 只声明追踪需求；反向开始前，叶子 `.grad` 通常仍是 `None`。
- `.grad` 默认累加。训练循环若未在正确时机清零，会把不同 batch 的梯度意外相加。
- 非标量输出调用 backward 时需要给出上游向量，实际计算的是 VJP，不是凭空得到完整 Jacobian。
- `detach()`、`no_grad()`、原地修改和跨设备复制可能截断或改变计算图。
- 梯度能算出来不代表训练目标正确；仍需数值梯度检查、最小样例和数据口径审计。

## 相关概念

### 前置
- Gradient Descent
- Backpropagation

### 关联
- PyTorch Tensor
- tinygrad Computation Graph

### 延伸
- PyTorch Tensor
- tinygrad Computation Graph

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
