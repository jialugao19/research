---
id: article-activation-functions
slug: activation-functions
title: 激活函数：从 ReLU 到 GELU
concepts:
- activation-functions
- relu-activation
- leaky-relu-activation
- sigmoid-activation
- tanh-activation
- gelu-activation
learning_units:
- activation-functions-overview
- relu-activation-overview
- leaky-relu-activation-overview
- sigmoid-activation-overview
- tanh-activation-overview
- gelu-activation-overview
domain: deep_learning
level: intermediate
content_type: algorithm
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Activation Functions
- activation
- deep learning
- beginner
- linear algebra
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 算法流程
  - 实现要点
  - 复杂度
  - 假设与限制
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: true
  complexity_required: true
status: published
article_plan:
  id: article-plan-activation-functions
  covered_concepts: 6
  primary_concept: activation-functions
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
  - multi_concept_article
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# 激活函数：从 ReLU 到 GELU

插在线性层之间、把逐层线性组合变成非线性表示的函数族。 本文把 以 Activation Functions 为主线的 6 个概念 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：Activation Functions
- activation
- deep learning
- beginner
- linear algebra

## 为什么需要它

如果没有激活函数，多层线性网络仍然等价于一层线性变换。模型表达会很受限。

这些概念放在一起看，是因为它们共享 Activation Functions 这条主线。

先看主线，再看 以 ReLU Activation 为主线的 5 个概念 的分工，能减少概念之间的跳跃感。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 Activation Functions 来说，Sigmoid、tanh、ReLU、GELU 通常逐元素作用，其反向传播可利用对角 Jacobian。softmax 会耦合同一向量内的所有分量，不能机械套用逐元素导数。

在 Activation Functions 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

## 核心直觉

缺少非线性时，多层线性变换仍能合并成一层。激活函数让表示空间弯折和分段。

常见隐藏层激活并不只是在比较公式：

- sigmoid 与 tanh 在大幅值区间会饱和。
- ReLU 正半轴梯度直接，但负半轴长期为零时可能出现 dead ReLU。
- Leaky ReLU 保留负半轴小斜率；GELU 常见于 Transformer。

这些隐藏层激活通常逐元素作用，Jacobian 对角。softmax 保持形状却耦合整组分量，不能套用同一逐元素导数。

## 数学定义

### 表达方式

`ReLU(x) = max(0, x)。它简单，也能缓解部分梯度消失问题`

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策

### 含义

这里保留的是 Activation Functions 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

把 Activation Functions 写成输入、状态更新和输出，推导时只保留影响目标的量。

## 算法流程

Input: Activation Functions
- Activation Functions 所处理的数据、状态或评价对象。
- 必要的超参数或停止条件。

Output: Activation Functions
- 如果没有激活函数，多层线性网络仍然等价于一层线性变换。模型表达会很受限。

Steps: Activation Functions
1. 固定输入、目标与停止条件。
2. 执行核心操作：Sigmoid、tanh、ReLU、GELU 通常逐元素作用，其反向传播可利用对角 Jacobian。softmax 会耦合同一向量内的所有分量，不能机械套用逐元素导数。
3. 检查输出，并在达到预算或稳定条件时停止。

## 实现要点

- 明确输入、输出和停止条件。
- 记录随机种子、超参数和数据版本。
- 用小规模样例验证每一步计算是否符合预期。

```python
import math

xs = [-2.0, -0.5, 0.0, 1.5]
relu = [max(0.0, x) for x in xs]
sigmoid = [1 / (1 + math.exp(-x)) for x in xs]
print(relu, sigmoid)
```

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Activation Functions 时要单独估计训练成本和推理成本。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。

## 常见误区

### 概念误解
- 不能只按输出形状判断激活函数是否逐元素作用。softmax 保持形状不变，但每个输出仍依赖整组 logits。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Activation Functions 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Activation Functions 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 激活函数用于几乎所有神经网络。输出层通常按任务选择，例如分类常用 softmax。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Linear Algebra
- Activation Functions
- ReLU Activation
- Probability

### 关联
- ReLU Activation
- Leaky ReLU Activation
- Sigmoid Activation
- Tanh Activation

### 延伸
- Softmax Function
- Neural Network
- Leaky ReLU Activation
- GELU Activation

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
