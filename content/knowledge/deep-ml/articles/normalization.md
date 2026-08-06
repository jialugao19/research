---
id: article-normalization
slug: normalization
title: Normalization：概念、直觉与边界
concepts:
- normalization
learning_units:
- normalization-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Normalization
- feature normalization
- data normalization
- machine learning
- beginner
- probability
- batch normalization
- layer normalization
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
  id: article-plan-normalization
  covered_concepts: 1
  primary_concept: normalization
confidence:
  concept: 0.95
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Normalization：概念、直觉与边界

把数据或中间表示调整到更稳定尺度的处理方法。

关键词：Normalization
- feature normalization
- data normalization
- machine learning
- beginner
- probability
- batch normalization
- layer normalization

## 为什么需要它

不同特征尺度差异太大时，优化会变难。模型也可能过度依赖数值范围大的特征。

## 核心直觉

- 输入：Normalization 所处理的数据、状态或评价对象。
- 操作：常见做法包括减均值、除标准差、缩放到固定区间。深度模型中还有内部激活的归一化。
- 观察结果：不同特征尺度差异太大时，优化会变难。模型也可能过度依赖数值范围大的特征。

它像把不同单位的量放到同一把尺子上。这样比较和更新都更稳定。

例子：房价数据里，面积是几百，房龄是几十。标准化后，两个特征更容易共同参与训练。

## 数学定义

### 表达方式

`z = (x - mean) / std 是常见标准化形式`

此处保留 Normalization 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Normalization 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Normalization 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Normalization 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 归一化不会自动增加信息。它改变尺度，不改变数据本身的事实来源。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Normalization 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Normalization 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于数据预处理、BatchNorm、LayerNorm 和相似度计算。异常值很多时要谨慎选择方法。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability

### 关联
- Batch Normalization
- Layer Normalization
- Covariance Matrix

### 延伸
- Batch Normalization
- Layer Normalization
- Covariance Matrix

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
