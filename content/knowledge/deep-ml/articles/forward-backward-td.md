---
id: article-forward-backward-td
slug: forward-backward-td
title: Forward and Backward TD：概念、直觉与边界
concepts:
- forward-backward-td
learning_units:
- forward-backward-td-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Forward and Backward TD
- forward TD
- backward TD
- reinforcement learning
- advanced
- td lambda
- eligibility traces
- action conditional trace
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
  id: article-plan-forward-backward-td
  covered_concepts: 1
  primary_concept: forward-backward-td
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Forward and Backward TD：概念、直觉与边界

从前向回报定义和后向资格迹更新两种视角理解 TD 学习的方法。

关键词：Forward and Backward TD
- forward TD
- backward TD
- reinforcement learning
- advanced
- td lambda
- eligibility traces
- action conditional trace

## 为什么需要它

TD(lambda) 公式有前向目标和在线更新两种等价表达，学习者容易割裂理解。

## 核心直觉

- 输入：Forward and Backward TD 所处理的数据、状态或评价对象。
- 操作：前向视角定义 lambda-return，后向视角用 eligibility trace 在线实现。
- 观察结果：TD(lambda) 公式有前向目标和在线更新两种等价表达，学习者容易割裂理解。

前向像事后算完整账，后向像边走边记责任。

例子：SARSA(lambda) 可用后向迹近似前向多步回报效果。

## 数学定义

### 表达方式

$$
forward return can be implemented by backward traces
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Forward and Backward TD 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Forward and Backward TD 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Forward and Backward TD 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 前向和后向不是两个无关算法，而是同一思想的两种表达。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Forward and Backward TD 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Forward and Backward TD 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 TD(lambda)、SARSA(lambda) 和信用分配教学。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- TD Lambda
- Eligibility Traces

### 关联
- Action-Conditional Trace
- Trace Clearing

### 延伸
- Action-Conditional Trace
- Trace Clearing

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
