---
id: article-feature-receptive-field
slug: feature-receptive-field
title: Feature Receptive Field：概念、直觉与边界
concepts:
- feature-receptive-field
learning_units:
- feature-receptive-field-overview
domain: machine_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Feature Receptive Field
- receptive field visualization
- machine learning
- intermediate
- feature space
- coarse coding
- convolution
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
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-feature-receptive-field
  covered_concepts: 1
  primary_concept: feature-receptive-field
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
---
# Feature Receptive Field：概念、直觉与边界

一个特征对输入空间中哪些区域或模式产生响应的范围。

关键词：Feature Receptive Field
- receptive field visualization
- machine learning
- intermediate
- feature space
- coarse coding
- convolution
- theory

## 为什么需要它

理解特征泛化，需要知道它覆盖了哪些输入变化。

## 核心直觉

- 输入：Feature Receptive Field 所处理的数据、状态或评价对象。
- 操作：感受野大小影响局部性、平滑性和泛化范围。
- 观察结果：理解特征泛化，需要知道它覆盖了哪些输入变化。

它像一个传感器能看到的区域。

例子：粗编码特征会对状态空间中一片区域同时响应。

## 数学定义

### 表达方式

$$
\mathcal R_{\ell}=\mathcal R_{\ell-1}+(k_\ell-1)\prod_{j=1}^{\ell-1}s_j
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Feature Receptive Field 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Feature Receptive Field 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Feature Receptive Field 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 感受野大不一定更好。它可能混合太多不同模式。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Feature Receptive Field 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Feature Receptive Field 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 CNN、RL 特征、可视化和表示诊断。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Feature Space

### 关联
- Coarse Coding
- Convolution

### 延伸
- Coarse Coding
- Convolution

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
