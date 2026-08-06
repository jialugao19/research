---
id: article-state-value-function
slug: state-value-function
title: State Value Function：概念、直觉与边界
concepts:
- state-value-function
learning_units:
- state-value-function-overview
domain: reinforcement_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- State Value Function
- state value
- value function
- reinforcement learning
- beginner
- markov decision process
- discounted return
- action value function
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
  id: article-plan-state-value-function
  covered_concepts: 1
  primary_concept: state-value-function
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# State Value Function：概念、直觉与边界

表示从某个状态出发，按策略行动可获得期望回报的函数。

关键词：State Value Function
- state value
- value function
- reinforcement learning
- beginner
- markov decision process
- discounted return
- action value function

## 为什么需要它

智能体需要判断状态好坏。状态价值函数给出长期收益估计。

## 核心直觉

- 输入：State Value Function 所处理的数据、状态或评价对象。
- 操作：价值来自未来奖励的折扣和。它依赖当前策略。
- 观察结果：智能体需要判断状态好坏。状态价值函数给出长期收益估计。

它像给棋盘局面打分，而不是只看当前奖励。

例子：在迷宫中，离出口更近的状态通常价值更高。

## 数学定义

### 表达方式

`V_pi(s) 表示从状态 s 出发的期望折扣回报`

此处保留 State Value Function 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- State Value Function 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 State Value Function 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 State Value Function 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 高价值状态不一定立即奖励高。长期收益才是重点。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 State Value Function 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 State Value Function 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于策略评估、动态规划和 actor-critic。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Markov Decision Process
- Discounted Return

### 关联
- Action Value Function
- Policy Evaluation

### 延伸
- Action Value Function
- Policy Evaluation

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
