---
id: article-r-learning
slug: r-learning
title: R-Learning：概念、直觉与边界
concepts:
- r-learning
learning_units:
- r-learning-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- R-Learning
- r learning
- reinforcement learning
- advanced
- temporal difference learning
- action value function
- q learning
- policy iteration
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
  id: article-plan-r-learning
  covered_concepts: 1
  primary_concept: r-learning
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
# R-Learning：概念、直觉与边界

面向平均奖励目标的时序差分控制方法。

关键词：R-Learning
- r learning
- reinforcement learning
- advanced
- temporal difference learning
- action value function
- q learning
- policy iteration

## 为什么需要它

有些持续任务没有自然终止点，折扣回报不一定合适。

## 核心直觉

- 输入：R-Learning 所处理的数据、状态或评价对象。
- 操作：R-learning 同时估计动作价值和平均奖励率。
- 观察结果：有些持续任务没有自然终止点，折扣回报不一定合适。

它像优化长期每步平均收益，而不是有限回合总收益。

例子：排队控制任务可用平均奖励目标建模长期吞吐。

## 数学定义

### 表达方式

$$
rho \leftarrow rho + beta \cdot  TD_error_for_greedy_action
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- R-Learning 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 R-Learning 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 R-Learning 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 平均奖励设置比折扣设置更难调试，收敛也更敏感。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 R-Learning 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 R-Learning 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于持续控制、排队系统、资源调度和平均回报 RL。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Temporal Difference Learning
- Action Value Function

### 关联
- Q-Learning
- Policy Iteration

### 延伸
- Q-Learning
- Policy Iteration

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
