---
id: article-multi-armed-bandit
slug: multi-armed-bandit
title: Multi-Armed Bandit：概念、直觉与边界
concepts:
- multi-armed-bandit
learning_units:
- multi-armed-bandit-overview
domain: reinforcement_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Multi-Armed Bandit
- bandit
- channel allocation
- reinforcement learning
- beginner
- probability
- exploration exploitation
- epsilon greedy policy
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
  id: article-plan-multi-armed-bandit
  covered_concepts: 1
  primary_concept: multi-armed-bandit
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Multi-Armed Bandit：概念、直觉与边界

只有动作选择和奖励反馈、没有复杂状态转移的决策问题。

关键词：Multi-Armed Bandit
- bandit
- channel allocation
- reinforcement learning
- beginner
- probability
- exploration exploitation
- epsilon greedy policy

## 为什么需要它

推荐和实验分流常需要边试边选。bandit 提供了简化决策模型。

## 核心直觉

- 输入：Multi-Armed Bandit 所处理的数据、状态或评价对象。
- 操作：核心是探索和利用权衡。常见方法包括 epsilon-greedy 和 UCB。
- 观察结果：推荐和实验分流常需要边试边选。bandit 提供了简化决策模型。

它像面对多台老虎机。每台回报未知，要边玩边判断哪台更好。

例子：在线广告可以在多个候选文案间分配流量。

## 数学定义

### 表达方式

`目标是最大化累计奖励或最小化 regret`

此处保留 Multi-Armed Bandit 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Multi-Armed Bandit 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Multi-Armed Bandit 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Multi-Armed Bandit 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- bandit 不是完整 MDP。它通常没有状态转移链。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Multi-Armed Bandit 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Multi-Armed Bandit 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于推荐、A/B 测试和在线学习。延迟反馈会增加难度。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability
- Exploration and Exploitation

### 关联
- Epsilon-Greedy Policy

### 延伸
- Epsilon-Greedy Policy

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
