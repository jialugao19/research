---
id: article-pointwise-mutual-information
slug: pointwise-mutual-information
title: Pointwise Mutual Information：概念、直觉与边界
concepts:
- pointwise-mutual-information
learning_units:
- pointwise-mutual-information-overview
domain: information_theory
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Pointwise Mutual Information
- PMI
- information theory
- intermediate
- probability
- information gain
- tf idf
- token frequency
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
  id: article-plan-pointwise-mutual-information
  covered_concepts: 1
  primary_concept: pointwise-mutual-information
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Pointwise Mutual Information：概念、直觉与边界

衡量两个具体事件共同出现比独立假设下多多少的信息量。

关键词：Pointwise Mutual Information
- PMI
- information theory
- intermediate
- probability
- information gain
- tf idf
- token frequency

## 为什么需要它

文本和推荐中常需要衡量两个符号的关联强度。PMI 提供统计指标。

## 核心直觉

- 输入：Pointwise Mutual Information 所处理的数据、状态或评价对象。
- 操作：PMI 为正表示共现高于独立期望。为负表示低于独立期望。
- 观察结果：文本和推荐中常需要衡量两个符号的关联强度。PMI 提供统计指标。

它像问两个词一起出现是不是超出偶然。

例子：词共现分析可用 PMI 找相关词对。

## 数学定义

### 表达方式

$$
\operatorname{PMI}(x,y)=\log\frac{p(x,y)}{p(x)p(y)}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Pointwise Mutual Information 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Pointwise Mutual Information 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Pointwise Mutual Information 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 低频事件会让 PMI 很不稳定。要设置频次阈值。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Pointwise Mutual Information 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Pointwise Mutual Information 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 NLP、推荐、词关联和特征分析。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability
- Information Gain

### 关联
- TF-IDF
- Token Frequency

### 延伸
- TF-IDF
- Token Frequency

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
