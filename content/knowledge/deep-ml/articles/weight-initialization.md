---
id: article-weight-initialization
slug: weight-initialization
title: Weight Initialization：概念、直觉与边界
concepts:
- weight-initialization
learning_units:
- weight-initialization-overview
domain: deep_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Weight Initialization
- initialization
- deep learning
- intermediate
- neural network
- activation functions
- gradient clipping
- residual connections
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-weight-initialization
  covered_concepts: 1
  primary_concept: weight-initialization
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
  - routine_auto_check
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Weight Initialization：概念、直觉与边界

训练开始前设置模型参数初始值的方法。

关键词：Weight Initialization
- initialization
- deep learning
- intermediate
- neural network
- activation functions
- gradient clipping
- residual connections

## 为什么需要它

初始值会影响信号和梯度传播。差的初始化会让训练很慢或不稳定。

## 核心直觉

- 输入：Weight Initialization 所处理的数据、状态或评价对象。
- 操作：常见方法包括 Xavier 和 Kaiming 初始化。它们根据输入输出维度控制方差。
- 观察结果：初始值会影响信号和梯度传播。差的初始化会让训练很慢或不稳定。

它像给训练找起点。起点太偏，后面每一步都更困难。

例子：ReLU 网络常使用 Kaiming 初始化，以适配激活的截断特性。

## 数学定义

### 表达方式

`初始化常让激活方差在层间尽量稳定`

此处保留 Weight Initialization 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Weight Initialization 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Weight Initialization 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Weight Initialization 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 随机初始化不是随便取随机数。尺度非常关键。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Weight Initialization 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Weight Initialization 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于深层网络、残差网络和自定义层。预训练模型则从已有权重开始。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Neural Network
- Activation Functions

### 关联
- Gradient Clipping
- Residual Connections

### 延伸
- Gradient Clipping
- Residual Connections

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
