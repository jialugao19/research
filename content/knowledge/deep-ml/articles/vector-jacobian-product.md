---
id: article-vector-jacobian-product
slug: vector-jacobian-product
title: Vector-Jacobian Product：概念、直觉与边界
concepts:
- vector-jacobian-product
learning_units:
- vector-jacobian-product-overview
domain: deep_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Vector-Jacobian Product
- VJP
- deep learning
- advanced
- jacobian matrix
- automatic differentiation
- custom autograd function
- backpropagation
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-vector-jacobian-product
  covered_concepts: 1
  primary_concept: vector-jacobian-product
confidence:
  concept: 0.94
  prerequisite: 0.9
  prerequisite_path_eligible: true
generated_version:
  model: curated-catalog-v3
  prompt_version: chapter-profile-v3
review:
  state: automated_editorial
  last_review: null
  reviewer: null
  triggers:
  - advanced_or_expert_topic
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Vector-Jacobian Product：概念、直觉与边界

向量与 Jacobian 相乘得到反向传播所需梯度的计算形式。

关键词：Vector-Jacobian Product
- VJP
- deep learning
- advanced
- jacobian matrix
- automatic differentiation
- custom autograd function
- backpropagation

## 为什么需要它

完整 Jacobian 太大。VJP 只计算反向传播真正需要的乘积。

## 核心直觉

- 输入：Vector-Jacobian Product 所处理的数据、状态或评价对象。
- 操作：反向模式自动微分的核心就是高效计算 VJP。
- 观察结果：完整 Jacobian 太大。VJP 只计算反向传播真正需要的乘积。

它像不打印整张影响表，只算最终需要的汇总影响。

例子：PyTorch backward 接收上游梯度，本质上会计算相关 VJP。

## 数学定义

### 表达方式

$$
v^{\top}J_f(x)=\nabla_x\!\left(v^{\top}f(x)\right)^{\top}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Vector-Jacobian Product 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Vector-Jacobian Product 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Vector-Jacobian Product 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- VJP 不是近似。它是精确链式法则的一种高效计算方式。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Vector-Jacobian Product 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Vector-Jacobian Product 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于自动微分、自定义反向和高阶梯度。理解它有助于写自定义算子。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Jacobian Matrix
- Automatic Differentiation

### 关联
- Custom Autograd Function
- Backpropagation

### 延伸
- Custom Autograd Function
- Backpropagation

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
