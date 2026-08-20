---
id: article-phi-coefficient
slug: phi-coefficient
title: Phi Coefficient：概念、直觉与边界
concepts:
- phi-coefficient
learning_units:
- phi-coefficient-overview
domain: statistics
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Phi Coefficient
- matthews correlation for binary table
- statistics
- intermediate
- correlation coefficient
- binary classification
- confusion matrix
- chi square test
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
  id: article-plan-phi-coefficient
  covered_concepts: 1
  primary_concept: phi-coefficient
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
# Phi Coefficient：概念、直觉与边界

衡量两个二元变量相关程度的统计系数。

关键词：Phi Coefficient
- matthews correlation for binary table
- statistics
- intermediate
- correlation coefficient
- binary classification
- confusion matrix
- chi square test

## 为什么需要它

两个变量都只有真或假时，普通相关分析需要适配二元表。

## 核心直觉

- 输入：Phi Coefficient 所处理的数据、状态或评价对象。
- 操作：Phi 系数可由四格表计数计算，取值范围通常在 -1 到 1。
- 观察结果：两个变量都只有真或假时，普通相关分析需要适配二元表。

它像二乘二列联表上的相关系数。

例子：分析两个二元标签是否倾向同时出现。

## 数学定义

### 表达方式

$$
\phi=\frac{ad-bc}{\sqrt{(a+b)(c+d)(a+c)(b+d)}}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Phi Coefficient 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Phi Coefficient 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Phi Coefficient 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- Phi 系数仍然不是因果证据。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Phi Coefficient 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Phi Coefficient 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于二元特征筛选、标签相关性和问卷数据分析。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Correlation Coefficient
- Binary Classification

### 关联
- Confusion Matrix
- Chi-Square Test

### 延伸
- Confusion Matrix
- Chi-Square Test

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **NumPy Documentation**：https://numpy.org/doc/stable/。用途：作为交叉核对材料，确认术语、公式和使用场景。
