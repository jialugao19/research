---
id: article-off-policy-learning
slug: off-policy-learning
title: Off-Policy Learning：概念、直觉与边界
concepts:
- off-policy-learning
learning_units:
- off-policy-learning-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Off-Policy Learning
- off-policy
- reinforcement learning
- intermediate
- q learning
- replay buffer
- sarsa
- deep q network
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
  id: article-plan-off-policy-learning
  covered_concepts: 1
  primary_concept: off-policy-learning
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Off-Policy Learning：概念、直觉与边界

用一种行为策略产生的数据来学习另一种目标策略的方法。

关键词：Off-Policy Learning
- off-policy
- reinforcement learning
- intermediate
- q learning
- replay buffer
- sarsa
- deep q network

## 为什么需要它

收集数据的策略不一定是最终想要优化的策略。off-policy 学习允许复用旧经验。

## 核心直觉

- 输入：Off-Policy Learning 所处理的数据、状态或评价对象。
- 操作：行为策略负责采样。目标策略负责被评估或改进。
- 观察结果：收集数据的策略不一定是最终想要优化的策略。off-policy 学习允许复用旧经验。

它像从别人走过的路线中学习自己的路线。

例子：经验回放中的旧样本可能来自较早策略，但仍用于更新当前 Q 网络。

## 数学定义

### 表达方式

`Q-learning 是常见 off-policy 方法`

此处保留 Off-Policy Learning 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Off-Policy Learning 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Off-Policy Learning 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Off-Policy Learning 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- off-policy 不等于一定更稳定。分布差异会带来估计风险。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Off-Policy Learning 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Off-Policy Learning 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 Q-learning、DQN 和离线强化学习。重要性采样常用于校正差异。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Q-Learning
- Replay Buffer

### 关联
- SARSA
- Deep Q-Network

### 延伸
- SARSA
- Deep Q-Network

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
