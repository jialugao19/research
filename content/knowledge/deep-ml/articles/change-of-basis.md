---
id: article-change-of-basis
slug: change-of-basis
title: Change of Basis：概念、直觉与边界
concepts:
- change-of-basis
learning_units:
- change-of-basis-overview
domain: linear_algebra
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Change of Basis
- basis transformation
- transformation basis
- linear algebra
- intermediate
- matrix multiplication
- orthonormal basis
- vector projection
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
  id: article-plan-change-of-basis
  covered_concepts: 1
  primary_concept: change-of-basis
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: NumPy Documentation
  url: https://numpy.org/doc/stable/
  type: official_docs
---
# Change of Basis：概念、直觉与边界

把同一个向量从一组基的坐标表示转换到另一组基的过程。

关键词：Change of Basis
- basis transformation
- transformation basis
- linear algebra
- intermediate
- matrix multiplication
- orthonormal basis
- vector projection

## 为什么需要它

同一对象在不同坐标系中表示不同。换基解释了表示如何变化。

## 核心直觉

- 输入：Change of Basis 所处理的数据、状态或评价对象。
- 操作：变换矩阵连接旧基和新基。向量本身不变，坐标数值改变。
- 观察结果：同一对象在不同坐标系中表示不同。换基解释了表示如何变化。

它像同一个位置用不同地图坐标描述。

例子：PCA 可以看成把数据表示到主成分基上。

## 数学定义

### 表达方式

$$
x_new = P^{-1} x_old
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Change of Basis 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Change of Basis 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Change of Basis 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 换基不是移动点，而是换描述坐标。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Change of Basis 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Change of Basis 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 PCA、线性变换、图形学和特征空间分析。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Matrix Multiplication
- Orthonormal Basis

### 关联
- Vector Projection
- Rotation Matrix

### 延伸
- Vector Projection
- Rotation Matrix

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **NumPy Documentation**：https://numpy.org/doc/stable/。用途：作为交叉核对材料，确认术语、公式和使用场景。
