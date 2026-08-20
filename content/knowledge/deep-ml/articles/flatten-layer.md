---
id: article-flatten-layer
slug: flatten-layer
title: Flatten Layer：概念、直觉与边界
concepts:
- flatten-layer
learning_units:
- flatten-layer-overview
domain: deep_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Flatten Layer
- flatten
- FlattenConsecutive layer
- deep learning
- beginner
- tensor shape
- reshape view
- sequential module
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
  id: article-plan-flatten-layer
  covered_concepts: 1
  primary_concept: flatten-layer
confidence:
  concept: 0.94
  prerequisite: 0.94
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
# Flatten Layer：概念、直觉与边界

把多维张量除 batch 维外展平成一维特征的网络层。

关键词：Flatten Layer
- flatten
- FlattenConsecutive layer
- deep learning
- beginner
- tensor shape
- reshape view
- sequential module

## 为什么需要它

卷积输出常是多维特征图。接全连接层前需要展平。

## 核心直觉

- 输入：Flatten Layer 所处理的数据、状态或评价对象。
- 操作：Flatten 只改变形状，不改变元素值。语义维度要提前确认。
- 观察结果：卷积输出常是多维特征图。接全连接层前需要展平。

它像把一叠网格摊平成一长条。

例子：CNN 分类头常先 flatten，再接线性层。

## 数学定义

### 表达方式

$$
X\in\mathbb R^{N\times C\times H\times W}\longmapsto \operatorname{reshape}(X)\in\mathbb R^{N\times(C H W)}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Flatten Layer 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Flatten Layer 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Flatten Layer 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 展平会丢失显式空间结构。位置关系交给后续层不一定合适。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Flatten Layer 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Flatten Layer 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 CNN、MLP 输入整理和特征拼接。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Tensor Shape
- Reshape and View

### 关联
- PyTorch Sequential

### 延伸
- PyTorch Sequential

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
