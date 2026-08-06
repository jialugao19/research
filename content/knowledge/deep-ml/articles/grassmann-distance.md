---
id: article-grassmann-distance
slug: grassmann-distance
title: Grassmann Distance：概念、直觉与边界
concepts:
- grassmann-distance
learning_units:
- grassmann-distance-overview
domain: linear_algebra
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Grassmann Distance
- linear algebra
- advanced
- orthonormal basis
- singular value decomposition
- vector projection
- theory
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
  id: article-plan-grassmann-distance
  covered_concepts: 1
  primary_concept: grassmann-distance
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: NumPy Documentation
  url: https://numpy.org/doc/stable/
  type: official_docs
---
# Grassmann Distance：概念、直觉与边界

衡量两个子空间在 Grassmann 流形上相距多远的距离概念。

关键词：Grassmann Distance
- linear algebra
- advanced
- orthonormal basis
- singular value decomposition
- vector projection
- theory

## 为什么需要它

比较子空间时，单个向量距离不够。Grassmann 距离关注子空间夹角。

## 核心直觉

- 输入：Grassmann Distance 所处理的数据、状态或评价对象。
- 操作：距离常基于主角。主角描述两个子空间之间的相对方向。
- 观察结果：比较子空间时，单个向量距离不够。Grassmann 距离关注子空间夹角。

它像比较两个平面朝向有多不同。

例子：比较两个低维表示子空间时，可使用 Grassmann 距离。

## 数学定义

### 表达方式

`distance depends on principal angles`

此处保留 Grassmann Distance 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Grassmann Distance 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Grassmann Distance 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Grassmann Distance 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 它不是样本点之间的普通距离。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Grassmann Distance 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Grassmann Distance 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于子空间学习、降维比较、信号处理和表示分析。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Orthonormal Basis
- Singular Value Decomposition

### 关联
- Vector Projection

### 延伸
- Vector Projection

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **NumPy Documentation**：https://numpy.org/doc/stable/。用途：作为交叉核对材料，确认术语、公式和使用场景。
