---
id: article-n-step-td
slug: n-step-td
title: N-Step TD：概念、直觉与边界
concepts:
- n-step-td
learning_units:
- n-step-td-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- N-Step TD
- n step return
- n-step return
- reinforcement learning
- intermediate
- td error
- monte carlo methods
- eligibility traces
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
  id: article-plan-n-step-td
  covered_concepts: 1
  primary_concept: n-step-td
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# N-Step TD：概念、直觉与边界

使用未来 n 步奖励和第 n 步价值估计构造目标的 TD 方法。

关键词：N-Step TD
- n step return
- n-step return
- reinforcement learning
- intermediate
- td error
- monte carlo methods
- eligibility traces

## 为什么需要它

一步 TD 偏差较大，Monte Carlo 方差较大。n-step TD 提供中间方案。

## 核心直觉

- 输入：N-Step TD 所处理的数据、状态或评价对象。
- 操作：n 越大越接近 Monte Carlo。n 越小越依赖 bootstrapping。
- 观察结果：一步 TD 偏差较大，Monte Carlo 方差较大。n-step TD 提供中间方案。

它像先看几步真实结果，再用估计补上更远未来。

例子：多步 DQN 会用 n-step return 构造训练目标。

## 数学定义

### 表达方式

$$
G_{t:t+n}=\sum_{k=0}^{n-1}\gamma^kR_{t+k+1}+\gamma^nV(S_{t+n})
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- N-Step TD 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 N-Step TD 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 N-Step TD 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- n 不是固定越大越好。任务长度和噪声都会影响选择。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 N-Step TD 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 N-Step TD 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于深度强化学习、价值估计和样本效率优化。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- TD Error
- Monte Carlo Methods

### 关联
- Eligibility Traces

### 延伸
- Eligibility Traces

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
