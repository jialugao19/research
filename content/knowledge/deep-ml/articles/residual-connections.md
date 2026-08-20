---
id: article-residual-connections
slug: residual-connections
title: Residual Connections：概念、直觉与边界
concepts:
- residual-connections
learning_units:
- residual-connections-overview
domain: deep_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Residual Connections
- skip connection
- deep learning
- intermediate
- neural network
- backpropagation
- transformer architecture
- weight initialization
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
  id: article-plan-residual-connections
  covered_concepts: 1
  primary_concept: residual-connections
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# Residual Connections：概念、直觉与边界

把层输入直接加到层输出上的网络连接方式。

关键词：Residual Connections
- skip connection
- deep learning
- intermediate
- neural network
- backpropagation
- transformer architecture
- weight initialization

## 为什么需要它

深层网络容易训练困难。残差连接让梯度和信息更容易跨层传递。

## 核心直觉

- 输入：Residual Connections 所处理的数据、状态或评价对象。
- 操作：典型形式是 y = F(x) + x。维度不同时需要投影匹配。
- 观察结果：深层网络容易训练困难。残差连接让梯度和信息更容易跨层传递。

它像给模型一条捷径。层可以学习修正量，而不是从零重建全部表示。

例子：ResNet 用残差块训练很深的卷积网络。

## 数学定义

### 表达方式

$$
y=x+F(x;\theta)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Residual Connections 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Residual Connections 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Residual Connections 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 残差连接不是简单堆更多层的许可证。归一化和初始化仍然重要。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Residual Connections 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Residual Connections 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 ResNet、Transformer 和扩散模型。结构设计要保证张量形状一致。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Neural Network
- Backpropagation

### 关联
- Transformer Architecture
- Weight Initialization

### 延伸
- Transformer Architecture
- Weight Initialization

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
