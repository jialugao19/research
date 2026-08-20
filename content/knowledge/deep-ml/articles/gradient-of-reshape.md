---
id: article-gradient-of-reshape
slug: gradient-of-reshape
title: Gradient of Reshape：概念、直觉与边界
concepts:
- gradient-of-reshape
learning_units:
- gradient-of-reshape-overview
domain: deep_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Gradient of Reshape
- reshape backward
- deep learning
- intermediate
- reshape view
- backpropagation
- gradient of broadcast
- contiguous memory
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
  id: article-plan-gradient-of-reshape
  covered_concepts: 1
  primary_concept: gradient-of-reshape
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
# Gradient of Reshape：概念、直觉与边界

reshape 操作在反向传播中把梯度恢复到输入形状的规则。

关键词：Gradient of Reshape
- reshape backward
- deep learning
- intermediate
- reshape view
- backpropagation
- gradient of broadcast
- contiguous memory

## 为什么需要它

reshape 改变张量形状，但不改变元素。反向时需要把梯度形状对回去。

## 核心直觉

- 输入：Gradient of Reshape 所处理的数据、状态或评价对象。
- 操作：reshape 的梯度通常只是形状变换，不涉及数值混合。
- 观察结果：reshape 改变张量形状，但不改变元素。反向时需要把梯度形状对回去。

它像把积木换了摆法。反向时再按原摆法放回。

例子：flatten 后接线性层，反向时梯度要恢复成原特征图形状。

## 数学定义

### 表达方式

$$
\frac{\partial L}{\partial x}=\operatorname{reshape}\!\left(\frac{\partial L}{\partial y},\operatorname{shape}(x)\right),\qquad y=\operatorname{reshape}(x)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Gradient of Reshape 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Gradient of Reshape 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Gradient of Reshape 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- reshape 反向简单，不代表所有形状操作都简单。索引和广播会更复杂。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Gradient of Reshape 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Gradient of Reshape 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于自动微分、模型调试和自定义算子。元素顺序必须一致。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Reshape and View
- Backpropagation

### 关联
- Gradient of Broadcasting
- Contiguous Memory

### 延伸
- Gradient of Broadcasting
- Contiguous Memory

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
