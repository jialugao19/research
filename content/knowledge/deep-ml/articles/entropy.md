---
id: article-entropy
slug: entropy
title: Entropy：概念、直觉与边界
concepts:
- entropy
learning_units:
- entropy-overview
domain: information_theory
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Entropy
- measure disorder
- disorder
- information theory
- beginner
- probability
- cross entropy
- decision tree
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
  id: article-plan-entropy
  covered_concepts: 1
  primary_concept: entropy
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Entropy：概念、直觉与边界

衡量随机变量不确定性的数量。

关键词：Entropy
- measure disorder
- disorder
- information theory
- beginner
- probability
- cross entropy
- decision tree

## 为什么需要它

概率分布有的很确定，有的很分散。熵给这种不确定性一个数值尺度。

## 核心直觉

- 输入：Entropy 所处理的数据、状态或评价对象。
- 操作：均匀分布通常熵更高。确定事件的熵为零。
- 观察结果：概率分布有的很确定，有的很分散。熵给这种不确定性一个数值尺度。

熵像猜答案的难度。结果越难猜，熵越高。

例子：公平硬币的不确定性高于总是正面的硬币。

## 数学定义

### 表达方式

$$
H(X)=-\sum_{x\in\mathcal X}p(x)\log p(x)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Entropy 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Entropy 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Entropy 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 熵不是混乱的口号。它有明确的概率定义。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Entropy 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Entropy 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于决策树、交叉熵、语言模型和压缩。底数不同会改变单位。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability

### 关联
- Cross Entropy
- Decision Tree

### 延伸
- Cross Entropy
- Decision Tree

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
