---
id: article-manhattan-median
slug: manhattan-median
title: Manhattan Median：概念、直觉与边界
concepts:
- manhattan-median
learning_units:
- manhattan-median-overview
domain: algorithms
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Manhattan Median
- best meeting point
- meeting point grid
- algorithms
- intermediate
- mae loss
- grid path search
- vector norm
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
  id: article-plan-manhattan-median
  covered_concepts: 1
  primary_concept: manhattan-median
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
- title: Introduction to Algorithms
  url: https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/
  type: textbook
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Manhattan Median：概念、直觉与边界

在曼哈顿距离下选择使总距离最小的位置的中位数性质。

关键词：Manhattan Median
- best meeting point
- meeting point grid
- algorithms
- intermediate
- mae loss
- grid path search
- vector norm

## 为什么需要它

网格中找最佳汇合点时，需要最小化所有人步行距离。

## 核心直觉

- 输入：Manhattan Median 所处理的数据、状态或评价对象。
- 操作：二维曼哈顿距离可拆成行和列两个一维中位数问题。
- 观察结果：网格中找最佳汇合点时，需要最小化所有人步行距离。

它像在一条街上约地点，中位数位置让总路程最短。

例子：在网格坐标中找总曼哈顿距离最小的 meeting point。

## 数学定义

### 表达方式

$$
m^{\star}\in\underset{m\in\mathbb R}{\operatorname{arg\,min}}\ \sum_{i=1}^{n}|x_i-m|\iff m^{\star}\in\operatorname{Median}(x_1,\ldots,x_n)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Manhattan Median 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Manhattan Median 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Manhattan Median 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 平均数适合平方误差，中位数适合绝对距离。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Manhattan Median 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Manhattan Median 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于网格算法、选址问题和 L1 距离优化。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Mean Absolute Error
- Grid Path Search

### 关联
- Vector Norm

### 延伸
- Vector Norm

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
